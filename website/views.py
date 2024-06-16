from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Mechlist, User, Build, Mech
from .parser import parse_mechlist
from . import db
from datetime import date

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/mechlist-update', methods=['GET', 'POST'])
@login_required
def mechlist_update():
    if request.method == 'POST':
        new_mechlist = request.form.get('newMechlist')
        mechs = parse_mechlist(new_mechlist)
        mechlist = Mechlist.query.filter_by(user_id=current_user.id).all()
        for item in mechlist:
            db.session.delete(item)
        
        for mech in mechs.values():
            new_item = Mechlist(user_id=current_user.id, mech_name=mech['Name'])
            db.session.add(new_item)
        
        db.session.commit()

    return render_template('mechlist-update.html', user=current_user)

@views.route('/mechlist-search')
@login_required
def mechlist_search():
    users = User.query.filter_by(admin=False).all()
    data = {}
    for user in users:
        mechlist = Mechlist.query.filter_by(user_id=user.id).all()
        data[user.in_game_name] = mechlist

    return render_template('mechlist-search.html', data=data)

@views.route('/calendar')
@login_required
def calendar():
    return render_template('not-implemented.html')

@views.route('/tournaments')
@login_required
def tournaments():
    return render_template('not-implemented.html')

@views.route('/dropdecks')
@login_required
def dropdecks():
    return render_template('not-implemented.html')

@views.route('/builds')
@login_required
def builds():
    all_builds = Build.query.all()
    return render_template('builds.html', builds=all_builds)

@views.route('/build-add', methods=['GET', 'POST'])
@login_required
def build_add():
    if request.method == 'POST':
        mech = request.form.get('Mech')
        name = request.form.get('Name')
        loadout = request.form.get('Loadout')
        engine = request.form.get('Engine')
        code = request.form.get('Code')
        notes = request.form.get('Notes')
        updated = date.today()

        build = Build(mech_id=mech, name=name, loadout=loadout, engine=engine, code=code, notes=notes, updated=updated)
        db.session.add(build)
        db.session.commit()

        all_builds = Build.query.all()
        return render_template('builds.html', builds=all_builds)
    else:
        build = {
            "id": "",
            "mech_id": "",
            "name": "",
            "loadout": "",
            "engine": "",
            "code": "",
            "notes": ""
        }
        mechs = Mech.query.all()
        return render_template('build-edit.html', build=build, mechs=mechs)

@views.route('/build-edit/<int:build_id>', methods=['GET', 'POST'])
@login_required
def build_edit(build_id):
    if build_id:
        if request.method == 'POST':
            build = Build.query.filter_by(id=build_id).first()
            if build:
                build.mech_id = request.form.get('Mech')
                build.name = request.form.get('Name')
                build.loadout = request.form.get('Loadout')
                build.engine = request.form.get('Engine')
                build.code = request.form.get('Code')
                build.notes = request.form.get('Notes')
                build.updated = date.today()

                db.session.add(build)
                db.session.commit()

                all_builds = Build.query.all()
                return render_template('builds.html', builds=all_builds)
            else:
                flash('Build id wasn\'t found in the database.', category='error')
                return render_template('builds.html')
        else:
            build = Build.query.filter_by(id=build_id).first()
            mechs = Mech.query.all()
            if build:
                return render_template('build-edit.html', build=build, mechs=mechs)
            else:
                flash('Build id wasn\'t found in the database.', category='error')
                all_builds = Build.query.all()
                return render_template('builds.html', builds=all_builds)
    else:
        flash('Error opening the build. Build id is not filled in.', category='error')
        all_builds = Build.query.all()
        return render_template('builds.html', builds=all_builds)
    
@views.route('/build-delete/<int:build_id>')
@login_required
def build_delete(build_id):
    if build_id:
        build = Build.query.filter_by(id=build_id).first()
        if build:
            db.session.delete(build)
            db.session.commit()
        else:
            flash('Can\'t delete the build. ID wasn\'t found in the database.', category='error')
    else:
        flash('Can\'t delete the build. Build id is not filled in.', category='error')
    
    all_builds = Build.query.all()
    return render_template('builds.html', builds=all_builds)
