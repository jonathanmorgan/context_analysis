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
from python_utilities.logging.logging_helper import LoggingHelper
from python_utilities.status.status_container import StatusContainer

# sourcenet imports

# sourcenet_analysis imports

#-------------------------------------------------------------------------------
# class definitions
#-------------------------------------------------------------------------------


class CoderIndexInfo( object ):
    
    
    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    


    # Logger name
    LOGGER_NAME = "sourcenet_analysis.reliability.coder_index_info"
        
    
    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __init__( self,
                  coder_user_id_IN = None,
                  coder_user_instance_IN = None,
                  index_IN = None,
                  priority_IN = None,
                  *args,
                  **kwargs ):
        
        # ! ==> call parent's __init__()
        super( CoderIndexInfo, self ).__init__()

        # ! ==> declare instance variables
        
        # coder info. init.
        self.m_coder_user_id = None
        self.m_coder_user_instance = None
        self.m_index = None
        self.m_priority = None        
        
        # set coder info.
        self.set_coder_user_id( coder_user_id_IN )
        self.set_coder_user_instance( coder_user_instance_IN )
        self.set_index( index_IN )
        self.set_priority( priority_IN )

        # exception helper
        self.m_exception_helper = ExceptionHelper()
        self.m_exception_helper.set_logger_name( self.LOGGER_NAME )
        self.m_exception_helper.logger_debug_flag = True
        self.m_exception_helper.logger_also_print_flag = False
        
    #-- END method __init__() --#
    
        
    def __str__( self ):
        
        # return reference
        string_OUT = ""
        
        # declare variables
        current_value = None
        current_value_label = None
        field_output_list = []
        
        current_value = self.get_coder_user_id()
        current_value_label = "user ID"
        if ( current_value is not None ):
        
            field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
            
        #-- END check to see if coder_user_id --#

        current_value = self.get_coder_user_instance()
        current_value_label = "user instance"
        if ( current_value is not None ):
        
            field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
            
        #-- END check to see if coder_user_id --#

        current_value = self.get_index()
        current_value_label = "index"
        if ( current_value is not None ):
        
            field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
            
        #-- END check to see if coder_user_id --#

        current_value = self.get_priority()
        current_value_label = "priority"
        if ( current_value is not None ):
        
            field_output_list.append( str( current_value_label ) + ": " + str( current_value ) )
            
        #-- END check to see if coder_user_id --#

        # convert output list to string
        string_OUT = ", ".join( field_output_list )
                
        return string_OUT
        
    #-- END method __str__() --#


    def get_coder_user_id( self ):
        
        '''
        Retrieves and returns the User ID from the current instance.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_coder_user_id"
        
        value_OUT = self.m_coder_user_id
        
        return value_OUT        
        
    #-- END method get_coder_user_id() --#
    
        
    def get_coder_user_instance( self ):
        
        '''
        Retrieves and returns the User instance from the current instance.  If
            None set yet, tries to get ID, then retrieve instance for current
            ID.
            
        Postconditions:  If no ID, returns None.  If no instance for ID, throws
            exception.  Other errors return None.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_coder_user_instance"
        coder_user_id = None
        coder_user_instance = None
        
        value_OUT = self.m_coder_user_instance
        
        # got anything?
        if ( value_OUT is None ):
        
            # No instance.  Got an id?
            coder_user_id = self.get_coder_user_id()
            if ( ( coder_user_id is not None ) and ( coder_user_id > 0 ) ):
            
                # We have an ID.  Look up the user instance.
                coder_user_instance = User.objects.get( id = coder_user_id )
                
                # store the result.
                self.set_coder_user_instance( coder_user_instance )
            
            #-- END check to see if we have a user ID. --#
            
            # try again.
            value_OUT = self.get_coder_user_instance()
        
        #-- END check to see if instance there already. --#
        
        return value_OUT        
        
    #-- END method get_coder_user_instance() --#
    
        
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
    
        
    def get_priority( self ):
        
        '''
        Retrieves and returns the priority from the current instance.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_priority"
        
        value_OUT = self.m_priority
        
        return value_OUT        
        
    #-- END method get_priority() --#
    
        
    def set_coder_user_id( self, value_IN ):
        
        '''
        Accepts a coder user id value.  Stores it in nested instance variable.
            Returns stored value.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "set_coder_user_id"
        temp_user_instance = None
        
        # store the value
        self.m_coder_user_id = value_IN
        
        # retrieve the value
        value_OUT = self.get_coder_user_id()
        
        # try to get User instance, which looks us User and loads it into
        #     this instance, as well.
        temp_user_instance = self.get_coder_user_instance()
        
        return value_OUT
    
    #-- END method set_coder_user_id() --#


    def set_coder_user_instance( self, value_IN ):
        
        '''
        Accepts a coder user instance.  Stores it in nested instance variable.
            Returns stored value.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "set_coder_user_instance"
        
        # store the value
        self.m_coder_user_instance = value_IN
        
        # retrieve the value
        value_OUT = self.get_coder_user_instance()
        
        return value_OUT
    
    #-- END method set_coder_user_instance() --#


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


    def set_priority( self, value_IN ):
        
        '''
        Accepts a priority value.  Stores it in nested instance variable.
            Returns stored value.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "set_priority"
        
        # store the value
        self.m_priority = value_IN
        
        # retrieve the value
        value_OUT = self.get_priority()
        
        return value_OUT
    
    #-- END method set_priority() --#


#-- END class ReliabilityNamesBuilder --#
