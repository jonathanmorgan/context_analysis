from __future__ import unicode_literals

'''
Copyright 2010-2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet_analysis.

sourcenet_analysis is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet_analysis is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet_analysis. If not, see http://www.gnu.org/licenses/.
'''

# import djanfgo.conf.urls.defaults stuff.
#from django.conf.urls.defaults import *
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# and import stuff to use the admin's login page for all authentication.
from django.contrib.auth import views as auth_views

# import sourcent_analysis views
import sourcenet_analysis.views

'''
# !tastypie API
# import tastypie stuff, so we can make REST-ful API
from tastypie.api import Api
from sourcenet.tastypie_api.sourcenet_api import ArticleResource

# initialize sourcenet API, v1
v1_api = Api( api_name='v1' )

# register resources
v1_api.register( ArticleResource() )
'''

# polls-specific URL settings, intended to be included in master urls.py file.
urlpatterns = [

    # index page
    url( r'^index$', sourcenet_analysis.views.index, name = "sourcenet_analysis-index" ),

    # view disagreements
    url( r'^reliability/names/disagreement/view$', sourcenet_analysis.views.reliability_names_disagreement_view, name = "sourcenet_analysis-reliability-names-disagreement-view" ),

]