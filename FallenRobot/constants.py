# FallenRobot/constants.py
import os

ALLOW_EXCL = bool(os.environ.get("ALLOW_EXCL", False))
LOAD = os.environ.get("LOAD", "").split()
NO_LOAD = os.environ.get("NO_LOAD", "").split()