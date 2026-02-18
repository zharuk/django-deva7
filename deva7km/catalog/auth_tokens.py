from django.conf import settings
from django.core import signing
from django.core.cache import cache

TOKEN_SALT = 'seller-cabinet-telegram-auth'
DEFAULT_TOKEN_TTL_SECONDS = 300


class TelegramAuthTokenError(Exception):
    """Raised when telegram auth token is invalid, expired, or already used."""


def create_telegram_auth_token(telegram_id):
    signer = signing.TimestampSigner(salt=TOKEN_SALT)
    return signer.sign(str(telegram_id))


def consume_telegram_auth_token(token):
    signer = signing.TimestampSigner(salt=TOKEN_SALT)
    max_age = getattr(settings, 'TELEGRAM_AUTH_TOKEN_TTL_SECONDS', DEFAULT_TOKEN_TTL_SECONDS)

    try:
        telegram_id_raw = signer.unsign(token, max_age=max_age)
        telegram_id = int(telegram_id_raw)
    except (signing.BadSignature, ValueError) as exc:
        raise TelegramAuthTokenError('Invalid or expired token.') from exc

    token_key = f'telegram_auth_token_used:{token}'
    was_unused = cache.add(token_key, True, timeout=max_age)

    if not was_unused:
        raise TelegramAuthTokenError('Token already used.')

    return telegram_id


def resolve_telegram_id_from_signed_token(token):
    """Return telegram_id from a signed token without TTL or one-time checks."""
    signer = signing.TimestampSigner(salt=TOKEN_SALT)

    try:
        telegram_id_raw = signer.unsign(token)
        return int(telegram_id_raw)
    except (signing.BadSignature, ValueError) as exc:
        raise TelegramAuthTokenError('Invalid token.') from exc

