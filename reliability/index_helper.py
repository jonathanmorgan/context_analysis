from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2017 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet_analysis.

sourcenet_analysis is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet_analysis is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet. If not, see http://www.gnu.org/licenses/.
'''

# ! TODO - Pull over all per-index crap from reliability_names_builder.

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

# sourcenet imports
from sourcenet.models import Article
from sourcenet.models import Article_Data
from sourcenet.models import Article_Subject
from sourcenet.models import Person

# sourcenet_analysis imports
from sourcenet_analysis.models import Reliability_Names
from sourcenet_analysis.reliability.index_info import IndexInfo
from sourcenet_analysis.reliability.coder_index_info import CoderIndexInfo

#-------------------------------------------------------------------------------
# class definitions
#-------------------------------------------------------------------------------


class IndexInfo( object ):
    
    
    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    


    # Logger name
    LOGGER_NAME = "sourcenet_analysis.reliability.coder_index_builder"

    # information about table.
    TABLE_MAX_CODERS = 10
    
    # INDEX_INFO_* variables
    INDEX_INFO_INDEX = "index"
    INDEX_INFO_PRIORITIZED_CODER_LIST = "prioritized_coder_list"
    INDEX_INFO_CODER_ID_TO_PRIORITY_MAP = "coder_id_to_priority_map"
    
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
        
        # quick reference - coder User ID to instance map.
        self.m_coder_id_to_instance_map = {}        

        # master index info map.
        self.m_index_to_info_map = {}

        # limit users included
        self.m_limit_to_user_id_list = []
        self.m_exclude_user_id_list = []
        
        # exception helper
        self.exception_helper = ExceptionHelper()
        self.exception_helper.set_logger_name( self.LOGGER_NAME )
        self.exception_helper.logger_debug_flag = True
        self.exception_helper.logger_also_print_flag = False
        
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
        me = "add_coder_at_index"
        coder_id_to_instance_dict = {}
        limit_to_user_id_list = []
        coder_user_id = -1
        coder_index = -1
        coder_priority = None
        is_valid_index = False
        index_info = None
        coder_user = None
        
        # get maps from instance
        coder_id_to_instance_dict = self.get_coder_id_to_instance_map()
        limit_to_user_id_list = self.get_limit_to_user_id_list()
        
        # init from input parameters.
        coder_user_id = coder_id_IN
        coder_index = index_IN
        coder_priority = priority_IN
        
        # got ID?
        if ( ( coder_user_id is not None ) and ( int( coder_user_id ) > 0 ) ):
        
            # do we have a valid index value?
            is_valid_index = self.is_index_valid( coder_index )
            if ( is_valid_index == True ):
            
                # yes.  Retrieve index info.
                index_info = self.get_info_for_index( coder_index )
                
                # add the coder.
                index_info.add_coder( coder_user_id, coder_priority )
                
                # Lookup the user.
                coder_user = User.objects.get( id = coder_user_id )
                
                # add to internal map of coder ID to User instance.
                coder_id_to_instance_dict[ coder_user_id ] = coder_user

                # is user in approved coder user list?
                if ( coder_user_id not in limit_to_user_id_list ):
                
                    # not in list - add.
                    limit_to_user_id_list.append( coder_user_id )
                    
                #-- END check to see if user in approved coder user list. --#
                
            else:
            
                # no index - broken.
                status_OUT = "No index - can't associate user with no index."
            
            #-- END check to see if index present. --#
        
        else:
        
            # no coder ID - broken.
            status_OUT = "No coder ID - can't associate user if no user."
        
        #-- END check to see if valid ID. --#

        return status_OUT        
        
    #-- END method add_coder_at_index() --#
    

    def build_index_info( self, *args, **kwargs ):
        
        '''
        Loops over indices represented in index_to_info_map.  For each, in
            IndexInfo instance, calls build_index_info().
            
        Updated information is stored within each IndexInfo instance, and in the
            IndexHelper instance.  Returns index-to-info dictionary that is
            housed inside this helper.
        '''
        
        # return reference
        index_to_info_map_OUT = {}
        
        # declare variables
        index_to_info_dict = None
        current_index = None
        current_index_info = None
        
        # get index-to-info map
        index_to_info_dict = self.get_index_to_info_map()
        
        # loop over indexes present in map.
        for current_index, current_index_info in six.iteritems( index_to_info_dict ):
        
            # call build_index_info() on info object, forcing rebuild.
            current_index_info.build_index_info( *args, **kwargs )
            
        #-- END loop over IndexInfo instances. --#
        
        index_to_info_map_OUT = index_to_info_dict
        
        return index_to_info_map_OUT
        
    #-- END method build_index_info() --#


    def get_coder_for_index( self, index_IN ):
        
        '''
        Accepts a coder index.  Uses it to get ID of coder associated with that
           index with the highest priority, and returns instance of that User.
           If none found, returns None.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        is_valid_index = False
        index_info = None
        
        # do we have a valid index value?
        is_valid_index = self.is_index_valid( index_IN )
        if ( is_valid_index == True ):

            # get index info for the requested index
            index_info = self.get_info_for_index( index_IN )
            
            # call get_coder_for_index() there.
            instance_OUT = index_info.get_coder_for_index()
            
        else:
        
            # bad index - return None.
            instance_OUT = None
        
        #-- END check to see if valid index. --#
        
        return instance_OUT        
        
    #-- END method get_coder_for_index() --#
    
        
    def get_coder_id_to_instance_map( self ):
        
        '''
        Retrieves nested m_coder_id_to_instance_map from this instance.
        '''
        
        # return reference
        value_OUT = None
        
        # get value and return it.
        value_OUT = self.m_coder_id_to_instance_map
        
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
        is_valid_index = False
        index_info = None
        
        # do we have a valid index value?
        is_valid_index = self.is_index_valid( index_IN )
        if ( is_valid_index == True ):

            # get index info
            index_info = self.get_info_for_index( index_IN )
            
            # ask for coders from index_info.
            coder_list_OUT = index_info.get_coders_for_index()
            
        else:
        
            # bad index - return empty list.
            coder_list_OUT = []
        
        #-- END check to see if valid index. --#
                
        return coder_list_OUT        
        
    #-- END method get_coders_for_index() --#
    
        
    def get_exclude_user_id_list( self ):
        
        '''
        Retrieves nested m_exclude_user_id_list from this instance.
        '''
        
        # return reference
        value_OUT = None
        
        # get value and return it.
        value_OUT = self.m_exclude_user_id_list
        
        return value_OUT
        
    #-- END method get_exclude_user_id_list() --#


    def get_info_for_index( self, index_IN ):
        
        '''
        Accepts a coder index.  Retrieves IndexInfo instance for that index.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        is_valid_index = False
        index_to_info_dict = None
        my_index_info = None

        # do we have a valid index value?
        is_valid_index = self.is_index_valid( index_IN )
        if ( is_valid_index == True ):

            # valid - retrieve m_index_to_info_map
            index_to_info_dict = self.get_index_to_info_map()
    
            # Is this index in the map?
            if ( index_IN not in index_to_info_dict ):
            
                # no.  Create IndexInfo, add it to the map.
                my_index_info = IndexInfo()
                my_index_info.index = index_IN
                index_to_info_dict[ index_IN ] = my_index_info
                
            #-- END check to see if info for index. --#
            
            # get info from index to info map
            instance_OUT = index_to_info_dict.get( index_IN, None )

        else:
        
            # no index, no instance
            instance_OUT = None
            
        #-- END check to see if valid index value --#
        
        return instance_OUT        
        
    #-- END method get_info_for_index() --#
    
        
    def get_index_priority_map( self, index_IN ):
        
        '''
        Accepts a coder index.  Uses it to get associated map of Coder User IDs
            to priority values, for use when more than one coder maps to a given
            index.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        is_valid_index = False
        index_to_priorities_dict = {}
        priority_dict = {}

        # do we have a valid index value?
        is_valid_index = self.is_index_valid( index_IN )
        if ( is_valid_index == True ):
        
            # got an index - get map from instance
            index_to_priorities_dict = self.index_to_coder_priorities_map
            
            # try to use index to get back priority_dict.
            if ( index_IN in index_to_priorities_dict ):
            
                # index is present, grab and return the value for the index.
                priority_dict = index_to_priorities_dict.get( index_IN, None )
            
            else:
            
                # no index present in the dictionary.  Add empty dictionary for
                #     the index, then come calling again.
                index_to_priorities_dict[ index_IN ] = {}
                priority_dict = self.get_index_priority_map( index_IN )
                
            #-- END retrieval of priority_dict. --#
            
            instance_OUT = priority_dict
        
        #-- END check to see if index. --#
                                            
        return instance_OUT        
        
    #-- END method get_index_priority_map() --#
    
        
    def get_index_to_info_map( self, *args, **kwargs ):
        
        '''
        Checks to see if we've already generated index_to_info_map.  If so,
            returns it.  If not, builds it, stores it, then returns it.
        '''
        
        # return reference
        index_to_info_map_OUT = None
        
        # see if we have a map already populated.
        index_to_info_map_OUT = self.m_index_to_info_map
        
        # got anything?
        if ( ( index_to_info_map_OUT is None )
            or ( isinstance( index_to_info_map_OUT, dict ) == False )
            or ( len( index_to_info_map_OUT ) <= 0 ) ):
        
            # no.  Make instance, store it, then return it.
            index_to_info_map_OUT = {}
            self.m_index_to_info_map = index_to_info_map_OUT
            
        #-- END check to see if map already made --#
            
        return index_to_info_map_OUT        
        
    #-- END method get_index_to_info_map() --#
    
        
    def get_limit_to_user_id_list( self ):
        
        '''
        Retrieves nested m_limit_to_user_id_list from this instance.
        '''
        
        # return reference
        value_OUT = None
        
        # get value and return it.
        value_OUT = self.m_limit_to_user_id_list
        
        return value_OUT
        
    #-- END method get_limit_to_user_id_list() --#


    def is_index_valid( self, index_IN ):
        
        '''
        Checks the index passed in to see if it is valid:
        - not None
        - integer
        - greater than 0
        - less then or equal to self.TABLE_MAX_CODERS
        
        If valid, returns True.  If not, returns False.
        '''
        
        # return reference
        is_valid_OUT = False
    
        # do we have a valid index value?
        if ( ( coder_index is not None )
            and ( isinstance( coder_index, six.integer_types ) == True )
            and ( coder_index > 0 )
            and ( coder_index <= self.TABLE_MAX_CODERS ) ):
            
            # valid.
            is_valid_OUT = True
            
        else:
        
            # not valid.
            is_valid_OUT = False
            
        #-- END index validity check. --#
        
        return is_valid_OUT
        
    #-- END method is_index_valid() --#


    def map_index_to_coder_for_article( self, article_IN, mapping_type_IN = MAPPING_INDEX_TO_CODER, *args, **kwargs ):

        '''
        Accepts an article for which we want to pick a coder for each index
            in our output.  For a given article, get index info, then for each
            index with coders, go through the prioritized list of coders and use
            the first that has an Article_Data in the current article.  Use this
            information to build a map of indices to coder User instances, and 
            then loop over that in processing (so no longer doing something with
            every coder, just looping over indices that had at least one coder).
            
        Preconditions: This object needs to have been configured with at least
            one coder assigned to an index.
            
        Postconditions: Returns dictionary that maps each index that has been
            assigned one or more coders to the User instance of coder who should
            be used to provide data for that index for the provided article.
        '''

        # return reference
        map_OUT = {}

        # declare variables - coding processing.
        me = "map_index_to_coder_for_article"
        my_logger = None
        article_data_qs = None
        index_to_info_map = None
        index = -1
        index_info = None
        current_coder = None
        current_coder_id = -1
        current_coder_index_list = None
        found_coder_for_index = False
        
        # init logger
        my_logger = self.exception_helper        
        
        # article
        if ( article_IN is not None ):
    
            # retrieve the Article_Data QuerySet.    
            article_data_qs = article_IN.article_data_set.all()

            # loop over indexes that have info (so just those that are
            #     configured, not all).  For each, call IndexInfo method
            #     get_coder_for_article() to get coder for article, add it to
            #     the return map.
            map_OUT = {}
            
            # to start, get index-to-info map
            index_to_info_map = self.get_index_to_info_map()

            # loop.
            for current_index, index_info in six.iteritems( index_to_info_map ):
            
                # init
                found_coder_for_index = False
                current_coder = None
            
                # use index_info to get coder for article.
                current_coder = index_info.get_coder_for_article( article_IN )
                
                # got something?
                if ( current_coder is not None ):
                
                    # got one.  How do we map?
                    if ( mapping_type_IN == self.MAPPING_INDEX_TO_CODER ):
                    
                        # Place coder in map of index to coder...
                        map_OUT[ current_index ] = current_coder
                    
                    elif ( mapping_type_IN == self.MAPPING_CODER_TO_INDEX ):
                    
                        # already in map? - coders can map to multiple indices.
                        if ( current_coder not in map_OUT ):
                        
                            # no - add list for coder.
                            map_OUT[ current_coder ] = []
                            
                        #-- END check to see if coder already in map --#
                        
                        # get coder's list.
                        current_coder_index_list = map_OUT.get( current_coder, None )
                        
                        # add index to list if not already there.
                        if ( current_index not in current_coder_index_list ):
                        
                            # not in list - add.
                            current_coder_index_list.append( current_index )
                            
                        #-- END check to see if index in coder's index list. --#
                        
                    #-- END check to see mapping type --#

                    # ...and set found flag to True to avoid
                    #     more lookups.
                    found_coder_for_index = True
                    
                else:
                
                    # no coder found.
                    found_coder_for_index = False
                
                #-- END check to see if coder for article. --#
                    
            #-- END loop over index info --#
            
        #-- END check to see if article actually passed in. --#
        
        return map_OUT
        
    #-- END method map_index_to_coder_for_article() --#


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
        self.m_index_to_info_map = map_IN
        
        return status_OUT

    #-- END function set_index_to_info_map() --#


#-- END class ReliabilityNamesBuilder --#
