from re import escape
import string

AVAILABLE_CHARS = (
    string.ascii_lowercase + string.ascii_uppercase + string.digits
)
AVAILABLE_CHARS_REGEX = rf'^[{escape(AVAILABLE_CHARS)}]+$'

ATTEMPTS_COUNT = 10
SHORT_MAX_LENGTH = 6
URL_MAX_LENGTH = 2048
REDIRECT_VIEW = 'redirect_view'
