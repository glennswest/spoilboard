#!/usr/bin/env python3
"""Copy the stick-ready spoilboard files into /Volumes/MASSO/spoilboard/."""
import glob
import os
import shutil
import subprocess
import sys

STICK, SUB = "/Volumes/MASSO", "spoilboard"
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
if not os.path.isdir(STICK):
    sys.exit("MASSO stick not mounted")
d = os.path.join(STICK, SUB)
os.makedirs(d, exist_ok=True)
for f in glob.glob(os.path.join(d, "*.nc")) \
        + glob.glob(os.path.join(d, "._*")):
    try:
        os.remove(f)
    except FileNotFoundError:
        pass
n = 0
for f in sorted(glob.glob(os.path.join(src, "*.nc"))):
    shutil.copyfile(f, os.path.join(d, os.path.basename(f)))
    n += 1
subprocess.run(["dot_clean", "-m", STICK], capture_output=True)
for f in glob.glob(os.path.join(d, "._*")):
    try:
        os.remove(f)
    except FileNotFoundError:
        pass
print(f"{SUB}: {n} nc files -> {d}")
