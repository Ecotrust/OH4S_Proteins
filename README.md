# OH4S_Proteins
Oregon Harvest For Schools Portal

# Installation

## Get Source Code
```
git clone https://github.com/Ecotrust/OH4S_Proteins.git
cd OH4S_Proteins
```

## Vagrant
```
vagrant up
```

## SSH into VM
```
vagrant ssh
```

## Dependencies

### Update Package Manager
```
sudo apt update
sudo apt upgrade -y
```

### Install Dependencies
```
sudo apt install git python3 python3-dev python3-virtualenv python3-pip postgresql postgresql-contrib postgresql-server-dev-16 build-essential libssl-dev libffi-dev python3-venv -y
```

## Create VM on VM
```
cd /usr/local/apps
python3 -m venv env
source env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r app/portal/requirements.txt
```

## Create Database
### Create and Configure PostgreSQL user
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

### Create the database
```
sudo -u postgres createdb -O <username> <databasename>
```

### Configure the database
```
sudo vim /etc/postgresql/16/main/pg_hba.conf
```
Near the bottom of the file, under "Database administrative login by Unix domain
socket", you'll see the line `local   all             postgres                  
              peer`. Add a new line underneath using your own dbname and dbuser
values that reads:
  * **LOCAL** Environment Configuration
  ```
  local   <dbname>            <dbuser>                             trust
  ```
  * All Other Environments
  ```
  local   <dbname>            <dbuser>                             md5
  ```

Save, then restart the postgreSQL server:
```
sudo service postgresql restart
```

### Additional steps to allow running tests
I know we said granting users 'create db' privileges was bad, but if you're just
building a dev environment, who cares? Also, Django testing needs permission to
create test databases, so:
```
sudo su postgres
psql

ALTER USER <username> CREATEDB;
\q

exit
sudo vim /etc/postgresql/16/main/pg_hba.conf
```
The test database is named 'test_\<dbname>' by default. To enable creation of
a test db, duplicate the line you created earlier, once for the test db, and
once again to grant access to the postgres database (needed for testing):
  * **LOCAL** Environment Configuration
  ```
  local   <dbname>            <dbuser>                             trust
  local   test_<dbname>       <dbuser>                             trust
  ```
  * All Other Environments
  ```
  local   <dbname>            <dbuser>                             md5
  local   test_<dbname>       <dbuser>                             md5
  ```
Save and then restart PostgreSQL to enable your changes:
```
sudo service postgresql restart
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
        # If you created a password for your user, add the following line:
        'PASSWORD': '<dbpassword>'
    }
}
```

NOTE: Do we need to explicitly set permissions for static, media, or log directories?

## Initialize the database, Option 1: Using a database dump of production
Refer to this [Google Doc](https://docs.google.com/document/d/1pF5kWFGjtw_fLhjQL3ygn_OkwuE3bf3Oy0KynJnPJ8Q/edit?usp=sharing) for instructions on how to dump the production database and loading it into your local database.

Note: If you use this option you can stop here! 🛑

## Initialize the database, Option 2: Using a fixture
If you have a fixture file, you can load it in now. This is a good time to do
this, as it will populate your database with the necessary data to run the site.

### Create tables and load in primary data
```
python /usr/local/apps/OH4S_Proteins/app/portal/manage.py migrate
```

If you have initial data to work with (as a fixture), do something like this:
```
python portal/manage.py loaddata  portal/fixtures/<FIXTURE_FILE.json>
```

Now is also a good time to import category images (if you have them already, as
associated in your fixture). Copy them into
`/usr/local/apps/OH4S_Proteins/app/portal/media/category_images/`.

### Permissions
User www-data needs write access to the media directory, so let's just give it ownership:
```
sudo chown -R www-data /usr/local/apps/OH4S_Proteins/app/portal/media
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

Check it out here: http://localhost:8000

### Create Homepage
If you didn't import a fixture for Wagtail Pages, then likely you were greeted
with a mostly blank page that said "Welcome to your new Wagtail site!"

To fix this, go here: http://localhost:8000/cms/
Create a new page (adjacent to the default homepage), and then set it as your
homepage in Wagtail's 'Settings -> Sites' area.

### NOTE:
If you are installing for development purposes, you can stop here. For a live
server, read on.

# Deployment
Once you have an server instance running, you can deploy the site to it.

```
ssh <username>@<server>
```

### Update Package Manager
```
sudo apt update
sudo apt upgrade -y
```

## Install Dependencies
```
sudo apt install git python3 python3-dev python3-virtualenv python3-pip postgresql postgresql-contrib postgresql-server-dev-16 build-essential libssl-dev libffi-dev nginx uwsgi uwsgi-plugin-python3 libpcre3 libpcre3-dev python3-venv -y
```

## Munin
Munin is a monitoring tool that can be used to monitor the health of your server.
```
sudo apt-get install munin munin-node -y
```

## Make Apps Directory
```
sudo mkdir /usr/local/apps
sudo chown <username> /usr/local/apps
cd apps
```

