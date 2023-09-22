from collections import namedtuple
import string

AVAILABLE_CHARS = (
    string.ascii_lowercase + string.ascii_uppercase + string.digits
)

ATTEMPTS_COUNT = 10
ID_MAX_LENGTH = 6
URL_MAX_LENGTH = 2048
SHORT_ID_NOT_FOUND_MESSAGE = 'Короткая ссылка не найдена!'

MODEL_FIELDS = namedtuple(
    'Fields',
    ['id', 'original', 'short', 'timestamp']
)
REQUEST_FIELDS = MODEL_FIELDS(None, 'url', 'custom_id', None)
REDIRECT_VIEW = 'redirect_view'
# form
ORIGINAL_LABEL = 'Длинная ссылка'
SHORT_LABEL = 'Ваш вариант короткой ссылки'
INVALID_ORIGINAL_LINK_MESSAGE = 'Некорректная длинная ссылка'
INVALID_SHORT_MESSAGE = ('Короткая ссылка может содержать только '
                         'латинские  буквы и цифры в диапазоне от 0 до 9')
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
SUBMIT_LABEL = 'Создать'
# view
INDEX_ROUTE = '/'
REDIRECT_ROUTE = '/<string:custom_id>'
INDEX_PAGE = 'index.html'
DB_FULL_MESSAGE = 'База данных заполнена. Обратитесь в службу поддержки.'
SHORT_LINK_EXIST_MESSAGE = 'Имя {} уже занято!'
SHORT_LINK_EXIST_MESSAGE_API = 'Имя "{}" уже занято.'
SHORT_LINK_TAG = 'short'
ORIGINAL_LINK_TAG = 'original'
# api_view
GET_URL_ROUTE = '/api/id/<string:short_id>/'
CREATE_ID_ROUTE = '/api/id/'
NO_DATA_MESSAGE = 'Отсутствует тело запроса'
NO_URL_IN_REQUEST_MESSAGE = '\"url\" является обязательным полем!'
INVALID_CUSTOM_ID = ('Указано недопустимое имя для короткой ссылки')
INVALID_ORIGINAL_LINK_LENGTH = ('Ссылка не может быть длинной больше чем'
                                ' {max_length} символов, ваша длинна: '
                                '{current_length} символов')
NO_SHORT_FOUND_MESSAGE = 'Указанный id не найден'
SERVER_ISSUE_ERROR = 'Неполадки на сервере, попробуйте попозже'
