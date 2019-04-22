from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2016-2017 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context_analysis.

context_analysis is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context_analysis is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context_analysis. If not, see http://www.gnu.org/licenses/.
'''

# ! TODO - integrate index_helper.py so each index can have its own settings.

# python built-in libraries
import hashlib

# python package imports
import six

# django imports
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# python_utilities
from python_utilities.exceptions.exception_helper import ExceptionHelper
from python_utilities.integers.integer_helper import IntegerHelper
from python_utilities.json.json_helper import JSONHelper
from python_utilities.logging.logging_helper import LoggingHelper
from python_utilities.status.status_container import StatusContainer

# context_text imports
from context_text.models import Article
from context_text.models import Article_Data
from context_text.models import Article_Subject
from context_text.models import Person

# context_analysis imports
from context_analysis.models import Reliability_Names
from context_analysis.reliability.index_helper import IndexHelper

#-------------------------------------------------------------------------------
# class definitions
#-------------------------------------------------------------------------------


class ReliabilityNamesBuilder( object ):
    
    
    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    


    # Logger name
    LOGGER_NAME = "context_analysis.reliability.reliability_names_builder"

    # article info dictionary field names
    ARTICLE_ID = "article_id"
    ARTICLE_DATA_ID_LIST = "article_data_id_list"
    ARTICLE_CODER_ID_LIST = "article_coder_id_list"
    AUTHOR_INFO_DICT = "author_info_dict"
    SUBJECT_INFO_DICT = "subject_info_dict"
    
    # source and author info dicts will use same field names.
    PERSON_ID = "person_id"
    PERSON_NAME = "person_name"
    PERSON_LAST_NAME = "person_last_name"
    PERSON_FIRST_NAME = "person_first_name"
    PERSON_CODER_ID_TO_CODING_INFO_DICT = "person_coder_id_to_coding_info_dict"
    # PERSON_CODER_ID_LIST = "person_coder_id_list"
    
    # coder-specific person coding info map
    PERSON_CODING_INFO_CODER_ID = Reliability_Names.FIELD_NAME_SUFFIX_CODER_ID
    PERSON_CODING_INFO_PERSON_TYPE = Reliability_Names.FIELD_NAME_SUFFIX_PERSON_TYPE
    PERSON_CODING_INFO_PERSON_TYPE_INT = Reliability_Names.FIELD_NAME_SUFFIX_PERSON_TYPE_INT
    PERSON_CODING_INFO_ARTICLE_PERSON_ID = Reliability_Names.FIELD_NAME_SUFFIX_ARTICLE_PERSON_ID
    PERSON_CODING_INFO_FIRST_QUOTE_GRAF = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF
    PERSON_CODING_INFO_FIRST_QUOTE_INDEX = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX
    PERSON_CODING_INFO_ORGANIZATION_HASH = Reliability_Names.FIELD_NAME_SUFFIX_ORGANIZATION_HASH
    PERSON_CODING_INFO_NAME_LIST = [ PERSON_CODING_INFO_CODER_ID, PERSON_CODING_INFO_PERSON_TYPE, PERSON_CODING_INFO_PERSON_TYPE_INT, PERSON_CODING_INFO_ARTICLE_PERSON_ID, PERSON_CODING_INFO_FIRST_QUOTE_GRAF, PERSON_CODING_INFO_FIRST_QUOTE_INDEX, PERSON_CODING_INFO_ORGANIZATION_HASH ]
    
    # person types
    PERSON_TYPE_AUTHOR = "author"
    PERSON_TYPE_SUBJECT = "subject"
    PERSON_TYPE_SOURCE = "source"

    # Article_Subject subject_types
    SUBJECT_TYPE_MENTIONED = Article_Subject.SUBJECT_TYPE_MENTIONED
    SUBJECT_TYPE_QUOTED = Article_Subject.SUBJECT_TYPE_QUOTED

    # person or subject types to int ID map.
    PERSON_TYPE_TO_INT_MAP = {}
    PERSON_TYPE_TO_INT_MAP[ PERSON_TYPE_AUTHOR ] = 1
    PERSON_TYPE_TO_INT_MAP[ PERSON_TYPE_SUBJECT ] = 2
    PERSON_TYPE_TO_INT_MAP[ PERSON_TYPE_SOURCE ] = 3
    PERSON_TYPE_TO_INT_MAP[ SUBJECT_TYPE_MENTIONED ] = 2
    PERSON_TYPE_TO_INT_MAP[ SUBJECT_TYPE_QUOTED ] = 3
        
    # Organizations ERROR value
    ORG_HASH_ERROR_STRING = "ORG_HASH_ERROR"
    
    # information about table.
    TABLE_MAX_CODERS = 10
    
    # INDEX_INFO_* variables
    INDEX_INFO_INDEX = "index"
    INDEX_INFO_PRIORITIZED_CODER_LIST = "prioritized_coder_list"
    
    # index-to-coder mappings
    MAPPING_INDEX_TO_CODER = "index-to-coder"
    MAPPING_CODER_TO_INDEX = "coder-to-index"

    
    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # ! ==> call parent's __init__()
        super( ReliabilityNamesBuilder, self ).__init__()

        # ! ==> declare instance variables
        
        # info for each article ID.
        self.article_id_to_info_map = {}
        
        # keep track of all users we encounter.
        self.m_coder_id_to_instance_map = {}        

        # master index info map.
        self.m_index_helper = IndexHelper()

        # multiple coders for an index
        self.index_to_coder_priorities_map = {}
        
        # initialize priorities map
        temp_index = -1
        current_index = -1
        for temp_index in range( self.TABLE_MAX_CODERS ):
        
            # add 1, since we are 1-indexed, not 0-indexed.
            current_index = temp_index + 1
            self.index_to_coder_priorities_map[ current_index ] = {}
        
        #-- END loop over indices to initialize priorities map --#
        
        # limit users included
        self.m_limit_to_user_id_list = []
        self.m_exclude_user_id_list = []
        
        # variable to hold desired automated coder type
        self.limit_to_automated_coder_type = ""
        self.automated_coder_type_include_list = []
        
        # exception helper
        self.m_exception_helper = ExceptionHelper()
        self.m_exception_helper.set_logger_name( self.LOGGER_NAME )
        self.m_exception_helper.logger_debug_flag = True
        self.m_exception_helper.logger_also_print_flag = False
        
        # debug variables
        self.debug_output_json_file_path = ""
        
    #-- END method __init__() --#
    

    def add_coder_at_index( self, coder_id_IN, index_IN, priority_IN = None, *args, **kwargs ):
        
        '''
        Accepts a coder ID and an index.  Updates all the stuff in this instance
            to make sure the coder is tied to the index passed in.
        '''
        
        # return reference
        status_OUT = ""
        
        # declare variables
        my_index_helper = None
        
        # get index_helper
        my_index_helper = self.get_index_helper()
        
        # add coder.
        status_OUT = my_index_helper.add_coder_at_index( coder_id_IN, index_IN, priority_IN, *args, **kwargs )
        
        return status_OUT        
        
    #-- END method add_coder_at_index() --#
    

    def build_index_info( self, *args, **kwargs ):
        
        '''
        Loops over indices from 1 to self.TABLE_MAX_CODERS.  For each, creates
            a dictionary that contains information on the index:
            - "prioritized_coder_list" - list of coders who combined make up the coding for a given index, in the order of their priorities from highest first to lowest last.
            
        Postconditions: stores the info dictionary inside the instance, and
            returns it.
        '''
        
        # return reference
        index_to_info_map_OUT = {}
        
        # declare variables
        my_index_helper = None
        
        # get IndexHelper instance
        my_index_helper = self.get_index_helper()

        # call method on helper.
        my_index_helper.build_index_info( *args, **kwargs )
        
        # return map
        index_to_info_map_OUT = my_index_helper.get_index_to_info_map( *args, **kwargs )
        
        return index_to_info_map_OUT
        
    #-- END method build_index_info() --#


    def build_reliability_names_data( self, tag_list_IN = None, label_IN = None ):
    
        '''
        Accepts tag list, label to apply to resulting Reliability_Names rows.
            Passes tag list to process_articles(), then passes the label to
            output_reliability_data().
        '''
        
        # return reference
        status_OUT = ""
    
        # got tag list?
        if ( ( tag_list_IN is not None ) and ( len( tag_list_IN ) > 0 ) ):
        
            # and got label?
            if ( ( label_IN is not None ) and ( label_IN != "" ) ):
            
                # got what we need.  Process articles.
                my_reliability_instance.process_articles( tag_list_IN )

                # output to database.
                my_reliability_instance.output_reliability_data( label_IN )
                
            else:
            
                # no label - error.
                status_OUT = "ERROR - must pass in a label."
            
            #-- END check to see if label --#
            
        else:
        
            # no tag list - error.
            status_OUT = "ERROR - must pass in a list of tags for filtering article data."

        #-- END check to see if tag list. --#
        
        return status_OUT
        
    #-- END method build_reliability_names_data() --#
    
    
    def filter_article_data( self, article_data_qs_IN ):
        
        '''
        Accepts Article_Data QuerySet.  Filters it based on any nested variables
            that relate to filtering.  Returns filtered QuerySet.
           
        Filters on:
            - self.limit_to_automated_coder_types - list of automated coder types we want included.\
            - list of coder IDs we want to limit to.
            - 
            - ).  Returns filtered QuerySet.
        '''
        
        # ! TODO - make static version that this calls.
        # ! TODO - push these all up into Article_Data model filter_records() method.
        
        # return reference
        qs_OUT = None
        
        # declare variables
        me = "filter_article_data"
        logging_message = ""
        my_index_helper = None
        my_logger = None
        automated_coder_type = None
        coder_type_list = None
        coder_id_include_list = None
        coder_id_exclude_list = None
        
        # init logger
        my_logger = LoggingHelper.get_a_logger( self.LOGGER_NAME )        
        
        # get index helper
        my_index_helper = self.get_index_helper()
        
        # start by just returning what is passed in.
        qs_OUT = article_data_qs_IN
        
        # see if we have a single automated coder type.
        automated_coder_type = self.limit_to_automated_coder_type
        if ( ( automated_coder_type is not None ) and ( automated_coder_type != "" ) ):
        
            # got one.  Filter the QuerySet.
            coder_type_list = [ automated_coder_type, ]

            logging_message = "- limit to single coder type: " + str( automated_coder_type ) + "; coder_type_list = " + str( coder_type_list )
            # print( logging_message )
            my_logger.debug( "**** " + logging_message )            
        
        else:
        
            # no single value, check if there is a list.
            coder_type_list = self.automated_coder_type_include_list
        
            logging_message = "- limit automated coding to coder types in list: coder_type_list = " + str( coder_type_list )
            # print( logging_message )
            my_logger.debug( "**** " + logging_message )            
        
        #-- END check to see if automated coder type. --#
        
        # anything in automated coder type include list?
        if ( ( isinstance( coder_type_list, list ) == True ) and ( len( coder_type_list ) > 0 ) ):
        
            qs_OUT = Article_Data.filter_automated_by_coder_type( qs_OUT, coder_type_list )
        
        #-- END check to see if anything in coder_type_list.

        # got a list of coder IDs to limit to?
        coder_id_include_list = self.get_limit_to_user_id_list()
        if ( ( isinstance( coder_id_include_list, list ) == True ) and ( len( coder_id_include_list ) > 0 ) ):
        
            qs_OUT = qs_OUT.filter( coder__in = coder_id_include_list )
        
        #-- END check to see if anything in coder_type_list.

        # got a list of coder IDs to explicitly exclude?
        coder_id_exclude_list = self.get_exclude_user_id_list()
        if ( ( isinstance( coder_id_exclude_list, list ) == True ) and ( len( coder_id_exclude_list ) > 0 ) ):
        
            qs_OUT = qs_OUT.exclude( coder__in = coder_id_exclude_list )
        
        #-- END check to see if anything in coder_type_list.

        return qs_OUT
    
    #-- END method filter_article_data() --#


    def get_coder_for_index( self, index_IN ):
        
        '''
        Accepts a coder index.  Uses it to get ID of coder associated with that
           index and returns instance of that User.  If none found, returns
           None.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        my_index_helper = None
        
        # get index_helper
        my_index_helper = self.get_index_helper()
        
        # add coder.
        instance_OUT = my_index_helper.get_coder_for_index( index_IN )
        
        return instance_OUT        
        
    #-- END method get_coder_for_index() --#
    
        
    def get_coder_id_to_instance_map( self ):
        
        '''
        Retrieves nested m_coder_id_to_instance_map from this instance.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_index_helper = None
        helper_map = None
        current_user_id = None
        current_user_instance = None
        
        # get the nested variable
        value_OUT = self.m_coder_id_to_instance_map
        
        # update with information from index helper.
        my_index_helper = self.get_index_helper()
        helper_map = self.m_coder_id_to_instance_map
        for current_user_id, current_user_instance in six.iteritems( helper_map ):
        
            # check to see if ID is in local map.
            if ( current_user_id not in value_OUT ):
            
                # not in our local map.  Add it.
                value_OUT[ current_user_id ] = current_user_instance
        
            #-- END check to see if helper user is in local map --#        
        
        #-- END loop over IndexHelper map. --#
                       
        return value_OUT
        
    #-- END method get_coder_id_to_instance_map() --#


    def get_coders_for_index( self, index_IN ):
        
        '''
        Accepts a coder index.  Uses it to get list of User instances of coders
            associated with that index, in priority order, highest first to
            lowest last.  If none found, returns empty list.
            
        Postconditions: If there are two coders with the same priority, they
            will be together in the list in the appropriate position for their
            priority, but arbitrarily ordered from invocation to invocation (so
            in no particular order).  You've been warned.  If you care, don't
            assign two coders the same priority, and/or don't have multiple
            coders assigned to a given index with no priorities.
        '''
        
        # return reference
        coder_list_OUT = []
        
        # declare variables
        me = "get_coders_for_index"
        debug_message = ""
        my_index_helper = None

        # get index helper
        my_index_helper = self.get_index_helper()
        
        # call helper method
        coder_list_OUT = my_index_helper.get_coders_for_index( index_IN )
                
        return coder_list_OUT        
        
    #-- END method get_coders_for_index() --#
    
        
    def get_exclude_user_id_list( self, update_from_index_helper_IN = True ):
        
        '''
        Retrieves nested m_exclude_user_id_list from this instance.
        '''
        
        # return reference
        value_OUT = None
                
        # get value and return it.
        value_OUT = self.m_exclude_user_id_list
        
        return value_OUT
        
    #-- END method get_exclude_user_id_list() --#


    def get_index_helper( self ):
        
        '''
        Retrieves nested m_index_helper from this instance.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_index_helper = None
        
        # get value and return it.
        value_OUT = self.m_index_helper
        
        return value_OUT
        
    #-- END method get_index_helper() --#


    def get_index_to_info_map( self, *args, **kwargs ):
        
        '''
        Checks to see if we've already generated index_to_info_map.  If so,
            returns it.  If not, builds it, stores it, then returns it.
        '''
        
        # return reference
        index_to_info_map_OUT = None
        
        # declare variables
        my_index_helper = None
        
        # get index helper
        my_index_helper = self.get_index_helper()
        
        # call this method on helper.
        index_to_info_map_OUT = my_index_helper.get_index_to_info_map( *args, **kwargs )
            
        return index_to_info_map_OUT        
        
    #-- END method get_index_to_info_map() --#
    
        
    def get_limit_to_user_id_list( self, update_from_index_helper_IN = True ):
        
        '''
        Retrieves nested m_limit_to_user_id_list from this instance.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_index_helper = None
        helper_user_id_include_list = None
        current_user_id = None
        
        # get value and return it.
        value_OUT = self.m_limit_to_user_id_list
        
        # update from IndexHelper?
        if ( ( update_from_index_helper_IN == True )
            or ( value_OUT is None )
            or ( len( value_OUT ) == 0 ) ):
        
            # get list from IndexHelper instance.
            my_index_helper = self.get_index_helper()
            helper_user_id_include_list = my_index_helper.get_limit_to_user_id_list()
            
            # loop, checking to make sure each is already in our local list.
            for current_user_id in helper_user_id_include_list:
            
                # is it in local list?
                if ( current_user_id not in value_OUT ):
                
                    # no.  Add it.
                    value_OUT.append( current_user_id )
                    
                #-- END check to see if current user not in list. --#
                
            #-- END loop over helper user include list. --#
            
        #-- end check to see if we update. --#
        
        return value_OUT
        
    #-- END method get_limit_to_user_id_list() --#


    def map_index_to_coder_for_article( self, article_IN, mapping_type_IN = MAPPING_INDEX_TO_CODER, *args, **kwargs ):

        '''
        Accepts an article for which we want to pick a coder for each index
            in our output.  This is a passthrough to the nested IndexHelper
            index.
            
        Preconditions: This object needs to have been configured with at least
            one coder assigned to an index.
            
        Postconditions: returns map of indices to the coder who should be used
            to provide data for that index for the provided article.
        '''

        # return reference
        map_OUT = {}

        # declare variables - coding processing.
        me = "map_index_to_coder_for_article"
        my_logger = None
        my_index_helper = None
        
        # init logger
        my_logger = self.m_exception_helper        
        
        # article
        if ( article_IN is not None ):
    
            # get index_helper
            my_index_helper = self.get_index_helper()
            
            # call IndexHelper method.
            map_OUT = my_index_helper.map_index_to_coder_for_article( article_IN, mapping_type_IN = mapping_type_IN )

        #-- END check to see if article actually passed in. --#
        
        return map_OUT
        
    #-- END method create_index_to_coder_map_for_article() --#


    def output_reliability_data( self,
                                 label_IN = "",
                                 include_undetected_IN = False ):
    
        '''
        Accepts article_info_dict_IN, dictionary that maps article IDs to the
           following:
           - article_id - ID of article.
           - article_data_id_list - list of IDs of Article_Data instances for the
              article.
           - article_coder_id_list - list of IDs of Coders who coded the article.
           - author_dict - dictionary that maps person IDs of authors to dictionary
              that contains details of author, including author ID, name, and 
              map of coder IDs who detected the author to their coding info for
              the author.
           - source_dict - dictionary that maps person IDs of sources to dictionary
              that contains details of source, including source ID, name, and
              map of coder IDs who detected the subject to their coding info for
              the subject.
              
        Loops over the items in the dictionary, processing each.  For each article,
           gets dictionaries of authors and sources and for each author and source,
           outputs a row to the reliability table containing coding information.
           
        Preconditions: expects that you already ran process_articles() with this
           instance.
        '''
    
        # declare variables.
        article_info_dict_IN = None
        article_info_count = -1
        article_info_counter = -1
        current_article_info_dict = {}
        my_article_id = -1
        my_article_info = {}
        my_article_data_id_list = []
        my_article_coder_id_list = []
        my_author_info_dict = {}
        my_subject_info_dict = {}
        my_article = None
        current_coder_index = -1
        my_person_id = -1
        my_person_info_dict = {}
        reliability_row = -1
        
        # get map of article IDs to attribution info.
        article_info_dict_IN = self.article_id_to_info_map
        
        # make sure we have something to output.
        if article_info_dict_IN is not None:
        
            # not None.  Initialize count variables.
            article_info_count = len( article_info_dict_IN )
            article_info_counter = 0
            
            # loop over info passed in.
            for my_article_id, my_article_info in six.iteritems( article_info_dict_IN ):
            
                # retrieve elements contained in article_info:
                my_article_data_id_list = my_article_info.get( self.ARTICLE_DATA_ID_LIST, [] )
                my_article_coder_id_list = my_article_info.get( self.ARTICLE_CODER_ID_LIST, [] )
                my_author_info_dict = my_article_info.get( self.AUTHOR_INFO_DICT, {} )
                my_subject_info_dict = my_article_info.get( self.SUBJECT_INFO_DICT, {} )
                
                # set up information needed for reliability row output.
                
                # get article for article ID.
                my_article = Article.objects.get( id = my_article_id )
                
                # for reliability table output, run through author and subject
                #    info, creating a row for each author and subject.
    
                # got author info?
                if ( ( my_author_info_dict is not None ) and ( len ( my_author_info_dict ) > 0 ) ):
                
                    # loop over the info in the dictionary, calling function to
                    #    output a given person's row to the reliability table
                    #    for each.
                    for my_person_id, my_person_info_dict in six.iteritems( my_author_info_dict ):
                    
                        # call function to output reliability table row.
                        reliability_row = self.output_reliability_name_row( my_article,
                                                                            my_person_info_dict,
                                                                            self.PERSON_TYPE_AUTHOR,
                                                                            label_IN = label_IN,
                                                                            include_undetected_IN = include_undetected_IN )
                        print ( "- author: " + str( reliability_row ) )
                    
                    #-- END loop over author info ---#
                
                #-- END check to see if we have author info. --#
                
                # got subject info?
                if ( ( my_subject_info_dict is not None ) and ( len ( my_subject_info_dict ) > 0 ) ):
                
                    # loop over the info in the dictionary, calling function to
                    #    output a given person's row to the reliability table
                    #    for each.
                    for my_person_id, my_person_info_dict in six.iteritems( my_subject_info_dict ):
                    
                        # call function to output reliability table row.
                        reliability_row = self.output_reliability_name_row( my_article,
                                                                            my_person_info_dict,
                                                                            self.PERSON_TYPE_SUBJECT,
                                                                            label_IN = label_IN,
                                                                            include_undetected_IN = include_undetected_IN )
                        print ( "- source: " + str( reliability_row ) )
                    
                    #-- END loop over author info ---#
    
                #-- END check to see if we have author info. --#            
            
            #-- END loop over article_info_dict_IN --#
            
        #-- END check to see if we got something passed in. --#
        
    #-- END method output_reliability_data --##
    
    
    def output_reliability_name_row( self,
                                     article_IN,
                                     person_info_dict_IN,
                                     article_person_type_IN,
                                     label_IN = "",
                                     include_undetected_IN = False ):
        
        '''
        Accepts:
        - article_IN - article this person was detected within.
        - person_info_dict_IN, dictionary that maps person IDs to the
            following:
            - person_id - ID of person found in article.
            - person_name - String name of that person.
            - person_coder_id_to_coding_info_dict - dictionary that maps IDs of
                coders who detected and recorded the presence of that person to
                details of their coding.  For now, just has coder ID, person
                type, and Article_Person record ID.  Could have more information
                in the future.
        - article_person_type_IN, the type of the Article_Person children we are
            processing ("author" or "subject").
        - label_IN - label to assign to this set of data in the database.
        - include_undetected_IN - boolean flag - if True, include rows for
            Authors or Subjects detected by someone, but not by any coders
            included in the current specifications.  Defaults to False.
         
        Creates an instance of Reliability_Names, stores values from
            the dictionary in the appropriate columns, then saves it.
           
        Returns the row model instance, or None if error.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        me = "output_reliability_name_row"
        my_logger = None
        logging_message = ""
        reliability_instance = None
        my_person_id = -1
        my_person = None
        my_person_name = ""
        my_person_first_name = ""
        my_person_last_name = ""
        my_coder_person_info_dict = None

        # declare variables - coding processing.
        index_to_coder_map = None
        coder_count = -1
        current_coder_index = -1
        current_coder_user = None
        current_coder_id = -1
        current_person_coding_info = None
        current_coding_info_name = None
        current_coding_info_value = None
        index_used_list = []
        index_used_count = -1
        current_number = -1
        current_index = -1
        
        # declare variables - getting appropriate Article_Data for automated
        article_data_qs = None
        coder_article_data_qs = None
        coder_article_data_count = -1
        coder_article_data = None
        coder_article_data_id = -1
        
        # init logger
        my_logger = self.m_exception_helper        
        
        # article
        if ( article_IN is not None ):
    
            # retrieve the Article_Data QuerySet.    
            article_data_qs = article_IN.article_data_set.all()
            
            # For a given article, get index info, and then for each index with
            #     coders, go through the prioritized list of coders and use the
            #     first that has an Article_Data in the current article.  Use
            #     this information to build a map of indices to coder IDs, and
            #     then loop over that in processing below (so no longer doing
            #     something with every coder, just looping over indices that had
            #     at least one coder).
            index_to_coder_map = self.map_index_to_coder_for_article( article_IN )
                    
            # person_info
            if ( person_info_dict_IN is not None ):
            
                # person type.
                if ( ( article_person_type_IN is not None ) and ( article_person_type_IN != "" ) ):
                
                    # got everything.  make reliability row.
                    reliability_instance = Reliability_Names()
                    
                    # got a label?
                    if ( ( label_IN is not None ) and ( label_IN != "" ) ):
                    
                        # yes, there is a label.  Add it to row.
                        reliability_instance.label = label_IN
                    
                    #-- END check to see if label --#
                    
                    # get information from info dictionary
                    my_person_id = person_info_dict_IN.get( self.PERSON_ID, -1 )
                    my_person = Person.objects.get( id = my_person_id )
                    my_person_name = person_info_dict_IN.get( self.PERSON_NAME, None )
                    my_person_first_name = person_info_dict_IN.get( self.PERSON_FIRST_NAME, None )
                    my_person_last_name = person_info_dict_IN.get( self.PERSON_LAST_NAME, None )
                    my_coder_person_info_dict = person_info_dict_IN.get( self.PERSON_CODER_ID_TO_CODING_INFO_DICT, {} )
                    
                    # place info inside
                    reliability_instance.article = article_IN
                    reliability_instance.person = my_person
                    reliability_instance.person_name = my_person_name
                    reliability_instance.person_first_name = my_person_first_name
                    reliability_instance.person_last_name = my_person_last_name
                    reliability_instance.person_type = article_person_type_IN
                    
                    # check to see if more than TABLE_MAX_CODERS.
                    coder_count = len( my_coder_person_info_dict )
                    if ( coder_count > self.TABLE_MAX_CODERS ):
                    
                        # bad news - print error.
                        logging_message = "possible ERROR - more coders ( " + str( coder_count ) + " ) than table allows ( " + str( self.TABLE_MAX_CODERS ) + " ).\""
                        my_logger.output_debug_message( logging_message, method_IN = me, indent_with_IN = "====> ", do_print_IN = True )
                        
                    #-- END check to see if more coders than slots in table --#
                    
                    # ! ----> loop over indexes in index_to_coder_map
                    # new - no more complex logic to see whose priority wins
                    #     for a given index.  Coders are put in priority
                    #     order for each index, and then index_to_coder_map
                    #     contains the coder with the highest priority who
                    #     coded this article for each index.

                    # loop over the indices in our index-to-coder map.  Only
                    #     include coding by coders referenced in this map.
                    for current_coder_index, current_coder_user in six.iteritems( index_to_coder_map ):
                    
                        # get coder ID.
                        current_coder_id = current_coder_user.id
                        
                        # see if there is person information for that coder.
                        current_person_coding_info = my_coder_person_info_dict.get( current_coder_id, None )
                        
                        # got any person information?
                        if ( current_person_coding_info is not None ):
                        
                            # yes.  If automated, make sure we get the right
                            #     record.
                            coder_article_data = None
                            coder_article_data_id = -1
                            coder_article_data_qs = article_data_qs.filter( coder = current_coder_user )
                                                       
                            logging_message = "- in " + me + "(): before filtering, coder_article_data_qs.count() = " + str( coder_article_data_qs.count() )
                            my_logger.output_debug_message( logging_message, method_IN = me, indent_with_IN = "**** ", do_print_IN = False )
                            
                            # ! --------> if "automated" user, filter on coder_type
                            coder_article_data_qs = self.filter_article_data( coder_article_data_qs )
                            coder_article_data_count = coder_article_data_qs.count()
                            
                            logging_message = "after filtering, coder_article_data_qs.count() = " + str( coder_article_data_qs.count() )
                            my_logger.output_debug_message( logging_message, method_IN = me, indent_with_IN = "**** ", do_print_IN = False )            

                            # how many?
                            if ( coder_article_data_count == 1 ):
                            
                                # ...and store information.
                                coder_article_data = coder_article_data_qs.get()
                                coder_article_data_id = coder_article_data.id
                            
                                # add current index to index_used_list.
                                index_used_list.append( current_coder_index )
                            
                                # ! --------> place info in "coder<index>" fields.
                                
                                # coder# - reference to User who coded.
                                field_name = "coder" + str( current_coder_index )
                                setattr( reliability_instance, field_name, current_coder_user )
                                
                                # coder#_detected - 1, since coder detected this person.
                                field_name = "coder" + str( current_coder_index ) + "_detected"
                                setattr( reliability_instance, field_name, 1 )
    
                                # coder#_person_id - id of person (will be
                                #    subsequently used to smoosh rows together for
                                #    same name, different person IDs).
                                field_name = "coder" + str( current_coder_index ) + "_person_id"
                                setattr( reliability_instance, field_name, my_person_id )
                                
                                # ! ------------> loop over standard coding info fields
                                
                                # set fields from current_person_coding_info.
                                #     Each name in dictionary corresponds to
                                #     column in database table.
                                for current_coding_info_name, current_coding_info_value in six.iteritems( current_person_coding_info ):
                                
                                    # set field name using name.
                                    field_name = "coder" + str( current_coder_index ) + "_" + current_coding_info_name
                                    
                                    # use that field name to set value.
                                    setattr( reliability_instance, field_name, current_coding_info_value )
                                    
                                #-- END loop over coding info. --#

                                # coder#_article_data_id - id of coder's
                                #    Article_Data row.
                                # Got an ID?
                                if ( coder_article_data_id > 0 ):
                                
                                    # yes.  store it.
                                    field_name = "coder" + str( current_coder_index ) + "_article_data_id"
                                    setattr( reliability_instance, field_name, coder_article_data_id )
                                
                                #-- END check to see if Article_Data ID --#

                            else:
                            
                                # zero or more than one matching Article_Data...
                                logging_message = "ERROR - Either 0 or more than 1 Article_Data instances ( count = " + str( coder_article_data_count ) + " ) for coder " + str( current_coder_user ) + ".  Should only be 1."
                                my_logger.output_debug_message( logging_message, method_IN = me, indent_with_IN = "====> ", do_print_IN = True )
                            
                            #-- END check to see if single matching Article_Data --#    
                                                            
                        #-- END check to see if person info for coder. --#
                        
                    #-- END loop over active indexes for this article. --# 
                                                
                    # get count of indexes used.
                    index_used_count = len( index_used_list )
                    
                    # Check to see if we actually save() - Is either:
                    # - the count of indexes used greater than 0 (at least one selected coder detected the person)
                    # - OR include_undetected_IN == True? (we don't care if selected coders detected the person)
                    if ( ( index_used_count > 0 ) or ( include_undetected_IN == True ) ):
                    
                        # We are saving - either at least one coder detected
                        #     this person, or we are cool with empty rows.
                        
                        # sort list of indexes with an Article_Data record
                        #     for the current person.
                        index_used_list.sort()
                        
                        logging_message = "len( index_used_list ) = " + str( index_used_count ) + "; list = " + str( index_used_list )
                        my_logger.output_debug_message( logging_message, method_IN = me, indent_with_IN = "----> ", do_print_IN = True )
                        
                        # ! --------> default values in unused indices.
                        
                        # check to make sure that all indexes were used.
                        if ( index_used_count < self.TABLE_MAX_CODERS ):
                        
                            # not all used.  put zeroes in fields for indices
                            #    not in the list.
                            for current_number in range( self.TABLE_MAX_CODERS ):
                            
                                # increment value by 1.
                                current_index = current_number + 1
                                
                                # is it in the list?
                                if ( current_index not in index_used_list ):
                                
                                    # no - add values.
                                    
                                    # If you are going to be calculating
                                    #     reliability on a numeric column, you
                                    #     need to set it to 0 here for coders
                                    #     who did not detect the current person,
                                    #     else you'll have NaN problems in R.
                                    # If you don't set it here, column will get
                                    #     default value, usually NULL in SQL.

                                    # coder# - reference to User who should have coded.
                                    
                                    # first, check for user in index_to_coder_map.
                                    current_coder_user = index_to_coder_map.get( current_index, None )
                                    if ( current_coder_user is None ):
                                        
                                        # no - get coder with highest priority
                                        current_coder_user = self.get_coder_for_index( current_index )
                                        
                                    #-- END check to see current index has coder in index-to-coder map. --#
                                    field_name = "coder" + str( current_index )
                                    setattr( reliability_instance, field_name, current_coder_user )
                                    
                                    # coder#_detected - 0, since coder did not
                                    #    detect this person.
                                    field_name = "coder" + str( current_index ) + "_detected"
                                    setattr( reliability_instance, field_name, 0 )
        
                                    # coder#_person_id - id of person (0, since
                                    #    coder didn't detect this person).
                                    field_name = "coder" + str( current_index ) + "_person_id"
                                    setattr( reliability_instance, field_name, 0 )
                                                                    
                                    # coder#_person_type_int - person type of 
                                    #    person (0, since coder didn't detect
                                    #    this person).
                                    field_name = "coder" + str( current_index ) + "_person_type_int"
                                    setattr( reliability_instance, field_name, 0 )
                                    
                                #-- END check to make sure current index not already processed --#                                
                                
                            #-- END loop over numbers 1 through TABLE_MAX_CODERS --#
                            
                        #-- END check to see if all indices used. --#
                        
                        # save
                        reliability_instance.save()
                        
                    else:
                    
                        # No selected coder detected this person, and we do
                        #     not want to include undetected people.  Return
                        #     None, do not fill in or save row.
                        reliability_instance = None
                    
                    # return
                    instance_OUT = reliability_instance
    
                #-- END check to see if we have person type. --#
    
            #-- END check to see if we have person info. --#
    
        #-- END check to see if we have an article. --#
        
        return instance_OUT
        
    #-- END method output_reliability_name_row() --#


    def process_articles( self, tag_list_IN = [], limit_to_sources_IN = False, article_id_in_list_IN = [] ):

        '''
        Grabs articles with a tag in tag_list_IN.  For each, loops through their
           Article_Data to build a dictionary that maps article ID to article
           info. that includes:
           - article_id - ID of article.
           - article_data_id_list - list of IDs of Article_Data instances for the
              article.
           - article_coder_id_list - list of IDs of Coders who coded the article.
           - author_dict - dictionary that maps person IDs of authors to dictionary
              that contains details of author, including author ID, name, and list of
              coders who found the author.
           - source_dict - dictionary that maps person IDs of sources to dictionary
              that contains details of source, including source ID, name, and list of
              coders who found the source.
        '''

        # declare variables - retrieving reliability sample.
        me = "process_articles"
        my_logger = None
        logging_message = ""
        my_index_helper = None
        coder_id_include_list = None
        coder_id_exclude_list = None
        article_qs = None
        current_article = None
        article_data_qs = None
        current_query = None
        article_data_count = -1
        
        # declare variables - compiling information for articles.
        article_id = -1
        article_to_info_dict = None
        article_info_dict = None
        coder_id_to_instance_dict = None
        coder_counter = -1
        current_article_data = None
        article_data_id_list = None
        article_data_author_qs = None
        article_data_subject_qs = None
        article_coder_id_list = None
        article_data_id = -1
        article_data_coder = None
        article_data_coder_id = None
        person_type = ""
        author_info_dict = None
        subject_info_dict = None
        
        # declare variables - debug output.
        debug_file_output_path = ""
        json_string = ""
        json_file_handle = None

        # init logger
        my_logger = LoggingHelper.get_a_logger( self.LOGGER_NAME )
        
        # get index helper
        my_index_helper = self.get_index_helper()
        
        # retrieve master list of users we are to include, if it exists.
        coder_id_include_list = self.get_limit_to_user_id_list()
        coder_id_exclude_list = self.get_exclude_user_id_list()
        
        #-------------------------------------------------------------------------------
        # process articles to build data
        #-------------------------------------------------------------------------------
        
        # got a tag IN list?
        if ( ( tag_list_IN is not None ) and ( len( tag_list_IN ) > 0 ) ):

            # get articles with tags in list passed in.
            article_qs = Article.objects.filter( tags__name__in = tag_list_IN )
            
        #-- END check to see if tag list --#
            
        # got an article id IN list?
        if ( ( article_id_in_list_IN is not None ) and ( len( article_id_in_list_IN ) > 0 ) ):

            # get articles with IDs in list passed in.
            article_qs = Article.objects.filter( id__in = article_id_in_list_IN )
            
        #-- END check to see if article ID IN list --#
            
        article_qs = article_qs.order_by( "id" )
        
        # build a dictionary that maps article ID to assorted details about the coding
        #    of each article.
        article_to_info_dict = self.article_id_to_info_map
        
        # For reference, also build up a dictionary of coder IDs that reference
        #    coder instances, so we know how many coders.
        coder_id_to_instance_dict = self.get_coder_id_to_instance_map()
        coder_counter = 0
        
        # loop over the articles.
        for current_article in article_qs:
        
            # initialize variables
            article_info_dict = {}
            article_data_id_list = []
            article_coder_id_list = []
            author_info_dict = {}
            subject_info_dict = {}
        
            # get article_id
            article_id = current_article.id
        
            # get article data for this article
            article_data_qs = current_article.article_data_set.all()
            
            # ! filter on automated coder_type, IDs of coders to include or
            #     exclude, if filters are specified.
            article_data_qs = self.filter_article_data( article_data_qs )
            
            # how many Article_Data?
            article_data_count = len( article_data_qs )
        
            # output summary row.
            logging_message = "- Article ID: " + str( current_article.id ) + "; Article_Data count: " + str( article_data_count )
            print( logging_message )
            my_logger.debug( "**** " + logging_message )
            
            # for each article, build a dictionary that maps article ID to article info.
            #    that includes:
            # - article_id - ID of article.
            # - article_data_id_list - list of IDs of Article_Data instances for the
            #    article.
            # - article_coder_id_list - list of IDs of Coders who coded the article.
            # - author_dict - dictionary that maps person IDs of authors to dictionary
            #    that contains details of author, including author ID, name, and list of
            #    coders who found the author.
            # - source_dict - dictionary that maps person IDs of sources to dictionary
            #    that contains details of source, including source ID, name, and list of
            #    coders who found the source.
            
            # check to see if article already has an info dictionary (it better not...).
            if article_id in article_to_info_dict:
            
                # retrieve info dictionary
                article_info_dict = article_to_info_dict.get( article_id, {} )
                
            else:
            
                # make new info dictionary and add reference to it to master dictionary.
                article_info_dict = {}
                article_to_info_dict[ article_id ] = article_info_dict
                
            #-- END check to see if article already has an information dictionary. --#
            
            # compile information.
            
            # loop over related Article_Data instances.
            for current_article_data in article_data_qs:
            
                # output summary row.
                logging_message = "---- - Article Data Info: " + str( current_article_data )
                print( logging_message )
                my_logger.debug( "******** " + logging_message )
    
                # get coder and coder's User ID.
                article_data_coder = current_article_data.coder
                article_data_coder_id = article_data_coder.id
                
                # make sure that:
                # - there either isn't a list of users to include, OR if there
                #     is a list of users to include, the coder is in the list.
                # - AND there either isn't a list of users to exclude, OR if
                #     there is a list of users to exclude, the coder is not in
                #     the list.
                if ( ( ( len( coder_id_include_list ) == 0 ) or ( article_data_coder_id in coder_id_include_list ) )
                    and ( ( len( coder_id_exclude_list ) == 0 ) or ( article_data_coder_id not in coder_id_exclude_list ) ) ):
                
                    # If not already there, add to list of IDs of coders for this article.
                    if article_data_coder_id not in article_coder_id_list:
            
                        # not there yet, add it.
                        article_coder_id_list.append( article_data_coder_id )
                        
                    #-- END check to see if ID is in coder ID list --#
                
                    # If not already there, add to master coder dictionary, also.
                    if article_data_coder_id not in coder_id_to_instance_dict:
            
                        # not there yet.  Increment coder counter.
                        coder_counter += 1
                        
                        # add coder to id to instance map.
                        coder_id_to_instance_dict[ article_data_coder_id ] = article_data_coder
                        
                    #-- END check to see if ID is in master coder dictionary --#
                                
                    # add Article_Data ID to list.
                    article_data_id = current_article_data.id
                    article_data_id_list.append( article_data_id )
                    
                    # get lists of authors and subjects.
                    article_data_author_qs = current_article_data.article_author_set.all()
    
                    # all subjects, or just sources?
                    if ( limit_to_sources_IN == True ):
    
                        # just sources.
                        article_data_subject_qs = current_article_data.get_quoted_article_sources_qs()
                        
                    else:
                    
                        # all subjects (the default).
                        article_data_subject_qs = current_article_data.article_subject_set.all()
                        
                    #-- END check to see if all subjects or just sources. --#
                    
                    # call process_person_qs for authors.
                    person_type = self.PERSON_TYPE_AUTHOR
                    author_info_dict = self.process_person_qs( article_data_coder, article_data_author_qs, author_info_dict, person_type )
                            
                    # and call process_person_qs for subjects.
                    person_type = self.PERSON_TYPE_SUBJECT
                    subject_info_dict = self.process_person_qs( article_data_coder, article_data_subject_qs, subject_info_dict, person_type )
                    
                else:
                
                    # not processing coding by this user.  Move on.
                    pass
                    
                #-- END check to see if we are including current user's coding. --#
                        
            #-- END loop over related Article_Data
            
            # update article info dictionary
            article_info_dict[ self.ARTICLE_ID ] = article_id
            article_info_dict[ self.ARTICLE_DATA_ID_LIST ] = article_data_id_list
            article_info_dict[ self.ARTICLE_CODER_ID_LIST ] = article_coder_id_list
            article_info_dict[ self.AUTHOR_INFO_DICT ] = author_info_dict
            article_info_dict[ self.SUBJECT_INFO_DICT ] = subject_info_dict    
        
            # shouldn't need to do anything more - reference to this dictionary is
            #    already in the master map of article IDs to article info.
        
        #-- END loop over articles. --#
        
        # ! output debug JSON to a file?
        debug_file_output_path = self.debug_output_json_file_path
        if ( ( debug_file_output_path is not None ) and ( debug_file_output_path != "" ) ):
        
            # user wants us to try to output JSON.
            json_string = JSONHelper.pretty_print_json( self.article_id_to_info_map )

            # open file and write json_string to it.
            with open( debug_file_output_path, "w" ) as json_file_handle:
            
                # write out the json string.
                json_file_handle.write( json_string )
            
            #-- END with json_file_handle --#
        
        #-- END check to see if we output debug JSON. --#

    #-- END method process_articles() --#


    def process_person_qs( self, coder_IN, article_person_qs_IN, person_info_dict_IN, article_person_type_IN ):
        
        '''
        Accepts User instance of user who coded the Article, Article_Person
            QuerySet (either Article_Author or Article_Subject) and a dictionary
            to be used to build up a map of IDs to information on people found
            in a given article. Loops over entries and builds up this dictionary
            that maps IDs of persons identified in the text to details on the
            person (including the Person's ID, string name, and a map of coder
            IDs to a dictionary for each coder who detected that person with
            their coding info, at this point their ID and the type they assigned
            to the person).  Returns the updated person_info_dict dictionary.
        '''
        
        # return reference
        person_info_dict_OUT = {}
        
        # declare variables
        me = "process_person_qs"
        my_logger = None
        current_article_person = None
        coder_id = -1
        person_instance = None
        person_id = -1
        person_name = ""
        person_parsed_name = None
        person_info = None
        person_coding_info_dict = None
        person_coding_info = None
        current_person_type = None
        current_person_type_int = None
        current_organization = ""
        encoded_organization = ""
        org_hash_object = None
        org_hash = ""

        # declare variables - subject-specific processing.
        is_subject = False
        subject_quote_qs = None
        subject_quote_count = -1
        subject_first_quote = None
        first_quote_graf = -1
        first_quote_index = -1
        
        # init logger
        my_logger = LoggingHelper.get_a_logger( self.LOGGER_NAME )
        
        # make sure we have a coder
        if ( coder_IN is not None ):
        
            # make sure we have a queryset.
            if ( article_person_qs_IN is not None ):
            
                # make sure we have a person type passed in.
                if ( ( article_person_type_IN is not None ) and ( article_person_type_IN != "" ) ):
            
                    # log the current person.
                    my_logger.debug( "--------> In " + me + ": current person type = " + str( article_person_type_IN ) )
                    
                    # got a dictionary passed in?
                    if ( person_info_dict_IN is not None ):
                    
                        person_info_dict_OUT = person_info_dict_IN
                    
                    #-- END check to see if we have a dictionary passed in. --#
            
                    # compile information on authors.
                    for current_article_person in article_person_qs_IN:
                    
                        # log the current person.
                        my_logger.debug( "====> In " + me + ": current person = " + str( current_article_person ) )
                        
                        # get coder ID.
                        coder_id = coder_IN.id
                        
                        # get current person type, different way based on person
                        #     type passed in.
                        # Article_Author QuerySet?
                        if ( article_person_type_IN == self.PERSON_TYPE_AUTHOR ):
                        
                            # only one type of author, so use the type passed in.
                            current_person_type = article_person_type_IN
                            is_subject = False
                        
                        # Article_Subject QuerySet?
                        elif ( ( article_person_type_IN == self.PERSON_TYPE_SUBJECT )
                            or ( article_person_type_IN == self.PERSON_TYPE_SOURCE ) ):
                        
                            # this is an Article_Subject, so get subject_type.
                            current_person_type = current_article_person.subject_type
                            is_subject = True
                            
                            # might have None.  If so, default to mentioned.
                            if ( current_person_type is None ):
                            
                                # it is None.  Sigh.  Default to mentioned.
                                current_person_type = self.SUBJECT_TYPE_MENTIONED
                            
                            #-- END check to see if person type is None --#
                        
                        else:
                        
                            # unknown Article_Person type.  set to empty string.
                            current_person_type = ""
                            is_subject = False
                        
                        #-- END check to see how we get person type. --#
                        
                        # log the current type.
                        my_logger.debug( "In " + me + ": current person type = " + str( current_person_type ) + " - to int map = " + str( self.PERSON_TYPE_TO_INT_MAP ) )
                        
                        # also get integer value
                        current_person_type_int = self.PERSON_TYPE_TO_INT_MAP.get( current_person_type, -1 )

                        # log the current type.
                        my_logger.debug( "In " + me + ": current person type as int = " + str( current_person_type_int ) )
                                                
                        # get person instance.
                        person_instance = current_article_person.person
                    
                        # got one?  Anonymous sources won't have one.  If we find a
                        #    record with no associated person, move on.
                        if ( person_instance is not None ):
                    
                            # get person ID and name values.
                            person_id = person_instance.id
                            person_name = person_instance.get_name_string()
                            person_parsed_name = person_instance.to_HumanName()
                            
                            # create coding info. for this coder.
                            person_coding_info = {}
                            
                            # ! Place data in person_coding_info
                            
                            # coder ID
                            person_coding_info[ self.PERSON_CODING_INFO_CODER_ID ] = coder_id
                            
                            # person type
                            person_coding_info[ self.PERSON_CODING_INFO_PERSON_TYPE ]  = current_person_type
                            person_coding_info[ self.PERSON_CODING_INFO_PERSON_TYPE_INT ]  = current_person_type_int
                            
                            # Article_Person child record ID.
                            person_coding_info[ self.PERSON_CODING_INFO_ARTICLE_PERSON_ID ] = current_article_person.id
                            
                            # if subject, tack on information on first quote
                            if ( is_subject == True ):
                            
                                # FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF = "first_quote_graf"
                                # FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX = "first_quote_index"
                                
                                # check to see if person has any quotes.
                                subject_quote_qs = current_article_person.article_subject_quotation_set.all()
                                subject_quote_count = subject_quote_qs.count()
                                if ( subject_quote_count > 0 ):
                                
                                    # we do.  Order by paragraph number, then
                                    #    index.
                                    subject_quote_qs = subject_quote_qs.order_by( "paragraph_number", "value_index" )
                                    
                                    # get the first record in the list.
                                    subject_quote_qs = subject_quote_qs[ : 1 ]
                                    subject_first_quote = subject_quote_qs.get()
                                    
                                    # retrieve and store the paragraph and index
                                    #    values
                                    first_quote_graf = subject_first_quote.paragraph_number
                                    first_quote_index = subject_first_quote.value_index
                                    
                                    # and store them.
                                    person_coding_info[ self.PERSON_CODING_INFO_FIRST_QUOTE_GRAF ] = first_quote_graf
                                    person_coding_info[ self.PERSON_CODING_INFO_FIRST_QUOTE_INDEX ] = first_quote_index
                                
                                #-- END check to see if we have quotes --#
                                
                            #-- END check to see if is subject. --#

                            # FIELD_NAME_SUFFIX_ORGANIZATION_HASH = "organization_hash"
                            current_organization = current_article_person.organization_string
                            
                            # see if there is an organization
                            if ( ( current_organization is not None ) and ( current_organization != "" ) ):
                            
                                # to start, wrap in try in case there are encoding
                                #    problems.
                                try:
                                
                                    # encode the string to "utf-8"
                                    encoded_organization = current_organization.encode( "utf-8" )
                                    
                                    # convert to sha256
                                    org_hash_object = hashlib.sha256( encoded_organization )
                                    org_hash = org_hash_object.hexdigest()
                                    
                                except Exception as e:
                                
                                    # exception
                                    self.m_exception_helper.process_exception( exception_IN = e, message_IN = "Exception caught converting organization_string to sha256 hash." )
                                
                                    # On error, store self.ORG_HASH_ERROR_STRING
                                    org_hash = self.ORG_HASH_ERROR_STRING
    
                                #-- END try/except --#
                                
                            else:
                            
                                # no organization, set to None.
                                org_hash = None
                                
                            #-- END check to see if any organization value to hash --#
                                
                            # store org_hash in person_coding_info
                            person_coding_info[ self.PERSON_CODING_INFO_ORGANIZATION_HASH ] = org_hash
    
                            # look for person in person info dictionary.
                            if person_id in person_info_dict_OUT:
                            
                                # person already encountered.  Add coding info
                                #    to the coding info list.
                                person_info = person_info_dict_OUT.get( person_id )
                                
                                # get person_coding_info_list.
                                person_coding_info_dict = person_info.get( self.PERSON_CODER_ID_TO_CODING_INFO_DICT )
                                
                                # append person_coding_info
                                person_coding_info_dict[ coder_id ] = person_coding_info
                                
                            else:
                            
                                # person not in the dictionary yet.  Create new dictionary.
                                person_info = {}
                                
                                # add information.
                                person_info[ self.PERSON_ID ] = person_id
                                person_info[ self.PERSON_NAME ] = person_name
                                person_info[ self.PERSON_FIRST_NAME ] = person_parsed_name.first
                                person_info[ self.PERSON_LAST_NAME ] = person_parsed_name.last
                                
                                # add person coding info. for this coder.
                                person_coding_info_dict = {}
                                person_coding_info_dict[ coder_id ] = person_coding_info
                                person_info[ self.PERSON_CODER_ID_TO_CODING_INFO_DICT ] = person_coding_info_dict
                                
                                # add info to return dictionary.
                                person_info_dict_OUT[ person_id ] = person_info
                                
                            #-- END check to see if person is already in the dictionary. --#
                            
                        else:
                        
                            # no person - output a message.
                            print( "In " + me + ": no person found for record: " + str( current_article_person ) )
                            
                        #-- END check to make sure that person is present. --#
            
                    #-- END loop over persons. --#
                    
                #-- END check to see if we have person type. --#
                
            #-- END check to see if QuerySet passed in. --#  
        
        #-- END check to see if Coder present --#
        
        return person_info_dict_OUT
        
    #-- END method process_person_qs() --#
    
    
    def set_index_helper( self, instance_IN ):
        
        '''
        Accepts IndexHelper instance, stores it internally.
        '''
        
        # return reference
        status_OUT = StatusContainer()
        
        # declare variables
        me = "set_index_to_info_map"
        
        # init status
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # store whatever is passed in.
        self.m_index_helper = instance_IN
        
        return status_OUT

    #-- END function set_index_helper() --#


    def set_index_to_info_map( self, map_IN, *args, **kwargs ):
        
        '''
        Accepts index_to_info_map, stores it internally.
        '''
        
        # return reference
        status_OUT = StatusContainer()
        
        # declare variables
        me = "set_index_to_info_map"
        
        # init status
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # store whatever is passed in.
        self.index_to_info_map = map_IN
        
        return status_OUT

    #-- END function set_index_to_info_map() --#


#-- END class ReliabilityNamesBuilder --#
