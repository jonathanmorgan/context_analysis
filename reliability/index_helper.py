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
    
    
    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # ! ==> call parent's __init__()
        super( ReliabilityNamesBuilder, self ).__init__()

        # ! ==> declare instance variables
        
        # tying coders to indexes in database.
        self.article_id_to_info_map = {}
        self.coder_id_to_instance_map = {}        

        # master index info map.
        self.index_to_info_map = {}

        # so a given user can be a part of multiple indexes, with a different
        #    priority in each.
        #self.coder_id_to_index_map = {}
        #self.coder_id_to_priority_map = {}
        
        # ! NEED THIS? - multiple coders for an index
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
        self.limit_to_user_ids = []
        self.exclude_user_ids = []
        
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
        coder_index_info = None
        #coder_id_to_index_dict = {}
        coder_id_to_instance_dict = {}
        limit_to_user_id_list = []
        coder_user_id = -1
        coder_index = -1
        coder_user = None
        is_priority_valid = False
        priority_status = None
        
        # get maps from instance
        #coder_id_to_index_dict = self.coder_id_to_index_map
        coder_id_to_instance_dict = self.coder_id_to_instance_map
        limit_to_user_id_list = self.limit_to_user_ids
        
        # init from input parameters.
        coder_user_id = coder_id_IN
        coder_index = index_IN
        coder_priority = None
        
        # got ID?
        if ( ( coder_user_id is not None ) and ( int( coder_user_id ) > 0 ) ):
        
            # got index?
            if ( ( coder_index is not None ) and ( int( coder_index ) > 0 ) ):
            
                # yes.  Lookup the user.
                coder_user = User.objects.get( id = coder_user_id )
                
                # Set all the things up internally.
                #coder_id_to_index_dict[ coder_user_id ] = coder_index
                coder_id_to_instance_dict[ coder_user_id ] = coder_user
                limit_to_user_id_list.append( coder_user_id )
                
                # set priority?
                is_priority_valid = IntegerHelper.is_valid_integer( priority_IN, must_be_greater_than_IN = -1 )
                if ( is_priority_valid == True ):

                    # priority value is valid - set priority.
                    priority_status = self.set_coder_priority( coder_user_id, priority_IN, index_IN )
                    
                #-- END check to see if priority value is valid --#
                                
                # Make CoderIndexInfo instance.
                coder_index_info = CoderIndexInfo( coder_user_id_IN = coder_user_id,
                                                   coder_instance_IN = coder_user,
                                                   index_IN = coder_index,
                                                   priority_IN =  )
                
                # add it to map of coder ID to info for current index.
                

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
        Loops over indices from 1 to self.TABLE_MAX_CODERS.  For each, creates
            a dictionary that contains information on the index:
            - "prioritized_coder_list" - list of coders who combined make up the coding for a given index, in the order of their priorities from highest first to lowest last.
            
        Postconditions: stores the info dictionary inside the instance, and
            returns it.
        '''
        
        # return reference
        index_to_info_map_OUT = {}
        
        # declare variables
        index_list = None
        current_index = -1
        index_info = None
        coder_list = None
        
        
        # create list of indices from 1 to self.TABLE_MAX_CODERS.
        index_list = range( 1, self.TABLE_MAX_CODERS + 1 )
        
        # loop
        for current_index in index_list:
        
            # create index_info
            index_info = {}
            
            # ! ----> add index
            index_info[ self.INDEX_INFO_INDEX ] = current_index
            
            # ! ----> retrieve coder list for index.
            coder_list = self.get_coders_for_index( current_index )
            
            # add result to info.
            index_info[ self.INDEX_INFO_PRIORITIZED_CODER_LIST ] = coder_list
            
            # add info to map
            index_to_info_map_OUT[ current_index ] = index_info
        
        #-- END loop over indices --#
        
        # save internally
        self.set_index_to_info_map( index_to_info_map_OUT )
        
        # return map
        index_to_info_map_OUT = self.get_index_to_info_map()
        
        return index_to_info_map_OUT
        
    #-- END method build_index_to_coder_list_map() --#


    def filter_article_data( self, article_data_qs_IN ):
        
        '''
        Accepts Article_Data QuerySet.  Filters it based on any nested variables
            that relate to filtering.  Returns filtered QuerySet.
           
        Filters on:
            - self.limit_to_automated_coder_types - list of automated coder types we want included.
            - ).  Returns filtered QuerySet.
        '''
        
        # return reference
        qs_OUT = None
        
        # declare variables
        me = "filter_article_data"
        logging_message = ""
        my_logger = None
        automated_coder_type = None
        coder_type_list = None
        coder_id_include_list = None
        coder_id_exclude_list = None
        
        # init logger
        my_logger = LoggingHelper.get_a_logger( self.LOGGER_NAME )        
        
        # start by just returning what is passed in.
        qs_OUT = article_data_qs_IN
        
        # see if we have a single coder type.
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
        coder_id_include_list = self.limit_to_user_ids
        if ( ( isinstance( coder_id_include_list, list ) == True ) and ( len( coder_id_include_list ) > 0 ) ):
        
            qs_OUT = qs_OUT.filter( coder__in = coder_id_include_list )
        
        #-- END check to see if anything in coder_type_list.

        # got a list of coder IDs to explicitly exclude?
        coder_id_exclude_list = self.exclude_user_ids
        if ( ( isinstance( coder_id_exclude_list, list ) == True ) and ( len( coder_id_exclude_list ) > 0 ) ):
        
            qs_OUT = qs_OUT.exclude( coder__in = coder_id_exclude_list )
        
        #-- END check to see if anything in coder_type_list.

        return qs_OUT
    
    #-- END method filter_article_data() --#


    def get_index_info_for_index( self, index_IN ):
        
        '''
        Accepts a coder index.  Retrieves map of coder User IDs to index info
            for that index.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        coder_info_map = None
        coder_count = -1

        # get list of coders for current index
        coder_list = self.get_coders_for_index( index_IN )
        
        # got anything?
        coder_count = len( coder_list )
        
        if ( coder_count > 0 ):
        
            # yes.  Return first item in the list (it is in priority order, from
            #     highest priority to lowest).
            instance_OUT = coder_list[ 0 ]
            print( "++++ found User: " + str( instance_OUT ) )
        
        #-- END check to see if we have a User ID. --#
        
        return instance_OUT        
        
    #-- END method get_coder_info_map_for_index() --#
    
        
    def get_coder_for_index( self, index_IN ):
        
        '''
        Accepts a coder index.  Uses it to get ID of coder associated with that
           index with the highest priority, and returns instance of that User.
           If none found, returns None.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        coder_list = None
        coder_count = -1

        # get list of coders for current index
        coder_list = self.get_coders_for_index( index_IN )
        
        # got anything?
        coder_count = len( coder_list )
        
        if ( coder_count > 0 ):
        
            # yes.  Return first item in the list (it is in priority order, from
            #     highest priority to lowest).
            instance_OUT = coder_list[ 0 ]
            print( "++++ found User: " + str( instance_OUT ) )
        
        #-- END check to see if we have a User ID. --#
        
        return instance_OUT        
        
    #-- END method get_coder_for_index() --#
    
        
    def get_coder_index( self, coder_id_IN ):
        
        '''
        Accepts a coder ID, retrieves and returns the index for that coder.
            Returns None if no associated index.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_coder_index"
        coder_index = -1
        
        # try to get index for coder.
        coder_index = self.coder_id_to_index_map.get( coder_id_IN, None )

        value_OUT = coder_index
        
        return value_OUT        
        
    #-- END method get_coder_index() --#
    
        
    def get_coder_priority( self, coder_id_IN, index_IN = None, default_priority_IN = -1 ):
        
        '''
        Accepts a coder ID and an index.  Uses this information to get the
            priority of the specified user, either in general, or in the context
            of the index passed in, if one present.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_coder_priority"
        coder_index = -1
        index_to_priority_map_dict = {}
        priority_map_dict = {}
        coder_priority = -1
        coder_index = -1
        
        # got an index?
        if ( index_IN is not None ):
        
            # passed in - use it.
            coder_index = index_IN
            
            # get priority map for selected index.
            priority_map_dict = self.get_index_priority_map( index_IN )
            
            # retrieve priority from there.
            coder_priority = priority_map_dict.get( coder_id_IN, None )
            
        #-- END check to see if coder's index passed in. --#

        # ! got a priority?
        if ( ( coder_priority is None )
            or ( isinstance( coder_priority, six.integer_types ) == False )
            or ( coder_priority < 0 ) ):
                
            # no.  Get coder ID to priority map.
            priority_map_dict = self.coder_id_to_priority_map
                
            # and then get the priority for the coder.
            coder_priority = priority_map_dict.get( coder_id_IN, None )

        #-- END check to see if we got a priority based on index. --#
        
        # store coder_priority in instance_OUT.
        value_OUT = coder_priority
        
        # got anything?
        if ( ( value_OUT is None ) or ( value_OUT < 0 ) ):
        
            # no.  Return the default.
            value_OUT = default_priority_IN
            
        #-- END check to see if value_OUT. --#
        
        return value_OUT        
        
    #-- END method get_coder_priority() --#
    
        
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
        coder_id_to_index_dict = {}
        coder_id_to_instance_dict = {}
        coder_user_id = -1
        coder_index = -1
        matching_user_id = -1
        matching_user_priority = -1
        user_id_list = []
        priority_list = []
        
        # declare variables - organize users
        coder_priority_to_user_list_map = {}
        id_count = -1
        coder_user_id = -1
        coder_priority = -1
        coder_user_instance = None
        id_index = -1
        priority_user_list = None
        priority_key_list = None
        priority_key = None
        
        # get maps from instance
        coder_id_to_index_dict = self.coder_id_to_index_map
        coder_id_to_instance_dict = self.coder_id_to_instance_map
        
        # first, loop over map of user ID to index to find all coders for the
        #     index.
        for coder_user_id, coder_index in six.iteritems( coder_id_to_index_dict ):
        
            # check to see if current index matches that passed in.
            if ( index_IN == coder_index ):
            
                # yes - get the ID...
                matching_user_id = coder_user_id
                
                # ...and get priority
                matching_user_priority = self.get_coder_priority( matching_user_id, index_IN )
                
                # add to running lists.
                user_id_list.append( matching_user_id )
                priority_list.append( matching_user_priority )
            
            #-- END check to see if indices match --#
            
        #-- END loop over ID-to-index map. --#
        
        debug_message = "for index " + str( index_IN ) + " - found IDs: " + str( user_id_list ) + " and priorities: " + str( priority_list )
        LoggingHelper.output_debug( debug_message,
                                    method_IN = me,
                                    indent_with_IN = "++++ " )
        
        # got any IDs?
        coder_priority_to_user_list_map = {}
        id_count = len( user_id_list )
        if ( id_count > 0 ):

            # more than one.  loop.
            id_index = -1
            for coder_user_id in user_id_list:
            
                # increment id_index
                id_index += 1
                
                # get priority at same index.
                coder_priority = priority_list[ id_index ]
                
                # get instance for user.
                coder_user_instance = coder_id_to_instance_dict.get( coder_user_id, None )
                
                # see if there is a user list for the current priority.
                if ( coder_priority not in coder_priority_to_user_list_map ):
                
                    # not yet.  Add one.
                    coder_priority_to_user_list_map[ coder_priority ] = []
                    
                #-- END check to see if list already in priority-to-user map --#
                
                # get list for current priority
                priority_user_list = coder_priority_to_user_list_map.get( coder_priority, None )
                
                # and append user to list.
                priority_user_list.append( coder_user_instance )
            
            #-- END loop over coder user IDs--#
            
            # get list of priorities (keys in the map)...
            priority_key_list = list( six.viewkeys( coder_priority_to_user_list_map ) )
            
            # ...and sort them in reverse order (largest first, to smallest).
            priority_key_list.sort( reverse = True )
            
            # for each priority, retrieve user list and combine it with the
            #     output list.
            coder_list_OUT = []
            for priority_key in priority_key_list:
            
                # get priority_user_list
                priority_user_list = coder_priority_to_user_list_map.get( priority_key, None )
                
                # got anything?
                if ( ( priority_user_list is not None )
                    and ( isinstance( priority_user_list, list ) == True )
                    and ( len( priority_user_list ) > 0 ) ):
                    
                    # yes, got one.  Add its values to the right end of the
                    #     list.
                    coder_list_OUT.extend( priority_user_list )
                
                #-- END check to see if user list for this priority --#

        #-- END check to see if we have User IDs. --#
        
        return coder_list_OUT        
        
    #-- END method get_coders_for_index() --#
    
        
    def get_index_priority_map( self, index_IN ):
        
        '''
        Accepts a coder index.  Uses it to get associated map of Coder User IDs
            to priority values, for use when more than one coder maps to a given
            index.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        index_to_priorities_dict = {}
        priority_dict = {}

        # got an index?
        if ( ( index_IN is not None )
            and ( isinstance( index_IN, six.integer_types ) == True )
            and ( index_IN > 0 ) ):
        
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
        index_to_info_map_OUT = self.index_to_info_map
        
        # got anything?
        if ( ( index_to_info_map_OUT is None )
            or ( isinstance( index_to_info_map_OUT, dict ) == False )
            or ( len( index_to_info_map_OUT ) <= 0 ) ):
        
            # no.  Build it, then return it.
            index_to_info_map_OUT = self.build_index_info()
            
        #-- END check to see if map already made --#
            
        return index_to_info_map_OUT        
        
    #-- END method get_index_to_info_map() --#
    
        
    def map_index_to_coder_for_article( self, article_IN, mapping_type_IN = MAPPING_INDEX_TO_CODER, *args, **kwargs ):

        '''
        Accepts an article for which we want to pick a coder for each index
            in our output.  Pulls in index-to-info map, uses it to choose from
            among the coders configured for each index.  Returns dictionary that
            maps each index that has been assigned one or more coders to the
            coder to use for the current article.
            
        Specifically, for a given article, get index info, and then for each
            index with coders, go through the prioritized list of coders and use
            the first that has an Article_Data in the current article.  Use this
            information to build a map of indices to coder IDs, and then loop
            over that in processing below (so no longer doing something with
            every coder, just looping over indices that had at least one coder).
            
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
        article_data_qs = None
        index_info_map = None
        index = -1
        index_info = None
        current_index = -1
        current_index_coder_list = None
        current_coder = None
        found_coder_for_index = False
        coder_article_data_qs = None
        article_data_count = -1
        
        # init logger
        my_logger = self.exception_helper        
        
        # article
        if ( article_IN is not None ):
    
            # retrieve the Article_Data QuerySet.    
            article_data_qs = article_IN.article_data_set.all()
            
            # ! TODO - figure out coder for each index.
            # Rather than use coder_id_to_index_map, for a given article, get
            #     index info, and then for each index with coders, go through
            #     the list of coders and use the first that has an Article_Data
            #     in the current article.

            # Build a map of indices to coder IDs, and then loop over that in
            #     processing below (so no longer doing something with every
            #     coder, just looping over indices that had at least one coder).
            index_to_coder_map_OUT = {}
            
            # to start, get index map
            index_info_map = self.get_index_to_info_map()

            # loop.
            for index, index_info in six.iteritems( index_info_map ):
            
                # get values from index_info
                current_index = index_info.get( self.INDEX_INFO_INDEX, -1 )
                current_index_coder_list = index_info.get( self.INDEX_INFO_PRIORITIZED_CODER_LIST, [] )
                
                # sanity check - make sure current_index = index.
                if ( index == current_index ):
                
                    # sanity check passed.  Check if we have a coder list.
                    if ( ( current_index_coder_list is not None )
                        and ( isinstance( current_index_coder_list, list ) == True )
                        and ( len( current_index_coder_list ) > 0 ) ):
                    
                        # we have a list.  Loop over coders to find first with
                        #     Article_Data for this article.
                        found_coder_for_index = False
                        for current_coder in current_index_coder_list:
                        
                            # coder already found?
                            if ( found_coder_for_index == False ):
                
                                # is there an article data by this coder for this
                                #     article?
                                try:
                                
                                    # do a get() where coder = current_coder
                                    coder_article_data_qs = article_data_qs.filter( coder = current_coder )
                                    
                                    # how many?
                                    article_data_count = coder_article_data_qs.count()
                                    
                                    # 1 or more?
                                    if ( article_data_count > 0 ):
    
                                        # got at least one.  How do we map?
                                        if ( mapping_type_IN == self.MAPPING_INDEX_TO_CODER ):
                                        
                                            # Place coder in map of index to coder...
                                            map_OUT[ current_index ] = current_coder
                                        
                                        elif ( mapping_type_IN == self.MAPPING_CODER_TO_INDEX ):
                                        
                                            # sanity check - already in map?
                                            if ( current_coder in map_OUT ):
                                            
                                                # Not the first time this coder was tied to an index.  A bad sign.  Log and move on?
                                                logging_message = "ERROR - coder " + str( current_coder ) + " is already in map, mapped to index " + str( map_OUT.get( current_coder, None ) ) + ".  Configuration is wrong. Should only have a given coder mapped to one index."
                                                my_logger.output_debug_message( logging_message, method_IN = me, indent_with_IN = "====> ", do_print_IN = True )
                                    
                                            #-- END check to see if already in map --# 
                                        
                                            # Place coder in map of index to coder...
                                            map_OUT[ current_coder ] = current_index
                                        
                                        #-- END check to see mapping type --#

                                        # ...and set found flag to True to avoid
                                        #     more lookups.
                                        found_coder_for_index = True
                                        
                                        # and, finally, call get(), so we can log
                                        #     if there are weird errors.
                                        article_data = coder_article_data_qs.get()
                                        
                                    #-- END check to see if anything returned. --#
                                    
                                except Article_Data.DoesNotExist as ad_dne:
                                
                                    # No match.  This is unexpected.  Log and move on?
                                    logging_message = "In " + me + "(): Article_Data.DoesNotExist caught, but after finding 1 or more Article_Data for the coder in question.  Something serious ain't right here.  Index = " + str( index ) + "; current_coder = " + str( current_coder ) + "."
                                    my_logger.process_exception( ad_dne, message_IN = logging_message )
                                    
                                except Article_Data.MultipleObjectsReturned as ad_mor:
                                
                                    # multiple Article_Data.  Hmmm...  Output a log
                                    #     message and move on.
                                    logging_message = "In " + me + "(): Article_Data.MultipleObjectsReturned caught - coder should have updated coding, rather than creating multiple.  Something ain't right here.  Index = " + str( index ) + "; current_coder = " + str( current_coder ) + "."
                                    my_logger.process_exception( ad_mor, message_IN = logging_message )
                                
                                except Exception as e:
                                
                                    # unexpected exception caught.  Log a message
                                    #     and move on.
                                    logging_message = "In " + me + "(): unexpected Exception caught.  Something definitely ain't right here.  Index = " + str( index ) + "; current_coder = " + str( current_coder ) + "."
                                    my_logger.process_exception( e, message_IN = logging_message )
                                
                                #-- END try-except to see if we have a coder --#
                                
                            #-- END check to see if already found a coder for this index --#
                
                        #-- END loop over this index's coder list --#
                        
                    else:
                    
                        # no coder list.  Log a message, omit this index, and
                        #     move on.
                        logging_message = "No coders for index " + str( index ) + ".  Moving on."
                        my_logger.output_debug_message( logging_message, method_IN = me  )
                        
                    #-- END check to see if there is a coder list. --#
                
                else:
                
                    logging_message = "ERROR - index ( \"" + str( index ) + "\" ) is not the same as the index stored in the info for " + str( index ) + " ( \"" + str( current_index ) + "\" )."
                    my_logger.output_debug_message( logging_message, method_IN = me, indent_with_IN = "====> ", do_print_IN = True )
                
                #-- END sanity check --#

            #-- END loop over index info --#
            
        #-- END check to see if article actually passed in. --#
        
        return map_OUT
        
    #-- END method create_index_to_coder_map_for_article() --#


    def set_coder_info_for_index( self, index_IN, coder_info_IN ):
        
        '''
        Accepts index and info.  Retrieves the map of coder IDs to info for the
            requested index.  Retrieves coder ID from info.  Stores the info in
            the map associated with the coder ID.  Returns a StatusContainer.
        '''
        
        # return reference
        status_OUT = StatusContainer()
        
        # declare variables
        index_coder_id_to_info_map = None
        
        # get coder ID to info map.
        index_coder_id_to_info_map = self.index_to_info_map
        
        return status_OUT
        
    #-- END method set_coder_info_for_index() --#

    
    def set_coder_priority( self, coder_id_IN, priority_IN, index_IN = None, *args, **kwargs ):
        
        '''
        Accepts a coder User ID, an integer priority for that coder, and an
            optional index for that coder.  Checks to make sure coder ID and
            priority are passed in.  If so, adds entry to map of coder IDs to
            priorities for the coder.  If index present, also adds an entry to
            map of indices to coder priorities within that index.  Returns
            StatusContainer instance.
        '''
        
        # return reference
        status_OUT = StatusContainer()
        
        # declare variables
        me = "set_coder_priority"
        coder_to_priority_dict = {}
        coder_index = -1
        index_priority_map = {}
        status_message = ""
        
        # init status
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # got a coder ID?
        if ( ( coder_id_IN is not None )
            and ( isinstance( coder_id_IN, six.integer_types ) == True )
            and ( coder_id_IN > 0 ) ):
            
            # got a coder ID - got a priority?
            if ( ( priority_IN is not None )
                and ( isinstance( priority_IN, six.integer_types ) == True )
                and ( priority_IN > 0 ) ):
                
                # add to coder_to_priority_dict
                coder_to_priority_dict = self.coder_id_to_priority_map
                coder_to_priority_dict[ coder_id_IN ] = priority_IN
                
                # got an index?
                if ( index_IN is not None ):
                
                    # passed in - use it.
                    coder_index = index_IN
                    
                else:
                
                    # see if one in memory already.
                    if ( coder_id_IN in self.coder_id_to_index_map ):
                    
                        # There is.  Use it.
                        coder_index = self.coder_id_to_index_map[ coder_id_IN ]
                        
                    #-- END check to see if coder associated with index. --#
                    
                #-- END check to see if coder's index passed in. --#
                
                # ! got an index?
                if ( ( coder_index is not None )
                    and ( isinstance( coder_index, six.integer_types ) == True )
                    and ( coder_index > 0 ) ):
                
                    # got an index - update the index-to-person_priority map.
                    index_priority_map = self.get_index_priority_map( coder_index )
                    
                    # set priority in this map, also.
                    index_priority_map[ coder_id_IN ] = priority_IN
                
                #-- END check to see if index for current person. --#
            
            else:
            
                # ERROR - must have a priority passed in.
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                status_message = "In " + me + ": No coder priority passed in ( value = \"" + str( priority_IN ) + "\" ), so can't set priority."
                status_OUT.add_message( status_message )
                
            #-- END check to see if priority passed in --#
            
        else:
        
            # ERROR - must have a coder ID passed in.
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
            status_message = "In " + me + ": No coder User ID passed in ( value = \"" + str( coder_id_IN ) + "\" ), so can't set priority."
            status_OUT.add_message( status_message )
        
        #-- END check to see if coder User ID passed in. --#
        
        return status_OUT
    
    #-- END method set_coder_priority() --#


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
