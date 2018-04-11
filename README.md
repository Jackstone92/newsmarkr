# Term 2 Data Networks and the Web Final Project:

### Flask_NewsmarkR - A Social News Sharing Platform
##### Main Submission Repo: http://gitlab.doc.gold.ac.uk/jston010/dnw-term2-project
##### Live server URL: http://doc.gold.ac.uk/usr/122

<br/>

<div id="table-of-contents" />
## Table of Contents
* [Table of Contents](#table-of-contents)
* [About](#about)
  * [Application Summary](#application-summary)
  * [Coursework Summary](#coursework-summary)
* [Application Checklist](#application-checklist)
  * [Main Checklist](#main-checklist)
  * [Extras To Note](#extras-to-note)
* [Application Login Credentials](#application-login-credentials)
* [How To Run The App Locally](#how-to-run-the-app-locally)
* [Accessing the NewsmarkR API](#accessing-api)
* [Screenshots](#screenshots)
* [Copyright Notes](#copyright-notes)

<br/>

<div id="about" />
## About

<div id="about-summary" />
### Application Summary
NewsmarkR is a social news sharing application that allows users to create an account, create a profile detailing their political interests, add profile pictures and cover photos, add friends and like, share, comment on and bookmark news headlines as they appear. It incorporates web scraping through the beautifulsoup4 module, allowing news stories to be scraped and converted into bookmarks. Users can create collections to organise their bookmarks and can join in the public discussion on all 'Browse Headlines' articles. Currently, the only supported website for web scraping is the BBC News website.

This flask application was built from scratch by myself and is separate from the my_twits application explored during our labs. In building this application, I aimed to follow python best-practices by adhering to a 'separation of concerns' divisional structure that follows the MVP programming paradigm (where views, models and templates are separated into individual files), and my CSS styling follows the BEM naming convention. All database models are created using SQLAlchemy classes along with flask_migrate to handle changes, and I used flask manager to create custom scripts for running the server and engaging with flask_migrate.  I started out by creating a custom login system using bcrypt and a custom 'login_required' decorator for ensuring that a route is only rendered if the user is logged in. However, later on, I replaced it by using recommended flask_login module. Finally, all forms incorporate the WTForms module, I have created custom api endpoints using flask_restless and all pip installs can be found in the `requirements.txt` file and can be installed by running `pip install -r requirements.txt`.

In terms of my commit history, I have been working solidly on this application as I wanted to make it look as professional as possible. Further details can be found below.

<div id="coursework-summary" />
### Coursework Summary
Regarding my coursework, I have included everything in the `/my-lab-work` folder. However, as I had initially created two separate Gitlab repos, the repo with my coursework commit history is here: http://gitlab.doc.gold.ac.uk/jston010/term-2-lab. I have followed along with all lab sessions, but my final application was created separately.

<br/>

<div id="application-checklist" />
## Application Checklist
<div id="main-checklist" />
#### Main Checklist:
- [x] It is a flask app
  - There is more than one route and more than one view &#10004;
- [x] The html is rendered using jinja templates
  - The jinja templates include some control structure(S) e.g. if/else, for/endfor &#10004; **(They also include custom macros eg. _formhelpers.html for simpler rendering of WTForms)**
- [x] It includes one or more forms
  - The forms have some validation &#10004;
  - There are useful feedback messages to the user &#10004;
  - Using wtforms is not required but is recommended &#10004;
- [x] It has a database backend that implements CRUD operations
  - The database can be mysql or mongodb &#10004; **(MySQL was used)**
  - The create & update operations take input data from a form or forms &#10004;
  - Using sqlalchemy is not required but will attract credit &#10004;
- [x] There is user authentication (i.e. logins)
  - The login process uses sessions &#10004; **(Username is stored in a session for validation)**
  - Passwords should be stored as hashes &#10004; **(Initially using bcrypt, then switched to werkzeug.security)**
  - Using a salt is not required but is recommended &#10004; **(Bcrypt salt was used before switch to werkzeug.security - see earlier commits)**
  - There is a way to logout &#10004;
  - Use of flask-login is not required but is recommended &#10004;
- [x] There is a basic api i.e. content can be accessed as json via http methods &#10004;
  - It should be clear how to access the api (this could include comments in code) &#10004; **(See below for all endpoints)**
  - Additional credit will be given for an api that implements get, post, push and delete &#10004;
  - Use of flask-restful is not required but is recommended &#10004;

<div id="extras-to-note" />
#### Extras To Note:
- [x] Python best-practices design patterns followed
  - Separation of concerns &#10004;
  - Divisional structure with MVP folder-structuring &#10004;
  - BEM CSS naming convention &#10004;
  - Split pip installs into requirements.txt file &#10004;
- [x] Incorporation of other modules into my application
  - BeautifulSoup4 &#10004;
  - Flask-Uploads &#10004;
  - Flask-Migrate &#10004;
  - Flask-Scripts Manager &#10004;
  - Bcrypt &#10004;
  - python-slugify &#10004;
  - geocoder &#10004;
- [x] Extensive use of WTForms
  - HTML5 Inputs &#10004;
  - SelectionFields and MultipleSelectionFields &#10004;
- [x] Use of SQLAlchemy with Flask_Migrate
- [x] Use of Flask-Scripts Manager
  - For commands including `python manage.py runserver` and `python manage.py db migrate` &#10004;

<br/>

<div id="application-login-credentials" />
## Application Login Credentials
Account login details for reviewing purposes:
- Username: `test`
- Password: `password`

Or, feel free to create a new account and try things out for yourself!

<br/>

<div id="how-to-run-the-app-locally" />
## How to run the app locally
1. Clone the repo
2. Rename the repo folder to `flask_newsmarkr`
3. Ensure you have the correct database:
  - Log into mysql with the following user credentials:
    - `mysql -u newsmarkr -p` with the password `newsmarkr`
  - Ensure that the database `newsmarkr` is created
4. Ensure you are running from the virtual environment by typing: `source venv/bin/activate`
5. Type the following command to access the shell: `python manage.py shell`
6. Enter the following commands to reset the database:
    ```python
    from flask_newsmarkr import db # import database
    db.session.commit() # need to commit before dropping all tables
    db.drop_all() # drop all tables
    # import all sqlalchemy models
    from articlepool.models import *
    from bookmark.models import *
    from profile.models import *
    from social.models import *
    from user.models import *
    # create tables from sqlalchemy models
    db.create_all()
    ```
7. Back out from the shell and enter the following commands to transfer database handling to flask_migrate:
  - `python manage.py db init`
  - `python manage.py db migrate`
  - `python manage.py db upgrade`
8. Run the server with the following command: `python manage.py runserver`
9. Open http://localhost:5000 in Chrome
10. Enjoy!

<br/>

<div id="accessing-api" />
## Accessing the NewsmarkR API

Here is a table that contains all of NewsmarkR's API endpoints:


| Endpoint | Model | URL | Supported Methods |
| --- | --- | --- | --- |
| ArticlePool | ArticlePool | http://localhost:5000/api/article_pool | `GET`, `POST`, `PUT`, `DELETE` |
| LiveComment | ArticlePool | http://localhost:5000/api/live_comment | `GET`, `POST`, `PUT`, `DELETE` |
| Collection | Bookmark | http://localhost:5000/api/collection | `GET`, `POST`, `PUT`, `DELETE` |
| Bookmark | Bookmark | http://localhost:5000/api/bookmark | `GET`, `POST`, `PUT`, `DELETE` |
| Category | Bookmark | http://localhost:5000/api/category | `GET`, `POST`, `PUT`, `DELETE` |
| Friends | Profile | http://localhost:5000/api/friends | `GET`, `POST`, `PUT`, `DELETE` |
| FriendRequest | Profile | http://localhost:5000/api/friend_request | `GET`, `POST`, `PUT`, `DELETE` |
| Profile | Profile | http://localhost:5000/api/profile | `GET`, `POST`, `PUT`, `DELETE` |
| Post | Social | http://localhost:5000/api/post | `GET`, `POST`, `PUT`, `DELETE` |
| Comment | Social | http://localhost:5000/api/comment | `GET`, `POST`, `PUT`, `DELETE` |
| User | User | http://localhost:5000/api/user | `GET`, `POST`, `PUT`, `DELETE` |



<br/>

<div id="screenshots" />
## Screenshots

#### Landing Page
![Landing Page](my-lab-work/README_SCREENSHOTS/1_landing_page.png?raw=true "Landing Page")
#### Login Page
![Login Page](my-lab-work/README_SCREENSHOTS/2_login_page.png?raw=true "Login Page")
#### Browse Headlines
![Browse Headlines](my-lab-work/README_SCREENSHOTS/3_browse_headlines.png?raw=true "Browse Headlines")
#### Social Feed
![Social Feed](my-lab-work/README_SCREENSHOTS/4_social_feed.png?raw=true "Social Feed")
#### Profile (Timeline)
![Profile Timeline](my-lab-work/README_SCREENSHOTS/5_profile_timeline.png?raw=true "Profile Timeline")
#### Profile (About)
![Profile About](my-lab-work/README_SCREENSHOTS/6_profile_about.png?raw=true "Profile About")
#### Profile (Edit)
![Profile Edit](my-lab-work/README_SCREENSHOTS/7_profile_edit.png?raw=true "Profile Edit")


<br/>

<div id="copyright-notes" />
## Copyright Notes
- All images used in the making of this application were downloaded from [pixabay.com](http://www.pixabay.com) and are royalty-free.
- BBC News articles are scraped and displayed using BeautifulSoup4 (I do not own any of their content)
