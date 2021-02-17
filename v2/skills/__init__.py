# This code adds the package to the path. NEEDED if package modules import each other.
# Also makes package modules importable in the original scope. Could be a potential naming issue.
# Using relative paths internally in the package is the way to avoid this; but that makes internal modules
# unable to be run as main. 

import sys
import os

sys.path.append(os.path.dirname(__file__))

# This lets one use package.module imports. Importing the package itself will do nothing.

__all__ = ['parser', 'commands']

# This makes the below modules available when importing the package itself; import package. 

import parser
import commands