from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import round
from builtins import int
from builtins import next
from builtins import str
from builtins import object
from future import standard_library
from collections import OrderedDict
standard_library.install_aliases()


class Smd(object):
    def __init__(self, data={}):
        """Creates an empty instance of Smd."""
        self.version = 1
        self.nodes = data.get('nodes', [])
        self.skeleton = data.get('skeleton', [])
        self.triangles = data.get('triangles', [])

    def smd_str(self):
        ret_str = 'version ' + str_int(self.version) + '\n'
        ret_str += 'nodes\n'
        for node in self.nodes:
            ret_str += node.smd_str() + '\n'
        ret_str += 'end\n'
        ret_str += 'skeleton\n'
        for keyf in self.skeleton:
            ret_str += keyf.smd_str() + '\n'
        ret_str += 'end\n'
        ret_str += 'triangles\n'
        for tri in self.triangles:
            ret_str += tri.smd_str() + '\n'
        ret_str += 'end\n'
        return ret_str


class SmdNode(object):
    def __init__(self, data={}):
        self.id = data.get('id', -1)
        self.name = data.get('name', 'root')
        self.parent_id = data.get('parent_id', -1)

    def smd_str(self):
        node_str = str_int(self.id)
        node_str += ' "' + self.name + '" '
        node_str += str_int(self.parent_id)
        return node_str


class SmdKeyframe(object):
    def __init__(self, data={}):
        self.frame = data.get('frame', 0)
        self.poses = data.get('poses', [])

    def smd_str(self):
        key_str = 'time ' + str_int(self.frame) + '\n'
        for p in self.poses:
            key_str += p.smd_str() + '\n'
        return key_str.strip()


class SmdBonePose(object):
    def __init__(self, data={}):
        self.boneid = data.get('boneid', '-1')
        self.position = data.get('position', (0, 0, 0))
        self.rotation = data.get('rotation', (0, 0, 0))

    def smd_str(self):
        key_str = str_int(self.boneid) + ' '
        for c in self.position:
            key_str += str_float(c, 6) + ' '
        for c in self.rotation:
            key_str += str_float(c, 6) + ' '
        return key_str.strip()


class SmdTriangle(object):

    def __init__(self, data={}):
        self.material = data.get('material', 'undefined')
        self.verts = data.get('verts', (None, None, None))

    def smd_str(self):
        tri_str = self.material + '\n'
        for v in self.verts:
            tri_str += v.smd_str() + '\n'
        return tri_str.strip()


class SmdVert(object):
    def __init__(self, data={}):
        self.parent_boneid = data.get('parent_boneid', -1)
        self.position = data.get('position', (None, None, None))
        self.normal = data.get('normal', (None, None, None))
        self.uv = data.get('uv', (None, None))

        self.links = data.get('links', None)
        self.boneid = data.get('boneid', None)
        self.weight = data.get('weight', None)

    def smd_str(self):
        vert_str = str_int(self.parent_boneid) + ' '
        for c in self.position:
            vert_str += str_float(c, 8, True) + ' '
        for c in self.normal:
            vert_str += str_float(c, 8) + ' '
        for c in self.uv:
            vert_str += str_float(c, 8) + ' '
        if self.links is not None:
            vert_str += str_int(self.links) + ' '
        if self.boneid is not None:
            vert_str += str_int(self.boneid) + ' '
        if self.weight is not None:
            vert_str += str_float(self.weight, 8, True) + ' '
        return vert_str.strip()


def str_int(number):
    return str(int(number))


def str_float(number, decimals=8, force=False):
    if force:
        return ("{0:."+str(decimals)+"f}").format(number)
    elif number % 1:
        return str(round(number, decimals))
    else:
        return str_int(number)
