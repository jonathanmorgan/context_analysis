from __future__ import unicode_literals
from __future__ import division

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

# Django query object for OR-ing selection criteria together.
from django.db.models import Q

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

# python_utilities
from python_utilities.dictionaries.dict_helper import DictHelper
from python_utilities.django_utils.django_view_helper import DjangoViewHelper
from python_utilities.lists.list_helper import ListHelper
#from python_utilities.exceptions.exception_helper import ExceptionHelper
#from python_utilities.json.json_helper import JSONHelper
#from python_utilities.logging.logging_helper import LoggingHelper
from python_utilities.strings.string_helper import StringHelper

# sourcenet imports
from sourcenet.models import Article_Author
from sourcenet.models import Article_Data
from sourcenet.models import Article_Subject

# Import form classes
from sourcenet_analysis.forms import ReliabilityNamesActionForm
from sourcenet_analysis.forms import ReliabilityNamesFilterForm
from sourcenet_analysis.forms import ReliabilityNamesResultsForm

# import models
from sourcenet_analysis.models import Reliability_Names
from sourcenet_analysis.models import Reliability_Names_Results

#================================================================================
# ! ==> Shared variables and functions
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


# ! reliability names results constants-ish.
PREFIX_AUTHOR = "author_"
PREFIX_SUBJECT = "subject_"
                # - detect %
                # - detect A
                # - detect pi
                # - lookup %
                # - lookup A
                # - lookup NZ %
                # - lookup NZ A
                # - lookup N
                # - type %
                # - type A



def build_reliability_name_detail_string( reliability_names_id_IN,
                                          delimiter_IN = "|",
                                          prefix_IN = "| ",
                                          suffix_IN = " |",
                                          default_status_IN = "CORRECT" ):
    
    '''
    Accepts Reliability_Names instance, and optional delimiter, prefix, and
        suffix.  Retrieves the Article_Data, and Article_Subject(s) that the
        Reliability_Name refers to.  Uses information from all to build a detail
        string that contains:
        - Reliability_Names ID.
        - Article ID.
        Article_Data that 
    '''
    
    # return reference
    detail_string_OUT = None
    
    # declare variables
    detail_string_list = []
    detail_string = ""
    reliability_names_id = -1
    reliability_names_qs = None
    reliability_names_instance = None
    related_article = None
    article_id = -1
    index_list = []
    current_index = -1
    
    # declare variables - retrieve information from Reliability_Names row.
    current_suffix = ""
    article_data_id = -1
    article_data_qs = None
    article_data_instance = None
    person_type_column_name = ""
    person_type = ""
    article_person_id_column_name = ""
    article_person_id = -1
    article_person_qs = None
    article_person_instance = None
    person_name = None
    person_verbatim_name = None
    person_lookup_name = None
    person_title = None
    person_organization = None
    
    # get information for output
    reliability_names_id = reliability_names_id_IN
    if ( ( reliability_names_id is not None ) and ( reliability_names_id > 0 ) ):
    
        # get Reliability_Names instane.
        reliability_names_qs = Reliability_Names.objects.all()
        reliability_names_instance = reliability_names_qs.get( pk = reliability_names_id )
        
        # get related article.
        related_article = reliability_names_instance.article
        article_id = related_article.id
        
        # Get info for all with related Article_Data.
        
        # initialize
        index_list = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
        for current_index in index_list:
        
            # see if there is an Article_Data ID.
            current_suffix = Reliability_Names.FIELD_NAME_SUFFIX_ARTICLE_DATA_ID
            article_data_id = reliability_names_instance.get_field_value( current_index, current_suffix )
            if ( article_data_id is not None ):
            
                # we have an ID value, try to get Article_Data...
                article_data_qs = Article_Data.objects.all()
                article_data_instance = article_data_qs.get( pk = article_data_id )
                
                # ...person_type...
                current_suffix = Reliability_Names.FIELD_NAME_SUFFIX_PERSON_TYPE
                person_type = reliability_names_instance.get_field_value( current_index, current_suffix )

                # ...and based on Type, Article_Subject or Article_Author.
                # is there also a person ID?
                current_suffix = Reliability_Names.FIELD_NAME_SUFFIX_ARTICLE_PERSON_ID
                article_person_id = reliability_names_instance.get_field_value( current_index, current_suffix )
                if ( ( article_person_id is not None ) and ( article_person_id > 0 ) ):
                
                    # get Article_Subject or Article_Author
                    if ( person_type == Reliability_Names.PERSON_TYPE_AUTHOR ):
                    
                        # author.
                        article_person_qs = Article_Author.objects.all()
                        article_person_instance = article_person_qs.get( pk = article_person_id )
                        
                    elif ( ( person_type == Reliability_Names.SUBJECT_TYPE_MENTIONED )
                        or ( person_type == Reliability_Names.SUBJECT_TYPE_QUOTED ) ):
                        
                        # subject.
                        article_person_qs = Article_Subject.objects.all()
                        article_person_instance = article_person_qs.get( pk = article_person_id )
                    
                    else:
                    
                        article_person_instance = None

                    #-- END check of person type. --#
                
                #-- END check to see if article_person_id --#
            
                # build detail string.
                detail_string = prefix_IN
                detail_string += str( reliability_names_id )
                detail_string += " " + delimiter_IN + " Article ["
                detail_string += str( article_id )
                detail_string += "](http://research.local/sourcenet/sourcenet/article/article_data/view_with_text/?article_id="
                detail_string += str( article_id )
                detail_string += ") " + delimiter_IN + " Article_Data ["
                detail_string += str( article_data_id )
                detail_string += "](http://research.local/sourcenet/sourcenet/article/article_data/view/?article_id="
                detail_string += str( article_id )
                detail_string += "&article_data_id_select="
                detail_string += str( article_data_id )
                detail_string += ") " + delimiter_IN + " "
                detail_string += StringHelper.object_to_unicode_string( article_person_instance )
                
                #------------------------------------------#
                # got a name?
                person_name = article_person_instance.name
                if ( ( person_name is not None ) and ( person_name != "" ) ):
                    detail_string += " ==> name: " + person_name
                #-- END check to see if name captured. --#
                
                # lookup name different from verbatim name?
                person_verbatim_name = article_person_instance.verbatim_name
                person_lookup_name = article_person_instance.lookup_name
                if ( ( person_lookup_name is not None ) and ( person_lookup_name != "" ) and ( person_lookup_name != person_verbatim_name ) ):
                    detail_string += " ====> verbatim name: " + person_verbatim_name
                    detail_string += " ====> lookup name: " + person_lookup_name
                #-- END check to see if name captured. --#
                
                person_title = article_person_instance.title
                if ( ( person_title is not None ) and ( person_title != "" ) ):
                    detail_string += " ==> title: " + person_title
                #-- END check to see if name captured. --#
                
                # got an organization string?
                person_organization = article_person_instance.organization_string
                if ( ( person_organization is not None ) and ( person_organization != "" ) ):
                    detail_string += " ==> organization: " + person_organization
                #-- END check to see if name captured. --#
                
                # add status
                detail_string += " " + delimiter_IN + " " + default_status_IN

                detail_string += suffix_IN
                
                # add to list
                detail_string_list.append( detail_string )
            
            #-- END check to see if Article_Data ID. --#
                        
        #-- END loop over indexes. --#
        
        # tie all populated together.
        detail_string_OUT = "\n".join( detail_string_list )

    else:
    
        # no ID passed in.  Return None.
        detail_string_OUT = None
    
    #-- END check to see if Reliabilty_Names ID passed in. --#
    
    return detail_string_OUT

