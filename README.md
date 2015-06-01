VaiTerCopaSim - API Server
===
Personal project to study Django, AngularJS, RESTFull web services and One Page Apps. This application is a sticker exchange facilitator of the world cup album.

* [Original project](https://github.com/wormangel/VaiTerCopaSim)
* [VaiTerCopaSim-client](https://github.com/otaciliolacerda/VaiTerCopaSim-client) - Client made in AngularJS

Features
---
* Manage a list of duplicated stickers;
* Manage a list of needed stickers
* Calculates statistics about you collection
* Search for other users who have needed stickers for the user
* Compare collection to other user's collection
* Facebook authentication

Dependencies
---
* Python 2.7.6
* Django 1.8.1
* python-social-auth 0.2.9
* django-cors-headers 1.1.0
* oauth2 1.5.211
* oauthlib 0.7.2

Environment Variables
---
You need to set three environment variables:
* STICKERS_IMAGES_PREFIX - this holds the location of the sticker images, up to the trailing slashes (e.g. /my/path/to/stickers/images/)
* FB_APP_ID - the Facebook application Id (used for logging users in)
* FB_APP_SECRET - the Facebook app secret

Installation
---
After download the code  and install the dependencies, run:

```python
python manage.py migrate
```

License
--
Do whatever you want. =)