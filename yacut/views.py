import string
import random

from flask import flash, redirect, render_template

from .error_handlers import DatabaseFullError
from .forms import URLMapForm
from .models import URLMap
from . import app, db, ID_MAX_LENGTH, MIN_LENGTH


AVAILABLE_CHARS = (
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
)
MAX_QUANTITY_DB_ITEMS = sum(
    [
        len(AVAILABLE_CHARS) ** current_len
        for current_len in range(1, ID_MAX_LENGTH + 1)
    ]
)
FULL_DB_MESSAGE = 'База данных заполнена. Обратитесь в службу поддержки.'
INDEX_PAGE = 'index.html'
SHORT_LINK_EXIST_MESSAGE = 'Такая короткая ссылка уже существует'
ORIGINAL_LINK_EXIST_MESSAGE = 'Такая длинная ссылка уже существует'
SHORT_LINK_TAG = 'short'
ORIGINAL_LINK_TAG = 'original'

def is_db_full():
    if URLMap.query.count() >= MAX_QUANTITY_DB_ITEMS:
        raise DatabaseFullError()


def get_unique_short_id():
    while True:
        short_id = ''.join(
            [random.choice(AVAILABLE_CHARS) for _ in range(
                random.randrange(MIN_LENGTH, ID_MAX_LENGTH + 1)
            )]
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX_PAGE, form=form)
    original_link = form.original_link.data
    url_map = URLMap.query.filter_by(original=original_link).first()
    if url_map:
        flash(ORIGINAL_LINK_EXIST_MESSAGE, ORIGINAL_LINK_TAG)
        return render_template(
            INDEX_PAGE,
            **{'form': form, 'url_map': url_map}
        )
    try:
        is_db_full()
    except DatabaseFullError:
        flash(FULL_DB_MESSAGE)
        return render_template(INDEX_PAGE, form=form)
    custom_id = form.custom_id.data
    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first():
            flash(SHORT_LINK_EXIST_MESSAGE, SHORT_LINK_TAG)
            return render_template(INDEX_PAGE, form=form)
    else:
        custom_id = get_unique_short_id()
    url_map = URLMap(
        original = original_link,
        short = custom_id
    )
    db.session.add(url_map)
    db.session.commit()
    form.custom_id.data = None
    return render_template(
        INDEX_PAGE,
        **{'form': form, 'url_map': url_map}
    )


@app.route('/<string:custom_id>')   # TODO тут возможно конвертер path - проверить
def redirect_view(custom_id):
    url_map = URLMap.query.filter_by(short=custom_id).first()
    return redirect(url_map.original)
