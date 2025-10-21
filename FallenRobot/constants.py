from os import environ

LOAD = environ.get("LOAD", "").split()
NO_LOAD = environ.get("NO_LOAD", "").split()