#-- END method build_reliability_name_detail_string() --#


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
    reliability_names_action_form = None
    reliability_names_filter_form = None
    ready_to_act = False
    is_filter_form_valid = False
    is_action_form_valid = False
    is_filter_form_empty = False
    reliability_names_filter_form_hidden_inputs = ""
    
    # declare variables - processing control
    reliability_names_action_IN = None
    reliability_names_action_tag_list_string = None
    reliability_names_action_tag_list = []
    cleaned_inputs = {}
    select_id_list = []
    merge_into_id_list = []
    input_name = ""
    input_value = ""
    person_id_string = ""
    person_id = -1
    action_summary = ""
    action_detail_list = []
    
    # declare variables - filtering/lookup
    reliability_names_filter_summary = ""
    reliability_names_label = ""
    reliability_names_coder_count = -1
    reliability_names_filter_type = ""
    reliability_names_id_in_list_string = None
    reliability_names_id_in_list = []
    reliability_names_tag_in_list_string = None
    reliability_names_tag_in_list = []
    reliability_names_id_count = -1
    reliability_names_article_id_in_list_string = None
    reliability_names_article_id_in_list = []
    article_id_count = -1
    reliability_names_only_first_name = False
    reliability_names_include_optional_fields = False
    reliability_names_counter = -1
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
    
    # declare variables - delete
    delete_count = -1
    delete_counter = -1
    reliability_names_id = -1
    reliability_names_instance = None
    detail_string = ""
    detail_string_list = []
    
    # declare variables - merge
    from_id = -1
    into_id = -1
    merge_status = None
    
    # declare variables - add and remove tags
    tag_list_count = -1
    select_count = -1
    add_tag_counter = -1
    remove_tag_counter = -1
    tag_value = None
    
    # initialize response dictionary
    response_dictionary = {}
    response_dictionary.update( csrf( request_IN ) )

    # set my default rendering template
    default_template = 'sourcenet_analysis/reliability/coding-name-disagreements.html'

    # add a few CONSTANTS-ISH for rendering.
    response_dictionary[ "input_name_select_prefix" ] = ReliabilityNamesActionForm.INPUT_NAME_SELECT_PREFIX
    response_dictionary[ "input_name_merge_into_prefix" ] = ReliabilityNamesActionForm.INPUT_NAME_MERGE_INTO_PREFIX
    
    # do we have input parameters?
    request_inputs = DjangoViewHelper.get_request_data( request_IN )
    
    # got inputs?
    if ( request_inputs is not None ):
        
        # create forms
        reliability_names_action_form = ReliabilityNamesActionForm( request_inputs )
        reliability_names_filter_form = ReliabilityNamesFilterForm( request_inputs )
        
        # we can try an action
        ready_to_act = True

    else:
    
        # no inputs - create empty forms
        reliability_names_action_form = ReliabilityNamesActionForm()
        reliability_names_filter_form = ReliabilityNamesFilterForm()
                
        # no action without some inputs
        ready_to_act = False

    #-- END check to see if inputs. --#

    # store forms in response
    response_dictionary[ "reliability_names_action_form" ] = reliability_names_action_form
    response_dictionary[ "reliability_names_filter_form" ] = reliability_names_filter_form

    # lookup forms ready?
    if ( ready_to_act == True ):

        # validate forms
        is_action_form_valid = reliability_names_action_form.is_valid()
        is_filter_form_valid = reliability_names_filter_form.is_valid()
        
        # make and use cleaned_inputs from forms when possible.
        cleaned_inputs = {}
        cleaned_inputs.update( reliability_names_action_form.cleaned_data )
        cleaned_inputs.update( reliability_names_filter_form.cleaned_data )

        # is action form valid?
        if ( is_action_form_valid == True ):

            # first, get the Reliability_Names (rn) action and add it to the
            #     response_dictionary.
            reliability_names_action_IN = request_inputs.get( "reliability_names_action", ReliabilityNamesActionForm.RELIABILITY_NAMES_ACTION_LOOKUP )
            response_dictionary[ "reliability_names_action" ] = reliability_names_action_IN
            
            # also grab tag list, if present.
            reliability_names_action_tag_list_string = cleaned_inputs.get( "reliability_names_action_tag_list", [] )
            reliability_names_action_tag_list = ListHelper.get_value_as_list( reliability_names_action_tag_list_string, delimiter_IN = "," )

            # got an action?
            if ( ( reliability_names_action_IN is not None ) and ( reliability_names_action_IN != "" ) ):

                # Yes, we have an action.  But first...
                
                # populate merge...id lists.            
                select_id_list = []
                merge_into_id_list = []
            
                # loop over inputs, looking for field names that start with
                #     either "select_person_id_<person_id>" or
                #     "merge_into_person_id_<person_id>".
                # Must loop over request_inputs, since these are dynamically
                #     named, and so not in a Form.
                for input_name, input_value in six.iteritems( request_inputs ):
                
                    # does input_name begin with "select_person_id_"?
                    if ( input_name.startswith( ReliabilityNamesActionForm.INPUT_NAME_SELECT_PREFIX ) == True ):
                    
                        # it is a "select_person_id_" input - remove this
                        #     prefix, convert to integer, then add the ID value
                        #     to the select_id_list.
                        person_id_string = input_name.replace( ReliabilityNamesActionForm.INPUT_NAME_SELECT_PREFIX, "" )
                        person_id = int( person_id_string )
                        select_id_list.append( person_id )
                        
                    # does input_name begin with "merge_into_person_id_"?
                    elif ( input_name.startswith( ReliabilityNamesActionForm.INPUT_NAME_MERGE_INTO_PREFIX ) == True ):
                    
                        # it is a "merge_into_person_id_" input - remove this
                        #     prefix, convert to integer, then add the ID value
                        #     to the merge_into_id_list.
                        person_id_string = input_name.replace( ReliabilityNamesActionForm.INPUT_NAME_MERGE_INTO_PREFIX, "" )
                        person_id = int( person_id_string )
                        merge_into_id_list.append( person_id )
                        
                    #-- END check for "*_person_id_<person_id>" prefixes --#
                                        
                #-- END loop over request_inputs --#
            
                # Got one.  what are we doing?  Lookup?
                if ( reliability_names_action_IN == ReliabilityNamesActionForm.RELIABILITY_NAMES_ACTION_LOOKUP ):
    
                    # ! ---- lookup
                    
                    #-------------------------------------------------------------------
                    # store the inputs for these forms as hidden input HTML, for use in
                    #     sending the filter on to a processing page.
                
                    # reliability_names_filter_form
                    reliability_names_filter_form_hidden_inputs = reliability_names_filter_form.to_html_as_hidden_inputs()
                    response_dictionary[ "reliability_names_filter_form_hidden_inputs" ] = reliability_names_filter_form_hidden_inputs
                
                    # is filter form valid?
                    if ( is_filter_form_valid == True ):
                    
                        # if valid, we at least have a label.
                        action_detail_list.append( "Filters:" )
                        
                        # get information we need from request...
                        
                        # label
                        reliability_names_label = cleaned_inputs.get( "reliability_names_label", "" )
                        action_detail_list.append( "label = " + str( reliability_names_label ) )

                        # coder count
                        reliability_names_coder_count = cleaned_inputs.get( "reliability_names_coder_count", -1 )
                        action_detail_list.append( "coder count = " + str( reliability_names_coder_count ) )
                        
                        # filter type
                        reliability_names_filter_type = cleaned_inputs.get( "reliability_names_filter_type", ReliabilityNamesFilterForm.RELIABILITY_NAMES_FILTER_TYPE_LOOKUP )
                        action_detail_list.append( "filter type = " + str( reliability_names_filter_type ) )
                        
                        # Reliability_Names ID IN list
                        reliability_names_id_in_list_string = cleaned_inputs.get( "reliability_names_id_in_list", None )
                        action_detail_list.append( "<lookup> IDs IN = " + str( reliability_names_id_in_list_string ) )

                        # Reliability_Names tag IN list
                        reliability_names_tag_in_list_string = cleaned_inputs.get( "reliability_names_tag_in_list", None )
                        action_detail_list.append( "<lookup> tags IN = " + str( reliability_names_tag_in_list_string ) )

                        # Reliability_Names related Article ID IN list
                        reliability_names_article_id_in_list_string = cleaned_inputs.get( "reliability_names_article_id_in_list", None )
                        action_detail_list.append( "<lookup> Article IDs IN = " + str( reliability_names_article_id_in_list_string ) )

                        # only first name present
                        reliability_names_only_first_name = cleaned_inputs.get( "reliability_names_only_first_name", False )
                        if ( reliability_names_only_first_name == "on" ):
                        
                            reliability_names_only_first_name = True
                        
                        #-- END check to see if checkbox "on" --#
                        action_detail_list.append( "<lookup> only first name? = " + str( reliability_names_only_first_name ) )
                
                        # disagree - include optional fields
                        reliability_names_include_optional_fields = cleaned_inputs.get( "reliability_names_include_optional_fields", False )
                        if ( reliability_names_include_optional_fields == "on" ):
                        
                            reliability_names_include_optional_fields = True
                        
                        #-- END check to see if checkbox "on" --#
                        action_detail_list.append( "<disagree> include optional? = " + str( reliability_names_include_optional_fields ) )
                
                        # filter type?
                        
                        # only_disagree?
                        if ( reliability_names_filter_type == ReliabilityNamesFilterForm.RELIABILITY_NAMES_FILTER_TYPE_ONLY_DISAGREE ):
            
                            # retrieve QuerySet of Reliability_Names that match
                            #    label and contain disagreements among specified
                            #    coders.
                            reliability_names_qs = Reliability_Names.lookup_disagreements(
                                label_IN = reliability_names_label,
                                coder_count_IN = reliability_names_coder_count,
                                include_optional_IN = reliability_names_include_optional_fields
                            )

                            # ORDER - lookup_disagreements() uses raw SQL, so it
                            #     is ordered in that SQL query, inside the
                            #     method call.
                            #reliability_names_qs = reliability_names_qs.order_by( "article__id", "person_type", "person_last_name", "person_first_name", "person_name", "person__id" )
            
                        # lookup?
                        elif ( reliability_names_filter_type == ReliabilityNamesFilterForm.RELIABILITY_NAMES_FILTER_TYPE_LOOKUP ):
                        
                            # lookup.  Filter on label.
                            reliability_names_qs = Reliability_Names.objects.filter( label = reliability_names_label )
                            # response_dictionary[ 'output_string' ] = "ALL ( " + str( reliability_names_only_disagree ) + " )"
                            
                            # got any IDs to filter on?
                            reliability_names_id_in_list = ListHelper.get_value_as_list( reliability_names_id_in_list_string, delimiter_IN = "," )
                            reliability_names_id_count = len( reliability_names_id_in_list )
                            if ( reliability_names_id_count > 0 ):
                            
                                # there are IDs to filter on.
                                reliability_names_qs = reliability_names_qs.filter( pk__in = reliability_names_id_in_list )
                            
                            #-- END check to see if IDs to filter on --#
                            
                            # got any tags to filter on?
                            reliability_names_tag_in_list = ListHelper.get_value_as_list( reliability_names_tag_in_list_string, delimiter_IN = "," )
                            reliability_names_tag_count = len( reliability_names_tag_in_list )
                            if ( reliability_names_tag_count > 0 ):
                            
                                # there are tags to filter on.
                                reliability_names_qs = reliability_names_qs.filter( tags__name__in = reliability_names_tag_in_list )
                                #response_dictionary[ 'output_string' ] = "Tried to filter on tags...: " + str( ",".join( reliability_names_tag_in_list ) ) + "; string: " + str( reliability_names_tag_in_list_string )
                                
                            else:
                            
                                #response_dictionary[ 'output_string' ] = "No tags in list: " + str( reliability_names_tag_in_list_string )
                                pass
                            
                            #-- END check to see if tags to filter on --#
                            
                            # got any article IDs to filter on?
                            reliability_names_article_id_in_list = ListHelper.get_value_as_list( reliability_names_article_id_in_list_string, delimiter_IN = "," )
                            article_id_count = len( reliability_names_article_id_in_list )
                            if ( article_id_count > 0 ):
                            
                                # there are IDs to filter on.
                                reliability_names_qs = reliability_names_qs.filter( article__pk__in = reliability_names_article_id_in_list )
                            
                            #-- END check to see if Article IDs to filter on --#
                            
                            # only records whose person has just first name?
                            if ( reliability_names_only_first_name == True ):
                            
                                # to start, first name needs to not be null and
                                #     not be empty.
                                reliability_names_qs = reliability_names_qs.filter( 
                                    Q( person__first_name__isnull = False ) & ~Q( person__first_name = "" ),
                                    Q( person__middle_name__isnull = True ) | Q( person__middle_name = "" ),
                                    Q( person__last_name__isnull = True ) | Q( person__last_name = "" ),
                                    Q( person__name_prefix__isnull = True ) | Q( person__name_prefix = "" ),
                                    Q( person__name_suffix__isnull = True ) | Q( person__name_suffix = "" ),
                                    Q( person__nickname__isnull = True ) | Q( person__nickname = "" ),
                                )
                            
                            #-- END only first name --#
                            
                            # order by (only for call to filter() - lookup_disagreements()
                            #     uses a raw SQL query, so it can't be re-ordered.
                            reliability_names_qs = reliability_names_qs.order_by( "article__id", "person_type", "person_last_name", "person_first_name", "person_name", "person__id" )
                            
                        #-- END check to see if only disagreements? --#
                        
                        # get count of queryset return items
                        reliability_names_counter = 0
                        if ( reliability_names_qs is not None ):
            
                            # get count of reliability rows.
                            #record_count = reliability_names_qs.count()
                            
                            # to start, just make a list and pass it to the template.
                            reliability_names_instance_list = list( reliability_names_qs )
            
                            # build list of dictionaries with disagreement information.
                            reliability_names_output_list = []
                            
                            # how many isntances we got?
                            output_count = len( reliability_names_instance_list )
                            reliability_names_filter_summary = "Found " + str( output_count ) + " records that match " + reliability_names_filter_summary
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
                                    reliability_names_output_info[ Reliability_Names.PROP_NAME_TAGS ] = reliability_names.tags
                                    reliability_names_output_info[ Reliability_Names.PROP_NAME_ARTICLE_ID ] = str( reliability_names.article_id )
                                    reliability_names_output_info[ Reliability_Names.PROP_NAME_PERSON_NAME ] = reliability_names.person_name
                                    reliability_names_output_info[ Reliability_Names.PROP_NAME_PERSON_FIRST_NAME ] = reliability_names.person_first_name
                                    reliability_names_output_info[ Reliability_Names.PROP_NAME_PERSON_LAST_NAME ] = reliability_names.person_last_name
                                    reliability_names_output_info[ Reliability_Names.PROP_NAME_PERSON_TYPE ] = reliability_names.person_type
                                    
                                    # got disagreement?
                                    has_disagreement = reliability_names.has_disagreement( reliability_names_coder_count, include_optional_IN = reliability_names_include_optional_fields )
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
                                            current_field_name = coder_string + "_id"  # grabbing foreign key value directly.
                                            disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_ID ] = getattr( reliability_names, current_field_name )
                                        
                                            # retrieve data - coder ID
                                            current_field_name = coder_string + "_" + Reliability_Names.FIELD_NAME_SUFFIX_DETECTED  # + "_detected"
                                            disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_DETECTED ] = getattr( reliability_names, current_field_name )
                
                                            # retrieve data - coder's selected person ID
                                            current_field_name = coder_string + "_" + Reliability_Names.FIELD_NAME_SUFFIX_PERSON_ID  # + "_person_id"
                                            disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_PERSON_ID ] = getattr( reliability_names, current_field_name )
                
                                            # retrieve data - coder's selected person type
                                            current_field_name = coder_string + "_" + Reliability_Names.FIELD_NAME_SUFFIX_PERSON_TYPE  # + "_person_type"
                                            disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_PERSON_TYPE ] = getattr( reliability_names, current_field_name )
                
                                            # retrieve data - coder's first quote paragraph number
                                            current_field_name = coder_string + "_" + Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF  # + "_first_quote_graf"
                                            disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_FIRST_QUOTE_GRAF ] = getattr( reliability_names, current_field_name )
                
                                            # retrieve data - coder's first quote index number
                                            current_field_name = coder_string + "_" + Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX  # + "_first_quote_index"
                                            disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_FIRST_QUOTE_INDEX ] = getattr( reliability_names, current_field_name )
                
                                            # retrieve data - organization string hash
                                            current_field_name = coder_string + "_" + Reliability_Names.FIELD_NAME_SUFFIX_ORGANIZATION_HASH  # + "_organization_hash"
                                            disagreement_details_dict[ Reliability_Names.PROP_NAME_CODER_ORGANIZATION_HASH ] = getattr( reliability_names, current_field_name )
                
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
                        
                        action_summary = "Found " + str( reliability_names_counter ) + " Reliability_Names records that match criteria."
                        
                    else:

                        # not valid - render the form again
                        response_dictionary[ 'output_string' ] = "Both a label and the number of coders to compare are required to properly filter reliability names data."
            
                    #-- END check to see if ReliabilityNamesFilterForm is valid --#

                # delete?
                elif ( reliability_names_action_IN == ReliabilityNamesActionForm.RELIABILITY_NAMES_ACTION_DELETE ):
                
                    # ! ---- delete
                    
                    # ! TODO - add confirm
                    
                    # check to see if anything in select_id_list
                    delete_count = len( select_id_list )
                    if ( delete_count > 0 ):
                        
                        # loop over IDs, looking up record for each, then
                        #     deleting it.
                        delete_counter = 0
                        for reliability_names_id in select_id_list:
                        
                            delete_counter += 1
                            
                            # lookup record for ID.
                            reliability_names_instance = Reliability_Names.objects.get( pk = reliability_names_id )
                            
                            # build a detail string:
                            detail_string = build_reliability_name_detail_string( reliability_names_id )
                            detail_string_list.append( detail_string )
                            
                            # delete it
                            reliability_names_instance.delete()
                            
                        #-- END loop over selected IDs. --#
                        
                        # update the action details list.
                        action_summary = "Deleted " + str( delete_counter ) + " Reliability_Names records with IDs: " + str( select_id_list )
                        action_detail_list.append( action_summary )
                        action_detail_list.extend( detail_string_list )
                        
                    else:
                    
                        # when merging coding, can only do one FROM and one INTO
                        response_dictionary[ 'output_string' ] = "Delete requested, but no records selected.  Nothing deleted."        

                    #-- END check to make sure at least one. --#
                    
                # merge?
                elif ( reliability_names_action_IN == ReliabilityNamesActionForm.RELIABILITY_NAMES_ACTION_MERGE_CODING ):
                
                    # ! ---- merge_coding from...to
                    
                    # first, check to make sure just one FROM and one INTO.
                    from_count = len( select_id_list )
                    into_count = len( merge_into_id_list )
                    
                    if ( ( from_count == 1 ) and ( into_count == 1 ) ):
                    
                        # one of each.  For all non-empty indices in the FROM,
                        #     copy the values for each index into the fields for
                        #     that index in the INTO.
                        
                        # get the person IDs.
                        from_id = select_id_list[ 0 ]
                        into_id = merge_into_id_list[ 0 ]
                        
                        # call the merge method.
                        merge_status = Reliability_Names.merge_records( from_id, into_id, delete_from_record_IN = False )
                        
                        # update the action details list.
                        action_summary = "Status = \"" + str( merge_status.get_status_code() ) + "\": merging person data from Reliability_Names record " + str( from_id ) + " into Reliability_Names record " + str( into_id )
                        action_detail_list.append( action_summary )
                        
                        # get message list from status container and append it to action summary.
                        merge_status_message_list = merge_status.get_message_list()
                        action_detail_list.extend( merge_status_message_list )
                        
                    else:
                    
                        # when merging coding, can only do one FROM and one INTO
                        response_dictionary[ 'output_string' ] = "When merging coding, you can only merge coding that refers to a single person INTO the coding that refers to a single other person (FROM 1 INTO 1)."        

                    #-- END check to make sure one FROM and one INTO. --#
                    
                # add tag(s)?
                elif ( reliability_names_action_IN == ReliabilityNamesActionForm.RELIABILITY_NAMES_ACTION_ADD_TAG ):
                
                    # ! ---- add tags
                    
                    # first, make sure there is something in tag list.
                    tag_list_count = len( reliability_names_action_tag_list )
                    if ( tag_list_count > 0 ):
                    
                        # got at least one tag - check to see if anything in select_id_list
                        select_count = len( select_id_list )
                        if ( select_count > 0 ):
                            
                            # loop over IDs, looking up record for each, then
                            #     add tag(s).
                            add_tag_counter = 0
                            for reliability_names_id in select_id_list:
                            
                                add_tag_counter += 1
                                
                                # lookup record for ID.
                                reliability_names_instance = Reliability_Names.objects.get( pk = reliability_names_id )
                                
                                # add all tags in list
                                reliability_names_instance.tags.add( *reliability_names_action_tag_list )
                                                                
                            #-- END loop over selected IDs. --#
                            
                            # update the action details list.
                            action_summary = "Added tag(s): " + str( reliability_names_action_tag_list ) + " to " + str( add_tag_counter ) + " Reliability_Names records."
                            action_detail_list.append( action_summary + " ==> IDs: " + str( select_id_list ) )
                            
                        else:
                        
                            # Nothing selected.
                            response_dictionary[ 'output_string' ] = "Add tag requested, but no records selected.  Did not add tag(s): " + str( ", ".join( reliability_names_tag_in_list ) )
    
                        #-- END check to make sure at least one selected. --#
                        
                    else:
                    
                        # when adding tags, must specify at least one tag.
                        response_dictionary[ 'output_string' ] = "Add tag requested, but no tags specified.  Nothing updated."        

                    #-- END check to see if tags --#
                    
                # remove tag(s)?
                elif ( reliability_names_action_IN == ReliabilityNamesActionForm.RELIABILITY_NAMES_ACTION_REMOVE_TAG ):
                
                    # ! ---- remove tags
                    
                    # first, make sure there is something in tag list.
                    tag_list_count = len( reliability_names_action_tag_list )
                    if ( tag_list_count > 0 ):
                    
                        # got at least one tag - check to see if anything in select_id_list
                        select_count = len( select_id_list )
                        if ( select_count > 0 ):
                            
                            # loop over IDs, looking up record for each, then
                            #     remove tags.
                            remove_tag_counter = 0
                            for reliability_names_id in select_id_list:
                            
                                remove_tag_counter += 1
                                
                                # lookup record for ID.
                                reliability_names_instance = Reliability_Names.objects.get( pk = reliability_names_id )
                                
                                # add all tags in list
                                reliability_names_instance.tags.remove( *reliability_names_action_tag_list )
                                                                
                            #-- END loop over selected IDs. --#
                            
                            # update the action details list.
                            action_summary = "Removed tag(s): " + str( reliability_names_action_tag_list ) + " from " + str( remove_tag_counter ) + " Reliability_Names records."
                            action_detail_list.append( action_summary + " ==> IDs: " + str( select_id_list ) )
                            
                        else:
                        
                            # Nothing selected.
                            response_dictionary[ 'output_string' ] = "Remove tag requested, but no records selected.  Did not remove tag(s): " + str( ", ".join( reliability_names_tag_in_list ) )
    
                        #-- END check to make sure at least one selected. --#
                        
                    else:
                    
                        # when adding tags, must specify at least one tag.
                        response_dictionary[ 'output_string' ] = "Remove tag requested, but no tags specified.  Nothing updated."        

                    #-- END check to see if tags --#
                    
                #-- END check to see what action --#                


                # add action_summary and action_detail_list to the response
                #     dictionary.
                response_dictionary[ "action_summary" ] = action_summary
                response_dictionary[ "action_detail_list" ] = action_detail_list
    
            else:
            
                # no merge_action
                response_dictionary[ 'output_string' ] = "No Reliability_Name action set.  Nothing to see here."        
                
            #-- END check to see if merge_action present. --#
            
        else:
        
            # not valid - render the form again
            response_dictionary[ 'output_string' ] = "Reliability_Name action form is not valid."

        #-- END check to see whether or not form is valid. --#

    else:
    
        # new request, just use empty instance of form created and stored above.
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
    current_result = None
    sum_dictionary = {}
    sum_dict_helper = None
    average_dictionary = {}
    #average_dict_helper = None
    column_name_list = None
    current_column_name = ""
    result_counter = -1
    current_result_value = None
    current_sum = -1
    current_average = -1
    
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
                      
                    # ! use QuerySet to calculate some averages, for both author and subject:
                    # - detect %
                    # - detect A
                    # - detect pi
                    # - lookup %
                    # - lookup A
                    # - lookup NZ %
                    # - lookup NZ A
                    # - lookup N
                    # - type %
                    # - type A
                    
                    # initialize dictionary to store sums.
                    sum_dictionary = {}
                    sum_dict_helper = DictHelper()
                    sum_dict_helper.set_dictionary( sum_dictionary )
                    
                    # ! make list of column names.
                    column_name_list = []
    
                    # authors
                    column_name_list.append( "author_count" )
                    column_name_list.append( "author_detect_percent" )
                    column_name_list.append( "author_detect_alpha" )
                    column_name_list.append( "author_detect_pi" )
                    column_name_list.append( "author_lookup_percent" )
                    column_name_list.append( "author_lookup_alpha" )
                    column_name_list.append( "author_lookup_non_zero_percent" )
                    column_name_list.append( "author_lookup_non_zero_alpha" )
                    column_name_list.append( "author_lookup_non_zero_count" )
                    column_name_list.append( "author_type_percent" )
                    column_name_list.append( "author_type_alpha" )
                    column_name_list.append( "author_type_pi" )
                    column_name_list.append( "author_type_non_zero_percent" )
                    column_name_list.append( "author_type_non_zero_alpha" )
                    column_name_list.append( "author_type_non_zero_pi" )
                    column_name_list.append( "author_type_non_zero_count" )
                    
                    # subjects
                    column_name_list.append( "subject_count" )
                    column_name_list.append( "subject_detect_percent" )
                    column_name_list.append( "subject_detect_alpha" )
                    column_name_list.append( "subject_detect_pi" )
                    column_name_list.append( "subject_lookup_percent" )
                    column_name_list.append( "subject_lookup_alpha" )
                    column_name_list.append( "subject_lookup_non_zero_percent" )
                    column_name_list.append( "subject_lookup_non_zero_alpha" )
                    column_name_list.append( "subject_lookup_non_zero_count" )
                    column_name_list.append( "subject_type_percent" )
                    column_name_list.append( "subject_type_alpha" )
                    column_name_list.append( "subject_type_pi" )
                    column_name_list.append( "subject_type_non_zero_percent" )
                    column_name_list.append( "subject_type_non_zero_alpha" )
                    column_name_list.append( "subject_type_non_zero_pi" )
                    column_name_list.append( "subject_type_non_zero_count" )
                    column_name_list.append( "subject_first_quote_graf_percent" )
                    column_name_list.append( "subject_first_quote_graf_alpha" )
                    column_name_list.append( "subject_first_quote_graf_pi" )
                    column_name_list.append( "subject_first_quote_graf_count" )
                    column_name_list.append( "subject_first_quote_index_percent" )
                    column_name_list.append( "subject_first_quote_index_alpha" )
                    column_name_list.append( "subject_first_quote_index_pi" )
                    column_name_list.append( "subject_first_quote_index_count" )
                    column_name_list.append( "subject_organization_hash_percent" )
                    column_name_list.append( "subject_organization_hash_alpha" )
                    column_name_list.append( "subject_organization_hash_pi" )
                    column_name_list.append( "subject_organization_hash_count" )
                    
                    # ! initialize all to 0
                    for current_column_name in column_name_list:
                    
                        # set value for column name to 0.
                        sum_dict_helper.set_value( current_column_name, 0 )
                        
                    #-- END loop over column names to set to 0. --#
    
                    # loop over results to first get sums for each field.
                    result_counter = 0
                    for current_result in reliability_names_results_qs:
                        
                        # increment counter
                        result_counter += 1
                        
                        # update all counters
                        for current_column_name in column_name_list:
                        
                            # retrieve value from current_result.
                            current_result_value = getattr( current_result, current_column_name )
                            
                            # if not None, add it to the column's sum in the
                            #     average dictionary.
                            if ( current_result_value is not None ):

                                # non-None - add it.
                                sum_dict_helper.increment_decimal_value( current_column_name, current_result_value )
                                
                            #-- END check to see if value is non-None --#
                        
                        #-- END loop over column names --#
    
                    #-- END loop over results. --#
                    
                    # finally, loop over sums to calculate and store the
                    #     averages.
                    average_dictionary = {}
                    for current_column_name in column_name_list:
    
                        # get sum
                        current_sum = sum_dict_helper.get_value_as_decimal( current_column_name, None )
                        
                        # divide by record count.
                        current_average = current_sum / result_counter
                        
                        # place the average in average_dictionary.
                        average_dictionary[ current_column_name ] = current_average
    
                    #-- END loop over column names to calculate average. --#
                    
                    # place sum and average dictionaries in response.
                    response_dictionary[ "sum_dictionary" ] = sum_dictionary
                    response_dictionary[ "average_dictionary" ] = average_dictionary
    
                else:
                    
                    # no matches for label.
                    response_dictionary[ 'output_string' ] = "ERROR - no QuerySet returned from call to filter() for label " + str( reliability_names_results_label )

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
