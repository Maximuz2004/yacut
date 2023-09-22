from flask import flash, redirect, render_template, url_for

from . import app

from .constants import REDIRECT_VIEW
from .forms import URLMapForm
from .models import URLMap

INDEX_ROUTE = '/'
INDEX_PAGE = 'index.html'
REDIRECT_ROUTE = '/<string:custom_id>'
SHORT_LINK_TAG = 'short'


@app.route(INDEX_ROUTE, methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX_PAGE, form=form)
    original = form.original_link.data
    short = form.custom_id.data
    try:
        url_map = URLMap.create(original, short, validate_api=False)
    except ValueError as error:
        flash(error.args[0], SHORT_LINK_TAG)
    return render_template(
        INDEX_PAGE,
        form=form,
        short=url_for(
            REDIRECT_VIEW,
            custom_id=url_map.short,
            _external=True
        )
    )


@app.route(REDIRECT_ROUTE)
def redirect_view(custom_id):
    return redirect(
        URLMap.get_original_link_or_404(custom_id)
    )
