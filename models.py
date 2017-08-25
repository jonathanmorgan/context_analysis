# start to support python 3:
from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet_analysis.

sourcenet_analysis is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

sourcenet_analysis is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with http://github.com/jonathanmorgan/sourcenet_analysis.  If not, see
<http://www.gnu.org/licenses/>.
'''

# imports - six
import six
from six.moves import range

# taggit tagging APIs
from taggit.managers import TaggableManager

# django imports
from django.contrib.auth.models import User
from django.db import models

# django encoding imports (for supporting 2 and 3).
import django.utils.encoding
from django.utils.encoding import python_2_unicode_compatible

# python utilities
from python_utilities.analysis.statistics.stats_helper import StatsHelper
from python_utilities.logging.logging_helper import LoggingHelper
from python_utilities.status.status_container import StatusContainer
from python_utilities.strings.string_helper import StringHelper

# sourcenet imports
from sourcenet.models import Article
from sourcenet.models import Article_Author
from sourcenet.models import Article_Data
from sourcenet.models import Article_Person
from sourcenet.models import Article_Subject
from sourcenet.models import Person
from sourcenet.shared.person_details import PersonDetails


# Debugging code, shared across all models.

DEBUG = True

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
            my_logger_name = "sourcenet.models"
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


#==============================================================================#
# ! Analysis models
#==============================================================================#


@python_2_unicode_compatible
class Reliability_Names( models.Model ):

    '''
    Class to hold information on name detection choices within a given article
        across coders, for use in inter-coder reliability testing.  Intended to
        be read or exported for use by statistical analysis packages (numpy, R, 
        etc.).  Example of how to populate this table:
        
        sourcenet_analysis/examples/reliability/reliability-build_name_data.py
       
        Examples of calculating reliability TK.
       
        Includes columns for ten coders.  If you need more, add more sets of
        coder columns.
    '''

    #----------------------------------------------------------------------
    # ! ==> constants-ish
    #----------------------------------------------------------------------    


    # logging
    LOGGER_NAME = "sourcenet_analysis.models.Reliability_Names"

    # maximum index value
    MAX_INDEX = 10

    # field types
    FIELD_TYPE_FOREIGN_KEY = "foreign_key"
    FIELD_TYPE_INTEGER = "integer"
    FIELD_TYPE_STRING = "string"
    FIELD_TYPE_NON_ZERO_INTEGER = "non_zero_integer"
    FIELD_NAME_DEFAULT_SUFFIX = FIELD_TYPE_STRING

    # field names
    FIELD_NAME_LABEL = "label"
    FIELD_NAME_PREFIX_CODER = "coder"
    FIELD_NAME_SUFFIX_CODER = ""
    FIELD_NAME_SUFFIX_CODER_ID = "coder_id"
    FIELD_NAME_SUFFIX_DETECTED = "detected"
    FIELD_NAME_SUFFIX_PERSON_ID = "person_id"
    FIELD_NAME_SUFFIX_PERSON_TYPE = "person_type"
    FIELD_NAME_SUFFIX_PERSON_TYPE_INT = "person_type_int"
    FIELD_NAME_SUFFIX_ARTICLE_DATA_ID = "article_data_id"
    FIELD_NAME_SUFFIX_ARTICLE_PERSON_ID = "article_person_id"
    FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF = "first_quote_graf"
    FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX = "first_quote_index"
    FIELD_NAME_SUFFIX_ORGANIZATION_HASH = "organization_hash"
    FIELD_NAME_TAGS = "tags"

    # make list of all fields
    ALL_FIELD_NAME_SUFFIX_LIST = [
        FIELD_NAME_SUFFIX_CODER,
        FIELD_NAME_SUFFIX_CODER_ID,
        FIELD_NAME_SUFFIX_DETECTED,
        FIELD_NAME_SUFFIX_PERSON_ID,
        FIELD_NAME_SUFFIX_PERSON_TYPE,
        FIELD_NAME_SUFFIX_PERSON_TYPE_INT,
        FIELD_NAME_SUFFIX_ARTICLE_DATA_ID,
        FIELD_NAME_SUFFIX_ARTICLE_PERSON_ID,
        FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF,
        FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX,
        FIELD_NAME_SUFFIX_ORGANIZATION_HASH,
    ]

    # make dictionary of field suffixes to field types.
    FIELD_NAME_SUFFIX_TO_TYPE_MAP = {}
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_CODER ] = FIELD_TYPE_FOREIGN_KEY
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_CODER_ID ] = FIELD_TYPE_NON_ZERO_INTEGER
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_DETECTED ] = FIELD_TYPE_INTEGER
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_PERSON_ID ] = FIELD_TYPE_NON_ZERO_INTEGER
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_PERSON_TYPE ] = FIELD_TYPE_STRING
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_PERSON_TYPE_INT ] = FIELD_TYPE_NON_ZERO_INTEGER
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_ARTICLE_DATA_ID ] = FIELD_TYPE_NON_ZERO_INTEGER
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_ARTICLE_PERSON_ID ] = FIELD_TYPE_NON_ZERO_INTEGER
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF ] = FIELD_TYPE_INTEGER
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX ] = FIELD_TYPE_INTEGER
    FIELD_NAME_SUFFIX_TO_TYPE_MAP[ FIELD_NAME_SUFFIX_ORGANIZATION_HASH ] = FIELD_TYPE_STRING

    # make lists of fields that are tested for agreement...
    DEFAULT_AGREEMENT_FIELD_SUFFIX_LIST = [ FIELD_NAME_SUFFIX_DETECTED, FIELD_NAME_SUFFIX_PERSON_ID, FIELD_NAME_SUFFIX_PERSON_TYPE, ]
    OPTIONAL_AGREEMENT_FIELD_SUFFIX_LIST = [ FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF, FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX, FIELD_NAME_SUFFIX_ORGANIZATION_HASH ]

    # property names for building disagreement output (if ues this elsewhere,
    #     make Disagreement and DisagreementDetail objects).
    PROP_NAME_INDEX = "index"
    PROP_NAME_INSTANCE = "instance"
    PROP_NAME_ID = "id"
    PROP_NAME_LABEL = FIELD_NAME_LABEL
    PROP_NAME_ARTICLE_ID = "article_id"
    PROP_NAME_PERSON_NAME = "person_name"
    PROP_NAME_PERSON_FIRST_NAME = "person_first_name"
    PROP_NAME_PERSON_LAST_NAME = "person_last_name"    
    PROP_NAME_PERSON_ID = FIELD_NAME_SUFFIX_PERSON_ID
    PROP_NAME_PERSON_TYPE = FIELD_NAME_SUFFIX_PERSON_TYPE
    PROP_NAME_CODER_DETAILS_LIST = "coder_details_list"
    PROP_NAME_CODER_ID = FIELD_NAME_SUFFIX_CODER_ID
    PROP_NAME_CODER_DETECTED = "coder_" + FIELD_NAME_SUFFIX_DETECTED
    PROP_NAME_CODER_PERSON_ID = "coder_" + FIELD_NAME_SUFFIX_PERSON_ID
    PROP_NAME_CODER_PERSON_TYPE = "coder_" + FIELD_NAME_SUFFIX_PERSON_TYPE
    PROP_NAME_CODER_FIRST_QUOTE_GRAF = "coder_" + FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF
    PROP_NAME_CODER_FIRST_QUOTE_INDEX = "coder_" + FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX
    PROP_NAME_CODER_ORGANIZATION_HASH = "coder_" + FIELD_NAME_SUFFIX_ORGANIZATION_HASH
    PROP_NAME_TAGS = FIELD_NAME_TAGS
    
    # DEFAULT ORDER
    DEFAULT_ORDER_COLUMN_LIST = [ "article", "person_type", "person_last_name", "person_first_name", "person_name", "person" ]
    DEFAULT_ORDER_BY = " ORDER BY article_id, person_type, person_last_name, person_first_name, person_name, person_id"
    
    # person type values
    PERSON_TYPE_SUBJECT = PersonDetails.PERSON_TYPE_SUBJECT
    PERSON_TYPE_SOURCE = PersonDetails.PERSON_TYPE_SOURCE
    PERSON_TYPE_AUTHOR = PersonDetails.PERSON_TYPE_AUTHOR
    
    # subjet types
    SUBJECT_TYPE_MENTIONED = PersonDetails.SUBJECT_TYPE_MENTIONED
    SUBJECT_TYPE_QUOTED = PersonDetails.SUBJECT_TYPE_QUOTED


    #----------------------------------------------------------------------
    # ! ==> model fields
    #----------------------------------------------------------------------


    article = models.ForeignKey( Article, blank = True, null = True )
    person = models.ForeignKey( Person, blank = True, null = True )
    person_name = models.CharField( max_length = 255, blank = True, null = True )
    person_first_name = models.CharField( max_length = 255, blank = True, null = True )
    person_last_name = models.CharField( max_length = 255, blank = True, null = True )
    person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder1 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder1_set" )
    coder1_coder_id = models.IntegerField( blank = True, null = True )
    coder1_detected = models.IntegerField( blank = True, null = True )
    coder1_person_id = models.IntegerField( blank = True, null = True )
    coder1_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder1_person_type_int = models.IntegerField( blank = True, null = True )
    coder1_article_data_id = models.IntegerField( blank = True, null = True )
    coder1_article_person_id = models.IntegerField( blank = True, null = True )
    coder1_first_quote_graf = models.IntegerField( blank = True, null = True )
    coder1_first_quote_index = models.IntegerField( blank = True, null = True )
    coder1_organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    coder2 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder2_set" )
    coder2_coder_id = models.IntegerField( blank = True, null = True )
    coder2_detected = models.IntegerField( blank = True, null = True )
    coder2_person_id = models.IntegerField( blank = True, null = True )
    coder2_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder2_person_type_int = models.IntegerField( blank = True, null = True )
    coder2_article_data_id = models.IntegerField( blank = True, null = True )
    coder2_article_person_id = models.IntegerField( blank = True, null = True )
    coder2_first_quote_graf = models.IntegerField( blank = True, null = True )
    coder2_first_quote_index = models.IntegerField( blank = True, null = True )
    coder2_organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    coder3 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder3_set" )
    coder3_coder_id = models.IntegerField( blank = True, null = True )
    coder3_detected = models.IntegerField( blank = True, null = True )
    coder3_person_id = models.IntegerField( blank = True, null = True )
    coder3_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder3_person_type_int = models.IntegerField( blank = True, null = True )
    coder3_article_data_id = models.IntegerField( blank = True, null = True )
    coder3_article_person_id = models.IntegerField( blank = True, null = True )
    coder3_first_quote_graf = models.IntegerField( blank = True, null = True )
    coder3_first_quote_index = models.IntegerField( blank = True, null = True )
    coder3_organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    coder4 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder4_set" )
    coder4_coder_id = models.IntegerField( blank = True, null = True )
    coder4_detected = models.IntegerField( blank = True, null = True )
    coder4_person_id = models.IntegerField( blank = True, null = True )
    coder4_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder4_person_type_int = models.IntegerField( blank = True, null = True )
    coder4_article_data_id = models.IntegerField( blank = True, null = True )
    coder4_article_person_id = models.IntegerField( blank = True, null = True )
    coder4_first_quote_graf = models.IntegerField( blank = True, null = True )
    coder4_first_quote_index = models.IntegerField( blank = True, null = True )
    coder4_organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    coder5 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder5_set" )
    coder5_coder_id = models.IntegerField( blank = True, null = True )
    coder5_detected = models.IntegerField( blank = True, null = True )
    coder5_person_id = models.IntegerField( blank = True, null = True )
    coder5_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder5_person_type_int = models.IntegerField( blank = True, null = True )
    coder5_article_data_id = models.IntegerField( blank = True, null = True )
    coder5_article_person_id = models.IntegerField( blank = True, null = True )
    coder5_first_quote_graf = models.IntegerField( blank = True, null = True )
    coder5_first_quote_index = models.IntegerField( blank = True, null = True )
    coder5_organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    coder6 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder6_set" )
    coder6_coder_id = models.IntegerField( blank = True, null = True )
    coder6_detected = models.IntegerField( blank = True, null = True )
    coder6_person_id = models.IntegerField( blank = True, null = True )
    coder6_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder6_person_type_int = models.IntegerField( blank = True, null = True )
    coder6_article_data_id = models.IntegerField( blank = True, null = True )
    coder6_article_person_id = models.IntegerField( blank = True, null = True )
    coder6_first_quote_graf = models.IntegerField( blank = True, null = True )
    coder6_first_quote_index = models.IntegerField( blank = True, null = True )
    coder6_organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    coder7 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder7_set" )
    coder7_coder_id = models.IntegerField( blank = True, null = True )
    coder7_detected = models.IntegerField( blank = True, null = True )
    coder7_person_id = models.IntegerField( blank = True, null = True )
    coder7_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder7_person_type_int = models.IntegerField( blank = True, null = True )
    coder7_article_data_id = models.IntegerField( blank = True, null = True )
    coder7_article_person_id = models.IntegerField( blank = True, null = True )
    coder7_first_quote_graf = models.IntegerField( blank = True, null = True )
    coder7_first_quote_index = models.IntegerField( blank = True, null = True )
    coder7_organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    coder8 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder8_set" )
    coder8_coder_id = models.IntegerField( blank = True, null = True )
    coder8_detected = models.IntegerField( blank = True, null = True )
    coder8_person_id = models.IntegerField( blank = True, null = True )
    coder8_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder8_person_type_int = models.IntegerField( blank = True, null = True )
    coder8_article_data_id = models.IntegerField( blank = True, null = True )
    coder8_article_person_id = models.IntegerField( blank = True, null = True )
    coder8_first_quote_graf = models.IntegerField( blank = True, null = True )
    coder8_first_quote_index = models.IntegerField( blank = True, null = True )
    coder8_organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    coder9 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder9_set" )
    coder9_coder_id = models.IntegerField( blank = True, null = True )
    coder9_detected = models.IntegerField( blank = True, null = True )
    coder9_person_id = models.IntegerField( blank = True, null = True )
    coder9_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder9_person_type_int = models.IntegerField( blank = True, null = True )
    coder9_article_data_id = models.IntegerField( blank = True, null = True )
    coder9_article_person_id = models.IntegerField( blank = True, null = True )
    coder9_first_quote_graf = models.IntegerField( blank = True, null = True )
    coder9_first_quote_index = models.IntegerField( blank = True, null = True )
    coder9_organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    coder10 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder10_set" )
    coder10_coder_id = models.IntegerField( blank = True, null = True )
    coder10_detected = models.IntegerField( blank = True, null = True )
    coder10_person_id = models.IntegerField( blank = True, null = True )
    coder10_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder10_person_type_int = models.IntegerField( blank = True, null = True )
    coder10_article_data_id = models.IntegerField( blank = True, null = True )
    coder10_article_person_id = models.IntegerField( blank = True, null = True )
    coder10_first_quote_graf = models.IntegerField( blank = True, null = True )
    coder10_first_quote_index = models.IntegerField( blank = True, null = True )
    coder10_organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    label = models.CharField( max_length = 255, blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )

    # tags!
    tags = TaggableManager( blank = True )


    #----------------------------------------------------------------------------
    # ! ==> Meta class
    #----------------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:

        ordering = [ "article", "person_type", "person_last_name", "person_first_name", "person_name", "person" ]
        
    #-- END nested Meta class --#


    #----------------------------------------------------------------------------
    # ! ==> class methods
    #----------------------------------------------------------------------------


    @classmethod
    def build_field_name( cls, index_IN, suffix_IN, *args, **kwargs ):
        
        '''
        Accepts index and suffix, uses them to construct field name.
        '''
        
        # return reference
        value_OUT = ""
        
        # construct field name
        value_OUT = cls.FIELD_NAME_PREFIX_CODER + str( index_IN )
        
        # is there a suffix?
        if ( ( suffix_IN is not None ) and ( suffix_IN != "" ) ):
        
            # yes.  does it begin with an underscore?
            if ( suffix_IN.startswith( "_" ) == False ):
            
                # no.  Add one.
                value_OUT += "_"
                
            #-- END check to see if underscore --#
            
            # add the suffix.
            value_OUT += suffix_IN
        
        #-- END check to see if suffix --#
        
        return value_OUT
        
    #-- END class method build_field_name() --#
        
    
    @classmethod
    def delete_reliabilty_names_for_article( cls, article_id_IN, label_IN = None, do_delete_IN = True ):
        
        '''
        Accepts article ID and optional label.  Finds all Reliability_Names
            records in that reference article ID and have label (if requested).
            Removes all matches.  Returns list of str() of each record removed.
        '''
        
        # return reference
        record_list_OUT = []
        
        # declare variables
        article_id = -1
        label = ""
        matching_names_qs = None
        current_record = None
        current_record_string = None
        do_delete = True
        
        # first, get existing Reliability_Names rows for article and label.
        article_id = article_id_IN
        label = label_IN
        do_delete = do_delete_IN
        
        # get matching Reliability_Names rows
        matching_names_qs = Reliability_Names.objects.all()
        matching_names_qs = matching_names_qs.filter( article__id = article_id )
        
        # got a label?
        if ( ( label is not None ) and ( label != "" ) ):
            
            # yes - filter.
            matching_names_qs = matching_names_qs.filter( label = label )
            
        #-- END check to see if label. --#
        
        print( "Found " + str( matching_names_qs.count() ) + " records." )
        
        # delete these records.
        for current_record in matching_names_qs:
        
            # add the str() of the row to the list.
            current_record_string = str( current_record )
            
            # DELETE?
            if ( do_delete == True ):
                
                # yes.  delete()
                current_record_string = "- delete()-ing: " + current_record_string
                current_record.delete()
                
            else:
                
                # print info on record.
                current_record_string = "- match: " + current_record_string
                
            #-- END check to see if we delete. --#
            
            record_list_OUT.append( current_record_string )
            
        #-- END loop over matching Reliability_Names --#
        
        return record_list_OUT
        
    #-- END class method delete_reliabilty_names_for_article() --#


    @classmethod
    def lookup_disagreements( cls,
                              label_IN = "",
                              coder_count_IN = -1,
                              include_optional_IN = False,
                              order_by_IN = None,
                              *args,
                              **kwargs ):
        
        # return reference
        qs_OUT = None
        
        # declare variables
        my_label = ""
        my_coder_count = -1
        current_outer_index = -1
        current_inner_index = -1

        # declare variables - building up SQL statement.
        sql_string = ""
        sql_temp_string = ""
        sql_detected_list = []
        sql_person_id_list = []
        sql_person_type_list = []
        sql_quote_graf_list = []
        sql_quote_index_list = []
        sql_org_hash_list = []
        sql_raw_params_list = []
        
        # do we have a label?
        if ( ( label_IN is not None ) and ( label_IN != "" ) ):

            # yes - use it.
            my_label = label_IN
        
        #-- END check to see if label --#
        
        # got coder_count_IN?
        if ( ( coder_count_IN is not None ) and ( coder_count_IN != "" ) and ( int( coder_count_IN ) > 2 ) ):
        
            # yes, and is at least 2.  Use it.
            my_coder_count = int( coder_count_IN )
        
        else:
        
            # no, or not at least 2.  Default to 2.
            my_coder_count = 2
            
        #-- END check to see if coder count passed in. --#
        
        # loop over coders we've been asked to compare
        sql_detected_list = []
        sql_person_id_list = []
        sql_person_type_list = []
        sql_quote_graf_list = []
        sql_quote_index_list = []
        sql_org_hash_list = []
        for current_outer_index in range( 1, my_coder_count + 1 ):
        
            # loop over indices past the current one, adding SQL fragments to
            #     our SQL lists for comparison of current to subsequent.
            for current_inner_index in range( current_outer_index + 1, my_coder_count + 1 ):

                # add inequality comparison for detected.
                column_name_suffix = "_" + cls.FIELD_NAME_SUFFIX_DETECTED
                sql_temp_string = "( " + cls.FIELD_NAME_PREFIX_CODER + str( current_outer_index ) + column_name_suffix + " != " + cls.FIELD_NAME_PREFIX_CODER + str( current_inner_index ) + column_name_suffix + " )"
                sql_detected_list.append( sql_temp_string )
                
                # add inequality comparison for lookup.
                column_name_suffix = "_" + cls.FIELD_NAME_SUFFIX_PERSON_ID
                sql_temp_string = "( " + cls.FIELD_NAME_PREFIX_CODER + str( current_outer_index ) + column_name_suffix + " != " + cls.FIELD_NAME_PREFIX_CODER + str( current_inner_index ) + column_name_suffix + " )"
                sql_person_id_list.append( sql_temp_string )
                
                # add inequality comparison for type.
                column_name_suffix = "_" + cls.FIELD_NAME_SUFFIX_PERSON_TYPE
                sql_temp_string = "( " + cls.FIELD_NAME_PREFIX_CODER + str( current_outer_index ) + column_name_suffix + " != " + cls.FIELD_NAME_PREFIX_CODER + str( current_inner_index ) + column_name_suffix + " )"
                sql_person_type_list.append( sql_temp_string )
                
                # include optional?
                if ( include_optional_IN == True ):
                
                    # add inequality comparison for first_quote_graf
                    column_name_suffix = "_" + cls.FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF
                    sql_temp_string = "( " + cls.FIELD_NAME_PREFIX_CODER + str( current_outer_index ) + column_name_suffix + " != " + cls.FIELD_NAME_PREFIX_CODER + str( current_inner_index ) + column_name_suffix + " )"
                    sql_quote_graf_list.append( sql_temp_string )
                
                    # add inequality comparison for first_quote_index
                    column_name_suffix = "_" + cls.FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX
                    sql_temp_string = "( " + cls.FIELD_NAME_PREFIX_CODER + str( current_outer_index ) + column_name_suffix + " != " + cls.FIELD_NAME_PREFIX_CODER + str( current_inner_index ) + column_name_suffix + " )"
                    sql_quote_index_list.append( sql_temp_string )
                
                    # add inequality comparison for organization_hash
                    column_name_suffix = "_" + cls.FIELD_NAME_SUFFIX_ORGANIZATION_HASH
                    sql_temp_string = "( " + cls.FIELD_NAME_PREFIX_CODER + str( current_outer_index ) + column_name_suffix + " != " + cls.FIELD_NAME_PREFIX_CODER + str( current_inner_index ) + column_name_suffix + " )"
                    sql_org_hash_list.append( sql_temp_string )
                                
                #-- END check to see if include optional --#

            #-- END loop over rest of indices past current --#
        
        #-- END loop over coders to compare --#
        
        # build SQL string
        sql_string = "SELECT * FROM sourcenet_analysis_reliability_names WHERE "
        
        # got a label?
        if ( ( my_label is not None ) and ( my_label != "" ) ):

            # yes.  Add to WHERE clause.
            sql_string += " label = %s AND ( "
            
            # and add value to params list.
            sql_raw_params_list.append( my_label )

        #-- END check to see if label set --#
        
        # append detected comparisons
        sql_temp_string = " OR ".join( sql_detected_list )
        sql_string += " ( " + sql_temp_string + " )"
        
        # append person id comparisons
        sql_temp_string = " OR ".join( sql_person_id_list )
        sql_string += " OR ( " + sql_temp_string + " )"

        # append person type comparisons
        sql_temp_string = " OR ".join( sql_person_type_list )
        sql_string += " OR ( " + sql_temp_string + " )"
        
        # got first_quote_graf?
        if ( ( sql_quote_graf_list is not None ) and ( len( sql_quote_graf_list ) > 0 ) ):
        
            # append person type comparisons
            sql_temp_string = " OR ".join( sql_person_type_list )
            sql_string += " OR ( " + sql_temp_string + " )"
            
        #-- END check to see if first_quote_graf list --#
            
        # got first_quote_index?
        if ( ( sql_quote_index_list is not None ) and ( len( sql_quote_index_list ) > 0 ) ):
        
            # append person type comparisons
            sql_temp_string = " OR ".join( sql_quote_index_list )
            sql_string += " OR ( " + sql_temp_string + " )"
            
        #-- END check to see if first_quote_graf list --#
            
        # got organization_hash?
        if ( ( sql_org_hash_list is not None ) and ( len( sql_org_hash_list ) > 0 ) ):
        
            # append person type comparisons
            sql_temp_string = " OR ".join( sql_org_hash_list )
            sql_string += " OR ( " + sql_temp_string + " )"
            
        #-- END check to see if first_quote_graf list --#
            
        # got a label?
        if ( ( my_label is not None ) and ( my_label != "" ) ):

            # yes.  Close parentheses.
            sql_string += " )"

        #-- END check to see if label set --#
        
        # ORDER BY
        if ( ( order_by_IN is not None ) and ( order_by_IN != "" ) ):
        
            # custom order by passed in - use it.
            sql_string += " " + order_by_IN
        
        else:

            # no custom order by passed in.  go with default.
            sql_string += cls.DEFAULT_ORDER_BY
            
        #-- END check to see if custom ORDER BY passed in. --#
        
        # execute raw query
        qs_OUT = cls.objects.raw( sql_string, sql_raw_params_list )

        return qs_OUT        
    
    #-- END class method lookup_disagreements() --#


    @classmethod
    def merge_records( cls,
                       merge_from_id_IN,
                       merge_into_id_IN,
                       delete_from_record_IN = False,
                       *args,
                       **kwargs ):
        
        '''
        Accepts IDs of two Reliability_Names rows.  Loads each into an instance.
            Then, loops over the indices.  For each index, checks to see if that
            index is empty in the FROM record.  If yes, moves on.  If no, checks
            to see if the index is empty in the TO record.  If yes, adds index
            to list of indexes to copy values FROM INTO.  If ever an index has
            data in both FROM and TO, does not change anything, returns an error
            message.
        '''
        
        # return reference
        status_OUT = StatusContainer()

        # declare variables
        me = "merge_records"
        debug_message = ""
        status_message = ""
        merge_from_instance = None
        merge_into_instance = None
        merge_index_list = []
        error_index_list = []
        is_from_index_empty = False
        is_into_index_empty = False
        error_count = -1
        current_index = -1
        
        # load instances.
        merge_from_instance = Reliability_Names.objects.get( pk = merge_from_id_IN )
        merge_into_instance = Reliability_Names.objects.get( pk = merge_into_id_IN )
        
        # loop over indexes
        merge_index_list = []
        error_index_list = []
        for current_index in range( 1, cls.MAX_INDEX + 1 ):
        
            debug_message = "In " + me + ": current index = " + str( current_index )
            output_debug( debug_message, me, logger_name_IN = cls.LOGGER_NAME )
        
            # check to see if FROM index is empty.
            is_from_index_empty = merge_from_instance.is_index_empty( current_index )
            if ( is_from_index_empty == False ):
            
                debug_message = "In " + me + ": FROM not empty."
                output_debug( debug_message, me, indent_with_IN = "----> ", logger_name_IN = cls.LOGGER_NAME )
            
                # not empty in FROM.  Empty in INTO?
                is_into_index_empty = merge_into_instance.is_index_empty( current_index )
                if ( is_into_index_empty == True ):
                
                    # Add index to merge list.
                    merge_index_list.append( current_index )
                    
                    debug_message = "In " + me + ": INTO is empty."
                    output_debug( debug_message, me, indent_with_IN = "----> ", logger_name_IN = cls.LOGGER_NAME )
                
                else:
                
                    # Both are populated.  ERROR.
                    error_index_list.append( current_index )
                    
                    debug_message = "In " + me + ": INTO not empty."
                    output_debug( debug_message, me, indent_with_IN = "----> ", logger_name_IN = cls.LOGGER_NAME )
                
                #-- END check to see if INTO is empty at current index. --#
                
            else:
            
                debug_message = "In " + me + ": FROM is empty."
                output_debug( debug_message, me, indent_with_IN = "----> ", logger_name_IN = cls.LOGGER_NAME )
            
            #-- END check to see if FROM is empty at current index. --#
        
        #-- END loop over indices --#
        
        # errors?
        error_count = len( error_index_list )
        if ( error_count == 0 ):

            # no errors, for each index to merge, copy values from FROM into
            #     INTO for all of a given index's fields.
            for current_index in merge_index_list:
            
                # copy values from FROM into INTO.
                merge_into_instance.copy_index_values( current_index, merge_from_instance )
            
            #-- END loop over indices. --#
            
            # add details of Person from FROM into notes for INTO.
            status_message = "Reliability_Names." + str( me ) + "() merged data from indexes " + str( merge_index_list ) + " in Reliability_Names ID = " + str( merge_from_instance.id ) + " ( Person: " +  str( merge_from_instance.person ) + " ) into this record ( Reliability_Names ID = " + str( merge_into_instance.id ) + " )."
            
            if ( ( merge_into_instance.notes is not None ) and ( merge_into_instance.notes != "" ) ):
            
                # notes aren't empty - append a newline and a dash.
                merge_into_instance.notes += "\n- "
                merge_into_instance.notes += status_message
                
            else:
            
                # else empty, so set to empty string so we can append below one way or the othst
                merge_into_instance.notes = status_message
            
            #-- END check to see if merge_into_instance.notes are empty. --#
            
            # save changes to INTO.
            merge_into_instance.save()
            
            # delete FROM?
            if ( delete_from_record_IN == True ):
            
                # delete the FROM record
                merge_from_instance.delete()
                
            #-- END check to see if we delete. --#
            
            # set status to success and return message.
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
            status_OUT.add_message( status_message )
        
        else:

            # there were errors.  Log status appropriately, then do nothing.
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
            status_message = "There is data present in both records for the following indices: " + str( error_index_list ) + ", and so nothing was changed and you'll have to sort that out manually at this point."
            status_OUT.add_message( status_message )
        
        #-- END check for errors. --#

        return status_OUT
        
    #-- END classmethod merge_records() --#


    #----------------------------------------------------------------------------
    # ! ==> instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        temp_string = ""
        current_index = -1
        attr_name = None
        attr_value = None
        coder_instance = None
        is_detected = None
        person_id = None
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got a label?
        if ( self.label ):
        
            # got a label
            string_OUT += " - label: " + self.label
            
        #-- END check for label --#
        
        # got an article?
        if ( self.article ):
        
            # yes - output ID.
            string_OUT += " - article ID: " + str( self.article.id )
            
        #-- END check to see if article. --#
        
        # got person_name?
        if ( self.person_name ):
        
            # yes, append it
            string_OUT += " - " + self.person_name
            
        #-- END check to see if person_name --#
            
        # got person?
        if ( self.person ):
        
            # yes, append ID in parens.
            string_OUT += " ( " + str( self.person.id ) + " )"
            
        #-- END check to see if we have a person. --#
        
        # got coder details?
        if ( ( self.coder1 ) or ( self.coder2 ) or ( self.coder3 ) ):
        
            # yes.  Output a summary of coding.
            string_OUT += " - coders: "
            
            temp_string = ""
            
            # loop over range from 1 to 10.
            for current_index in range( 1, 11 ):
            
                # get attribute values.

                # ==> coder instance - build field name, then retrieve it.
                
                # build attribute name
                attr_name = self.FIELD_NAME_PREFIX_CODER + str( current_index )
                if ( ( self.FIELD_NAME_SUFFIX_CODER is not None ) and ( self.FIELD_NAME_SUFFIX_CODER != "" ) ):
                
                    attr_name += "_" + self.FIELD_NAME_SUFFIX_CODER
                    
                #-- END check to see if there is a coder suffix. --#
                
                # get value
                coder_instance = getattr( self, attr_name, None )
                
                # ==> detected flag - build field name, then retrieve it.
                
                # build attribute name
                attr_name = self.FIELD_NAME_PREFIX_CODER + str( current_index ) + "_" + self.FIELD_NAME_SUFFIX_DETECTED
                
                # get value
                is_detected = getattr( self, attr_name, None )
                
                # ==> person ID - build field name, then retrieve it.
                
                # build attribute name
                attr_name = self.FIELD_NAME_PREFIX_CODER + str( current_index ) + "_" + self.FIELD_NAME_SUFFIX_PERSON_ID
                
                # get value
                person_id = getattr( self, attr_name, None )
                
                # got a coder?
                if ( coder_instance ):
                
                    # yes - output details for coder.
                    string_OUT += "[" + str( current_index ) + "]"
                    temp_string += " ==> [" + str( current_index ) + "] - coder=" + str( coder_instance.id ) + "; detected=" + str( is_detected ) + "; person=" + str( person_id )
                    
                #-- END check to see if coder instance. --#
                
            #-- END loop over coders --#
            
            string_OUT += ": " + temp_string
        
        return string_OUT

    #-- END method __str__() --#
    
    
    def copy_index_values( self, index_IN, copy_from_instance_IN, *args, **kwargs ):
        
        '''
        Accepts index whose contents we want to copy and the record instance
            from which we want to copy.  Loops through all the suffixes, builds
            field name for the requested index for each suffix, then reads the
            values for each field from the FROM instance passed in and stores
            those values in the same field in this instance.  Returns status in
            a StatusContainer.
        '''
        
        # return reference
        status_OUT = StatusContainer()
        
        # declare variables
        me = "copy_index_values"
        suffix_list = []
        field_name_suffix = ""
        field_name = ""
        field_value = ""
        
        # get list of all suffixes
        suffix_list = self.ALL_FIELD_NAME_SUFFIX_LIST
        
        # loop over the suffixes
        for field_name_suffix in suffix_list:
        
            # build field/column name.
            field_name = self.build_field_name( index_IN, field_name_suffix )
            
            # get field value from FROM instance.
            field_value = copy_from_instance_IN.get_field_value( index_IN, field_name_suffix )
            
            # set field value in self
            setattr( self, field_name, field_value )
            
        #-- END loop over field name/column name suffixes --#
        
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        return status_OUT
                
    #-- END method copy_index_values() --#


    def find_disagreement( self, coder_count_IN = -1, comparison_suffix_list_IN = None, include_optional_IN = False ):
        
        '''
        Accepts count of coders we want to include in search for disagreements,
            optional list of suffixes to examine, and if no list present,
            another optional parameter that tells whether we want to include
            non-essential fields (1st quote graf and index, and organization
            hash).  Returns a list of suffixes where there was a disagreement.
            If list is empty, no disagreement.
        '''
        
        # return reference
        disagree_list_OUT = []
        
        # declare variables
        my_coder_count = -1
        current_outer_index = -1
        current_inner_index = -1
        comparison_suffix_list = []
        field_name_suffix = ""
        field_name_1 = ""
        field_name_2 = ""
        field_value_1 = ""
        field_value_2 = ""
        
        # got a suffix list passed in?
        if ( comparison_suffix_list_IN is not None ):
        
            # yes - use it.
            comparison_suffix_list = comparison_suffix_list_IN
            
        else:
        
            # no.  Use default.
            
            # init comparison suffix list
            comparison_suffix_list = self.DEFAULT_AGREEMENT_FIELD_SUFFIX_LIST
            
            # include optional?
            if ( include_optional_IN == True ):
            
                # Yes. add the optional list to our comparison suffix list.
                comparison_suffix_list.extend( self.OPTIONAL_AGREEMENT_FIELD_SUFFIX_LIST )
            
            #-- END check to see if we include optional. --#
            
        #-- END check to see if suffix list passed in. --#

        # got coder_count_IN?
        if ( ( coder_count_IN is not None ) and ( coder_count_IN != "" ) and ( int( coder_count_IN ) > 2 ) ):
        
            # yes, and is at least 2.  Use it.
            my_coder_count = int( coder_count_IN )
        
        else:
        
            # no, or not at least 2.  Default to 2.
            my_coder_count = 2
            
        #-- END check to see if coder count passed in. --#
        
        # loop over coders we've been asked to compare
        for current_outer_index in range( 1, my_coder_count + 1 ):
        
            # loop over indices past the current one, the "to whom" we will
            #     compare.
            for current_inner_index in range( current_outer_index + 1, my_coder_count + 1 ):

                # loop over the list of fields to compare (contains the
                #     suffixes).
                for field_name_suffix in comparison_suffix_list:

                    # do inequality comparison for detected.
                    
                    # make field/column names.
                    field_name_1 = self.build_field_name( current_outer_index, field_name_suffix )
                    field_name_2 = self.build_field_name( current_inner_index, field_name_suffix )

                    # get field values
                    field_value_1 = getattr( self, field_name_1 )
                    field_value_2 = getattr( self, field_name_2 )

                    # check for disagreement.
                    if ( field_value_1 != field_value_2 ):
                    
                        # not the same - check to see if field_name_suffix is
                        #     already in the list.
                        if ( field_name_suffix not in disagree_list_OUT ):
                        
                            # add it to the list.
                            disagree_list_OUT.append( field_name_suffix )
                            
                        #-- END check to see if suffix in list. --#
                    
                    #-- END check to see if values are the same --#
                
                #-- END check to see if field values are different --#

            #-- END loop over rest of indices past current --#
        
        #-- END loop over coders to compare --#

        return disagree_list_OUT
        
    #-- END method find_disagreement() --#
     

    def get_field_value( self, index_IN, field_name_suffix_IN, default_IN = None, *args, **kwargs ):
        
        '''
        Accepts index and suffix of field we want to get a value for.  Builds
            field name for the requested index and suffix, then reads the
            value for that field and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_field_value"
        field_name = ""
        field_value = ""
        
        # build field/column name.
        field_name = self.build_field_name( index_IN, field_name_suffix_IN )
        
        # get field value from FROM instance.
        value_OUT = getattr( self, field_name, default_IN )
                
        return value_OUT
                
    #-- END method get_field_value() --#


    def get_field_values( self, field_name_suffix_IN, default_IN = None, omit_empty_IN = True, empty_values_IN = ( None, ) ):
        
        '''
        Accepts a field_name_suffix and optional:
        - default_IN - default field value in case field name doesn't exist (defaults to None)
        - omit_empty_IN - boolean flag telling whether we want function to omit empty values from output (defaults to True).
        - empty_values_IN - tuple or list of values that should be considered empty.  Defaults to just None.  For number, could include 0 and -1, for string include "", etc.'
        
        Loops over all available indexes.  For each, tries to get value for the
            field name with that index.  If not omitting empty, stores the value
            in dictionary mapped to current index (coder number).  If omitting
            empty, only adds to dictionary if value is not in the values listed
            in variable empty_values_IN.
        
        Returns dictionary of all values found in current record, with each
            mapped in a dictionary to their index/coder number.
        '''
        
        # return reference
        dictionary_OUT = {}
        
        # declare variables.
        coder_number = -1
        coder_number_string = None
        current_field_name = ""
        current_field_value = ""
        
        # loop over indexes 1 through 10.
        for coder_number in range( 1, 11 ):
        
            # Make field name
            coder_number_string = str( coder_number )
            current_field_name = ""
            
            # build field name.
            current_field_name = Reliability_Names.build_field_name( coder_number, field_name_suffix_IN )
            
            # get the value
            current_field_value = getattr( self, current_field_name, default_IN )
            
            # omitting empty?
            if ( omit_empty_IN == True ):
            
                # empty?
                if ( current_field_value not in empty_values_IN ):
                
                    # not empty - add to dictionary.
                    dictionary_OUT[ coder_number ] = current_field_value
                    
                #-- END check to see if empty --#
                    
            else:
            
                # add to dictionary
                dictionary_OUT[ coder_number ] = current_field_value
                
            #-- END check to see if omitting empty. --#
    
        #-- END loop over coder numbers. --#
        
        return dictionary_OUT
        
    #-- END method get_field_values() --#
    


    def has_disagreement( self, coder_count_IN = -1, comparison_suffix_list_IN = None, include_optional_IN = False ):
        
        '''
        Accepts count of coders we want to include in search for disagreements,
        
        '''
        
        # return reference
        value_OUT = False
        
        # declare variables
        disagree_list = None
        
        # call find_disagreement to get list of suffixes where there is
        #     disagreement.
        disagree_list = self.find_disagreement( 
                coder_count_IN = coder_count_IN,
                comparison_suffix_list_IN = comparison_suffix_list_IN,
                include_optional_IN = include_optional_IN
            )
            
        # anything in list?  If so, disagreement.  If not, agree!
        if ( ( disagree_list is not None ) and ( isinstance( disagree_list, list ) == True ) and ( len( disagree_list ) > 0 ) ):
        
            # list has something in it.  There is disagreement.  Return True.
            value_OUT = True
            
        else:
        
            # nothing in disagreement list.  Return False.
            value_OUT = False
        
        #-- END check to see if disagrement list has anything in it. --#
                
        return value_OUT
        
    #-- END method has_disagreement() --#
     

    def is_field_empty( self, index_IN, field_name_suffix_IN, *args, **kwargs ):
        
        '''
        Accepts an index and a field name suffix.  Builds field name, gets field
            type, then check to see if field is empty based on type.  Returns
            True if empty, False if not.  If unknown suffix, returns True...
        '''
        
        # return reference
        is_empty_OUT = True
        
        # declare variables
        me = "is_field_empty"
        debug_message = ""
        field_name = ""
        field_value = None
        field_type = ""
        
        # make field/column name.
        field_name = self.build_field_name( index_IN, field_name_suffix_IN )
        
        # get field value
        field_value = getattr( self, field_name )
        
        # get field type
        field_type = self.FIELD_NAME_SUFFIX_TO_TYPE_MAP.get( field_name_suffix_IN, None )
        
        debug_message = "In " + me + ": Current Request - field_name = " + str( field_name ) + "; field_value = " + str( field_value ) + "; field type = " + str( field_type )
        output_debug( debug_message, me, indent_with_IN = "--------> ", logger_name_IN = self.LOGGER_NAME )
    
        # do empty check based on type.
        if ( field_type == self.FIELD_TYPE_FOREIGN_KEY ):
        
            # foreign key - None is empty
            if ( field_value is not None ):
            
                # not empty
                is_empty_OUT = False
                
            else:
            
                # empty
                is_empty_OUT = True
                
            #-- END check to see if empty. --#
            
        elif ( field_type == self.FIELD_TYPE_NON_ZERO_INTEGER ):
        
            # integer - must be not None and type int and greater than 0.
            if ( ( field_value is not None )
                and ( isinstance( field_value, int ) == True )
                and ( field_value > 0 ) ):

                # not empty
                is_empty_OUT = False
                
            else:
            
                # empty
                is_empty_OUT = True
                
            #-- END check to see if empty. --#
        
        elif ( field_type == self.FIELD_TYPE_INTEGER ):
        
            # integer - must be not None and type int
            if ( ( field_value is not None ) and ( isinstance( field_value, int ) == True ) ):

                # not empty
                is_empty_OUT = False
                
            else:
            
                # empty
                is_empty_OUT = True
                
            #-- END check to see if empty. --#
        
        elif ( field_type == self.FIELD_TYPE_STRING ):
        
            # integer - must be not None and not "".
            if ( ( field_value is not None ) and ( field_value != "" ) ):

                # not empty
                is_empty_OUT = False
                
            else:
            
                # empty
                is_empty_OUT = True
                
            #-- END check to see if empty. --#
            
        else:
        
            # default - not None and not "".
            if ( ( field_value is not None ) and ( field_value != "" ) ):

                # not empty
                is_empty_OUT = False
                
            else:
            
                # empty
                is_empty_OUT = True
                
            #-- END check to see if empty. --#
                    
        #-- END empty check based on type. --#
        
        return is_empty_OUT
        
    #-- END method is_field_empty() --#
    
    
    def is_index_empty( self, index_IN, comparison_suffix_list_IN = None, *args, **kwargs ):
        
        '''
        Accepts index whose contents we want to inspect.  Loops through all the
            fields for a given index, checking to see if each is empty.  If all
            are empty, returns True.  If any are not empty, returns False.
        '''
        
        # return reference
        is_empty_OUT = True
        
        # declare variables
        comparison_suffix_list = []
        my_coder_count = -1
        field_name_suffix = ""
        is_field_empty = False

        # got a suffix list passed in?
        if ( comparison_suffix_list_IN is not None ):
        
            # yes - use it.
            comparison_suffix_list = comparison_suffix_list_IN
            
        else:
        
            # no.  Use default.
            
            # init comparison suffix list - just coder ID integer field (coder
            #     reference is always set, for reference), IDs of other records,
            #     and person type, string and int.
            comparison_suffix_list = [
                self.FIELD_NAME_SUFFIX_CODER_ID,
                self.FIELD_NAME_SUFFIX_PERSON_ID,
                self.FIELD_NAME_SUFFIX_PERSON_TYPE,
                self.FIELD_NAME_SUFFIX_PERSON_TYPE_INT,
                self.FIELD_NAME_SUFFIX_ARTICLE_DATA_ID,
                self.FIELD_NAME_SUFFIX_ARTICLE_PERSON_ID,
            ]
            
        #-- END check to see if suffix list passed in. --#

        # start with is_empty_OUT = True
        is_empty_OUT = True
        
        # loop over suffixes we've been asked to compare
        for field_name_suffix in comparison_suffix_list:

            # is field empty?
            is_field_empty = self.is_field_empty( index_IN, field_name_suffix )
            
            # if not empty, change return value to False, also.
            if ( is_field_empty == False ):

                # not empty.
                is_empty_OUT = False
                
            #-- END check if field is empty --#
            
        #-- END loop over field suffixes. --#
        
        return is_empty_OUT
        
    #-- END method is_index_empty() --#
     

