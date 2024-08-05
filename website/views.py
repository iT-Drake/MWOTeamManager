from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash

from flask_login import login_required
from flask_login import current_user

from .utility import Now, Today, LocalDate, UniversalDate, FormData, Sort

from .models import Mechlist, User
from .models import Build, Mech
from .models import Tournament, Event, Map
from .models import Dropdeck, DropdeckLine
from .parser import parse_mechlist
from .scraper import scrape_url
from . import db

views = Blueprint('views', __name__)

## ------------------------------------------------------------------------------------------------
##  Route:
##      /
##      /home
## ------------------------------------------------------------------------------------------------

@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    events = Event.ActiveEvents()
    stats = {
        "users": User.Total(),
        "mechs": Mechlist.Total(),
        "builds": Build.Total(),
        "events": len(events)
    }
    return render_template("home.html", user=current_user, stats=stats, events=events)

## ------------------------------------------------------------------------------------------------
##  Route:
##      /mechlist-update
##      /mechlist-search
##      /mechlist-add
## ------------------------------------------------------------------------------------------------

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

    mechs = Mech.All()
    return render_template('mechlist-update.html', user=current_user, mechs=mechs)

@views.route('/mechlist-search')
@login_required
def mechlist_search():
    users = User.All()
    data = {}
    for user in users:
        mechlist = Mechlist.query.filter_by(user_id=user.id).all()
        data[user.in_game_name] = mechlist

    team_total = Mechlist.TeamTotal()

    return render_template('mechlist-search.html', data=data, team_total=team_total)

@views.route('/mechlist-add', methods=['POST'])
@login_required
def mechlist_add():
    data = request.get_json()
    id = data.get('id')
    mech = Mech.query.get(id)

    response = {}
    if mech:
        new_item = Mechlist(user_id=current_user.id, mech_name=mech.name)
        db.session.add(new_item)
        db.session.commit()

        response['success'] = True
        response['mech'] = mech.name
        response['chassis'] = mech.chassis
        response['side'] = mech.side
        response['tonnage'] = mech.tonnage
        response['class'] = mech.weight_class
        response['type'] = mech.chassis_type
    else:
        response['success'] = False
        response['error'] = f'Selected mech wasn\'t found in the database.'

    return response

## ------------------------------------------------------------------------------------------------
##  Route:
##      /calendar
## ------------------------------------------------------------------------------------------------

@views.route('/calendar')
@login_required
def calendar():
    return render_template('not-implemented.html')

## ------------------------------------------------------------------------------------------------
##  Route:
##      /tournaments
##      /tournament-add
##      /tournament-edit/tournament_id
##      /tournament-finish/tournament_id
## ------------------------------------------------------------------------------------------------

@views.route('/tournaments')
@login_required
def tournaments():
    all_tournaments = Tournament.query.all()
    return render_template('tournaments.html', tournaments=all_tournaments)

@views.route('/tournament-add', methods=['GET', 'POST'])
@login_required
def tournament_add():
    if request.method == 'POST':
        form_data = FormData(request.form)
        tournament = Tournament().Add(data=form_data)
        db.session.add(tournament)
        db.session.commit()

        all_tournaments = Tournament.query.all()
        return render_template('tournaments.html', tournaments=all_tournaments)
    else:
        tournament = {
            "id": "",
            "name": "",
            "full_name": "",
            "team_size": "",
            "is_active": False
        }
        return render_template('tournament-edit.html', tournament=tournament)

@views.route('/tournament-edit/<int:tournament_id>', methods=['GET', 'POST'])
@login_required
def tournament_edit(tournament_id):
    if request.method == 'POST':
        tournament = Tournament.query.filter_by(id=tournament_id).first()
        tournament.name = request.form.get('name')
        tournament.full_name = request.form.get('full_name')

        db.session.add(tournament)
        db.session.commit()
    else:
        tournament = Tournament.query.filter_by(id=tournament_id).first()
        if tournament:
            if tournament.is_active:
                return render_template('tournament-edit.html', tournament=tournament)
            else:
                flash('Tournament finished and can\'t be edited.', category='error')
        else:
            flash('Tournament id wasn\'t found in the database.', category='error')

    all_tournaments = Tournament.query.all()
    return render_template('tournaments.html', tournaments=all_tournaments)