## Get Source Code
```
git clone https://github.com/Ecotrust/OH4S_Proteins.git
cd OH4S_Proteins
```

## Create Virtual Environment
```
python3 -m venv env
source env/bin/activate
pip install -r app/portal/requirements.txt
```

## Create Database
### Create and Configure PostgreSQL user
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

### Create the database
```
sudo -u postgres createdb -O <username> <databasename>
```

### Configure the database
```
sudo vim /etc/postgresql/16/main/pg_hba.conf
```
Near the bottom of the file, under "Database administrative login by Unix domain
socket", you'll see the line `local   all             postgres                  
              peer`. Add a new line underneath using your own dbname and dbuser
values that reads:
  * All Other Environments
  ```
  local   <dbname>            <dbuser>                             md5
  ```

Save, then restart the postgreSQL server:
```
sudo service postgresql restart
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
        # If you created a password for your user, add the following line:
        'PASSWORD': '<dbpassword>'
    }
}
```

## Initialize the database, Option 1: Using a database dump of production
Refer to this [Google Doc](https://docs.google.com/document/d/1pF5kWFGjtw_fLhjQL3ygn_OkwuE3bf3Oy0KynJnPJ8Q/edit?usp=sharing) for instructions on how to dump the production database and loading it into your local database.

## Setup NGINX and uWSGI

Install NGINX and uWSGI:
```
sudo apt install nginx uwsgi uwsgi-plugin-python3 libpcre3 libpcre3-dev -y
pip install uwsgi
```

### NGINX Configuration
```
sudo cp /usr/local/apps/OH4S_Proteins/deploy/nginx.conf /etc/nginx/sites-available/oh4s
sudo rm /etc/nginx/sites-enabled/default
sudo vim /etc/nginx/sites-available/oh4s
```

Update the file with the correct `server_name` (the URL to be used to access the site), munin location, and static and media locations.

```
server {
        client_max_body_size 50M;

        server_name oh4s-stage.ecotrust.org stage.oregonharvestforschools.com oregonharvestforschools.com portal.oregonharvestforschools.com directory.oregonharvestforschools.com www.oregonharvestforschools.com;
        access_log /var/log/nginx/oh4s.access.log;
        error_log /var/log/nginx/oh4s.error.log;

        location /static {
                alias /usr/local/apps/OH4S_Proteins/app/portal/static;
        }

        location /media {
                alias /usr/local/apps/OH4S_Proteins/app/portal/media;
        }

        location /munin/static/ {
                alias /etc/munin/static/;
        }

        location /munin {
                alias /var/cache/munin/www;
        }

        location / {
                uwsgi_pass unix:///tmp/oh4s-socket;
                include uwsgi_params;
        }
} 
```

```
sudo ln -s /etc/nginx/sites-available/oh4s /etc/nginx/sites-enabled/oh4s
sudo nginx -t
```


### uWSGI Configuration
```
sudo cp /usr/local/apps/OH4S_Proteins/deploy/emperor.ini /etc/uwsgi/
sudo cp /usr/local/apps/OH4S_Proteins/deploy/uwsgi.service /etc/systemd/system/
sudo systemctl enable uwsgi.service
sudo cp /usr/local/apps/OH4S_Proteins/deploy/oh4s.ini /etc/uwsgi/apps-enabled/oh4s.ini
```

### Restart Services
```
sudo service nginx restart
sudo service uwsgi restart
```

## Static Files
```
python /usr/local/apps/OH4S_Proteins/app/portal/manage.py collectstatic
```

## Security and Maintenance
### Unattended upgrades,
```
sudo apt-get install unattended-upgrades update-notifier-common -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```
Select 'Yes' in the interactive console.

Edit the file `/etc/apt/apt.conf.d/50unattended-upgrades` near the bottom you will find the line
`//Unattended-Upgrade::Automatic-Reboot "false";`

uncomment it and set value to true:
`Unattended-Upgrade::Automatic-Reboot "true";`

To tell the server what time is most safe to reboot (when needed), uncomment the line
`//Unattended-Upgrade::Automatic-Reboot-Time "02:00";`
And set the time to your desired restart time. Unless you set it otherwise, this is in UTC.

### Antivirus
Install [ClamAV](https://help.ubuntu.com/community/ClamAV)
Installing this and configuring it is beyond the scope of this document, but is
highly recommended.

### backup strategy
This is outside of the scope of this document, but I will say that AWS snapshot
policies make this pretty easy...

### SSL/Certbot
```
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d <YOUR_URL>
```
Be sure <YOUR_URL> is referenced explicitly and typed the same as in your NGINX
configuration file at `/etc/nginx/sites-enabled/oh4s`

* provide an email address
* Type 'A' to agree to the terms
* 'Y' or 'N' to get on the awesome EFF mailing list
* '2' -- you want to redirect all traffic to HTTPS.

## Other considerations

### Uptime Monitoring
It is recommended that you use uptimerobot.com
