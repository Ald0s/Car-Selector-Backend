import os
import sys

from dotenv import load_dotenv

from . import settings

# Get the app environment, by default use Development.
APP_ENV = os.getenv('APP_ENV', 'Development')

# For app environment, get the matching configuration class from settings.
try:
    # Get the current configuration.
    _current_config = settings.__dict__[f"{APP_ENV}Config"]
except AttributeError as ae:
    # This configuration doesn't exist. Fallback to development and report
    # the issue.
    print(f"WARNING! While loading settings for module {__name__}, we were" \
          " unable to locate the desired environment; '{APP_ENV}', fallback" \
          " to Development.")
    try:
        _current_config = settings.__dict__[f"DevelopmentConfig"]
    except AttributeError as ae2:
        # Just give up, mate.
        raise NotImplementedError

# copy attributes to the module for convenience
for atr in [f for f in dir(_current_config) if not "__" in f]:
    # Load .env settings.
    load_dotenv()
    # environment can override anything, as long as it is not Test; in which
    # settings configuration takes priority.
    if APP_ENV == "Test":
        val = getattr(_current_config, atr) or os.environ.get(atr, None)
    else:
        val = os.environ.get(atr, getattr(_current_config, atr))
    setattr(sys.modules[__name__], atr, val)