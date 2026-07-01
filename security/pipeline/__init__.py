"""
Pipeline package.
"""

#                     User Input
#                          │
#                          ▼
#         ┌─────────────────────────────────────┐
#         │      Enterprise Security Pipeline   │
#         └─────────────────────────────────────┘
#                          │
#         ┌────────────────┼────────────────┐
#         ▼                ▼                ▼
#  Prompt Injection      PII           Secrets
#         │                │                │
#         └────────────┬───┴────────────────┘
#                      ▼
#              Confidential Data
#                      │
#                      ▼
#             Policy Decision Engine
#                      │
#         ┌────────────┴─────────────┐
#         ▼                          ▼
#       BLOCK                 SANITIZE
#                                      │
#                                      ▼
#                               Safe Prompt