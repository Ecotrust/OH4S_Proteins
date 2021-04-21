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

## Get Python 3.8
This is installed by default on Ubuntu 20.04. Ideally we'd install 3.9, but it
seems to introduce extra complexity at this time.
```
sudo apt install vim python3.8 python3.8-dev python3.8-venv -y
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
sudo service postgresql restart
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
python3.8 -m venv env
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

## Serving the site

### NGINX & uWSGI Configuration
```
sudo apt install nginx uwsgi uwsgi-plugin-python3 libpcre3 libpcre3-dev -y
pip install uwsgi
sudo cp /usr/local/apps/OH4S_Proteins/deploy/nginx.conf /etc/nginx/sites-available/oh4s
sudo rm /etc/nginx/sites-enabled/default
sudo vim /etc/nginx/sites-available/oh4s
```

Update the file with the correct `server_name` (the URL to be used to access the site).

```
sudo ln -s /etc/nginx/sites-available/oh4s /etc/nginx/sites-enabled/oh4s
sudo nginx -t
```
See the the output of that last command doesn't reveal any errors.


Put uWSGI configuration files in the correct place and enable auto-launch:
```
sudo cp /usr/local/apps/OH4S_Proteins/deploy/emperor.ini /etc/uwsgi/
sudo cp /usr/local/apps/OH4S_Proteins/deploy/uwsgi.service /etc/systemd/system/
sudo systemctl enable uwsgi.service
sudo cp /usr/local/apps/OH4S_Proteins/deploy/oh4s.ini /etc/uwsgi/apps-enabled/oh4s.ini
```

Restart the services:
```
sudo service nginx restart
sudo service uwsgi restart
```

### Static Files
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
### Munin
```
sudo apt-get install munin munin-node -y
sudo vim /etc/nginx/sites-enabled oh4s
```
Add the following lines inside your `server{}` block:
```
location /munin/static/ {
        alias /etc/munin/static/;
}

location /munin {
        alias /var/cache/munin/www;
}
```

### Uptime Monitoring
It is recommended that you use uptimerobot.com
