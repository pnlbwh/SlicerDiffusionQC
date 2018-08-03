#!/usr/bin/env python-real

import sys, subprocess, os

# TODO: Make path/to/Anaconda/Python automatically discoverable

# Windows
# command= [r"C:\ProgramData\Anaconda3\python", os.path.join(os.path.dirname(__file__), "diffusionQC_real.py")] \
#           + sys.argv[1:]

# Linux
command= [r"/home/pnl/anaconda3/bin/python", os.path.join(os.path.dirname(__file__), "diffusionQC_real.py")] \
           + sys.argv[1:]

env = dict(filter(lambda x: not x[0].startswith("PYTHON") or x[0].startswith("LD_"), os.environ.iteritems()))
subprocess.Popen(command, env=env)
