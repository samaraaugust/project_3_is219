from flask_login import login_required
from flask import Blueprint, render_template, abort
from app.map.forms import csv_upload
from jinja2 import TemplateNotFound

map = Blueprint('map', __name__,
                        template_folder='templates')

@map.route('/locations/upload', methods=['POST', 'GET'])
@login_required
def upload():
    form = csv_upload()
    try:
        return render_template('upload_map.html', form=form)
    except TemplateNotFound:
        abort(404)