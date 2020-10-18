from django.contrib import admin

# Register your models here.

import six
from six.moves import range

# Import models
from context_analysis.models import Reliability_Names
from context_analysis.models import Reliability_Names_Eval
from context_analysis.models import Reliability_Ties

#admin.site.register( Reliability_Names )
#admin.site.register( Reliability_Names_Eval )
admin.site.register( Reliability_Ties )

#-------------------------------------------------------------------------------
# Reliability_Names_Eval admin definition
#-------------------------------------------------------------------------------

class Reliability_NamesAdmin( admin.ModelAdmin ):

    # ajax-based autocomplete
    autocomplete_fields = [ 'person', 'article' ]

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
        
            # build field name.
            current_field_name = Reliability_Names.build_field_name( coder_number, current_suffix )
                    
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
# Reliability_Names_Eval admin definition
#-------------------------------------------------------------------------------

class Reliability_Names_EvalAdmin( admin.ModelAdmin ):

    # ajax-based autocomplete
    autocomplete_fields = [ 'reliability_names', 'persons', 'article', 'article_datas', 'merged_from_ad', 'merged_to_ad' ]

    fieldsets = [
        (
            None,
            {
                'fields' : [ 'label', 'event_type', 'person_name', 'persons', 'article', 'reliability_names', 'original_reliability_names_id', 'article_datas', 'status', 'status_message', 'notes', 'tags' ]
            }
        ),
        (
            "Article Information",
            {
                'fields' : [ 'is_not_hard_news', 'is_list', 'is_sports',  ],
            }
        ),
        (
            "Work columns",
            {
                'fields' : [ 'is_to_do', 'work_status', 'is_skipped', 'is_ground_truth_fixed', 'is_single_name', 'is_duplicate', 'is_deleted' ]
            }
        ),
        (
            "Basic Error Codes",
            {
                'fields' : [ 'is_error', 'is_human_error', 'is_automated_error' ],
            }
        ),
        (
            "Basic Error Meta-Data",
            {
                'fields' : [ 'is_missed_author', 'is_missed_subject', 'is_author_shb_subject', 'is_subject_shb_author', 'is_quoted_shb_mentioned', 'is_mentioned_shb_quoted', 'is_wrong_text_captured', 'is_not_a_person', 'is_a_company', 'is_a_place', 'is_complex', 'is_interesting' ],
                'classes' : ( "collapse", )
            }
        ),
        (
            "Detailed Error Meta-Data",
            {
                'fields' : [ 'is_ambiguous', 'is_attribution_compound', 'is_attribution_follow_on', 'is_attribution_pronoun', 'is_attribution_second_hand', 'is_compound_names', 'is_contributed_to', 'is_dictionary_error', 'is_disambiguation', 'is_editing_error', 'is_foreign_names', 'is_gender_confusion', 'is_initials_error', 'is_layout_or_design', 'is_lookup_error', 'is_no_html', 'is_possessive', 'is_pronouns', 'is_proper_noun', 'is_quote_distance', 'is_said_verb', 'is_short_n_gram', 'is_software_error', 'is_spanish', 'is_straightforward', 'is_title', 'is_title_complex', 'is_title_prefix' ],
                'classes' : ( "collapse", )
            }
        ),
        (
            "Merge Detail",
            {
                'fields' : [ 'merged_from_reliability_names_id', 'merged_from_ad', 'merged_to_reliability_names_id', 'merged_to_ad' ],
                'classes' : ( "collapse", )
            }
        ),
    ]

    list_display = ( 'id', 'last_modified', 'event_type', 'person_name', 'original_reliability_names_id', 'status', 'status_message', 'label', 'article' )
    list_display_links = ( 'id', 'event_type', 'original_reliability_names_id', 'person_name', 'status', 'status_message', 'label' )
    list_filter = [ 'label', 'event_type', 'status', 'is_not_hard_news', 'is_list', 'is_sports', 'is_to_do', 'work_status', 'is_skipped', 'is_ground_truth_fixed', 'is_single_name', 'is_duplicate', 'is_deleted', 'is_error', 'is_human_error', 'is_automated_error', 'is_missed_author', 'is_missed_subject', 'is_author_shb_subject', 'is_subject_shb_author', 'is_quoted_shb_mentioned', 'is_mentioned_shb_quoted', 'is_wrong_text_captured', 'is_not_a_person', 'is_a_company', 'is_a_place', 'is_complex', 'is_interesting', 'is_ambiguous', 'is_attribution_compound', 'is_attribution_follow_on', 'is_attribution_pronoun', 'is_attribution_second_hand', 'is_compound_names', 'is_contributed_to', 'is_dictionary_error', 'is_disambiguation', 'is_editing_error', 'is_foreign_names', 'is_gender_confusion', 'is_initials_error', 'is_layout_or_design', 'is_lookup_error', 'is_no_html', 'is_possessive', 'is_pronouns', 'is_proper_noun', 'is_quote_distance', 'is_said_verb', 'is_short_n_gram', 'is_software_error', 'is_spanish', 'is_straightforward', 'is_title', 'is_title_complex', 'is_title_prefix' ]
    search_fields = [ 'person_name', 'status', 'status_message', 'notes', 'event_type', 'work_status', 'label' ]
    date_hierarchy = 'create_date'
    
#-- END admin class Reliability_Names_EvalAdmin --#

admin.site.register( Reliability_Names_Eval, Reliability_Names_EvalAdmin )