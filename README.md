# NewsmarkR Social News Sharing Platform

## About

### Application Summary
NewsmarkR is a social news sharing application that allows users to create an account, create a profile detailing their political interests, add profile pictures and cover photos, add friends and like, share, comment on and bookmark news headlines as they appear. It incorporates web scraping through the beautifulsoup4 module, allowing news stories to be scraped and converted into bookmarks. Users can create collections to organise their bookmarks and can join in the public discussion on all 'Browse Headlines' articles. Currently, the only supported website for web scraping is the BBC News website.

This flask application was built from scratch by myself and is separate from the my_twits application explored during our labs. In building this application, I aimed to follow python best-practices by adhering to a 'separation of concerns' divisional structure that follows the MVP programming paradigm (where views, models and templates are separated into individual files), and my CSS styling follows the BEM naming convention. All database models are created using SQLAlchemy classes along with flask_migrate to handle changes, and I used flask manager to create custom scripts for running the server and engaging with flask_migrate.  I started out by creating a custom login system using bcrypt and a custom 'login_required' decorator for ensuring that a route is only rendered if the user is logged in. However, later on, I replaced it by using recommended flask_login module. Finally, all forms incorporate the WTForms module, I have created custom api endpoints using flask_restless and all pip installs can be found in the `requirements.txt` file and can be installed by running `pip install -r requirements.txt`.

In terms of my commit history, I have been working solidly on this application as I wanted to make it look as professional as possible. Further details can be found below.


## How to run the app locally
1. Clone the repo
2. Rename the repo folder to `flask_newsmarkr`
3. Ensure you have the correct database:
  - Log into mysql as root
  - `CREATE DATABASE newsmarkr;`
  - `CREATE USER 'newsmarkr'@'localhost' IDENTIFIED BY 'newsmarkr';`
  - `GRANT ALL PRIVILEGES ON newsmarkr.* TO 'newsmarkr'@'localhost';`
  - Log into mysql with the following user credentials:
    - `mysql -u newsmarkr -p` with the password `newsmarkr`
4. Ensure you are running from the virtual environment by typing: `source venv/bin/activate`
  - `sudo pip install virtualenv` if virtual environment is not installed
5. Pip install requirements by `pip install -r requirements.txt`
6. Type the following command to access the shell: `python manage.py shell`
7. Enter the following commands to reset the database:

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

8. Back out from the shell and enter the following commands to transfer database handling to flask_migrate:
  - `python manage.py db init` (don't need to do this as already initiated)
  - `python manage.py db migrate`
  - `python manage.py db upgrade`
9. Run the server with the following command: `python manage.py runserver`
10. Open http://localhost:8000 in Chrome


## Accessing the NewsmarkR API

Here is a table that contains all of NewsmarkR's API endpoints:


| Endpoint | Model | URL | Supported Methods |
| --- | --- | --- | --- |
| ArticlePool | ArticlePool | http://localhost:8000/api/article_pool | `GET`, `POST`, `PUT`, `DELETE` |
| LiveComment | ArticlePool | http://localhost:8000/api/live_comment | `GET`, `POST`, `PUT`, `DELETE` |
| Collection | Bookmark | http://localhost:8000/api/collection | `GET`, `POST`, `PUT`, `DELETE` |
| Bookmark | Bookmark | http://localhost:8000/api/bookmark | `GET`, `POST`, `PUT`, `DELETE` |
| Category | Bookmark | http://localhost:8000/api/category | `GET`, `POST`, `PUT`, `DELETE` |
| Friends | Profile | http://localhost:8000/api/friends | `GET`, `POST`, `PUT`, `DELETE` |
| FriendRequest | Profile | http://localhost:8000/api/friend_request | `GET`, `POST`, `PUT`, `DELETE` |
| Profile | Profile | http://localhost:8000/api/profile | `GET`, `POST`, `PUT`, `DELETE` |
| Post | Social | http://localhost:8000/api/post | `GET`, `POST`, `PUT`, `DELETE` |
| Comment | Social | http://localhost:8000/api/comment | `GET`, `POST`, `PUT`, `DELETE` |
| User | User | http://localhost:8000/api/user | `GET`, `POST`, `PUT`, `DELETE` |



# Screenshots

### Landing Page
![Landing Page](my-lab-work/README_SCREENSHOTS/1_landing_page.png?raw=true "Landing Page")
---

### Login Page
![Login Page](my-lab-work/README_SCREENSHOTS/2_login_page.png?raw=true "Login Page")
---

### Browse Headlines
![Browse Headlines](my-lab-work/README_SCREENSHOTS/3_browse_headlines.png?raw=true "Browse Headlines")
---

### Social Feed
![Social Feed](my-lab-work/README_SCREENSHOTS/4_social_feed.png?raw=true "Social Feed")
---

### Profile (Timeline)
![Profile Timeline](my-lab-work/README_SCREENSHOTS/5_profile_timeline.png?raw=true "Profile Timeline")
---

### Profile (About)
![Profile About](my-lab-work/README_SCREENSHOTS/6_profile_about.png?raw=true "Profile About")
---

### Profile (Edit)
![Profile Edit](my-lab-work/README_SCREENSHOTS/7_profile_edit.png?raw=true "Profile Edit")
---



## Copyright Notes
- All images used in the making of this application were downloaded from [pixabay.com](http://www.pixabay.com) and are royalty-free.
- BBC News articles are scraped and displayed using BeautifulSoup4 (I do not own any content)
