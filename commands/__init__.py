from .core import REFERENCE as core
from .character_sheets import REFERENCE as character_sheets
from .counters import REFERENCE as counters

core.update(character_sheets)
core.update(counters)
REFERENCE = core