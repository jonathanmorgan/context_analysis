from django.contrib import admin

# Register your models here.

import six
from six.moves import range

# import code for AJAX select
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

# Import models
from sourcenet_analysis.models import Reliability_Names
from sourcenet_analysis.models import Reliability_Names_Evaluation
from sourcenet_analysis.models import Reliability_Ties

#admin.site.register( Reliability_Names )
#admin.site.register( Reliability_Names_Evaluation )
admin.site.register( Reliability_Ties )

#-------------------------------------------------------------------------------
# Reliability_Names_Evaluation admin definition
#-------------------------------------------------------------------------------

class Reliability_NamesAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #     are looking to make ajax selects form fields for; 2nd argument is a
    #     dict of pairs of field names in the model in argument 1 (with no quotes
    #     around them) mapped to lookup channels used to service them (lookup
    #     channels are defined in settings.py, implemented in a separate module -
    #     in this case, implemented in sourcenet/lookups.py and
    #     sourcenet_analysis/lookups.py
    form = make_ajax_form( Reliability_Names, dict( person = 'person', article = 'article' ) )

    fieldsets = [
        (
            None,
            {
                'fields' : [ 'article', 'person', 'person_name', 'person_first_name', 'person_last_name', 'person_type', 'label', 'notes', 'tags' ]
            }
        )
    ]
    
    # declare variables - add on entries for each coder.
    coder_number = -1
    coder_number_string = None
    fields_list = None
    current_field_name = None
    current_suffix = None
    field_set_name = None
    field_set_tuple = None
    
    # add on entries for each coder.
    for coder_number in range( 1, 11 ):
    
        # Make field list
        coder_number_string = str( coder_number )
        fields_list = []
        current_field_name = ""
        
        # render field set name.
        field_set_name = "Coder " + coder_number_string
        
        # loop over suffixes
        for current_suffix in Reliability_Names.ALL_FIELD_NAME_SUFFIX_LIST:
        
            # start field name.
            current_field_name = Reliability_Names.FIELD_NAME_PREFIX_CODER + coder_number_string
        
            # check if value empty (there is one empty, which is intentional,
            #     for the actual coder Foreign Key).
            if ( ( current_suffix is not None ) and ( current_suffix != "" ) ):
            
                # append.
                current_field_name += "_" + current_suffix
            
            #-- END check to see if suffix empty or None --#
            
            # append to the list.
            fields_list.append( current_field_name )
            
        #-- END loop over suffixes --#
        
        # add field set for the current coder.
        field_set_tuple = (
            field_set_name,
            {
                'fields' : fields_list,
                'classes' : ( "collapse", )
            }
        )
        fieldsets.append( field_set_tuple )

    #-- END loop over coders. --#

    list_display = ( 'id', 'person_name', 'person_type', 'label', 'article' )
    list_display_links = ( 'id', 'person_name', 'person_type', 'label' )
    list_filter = [ 'label', 'person_type' ]
    search_fields = [ 'person_name', 'person_type', 'label', 'notes' ]
    date_hierarchy = 'create_date'
    
#-- END admin class Reliability_NamesAdmin --#

admin.site.register( Reliability_Names, Reliability_NamesAdmin )

#-------------------------------------------------------------------------------
# Reliability_Names_Evaluation admin definition
#-------------------------------------------------------------------------------

class Reliability_Names_EvaluationAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #     are looking to make ajax selects form fields for; 2nd argument is a
    #     dict of pairs of field names in the model in argument 1 (with no quotes
    #     around them) mapped to lookup channels used to service them (lookup
    #     channels are defined in settings.py, implemented in a separate module -
    #     in this case, implemented in sourcenet/lookups.py and
    #     sourcenet_analysis/lookups.py
    form = make_ajax_form( Reliability_Names_Evaluation, dict( reliability_names = 'reliability_names', persons = 'person', article = 'article', article_datas = 'article_data', merged_from_article_data = 'article_data', merged_to_article_data = 'article_data' ) )

    fieldsets = [
        (
            None,
            {
                'fields' : [ 'event_type', 'person_name', 'persons', 'article', 'reliability_names', 'original_reliability_names_id', 'article_datas', 'status', 'status_message', 'notes', 'is_ground_truth_fixed', 'is_deleted', 'is_automated_error', 'is_single_name', 'is_ambiguous', 'label', 'tags' ]
            }
        ),
        (
            "Merge Detail",
            {
                'fields' : [ 'merged_from_reliability_names_id', 'merged_from_article_data', 'merged_to_reliability_names_id', 'merged_to_article_data' ],
                'classes' : ( "collapse", )
            }
        ),
    ]

    list_display = ( 'id', 'last_modified', 'event_type', 'person_name', 'original_reliability_names_id', 'status', 'status_message', 'label', 'article' )
    list_display_links = ( 'id', 'event_type', 'original_reliability_names_id', 'person_name', 'status', 'status_message', 'label' )
    list_filter = [ 'label', 'event_type', 'is_ground_truth_fixed', 'is_deleted', 'is_automated_error', 'is_single_name', 'is_ambiguous', 'status' ]
    search_fields = [ 'person_name', 'status', 'status_message', 'notes', 'event_type' ]
    date_hierarchy = 'create_date'
    
#-- END admin class Reliability_Names_EvaluationAdmin --#

admin.site.register( Reliability_Names_Evaluation, Reliability_Names_EvaluationAdmin )