@views.route('/tournament-finish/<int:tournament_id>')
@login_required
def tournament_finish(tournament_id):
    tournament = Tournament.query.filter_by(id=tournament_id).first()
    tournament.is_active = False

    db.session.add(tournament)
    db.session.commit()

    all_tournaments = Tournament.query.all()
    return render_template('tournaments.html', tournaments=all_tournaments)

## ------------------------------------------------------------------------------------------------
##  Route:
##      /events
##      /event-add
##      /event-edit/<int:event_id>
##      /event-view/<int:event_id>
##      /event-cancel/<int:event_id>
## ------------------------------------------------------------------------------------------------

def EventList():
    active_events = Event.ActiveEvents()
    passed_events = Event.PassedEvents()
    return render_template('events.html', events=active_events, passed=passed_events)

@views.route('/events')
@login_required
def events():
    return EventList()

@views.route('/event-add', methods=['GET', 'POST'])
@login_required
def event_add():
    if request.method == 'POST':
        form_data = FormData(request.form, date_columns=['date'])
        form_data['date'] = UniversalDate(form_data['date'])
        event = Event().Add(form_data)
        db.session.add(event)
        db.session.commit()

        return EventList()
    else:
        tournaments = Tournament.query.filter_by(is_active=True).all()
        event_data = {
            "id": "",
            "tournament_id": "",
            "name": "",
            "date": Now(local=True),
            "duration": "",
            "details": ""
        }
        return render_template('event-edit.html', event=event_data, tournaments=tournaments)

