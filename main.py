"""
Enterprise AI Gateway (EAIG)

Feature 01
Project Bootstrap
"""

from common.console import title
from config.config import settings

if settings.debug:
    print("--> Entering main")

title(
    "Enterprise AI Gateway (EAIG)\n"
    "Feature 01 - Prompt Injection Detection"
)

print()
print("Framework initialized successfully.")
print()
print("Next step: Prompt Injection Detector")
if settings.debug:
    print("<-- Exiting main")
