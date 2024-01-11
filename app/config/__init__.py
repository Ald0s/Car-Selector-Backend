"""Still using this class, haha.
https://www.toptal.com/flask/flask-production-recipes"""

import os
import sys
import logging

from . import settings


# create settings object corresponding to specified env
APP_ENV = os.environ.get("APP_ENV", "Development")
_current = getattr(sys.modules["app.config.settings"], "{0}Config".format(APP_ENV))()


if APP_ENV == "Production":
    logging.basicConfig( level = logging.INFO )

elif APP_ENV == "Test" or APP_ENV == "Development":
    logging.basicConfig( level = logging.DEBUG )

# copy attributes to the module for convenience
for atr in [f for f in dir(_current) if not "__" in f]:
    # environment can override anything
    val = os.environ.get(atr, getattr(_current, atr))
    setattr(sys.modules[__name__], atr, val)


def as_dict():
    res = {}
    for atr in [f for f in dir(_current) if not "__" in f]:
        val = getattr(_current, atr)
        res[atr] = val
    return res