@views.route('/event-edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def event_edit(event_id):
    if request.method == 'POST':
        event = Event.query.filter_by(id=event_id).first()
        if event:
            form_data = FormData(request.form, date_columns=['date'])
            form_data['date'] = UniversalDate(form_data['date'])
            event.Update(form_data)

            db.session.add(event)
            db.session.commit()
        else:
            flash('Event wasn\'t found.')
    else:
        event = Event.query.filter_by(id=event_id).first()
        if event:
            current_date = Now(local=True)
            end_date = LocalDate(event.EndDate())
            if end_date > current_date:
                event.date = LocalDate(event.date)
                tournaments = Tournament.query.filter_by(is_active=True).all()
                return render_template('event-edit.html', event=event, tournaments=tournaments)
            else:
                flash('Event have ended and can\'t be edited.', category='error')
        else:
            flash('Event id wasn\'t found in the database.', category='error')

    return EventList()

@views.route('/event-cancel/<int:event_id>', methods=['GET', 'POST'])
@login_required
def event_cancel(event_id):
    event = Event.query.get(event_id)
    if event:
        event.is_canceled = True
        for attendee in event.attendees:
            db.session.delete(attendee)
        
        db.session.add(event)
        db.session.commit()
    else:
        flash('Event id wasn\'t found in the database.', category='error')

    return EventList()

@views.route('/event-view/<int:event_id>')
@login_required
def event_view(event_id):
    event = Event.query.get(event_id)
    dropdecks = []
    pilots_assigned = {}
    mechs_used = {}
    all_users = {user.id: user.in_game_name for user in User.All()}
    event_dropdecks = Dropdeck.query.filter_by(event_id=event_id, is_finalized=True).all()
    for dropdeck in event_dropdecks:
        rows = []
        drop_tonnage = 0
        for row in dropdeck.rows:
            if row.pilot_id and row.pilot_id in all_users:
                pilot_name = all_users[row.pilot_id]
                if pilot_name in pilots_assigned:
                    pilots_assigned[pilot_name] += 1
                else:
                    pilots_assigned[pilot_name] = 1
            if row.mech_id:
                mech = Mech.query.get(row.mech_id)
                if mech.name in mechs_used:
                    mechs_used[mech.name] += 1
                else:
                    mechs_used[mech.name] = 1
                drop_tonnage += mech.tonnage
            
            item = {
                "pilot": all_users[row.pilot_id] if row.pilot_id and row.pilot_id in all_users else "",
                "spawn": row.spawn,
                "mech": mech.name if row.mech_id else "",
                "chassis": mech.chassis if row.mech_id else "",
                "tonnage": mech.tonnage if row.mech_id else "",
                "class": mech.weight_class if row.mech_id else "",
                "build": {
                    "name": row.build.name if row.build else "",
                    "code": row.build.code if row.build else "",
                    "loadout": row.build.loadout if row.build else ""
                },
                "notes": row.notes
            }
            rows.append(item)
        
        item = {
            "id": dropdeck.id,
            "starting_side": dropdeck.starting_side,
            "name": dropdeck.name,
            "drop_number": dropdeck.drop_number,
            "tonnage": drop_tonnage,
            "map": dropdeck.map.name if dropdeck.map else "",
            "rows": rows
        }
        dropdecks.append(item)

    Sort(dropdecks, 'drop_number')
    
    stats = {
        "mechs": sorted(mechs_used.items(), key=lambda x: x[1], reverse=True),
        "pilots": pilots_assigned
    }
    data = {
        "event": event.name,
        "map_planner_link": event.map_planner_link if event.map_planner_link else "",
        "stats": stats,
        "dropdecks": dropdecks,
        "users": all_users
    }
    return render_template('event-view.html', data=data)

## ------------------------------------------------------------------------------------------------
##  Route:
##      /dropdecks
##      /dropdeck-edit/<int:dropdeck_id>
##      /dropdeck-add
##      /dropdeck-finalize/<int:dropdeck_id>
## ------------------------------------------------------------------------------------------------

def DropdeckList():
    dropdecks = Dropdeck.ActiveDropdecks()
    return render_template('dropdecks.html', dropdecks=dropdecks)

@views.route('/dropdecks')
@login_required
def dropdecks():
    return DropdeckList()

@views.route('/dropdeck-edit/<int:dropdeck_id>', methods=['GET', 'POST'])
@login_required
def dropdeck_edit(dropdeck_id):
    if request.method == 'POST':
        event_id = request.form.get("event_id")
        data = {
            "name": request.form.get("name"),
            "drop_number": request.form.get("drop_number"),
            "author_id": current_user.id,
            "map_id": request.form.get("map_id"),
            "starting_side": request.form.get("starting_side"),
        }
        if event_id:
            data["event_id"] = event_id
        dropdeck = Dropdeck.query.filter_by(id=dropdeck_id).first()
        dropdeck.Update(data)
        db.session.add(dropdeck)

        rows = DropdeckLine.query.filter_by(dropdeck_id=dropdeck_id).all()
        for row in rows:
            db.session.delete(row)

        pilot_id = request.form.getlist('pilot_id')
        spawn = request.form.getlist('spawn')
        mech_id = request.form.getlist('mech_id')
        build_id = request.form.getlist('build_id')
        notes = request.form.getlist('notes')

        for row in list(zip(pilot_id, spawn, mech_id, build_id, notes)):
            line = DropdeckLine(dropdeck_id=dropdeck.id, pilot_id=row[0], spawn=row[1],\
                                mech_id=row[2], build_id=row[3], notes=row[4])
            db.session.add(line)
        db.session.commit()
        
        return DropdeckList()
    else:
        dropdeck = Dropdeck.query.filter_by(id=dropdeck_id).first()
        all_users = User.All()
        all_mechs = Mech.query.all()
        if dropdeck.event_id:
            event = Event.query.get(dropdeck.event_id)
            users = event.Attendees()
        else:
            users = all_users

        rows = []
        for item in dropdeck.rows:
            if item.pilot_id:
                mechlist = Mechlist.query.filter_by(user_id=item.pilot_id).join(Mech).all()
                mechs = [{"id": line.data.id, "name": line.data.name} for line in mechlist]
            else:
                mechs = all_mechs

            if item.mech_id:
                mech = Mech.query.get(item.mech_id)
                lines = Mechlist.query.filter_by(mech_name=mech.name).join(User).all()
                pilots = [{"id": line.user.id, "in_game_name": line.user.in_game_name} for line in lines]

                builds = Build.query.filter_by(mech_id=mech.id, approved=True)
                loadouts = {build.id: build.name for build in builds}
            else:
                pilots = users

            row = {
                "pilot_id": item.pilot_id,
                "spawn": item.spawn,
                "mech_id": item.mech_id,
                "chassis": mech.chassis if item.mech_id else "",
                "tonnage": mech.tonnage if item.mech_id else "",
                "weight_class": mech.weight_class if item.mech_id else "",
                "build": {
                    "id": item.build.id if item.build else "",
                    "name": item.build.name if item.build else ""
                },
                "notes": item.notes,
                "mechs": mechs,
                "pilots": pilots,
                "loadouts": loadouts if item.mech_id else {}
            }
            rows.append(row)

        data = {
            "id": dropdeck_id,
            "name": dropdeck.name,
            "drop_number": dropdeck.drop_number,
            "map_id": dropdeck.map_id,
            "event_id": dropdeck.event_id,
            "is_finalized": dropdeck.is_finalized,
            "starting_side": dropdeck.starting_side,
            "maps": Map.query.all(),
            "events": Event.ActiveEvents(),
            "spawns": ["Alpha", "Bravo", "Charlie"],
            "users": users,
            "mechs": all_mechs,
            "rows": rows
        }
        return render_template('dropdeck-edit.html', data=data)

@views.route('/dropdeck-add', methods=['GET', 'POST'])
@login_required
def dropdeck_add():
    if request.method == 'POST':
        data = {
            "is_finalized": False,
            "name": request.form.get("name"),
            "drop_number": request.form.get("drop_number"),
            "event_id": request.form.get("event_id"),
            "author_id": current_user.id,
            "map_id": request.form.get("map_id"),
            "starting_side": request.form.get("starting_side"),
        }
        dropdeck = Dropdeck().Add(data=data)
        db.session.add(dropdeck)
        db.session.commit()

        pilot_id = request.form.getlist('pilot_id')
        spawn = request.form.getlist('spawn')
        mech_id = request.form.getlist('mech_id')
        build_id = request.form.getlist('build_id')
        notes = request.form.getlist('notes')

        for row in list(zip(pilot_id, spawn, mech_id, build_id, notes)):
            line = DropdeckLine(dropdeck_id=dropdeck.id, pilot_id=row[0], spawn=row[1],\
                                mech_id=row[2], build_id=row[3], notes=row[4])
            db.session.add(line)
        db.session.commit()
        
        return DropdeckList()
    else:
        data = {
            "id": "",
            "name": "",
            "drop_number": 1,
            "map_id": "",
            "event_id": "",
            "is_finalized": False,
            "starting_side": 1,
            "maps": Map.query.all(),
            "events": Event.ActiveEvents(),
            "spawns": ["Alpha", "Bravo", "Charlie"],
            "users": User.All(),
            "mechs": Mech.query.all(),
            "rows": []
        }
        return render_template('dropdeck-edit.html', data=data)

@views.route('/dropdeck-finalize/<int:dropdeck_id>')
@login_required
def dropdeck_finalize(dropdeck_id):
    dropdeck = Dropdeck.query.get(dropdeck_id)
    if dropdeck:
        dropdeck.is_finalized = True
        db.session.add(dropdeck)
        db.session.commit()
    else:
        flash('Dropdeck ID wasn\'t found in the database.', category='error')
    
    return DropdeckList()

## ------------------------------------------------------------------------------------------------
##  Route:
##      /builds
##      /builds-add
##      /builds-edit/<int:build_id>
##      /builds-finish/<int:build_id>
## ------------------------------------------------------------------------------------------------

@views.route('/builds')
@login_required
def builds():
    all_builds = Build.query.all()
    return render_template('builds.html', builds=all_builds)

@views.route('/build-add', methods=['GET', 'POST'])
@login_required
def build_add():
    if request.method == 'POST':
        form_data = FormData(request.form, boolean_columns=['for_omni_mechs', 'approved'])
        form_data['updated'] = Today()

        build = Build().Add(data=form_data)
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
            "code": "",
            "notes": "",
            "armor": "",
            "engine": "",
            "speed": "",
            "firepower": "",
            "dps": "",
            "heatsinks": "",
            "dissipation": "",
            "for_omni_mechs": False,
            "approved": False
        }
        mechs = Mech.query.all()
        return render_template('build-edit.html', build=build, mechs=mechs)

