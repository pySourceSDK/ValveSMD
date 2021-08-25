from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str
from builtins import range
from builtins import dict
from builtins import open
from builtins import int
from future import standard_library
standard_library.install_aliases()

import os  # NOQA: E402
from pyparsing import *  # NOQA: E402
from valvesmd.smd import *  # NOQA: E402


def asTuple(data):
    return tuple(data.asList()[0])


def asList(data):
    return list(data.asList())


def asDict(data):
    keys = [v for v in data.keys()]
    if len(data) == len(keys):
        return {keys[i]: value(data[i]) for i in range(len(keys))}
    else:
        return {k: value(data[k]) for k in keys}


def value(val):
    if isinstance(val, ParseResults):
        return val.asList() or val.asDict() or val
    return val


pp_comment = Literal('//') + SkipTo(lineEnd)
pp_int = Word(nums+'-').setParseAction(lambda toks: int(toks[0]))
pp_float = Word(nums+'-.').setParseAction(lambda toks: float(toks[0]))

pp_version = Suppress(ZeroOrMore(pp_comment)) + \
    Suppress(CaselessLiteral('version')) + Word(nums)
pp_version.setResultsName('version')


# Triangles
pp_material = Word(printables+' ')
pp_material = pp_material.setResultsName('material')

pp_pbone = pp_int.setResultsName('parent_boneid')

pp_pos = Group(pp_float + pp_float + pp_float)
pp_pos = pp_pos.setResultsName(
    'position').setParseAction(asTuple)

pp_norm = Group(pp_float + pp_float + pp_float)
pp_norm = pp_norm.setResultsName('normal').setParseAction(asTuple)

pp_uv = Group(pp_float + pp_float)
pp_uv = pp_uv.setResultsName('uv').setParseAction(asTuple)

pp_boneid = pp_int.setResultsName('boneid')
pp_weight = pp_float.setResultsName('weight')

pp_link = Group(pp_boneid + pp_weight)
pp_link = pp_link.setParseAction(lambda l: SmdLink(asDict(l[0])))

pp_links = countedArray(pp_link)
pp_links = pp_links.setResultsName('links')

pp_vert_base = pp_pbone + pp_pos + pp_norm + pp_uv
pp_vert_base.setParseAction(lambda v: SmdVert(asDict(v)))

pp_vert_extended = pp_pbone + pp_pos + pp_norm + pp_uv + pp_links
pp_vert_extended.setParseAction(lambda v: SmdVert(asDict(v)))

pp_verts_base = Group(
    pp_vert_base + pp_vert_base + pp_vert_base)
pp_verts_extended = Group(
    pp_vert_extended + pp_vert_extended + pp_vert_extended)
pp_verts_base.setParseAction(asTuple)
pp_verts_extended.setParseAction(asTuple)

pp_verts = pp_verts_extended ^ pp_verts_base
pp_verts = pp_verts.setResultsName('verts')

pp_triangle = Group(pp_material + pp_verts)
pp_triangle.addParseAction(lambda t: SmdTriangle(asDict(t[0])))

pp_triangles = Group(Suppress('triangles') +
                     ZeroOrMore(pp_triangle) + Suppress('end'))
pp_triangles = pp_triangles.setResultsName('triangles')
pp_triangles = pp_triangles.setParseAction(asList)

# Nodes
pp_nid = pp_int.setResultsName('id')
pp_nname = QuotedString('"').setResultsName('name')
pp_nparent_id = pp_int.setResultsName('parent_id')

pp_node = pp_nid + pp_nname + pp_nparent_id
pp_node = pp_node.setParseAction(lambda n: SmdNode(asDict(n)))

pp_nodes = Group(Suppress('nodes') + ZeroOrMore(pp_node) + Suppress('end'))
pp_nodes = pp_nodes.setResultsName('nodes')
pp_nodes = pp_nodes.setParseAction(asList)

# Skeleton
pp_framedef = pp_int.setResultsName('frame')

pp_sbid = pp_int.setResultsName('boneid')

pp_spos = Group(pp_float + pp_float + pp_float)
pp_spos = pp_norm.setResultsName('position').setParseAction(asTuple)

pp_srot = Group(pp_float + pp_float + pp_float)
pp_srot = pp_norm.setResultsName('rotation').setParseAction(asTuple)

pp_bonepose = pp_sbid + pp_spos + pp_srot
pp_bonepose = pp_bonepose.setParseAction(lambda p: SmdBonePose(asDict(p)))

pp_boneposes = Group(ZeroOrMore(pp_bonepose))
pp_boneposes = pp_boneposes.setResultsName('poses')
pp_boneposes = pp_boneposes.setParseAction(asList)

pp_keyframe = Suppress('time') + pp_framedef + pp_boneposes
pp_keyframe = pp_keyframe.setParseAction(lambda k: SmdKeyframe(asDict(k)))

pp_skeleton = Group(Suppress('skeleton') +
                    ZeroOrMore(pp_keyframe) + Suppress('end'))
pp_skeleton = pp_skeleton.setResultsName('skeleton')
pp_skeleton = pp_skeleton.setParseAction(asList)


pp_smd = Group(pp_version + pp_nodes + pp_skeleton + pp_triangles)
pp_smd.setParseAction(lambda s: SmdRoot(asDict(s[0])))


class SmdSyntaxError(Exception):
    pass


def SmdParse(filename):
    results = []

    try:
        f = open(filename, "r", encoding="iso-8859-1")
        try:
            results = pp_smd.ignore(cStyleComment).parseFile(f)
            f.close()
        except Exception as e:
            f.close()
            raise
    except Exception as e:
        raise
    return results[0]
