# filepath: src/services/sms.py

"""SMS delivery behind a Twilio-shaped seam.

Two backends:
- MockTwilioBackend (default): mimics Twilio's Messages API semantics —
  validates inputs, returns an SM... sid, records to an outbox (tests read
  it), logs the body instead of sending. Costs nothing.
- TwilioBackend: the real thing via Twilio's REST API (plain httpx with
  basic auth — no SDK dependency). Activated by SMS_BACKEND=twilio plus
  credentials; switching is a config change only.
"""

import logging
import secrets
import string
from dataclasses import dataclass

import httpx

from config import settings

logger = logging.getLogger(__name__)


class SmsDeliveryError(Exception):
    pass


@dataclass
class SentSms:
    sid: str
    to: str
    body: str


class MockTwilioBackend:
    """Twilio Messages API lookalike that never leaves the process."""

    outbox: list[SentSms] = []  # class-level so tests can inspect deliveries

    def send(self, to: str, body: str) -> str:
        if not to.startswith("+"):
            # Twilio rejects non-E.164 numbers with error 21211; so do we.
            raise SmsDeliveryError(f"Invalid 'To' phone number: {to}")
        sid = "SM" + "".join(secrets.choice(string.hexdigits.lower()) for _ in range(32))
        self.outbox.append(SentSms(sid=sid, to=to, body=body))
        logger.info("SMS (mock twilio) sid=%s to=%s body=%r", sid, to, body)
        return sid

    @classmethod
    def reset(cls) -> None:
        cls.outbox.clear()


class TwilioBackend:
    """Real Twilio Messages API. https://api.twilio.com/2010-04-01"""

    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self._sid = account_sid
        self._auth = (account_sid, auth_token)
        self._from = from_number

    def send(self, to: str, body: str) -> str:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self._sid}/Messages.json"
        try:
            r = httpx.post(
                url,
                auth=self._auth,
                data={"To": to, "From": self._from, "Body": body},
                timeout=15.0,
            )
        except httpx.HTTPError as e:
            raise SmsDeliveryError(f"Twilio unreachable: {e}") from None
        if r.status_code >= 400:
            raise SmsDeliveryError(f"Twilio error {r.status_code}: {r.text[:200]}")
        return r.json()["sid"]


def get_sms_backend():
    if settings.SMS_BACKEND == "twilio":
        if not all(
            (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_FROM_NUMBER)
        ):
            raise SmsDeliveryError(
                "SMS_BACKEND=twilio but TWILIO_ACCOUNT_SID/AUTH_TOKEN/FROM_NUMBER are not all set"
            )
        return TwilioBackend(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
            settings.TWILIO_FROM_NUMBER,
        )
    return MockTwilioBackend()
