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
    return [tuple(data.asList()[0])]


def asList(data):
    return list(data.asList())


def asDict(data):
    return {k: value(v) for k, v in data.items()}


def value(val):
    if isinstance(val, ParseResults):
        while isinstance(val[0], ParseResults):
            val = val[0]
        if isinstance(val[0], tuple):
            return val[0]
        return val.asList() or val.asDict() or val[0]
    return val


pp_comment = Literal('//') + SkipTo(lineEnd)
pp_int = Word(nums+'-').setParseAction(lambda toks: int(toks[0]))
pp_float = Word(nums+'-.').setParseAction(lambda toks: float(toks[0]))
pp_float2 = Group(pp_float * 2).setParseAction(asTuple)
pp_float3 = Group(pp_float * 3).setParseAction(asTuple)

# Version
pp_version = Suppress(ZeroOrMore(pp_comment)) + \
    Suppress(CaselessLiteral('version')) + pp_int('version')

# Triangles
pp_link = Group(pp_int('boneid') + pp_float('weight'))
pp_link.setParseAction(lambda l: SmdLink(asDict(l[0])))
pp_links = countedArray(pp_link)('links')

pp_vert_base = pp_int('parent_boneid') + pp_float3('position') + \
    pp_float3('normal') + pp_float2('uv')
pp_vert_base.setParseAction(lambda v: SmdVert(asDict(v)))

pp_vert_extended = pp_int('parent_boneid') + pp_float3('position') + \
    pp_float3('normal') + pp_float2('uv') + pp_links
pp_vert_extended.setParseAction(lambda v: SmdVert(asDict(v)))

pp_verts_base = Group(pp_vert_base * 3).setParseAction(asTuple)
pp_verts_extended = Group(pp_vert_extended * 3).setParseAction(asTuple)
pp_verts = pp_verts_extended('verts') ^ pp_verts_base('verts')

pp_triangle = Group(Word(printables+' ')('material') + pp_verts('verts'))
pp_triangle.addParseAction(lambda t: SmdTriangle(asDict(t[0])))

pp_triangles = Group(Suppress('triangles') + ZeroOrMore(pp_triangle) +
                     Suppress('end'))('triangles').setParseAction(asList)

# Nodes
pp_node = pp_int('id') + QuotedString('"')('name') + pp_int('parent_id')
pp_node.setParseAction(lambda n: SmdNode(asDict(n)))
pp_nodes = Group(Suppress('nodes') + ZeroOrMore(pp_node) +
                 Suppress('end'))('nodes').setParseAction(asList)

# Skeleton
pp_bonepose = pp_int('boneid') + pp_float3('position') + pp_float3('rotation')
pp_bonepose.setParseAction(lambda p: SmdBonePose(asDict(p)))
pp_boneposes = Group(ZeroOrMore(pp_bonepose))('poses').setParseAction(asList)

pp_keyframe = Suppress('time') + pp_int('frame') + pp_boneposes
pp_keyframe.setParseAction(lambda k: SmdKeyframe(asDict(k)))

pp_skeleton = Group(Suppress('skeleton') + ZeroOrMore(pp_keyframe) +
                    Suppress('end'))('skeleton').setParseAction(asList)

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