#= END Reliability_Names model ===============================================#


@python_2_unicode_compatible
class Reliability_Names_Evaluation( models.Model ):

    '''
    Class to hold details on individual Reliability_Names rows that have been
        validated.  This includes information on the related Article and
        Article_Data instances, and notes on the denouement of the evaluation.
    '''

    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------


    # statuses
    STATUS_CORRECT = "CORRECT"
    STATUS_ERROR = "ERROR"
    STATUS_INCOMPLETE = "INCOMPLETE"
    STATUS_CHOICES = (
        ( STATUS_CORRECT, "CORRECT" ),
        ( STATUS_ERROR, "ERROR" ),
        ( STATUS_INCOMPLETE, "INCOMPLETE" )
    )
    
    # default status message
    STATUS_MESSAGE_DEFAULT = "MISSED"
    
    # event type
    EVENT_TYPE_DELETE = "delete"
    EVENT_TYPE_MERGE = "merge"
    EVENT_TYPE_ADD_TAGS = "add_tags"
    EVENT_TYPE_REMOVE_TAGS = "remove_tags"
    EVENT_TYPE_CHOICES = (
        ( EVENT_TYPE_DELETE, EVENT_TYPE_DELETE ),
        ( EVENT_TYPE_MERGE, EVENT_TYPE_MERGE ),
        ( EVENT_TYPE_ADD_TAGS, "add tags" ),
        ( EVENT_TYPE_REMOVE_TAGS, "remove tags" )
    )
 

    #----------------------------------------------------------------------
    # model fields
    #----------------------------------------------------------------------

    label = models.CharField( max_length = 255, blank = True, null = True )
    reliability_names = models.ForeignKey( Reliability_Names, blank = True, null = True, on_delete = models.SET_NULL )
    original_reliability_names_id = models.IntegerField( blank = True, null = True )
    person_name = models.CharField( max_length = 255, blank = True, null = True )
    persons = models.ManyToManyField( Person, blank = True )
    article = models.ForeignKey( Article, blank = True, null = True, on_delete = models.SET_NULL )
    article_datas = models.ManyToManyField( Article_Data, blank = True, related_name = "rne_article_data" )
    status = models.CharField( max_length = 255, blank = True, null = True, choices = STATUS_CHOICES )
    status_message = models.TextField( blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    is_ground_truth_fixed = models.BooleanField( default = False )
    is_deleted = models.BooleanField( default = False )
    is_automated_error = models.BooleanField( default = False )
    is_single_name = models.BooleanField( default = False )
    is_ambiguous = models.BooleanField( default = False )
    is_quoted_shb_mentioned = models.BooleanField( default = False )
    is_mentioned_shb_quoted = models.BooleanField( default = False )
    is_not_hard_news = models.BooleanField( default = False )
    event_type = models.CharField( max_length = 255, blank = True, null = True, choices = EVENT_TYPE_CHOICES )
    
    # need to add fields for merge from/to Reliability_Names ID and Article_Data.
    merged_from_reliability_names_id = models.IntegerField( blank = True, null = True )
    merged_to_reliability_names_id = models.IntegerField( blank = True, null = True )
    merged_from_article_datas = models.ManyToManyField( Article_Data, blank = True, related_name = "rne_merged_from_article_data" )
    merged_to_article_datas = models.ManyToManyField( Article_Data, blank = True, related_name = "rne_merged_to_article_data" )
    
    # time stamps
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )

    # tags!
    tags = TaggableManager( blank = True )
    

    #----------------------------------------------------------------------------
    # Meta class
    #----------------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:
        ordering = [ '-last_modified' ]
        #ordering = [ 'id', 'label', 'article', 'person_name', 'status' ]


    #----------------------------------------------------------------------------
    # ! ==> class methods
    #----------------------------------------------------------------------------


    @classmethod
    def build_detail_string_from_rn_id( cls,
                                        reliability_names_id_IN,
                                        delimiter_IN = "|",
                                        prefix_IN = "| ",
                                        suffix_IN = " |",
                                        default_status_IN = "CORRECT",
                                        protocol_IN = "http",
                                        host_IN = "research.local",
                                        app_path_IN = "sourcenet/",
                                        rne_instance_IN = None ):
    
        '''
        Accepts Reliability_Names instance, and optional delimiter, prefix, and
            suffix.  Retrieves the Article_Data, and Article_Subject(s) that the
            Reliability_Name refers to.  Uses information from all to build a detail
            string. 
        '''
        
        # return reference
        detail_string_OUT = None
        
        # declare variables
        rne_instance = None
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
        
        # do we have Reliability_Names_Evaluation (rne) instance?
        if ( rne_instance_IN is not None ):
        
            # we do.  Use it.
            rne_instance = rne_instance_IN
            
        #-- END check to see if Reliability_Names_Evaluation instance --#
        
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
                    
                    # ==> Reliability_Names_Evaluation ID?
                    if ( rne_instance is not None ):

                        # make it a link
                        # example: http://research.local/sourcenet/admin/sourcenet_analysis/reliability_names_evaluation/6/change/
                        detail_string += "<a href=\""
                        detail_string += str( protocol_IN ) + "://"
                        detail_string += str( host_IN ) + "/" + str( app_path_IN )
                        detail_string += "admin/sourcenet_analysis/reliability_names_evaluation/"
                        detail_string += str( rne_instance.id )
                        detail_string += "/change/\">"
                        detail_string += str( rne_instance.id )
                        detail_string += "</a>"
                        
                        # and add a delimiter
                        detail_string += " " + delimiter_IN + " "
                        
                    #-- END check to see if Reliability_Names_Evaluation ID --#
            
                    # ==> Reliability_Names ID
                    detail_string += str( reliability_names_id )
                    detail_string += " " + delimiter_IN + " "
                    
                    # ==> Article ID and link
                    detail_string += "Article ["
                    detail_string += str( article_id )
                    detail_string += "](" + str( protocol_IN ) + "://" + str( host_IN ) + "/" + str( app_path_IN ) + "sourcenet/article/article_data/view_with_text/?article_id="
                    detail_string += str( article_id )
                    detail_string += ")"
                    detail_string += " " + delimiter_IN + " "

                    # ==> Article_Data ID and link
                    detail_string += "Article_Data ["
                    detail_string += str( article_data_id )
                    detail_string += "](" + str( protocol_IN ) + "://" + str( host_IN ) + "/" + str( app_path_IN ) + "sourcenet/article/article_data/view/?article_id="
                    detail_string += str( article_id )
                    detail_string += "&article_data_id_select="
                    detail_string += str( article_data_id )
                    detail_string += ") " + delimiter_IN + " "
                    
                    # ==> Person instance
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
    
    #-- END method build_detail_string_from_rn_id() --#


    @classmethod
    def build_summary_string_from_rn_id( cls,
                                         reliability_names_id_IN,
                                         delimiter_IN = "|",
                                         prefix_IN = "| ",
                                         suffix_IN = " |",
                                         default_status_IN = "CORRECT",
                                         protocol_IN = "http",
                                         host_IN = "research.local",
                                         app_path_IN = "sourcenet/",
                                         default_error_IN = "MISSED",
                                         rne_instance_IN = None ):
        
        '''
        Accepts Reliability_Names instance, and optional delimiter, prefix, and
            suffix.  Retrieves the Article_Data, and Article_Subject(s) that the
            Reliability_Name refers to.  Uses information from all to build a 
            delimited summary string.
        '''
        
        # return reference
        detail_string_OUT = None
        
        # declare variables
        detail_string_list = []
        detail_string = ""
        reliability_names_id = -1
        reliability_names_qs = None
        reliability_names_instance = None
        person_name = ""
        related_article = None
        article_id = -1
        index_list = []
        current_index = -1
        
        # declare variables - retrieve information from Reliability_Names row.
        current_suffix = ""
        article_data_id = -1
        article_data_qs = None
        article_data_instance = None
        article_data_coder_id = -1
        article_data_id_list = []
        person_type_column_name = ""
        person_type = ""
        article_person_id_column_name = ""
        article_person_id = -1
        article_person_qs = None
        article_person_instance = None
        
        # declare variables - output rendering.
        article_data_link_list = []
        article_data_link = ""
        
        # do we have Reliability_Names_Evaluation (rne) instance?
        if ( rne_instance_IN is not None ):
        
            # we do.  Use it.
            rne_instance = rne_instance_IN
            
        #-- END check to see if Reliability_Names_Evaluation instance --#
        
        # get information for output
        reliability_names_id = reliability_names_id_IN
        if ( ( reliability_names_id is not None ) and ( reliability_names_id > 0 ) ):
        
            # get Reliability_Names instane.
            reliability_names_qs = Reliability_Names.objects.all()
            reliability_names_instance = reliability_names_qs.get( pk = reliability_names_id )

            # get person name
            person_name = reliability_names_instance.person_name
            
            # get related article.
            related_article = reliability_names_instance.article
            article_id = related_article.id
            
            # Get list of related Article_Data ids.
            article_data_id_list = []
            article_data_link_list = []
            
            # initialize
            index_list = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
            for current_index in index_list:
            
                # see if there is an Article_Data ID.
                current_suffix = Reliability_Names.FIELD_NAME_SUFFIX_ARTICLE_DATA_ID
                article_data_id = reliability_names_instance.get_field_value( current_index, current_suffix )
                if ( article_data_id is not None ):
        
                    # add to list
                    article_data_id_list.append( article_data_id )
    
                    # we have an ID value, try to get Article_Data...
                    article_data_qs = Article_Data.objects.all()
                    article_data_instance = article_data_qs.get( pk = article_data_id )
                    article_data_coder_id = article_data_instance.coder_id
                    
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
                    
                    # create link (very basic for now):
                    article_data_link = "[" + str( article_data_id ) + " (coder=" + str( article_data_coder_id ) + ")]"
                    article_data_link += "(" + str( protocol_IN ) + "://" + str( host_IN ) + "/" + str( app_path_IN ) + "sourcenet/article/article_data/view/?article_id="
                    article_data_link += str( article_id )
                    article_data_link += "&article_data_id_select="
                    article_data_link += str( article_data_id )
                    article_data_link += ")"
                    
                    # add to list.
                    article_data_link_list.append( article_data_link )
    
                #-- END check to see if Article_Data ID. --#
                            
            #-- END loop over indexes. --#
            
            # build detail string.
            detail_string = prefix_IN
            
            # ==> Reliability_Names_Evaluation ID?
            if ( rne_instance is not None ):

                # make it a link
                # example: http://research.local/sourcenet/admin/sourcenet_analysis/reliability_names_evaluation/6/change/
                detail_string += "<a href=\""
                detail_string += str( protocol_IN ) + "://"
                detail_string += str( host_IN ) + "/" + str( app_path_IN )
                detail_string += "admin/sourcenet_analysis/reliability_names_evaluation/"
                detail_string += str( rne_instance.id )
                detail_string += "/change/\">"
                detail_string += str( rne_instance.id )
                detail_string += "</a>"
                
                # and add a delimiter
                detail_string += " " + delimiter_IN + " "
                
            #-- END check to see if Reliability_Names_Evaluation ID --#
            
            # ==> Reliability_Names ID
            detail_string += str( reliability_names_id )
    
            detail_string += " " + delimiter_IN + " "
            
            # ==> person name
            detail_string += person_name
            
            detail_string += " " + delimiter_IN + " "
    
            # ==> Article ID and link
            detail_string += "Article "
            detail_string += "[" + str( article_id ) + "]"
            detail_string += "(" + str( protocol_IN ) + "://" + str( host_IN ) + "/" + str( app_path_IN ) + "sourcenet/article/article_data/view_with_text/?article_id="
            detail_string += str( article_id )
            detail_string += ")"
            
            detail_string += " " + delimiter_IN + " "
    
            # ==> Article_Data IDs and links
            detail_string += "Article_Data: "
            detail_string += "; ".join( article_data_link_list )
            
            # ==> status
            detail_string += " " + delimiter_IN + " " + default_status_IN
            
            # ==> error
            detail_string += " " + delimiter_IN + " " + default_error_IN
            
            # ==> notes
            detail_string += " " + delimiter_IN + " None"
            
            detail_string += suffix_IN
    
            detail_string_OUT = detail_string
    
        else:
        
            # no ID passed in.  Return None.
            detail_string_OUT = None
        
        #-- END check to see if Reliabilty_Names ID passed in. --#
        
        return detail_string_OUT
    
    #-- END method build_summary_string_from_rn_id() --#


    @classmethod
    def create_from_reliability_names( cls,
                                       reliability_names_id_IN,
                                       label_IN = None,
                                       status_IN = "CORRECT",
                                       status_message_IN = "MISSED",
                                       notes_IN = None,
                                       tag_list_IN = None,
                                       reliability_names_instance_IN = None,
                                       event_type_IN = None ):
        
        '''
        Accepts Reliability_Names ID and a few optional parameters.  Uses
            information from it to populate a Reliability_Names_Evaluation
            instance.
        '''
        
        # return reference
        instance_OUT = None
        
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
        master_person_instance = None
        master_person_name = None
        
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
        current_person = None
        person_name = None
        person_verbatim_name = None
        person_lookup_name = None
        person_title = None
        person_organization = None
        
        # get information for output
        reliability_names_id = reliability_names_id_IN
        if ( ( reliability_names_id is not None ) and ( reliability_names_id > 0 ) ):
        
            # create Reliability_Names_Evaluation instance
            instance_OUT = cls()
            
            # ==> status and status_message
            instance_OUT.status = status_IN
            instance_OUT.status_message = status_message_IN

            # ==> got a label?
            if ( ( label_IN is not None ) and ( label_IN != "" ) ):

                # yes - set it.
                instance_OUT.label = label_IN

            #-- END label --#
            
            # ==> got event_type?
            if ( ( event_type_IN is not None ) and ( event_type_IN != "" ) ):

                # yes - set it.
                instance_OUT.event_type = event_type_IN

            #-- END event_type --#
            
            # ==> got notes?
            if ( ( notes_IN is not None ) and ( notes_IN != "" ) ):

                # yes - set it.
                instance_OUT.notes = notes_IN

            #-- END notes --#
            
            # ==> tags?
            if ( ( tag_list_IN is not None ) and ( len( tag_list_IN ) > 0 ) ):
            
                # loop over tags.
                for tag_value in tag_list_IN:
                
                    # add tag.
                    instance_OUT.tags.add( tag_value )
                
                #-- END loop over tags --#
            
            #-- END tags. --#
            
            # get Reliability_Names instance.
            if ( reliability_names_instance_IN is not None ):
            
                # instance passed in.  Use it.
                reliability_names_instance = reliability_names_instance_IN
                
            else:

                # no instance passed in.  Retrieve it.
                reliability_names_qs = Reliability_Names.objects.all()
                reliability_names_instance = reliability_names_qs.get( pk = reliability_names_id )
                
            #-- END check to see if instance passed in --#                
            
            # ==> Reliability_Names information
            instance_OUT.reliability_names = reliability_names_instance
            instance_OUT.original_reliability_names_id = reliability_names_id

            # get related article.
            related_article = reliability_names_instance.article
            article_id = related_article.id
            
            # ==> related article
            if ( related_article is not None ):

                # we have a related article.  Store it.
                instance_OUT.article = related_article
                
            #-- END related article --#
            
            # person information
            master_person_instance = reliability_names_instance.person
            master_person_name = reliability_names_instance.person_name
            
            # ==> person information
            if ( ( master_person_name is not None ) and ( master_person_name != "" ) ):

                # store person name.
                instance_OUT.person_name = master_person_name
                
            #-- END check for person name --#
            
            # save so we can add related Article_Data and Person.
            instance_OUT.save()

            # Get info for all coders that have related Article_Data.
            
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
                    
                    # ==> Add to set of Article_Datas.
                    instance_OUT.article_datas.add( article_data_instance )
                    
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
                    
                    # got an Article_Person of one type or another?
                    current_person = None
                    if ( article_person_instance is not None ):
                    
                        current_person = article_person_instance.person
                    
                    #-- END check to see if Article_Person instance --#
                    
                    # ==> persons
                    if ( current_person is not None ):
                
                        # add to persons.
                        instance_OUT.persons.add( current_person )
                        
                    #-- END check to see if associated person. --#
                
                #-- END check to see if Article_Data ID. --#
                            
            #-- END loop over indexes. --#

            # and, save again, just to be sure.
            instance_OUT.save()
    
        else:
        
            # no ID passed in.  Return None.
            instance_OUT = None
        
        #-- END check to see if Reliabilty_Names ID passed in. --#
        
        return instance_OUT
    
    #-- END method create_from_reliability_names() --#
    
    
    @classmethod
    def create_from_reliability_data( cls,
                                      reliability_names_id_IN,
                                      label_IN = None,
                                      person_name_IN = None,
                                      article_id_IN = None,
                                      article_data_id_list_IN = None,
                                      status_IN = "CORRECT",
                                      status_message_IN = "MISSED",
                                      notes_IN = None,
                                      tag_list_IN = None,
                                      event_type_IN = None ):
        
        '''
        Accepts Reliability_Names ID and a few optional parameters.  Uses
            information from it to populate a Reliability_Names_Evaluation
            instance.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        detail_string_list = []
        detail_string = ""
        reliability_names_id = -1
        reliability_names_qs = None
        reliability_names_instance = None
        related_article = None
        article_id = -1
        article_data_id = -1
        master_person_instance = None
        master_person_name = None
        
        # declare variables - retrieve information from Article_Data rows.
        article_data_id = -1
        article_data_qs = None
        article_data_instance = None
        
        # get information for output
        reliability_names_id = reliability_names_id_IN
        if ( ( reliability_names_id is not None ) and ( reliability_names_id > 0 ) ):
        
            # see if there is a Reliability_Names instance for ID.
            try:
            
                # get Reliability_Names instance.
                reliability_names_qs = Reliability_Names.objects.all()
                
                # try to retrieve the Reliability_Names row.
                reliability_names_instance = reliability_names_qs.get( pk = reliability_names_id )
                
                # Success!  Call create_from_reliability_names()
                instance_OUT = cls.create_from_reliability_names( reliability_names_id,
                                                                  label_IN = label_IN,
                                                                  status_IN = status_IN,
                                                                  status_message_IN = status_message_IN,
                                                                  notes_IN = notes_IN,
                                                                  tag_list_IN = tag_list_IN,
                                                                  reliability_names_instance_IN = reliability_names_instance,
                                                                  event_type_IN = event_type_IN )
                                                                  
            except Reliability_Names.DoesNotExist as rn_dne:
            
                # create Reliability_Names_Evaluation instance
                instance_OUT = cls()
                
                # ==> status and status_message
                instance_OUT.status = status_IN
                instance_OUT.status_message = status_message_IN
    
                # ==> got a label?
                if ( ( label_IN is not None ) and ( label_IN != "" ) ):
    
                    # yes - set it.
                    instance_OUT.label = label_IN
    
                #-- END label --#
                
                # ==> got event_type?
                if ( ( event_type_IN is not None ) and ( event_type_IN != "" ) ):
    
                    # yes - set it.
                    instance_OUT.event_type = event_type_IN
    
                #-- END event_type --#
                
                # ==> got notes?
                if ( ( notes_IN is not None ) and ( notes_IN != "" ) ):
    
                    # yes - set it.
                    instance_OUT.notes = notes_IN
    
                #-- END notes --#
                
                # ==> tags?
                if ( ( tag_list_IN is not None ) and ( len( tag_list_IN ) > 0 ) ):
                
                    # loop over tags.
                    for tag_value in tag_list_IN:
                    
                        # add tag.
                        instance_OUT.tags.add( tag_value )
                    
                    #-- END loop over tags --#
                
                #-- END tags. --#
                
                # person information
                master_person_name = person_name_IN
                
                # ==> person information
                if ( ( master_person_name is not None ) and ( master_person_name != "" ) ):
    
                    # store person name.
                    instance_OUT.person_name = master_person_name
                    
                #-- END check for person name --#
    
                # ==> Reliability_Names information
                instance_OUT.original_reliability_names_id = reliability_names_id
    
                # get related article.
                if ( article_id_IN is not None ):

                    related_article = Article.objects.get( id = article_id_IN )
                    article_id = related_article.id
                    
                #-- END check to see if article ID --#
                
                # ==> related article
                if ( related_article is not None ):
    
                    # we have a related article.  Store it.
                    instance_OUT.article = related_article
                    
                #-- END related article --#
                
                # save so we can add related Article_Data.
                instance_OUT.save()
    
                # Got Article_Data ids in list?
                if ( ( article_data_id_list_IN is not None ) and ( len( article_data_id_list_IN ) > 0 ) ):
                
                    # Get info for Article_Data ids in list.
                    for article_data_id in article_data_id_list_IN:
                    
                        # we have an ID value, try to get Article_Data...
                        article_data_qs = Article_Data.objects.all()
                        article_data_instance = article_data_qs.get( pk = article_data_id )
                        
                        # ==> Add to set of Article_Datas.
                        instance_OUT.article_datas.add( article_data_instance )                        
                                    
                    #-- END loop over Article_Data IDs. --#
                    
                #-- END check to see if Article_Data ID list --#
                
                # and, save again, just to be sure.
                instance_OUT.save()
        
            #-- END try...except --#

        else:
        
            # no ID passed in.  Return None.
            instance_OUT = None
        
        #-- END check to see if Reliabilty_Names ID passed in. --#
        
        return instance_OUT
    
    #-- END method create_from_reliability_data() --#
    
    
    #----------------------------------------------------------------------------
    # ! ==> instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        temp_string = ""
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got a related Reliability_Names instance?
        if ( self.reliability_names is not None ):
        
            string_OUT += " - RN ID: " + str( self.reliability_names.id )
        
        #-- END check to see if Reliability_Names --#
        
        # got an original ID?
        if ( self.original_reliability_names_id is not None ):
        
            # got an original ID
            string_OUT += " ( original RN ID: " + str( self.original_reliability_names_id ) + " )"
            
        #-- END check for original ID --#
        
        # got person_name?
        if ( ( self.person_name is not None ) and ( self.person_name != "" ) ):
        
            # yes, append it
            string_OUT += " - from " + self.person_name
            
        #-- END check to see if person_name --#
            
        # got status?
        if ( ( self.status is not None ) and ( self.status != "" ) ):
        
            # yes, append.
            string_OUT += "; STATUS: " + self.status
            
        #-- END check to see if we have a status. --#

        # got status_message?
        if ( ( self.status_message is not None ) and ( self.status_message != "" ) ):
        
            # yes, append.
            string_OUT += "; status_message: " + self.status_message
            
        #-- END check to see if we have a status. --#
        
        return string_OUT

    #-- END method __str__() --#
     

    def build_detail_string( self,
                             delimiter_IN = "|",
                             prefix_IN = "| ",
                             suffix_IN = " |",
                             default_status_IN = "CORRECT",
                             protocol_IN = "http",
                             host_IN = "research.local",
                             app_path_IN = "sourcenet/" ):
    
        '''
        Accepts Reliability_Names (from self), and optional delimiter, prefix,
            and suffix.  Retrieves the Article_Data, and Article_Subject(s) that
            the Reliability_Names refers to.  Uses information from all to build
            a delimited detail string.
        '''
        
        # return reference
        detail_string_OUT = None
        
        # declare variables
        reliability_names_id = -1
                
        # get information for output
        reliability_names_id = self.original_reliability_names_id
        if ( ( reliability_names_id is not None ) and ( reliability_names_id > 0 ) ):
        
            # call method
            detail_string_OUT = Reliability_Names_Evaluation.build_detail_string_from_rn_id(
                    reliability_names_id,
                    delimiter_IN = delimiter_IN,
                    prefix_IN = prefix_IN,
                    suffix_IN = suffix_IN,
                    default_status_IN = default_status_IN,
                    protocol_IN = protocol_IN,
                    host_IN = host_IN,
                    app_path_IN = app_path_IN,
                    rne_instance_IN = self
                )

            
        else:
        
            # error - no Reliability_Names ID.
            detail_string_OUT = "ERROR - no Reliability_Names ID, so can't make detail string."

        #-- END check to see if Reliabilty_Names ID. --#
        
        return detail_string_OUT
    
    #-- END method build_detail_string() --#


    def build_summary_string( self,
                              delimiter_IN = "|",
                              prefix_IN = "| ",
                              suffix_IN = " |",
                              default_status_IN = "CORRECT",
                              protocol_IN = "http",
                              host_IN = "research.local",
                              app_path_IN = "sourcenet/",
                              default_error_IN = "MISSED" ):
        
        '''
        Accepts Reliability_Names (from self), and optional delimiter, prefix,
            and suffix.  Retrieves the Article_Data, and Article_Subject(s) that
            the Reliability_Names refers to.  Uses information from all to build
            a delimited summary string.
        '''
        
        # return reference
        detail_string_OUT = None
        
        # declare variables
        reliability_names_id = -1
                
        # get information for output
        reliability_names_id = self.original_reliability_names_id
        if ( ( reliability_names_id is not None ) and ( reliability_names_id > 0 ) ):
        
            # call method
            detail_string_OUT = Reliability_Names_Evaluation.build_summary_string_from_rn_id(
                     reliability_names_id,
                     delimiter_IN = delimiter_IN,
                     prefix_IN = prefix_IN,
                     suffix_IN = suffix_IN,
                     default_status_IN = default_status_IN,
                     protocol_IN = protocol_IN,
                     host_IN = host_IN,
                     app_path_IN = app_path_IN,
                     default_error_IN = default_error_IN,
                     rne_instance_IN = self
                )

        else:
        
            # error - no Reliability_Names ID.
            detail_string_OUT = "ERROR - no Reliability_Names ID, so can't make summary string."

        #-- END check to see if Reliabilty_Names ID. --#
        
        return detail_string_OUT
    
    #-- END method build_summary_string() --#


#= END Reliability_Names_Evaluation model ===============================================#


@python_2_unicode_compatible
class Reliability_Ties( models.Model ):

    '''
    Class to hold information on name detection choices within a given article
        across coders, for use in inter-coder reliability testing.  Intended to
        be read or exported for use by statistical analysis packages (numpy, R, 
        etc.).  Example of how to populate this table:
       
        sourcenet_analysis/examples/reliability/reliability-build_relation_data.py
       
        Examples of calculating reliability TK.
       
        Includes columns for three coders.  If you need more, add more sets of
        coder columns.
    '''

    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------


    # person types
    PERSON_TYPE_AUTHOR = "author"
    PERSON_TYPE_SOURCE = "source"
    
    # relation types
    RELATION_AUTHOR_TO_SOURCE = "author_to_source"
    RELATION_AUTHOR_TO_AUTHOR = "author_to_author"
    RELATION_SOURCE_TO_SOURCE = "source_to_source"
    

    #----------------------------------------------------------------------
    # model fields
    #----------------------------------------------------------------------

    person = models.ForeignKey( Person, blank = True, null = True, related_name = "reliability_ties_from_set" )
    person_name = models.CharField( max_length = 255, blank = True, null = True )
    person_type = models.CharField( max_length = 255, blank = True, null = True )
    relation_type = models.CharField( max_length = 255, blank = True, null = True )
    relation_person = models.ForeignKey( Person, blank = True, null = True, related_name = "reliability_ties_to_set" )
    relation_person_name = models.CharField( max_length = 255, blank = True, null = True )
    relation_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder1 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder1_set" )
    coder1_mention_count = models.IntegerField( blank = True, null = True )
    coder1_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder2 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder2_set" )
    coder2_mention_count = models.IntegerField( blank = True, null = True )
    coder2_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder3 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder3_set" )
    coder3_mention_count = models.IntegerField( blank = True, null = True )
    coder3_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder4 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder4_set" )
    coder4_mention_count = models.IntegerField( blank = True, null = True )
    coder4_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder5 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder5_set" )
    coder5_mention_count = models.IntegerField( blank = True, null = True )
    coder5_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder6 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder6_set" )
    coder6_mention_count = models.IntegerField( blank = True, null = True )
    coder6_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder7 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder7_set" )
    coder7_mention_count = models.IntegerField( blank = True, null = True )
    coder7_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder8 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder8_set" )
    coder8_mention_count = models.IntegerField( blank = True, null = True )
    coder8_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder9 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder9_set" )
    coder9_mention_count = models.IntegerField( blank = True, null = True )
    coder9_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder10 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder10_set" )
    coder10_mention_count = models.IntegerField( blank = True, null = True )
    coder10_id_list = models.CharField( max_length = 255, blank = True, null = True )
    label = models.CharField( max_length = 255, blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )


    #----------------------------------------------------------------------------
    # Meta class
    #----------------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:
        ordering = [ 'person_type', 'person', 'relation_person' ]


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        temp_string = ""
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got a label?
        if ( self.label ):
        
            # got a label
            string_OUT += " - label: " + self.label
            
        #-- END check for label --#
        
        # got person_name?
        if ( self.person_name ):
        
            # yes, append it
            string_OUT += " - from " + self.person_name
            
        #-- END check to see if person_name --#
            
        # got person?
        if ( self.person ):
        
            # yes, append ID in parens.
            string_OUT += " ( " + str( self.person.id ) + " )"
            
        #-- END check to see if we have a person. --#
        
        # got relation_person?
        if ( self.relation_person ):
        
            # yes.  add information.
            string_OUT += " to " + self.relation_person.get_name_string() + " ( " + str( self.relation_person.id ) + " )"
        
        #-- END check to see if relation_person --#
        
        # got coder details?
        if ( ( self.coder1 ) or ( self.coder2 ) or ( self.coder3 ) ):
        
            # yes.  Output a summary of coding.
            string_OUT += " - coders: "
            
            temp_string = ""
            
            if ( self.coder1 ):
            
                # output details for coder 1
                string_OUT += "1"
                temp_string += " ====> 1 - " + str( self.coder1.id ) + "; mentions: " + str( self.coder1_mention_count )
                
            #-- END check to see if coder1 --#

            if ( self.coder2 ):
            
                # output details for coder 2
                string_OUT += "2"
                temp_string += " ====> 2 - " + str( self.coder2.id ) + "; mentions: " + str( self.coder2_mention_count )
                
            #-- END check to see if coder2 --#
        
            if ( self.coder3 ):
            
                # output details for coder 3
                string_OUT += "3"
                temp_string += " ====> 3 - " + str( self.coder3.id ) + "; mentions: " + str( self.coder3_mention_count )
                
            #-- END check to see if coder3 --#
            
            string_OUT += temp_string
        
        return string_OUT

    #-- END method __str__() --#
     

#= END Reliability_Ties model ===============================================#


#==============================================================================#
# ! ++++++> Development
#==============================================================================#


@python_2_unicode_compatible
class Field_Spec( models.Model ):
    
    '''
    Class to hold specification for a field, initially for the purposes of it
        being compared for reliability.  Each field you compare will have:
        - one or more tags (so you can group fields)
        - a name
        - data type (string, int, decimal, hex to start)
        - a measurement level
        - an optional number of values to choose from
        - an optional set of potential/valid values.
        
    If this is used more broadly, will add columns as appropriate.
    '''

    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    

    # measurement levels
    MEASUREMENT_LEVEL_NOMINAL = StatsHelper.MEASUREMENT_LEVEL_NOMINAL
    MEASUREMENT_LEVEL_ORDINAL = StatsHelper.MEASUREMENT_LEVEL_ORDINAL
    MEASUREMENT_LEVEL_INTERVAL = StatsHelper.MEASUREMENT_LEVEL_INTERVAL
    MEASUREMENT_LEVEL_RATIO = StatsHelper.MEASUREMENT_LEVEL_RATIO

    # data types
    DATA_TYPE_INTEGER = "integer"
    DATA_TYPE_DECIMAL = "decimal"
    DATA_TYPE_HEX_HASH = "hex_hash"
    DATA_TYPE_STRING = "string"
    DATA_TYPE_LIST = [ DATA_TYPE_INTEGER, DATA_TYPE_DECIMAL, DATA_TYPE_HEX_HASH, DATA_TYPE_STRING ]
    DATA_TYPE_CHOICES = (
        ( DATA_TYPE_INTEGER, "Integer" ),
        ( DATA_TYPE_DECIMAL, "Decimal" ),
        ( DATA_TYPE_HEX_HASH, "Hexadecimal Hash" ),
        ( DATA_TYPE_STRING, "String" )
    )
    
    # truncation directions:
    TRUNCATE_FROM_LEFT = "left"
    TRUNCATE_FROM_RIGHT = "right"
    TRUNCATE_FROM_LIST = [ TRUNCATE_FROM_LEFT, TRUNCATE_FROM_RIGHT ]
    TRUNCATE_FROM_CHOICES = (
        ( TRUNCATE_FROM_LEFT, "Chop from left" ),
        ( TRUNCATE_FROM_RIGHT, "Chop from right" )
    )

    #----------------------------------------------------------------------
    # model fields
    #----------------------------------------------------------------------

    tags = TaggableManager( blank = True )
    name = models.CharField( max_length = 255 )
    data_type = models.CharField( max_length = 255, blank = True, null = True, choices = DATA_TYPE_CHOICES )
    measurement_level = models.CharField( max_length = 255, blank = True, null = True )
    value_count = models.IntegerField( blank = True, null = True )
    integer_base = models.IntegerField( blank = True, null = True )
    truncate_to_length = models.IntegerField( blank = True, null = True )
    truncate_from = models.CharField( max_length = 255, blank = True, null = True, choices = TRUNCATE_FROM_CHOICES )
    notes = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )
    
    
    #----------------------------------------------------------------------------
    # Meta class
    #----------------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:
        ordering = [ 'name', ]


    #----------------------------------------------------------------------------
    # class methods
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        detail_list = []
        temp_string = ""
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got a name?
        if ( ( self.name is not None ) and ( self.name != "" ) ):
        
            # got a label
            string_OUT += " - " + name
            
        #-- END check for name --#
        
        # got measurement_level?
        if ( ( self.measurement_level is not None ) and ( self.measurement_level != "" ) ):
        
            # got one
            detail_list.append( self.measurement_level )
        
        #-- END check for measurement level --#

        # got data_type?
        if ( ( self.data_type is not None ) and ( self.data_type != "" ) ):
        
            # got one
            detail_list.append( self.data_type )
        
        #-- END check to see if coder --#
        
        # any details?
        if ( len( detail_list ) > 0 ):
        
            # yes.  combine, separated by " ".
            temp_string = " ".join( detail_list )
            
            # add to string.
            string_OUT += " ( " + temp_string + " )"
            
        #-- END check to see if details --#
                
        return string_OUT

    #-- END method __str__() --#

    
#= END Field_Spec model ================================================#


@python_2_unicode_compatible
class Field_Spec_Value( models.Model ):
    
    '''
    Class to hold valid values for a given field.
    '''

    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    

    #----------------------------------------------------------------------
    # model fields
    #----------------------------------------------------------------------

    field_spec = models.ForeignKey( Field_Spec )
    value = models.CharField( max_length = 255 )
    
    #----------------------------------------------------------------------------
    # Meta class
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # class methods
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        detail_list = []
        temp_string = ""
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got field_spec?
        if ( self.field_spec ):
        
            # got one
            string_OUT += " - Field Spec: " + str( self.field_spec )
        
        #-- END check for field_spec --#

        # got a value?
        if ( ( self.value is not None ) and ( self.value != "" ) ):
        
            # got a label
            string_OUT += " - Value: " + name
            
        #-- END check for name --#
        
        return string_OUT

    #-- END method __str__() --#


#= END Field_Spec_Value model ================================================#


@python_2_unicode_compatible
class Reliability_Names_Coder_Data( models.Model ):

    '''
    Class to hold information on name detection choices within a given article
        for a given coder, for use in inter-coder reliability testing.  Making
        this class now, but not using it - will eventually want to remove these
        details from Reliability_Names, switch over to having a set of these
        records per name if I continue to add fields to test.
    '''

    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    


    #----------------------------------------------------------------------
    # model fields
    #----------------------------------------------------------------------

    # in Reliability_Names, so only one per person.
    #article = models.ForeignKey( Article, blank = True, null = True )
    #person = models.ForeignKey( Person, blank = True, null = True )
    #person_name = models.CharField( max_length = 255, blank = True, null = True )
    #person_type = models.CharField( max_length = 255, blank = True, null = True )
    #label = models.CharField( max_length = 255, blank = True, null = True )

    reliability_names = models.ForeignKey( Reliability_Names, blank = True, null = True )
    coder = models.ForeignKey( User, blank = True, null = True )
    coder_numeric_id = models.IntegerField( blank = True, null = True )
    detected = models.IntegerField( blank = True, null = True )
    person_id = models.IntegerField( blank = True, null = True )
    person_type = models.CharField( max_length = 255, blank = True, null = True )
    person_type_int = models.IntegerField( blank = True, null = True )
    article_data_id = models.IntegerField( blank = True, null = True )
    article_person_id = models.IntegerField( blank = True, null = True )
    first_quote_graph = models.IntegerField( blank = True, null = True )
    first_quote_index = models.IntegerField( blank = True, null = True )
    organization_hash = models.CharField( max_length = 255, blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )


    #----------------------------------------------------------------------------
    # Meta class
    #----------------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:
        ordering = [ 'reliability_names', 'coder', ]


    #----------------------------------------------------------------------------
    # class methods
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        temp_string = ""
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got a label?
        if ( self.reliability_names ):
        
            # got a label
            string_OUT += " - Reliability_Names: " + str( self.reliability_names )
            
        #-- END check for label --#
        
        # got coder details?
        if ( self.coder ):
        
            # yes.  Output a summary of coding.
            string_OUT += " - coder: " + str( self.coder.id ) + "; " + str( self.detected ) + "; " + str( self.person_id )
        
        #-- END check to see if coder --#
                
        return string_OUT

    #-- END method __str__() --#
     

#= END Reliability_Names_Coder_Data model =====================================#


@python_2_unicode_compatible
class Reliability_Names_Results( models.Model ):

    '''
    Class to hold agreement scores for comparisons between pairs of coders whose
        coding data is captured in Reliability_Names.  To start, holds results
        of agreement on detecting and looking up authors and subjects, and for 
        subjects, on deciding if subject was source or simply mentioned.
        For each, calculates percentage agreement and Krippendorff's Alpha.  If
        desired, can also calculate a modified version of Scott's Pi for nominal
        variables where there is little variation in the data (lots of 1s,
        almost no 0s, for example) - this is only implemented for author and
        subject detect (1 or 0), and subject type (0 through 3).

        sourcenet_analysis/examples/reliability/reliability-assess_name_data.py
    '''

    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    

 
    # field name prefixes
    PREFIX_AUTHOR = "author_"
    PREFIX_SUBJECT = "subject_"
    
    # standard suffixes
    SUFFIX_PERCENT = "_percent"
    SUFFIX_ALPHA = "_alpha"
    SUFFIX_PI = "_pi"
    SUFFIX_COUNT = "_count"
    
    # field name suffixes
    FIELD_DETECT_PERCENT = "detect_percent"
    FIELD_DETECT_ALPHA = "detect_alpha"
    FIELD_DETECT_PI = "detect_pi"
    FIELD_LOOKUP_PERCENT = "lookup_percent"
    FIELD_LOOKUP_ALPHA = "lookup_alpha"
    FIELD_LOOKUP_NONZERO_PERCENT = "lookup_non_zero_percent"
    FIELD_LOOKUP_NONZERO_ALPHA = "lookup_non_zero_alpha"
    FIELD_LOOKUP_NONZERO_COUNT = "lookup_non_zero_count"
    FIELD_TYPE_PERCENT = "type_percent"
    FIELD_TYPE_PERCENT = "type_alpha"
    FIELD_TYPE_PERCENT = "type_pi"
    FIELD_TYPE_NONZERO_PERCENT = "type_non_zero_percent"
    FIELD_TYPE_NONZERO_ALPHA = "type_non_zero_alpha"
    FIELD_TYPE_NONZERO_PI = "type_non_zero_pi"
    FIELD_TYPE_NONZERO_COUNT = "type_non_zero_count"
    FIELD_FIRST_QUOTE_GRAF_PERCENT = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF + SUFFIX_PERCENT
    FIELD_FIRST_QUOTE_GRAF_ALPHA = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF + SUFFIX_ALPHA
    FIELD_FIRST_QUOTE_GRAF_PI = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF + SUFFIX_PI
    FIELD_FIRST_QUOTE_GRAF_COUNT = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF + SUFFIX_COUNT
    FIELD_FIRST_QUOTE_INDEX_PERCENT = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX + SUFFIX_PERCENT
    FIELD_FIRST_QUOTE_INDEX_ALPHA = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX + SUFFIX_ALPHA
    FIELD_FIRST_QUOTE_INDEX_PI = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX + SUFFIX_PI
    FIELD_FIRST_QUOTE_INDEX_COUNT = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX + SUFFIX_COUNT
    FIELD_ORGANIZATION_HASH_PERCENT = Reliability_Names.FIELD_NAME_SUFFIX_ORGANIZATION_HASH + SUFFIX_PERCENT
    FIELD_ORGANIZATION_HASH_ALPHA = Reliability_Names.FIELD_NAME_SUFFIX_ORGANIZATION_HASH + SUFFIX_ALPHA
    FIELD_ORGANIZATION_HASH_PI = Reliability_Names.FIELD_NAME_SUFFIX_ORGANIZATION_HASH + SUFFIX_PI
    FIELD_ORGANIZATION_HASH_COUNT = Reliability_Names.FIELD_NAME_SUFFIX_ORGANIZATION_HASH + SUFFIX_COUNT

 
    #----------------------------------------------------------------------
    # model fields
    #----------------------------------------------------------------------

    label = models.CharField( max_length = 255, blank = True, null = True )
    coder1 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_results_coder1_set" )
    coder1_coder_index = models.IntegerField( blank = True, null = True )
    coder2 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_results_coder2_set" )
    coder2_coder_index = models.IntegerField( blank = True, null = True )
    author_count = models.IntegerField( blank = True, null = True )
    author_detect_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    author_detect_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_detect_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_lookup_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    author_lookup_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_lookup_non_zero_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    author_lookup_non_zero_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_lookup_non_zero_count = models.IntegerField( blank = True, null = True )
    author_type_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    author_type_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_type_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_type_non_zero_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    author_type_non_zero_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_type_non_zero_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_type_non_zero_count = models.IntegerField( blank = True, null = True )
    subject_count = models.IntegerField( blank = True, null = True )
    subject_detect_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_detect_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_detect_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_lookup_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_lookup_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_lookup_non_zero_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_lookup_non_zero_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_lookup_non_zero_count = models.IntegerField( blank = True, null = True )
    subject_type_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_type_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_type_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_type_non_zero_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_type_non_zero_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_type_non_zero_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_type_non_zero_count = models.IntegerField( blank = True, null = True )
    subject_first_quote_graf_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_first_quote_graf_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_first_quote_graf_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_first_quote_graf_count = models.IntegerField( blank = True, null = True )
    subject_first_quote_index_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_first_quote_index_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_first_quote_index_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_first_quote_index_count = models.IntegerField( blank = True, null = True )
    subject_organization_hash_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_organization_hash_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_organization_hash_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_organization_hash_count = models.IntegerField( blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )


    #----------------------------------------------------------------------------
    # Meta class
    #----------------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:
        ordering = [ 'label', 'coder1', 'coder2' ]


    #----------------------------------------------------------------------------
    # class methods
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        temp_string = ""
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got a label?
        if ( self.label ):
        
            # got a label
            string_OUT += " - label: " + self.label
            
        #-- END check for label --#
        
        # got coder details?
        if ( ( self.coder1 ) or ( self.coder2 ) ):
        
            # yes.  Output a summary of coding.
            string_OUT += " - coders: "
            
            temp_string = ""
            
            if ( self.coder1 ):
            
                # output details for coder 1
                string_OUT += "1"
                temp_string += " ====> 1 - " + str( self.coder1.id ) + "; " + str( self.coder1_detected ) + "; " + str( self.coder1_person_id )
                
            #-- END check to see if coder1 --#

            if ( self.coder2 ):
            
                # output details for coder 2
                string_OUT += "2"
                temp_string += " ====> 2 - " + str( self.coder2.id ) + "; " + str( self.coder2_detected ) + "; " + str( self.coder2_person_id )
                
            #-- END check to see if coder2 --#
        
            string_OUT += temp_string
        
        return string_OUT

    #-- END method __str__() --#
     

#= END Reliability_Names_Results model ========================================#


@python_2_unicode_compatible
class Reliability_Result_Details( models.Model ):

    '''
    Class to hold agreement scores for comparisons between pairs of coders.
        This model holds the results of one comparison.  For a given comparison,
        you store the name of the comparison, the value calculated, and the
        number of values compared.
    '''

    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    


    # comparison names
    COMPARISON_NAME_PERCENT_AGREE = "percent_agree"
    COMPARISON_NAME_KRIPP_ALPHA = "k_alpha"
    COMPARISON_NAME_POTTER_PI = "p_pi"
 
 
    #----------------------------------------------------------------------
    # model fields
    #----------------------------------------------------------------------


    reliability_names_results = models.ForeignKey( Reliability_Names_Results )
    field_spec = models.ForeignKey( Field_Spec )
    comparison_name = models.CharField( max_length = 255, blank = True, null = True )
    comparison_value = models.CharField( max_length = 255, blank = True, null = True )
    case_count = models.IntegerField( blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )


    #----------------------------------------------------------------------------
    # Meta class
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # class methods
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        temp_string = ""
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got field_spec?
        if ( self.field_spec ):
        
            # got one
            string_OUT += " - Field Spec: " + str( self.field_spec )
        
        #-- END check for field_spec --#
        
        string_OUT += " - "

        # got a comparison_name?
        if ( ( self.comparison_name is not None ) and ( self.comparison_name != "" ) ):
        
            # got a label
            string_OUT += self.comparison_name + " = "
            
        #-- END check for comparison_name --#
        
        # got a comparison_value?
        if ( ( self.comparison_value is not None ) and ( self.comparison_value != "" ) ):
        
            # got a label
            string_OUT += self.comparison_value
            
        #-- END check for comparison_value --#
        
        return string_OUT

    #-- END method __str__() --#
     

#= END Reliability_Names_Result_Details model ========================================#


