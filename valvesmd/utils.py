from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import int
from future import standard_library
standard_library.install_aliases()
import math
import numbers

AXIS = ['x', 'y', 'z']


def _cardinal(n):
    return int((n != 0) * math.copysign(1, n))


def mirrorSmd(smd, axis='x'):
    try:
        axis = AXIS.index(axis)
    except:
        raise

    for vert in [v for t in smd.triangles for v in t.verts]:
        vert.position[axis] = vert.position[axis] * -1
        vert.normal[axis] = vert.normal[axis] * -1

    for tri in smd.triangles:
        tri.verts = (tri.verts[2], tri.verts[1], tri.verts[0])


def scaleSmd(smd, scale=(1, 1, 1)):
    if isinstance(scale, numbers.Number):
        scale = (scale, scale, scale)
    elif hasattr(scale, '__len__') and len(scale) == 3:
        scale = tuple(scale)
    else:
        raise ValueError

    for vert in [v for t in smd.triangles for v in t.verts]:
        vert.position = tuple([vert.position[x] * scale[x]
                               for x in range(len(AXIS))])
        vert.normal = tuple([vert.normal[x] * scale[x]
                             for x in range(len(AXIS))])


def translateSmd(smd, delta=(0, 0, 0)):
    pass


def cleanSmd(smd):
    unclean_mats = ['TOOLSNODRAW']
    smd.triangles = [t for t in smd.triangles if t.material not in unclean_mats]
    # remove unused nodes
    # remove unused keyframes


def matReplaceSmd(smd, original, replacement):
    for triangle in [t for t in smd.triangles if t.material == original]:
        triangle.material = replacement
