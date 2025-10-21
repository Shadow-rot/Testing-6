# FallenRobot/constants.py
import os

ALLOW_EXCL = bool(os.environ.get("ALLOW_EXCL", True))
LOAD = os.environ.get("LOAD", "").split()
NO_LOAD = os.environ.get("NO_LOAD", "").split()