from flask_login import login_required, current_user
from flask import Blueprint, render_template, abort, current_app, url_for
from app.map.forms import csv_upload
from jinja2 import TemplateNotFound
from app.db.models import Location
from app.db import db
import csv
import os
from werkzeug.utils import secure_filename, redirect

map = Blueprint('map', __name__,
                        template_folder='templates')

@map.route('/locations', methods=['GET', 'POST'], defaults={"page": 1})
@map.route('/locations/<int:page>', methods=['GET', 'POST'])
@login_required
def browse_locations(page):
    page = page
    per_page = 20
    pagination = Location.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_locations.html', Location=Location, data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)

@map.route('/locations/upload', methods=['POST', 'GET'])
@login_required
def upload():
    form = csv_upload()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        list_of_locations = []
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                list_of_locations.append(
                    Location(row['location'], row['longitude'], row['latitude'], row['population']))

        current_user.locations = list_of_locations
        db.session.commit()
        return redirect(url_for('map.browse_locations'))
    try:
        return render_template('upload_map.html', form=form)
    except TemplateNotFound:
        abort(404)