<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/iT-Drake/MWOTeamManager">
    <img src="doc/images/Logo.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">MWO Team Manager v0.1</h3>
  <p align="center">
    A web application that you need to manage your competitive MWO team.
  </p>
</div>

<details>
  <summary>Table of contents</summary>

- [About The Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Deployment](#deployment)
- [Usage](#usage)
  - [Environment variables](#environment-variables)
  - [First launch](#first-launch)
- [Planned improvements](#planned-improvements)
- [License](#license)

</details>

<!-- ABOUT THE PROJECT -->
## About The Project

![Application](/doc/images/Application.png)

If you are tired of using Excel, Discord pinned messages, text files on your desktop with the dropdecks that you plan to use for the event, or even coming up with them every time just before the drop, then this application is what you need.

It helps you:
- Keep track of your team mech lists (each pilot can update them by copy-pasting content from mwo profile page);
- Create your own database of builds (we all love Grimmechs, but need to store our own ideas somewhere);
- Manage tournaments and events, keep track of attendance;
- Design dropdecks with useful tools that ease the flow of the process.

## Built With

[![Python][Python]][python-url]
[![Flask][Flask]][flask-url]
[![Flask-SQLAlchemy][Flask-SQLAlchemy]][flask-sqlalchemy-url]
[![AdminLTE][AdminLTE]][adminlte-url]

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

You need your own server accessible to the team with Git and Python3 pre-installed. You can run the web app on your own PC and share designed dropdecks with teammates, but that is much less useful.

### Deployment

For a Linux-based system:
- Make a folder for the project
- Initialize Git and clone repository:
  ```shell
  git init
  git clone https://github.com/iT-Drake/MWOTeamManager.git
  ```
- Create virtual environment with Python, activate it and install dependencies:
  ```shell
  python3 -m venv .venv
  . .venv/bin/activate
  .venv/bin/pip install -r requirements.txt
  ```
- Run [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) - Python WSGI server (comes with dependencies, but you can use different one, like Gunicorn):
  ```shell
  waitress-serve --port <specify your port number> --call website:create_app
  ```
  Take a look [here](/doc/Waitress.md) on how to run server as a daemon.
- Run your browser, enter server address and specified port and test the application.

<!-- USAGE EXAMPLES -->
## Usage

### Environment variables

Web application is using a list of environmental variables:
- `SECRET_KEY` - a string unique to your application that will be used to encode user session data;
- Database specific variables:
  1. If you are using SQLite database that comes default with SQLAlchemy:
    - `DB_NAME` - name of your database file that application will search for after launch, for example: database.sqlite3
  2. If you are using PostrgeSQL, you need to make adjustments in `create_app()` method of `website/__init__.py` file, there is a commented alternative to SQLALCHEMY_DATABASE_URI line:
    - `DB_NAME` - name of the database on SQL-server;
    - `SQL_USER` - name of the user that have access to the database;
    - `SQL_PASSWORD` - password of the user that have access to the database.
- `DEFAULT_USER` - will be used as the name and password for the admin user when database is created;
- `MECH_DATA` - file name that contains data for all existing mechs, comes with the project `website/data/mechdata.csv`;
- `MAP_DATA` - file name that contains data for all existing maps, comes with the project `website/data/mapdata.csv`;

Easiest way to manage enviromental variables is to create `.env` file in project folder (notice the dot in front of the name) and fill it like this:
```shell
SECRET_KEY=your-really-random-secret-key
DB_NAME=database.sqlite3
MECH_DATA=website/data/mechdata.csv
MAP_DATA=website/data/mapdata.csv
DEFAULT_USER=Admin
SQL_USER=
SQL_PASSWORD=
```

### First launch

<details>
  <summary>Introduction to the application. Images and a lot of text inside.</summary>

Open web app page in your browser. Log in with existing admin user or register a new one:

![Login](/doc/images/Login.png) ![Register](/doc/images/Register.png)

In-game-name will be used to represent user in dropdecks and mechlists.

After successful login press the button in top right corner of the screen and open your user profile:

![Login](/doc/images/Profile.png)

Here you can change your password if needed and specify a time zone in which events time will be displayed.

On the leftside menu you can find `Mechlists\Update` section. You can copy-paste there text from [MWO Profile](https://mwomercs.com/profile) page. It will be automatically parsed and your mechlist will be updated.

![Login](/doc/images/Mechlist.png)

Take a note that search field above the table let you enter a multiple column prompt like: "CLAN HERO 65 OMNI". It will search for every space-separated word in each column.

Create a tournament that your team is taking part in (it shouldn't be an official one, may be just "Summer scrims"). `Add` button will open a page for a new tournament.

![Login](/doc/images/Tournaments.png)

Add event in the same manner for existing tournament.

![Login](/doc/images/Events.png)

In the builds section you have filter buttons that can help you find the build you want. Take a note that only approved builds can be selected on dropdeck design page (marked with green).

![Login](/doc/images/Builds.png)

Now you are ready to make dropdecks. Application will message you if you left blank a field that is required to save data. Like event for a dropdeck, for example.

![Login](/doc/images/Dropdeck.png)

After you finallized your dropdecks, they will appear on event view page and you can send a link to your teammates.

![Login](/doc/images/EventView.png)

On event view page you can check if you managed to spread pilots between drops evenly, mech used not over tournament limit. Each pilot can filter dropdecks to see only the mechs that they playing. Build code could be copied to a clipboard and a link to MechDB opened in a separate tab.

</details>

<!-- Planned improvements -->
## Planned improvements

1. Panel for admin user to update the list of maps and mechs with recent ones added by PGI.
2. Event attendance system for pilots and calendar view for events.
3. Pilot preferences system (small or big mechs, long or short range weapons etc.) and build tags to make it easier to match pilot preferences while designing dropdecks.
4. Ability to copy dropdecks from previous events to a current one.
5. Automatic parser for MechDB links that will extract weapons, engine and other stats.

<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/iT-Drake/MWOTeamManager.svg?style=for-the-badge
[contributors-url]: https://github.com/iT-Drake/MWOTeamManager/graphs/contributors

[license-shield]: https://img.shields.io/github/license/iT-Drake/MWOTeamManager.svg?style=for-the-badge
[license-url]: https://github.com/iT-Drake/MWOTeamManager/blob/main/LICENSE

[Python]: https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=Python&logoColor=white
[python-url]: https://www.python.org

[Flask]: https://img.shields.io/badge/Flask-red?style=for-the-badge&logo=Flask&logoColor=white
[flask-url]: https://flask.palletsprojects.com/en/3.0.x

[Flask-SQLAlchemy]: https://img.shields.io/badge/SQLAlchemy-orange?style=for-the-badge&logo=SQLAlchemy&logoColor=white
[flask-sqlalchemy-url]: https://flask-sqlalchemy.palletsprojects.com/en/3.1.x

[AdminLTE]: https://img.shields.io/badge/AdminLTE-black?style=for-the-badge&logo=AdminLTE&logoColor=white
[adminlte-url]: https://adminlte.io
