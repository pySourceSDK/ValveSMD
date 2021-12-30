from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
from future import standard_library
standard_library.install_aliases()
from valvesmd.classes import *
from valvesmd.parser import SmdParse
from valvesmd.writer import SmdWrite


class Smd(SmdRoot):
    """
    This is the basic class to interact with smd files.
    To interact with the data, consult :py:class:`SmdRoot<SmdRoot>`
    which this class inherits
    """

    def __init__(self, path=None):
        """
        initalize a smd file.

        :param path: The location of the smd file to be parsed
        :type path: str, optional
        """
        self.source_path = path  #: :type: (str) - The location of the parsed file

        super().__init__()

        if self.source_path:
            data = SmdParse(self.source_path)
            self.version = data.version
            self.nodes = data.nodes
            self.skeleton = data.skeleton
            self.triangles = data.triangles

    def save(self, destination=None):
        """Saves the current instance of the Smd. Overwrites original smd file if no destination is provided.

        :param destination: A path (directory + filename) to determine where to save the smd file.
        :type destination: str, optional
        """
        SmdWrite(self, destination or self.source_path)
