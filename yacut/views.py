from flask import flash, redirect, render_template, url_for

from . import app

from .constants import (DB_FULL_MESSAGE, INDEX_PAGE, SHORT_LINK_EXIST_MESSAGE,
                        SHORT_LINK_TAG)
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id, save_to_db
from .validators import already_exist, is_db_full



@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX_PAGE, form=form)
    original = form.original_link.data
    short = form.custom_id.data
    if not short:
        short = get_unique_short_id()
    elif not already_exist(short):
        flash(SHORT_LINK_EXIST_MESSAGE.format(short), SHORT_LINK_TAG)
        return render_template(INDEX_PAGE, form=form)
    elif not is_db_full(short):
        flash(DB_FULL_MESSAGE, SHORT_LINK_TAG)
    url_map = URLMap(
        original = original,
        short = short
    )
    save_to_db(url_map)
    form.custom_id.data = None
    return render_template(
        INDEX_PAGE,
        form=form,
        short=url_for(
            'redirect_view',
            custom_id=url_map.short,
            _external=True
        )
    )


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    return redirect(
        URLMap.query.filter_by(short=custom_id).first_or_404().original
    )
