"""
To add a new ajax select:
- Include the import for the model class you will be selecting from at the top of this file (put it in alphabetical order).
- In this file, make a new class that extends LookupParent for the model you want to lookup using AJAX-selects (It is OK to just copy one of the other ones here).  Place it in alphabetical order in the file.
- Modify the get_query() and get_objects() methods to reference the correct model, fields in that model.
- If django 1.6 or earlier, in settings.py, add a line for your new channel to the AJAX_LOOKUP_CHANNELS property, like this, for person:
    'person' : ('sourcenet.lookups', 'PersonLookup'),
- In admin.py, either add or edit a form attribute to include your channel, and to tell the admin which field to map to which AJAX lookup.  So, for example, in Article, there is the following line:

        form = make_ajax_form( Article_Subject, dict( person = 'person', ) )

    - This line says, for Article_Subject, when entering 'person' field, lookup using the 'person' AJAX lookup channel.
    - The field names are the names from the model class definition, and can be any type of relation.  Channel names are the @register decorator contents in this file, or if django <= 1.6, the keys in AJAX_LOOKUP_CHANNELS in your settings.py file.
    - So, If you were to add a lookup for organization, then you'd have:

            form = make_ajax_form( Article_Subject, dict( person = 'person', subject_organization = 'organization', ) )

- To use in a plain django Form, use `ajax_select.make_ajax_field` inside a ModelForm child, assigned to a variable named for the field you want to look up:

    - person  = make_ajax_field( Article_Subject, 'person', 'coding_person', help_text = None )
"""

# python imports
import logging

# django imports
from django.db.models import Q

# sourcenet imports
import sourcenet.lookups

# sourcenet_analysis imports
from sourcenet_analysis.models import Reliability_Names

# python_utilities - logging
from python_utilities.logging.logging_helper import LoggingHelper

# ajax_select imports
from ajax_select import register, LookupChannel


#===============================================================================#
# Debug logging
#===============================================================================#


DEBUG = False

def output_debug( message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = "" ):
    
    '''
    Accepts message string.  If debug is on, logs it.  If not,
       does nothing for now.
    '''
    
    # declare variables
    my_message = ""
    my_logger = None
    my_logger_name = ""

    # got a message?
    if ( message_IN ):
    
        # only print if debug is on.
        if ( DEBUG == True ):
        
            my_message = message_IN
        
            # got a method?
            if ( method_IN ):
            
                # We do - append to front of message.
                my_message = "In " + method_IN + ": " + my_message
                
            #-- END check to see if method passed in --#
            
            # indent?
            if ( indent_with_IN ):
                
                my_message = indent_with_IN + my_message
                
            #-- END check to see if we indent. --#
        
            # debug is on.  Start logging rather than using print().
            #print( my_message )
            
            # got a logger name?
            my_logger_name = "sourcenet_analysis.lookups"
            if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):
            
                # use logger name passed in.
                my_logger_name = logger_name_IN
                
            #-- END check to see if logger name --#
                
            # get logger
            my_logger = LoggingHelper.get_a_logger( my_logger_name )
            
            # log debug.
            my_logger.debug( my_message )
        
        #-- END check to see if debug is on --#
    
    #-- END check to see if message. --#

#-- END method output_debug() --#


#===============================================================================#
# Individual child Lookup classes
#===============================================================================#


@register( "reliability_names" )
class Reliability_NamesLookup( sourcenet.lookups.LookupParent ):

    my_class = Reliability_Names	

    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an article?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( person_name__icontains = q )
                                                          | Q( person_type__icontains = q )
                                                          | Q( notes__icontains = q )
                                                          | Q( label__icontains = q )
                                                        )

        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'label', 'article', 'person_name' )

    #-- END method get_objects --#

#-- END class Reliability_NamesLookup --#
