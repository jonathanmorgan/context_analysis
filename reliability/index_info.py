from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2017 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet_analysis.

sourcenet_analysis is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet_analysis is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet. If not, see http://www.gnu.org/licenses/.
'''

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
from sourcenet.models import Article_Data

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
    LOGGER_NAME = "sourcenet_analysis.reliability.index_info"

    # information about table.
    TABLE_MAX_CODERS = 10
    
    # INDEX_INFO_* variables
    INDEX_INFO_INDEX = "index"
    INDEX_INFO_PRIORITIZED_CODER_LIST = "prioritized_coder_list"
    INDEX_INFO_CODER_ID_TO_PRIORITY_MAP = "coder_id_to_priority_map"
    
    # debug flag
    DEBUG = False
    
    
    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # ! ==> call parent's __init__()
        super( IndexInfo, self ).__init__()

        # ! ==> declare instance variables
        
        # basics - what index am I?
        self.m_index = -1
        
        # master map of coder ID to coder index info.
        self.m_coder_id_to_info_map = {}
        
        # coder quick reference lookup tables.
        self.m_coder_id_to_instance_map = {}
        self.m_coder_id_to_priority_map = {}
        self.m_prioritized_coder_list = []
                
        # exception helper
        self.m_exception_helper = ExceptionHelper()
        self.m_exception_helper.set_logger_name( self.LOGGER_NAME )
        self.m_exception_helper.logger_debug_flag = True
        self.m_exception_helper.logger_also_print_flag = False
        
        # debug variables
        self.m_debug_output_json_file_path = ""
        
    #-- END method __init__() --#
    

    def __str__( self ):
        
        # return reference
        string_OUT = ""
        
        # declare variables
        current_value = None
        current_value_label = None
        field_output_list = []
        
        current_value = self.get_index()
        current_value_label = "index"
        if ( current_value is not None ):
        
            field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
            
        #-- END check to see if coder_user_id --#

        current_value = self.get_coder_id_to_info_map()
        current_value_label = "coder info"
        if ( current_value is not None ):
        
            field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
            
        #-- END check to see if coder_user_id --#

        # DEBUG?
        if ( self.DEBUG == True ):

            current_value = self.get_coder_id_to_instance_map()
            current_value_label = "id-to-instance-info"
            if ( current_value is not None ):
            
                field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
                
            #-- END check to see if coder_user_id --#
    
            current_value = self.get_coder_id_to_priority_map()
            current_value_label = "id-to-priority"
            if ( current_value is not None ):
            
                field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
                
            #-- END check to see if coder_user_id --#
            
            current_value = self.get_prioritized_coder_list( rebuild_IN = True )
            current_value_label = "get_prioritized_coder_list()"
            if ( current_value is not None ):
            
                field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
                
            #-- END check to see if coder_user_id --#
            
            current_value = self.get_prioritized_coder_id_list( rebuild_IN = True )
            current_value_label = "get_prioritized_coder_id_list()"
            if ( current_value is not None ):
            
                field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
                
            #-- END check to see if coder_user_id --#
            
            current_value = self.get_coders_for_index( rebuild_IN = True )
            current_value_label = "get_coders_for_index()"
            if ( current_value is not None ):
            
                field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
                
            #-- END check to see if coder_user_id --#
            
            current_value = self.get_coder_for_index()
            current_value_label = "get_coder_for_index()"
            if ( current_value is not None ):
            
                field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
                
            #-- END check to see if coder_user_id --#
            
        #-- END check to see if debug --#

        # convert output list to string
        string_OUT = "\n====>".join( field_output_list )
                
        return string_OUT
        
    #-- END method __str__() --#


    def add_coder( self, coder_id_IN, priority_IN = None, *args, **kwargs ):
        
        '''
        Accepts a coder ID and an optional priority.  Updates all the stuff in
            this instance to make sure the coder is added correctly, Including:
            - create and store CoderIndexInfo instance.
            - map coder's User ID to their User instance.
            - map coder's User ID to their priority.
        '''
        
        # return reference
        status_OUT = ""
        
        # declare variables
        coder_index_info = None
        coder_id_to_info_dict = None
        coder_user_id = -1
        coder_index = -1
        coder_user = None
        coder_priority = None
        is_priority_valid = False
        priority_status = None
        
        # get maps from instance
        coder_id_to_info_dict = self.get_coder_id_to_info_map()
        
        # init from input parameters.
        coder_user_id = coder_id_IN
        coder_user = None
        coder_index = self.get_index()
        coder_priority = priority_IN
        
        # got ID?
        if ( ( coder_user_id is not None ) and ( int( coder_user_id ) > 0 ) ):
        
            # got index?
            if ( ( coder_index is not None ) and ( int( coder_index ) > 0 ) ):
            
                # yes.  Lookup the user.
                coder_user = User.objects.get( id = coder_user_id )
                
                # Make CoderIndexInfo instance.
                coder_index_info = CoderIndexInfo( coder_user_id_IN = coder_user_id,
                                                   coder_instance_IN = coder_user,
                                                   index_IN = coder_index,
                                                   priority_IN = coder_priority )
                
                # add it to map of coder ID to info for current index.
                coder_id_to_info_dict[ coder_user_id ] = coder_index_info
                
                # always rebuild other derived index information.
                self.build_index_info()

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
        Creates any helpful derived information on this index that can be used
            for processing.  Includes:
            - self.m_coder_id_to_instance_map - map coder's User ID to their User instance.
            - self.m_coder_id_to_priority_map - map coder's User ID to their priority.
            - self.m_prioritized_coder_list - list of coder User instances for this
                index, in order of their priority, from highest to lowest.
            
        Postconditions: Returns StatusContainer.
        '''
        
        # return reference
        status_OUT = StatusContainer()
        
        # declare variables
        me = "build_index_info"
        status_message = None
        coder_info_map = None
        coder_user_id = None
        coder_info = None
        coder_list = None
        
        # init status
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # ! ----> clear out existing derived information
        self.m_coder_id_to_instance_map = {}
        self.m_coder_id_to_priority_map = {}
        self.m_prioritized_coder_list = None
        
        # ! ----> loop over coder info records.
        coder_info_map = self.get_coder_id_to_info_map()
        for coder_user_id, coder_info in six.iteritems( coder_info_map ):
        
            # update information for current coder:
            # ! --------> update id-to-instance map
            # ! --------> update id-to-priority map
            self.update_index_info_for_coder( coder_info )
            
        #-- END loop over coder info records --#
                
        # ! ----> rebuild coder list for index.
        coder_list = self.get_prioritized_coder_list( rebuild_IN = True )
        
        return status_OUT
        
    #-- END method build_index_info() --#


    def get_coder_for_article( self, article_IN, *args, **kwargs ):

        '''
        Accepts an article for which we want to pick a coder.  Returns User
            instance of coder to use for the current article.
            
        Specifically, for a given article, get index info, and then for each
            index with coders, go through the prioritized list of coders and use
            the first that has an Article_Data in the current article.
            
        Preconditions: This object needs to have been configured with at least
            one coder assigned to an index.
            
        Postconditions: returns User instance of coder for current article.
        '''

        # return reference
        coder_OUT = None

        # declare variables - coding processing.
        me = "get_coder_for_article"
        my_logger = None
        article_data_qs = None
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

            # For a given article, go through the prioritized list of coders and
            #     use the first that has an Article_Data in the current article.
            current_index_coder_list = self.get_prioritized_coder_list()
                
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

                                # got at least one.  Return this coder!
                                coder_OUT = current_coder

                                # ...and set found flag to True to avoid
                                #     more lookups.
                                found_coder_for_index = True
                                
                                # and, finally, call get(), so we can log
                                #     if there are weird errors.
                                article_data = coder_article_data_qs.get()
                                
                            #-- END check to see if anything returned. --#
                            
                        except Article_Data.DoesNotExist as ad_dne:
                        
                            # No match.  This is unexpected.  Log and move on?
                            logging_message = "In " + me + "(): Article_Data.DoesNotExist caught, but after finding 1 or more Article_Data for the coder in question.  Something serious ain't right here.  Index = " + str( self.get_index() ) + "; current_coder = " + str( current_coder ) + "."
                            my_logger.process_exception( ad_dne, message_IN = logging_message )
                            
                        except Article_Data.MultipleObjectsReturned as ad_mor:
                        
                            # multiple Article_Data.  Hmmm...  Output a log
                            #     message and move on.
                            logging_message = "In " + me + "(): Article_Data.MultipleObjectsReturned caught - coder should have updated coding, rather than creating multiple.  Something ain't right here.  Index = " + str( self.get_index() ) + "; current_coder = " + str( current_coder ) + "."
                            my_logger.process_exception( ad_mor, message_IN = logging_message )
                        
                        except Exception as e:
                        
                            # unexpected exception caught.  Log a message
                            #     and move on.
                            logging_message = "In " + me + "(): unexpected Exception caught.  Something definitely ain't right here.  Index = " + str( self.get_index() ) + "; current_coder = " + str( current_coder ) + "."
                            my_logger.process_exception( e, message_IN = logging_message )
                        
                        #-- END try-except to see if we have a coder --#
                        
                    #-- END check to see if already found a coder for this index --#
        
                #-- END loop over this index's coder list --#
                        
            else:
            
                # no coder list.  Log a message, omit this index, and
                #     move on.
                logging_message = "No coders for index " + str( self.get_index() ) + ".  Moving on."
                my_logger.output_debug_message( logging_message, method_IN = me  )
                
            #-- END check to see if there is a coder list. --#
            
        #-- END check to see if article actually passed in. --#
        
        return coder_OUT
        
    #-- END method get_coder_for_article() --#


    def get_coder_for_index( self ):
        
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
        coder_list = self.get_coders_for_index()
        
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
    
        
    def get_coder_id_to_info_map( self ):
        
        '''
        Retrieves nested m_coder_id_to_info_map from this instance.
        '''
        
        # return reference
        value_OUT = None
        
        # get value and return it.
        value_OUT = self.m_coder_id_to_info_map
        
        return value_OUT
        
    #-- END method get_coder_id_to_info_map() --#


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


    def get_coder_id_to_priority_map( self ):
        
        '''
        Retrieves nested m_coder_id_to_priority_map from this instance.
        '''
        
        # return reference
        value_OUT = None
        
        # get value and return it.
        value_OUT = self.m_coder_id_to_priority_map
        
        return value_OUT
        
    #-- END method get_coder_id_to_priority_map() --#


    def get_coder_priority( self, coder_id_IN, default_priority_IN = -1 ):
        
        '''
        Accepts a coder ID.  Uses this information to get the priority of the
            specified user in the context of the current index.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_coder_priority"
        coder_id_to_info_dict = None
        coder_info = None
        coder_priority = -1

        # retrieve the map of coder IDs to priorities.
        coder_id_to_info_dict = self.get_coder_id_to_info_map()
        
        # retrieve priority from there.
        coder_info = coder_id_to_info_dict.get( coder_id_IN, None )
        coder_priority = coder_info.get_priority()
            
        # ! got a priority?
        if ( ( coder_priority is None )
            or ( isinstance( coder_priority, six.integer_types ) == False )
            or ( coder_priority < 0 ) ):
                
            # no.  Return Default.
            coder_priority = default_priority_IN

        #-- END check to see if we got a priority based on index. --#
        
        # store coder_priority in value_OUT.
        value_OUT = coder_priority
                
        return value_OUT        
        
    #-- END method get_coder_priority() --#
    
        
    def get_coders_for_index( self, rebuild_IN = False ):
        
        '''
        Retrieves list of User instances of coders associated with this index,
            in priority order, highest first to lowest last.  If none found,
            returns empty list.
            
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

        # get value from instance.
        coder_list_OUT = self.get_prioritized_coder_list( rebuild_IN = rebuild_IN )
                
        return coder_list_OUT        
        
    #-- END method get_coders_for_index() --#
        
        
    def get_index( self ):
        
        '''
        Retrieves and returns the index from the current instance.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_index"
        
        value_OUT = self.m_index
        
        return value_OUT        
        
    #-- END method get_index() --#
    
        
    def get_prioritized_coder_id_list( self, rebuild_IN = False ):
        
        '''
        Retrieves list of User IDs of coders associated with this index,
            in priority order, highest first to lowest last.  If none found,
            returns empty list.
            
        Postconditions: If there are two coders with the same priority, they
            will be together in the list in the appropriate position for their
            priority, but arbitrarily ordered from invocation to invocation (so
            in no particular order).  You've been warned.  If you care, don't
            assign two coders the same priority, and/or don't have multiple
            coders assigned to a given index with no priorities.
        '''
        
        # return reference
        coder_id_list_OUT = []
        
        # declare variables
        me = "get_prioritized_coder_id_list"
        status_message = ""
        prioritized_coder_list = None
        current_coder = None
        current_coder_id = None
        
        # get prioritized coder/User instance list.
        prioritized_coder_list = self.get_prioritized_coder_list( rebuild_IN = rebuild_IN )
        
        # loop, grabbing ID from each instance and adding it to output list.
        for current_coder in prioritized_coder_list:
        
            # get id.
            current_coder_id = current_coder.id
            
            # add to the list.
            coder_id_list_OUT.append( current_coder_id )
            
        #-- END loop over coders. --#
                
        return coder_id_list_OUT        
        
    #-- END method get_prioritized_coder_id_list() --#
        
        
    def get_prioritized_coder_list( self, rebuild_IN = False ):
        
        '''
        Retrieves list of User instances of coders associated with this index,
            in priority order, highest first to lowest last.  If none found,
            returns empty list.
            
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
        me = "get_prioritized_coder_list"
        debug_message = ""
        coder_id_to_info_dict = None
        
        # declare variables - organize users
        coder_priority_to_user_list_map = {}
        id_count = -1
        coder_user_id = -1
        coder_info = -1
        coder_priority = -1
        coder_user_instance = None
        priority_user_list = None
        priority_key_list = None
        priority_key = None
        
        # get value from instance.
        coder_list_OUT = self.m_prioritized_coder_list
        
        # Do we need to build/rebuild?
        if ( ( coder_list_OUT is None ) or ( rebuild_IN == True ) ):
        
            # ! ==> Build/Rebuild!
            
            # Get map of coder user ID to info from instance
            coder_id_to_info_dict = self.get_coder_id_to_info_map()
    
            # loop over coders to build priority-to-user list.
            coder_priority_to_user_list_map = {}
            for coder_user_id, coder_info in six.iteritems( coder_id_to_info_dict ):
                
                # get priority.
                coder_priority = coder_info.get_priority()
                
                # get instance for user.
                coder_user_instance = coder_info.get_coder_user_instance()
                
                # see if there is a user list for the current priority.
                if ( coder_priority not in coder_priority_to_user_list_map ):
                
                    # not yet.  Add one.
                    coder_priority_to_user_list_map[ coder_priority ] = []
                    
                #-- END check to see if list already in priority-to-user map --#
                
                # get list for current priority
                priority_user_list = coder_priority_to_user_list_map.get( coder_priority, None )
                
                # and append user to list.
                priority_user_list.append( coder_user_instance )
            
            #-- END loop over coders --#
                
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
    
            #-- END loop over priorities. --#
            
            # store the list in this instance.
            self.set_prioritized_coder_list( coder_list_OUT )
            coder_list_OUT = self.get_prioritized_coder_list( rebuild_IN = False )
            
        #-- END check to see if we need to build/rebuild --#
        
        return coder_list_OUT        
        
    #-- END method get_prioritized_coder_list() --#
        
        
    def set_coder_priority( self, coder_id_IN, priority_IN, *args, **kwargs ):
        
        '''
        Accepts a coder User ID, an integer priority for that coder.  Checks to
            make sure coder ID and priority are passed in.  If so, adds entry to
            map of coder IDs to priorities for the coder.
            
        Returns StatusContainer instance.
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
                coder_to_priority_dict = self.get_coder_id_to_priority_map()
                coder_to_priority_dict[ coder_id_IN ] = priority_IN
                            
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


    def set_index( self, value_IN ):
        
        '''
        Accepts an index value.  Stores it in nested instance variable.
            Returns stored value.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "set_index"
        
        # store the value
        self.m_index = value_IN
        
        # retrieve the value
        value_OUT = self.get_index()
        
        return value_OUT
    
    #-- END method set_index() --#


    def set_prioritized_coder_list( self, value_IN ):
        
        '''
        Accepts a prioritized list of coders.  Stores it in nested instance
            variable.  Returns stored value.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "set_prioritized_coder_list"
        
        # store the value
        self.m_prioritized_coder_list = value_IN
        
        # retrieve the value
        value_OUT = self.get_prioritized_coder_list()
        
        return value_OUT
    
    #-- END method set_prioritized_coder_list() --#
    
    
    def update_index_info_for_coder( self, coder_info_IN, *args, **kwargs ):
        
        '''
        Accepts a CoderIndexInfo instance.  Updates all the stuff in this
            instance to make sure the coder is added correctly, Including:
            - map coder's User ID to their User instance.
            - map coder's User ID to their priority.
            
        Preconditions: called as part of self.build_index_info(), so this does
            not call that.
        '''
        
        # return reference
        status_OUT = ""
        
        # declare variables
        coder_index_info = None
        coder_id_to_instance_dict = {}
        coder_user_id = -1
        coder_index = -1
        coder_user = None
        coder_priority = None
        is_priority_valid = False
        priority_status = None
        
        # get maps from instance
        coder_id_to_instance_dict = self.get_coder_id_to_instance_map()
        
        # got info?
        if ( coder_info_IN is not None ):
        
            # yes - get info on user from it.
            coder_index_info = coder_info_IN
        
            # init from info.
            coder_user_id = coder_index_info.get_coder_user_id()
            coder_user = coder_index_info.get_coder_user_instance()
            coder_index = coder_index_info.get_index()
            coder_priority = coder_index_info.get_priority()
            
            # got ID?
            if ( ( coder_user_id is not None ) and ( int( coder_user_id ) > 0 ) ):
            
                # got index?
                if ( ( coder_index is not None ) and ( int( coder_index ) > 0 ) ):
                
                    # Set all the things up internally.
                    coder_id_to_instance_dict[ coder_user_id ] = coder_user
                    
                    # set priority?
                    is_priority_valid = IntegerHelper.is_valid_integer( coder_priority, must_be_greater_than_IN = -1 )
                    if ( is_priority_valid == True ):
    
                        # priority value is valid - set priority.
                        priority_status = self.set_coder_priority( coder_user_id, coder_priority )
                        
                    else:
                    
                        # not valid.  Set coder_priority to None.
                        coder_priority = None
                        
                    #-- END check to see if priority value is valid --#
                                    
                    # rebuild other derived index information.
                    #self.build_index_info()
    
                else:
                
                    # no index - broken.
                    status_OUT = "No index - can't associate user with no index."
                
                #-- END check to see if index present. --#
            
            else:
            
                # no coder ID - broken.
                status_OUT = "No coder ID - can't associate user if no user."
            
            #-- END check to see if valid ID. --#
            
        else:
        
            # no info passed in, nothing to do.
            status_OUT = "No coder info passed in, nothing to do."
            
        #-- END check to see if coder info. --#

        return status_OUT        
        
    #-- END method update_index_info_for_user() --#


#-- END class IndexInfo --#
