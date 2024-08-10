<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]
[![][version-shield]][version-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/iT-Drake/MWOTeamManager">
    <img src="doc/images/Logo.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">MWO Team Manager</h3>
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
- [Roadmap](#roadmap)
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

Project tested on Windows 10 and Ubuntu 22.04.
You need a dedicated server to run it either rented one or the one at home with static IP that is always on.
Preinstall Git and Python3.10.
It could be used in offline mode for testing purposes, but it will require manual management of each user's settings and mechlists.

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

For a Windows-based systems:
- Make a folder for the project
- Use CMD or Powershell to run following commands:
  ```
  git init
  git clone https://github.com/iT-Drake/MWOTeamManager.git
  ```
- Create virtual environment with Python, activate it and install dependencies:
  ```
  python -m venv .venv
  .venv\bin\activate.bat
  .venv\bin\pip install -r requirements.txt
  ```
- Run [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) - Python WSGI server (comes with dependencies):
  ```
  waitress-serve --port <specify your port number> --call website:create_app
  ```

Start your browser, navigate the server address (don't forget the port specified) and test the application.

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

Easiest way to manage enviromental variables is to create `.env` file in a project folder (notice the dot in front of the name) and fill it like this:
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
  <summary>Introduction to the application (beware of images and a lot of text inside).</summary>

Open web app page in your browser. Log in with existing admin user or register a new one:

![Login](/doc/images/Login.png) ![Register](/doc/images/Register.png)

In-game-name will be used to represent user in dropdecks and mechlists.

After successful login press the button in top right corner of the screen and open your user profile:

![Profile](/doc/images/Profile.png)

Here you can change your password if needed and specify a time zone in which events time will be displayed.

On the leftside menu you can find `Mechlists\Update` section. You can add mechs manually one by one or paste the content of [MWO Profile](https://mwomercs.com/profile) page. It will be automatically parsed and your mechlist will be updated.

![Mechlist](/doc/images/Mechlist.png)

> [!NOTE]
> Search field let you enter a multi-column prompt like: "CLAN HERO 65 OMNI". It will search for every space-separated word in each column.

Create a tournament that your team is taking part in (it shouldn't be an official one, may be just "Summer scrims").
`Add` button will open a page for a new tournament.

![Tournaments](/doc/images/Tournaments.png)

Add event in the same manner for existing tournament.

![Events](/doc/images/Events.png)

In the builds section you have filter buttons that can help you find the build you want.
> [!NOTE]
> Only builds with "Approved" flag can be selected on dropdeck design page (marked with green).

![Builds](/doc/images/Builds.png)

Now you are ready to make dropdecks.

![Dropdeck](/doc/images/Dropdeck.png)

> [!TIP]
> You'll get a browser notification if you didn't fill required fields when trying to save the changes.

Finalizing a dropdeck means that you can no longer change event it will be used for and it will appear on event view page.

![EventView](/doc/images/EventView.png)

On event view page you can check if you managed to spread pilots between drops evenly, used mechs do not exceed tournament limit. Each pilot can filter dropdecks to see only the mechs that they're playing. Build code could be copied to a clipboard and a link to MechDB opens in a separate tab.

If your team is working with fill-in players for events, it may be handful to provide them a link with dropdecks which contain mechs and builds you expect them to bring.
"Share" button will let you generate an external link that you can share with users that don't have team member role. These links have a lifespan of 7 days and can be deleted from event list page.

![Users](/doc/images/Users.png)

Application supports three level of user roles:
- User - have access only to profile and mechlist update page;
- Team member - have access to most of the content;
- Admin - have access to admin panel that let you control user roles (this level is assigned to default admin user).

</details>

<!-- Roadmap -->
## Roadmap

v0.3:
- Admin panel for new mechs and maps;
- MechDB parser that will allow to select, copy and paste mech stats to store them inside web-application to compare builds without opening MechDB;

  ![MechDB](/doc/images/MechDB.png)
- Match ID's parser and pilot statistics.

v0.4:
- Calendar event view;
- Pilot preferences system that will let them rank different categories (short range, long range, dakka, laservomit, masc mechs, etc.);
- Build tags using the same categories;
- Color the loadout field on dropdeck edit page depending on how well selected build matches the pilot preferences.

v0.9:
- Redesign of the application to be a community service;
- Multiple teams on the same server and team data separation;
- Optimization of database calls and addition of caching mechanisms.

<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/iT-Drake/MWOTeamManager.svg?style=for-the-badge
[contributors-url]: https://github.com/iT-Drake/MWOTeamManager/graphs/contributors

[license-shield]: https://img.shields.io/github/license/iT-Drake/MWOTeamManager.svg?style=for-the-badge
[license-url]: https://github.com/iT-Drake/MWOTeamManager/blob/main/LICENSE

[version-shield]: https://img.shields.io/badge/Version-0.2-blue?style=for-the-badge
[version-url]: https://github.com/iT-Drake/MWOTeamManager

[Python]: https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=Python&logoColor=white
[python-url]: https://www.python.org

[Flask]: https://img.shields.io/badge/Flask-red?style=for-the-badge&logo=Flask&logoColor=white
[flask-url]: https://flask.palletsprojects.com/en/3.0.x

[Flask-SQLAlchemy]: https://img.shields.io/badge/SQLAlchemy-orange?style=for-the-badge&logo=SQLAlchemy&logoColor=white
[flask-sqlalchemy-url]: https://flask-sqlalchemy.palletsprojects.com/en/3.1.x

[AdminLTE]: https://img.shields.io/badge/AdminLTE-black?style=for-the-badge&logo=AdminLTE&logoColor=white
[adminlte-url]: https://adminlte.io
