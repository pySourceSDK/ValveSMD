from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import dict
from builtins import open
from builtins import int
from future import standard_library
standard_library.install_aliases()

import os  # NOQA: E402
from pyparsing import *  # NOQA: E402
from valvesmd.smd import *  # NOQA: E402


def asTuple(data):
    data[0] = tuple(data[0])
    return data


def asDict(data):
    return {k: v[0] if isinstance(v, list) else v for (k, v) in data[0].items()}


pp_comment = Literal('//') + SkipTo(lineEnd)
pp_int = Word(nums+'-').setParseAction(lambda toks: int(toks[0]))
pp_float = Word(nums+'-.').setParseAction(lambda toks: float(toks[0]))

pp_version = Suppress(ZeroOrMore(pp_comment)) + \
    Suppress(CaselessLiteral('version')) + Word(nums)
pp_version.setResultsName('version')


# Triangles
pp_material = Word(printables)
pp_material = pp_material.setResultsName('material')

pp_pbone = pp_int.setResultsName('parent_boneid')

pp_pos = Group(pp_float + pp_float + pp_float)
pp_pos = pp_pos.setResultsName('position').setParseAction(asTuple)

pp_norm = Group(pp_float + pp_float + pp_float)
pp_norm = pp_norm.setResultsName('normal').setParseAction(asTuple)

pp_uv = Group(pp_float + pp_float)
pp_uv = pp_uv.setResultsName('uv').setParseAction(asTuple)

pp_vert = Group(pp_pbone + pp_pos + pp_norm + pp_uv)
pp_vert = pp_vert.setParseAction(lambda v: SmdVert(asDict(v)))

pp_tri = pp_vert + pp_vert + pp_vert
pp_tri = pp_tri.setResultsName('verts')

pp_triangle = Group(pp_material + pp_tri)
pp_triangle.addParseAction(lambda t: SmdTriangle(asDict(t)))

pp_triangles = Suppress('triangles') + ZeroOrMore(pp_triangle) + Suppress('end')
pp_triangles = pp_triangles.setResultsName('triangles')

# Nodes
pp_nid = pp_int.setResultsName('id')
pp_nname = QuotedString('"').setResultsName('name')
pp_nparent_id = pp_int.setResultsName('parent_id')

pp_node = pp_nid + pp_nname + pp_nparent_id
pp_node = pp_node.setParseAction(lambda n: SmdNode(n.asDict()))

pp_nodes = Suppress('nodes') + ZeroOrMore(pp_node) + Suppress('end')
pp_nodes = pp_nodes.setResultsName('nodes')

# Skeleton
pp_framedef = Suppress('time') + pp_int.setResultsName('frame')

pp_sbid = pp_int.setResultsName('boneid')

pp_spos = Group(pp_float + pp_float + pp_float)
pp_spos = pp_norm.setResultsName('position').setParseAction(asTuple)

pp_srot = Group(pp_float + pp_float + pp_float)
pp_srot = pp_norm.setResultsName('rotation').setParseAction(asTuple)

pp_bonepose = Group(pp_sbid + pp_spos + pp_srot)
pp_bonepose = pp_bonepose.setParseAction(lambda p: SmdBonePose(asDict(p)))

pp_boneposes = ZeroOrMore(pp_bonepose)
pp_boneposes = pp_boneposes.setResultsName('poses')

pp_keyframe = Group(pp_framedef + pp_boneposes)
pp_keyframe = pp_keyframe.setParseAction(lambda k: SmdKeyframe(asDict(k)))

pp_skeleton = Suppress('skeleton') + ZeroOrMore(pp_keyframe) + Suppress('end')
pp_skeleton = pp_skeleton.setResultsName('skeleton')

pp_smd = pp_version + Optional(pp_nodes) + Optional(pp_skeleton) + \
    Optional(pp_triangles)
pp_smd.setParseAction(lambda s: Smd(s.asDict()))


def SmdParse(filename):
    filepath = os.path.abspath(filename)
    filedir = os.path.dirname(filepath)

    results = []
    try:
        f = open(filename, "r", encoding="iso-8859-1")
        results = pp_smd.ignore(cStyleComment).parseFile(f)
        f.close()
    except Exception as e:
        raise

    if len(results):
        return results[0]
    else:
        # parse failure
        pass
