from .core import REFERENCE as core
from .character_sheets import REFERENCE as character_sheets
from .counters import REFERENCE as counters

REFERENCE = dict(core)
REFERENCE.update(dict(character_sheets))
REFERENCE.update(dict(counters))