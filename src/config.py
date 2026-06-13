# filepath: src/config.py

import sys
from pathlib import Path

from pydantic import ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent


class Settings(BaseSettings):
    """All configuration. The only place environment variables are read."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    SECRET_KEY: str
    # Shared secret for the bot -> API trust bridge (/auth/telegram).
    # None disables the endpoint.
    BOT_BRIDGE_SECRET: str | None = None
    DATABASE_URL: str = f"sqlite:///{SRC_DIR / 'db' / 'data' / 'crowdjump.db'}"
    ACCESS_TOKEN_MINUTES: int = 30
    REFRESH_TOKEN_DAYS: int = 14
    EMAIL_TOKEN_HOURS: int = 48
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"
    # --- Telegram bot (separate process; the bot is a pure API client) ---
    BOT_TOKEN: str | None = None
    API_BASE_URL: str = "http://localhost:8000"
    TG_FILE_LIMIT_MB: int = 20  # standard Bot API download cap; raise after self-hosting
    # Proof uploads stay stubbed until the verification component lands.
    PROOF_UPLOAD_ENABLED: bool = False

    # --- email delivery ---
    EMAIL_BACKEND: str = "console"  # "console" (log only) | "smtp"
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_FROM: str | None = None  # defaults to SMTP_USER
    PUBLIC_BASE_URL: str = "http://localhost:8000"  # used in emailed links

    # --- SMS / phone verification ---
    SMS_BACKEND: str = "mock"  # "mock" (Twilio-shaped, logs) | "twilio"
    TWILIO_ACCOUNT_SID: str | None = None
    TWILIO_AUTH_TOKEN: str | None = None
    TWILIO_FROM_NUMBER: str | None = None
    SMS_CODE_TTL_MINUTES: int = 10
    SMS_RESEND_COOLDOWN_SECONDS: int = 60
    SMS_MAX_ATTEMPTS: int = 5

    # --- matching + notifications ---
    MATCH_CONFIDENCE_MIN: float = 0.8  # attribute rows below this don't count
    MATCH_NOTIFY_CAP: int = 50  # max Jumpers notified per launch
    AUDIENCE_PRIVACY_FLOOR: int = 10  # below this, preview says "fewer than N"
    BROWSE_SCAN_LIMIT: int = 200  # open tasks scanned for the eligible feed
    NOTIFY_BACKEND: str = "console"  # "console" (log) | "telegram" (real sends)

    # --- clarifier (task-consumer LLM; devdocs/scoped/be/clarifier/bom.md) ---
    # "off" = clients use today's direct launch flow; "mock" = deterministic
    # catalog-shaped backend (the MVP product, keyless); "real" = LLM API.
    CLARIFIER_BACKEND: str = "off"
    CLARIFIER_API_KEY: str | None = None  # required when CLARIFIER_BACKEND="real"
    CLARIFIER_MODEL: str | None = None  # vendor model id; required when "real"
    # Knobs mirror task_consumer_catalog.md §4 provisional constants — every
    # value below is uncalibrated until ~100 real submissions exist.
    CLARIFIER_MIN_TASK_CHARS: int = 12  # CJ-X3 code half
    CLARIFIER_QUESTION_CAP: int = 3  # blocking questions per card (§5)
    CLARIFIER_RUNS_PER_USER_PER_HOUR: int = 20  # token-abuse guard (429 beyond)
    # Drafts persist indefinitely at MVP; retention POLICY is open (PII posture,
    # finding's T7). The knob ships so enabling cleanup is config, not code.
    CLARIFIER_DRAFT_TTL_DAYS: int | None = None
    # Operator gate for CJ-K3 holds — no admin/roles component exists yet;
    # these user ids may resolve held drafts. Migrates to real roles later.
    OPERATOR_USER_IDS: list[int] = []
    # Per-row kill-switch (ToS matrix v1, ratified): a listed tos_category is
    # gated instantly — incident playbook step 1. E.g. ["engagement"].
    CLARIFIER_TOS_KILLED_ROWS: list[str] = []
    # Mock-backend latency injection (ms) for the slow-backend simulation (§8).
    CLARIFIER_MOCK_LATENCY_MS: int = 0

    @model_validator(mode="after")
    def _clarifier_real_needs_credentials(self) -> "Settings":
        if self.CLARIFIER_BACKEND == "real" and not (
            self.CLARIFIER_API_KEY and self.CLARIFIER_MODEL
        ):
            raise ValueError(
                "CLARIFIER_BACKEND='real' requires CLARIFIER_API_KEY and CLARIFIER_MODEL"
            )
        return self

    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:8080",
    ]


try:
    settings = Settings()
except ValidationError as e:
    _missing = ", ".join(str(err["loc"][0]) for err in e.errors())
    sys.exit(
        f"Configuration error — missing or invalid: {_missing}. "
        "Copy .env.example to .env and fill in the values."
    )
