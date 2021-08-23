import unittest
from valvesmd import *


class SmdParseTypeTestCase(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def testSmdtypes(self):
        smd = SmdParse('tests/smds/stairs001.smd')
        # Smd
        self.assertIsInstance(smd.version, int)
        self.assertIsInstance(smd.nodes, list)
        self.assertIsInstance(smd.skeleton, list)
        self.assertIsInstance(smd.triangles, list)

        self.assertIsInstance(smd.nodes[0], SmdNode)
        self.assertIsInstance(smd.skeleton[0], SmdKeyframe)
        self.assertIsInstance(smd.triangles[0], SmdTriangle)

        # SmdNode
        self.assertIsInstance(smd.nodes[0].id, int)
        self.assertIsInstance(smd.nodes[0].parent_id, int)
        self.assertIsInstance(smd.nodes[0].name, str)
        self.assertEqual(smd.nodes[0].name, 'Brush001')

        # SmdSkeleton
        self.assertIsInstance(smd.skeleton[0].frame, int)
        self.assertIsInstance(smd.skeleton[0].poses, list)
        self.assertIsInstance(smd.skeleton[0].poses[0], SmdBonePose)

        # SmdBonePose
        pose = smd.skeleton[0].poses[0]
        self.assertIsInstance(pose.boneid, int)
        self.assertIsInstance(pose.position, tuple)
        self.assertIsInstance(pose.position[0], float)
        self.assertIsInstance(pose.rotation, tuple)
        self.assertIsInstance(pose.rotation[0], float)
        self.assertEqual(pose.position[0], -44.4444)
        self.assertEqual(pose.rotation[0], 0)

        # SmdTriangle
        self.assertIsInstance(smd.triangles[0].material, str)
        self.assertIsInstance(smd.triangles[0].verts, tuple)

        # SmdVert
        vert = smd.triangles[0].verts[0]
        self.assertIsInstance(vert, SmdVert)
        self.assertIsInstance(vert.parent_boneid, int)
        self.assertIsInstance(vert.position, tuple)
        self.assertIsInstance(vert.position[0], float)
        self.assertIsInstance(vert.normal, tuple)
        self.assertIsInstance(vert.normal[0], float)
        self.assertIsInstance(vert.uv, tuple)
        self.assertIsInstance(vert.uv[0], float)
        self.assertIsInstance(vert.links, list)
        self.assertIsInstance(vert.links[0], SmdLink)

        # SmdLink
        link = vert.links[0]
        self.assertIsInstance(link.boneid, int)
        self.assertIsInstance(link.weight, float)
