from django.contrib import admin

# Register your models here.

# import code for AJAX select
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

# Import models
from sourcenet_analysis.models import Reliability_Names
from sourcenet_analysis.models import Reliability_Names_Evaluation
from sourcenet_analysis.models import Reliability_Ties

admin.site.register( Reliability_Names )
#admin.site.register( Reliability_Names_Evaluation )
admin.site.register( Reliability_Ties )

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
                'fields' : [ 'event_type', 'person_name', 'persons', 'article', 'reliability_names', 'original_reliability_names_id', 'article_datas', 'status', 'status_message', 'notes', 'is_ground_truth_fixed', 'is_deleted', 'is_automated_error', 'is_single_name', 'label', 'tags' ]
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

    list_display = ( 'id', 'event_type', 'person_name', 'original_reliability_names_id', 'status', 'status_message', 'label', 'article' )
    list_display_links = ( 'id', 'event_type', 'original_reliability_names_id', 'person_name', 'status', 'status_message', 'label' )
    list_filter = [ 'label', 'event_type', 'is_ground_truth_fixed', 'is_deleted', 'is_automated_error', 'is_single_name', 'status' ]
    search_fields = [ 'person_name', 'status', 'status_message', 'notes', 'event_type' ]
    date_hierarchy = 'create_date'
    
#-- END admin class Reliability_Names_EvaluationAdmin --#

admin.site.register( Reliability_Names_Evaluation, Reliability_Names_EvaluationAdmin )