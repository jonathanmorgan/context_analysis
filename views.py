from __future__ import unicode_literals

'''
Copyright 2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet.

sourcenet is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet. If not, see http://www.gnu.org/licenses/.
'''

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# import Python libraries for CSV output
#import csv
#import datetime
#import json
#from StringIO import StringIO
#import pickle
#import sys

# six
import six

# HTML parsing
#from bs4 import BeautifulSoup

# import django authentication code.
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# include the django conf settings
#from django.conf import settings

# django core imports
from django.core.urlresolvers import reverse

# Import objects from the django.http library.
#from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect

# django.shortcuts imports - remder() method
#from django.shortcuts import get_object_or_404
from django.shortcuts import render

# import django template code
#from django.template import Context
#from django.template import loader

# import django code for csrf security stuff.
from django.template.context_processors import csrf

# python_utilities - django view helper
from python_utilities.django_utils.django_view_helper import DjangoViewHelper

# python_utilities - exceptions
#from python_utilities.exceptions.exception_helper import ExceptionHelper

# python_utilities - JSON
#from python_utilities.json.json_helper import JSONHelper

# python_utilities - logging
#from python_utilities.logging.logging_helper import LoggingHelper

# python_utilities - string helper
#from python_utilities.strings.string_helper import StringHelper

# Import form classes
from sourcenet_analysis.forms import ReliabilityNamesFilterForm
from sourcenet_analysis.forms import ReliabilityNamesResultsForm

# import models
from sourcenet_analysis.models import Reliability_Names
from sourcenet_analysis.models import Reliability_Names_Results

#================================================================================
# Shared variables and functions
#================================================================================


'''
debugging code, shared across all models.
'''

DEBUG = False
LOGGER_NAME = "sourcenet_analysis.views"

def output_debug( message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = "" ):
    
    '''
    Accepts message string.  If debug is on, logs it.  If not,
       does nothing for now.
    '''
    
    # declare variables
    my_logger_name = ""
    
    # got a logger name?
    my_logger_name = LOGGER_NAME
    if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):
    
        # use logger name passed in.
        my_logger_name = logger_name_IN
        
    #-- END check to see if logger name --#

    # call DjangoViewHelper method.
    DjangoViewHelper.output_debug( message_IN,
                                   method_IN = method_IN,
                                   indent_with_IN = indent_with_IN,
                                   logger_name_IN = my_logger_name,
                                   debug_flag_IN = DEBUG )

#-- END method output_debug() --#


#===============================================================================
# ! ==> view action methods (in alphabetical order)
#===============================================================================


@login_required
def index( request_IN ):
    
    # return reference
    me = "index"
    response_OUT = None
    response_dictionary = {}
    default_template = ''

    # initialize response dictionary
    response_dictionary = {}
    response_dictionary.update( csrf( request_IN ) )

    # set my default rendering template
    default_template = 'sourcenet_analysis/index.html'

    # add on the "me" property.
    response_dictionary[ 'current_view' ] = me        

    # render response
    response_OUT = render( request_IN, default_template, response_dictionary )

    return response_OUT

#-- END view method index() --#