@views.route('/build-edit/<int:build_id>', methods=['GET', 'POST'])
@login_required
def build_edit(build_id):
    if request.method == 'POST':
        build = Build.query.filter_by(id=build_id).first()
        if build:
            form_data = FormData(request.form, boolean_columns=['for_omni_mechs', 'approved'])
            form_data['updated'] = Today()

            build.Update(data=form_data)
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

@views.route('/build-delete/<int:build_id>')
@login_required
def build_delete(build_id):
    build = Build.query.filter_by(id=build_id).first()
    if build:
        db.session.delete(build)
        db.session.commit()
    else:
        flash('Can\'t delete the build. ID wasn\'t found in the database.', category='error')
    
    all_builds = Build.query.all()
    return render_template('builds.html', builds=all_builds)

## ------------------------------------------------------------------------------------------------
##  Route:
##      /deck-building?event_id=event_id&mech_id=mech_id&pilot_id=pilot_id
## ------------------------------------------------------------------------------------------------

@views.route('/deck-building')
@login_required
def deck_building():
    result = {}
    # Event changed
    event_id = request.args.get('event_id')
    if event_id:
        event = Event.query.get(event_id)
        result['pilots_number'] = event.tournament.team_size
        result['pilots'] = event.Attendees()

        mechs = {}
        items = Mech.All()
        for item in items:
            mechs[item.id] = item.name
        result['mechs'] = mechs

        return result

    # Mech changed
    mech_id = request.args.get('mech_id')
    if mech_id is not None:
        if mech_id:
            mech = Mech.query.get(mech_id)

            pilots = {}
            items = Mechlist.query.filter_by(mech_name=mech.name).join(User).all()
            for item in items:
                pilots[item.user.id] = item.user.in_game_name
            result['pilots'] = pilots
            
            loadouts = {}
            items = Build.query.filter_by(mech_id=mech_id, approved=True).all()
            for item in items:
                loadouts[item.id] = item.name
            result['loadouts'] = loadouts

            details = {
                "chassis": mech.chassis,
                "tonnage": mech.tonnage,
                "class": mech.weight_class
            }
            result['details'] = details

            return result
        else:
            pilots = {}
            items = User.All()
            for item in items:
                pilots[item.id] = item.in_game_name
            
            result['pilots'] = pilots
            result['loadouts'] = {}

            return result

    # Pilot changed
    pilot_id = request.args.get('pilot_id')
    if pilot_id is not None:
        if pilot_id:
            mechlist = Mechlist.query.filter_by(user_id=pilot_id).join(Mech).all()
            for item in mechlist:
                result[item.data.id] = item.data.name
            return result
        else:
            items = Mech.All()
            for item in items:
                result[item.id] = item.name

            return result

    return result

@views.route('/build-details')
def build_details():
    result = {}
    url = request.args.get('url')
    if url:
        result = scrape_url(url=url, sleep=5)

    return result
