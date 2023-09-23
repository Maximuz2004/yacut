from flask import flash, redirect, render_template, url_for

from . import app

from .constants import REDIRECT_VIEW
from .forms import URLMapForm
from .models import ShortNotFoundError, URLMap

INDEX_ROUTE = '/'
INDEX_PAGE = 'index.html'
REDIRECT_ROUTE = '/<string:custom_id>'


@app.route(INDEX_ROUTE, methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX_PAGE, form=form)
    try:
        return render_template(
            INDEX_PAGE,
            form=form,
            short=url_for(
                REDIRECT_VIEW,
                custom_id=URLMap.create(
                    form.original_link.data,
                    form.custom_id.data,
                    validate=False
                ).short,
                _external=True
            )
        )
    except ValueError as error:
        flash(str(error))
    except ShortNotFoundError as error:
        flash(str(error))


@app.route(REDIRECT_ROUTE)
def redirect_view(custom_id):
    return redirect(
        URLMap.get_original_link_or_404(custom_id)
    )
