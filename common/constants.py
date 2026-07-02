"""
Application constants.
"""

from config.config import settings

if settings.debug:
    print("--> Entering: constants.py")

APP_NAME = "Enterprise AI Gateway (EAIG)"
VERSION = "1.0"
LINE = "=" * 80
SUB_LINE = "-" * 80

if settings.debug:
    print("<-- Exiting : constants.py")
