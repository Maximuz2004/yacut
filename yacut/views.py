from flask import redirect, render_template, url_for

from . import app

from .constants import INDEX_PAGE, INDEX_ROUTE, REDIRECT_ROUTE, REDIRECT_VIEW

from .forms import URLMapForm
from .models import URLMap


@app.route(INDEX_ROUTE, methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX_PAGE, form=form)
    original = form.original_link.data
    short = form.custom_id.data
    url_map = URLMap.create_url_map(original, short)
    form.custom_id.data = None
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
