"""A teaching example for redacting common secret assignments."""
import logging
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("secure-app")

SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(password|token|api_key)\s*=\s*([^\s&,;]+)"
)


def redact_sensitive_data(message: str) -> str:
    """Redact common key=value patterns; not a complete DLP solution."""
    return SECRET_ASSIGNMENT.sub(r"\1=[REDACTED]", message)


def log_event(event: str) -> None:
    logger.info("%s", redact_sensitive_data(event))


if __name__ == "__main__":
    log_event("login failed for user=alice")
    log_event("token=example-secret password=example-password")
