from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()


def SmdWrite(smd, filename):

    smd_text = smd.smd_str()

    f = open(filename, "w")
    f.write(smd_text)
    f.close()
