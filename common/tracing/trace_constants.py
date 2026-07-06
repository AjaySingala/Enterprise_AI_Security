from enum import StrEnum

class TraceOutput(StrEnum):
    NONE = "none"
    CONSOLE = "console"
    LOGGER = "logger"
    LANGSMITH = "langsmith"
    OPENTELEMETRY = "otel"
