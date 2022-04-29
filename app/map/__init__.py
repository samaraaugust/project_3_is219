from flask_login import login_required, current_user
from flask import Blueprint, render_template, abort, flash, current_app, url_for
from app.map.forms import csv_upload, edit_location, new_location
from jinja2 import TemplateNotFound
from app.db.models import Location
from app.db import db
import csv
import os
from werkzeug.utils import secure_filename, redirect

map = Blueprint('map', __name__,
                        template_folder='templates')

@map.route('/locations/<int:location_id>/delete', methods=['POST'])
@login_required
def delete_location(location_id):
    location = Location.query.get(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location Deleted', 'success')
    return redirect(url_for('map.browse_locations'), 302)

@map.route('/locations/<int:location_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_locations(location_id):
    location = Location.query.get(location_id)
    form = edit_location(obj=location)
    if form.validate_on_submit():
        location.title = form.title.data
        location.longitude = form.longitude.data
        location.latitude = form.latitude.data
        location.population = form.population.data
        db.session.add(location)
        db.session.commit()
        flash('Location Edited Successfully', 'success')
        return redirect(url_for('map.browse_locations'))
    return render_template('location_edit.html', form=form)

@map.route('/locations/new', methods=['POST', 'GET'])
@login_required
def add_location():
    form = new_location()
    if form.validate_on_submit():
        location = Location(title=form.title.data, longitude=form.longitude.data, latitude=form.latitude.data, population=form.population.data)
        db.session.add(location)
        db.session.commit()
        flash('Congratulations, you just add a new location', 'success')
        return redirect(url_for('map.browse_locations'))

    return render_template('new_location.html', form=form)

@map.route('/locations/map/<int:location_id>')
@login_required
def retrieve_location(location_id):
    location = Location.query.get(location_id)
    return render_template('location_view.html', location=location)

@map.route('/locations_table', methods=['GET', 'POST'], defaults={"page": 1})
@login_required
def browse_locations(page):
    page = page
    per_page = 20
    pagination = Location.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    edit_url = ('map.edit_locations', [('location_id', ':id')])
    retrieve_url = ('map.retrieve_location', [('location_id', ':id')])
    delete_url = ('map.delete_location', [('location_id', ':id')])
    add_url = url_for('map.add_location')
    try:
        return render_template('browse_locations.html',retrieve_url=retrieve_url, edit_url=edit_url, add_url=add_url, Location=Location, data=data,pagination=pagination, delete_url=delete_url)
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