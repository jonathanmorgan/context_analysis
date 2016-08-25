from __future__ import unicode_literals

'''
Copyright 2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet.

sourcenet is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet. If not, see http://www.gnu.org/licenses/.
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
    
    RELIABILITY_NAMES_ACTION_CHOICES = (
        ( RELIABILITY_NAMES_ACTION_LOOKUP, "Lookup (no changes)" ),
        ( RELIABILITY_NAMES_ACTION_DELETE, "Delete Selected" ),
        ( RELIABILITY_NAMES_ACTION_MERGE_CODING, "Merge Coding --> FROM 1 SELECTED / INTO 1" ),
    )
    
    # other constants
    INPUT_NAME_SELECT_PREFIX = "select_person_id_"
    INPUT_NAME_MERGE_INTO_PREFIX = "merge_into_person_id_"

    #===========================================================================
    # ! ==> fields
    #===========================================================================

    reliability_names_action = forms.ChoiceField( required = False, choices = RELIABILITY_NAMES_ACTION_CHOICES )

#-- END Form class ReliabilityNamesActionForm --#


class ReliabilityNamesFilterForm( FormParent ):

    '''
    form to hold variables used in looking up Reliability_Names instances.
    '''

    # label
    reliability_names_label = forms.CharField( required = True, label = "Label" )
    reliability_names_coder_count = forms.CharField( required = True, label = "Coders to compare (1 through ==>)" )
    reliability_names_only_disagree = forms.BooleanField( required = False, label = "Limit to disagreements?" )
    reliability_names_include_optional_fields = forms.BooleanField( required = False, label = "Disagreements - Include optional fields?" )
    #reliability_names_coder_id_list = forms.CharField( required = True, label = "Coders to compare (separated by commas)" )

#-- END ReliabilityNamesFilterForm --#


class ReliabilityNamesResultsForm( forms.Form ):

    '''
    form to hold variables used in looking up Reliability_Names_Results for a
        given label.
    '''

    # label
    reliability_names_results_label = forms.CharField( required = True, label = "Label" )

#-- END ReliabilityNamesResultsForm --#
