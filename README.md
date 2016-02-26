# sourcenet_analysis

<!-- TOC -->

sourcenet is a django application for capturing and analyzing networks of news based on articles.  In order for database migrations to work, you need to use django 1.7 or greater.  south_migrations are present, but they won't be updated going forward.

# Installation and configuration

This Django application is dependent on the sourcenet application.

Before you can use this, you need to install and configure sourcenet.

For instructions on installing and configuring sourcenet, see [https://github.com/jonathanmorgan/sourcenet](https://github.com/jonathanmorgan/sourcenet).

## OS packages

Likely, we'll end up using numpy and scipy, so might need to have OS packages installed to get them to compile.  We shall see.  Also planning on using pyRserve, might need OS libraries to get it to install, as well.

## virtualenv and virtualenvwrapper

if you are on a shared or complicated server (and who isn't, really?), using virtualenv and virtualenvwrapper to create isolated python environments for specific applications can save lots of headaches.  this application isn't stand-alone, so for now I've reproduced the instructions you'll have followed when you installed sourcenet.  For more details, see the sourcenet README.md file ( [https://github.com/jonathanmorgan/sourcenet](https://github.com/jonathanmorgan/sourcenet) ).

More details:

- Detailed documentation: [http://virtualenvwrapper.readthedocs.org/en/latest/install.html](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)

- first, install virtualenv and virtualenvwrapper in all the versions of python you might use:

    - `(sudo) pip install virtualenv`
    - `(sudo) pip install virtualenvwrapper`
    
- next, you'll need to update environment variables (assuming linux, for other OS, see documentation at link above).  Add the following to your shell startup file (on ubuntu, .bashrc is invoked by .profile, so I do this in .bashrc):

        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=$HOME/work/virtualenvwrapper-projects
        source /usr/local/bin/virtualenvwrapper.sh

- restart your shell so these settings take effect.

- use virtualenvwrapper to create a virtualenv for sourcenet:

        # for system python:
        mkvirtualenv sourcenet --no-site-packages

        # if your system python is python 3, and you want to use python 2 (since sourcenet is python 2 at the moment):
        mkvirtualenv sourcenet --no-site-packages -p /usr/bin/python2.7

- activate the virtualenv

        workon sourcenet
        
- now you are in a virtual python environment independent of the system's.  If you do this, in the examples below, you don't need to use `sudo` when you use pip, etc.

## Python packages

- first, install all the packages required by sourcenet, including one for connecting to and interacting with your database of choice (but you should really choose postgresql, or sqlite if you want something simpler, rather than mysql - mysql struggles with large databases).  Inside the sourcenet project, requirements.txt contains all of these things, assumes you will use postgresql and so includes psycopg2.  To install requirements using requirements.txt from this repository:

        - install django now using pip: `(sudo) pip install django`
        - continue on in this guide until you 
        - `(sudo) pip install -r sourcenet/requirements.txt`

- python packages that I find helpful:

    - ipython - `(sudo) pip install ipython`

## Other things to install

These are installed with sourcenet, but just so you know they are dependencies:

- You'll also need python\_utilities.  Clone python\_utilities into the research folder alongside sourcenet:

        git clone https://github.com/jonathanmorgan/python_utilities.git

- And you'll need django\_config.  Clone django\_config into the research folder alongside sourcenet:

        git clone https://github.com/jonathanmorgan/django_config.git

## settings.py - Configure logging, database, applications:

In addition to the configuration you'll need to do for sourcenet in `settings.py`, you'll also need to do the following:

### applications

Edit the `research/research/settings.py` file and add 'sourcenet_analysis' to your list of `INSTALLED_APPS` using the new django Config classes (stored by default in apps.py in the root of the application), rather than the app name:

        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            # Uncomment the next line to enable the admin:
            'django.contrib.admin',
            # Uncomment the next line to enable admin documentation:
            # 'django.contrib.admindocs',
            'sourcenet.apps.SourcenetConfig',
            'django_config.apps.Django_ConfigConfig',
            'taggit',
            'sourcenet_analysis.apps.Sourcenet_AnalysisConfig',
        )

- save the file.
    
### initialize the database

Once you've made the changes above, save the `settings.py` file, then go into the `research` directory where manage.py is installed, and run `python manage.py migrate`.

    python manage.py migrate

## Enable sourcenet_analysis pages

- get the admins working and sourcenet pages working.

- add a line to resesarch/urls.py to enable the sourcenet_analysis URLs (in `sourcenet_analysis.urls`) to the urlpatterns structure.

    - Add:

            # sourcenet_analysis URLs:
            url( r'^sourcenet_analysis/', include( 'sourcenet_analysis.urls' ) ),

    - Result:

            urlpatterns = [

                # Examples:
                # url(r'^$', 'research.views.home', name='home'),
                # url(r'^research/', include('research.foo.urls')),
                
                # django-ajax-select URLs
                url( r'^admin/lookups/', include( ajax_select_urls ) ),
                
                # Uncomment the admin/doc line below to enable admin documentation:
                url( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),
            
                # Uncomment the next line to enable the admin:
                url( r'^admin/', include( admin.site.urls ) ),
                
                # sourcenet URLs:
                url( r'^sourcenet/', include( 'sourcenet.urls' ) ),

                # sourcenet_analysis URLs:
                url( r'^sourcenet_analysis/', include( 'sourcenet_analysis.urls' ) ),

            ]
            
### Test!

- test by going to the URL:

        http://<your_server>/sourcenet/sourcenet_analysis/index

# Testing

The sourcenet_analysis project has a small but growing set of unit tests that one can auto-run.  These tests use django's testing framework, based on the Python `unittest` package.

## Unit Tests

### Configuration

#### Database configuration

In order to run unit tests, your database configuration in `settings.py` will need to be connecting to the database with a user who is allowed to create databases.  When django runs unit tests, it creates a test database, then deletes it once testing is done.
- _NOTE: This means the database user you use for unit testing SHOULD NOT be the user you'd use in production.  The production database user should not be able to do anything outside a given database._

### Running unit tests

To run unit tests, at the command line in your django project/site folder (where `manage.py` lives):

    python manage.py test sourcenet_analysis.tests
    
Specific sets of tests:

- TK

## Test data

There is a set of test data stored in the `fixtures` folder inside this django application.  The files:

- **_`sourcenet_analysis_reliability_names.json`_** - Reliability data related to detecting and categorizing names.
- **_`sourcenet_analysis_reliability_ties.json`_** - Reliability data related to building ties between reporters and reporters and reporters and sources based on attribution over time.


### Using unittest data for development

First, follow the instructions to set up sourcenet test data in the sourcenet readme: [https://github.com/jonathanmorgan/sourcenet](https://github.com/jonathanmorgan/sourcenet).

- cd into your django application's home directory, activate your virtualenv if you created one, then run "`python manage.py migrate`" to create all the tables in the database.

        cd <django_app_directory>
        workon sourcenet
        python manage.py migrate

- load the unit test fixtures into the database:

        python manage.py loaddata sourcenet_analysis_reliability_names.json
        python manage.py loaddata sourcenet_analysis_reliability_ties.json

# License

Copyright 2010-present (2016) Jonathan Morgan

This file is part of [http://github.com/jonathanmorgan/sourcenet_analysis](http://github.com/jonathanmorgan/sourcenet_analysis).

sourcenet\_analysis is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

sourcenet\_analysis is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with [http://github.com/jonathanmorgan/sourcenet_analysis](http://github.com/jonathanmorgan/sourcenet_analysis).  If not, see
[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).