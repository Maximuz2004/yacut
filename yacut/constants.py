from collections import namedtuple
import re
import string


AVAILABLE_CHARS = (
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
)

MIN_LENGTH = 1
ID_MAX_LENGTH = 6
URL_MAX_LENGTH = 2048
URL_PATTERN = re.compile(r'^(https?://)?([a-zA-Z0-9.-]+)(/.*)?')
SHORT_PATTERN = r'^[a-zA-Z0-9]+$'

MAX_QUANTITY_DB_ITEMS = sum(
    [
        len(AVAILABLE_CHARS) ** current_len
        for current_len in range(1, ID_MAX_LENGTH + 1)
    ]
)
MODEL_FIELDS = namedtuple(
    'Fields',
    ['id', 'original', 'short', 'timestamp']
)
REQUEST_FIELDS = MODEL_FIELDS(None, 'url', 'custom_id', None)
# form
ORIGINAL_LABEL = 'Длинная ссылка'
SHORT_LABEL = 'Ваш вариант короткой ссылки'
INVALID_ORIGINAL_LINK_MESSAGE = 'Некоректная длинная ссылка'
INVALID_SHORT_MESSAGE = ('Короткая ссылка может содержать только '
                         'латинские  буквы и цифры в диапазоне от 0 до 9')
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
SUBMIT_LABEL = 'Создать'
# view
DB_FULL_MESSAGE = 'База данных заполнена. Обратитесь в службу поддержки.'
INDEX_PAGE = 'index.html'

SHORT_LINK_EXIST_MESSAGE = 'Имя {} уже занято!'
SHORT_LINK_EXIST_MESSAGE_API = 'Имя "{}" уже занято.'
SHORT_LINK_TAG = 'short'
ORIGINAL_LINK_TAG = 'original'
# api_view
NO_DATA_MESSAGE = 'Отсутствует тело запроса'
NO_URL_IN_REQUEST_MESSAGE = '\"url\" является обязательным полем!'
INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
NO_SHORT_FOUND_MESSAGE = 'Указанный id не найден'
ID_PATTERN = re.compile(SHORT_PATTERN)