@login_required
def reliability_names_disagreement_view( request_IN ):

    # return reference
    response_OUT = None

    # declare variables
    me = "reliability_names_disagreement_view"
    response_dictionary = {}
    default_template = ''
    request_inputs = None
    reliability_names_filter_form = None
    reliability_names_label = ""
    reliability_names_coder_count = -1
    reliability_names_only_disagree = False
    reliability_names_qs = None
    record_count = -1
    reliability_names_instance_list = None
    
    # declare variables - pulling together disagreement info for output.
    reliability_names_output_list = ""
    reliability_names_output_info = ""
    output_count = -1
    disagreement_flag_list = []
    disagreement_details_list = []
    disagreement_details_dict = {}
    coder_index = -1
    coder_string = ""
    current_field_name = ""
    
    # initialize response dictionary
    response_dictionary = {}
    response_dictionary.update( csrf( request_IN ) )

    # set my default rendering template
    default_template = 'sourcenet_analysis/reliability/coding-name-disagreements.html'

    # get request inputs
    request_inputs = DjangoViewHelper.get_request_data( request_IN )
    
    # create ArticleLookupForm
    reliability_names_filter_form = ReliabilityNamesFilterForm( request_inputs )
    response_dictionary[ 'reliability_names_filter_form' ] = reliability_names_filter_form

    # got inputs?
    if ( request_inputs is not None ):
        
        # get information we need from request...
        reliability_names_label = request_inputs.get( "reliability_names_label", "" )
        reliability_names_coder_count = request_inputs.get( "reliability_names_coder_count", -1 )
        reliability_names_only_disagree = request_inputs.get( "reliability_names_only_disagree", False )
        if ( reliability_names_only_disagree == "on" ):
        
            reliability_names_only_disagree = True
        
        #-- END check to see if checkbox "on" --#

        # ...and the form is ready.
        is_form_ready = True
    
    #-- END check to see if inputs. --#
    
    # form ready?
    if ( is_form_ready == True ):

        if ( reliability_names_filter_form.is_valid() == True ):

            # only disagreements?
            if ( reliability_names_only_disagree == True ):

                # retrieve QuerySet of Reliability_Names that match label and
                #    contain disagreements.
                reliability_names_qs = Reliability_Names.lookup_disagreements( label_IN = reliability_names_label, coder_count_IN = reliability_names_coder_count )
                # response_dictionary[ 'output_string' ] = "ONLY DISAGREE ( " + str( reliability_names_only_disagree ) + " )"
                
            else:
            
                # no.  Just filter on label.
                reliability_names_qs = Reliability_Names.objects.filter( label = reliability_names_label )
                # response_dictionary[ 'output_string' ] = "ALL ( " + str( reliability_names_only_disagree ) + " )"
                
                # order by:
                reliability_names_qs = reliability_names_qs.order_by( "article__id", "person_type", "person__id" )
                
            #-- END check to see if only disagreements? --#
            
            # get count of queryset return items
            if ( reliability_names_qs is not None ):

                # get count of reliability rows.
                #record_count = reliability_names_qs.count()
                
                # to start, just make a list and pass it to the template.
                reliability_names_instance_list = list( reliability_names_qs )

                # build list of dictionaries with disagreement information.
                reliability_names_output_list = []
                
                # how many isntances we got?
                output_count = len( reliability_names_instance_list )
                if ( output_count > 0 ):
                
                    # at least one - loop.
                    reliability_names_counter = 0
                    for reliability_names in reliability_names_instance_list:
        
                        # increment counter
                        reliability_names_counter += 1
        
                        # store information per row in a dictionary, for access by the view.
                        reliability_names_output_info = {}
                        reliability_names_output_info[ Reliability_Names.PROP_NAME_INDEX ] = reliability_names_counter
                        reliability_names_output_info[ Reliability_Names.PROP_NAME_INSTANCE ] = reliability_names
                        reliability_names_output_info[ Reliability_Names.PROP_NAME_ID ] = str( reliability_names.id )
                        reliability_names_output_info[ Reliability_Names.PROP_NAME_LABEL ] = reliability_names.label
                        reliability_names_output_info[ Reliability_Names.PROP_NAME_ARTICLE_ID ] = str( reliability_names.article_id )
                        reliability_names_output_info[ Reliability_Names.PROP_NAME_PERSON_NAME ] = reliability_names.person_name
                        reliability_names_output_info[ Reliability_Names.PROP_NAME_PERSON_TYPE ] = reliability_names.person_type
                        
                        # got disagreement?
                        has_disagreement = reliability_names.has_disagreement( reliability_names_coder_count )
                        #disagreement_flag_list.append( has_disagreement )
                        if ( has_disagreement == True ):

                            # yes - create list of details.
                            disagreement_details_list = []
                        
                            # create a record per coder we included when looking for
                            #     disagreements.
                            for coder_index in range( 1, int( reliability_names_coder_count ) + 1 ):
                            
                                # create dictionary to hold details for this coder
                                disagreement_details_dict = {}
                                
                                # build column names based on index.
                                coder_string = "coder" + str( coder_index )
    
                                # retrieve data - coder ID
                                current_field_name = coder_string + "_id"
                                disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_ID ] = getattr( reliability_names, current_field_name )
                            
                                # retrieve data - coder ID
                                current_field_name = coder_string + "_detected"
                                disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_DETECTED ] = getattr( reliability_names, current_field_name )
    
                                # retrieve data - coder's selected person ID
                                current_field_name = coder_string + "_person_id"
                                disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_PERSON_ID ] = getattr( reliability_names, current_field_name )
    
                                # retrieve data - coder's selected person type
                                current_field_name = coder_string + "_person_type"
                                disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_PERSON_TYPE ] = getattr( reliability_names, current_field_name )
    
                                # retrieve data - coder's first quote paragraph number
                                current_field_name = coder_string + "_first_quote_graf"
                                disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_FIRST_QUOTE_GRAF ] = getattr( reliability_names, current_field_name )
    
                                # retrieve data - coder's first quote index number
                                current_field_name = coder_string + "_first_quote_index"
                                disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_FIRST_QUOTE_INDEX ] = getattr( reliability_names, current_field_name )
    
                                # add to list.
                                disagreement_details_list.append( disagreement_details_dict )
                            
                            #-- END loop over coder indices --#
                            
                            # add details to current dictionary.
                            reliability_names_output_info[ Reliability_Names.PROP_NAME_CODER_DETAILS_LIST ] = disagreement_details_list
                            
                        else:
                        
                            # no disagreements - just set the list to None.
                            reliability_names_output_info[ Reliability_Names.PROP_NAME_CODER_DETAILS_LIST ] = None
                        
                        #-- END check to see if disagreement --#
                        
                        # add current dictionary to list.
                        reliability_names_output_list.append( reliability_names_output_info )
                        
                    #-- END loop over reliability_names --#
                    
                #-- END check to see if anything in 

                # seed response dictionary.
                response_dictionary[ 'reliability_names_label' ] = reliability_names_label
                response_dictionary[ 'reliability_names_instance_list' ] = reliability_names_instance_list
                response_dictionary[ 'reliability_names_output_list' ] = reliability_names_output_list
                response_dictionary[ 'rn_class' ] = Reliability_Names
                #response_dictionary[ 'output_string' ] = str( disagreement_flag_list )

            else:
            
                # ERROR - nothing returned from attempt to get queryset (would expect empty query set)
                response_dictionary[ 'output_string' ] = "ERROR - no QuerySet returned from call to filter().  This is odd."
            
            #-- END check to see if query set is None --#

        else:

            # not valid - render the form again
            response_dictionary[ 'output_string' ] = "Please enter a label to use to filter reliability names data."

        #-- END check to see whether or not form is valid. --#

    else:
    
        # new request, make an empty instance of network output form.
        #response_dictionary[ 'output_string' ] = "Please enter a label to use to filter reliability names data."
        pass

    #-- END check to see if new request or POST --#
    
    # add on the "me" property.
    response_dictionary[ 'current_view' ] = me        

    # render response
    response_OUT = render( request_IN, default_template, response_dictionary )

    return response_OUT

