from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import map
from builtins import range
from builtins import int
from future import standard_library
standard_library.install_aliases()
import math
import numbers
from operator import mul


AXIS = ['x', 'y', 'z']


def SmdMirror(smd, axis='x'):
    try:
        axis = AXIS.index(axis)
    except:
        raise ValueError(
            "ValueError: Expected mirror axis to be either 'x', 'y' or 'z'")

    transform = (-1 if axis == 'x' else 1,
                 -1 if axis == 'y' else 1,
                 -1 if axis == 'z' else 1)

    for vert in [v for t in smd.triangles for v in t.verts]:
        vert.position = tuple(map(mul, vert.position, transform))
        vert.normal = tuple(map(mul, vert.normal, transform))

    for pose in [p for s in smd.skeleton for p in s.poses]:
        pose.position = tuple(map(mul, pose.position, transform))
        pose.rotation = tuple(map(mul, pose.rotation, transform))

    SmdFlipNormal(smd)


def SmdFlipNormal(smd):
    for tri in smd.triangles:
        tri.verts = (tri.verts[2], tri.verts[1], tri.verts[0])


def SmdScale(smd, scale=(1, 1, 1)):
    if isinstance(scale, numbers.Number):
        scale = (scale, scale, scale)
    elif hasattr(scale, '__len__') and len(scale) == 3:
        scale = tuple(scale)
    else:
        raise ValueError(
            "ValueError: Expected scale factor as a tuple (x,y,z)")

    for vert in [v for t in smd.triangles for v in t.verts]:
        vert.position = tuple([vert.position[x] * scale[x]
                               for x in range(len(AXIS))])
        vert.normal = tuple([vert.normal[x] * scale[x]
                             for x in range(len(AXIS))])

    for pose in [p for s in smd.skeleton for p in s.poses]:
        pose.position = tuple([pose.position[x] * scale[x]
                               for x in range(len(AXIS))])


def SmdTranslate(smd, delta=(0, 0, 0)):
    if hasattr(delta, '__len__') and len(delta) == 3:
        delta = tuple(delta)
    else:
        raise ValueError(
            "ValueError: Expected translation value as a tuple (x,y,z)")

    for vert in [v for t in smd.triangles for v in t.verts]:
        vert.position = tuple([vert.position[x] + delta[x]
                               for x in range(len(AXIS))])

    for pose in [p for s in smd.skeleton for p in s.poses]:
        pose.position = tuple([pose.position[x] + delta[x]
                               for x in range(len(AXIS))])


def SmdClean(smd):
    unclean_mats = ['TOOLSNODRAW']
    smd.triangles = [t for t in smd.triangles if t.material not in unclean_mats]
    # remove unused nodes
    # remove unused keyframes


def SmdMatReplace(smd, original, replacement):
    for triangle in [t for t in smd.triangles if t.material == original]:
        triangle.material = replacement
