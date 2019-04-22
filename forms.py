from __future__ import unicode_literals

'''
Copyright 2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context_analysis.

context_analysis is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context_analysis is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context_analysis. If not, see http://www.gnu.org/licenses/.
'''

# import django form object.
from django import forms

# python_utilities
from python_utilities.django_utils.django_form_helper import DjangoFormHelper
from python_utilities.django_utils.django_form_helper import FormParent
from python_utilities.django_utils.django_form_helper import ModelFormParent
from python_utilities.lists.list_helper import ListHelper
from python_utilities.logging.logging_helper import LoggingHelper


class ReliabilityNamesActionForm( FormParent ):
        
    '''
    Allows user to select from different types of actions to perform on selected
        Reliability_Names rows.  To start, delete and merge coding.
    '''
    
    #===========================================================================
    # ! ==> CONSTANTS-ISH
    #===========================================================================
    
    # merge_action choices
    RELIABILITY_NAMES_ACTION_LOOKUP = "lookup"
    RELIABILITY_NAMES_ACTION_DELETE = "delete"
    RELIABILITY_NAMES_ACTION_MERGE_CODING = "merge_coding"
    RELIABILITY_NAMES_ACTION_ADD_TAG = "add_tag"
    RELIABILITY_NAMES_ACTION_REMOVE_TAG = "remove_tag"    
    
    RELIABILITY_NAMES_ACTION_CHOICES = (
        ( RELIABILITY_NAMES_ACTION_LOOKUP, "Lookup (no changes)" ),
        ( RELIABILITY_NAMES_ACTION_DELETE, "Delete Selected" ),
        ( RELIABILITY_NAMES_ACTION_MERGE_CODING, "Merge Coding --> FROM 'select' TO 'merge INTO'" ),
        ( RELIABILITY_NAMES_ACTION_ADD_TAG, "Add tag(s) to selected" ),
        ( RELIABILITY_NAMES_ACTION_REMOVE_TAG, "Remove tag(s) from selected" ),
    )
    
    # other constants
    INPUT_NAME_SELECT_PREFIX = "select_person_id_"
    INPUT_NAME_MERGE_INTO_PREFIX = "merge_into_person_id_"

    #===========================================================================
    # ! ==> fields
    #===========================================================================

    reliability_names_action = forms.ChoiceField( required = False, choices = RELIABILITY_NAMES_ACTION_CHOICES )
    reliability_names_action_tag_list = forms.CharField( required = False, label = "Tag(s) - (comma-delimited)" )

#-- END Form class ReliabilityNamesActionForm --#


class ReliabilityNamesFilterForm( FormParent ):

    '''
    form to hold variables used in looking up Reliability_Names instances.
    '''

    # filter_type choices
    RELIABILITY_NAMES_FILTER_TYPE_LOOKUP = "lookup"
    RELIABILITY_NAMES_FILTER_TYPE_ONLY_DISAGREE = "only_disagree"
    
    RELIABILITY_NAMES_FILTER_TYPE_CHOICES = (
        ( RELIABILITY_NAMES_FILTER_TYPE_LOOKUP, "Lookup" ),
        ( RELIABILITY_NAMES_FILTER_TYPE_ONLY_DISAGREE, "Disagree (only rows with disagreement between coders)" ),
    )
    
    # label
    reliability_names_label = forms.CharField( required = True, label = "Label" )
    reliability_names_coder_count = forms.CharField( required = True, label = "Coders to compare (1 through ==>)" )
    reliability_names_filter_type = forms.ChoiceField( required = True, choices = RELIABILITY_NAMES_FILTER_TYPE_CHOICES )
    reliability_names_id_in_list = forms.CharField( required = False, label = "[Lookup] - Reliability_Names IDs (comma-delimited)" )
    reliability_names_tag_in_list = forms.CharField( required = False, label = "[Lookup] - Reliability_Names tags (comma-delimited)" )    
    reliability_names_article_id_in_list = forms.CharField( required = False, label = "[Lookup] - Associated Article IDs (comma-delimited)" )
    reliability_names_only_first_name = forms.BooleanField( required = False, label = "[Lookup] - Person has first name, no other name parts." )
    reliability_names_include_optional_fields = forms.BooleanField( required = False, label = "[Disagree] - Include optional fields?" )

#-- END ReliabilityNamesFilterForm --#


class ReliabilityNamesResultsForm( forms.Form ):

    '''
    form to hold variables used in looking up Reliability_Names_Results for a
        given label.
    '''

    # label
    reliability_names_results_label = forms.CharField( required = True, label = "Label" )

#-- END ReliabilityNamesResultsForm --#
