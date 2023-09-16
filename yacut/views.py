import string
import random

from flask import redirect, render_template

from .forms import URLMapForm
from .models import URLMap
from yacut import app, db, ID_MAX_LENGTH, MIN_LENGTH


AVAILABLE_CHARS = (
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
)


def get_unique_short_id():
    return ''.join(
        [random.choice(AVAILABLE_CHARS) for _ in range(
            random.randrange(MIN_LENGTH, ID_MAX_LENGTH + 1)
        )]
    )


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    return render_template('index.html', form=form)

@app.route('/')
def redirect_view():
    return redirect('ya.ru') # TODO Заглушка. Переделать.


if __name__ == '__main__':
    print(get_unique_short_id())