#-- END view method reliability_names_disagreement_view() --#


@login_required
def reliability_names_results_view( request_IN ):

    # return reference
    response_OUT = None

    # declare variables
    me = "reliability_names_results_view"
    response_dictionary = {}
    default_template = ''
    request_inputs = None
    reliability_names_results_form = None
    reliability_names_results_label = ""
    reliability_names_results_qs = None
    results_count = -1
    reliability_names_results_instance_list = None
    
    # declare variables - pulling together reliability info for output.
    results_info = None
    author_results_list = None
    subject_results_list = None
    reliability_names_results_counter = -1
    reliability_names_results = None
    
    # initialize response dictionary
    response_dictionary = {}
    response_dictionary.update( csrf( request_IN ) )

    # set my default rendering template
    default_template = 'sourcenet_analysis/reliability/coding-name-reliability-results.html'

    # get request inputs
    request_inputs = DjangoViewHelper.get_request_data( request_IN )
    
    # create ArticleLookupForm
    reliability_names_results_form = ReliabilityNamesResultsForm( request_inputs )
    response_dictionary[ 'reliability_names_results_form' ] = reliability_names_results_form

    # got inputs?
    if ( request_inputs is not None ):
        
        # get information we need from request...
        reliability_names_results_label = request_inputs.get( "reliability_names_results_label", "" )

        # ...and the form is ready.
        is_form_ready = True
    
    #-- END check to see if inputs. --#
    
    # form ready?
    if ( is_form_ready == True ):

        if ( reliability_names_results_form.is_valid() == True ):

            # OK.  Filter on label.
            reliability_names_results_qs = Reliability_Names_Results.objects.filter( label = reliability_names_results_label )
            # response_dictionary[ 'output_string' ] = "ALL ( " + str( reliability_names_only_disagree ) + " )"

            # order by:
            reliability_names_results_qs = reliability_names_results_qs.order_by( "coder1_coder_index", "coder2_coder_index", "id" )
            
            # get count of queryset return items
            if ( reliability_names_results_qs is not None ):

                # get count of reliability rows.
                results_count = reliability_names_results_qs.count()

                # got at least 1?
                if ( results_count > 0 ):
                
                    # yes - add query set to response dictionary so we can use
                    #     it when outputting.
                    response_dictionary[ 'reliability_names_results_qs' ] = reliability_names_results_qs
                      
                #-- END check to see if any matching results --#

                # seed response dictionary.
                response_dictionary[ 'results_count' ] = results_count
                response_dictionary[ 'reliability_names_results_label' ] = reliability_names_results_label
                response_dictionary[ 'rnr_class' ] = Reliability_Names_Results
                #response_dictionary[ 'output_string' ] = str( disagreement_flag_list )

            else:
            
                # ERROR - nothing returned from attempt to get queryset (would expect empty query set)
                response_dictionary[ 'output_string' ] = "ERROR - no QuerySet returned from call to filter().  This is odd."
            
            #-- END check to see if query set is None --#

        else:

            # not valid - render the form again
            response_dictionary[ 'output_string' ] = "Please enter a label to use to filter reliability names results data."

        #-- END check to see whether or not form is valid. --#

    else:
    
        # new request, make an empty instance of network output form.
        #response_dictionary[ 'output_string' ] = "Please enter a label to use to filter reliability names data."
        pass

    #-- END check to see if new request or POST --#
    
    # add on the "me" property.
    response_dictionary[ 'current_view' ] = me        

    # render response
    response_OUT = render( request_IN, default_template, response_dictionary )

    return response_OUT

#-- END view method reliability_names_results_view() --#
