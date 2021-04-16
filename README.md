# OH4S_Proteins
Oregon Harvest For Schools Portal

# Installation
## Notes
This guide uses vim as the primary text editor. If you have a different
preference, nano for example, knock yourself out.

## Requirements
* Ubuntu 20.04 LTS
* sudo privileges

## Dependencies
### Update Package Manager
```
sudo apt update
sudo apt upgrade -y
```

### Get Python 3.9
```
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install vim python3.9 python3.9-dev python3.9-venv -y
```

### Install Additional Dependencies
```
sudo apt install git postgresql postgresql-contrib postgresql-server-dev-12 build-essential libssl-dev libffi-dev -y
```

### Create and Configure PostgreSQL user, database, and permissions
```
sudo -u postgres createuser --interactive --pwprompt
```
You will be prompted to provide a username and a password for your new database user.
Note these down as they will be needed both in this next step and in configuring
local_settings later in this guide.

NOTE: It is safer if you do *NOT* give your new user superuser privileges, nor
the ability to create new DBs, nor roles.

Once done, decide on a name for your database (also needed later for local_settings).
Plug both the username you created and the database name into the section below.
```
sudo -u postgres createdb -O <username> <databasename>
sudo vim /etc/postgresql/12/main/pg_hba.conf
```
Near the bottom of the file, under "Database administrative login by Unix domain
socket", you'll see the line `local   all             postgres                  
              peer`. Add a new line underneath using your own dbname and dbuser
values that reads:
```
local   <dbname>            <dbuser>                             md5
```

Save, then restart the postgreSQL server:
```
# sudo service postgresql restart
```

## Install OH4S Portal App
### Download the source code
```
mkdir /usr/local/apps
cd /usr/local/apps
git clone https://github.com/Ecotrust/OH4S_Proteins.git
```

### Create and populate the Python Virtual Environment
NOTE: At the time of this writing, Wagtail does not officially support
Django 3.2, but they do work just fine. Wagtail has been commented out, but
needs to be installed on its own, then Django 3.2 needs to be reinstalled when
Wagtail invariably downgrades it.
```
cd /usr/local/apps/OH4S_Proteins/
python -m venv env
source env/bin/activate
pip3 install --upgrade pip
pip3 install "wagtail>=2.12"
pip3 install -r app/portal/requirements.txt
```

### Configure permissions and settings
```
cd /usr/local/apps/OH4S_Proteins/app
cp portal/portal/local_settings.py.template portal/portal/local_settings.py
vim portal/portal/local_settings.py
```

Add your URL to the `ALLOWED_HOSTS` list. Use 'localhost' for local development
installations, or a url for live instances, for example:
```
ALLOWED_HOSTS = [
  'localhost',
  'portal.oregonharvestforschools.com',
]
```

Edit local_settings.py using the db name, username, and password you created
during the PostgreSQL configuration steps:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<dbname>',
        'USER': '<username>',
        'PASSWORD': '<dbpassword>'
    }
}
```

NOTE: Do we need to explicitly set permissions for static, media, or log directories?

### Create tables and load in primary data
```
python /usr/local/apps/OH4S_Proteins/app/portal/manage.py migrate
```

If you have initial data to work with (as a fixture), do something like this:
```
python portal/manage.py loaddata  portal/fixtures/<FIXTURE_FILE.json>
```

Create a Django/Wagtail superuser running the following command and following the prompts:
```
python portal/manage.py createsuperuser
```

### Test
If you have port 8000 open, you can run a test server like so:
```
python portal/manage.py runserver 0:8000
```

Check it out here: (http://localhost:8000)[http://localhost:8000]

### Create Homepage
If you didn't import a fixture for Wagtail Pages, then likely you were greeted
with a mostly blank page that said "Welcome to your new Wagtail site!"

To fix this, go here: http://localhost:8000/cms/
Create a new page (adjacent to the default homepage), and then set it as your
homepage in Wagtail's 'Settings -> Sites' area.




If you are installing for development purposes, you can stop here. For a live
server, read on.

## Serving the site
```
sudo apt install nginx uwsgi uwsgi-plugin-python3 libpcre3 libpcre3-dev -y
pip install uwsgi
sudo cp /usr/local/apps/OH4S_Proteins/deploy/nginx.conf /etc/nginx/sites-available/oh4s
sudo rm /etc/nginx/sites-enabled/default
sudo vim /etc/nginx/sites-available/oh4s
```

TODO: Write up any additional configuration needs to be done.

```
sudo ln -s /etc/nginx/sites-available/oh4s /etc/nginx/sites-enabled/oh4s
sudo nginx -t
```
See the the output of that last command doesn't reveal any errors.

TODO: copy and configure deploy/oh4s.ini and deploy/uwsgi.service to their correct locations

```
sudo service nginx restart
sudo service uwsgi restart
```

## Security and Maintenance
TODO: Unattended upgrades, AV, backup strategy, SSL

## Other considerations
