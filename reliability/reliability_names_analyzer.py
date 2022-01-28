# start to support python 3:
from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context_analysis.

context_analysis is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context_analysis is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context_analysis. If not, see http://www.gnu.org/licenses/.
'''

#==============================================================================#
# ! imports
#==============================================================================#

# grouped by functional area, then alphabetical order by package, then
#     alphabetical order by name of thing being imported.

# try to get django imports.
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist

# python package imports
import six

# stats and analysis
import numpy
import pandas
import scipy.stats.stats

# database - postgresql and sqlalchemy for pandas database connection
import sqlalchemy
import psycopg2.extensions

# integrate with R
import pyRserve

# import basic django configuration application.
from django_config.models import Config_Property

'''   
Example of getting properties from django_config:

# get settings from django_config.
email_smtp_server_host = Config_Property.get_property_value( Issue.CONFIG_APPLICATION, Issue.CONFIG_PROP_SMTP_HOST )
email_smtp_server_port = Config_Property.get_property_int_value( Issue.CONFIG_APPLICATION, Issue.CONFIG_PROP_SMTP_PORT, default_IN = -1 )
email_smtp_server_username = Config_Property.get_property_value( Issue.CONFIG_APPLICATION, Issue.CONFIG_PROP_SMTP_USERNAME, default_IN = "" )
email_smtp_server_password = Config_Property.get_property_value( Issue.CONFIG_APPLICATION, Issue.CONFIG_PROP_SMTP_PASSWORD, default_IN = "" )
use_SSL = Config_Property.get_property_boolean_value( Issue.CONFIG_APPLICATION, Issue.CONFIG_PROP_SMTP_USE_SSL, default_IN = False )
email_from_address = Config_Property.get_property_value( Issue.CONFIG_APPLICATION, Issue.CONFIG_PROP_FROM_EMAIL )
'''

# python_utilities
from python_utilities.analysis.statistics.stats_helper import StatsHelper
from python_utilities.exceptions.exception_helper import ExceptionHelper
from python_utilities.logging.logging_helper import LoggingHelper
from python_utilities.R.rserve_helper import RserveHelper

# context_text imports
from context_text.article_coding.manual_coding.manual_article_coder import ManualArticleCoder
from context_text.shared.context_text_base import ContextTextBase

# context_analysis imports
from context_analysis.models import Reliability_Names
from context_analysis.models import Reliability_Names_Results


#-------------------------------------------------------------------------------
# ! class definitions
#-------------------------------------------------------------------------------


class ReliabilityNamesAnalyzer( RserveHelper ):
    
    
    #---------------------------------------------------------------------------
    # constants-ish
    #---------------------------------------------------------------------------


    # logging
    LOGGER_NAME = "python_utilities.R.rserve_helper.RserveHelper"

    # column names in Reliability_Names table
    COLUMN_NAME_LABEL = Reliability_Names.FIELD_NAME_LABEL
    COLUMN_NAME_SUFFIX_CODER_ID = "_" + Reliability_Names.FIELD_NAME_SUFFIX_CODER_ID
    COLUMN_NAME_SUFFIX_DETECTED = "_" + Reliability_Names.FIELD_NAME_SUFFIX_DETECTED
    COLUMN_NAME_SUFFIX_PERSON_ID = "_" + Reliability_Names.FIELD_NAME_SUFFIX_PERSON_ID
    COLUMN_NAME_SUFFIX_PERSON_TYPE_INT = "_" + Reliability_Names.FIELD_NAME_SUFFIX_PERSON_TYPE_INT
    COLUMN_NAME_SUFFIX_FIRST_QUOTE_GRAF = "_" + Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF
    COLUMN_NAME_SUFFIX_FIRST_QUOTE_INDEX = "_" + Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX
    COLUMN_NAME_SUFFIX_ORGANIZATION_HASH = "_" + Reliability_Names.FIELD_NAME_SUFFIX_ORGANIZATION_HASH
    COLUMN_NAME_PREFIX_CODER = Reliability_Names.FIELD_NAME_PREFIX_CODER
    
    # column names in Reliability_Names_Results table
    RESULTS_COLUMN_NAME_DETECT = "detect"
    RESULTS_COLUMN_NAME_LOOKUP = "lookup"
    RESULTS_COLUMN_NAME_LOOKUP_NON_ZERO = "lookup_non_zero"
    RESULTS_COLUMN_NAME_TYPE = "type"
    RESULTS_COLUMN_NAME_TYPE_NON_ZERO = "type_non_zero"
    RESULTS_COLUMN_NAME_FIRST_QUOTE_GRAF = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF
    RESULTS_COLUMN_NAME_FIRST_QUOTE_INDEX = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX
    RESULTS_COLUMN_NAME_ORGANIZATION_HASH = Reliability_Names.FIELD_NAME_SUFFIX_ORGANIZATION_HASH
    RESULTS_COLUMN_NAME_SUFFIX_PERCENT = Reliability_Names_Results.SUFFIX_PERCENT  # "_percent"
    RESULTS_COLUMN_NAME_SUFFIX_ALPHA = Reliability_Names_Results.SUFFIX_ALPHA  # "_alpha"
    RESULTS_COLUMN_NAME_SUFFIX_PI = Reliability_Names_Results.SUFFIX_PI  # "_pi"
    RESULTS_COLUMN_NAME_SUFFIX_COUNT = Reliability_Names_Results.SUFFIX_COUNT  # "_count"
    RESULTS_COLUMN_NAME_PREFIX_AUTHOR = Reliability_Names_Results.PREFIX_AUTHOR  # "author_"
    RESULTS_COLUMN_NAME_PREFIX_SUBJECT = Reliability_Names_Results.PREFIX_SUBJECT  # "subject_"
    RESULTS_COLUMN_NAME_PREFIX_LIST = [ RESULTS_COLUMN_NAME_PREFIX_AUTHOR, RESULTS_COLUMN_NAME_PREFIX_SUBJECT ]
    
    # names of things in self.columns_to_compare (column info).
    CTC_COLUMN_NAME_SUFFIX = "column_name_suffix"
    CTC_COLUMN_MEASUREMENT_LEVEL = "measurement_level"
    CTC_COLUMN_VALUE_COUNT = "value_count"
    CTC_RESULT_COLUMN_NAME = "result_column_name"
    CTC_COLUMN_INTEGER_BASE = "integer_base"
    CTC_COLUMN_DATA_TYPE = "data_type"
    CTC_TRUNCATE_TO_LENGTH = "truncate_to_length"  # desired size of truncate result.
    CTC_TRUNCATE_FROM = "truncate_from"  # truncate from right or left side of values.
    
    # person types
    PERSON_TYPE_AUTHOR = RESULTS_COLUMN_NAME_PREFIX_AUTHOR
    PERSON_TYPE_SUBJECT = RESULTS_COLUMN_NAME_PREFIX_SUBJECT
    PERSON_TYPE_LIST = [ PERSON_TYPE_AUTHOR, PERSON_TYPE_SUBJECT ]

    # measurement levels
    MEASUREMENT_LEVEL_NOMINAL = StatsHelper.MEASUREMENT_LEVEL_NOMINAL
    MEASUREMENT_LEVEL_ORDINAL = StatsHelper.MEASUREMENT_LEVEL_ORDINAL
    MEASUREMENT_LEVEL_INTERVAL = StatsHelper.MEASUREMENT_LEVEL_INTERVAL
    MEASUREMENT_LEVEL_RATIO = StatsHelper.MEASUREMENT_LEVEL_RATIO
    
    # data types
    DATA_TYPE_INTEGER = "integer"
    DATA_TYPE_DECIMAL = "decimal"
    DATA_TYPE_HEX_HASH = "hex_hash"
    DATA_TYPE_LIST = [ DATA_TYPE_INTEGER, DATA_TYPE_DECIMAL, DATA_TYPE_HEX_HASH ]
    
    # truncation directions:
    TRUNCATE_FROM_LEFT = "left"
    TRUNCATE_FROM_RIGHT = "right"
    TRUNCATE_FROM_LIST = [ TRUNCATE_FROM_LEFT, TRUNCATE_FROM_RIGHT ]

    # pre-built column info
    
    # Reliability_Names.coderX_detected
    COLUMN_INFO_DETECTED = {
        CTC_COLUMN_NAME_SUFFIX : COLUMN_NAME_SUFFIX_DETECTED,
        CTC_COLUMN_MEASUREMENT_LEVEL : MEASUREMENT_LEVEL_NOMINAL,
        CTC_COLUMN_VALUE_COUNT : 2,
        CTC_RESULT_COLUMN_NAME : RESULTS_COLUMN_NAME_DETECT,
        CTC_COLUMN_INTEGER_BASE : 10,
        CTC_COLUMN_DATA_TYPE : DATA_TYPE_INTEGER
    }    

    # Reliability_Names.coderX_person_id (0s included)
    COLUMN_INFO_PERSON_ID_LOOKUP = {
        CTC_COLUMN_NAME_SUFFIX : COLUMN_NAME_SUFFIX_PERSON_ID,
        CTC_COLUMN_MEASUREMENT_LEVEL : MEASUREMENT_LEVEL_NOMINAL,
        CTC_COLUMN_VALUE_COUNT : -1,
        CTC_RESULT_COLUMN_NAME : RESULTS_COLUMN_NAME_LOOKUP,
        CTC_COLUMN_INTEGER_BASE : 10,
        CTC_COLUMN_DATA_TYPE : DATA_TYPE_INTEGER
    }
    
    # Reliability_Names.coderX_person_id (no 0s)
    COLUMN_INFO_PERSON_ID_LOOKUP_NON_ZERO = {
        CTC_COLUMN_NAME_SUFFIX : COLUMN_NAME_SUFFIX_PERSON_ID,
        CTC_COLUMN_MEASUREMENT_LEVEL : MEASUREMENT_LEVEL_NOMINAL,
        CTC_COLUMN_VALUE_COUNT : -1,
        CTC_RESULT_COLUMN_NAME : RESULTS_COLUMN_NAME_LOOKUP_NON_ZERO,
        CTC_COLUMN_INTEGER_BASE : 10,
        CTC_COLUMN_DATA_TYPE : DATA_TYPE_INTEGER
    }
    
    # Reliability_Names.coderX_person_type_int (0s included)
    COLUMN_INFO_PERSON_TYPE_INT = {
        CTC_COLUMN_NAME_SUFFIX : COLUMN_NAME_SUFFIX_PERSON_TYPE_INT,
        CTC_COLUMN_MEASUREMENT_LEVEL : MEASUREMENT_LEVEL_NOMINAL,
        CTC_COLUMN_VALUE_COUNT : 4,
        CTC_RESULT_COLUMN_NAME : RESULTS_COLUMN_NAME_TYPE,
        CTC_COLUMN_INTEGER_BASE : 10,
        CTC_COLUMN_DATA_TYPE : DATA_TYPE_INTEGER
    }
    
    # Reliability_Names.coderX_person_type_int (no 0s)
    COLUMN_INFO_PERSON_TYPE_INT_NON_ZERO = {
        CTC_COLUMN_NAME_SUFFIX : COLUMN_NAME_SUFFIX_PERSON_TYPE_INT,
        CTC_COLUMN_MEASUREMENT_LEVEL : MEASUREMENT_LEVEL_NOMINAL,
        CTC_COLUMN_VALUE_COUNT : 3,
        CTC_RESULT_COLUMN_NAME : RESULTS_COLUMN_NAME_TYPE_NON_ZERO,
        CTC_COLUMN_INTEGER_BASE : 10,
        CTC_COLUMN_DATA_TYPE : DATA_TYPE_INTEGER
    }
    
    # Reliability_Names.coderX_first_quote_graf
    COLUMN_INFO_FIRST_QUOTE_GRAF = {
        CTC_COLUMN_NAME_SUFFIX : COLUMN_NAME_SUFFIX_FIRST_QUOTE_GRAF,
        CTC_COLUMN_MEASUREMENT_LEVEL : MEASUREMENT_LEVEL_NOMINAL,
        CTC_COLUMN_VALUE_COUNT : -1,
        CTC_RESULT_COLUMN_NAME : RESULTS_COLUMN_NAME_FIRST_QUOTE_GRAF,
        CTC_COLUMN_INTEGER_BASE : 10,
        CTC_COLUMN_DATA_TYPE : DATA_TYPE_INTEGER
    }
    
    # Reliability_Names.coder1_first_quote_index
    COLUMN_INFO_FIRST_QUOTE_INDEX = {
        CTC_COLUMN_NAME_SUFFIX : COLUMN_NAME_SUFFIX_FIRST_QUOTE_INDEX,
        CTC_COLUMN_MEASUREMENT_LEVEL : MEASUREMENT_LEVEL_NOMINAL,
        CTC_COLUMN_VALUE_COUNT : -1,
        CTC_RESULT_COLUMN_NAME : RESULTS_COLUMN_NAME_FIRST_QUOTE_INDEX,
        CTC_COLUMN_INTEGER_BASE : 10,
        CTC_COLUMN_DATA_TYPE : DATA_TYPE_INTEGER
    }
    
    # Reliability_Names.coder1_organization_hash
    COLUMN_INFO_ORGANIZATION_HASH = {
        CTC_COLUMN_NAME_SUFFIX : COLUMN_NAME_SUFFIX_ORGANIZATION_HASH,
        CTC_COLUMN_MEASUREMENT_LEVEL : MEASUREMENT_LEVEL_NOMINAL,
        CTC_COLUMN_VALUE_COUNT : -1,
        CTC_RESULT_COLUMN_NAME : RESULTS_COLUMN_NAME_ORGANIZATION_HASH,
        CTC_COLUMN_INTEGER_BASE : 16,
        CTC_COLUMN_DATA_TYPE : DATA_TYPE_HEX_HASH,
        CTC_TRUNCATE_TO_LENGTH : 7, # R has a limit on integers - must be under ( 2 ^ 31 ) - 1
        CTC_TRUNCATE_FROM : TRUNCATE_FROM_LEFT
    }
    
    DEFAULT_COLUMN_INFO_LIST = [ COLUMN_INFO_DETECTED, COLUMN_INFO_PERSON_ID_LOOKUP, COLUMN_INFO_PERSON_TYPE_INT, COLUMN_INFO_FIRST_QUOTE_GRAF, COLUMN_INFO_FIRST_QUOTE_INDEX, COLUMN_INFO_ORGANIZATION_HASH ]

    
    #---------------------------------------------------------------------------
    # instance methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init__()
        super( ReliabilityNamesAnalyzer, self ).__init__()
        
        # logging
        self.set_logger_name( self.LOGGER_NAME )
        self.logger_debug_flag = True
        
        # declare instance variables
        self.coder_index_to_instance_map = {}        
        self.coder_index_to_id_map = {}
        
        # variable to hold desired automated coder type
        self.limit_to_automated_coder_type = ""
        
        # Rserve host information (from RserveHelper)
        # self.rserve_host = ""
        # self.rserve_port = -1
        
        # variables for configuring analysis
        self.indices_to_compare = -1
        self.columns_to_compare = {}
        
        # database credentials - try reading from config.
        self.db_username = ""
        self.db_password = ""
        self.db_host = ""
        self.db_port = -1
        self.db_name = ""
        
        # database credentials - try reading from config.
        self.db_username = Config_Property.get_property_value(
            ContextTextBase.DJANGO_CONFIG_APPLICATION_CONTEXT_TEXT_DB_ADMIN,
            ContextTextBase.DJANGO_CONFIG_PROP_DB_USERNAME,
            default_IN = None )
        self.db_password = Config_Property.get_property_value(
            ContextTextBase.DJANGO_CONFIG_APPLICATION_CONTEXT_TEXT_DB_ADMIN,
            ContextTextBase.DJANGO_CONFIG_PROP_DB_PASSWORD,
            default_IN = None )
        self.db_host = Config_Property.get_property_value(
            ContextTextBase.DJANGO_CONFIG_APPLICATION_CONTEXT_TEXT_DB_ADMIN,
            ContextTextBase.DJANGO_CONFIG_PROP_DB_HOST,
            default_IN = None )
        self.db_port = Config_Property.get_property_int_value(
            ContextTextBase.DJANGO_CONFIG_APPLICATION_CONTEXT_TEXT_DB_ADMIN,
            ContextTextBase.DJANGO_CONFIG_PROP_DB_PORT,
            default_IN = -1 )
        self.db_name = Config_Property.get_property_value(
            ContextTextBase.DJANGO_CONFIG_APPLICATION_CONTEXT_TEXT_DB_ADMIN,
            ContextTextBase.DJANGO_CONFIG_PROP_DB_NAME,
            default_IN = None )
        
    #-- END method __init__() --#
    

    def analyze_column( self,
                        index_1_IN,
                        index_2_IN,
                        person_df_IN,
                        column_info_IN,
                        results_instance_IN,
                        column_name_prefix_IN ):
        
        # return reference
        instance_OUT = None
        
        # declare variables
        me = "ReliabilityNamesAnalyzer.analyze_column"
        my_logger = None
        debug_message = ""
        current_index = -1
        comparison_index = -1
        person_df = None
        current_column_info = {}
        column_name_prefix = ""
        current_column_name_suffix = ""
        current_column_level = ""
        current_column_value_count = -1
        current_column_result_name = ""
        current_column_integer_base = -1
        current_column_data_type = ""
        current_column_truncate_to_length = ""
        current_column_truncate_from = ""
        chop_from = ""
        chop_result_size = -1
        chop_lambda = None
        compare_column_name_1 = ""
        compare_column_name_2 = ""
        compare_values_1 = ""
        compare_values_2 = ""
        result_column_prefix = ""
        result_column_name = ""
        percentage_agreement = -1
        value_df = None
        value_array = None
        kripp_alpha_result = None
        kripp_alpha = -1
        my_indices_to_compare = -1
        potter_pi = -1
        
        # get logger
        my_logger = self.get_logger()
        
        # get Rserve connection
        r_conn = self.get_rserve_connection()
        
        # got index 1?
        if ( ( index_1_IN is not None ) and ( index_1_IN != "" ) and ( index_1_IN > 0 ) ):
        
            # yes.  Use it.
            current_index = index_1_IN
            
            # how about index 2?
            if ( ( index_2_IN is not None ) and ( index_2_IN != "" ) and ( index_2_IN > 0 ) ):
            
                # yes, got both indices.
                comparison_index = index_2_IN
                
                # got Reliability_Name data frame?
                if ( person_df_IN is not None ):
                
                    # yes.  Use it.
                    person_df = person_df_IN
                    
                    # Now, got column info?
                    if ( ( column_info_IN is not None ) and ( len( column_info_IN ) > 0 ) ):
                    
                        # yes.  Use it.
                        current_column_info = column_info_IN
                        
                        # do we have a results instance?
                        if ( results_instance_IN is not None ):
                        
                            # we do.  Use it.
                            instance_OUT = results_instance_IN
                            
                            # and, finally, do we have column name prefix?
                            if ( ( column_name_prefix_IN is not None )
                                and ( column_name_prefix_IN != "" )
                                and ( column_name_prefix_IN in self.RESULTS_COLUMN_NAME_PREFIX_LIST ) ):
                            
                                # yes.  good to go (finally).
                                column_name_prefix = column_name_prefix_IN
                            
                                # unpack column info
                                current_column_name_suffix = current_column_info.get( self.CTC_COLUMN_NAME_SUFFIX, None )
                                current_column_level = current_column_info.get( self.CTC_COLUMN_MEASUREMENT_LEVEL, None )
                                current_column_value_count = current_column_info.get( self.CTC_COLUMN_VALUE_COUNT, None )
                                current_column_result_name = current_column_info.get( self.CTC_RESULT_COLUMN_NAME, None )
                                current_column_integer_base = current_column_info.get( self.CTC_COLUMN_INTEGER_BASE, None )
                                current_column_data_type = current_column_info.get( self.CTC_COLUMN_DATA_TYPE, None )
                                current_column_truncate_to_length = current_column_info.get( self.CTC_TRUNCATE_TO_LENGTH, None )
                                current_column_truncate_from = current_column_info.get( self.CTC_TRUNCATE_FROM, None )

                                debug_message = "====> current_column_name_suffix = " + str( current_column_name_suffix )
                                print( debug_message )
                                self.output_debug_message( debug_message, method_IN = me )

                                debug_message = "====> current_column_result_name = " + str( current_column_result_name )
                                print( debug_message )
                                self.output_debug_message( debug_message, method_IN = me )

                                # build result column name prefix
                                result_column_prefix = column_name_prefix_IN + current_column_result_name
                
                                # build comparison column names from indices and column
                                #     name.
                                compare_column_name_1 = self.COLUMN_NAME_PREFIX_CODER + str( current_index ) + current_column_name_suffix
                                compare_column_name_2 = self.COLUMN_NAME_PREFIX_CODER + str( comparison_index ) + current_column_name_suffix
                                
                                debug_message = "======> compare_column_name_1 = " + str( compare_column_name_1 )
                                print( debug_message )
                                self.output_debug_message( debug_message, method_IN = me )

                                debug_message = "======> compare_column_name_2 = " + str( compare_column_name_2 )
                                print( debug_message )
                                self.output_debug_message( debug_message, method_IN = me )
                
                                # retrieve numpy arrays of column values.
                                compare_values_1 = person_df[ compare_column_name_1 ]
                                compare_values_2 = person_df[ compare_column_name_2 ]
                                
                                debug_message = "========> compare_values_1 ( type = " + str( type ( compare_values_1 ) ) + " ) = " + str( compare_values_1 )
                                self.output_debug_message( debug_message, method_IN = me )
                                
                                debug_message = "========> compare_values_2 ( type = " + str( type ( compare_values_2 ) ) + " ) = " + str( compare_values_2 )
                                self.output_debug_message( debug_message, method_IN = me )
                                
                                # check if there is a column data type.
                                if ( ( current_column_data_type is not None )
                                    and ( current_column_data_type != "" )
                                    and ( current_column_data_type in self.DATA_TYPE_LIST ) ):
                                    
                                    # got a hexadecimal hash value we need to
                                    #     convert to base 10 integer?
                                    if ( current_column_data_type == self.DATA_TYPE_HEX_HASH ):
                                    
                                        # convert any None to "-1".
                                        #compare_values_1.fillna( "-1" )
                                        compare_values_1[ compare_values_1.isnull() ] = "-1"
                                        #compare_values_2.fillna( "-1" )
                                        compare_values_2[ compare_values_2.isnull() ] = "-1"

                                        # truncate?
                                        if ( ( current_column_truncate_to_length is not None )
                                            and ( int( current_column_truncate_to_length ) > 0 ) ):
                                            
                                            # chop from left or right?
                                            if ( current_column_truncate_from == self.TRUNCATE_FROM_LEFT ):
                                            
                                                # chop from left side.
                                                chop_from = self.TRUNCATE_FROM_LEFT
                                                chop_result_size = -1 * current_column_truncate_to_length
                                                chop_lambda = lambda x: x[ chop_result_size : ]

                                            elif ( current_column_truncate_from == self.TRUNCATE_FROM_RIGHT ):
                                            
                                                # chop from the right.
                                                chop_from = self.TRUNCATE_FROM_RIGHT
                                                chop_result_size = current_column_truncate_to_length
                                                chop_lambda = lambda x: x[ : chop_result_size ]
                                            
                                            else:
                                            
                                                # chop from left side.
                                                chop_from = self.TRUNCATE_FROM_LEFT
                                                chop_result_size = -1 * current_column_truncate_to_length
                                                chop_lambda = lambda x: x[ chop_result_size : ]
                                                
                                            #-- END CHECK To see what end of string we truncate from. --#
                                            
                                            compare_values_1 = compare_values_1.apply( chop_lambda )
                                            compare_values_2 = compare_values_2.apply( chop_lambda )

                                        #-- END check to see if we truncate. --#
                                        
                                        # convert to base 10 integer.
                                        compare_values_1 = compare_values_1.apply( int, args = ( 16, ) )
                                        # compare_values_1 = compare_values_1.astype( numpy.uint64 ) # R doesn't know what data type uint64 corresponds to.
                                        compare_values_1 = compare_values_1.astype( numpy.int64 )
                                        compare_values_2 = compare_values_2.apply( int, args = ( 16, ) )
                                        compare_values_2 = compare_values_2.astype( numpy.int64 )

                                        debug_message = "========> (in hex hash type) compare_values_1 ( type = " + str( type ( compare_values_1 ) ) + " ) = " + str( compare_values_1 )
                                        self.output_debug_message( debug_message, method_IN = me )

                                        debug_message = "========> (in hex hash type) compare_values_2 ( type = " + str( type ( compare_values_2 ) ) + " ) = " + str( compare_values_2 )
                                        self.output_debug_message( debug_message, method_IN = me )
                                        
                                    #-- END check to see if hex hash type. --#
                                    
                                #-- END check to see if data type. --#
                                    
                                # for each type, get columns/numpy arrays for fields we want to check, then:
                
                                # ==> Pearson correlation coefficient
                                #correlation_result = scipy.stats.stats.pearsonr( compare_values_1, compare_values_2 )
                                #print( "========> correlation = " + str( correlation_result ) )
                                
                                # ! ==> percent agreement
                                percentage_agreement = StatsHelper.percentage_agreement( compare_values_1, compare_values_2 )
                                debug_message = "========> percentage_agreement = " + str( percentage_agreement )
                                print( debug_message )
                                self.output_debug_message( debug_message, method_IN = me )
                                
                                # add to results
                                result_column_name = result_column_prefix + self.RESULTS_COLUMN_NAME_SUFFIX_PERCENT
                                setattr( instance_OUT, result_column_name, percentage_agreement )
                                
                                # ! ==> krippendorff's alpha at appropriate measurement level.
                                # - first, try in R.
                                
                                # combine values into a dataframe
                                value_df = pandas.DataFrame()
                                value_df[ "value_list_1" ] = compare_values_1
                                value_df[ "value_list_2" ] = compare_values_2
                                
                                # convert to numpy array
                                value_array_tall = value_df.values
                                
                                # transpose columns to rows (because the alpha function
                                #     wants the data this way).
                                value_array_wide = numpy.transpose( value_array_tall )
                                
                                # R - store values in R.
                                r_conn.r.valueArrayWide = value_array_wide
                                
                                # R - call irr::kripp.alpha()
                                kripp_alpha_result = r_conn.eval( "irr::kripp.alpha( valueArrayWide, method = \"" + current_column_level + "\" )" )
                                #print( str( kripp_alpha_result ) )
                                
                                # get alpha value from result.
                                R_kripp_alpha = kripp_alpha_result[ str( "value" ) ]

                                debug_message = "========> R irr::kripp.alpha = " + str( R_kripp_alpha )
                                print( debug_message )
                                self.output_debug_message( debug_message, method_IN = me )
                                
                                # add to results
                                result_column_name = result_column_prefix + self.RESULTS_COLUMN_NAME_SUFFIX_ALPHA
                                setattr( instance_OUT, result_column_name, R_kripp_alpha )
                                
                                # ! ==> if necessary, modified Scott's Pi.
                                # see if there is a count of values.
                                if ( ( current_column_value_count is not None ) and ( current_column_value_count != "" ) and ( current_column_value_count > 0 ) ):
                                
                                    # got a value count.  Make sure we are nominal, as well.
                                    if ( ( current_column_level is not None ) and ( current_column_level == self.MEASUREMENT_LEVEL_NOMINAL ) ):
                                    
                                        # and we are nominal.  Potter's Pi!
                                        my_indices_to_compare = self.indices_to_compare
                                        potter_pi = StatsHelper.potter_pi( compare_values_1, compare_values_2, coder_count_IN = int( my_indices_to_compare ), option_count_IN = int( current_column_value_count ) )

                                        debug_message = "========> Potter's Pi = " + str( potter_pi )
                                        print( debug_message )
                                        self.output_debug_message( debug_message, method_IN = me )
                                        
                                        # add to results
                                        result_column_name = result_column_prefix + self.RESULTS_COLUMN_NAME_SUFFIX_PI
                                        setattr( instance_OUT, result_column_name, potter_pi )
                                
                                    #-- END check to see if nominal variable --#
                                    
                                #-- END check to see if value count is non-zero. --#
                            
                            else:
                            
                                # no column name prefix passed in.
                                debug_message = "No column name prefix passed in, won't be able to place results in correct columns in results table."
                                self.output_debug_message( debug_message, method_IN = me )
                                instance_OUT = None
                            
                            #-- END check to see if results instance passed in. --#
                            
                        else:
                        
                            # no results instance passed in.
                            debug_message = "No results instance passed in, no place to store results."
                            self.output_debug_message( debug_message, method_IN = me )
                            instance_OUT = None
                        
                        #-- END check to see if results instance passed in. --#
                        
                    else:
                    
                        # no column info passed in.
                        debug_message = "No column info passed in, no idea what column we want to analyze."
                        self.output_debug_message( debug_message, method_IN = me )
                        instance_OUT = None
                            
                    #-- END check to see if column info passed in. --#
    
                else:
                
                    # no data frame passed in.
                    debug_message = "No data frame passed in, no data to compare."
                    self.output_debug_message( debug_message, method_IN = me )
                    instance_OUT = None
                        
                #-- END check to see if column info passed in. --#

            else:
            
                # no index_2_IN.
                debug_message = "No 2nd index value passed in, nothing to compare."
                self.output_debug_message( debug_message, method_IN = me )
                instance_OUT = None
            
            #-- END check to see if results instance passed in. --#
            
        else:
        
            # no index_1_IN.
            debug_message = "No 1st index value passed in, nothing to compare."
            self.output_debug_message( debug_message, method_IN = me )
            instance_OUT = None
                
        #-- END check to see if column info passed in. --#

        return instance_OUT

    #-- END method analyze_column() --#


    def analyze_person_coding( self, index_1_IN, index_2_IN, person_df_IN, person_type_IN, results_instance_IN ):
    
        '''
        Accepts 2 indices, a data frame of Reliability_Name rows, the type of
            the person coding we are assessing ( "subject" or "author" ) and an
            instance of Reliability_Names_Results to store results in.  Assesses
            reliability for person, updating the results instance with the
            results.  Returns the results instance.
        '''
    
        # return reference
        instance_OUT = None
        
        # declare variables
        me = ""
        my_logger = None
        columns_to_compare = None
        current_column_info = None
        person_count = -1
        column_name_person_count = ""
        column_name_prefix = ""
        person_df_lookup = None
        lookup_count = -1
        column_name_lookup_count = ""
        person_type_no_zeros_df = None
        person_type_no_zeros_count = -1
        column_name_person_type_no_zeros_count = ""

        # get logger
        my_logger = self.get_logger()
        
        # configure processing
        columns_to_compare = self.DEFAULT_COLUMN_INFO_LIST
        
        # got index 1?
        if ( ( index_1_IN is not None ) and ( index_1_IN != "" ) and ( index_1_IN > 0 ) ):
        
            # how about index 2?
            if ( ( index_2_IN is not None ) and ( index_2_IN != "" ) and ( index_2_IN > 0 ) ):
            
                # got Reliability_Name data frame?
                if ( person_df_IN is not None ):
                
                    # Now, got person_type?
                    if ( ( person_type_IN is not None ) and ( person_type_IN != "" ) and ( person_type_IN in self.PERSON_TYPE_LIST ) ):
                    
                        # do we have a results instance?
                        if ( results_instance_IN is not None ):
                        
                            # we do.  Use it.
                            instance_OUT = results_instance_IN
                            
                            # column name prefix = person type
                            column_name_prefix = person_type_IN
                            
                            # first, get count of people in the data frame, and
                            #     store it in results (author_count or
                            #     subject_count).
                            person_count = len( person_df_IN )
                            column_name_person_count = column_name_prefix + "count"
                            setattr( instance_OUT, column_name_person_count, person_count )
                            
                            # loop over columns_to_compare
                            for current_column_info in columns_to_compare:
                            
                                # call analyze_column()
                                instance_OUT = self.analyze_column( index_1_IN,
                                                                    index_2_IN,
                                                                    person_df_IN,
                                                                    current_column_info,
                                                                    instance_OUT,
                                                                    column_name_prefix )
            
                            #-- END loop over column info --#
                            
                            # ! calculate agreement on person_id and person_type
                            #     only where the two coders have a non-zero
                            #     value.  If either has a 0, remove the row.
                            
                            #--------------------------------------------------#
                            # ! ==> Person lookup (no 0s)
                            #--------------------------------------------------#
                            
                            # make names of person ID columns for indices we are
                            #     looking at now.
                            column_name_person_id_1 = self.COLUMN_NAME_PREFIX_CODER + str( index_1_IN ) + self.COLUMN_NAME_SUFFIX_PERSON_ID
                            column_name_person_id_2 = self.COLUMN_NAME_PREFIX_CODER + str( index_2_IN ) + self.COLUMN_NAME_SUFFIX_PERSON_ID

                            # make new data frame with only rows where both are
                            #    greater than 0 (so where both detected the
                            #    person and attempted a database lookup).
                            person_df_lookup = person_df_IN[ ( person_df_IN[ column_name_person_id_1 ] > 0 ) & ( person_df_IN[ column_name_person_id_2 ] > 0 ) ]
                            
                            #temp_df = person_df_lookup[ person_df_lookup[ column_name_person_id_1 ] != person_df_lookup[ column_name_person_id_2 ] ]
                            #temp_df = temp_df[ [ "id", column_name_person_id_1, column_name_person_id_2 ] ]
                            #print( temp_df )

                            # then, call analyze_column() with column_info for
                            #     person lookup, rather than combined.
                            instance_OUT = self.analyze_column( index_1_IN,
                                                                index_2_IN,
                                                                person_df_lookup,
                                                                self.COLUMN_INFO_PERSON_ID_LOOKUP_NON_ZERO,
                                                                instance_OUT,
                                                                column_name_prefix )
                                                                
                            # finally, get count of records in lookup and store
                            #     in results (author_lookup_count or
                            #     subject_lookup_count).
                            lookup_count = len( person_df_lookup )
                            column_name_lookup_count = person_type_IN + self.RESULTS_COLUMN_NAME_LOOKUP_NON_ZERO + self.RESULTS_COLUMN_NAME_SUFFIX_COUNT
                            setattr( instance_OUT, column_name_lookup_count, lookup_count )

                            #--------------------------------------------------#
                            # ! ==> Person type (no 0s)
                            #--------------------------------------------------#
                            
                            # make names of person ID columns for indices we are
                            #     looking at now.
                            column_name_person_id_1 = self.COLUMN_NAME_PREFIX_CODER + str( index_1_IN ) + self.COLUMN_NAME_SUFFIX_PERSON_TYPE_INT
                            column_name_person_id_2 = self.COLUMN_NAME_PREFIX_CODER + str( index_2_IN ) + self.COLUMN_NAME_SUFFIX_PERSON_TYPE_INT

                            # make new data frame with only rows where both are
                            #    greater than 0 (so where both detected the
                            #    person and attempted a database lookup).
                            person_type_no_zeros_df = person_df_IN[ ( person_df_IN[ column_name_person_id_1 ] > 0 ) & ( person_df_IN[ column_name_person_id_2 ] > 0 ) ]
    
                            # then, call analyze_column() with column_info for
                            #     person type, rather than combined.
                            instance_OUT = self.analyze_column( index_1_IN,
                                                                index_2_IN,
                                                                person_type_no_zeros_df,
                                                                self.COLUMN_INFO_PERSON_TYPE_INT_NON_ZERO,
                                                                instance_OUT,
                                                                column_name_prefix )
                                                                
                            # finally, get count of records in lookup and store
                            #     in results (author_lookup_count or
                            #     subject_lookup_count).
                            person_type_no_zeros_count = len( person_df_lookup )
                            column_name_person_type_no_zeros_count = person_type_IN + self.RESULTS_COLUMN_NAME_TYPE_NON_ZERO + self.RESULTS_COLUMN_NAME_SUFFIX_COUNT
                            setattr( instance_OUT, column_name_person_type_no_zeros_count, person_type_no_zeros_count )

                        else:
                        
                            # no results instance passed in.
                            self.output_debug_message( "No results instance passed in, no place to store results.", method_IN = me )
                            instance_OUT = None
                        
                        #-- END check to see if results instance passed in. --#
                    
                    else:
                    
                        # no person type passed in.
                        self.output_debug_message( "Unknown or no person type passed in ( \"" + str( person_type_IN ) + "\" ), no idea which columns we want to analyze ( valid = " + str( self.PERSON_TYPE_LIST ) + " ).", method_IN = me )
                        instance_OUT = None
                            
                    #-- END check to see if column info passed in. --#
    
                else:
                
                    # no data frame passed in.
                    self.output_debug_message( "No data frame passed in, no data to compare.", method_IN = me )
                    instance_OUT = None
                        
                #-- END check to see if column info passed in. --#

            else:
            
                # no index_2_IN.
                self.output_debug_message( "No 2nd index value passed in, nothing to compare.", method_IN = me )
                instance_OUT = None
            
            #-- END check to see if results instance passed in. --#
            
        else:
        
            # no index_1_IN.
            self.output_debug_message( "No 1st index value passed in, nothing to compare.", method_IN = me )
            instance_OUT = None
                
        #-- END check to see if column info passed in. --#

        return instance_OUT
        
    #-- END method analyze_person_coding() --#
    
        
    def analyze_reliability_names( self, label_IN, indices_to_compare_IN = -1 ):
        
        '''
        Analyzes records in Reliability_Names with a given label to see how well
            the coding values agree across coders.
            
        Accepts:
        - label_IN - required label we want to use to filter Reliability_Names records.
        - indices_to_compare_IN - number of the coder indices you want to include in pairwise analysis (there are 10 total at the moment).
        '''

        # return reference
        status_OUT = ""
        
        # declare variables - set up database credentials
        me = "ReliabilityNamesAnalyzer.analyze_reliability_names"
        db_username = ""
        db_password = ""
        pandas_db_engine = None
        selected_label = ""
        
        # declare variables - use django to verify selected label.
        reliability_qs = None
        label_list = None
        label_in_list = []
        coder_index = -1
        
        # declare variables - SQLAlchemy lookup.
        cleaned_label = ""
        reliability_names_sql = ""
        reliability_names_df = None
        
        # declare variables - split into subjects and authors
        author_df = None
        subject_df = None
        
        # declare variables - set up comparisons
        indices_to_compare = -1
        current_index = -1
        compare_index = -1
        results_instance = None
        coder_1_user = -1
        coder_2_user = -1
        current_person_type = ""
        
        # declare variables - R connection
        r_conn = None
        
        # configuration - filter on a specific label.
        selected_label = label_IN
        
        # configuration - configure analysis
        indices_to_compare = indices_to_compare_IN
        self.indices_to_compare = indices_to_compare

        # configuration - init R connection
        r_conn = self.get_rserve_connection()
        r_conn.eval( "library( irr )" )
        
        # got a label?
        if ( ( selected_label is not None ) and ( selected_label != "" ) ):
        
            # first, use django to check if label is valid.
            
            # get list of label values.
            label_list = Reliability_Names.objects.values_list( self.COLUMN_NAME_LABEL, flat = True )
        
            # see if selected label is in list.
            if ( selected_label in label_list ):
            
                # yes - switch over to SQLAlchemy and pandas.
        
                self.output_debug_message( "Selected label: " + selected_label, method_IN = me )
                
                # escape out any illegal characters (PostgreSQL-specific).
                cleaned_label = psycopg2.extensions.adapt( selected_label ).getquoted()
                
                self.output_debug_message( "Cleaned label: " + str( cleaned_label ), method_IN = me )
                
                # Convert to unicode?
                cleaned_label = cleaned_label.decode()
                
                self.output_debug_message( "Cleaned Unicode label: " + str( cleaned_label ), method_IN = me )
            
                try:
            
                    # yes - set up database credentials
                    db_username = self.db_username
                    db_password = self.db_password
                    db_host = self.db_host
                    db_name = self.db_name
                    
                    # Create SQLAlchemy database engine for pandas.
                    pandas_db = sqlalchemy.create_engine( "postgresql://%s:%s@%s/%s" % ( db_username, db_password, db_host, db_name ) )
                    
                    # create SQL to load data from database into pandas data frame.
                    reliability_names_sql = "SELECT * FROM context_analysis_reliability_names WHERE label = %s" % ( cleaned_label )
    
                    self.output_debug_message( "Reliability_Names SQL Query: " + reliability_names_sql, method_IN = me )
                    
                    # load the data
                    reliability_names_df = pandas.read_sql_query( reliability_names_sql, pandas_db, parse_dates = [ 'create_date', 'last_modified' ] )
                    
                    # store coder info
                    self.store_coder_info( reliability_names_df, indices_to_compare )
                    
                    # break out into author and subject.
                    author_df = reliability_names_df[ reliability_names_df[ "person_type" ] == ManualArticleCoder.PERSON_TYPE_AUTHOR ]
                    subject_df = reliability_names_df[ reliability_names_df[ "person_type" ] == ManualArticleCoder.PERSON_TYPE_SUBJECT ]
                    
                    # loop over indices to compare
                    for current_index in range( 1, indices_to_compare + 1 ):
                    
                        print( "==> current index = " + str( current_index ) )
                    
                        # now, get comparison index
                        for comparison_index in range( current_index + 1, indices_to_compare + 1 ):
                        
                            print( "====> comparison index = " + str( comparison_index ) )
                    
                            # ! pair-wise comparison
                            
                            # create results instance to hold results.
                            results_instance = Reliability_Names_Results()
                            
                            # populate general information
                            results_instance.label = selected_label
                            results_instance.coder1_coder_index = current_index
                            results_instance.coder2_coder_index = comparison_index
                            
                            # user instances
                            coder_1_user = self.get_coder_for_index( current_index )
                            results_instance.coder1 = coder_1_user
                            coder_2_user = self.get_coder_for_index( comparison_index )
                            results_instance.coder2 = coder_2_user
            
                            # ! author
                            current_person_type = self.PERSON_TYPE_AUTHOR
                            
                            # call analyze_person_coding()
                            results_instance = self.analyze_person_coding( current_index,
                                                                           comparison_index,
                                                                           author_df,
                                                                           current_person_type,
                                                                           results_instance )
            
                            # ! subject
                            current_person_type = self.PERSON_TYPE_SUBJECT
                            
                            # call analyze_person_coding()
                            results_instance = self.analyze_person_coding( current_index,
                                                                           comparison_index,
                                                                           subject_df,
                                                                           current_person_type,
                                                                           results_instance )
                                                                           
                            # save the results.
                            results_instance.save()
    
                        #-- END loop over comparison indices --#
                        
                    #-- END loop over indices --#
                    
                    # ==> optionally, use pandas to output Excel.
                    
                except Exception as e:
                
                    # use ExceptionHelper to process the exception.
                    self.process_exception( e, message_IN = "Exception caught in " + me )
                    
                    status_OUT = "Exception caught: " + str( e )
                    
                    self.output_debug_message( "In " + me + "(): " + status_OUT )
                
                #-- END try-except around database and R access --#
        
            else:
            
                # no matches - either hack attack, or unknown label. Assume the latter.
                status_OUT = "No matches for label " + selected_label
            
            #-- END check to see if anything to filter on --#
        
        else:
        
            # no matches - either hack attack, or unknown label. Assume the latter.
            status_OUT = "No label passed in - nothing to see here."
            
        #-- END check to make sure we have a label.
        
        self.close_rserve_connection()
        
        return status_OUT

    #-- END method analyze_reliability_names() --#

       
    def get_coder_for_index( self, index_IN ):
        
        '''
        Accepts a coder index.  Uses it to get ID of coder associated with that
           index, and returns instance of that User.  If none found, returns
           None.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        coder_index_to_instance_dict = {}
        
        # get map from instance
        coder_index_to_instance_dict = self.coder_index_to_instance_map
        
        # retrieve instance for index passed in.
        instance_OUT = coder_index_to_instance_dict.get( index_IN, None )
        
        return instance_OUT        
        
    #-- END method get_coder_for_index() --#
    

    def store_coder_info( self, reliability_names_df_IN, indices_to_compare_IN = -1 ):
        
        '''
        for the number of indices we are comparing, go through and update
            internal maps to match coder information from the first row of our
            data frame.
        '''
        
        # declare variables
        me = "store_coder_info"
        current_index = -1
        column_name = ""
        user_id = -1
        user_instance = -1
        
        # is indices_to_compare_IN > 0?
        if ( ( indices_to_compare_IN is not None ) and ( indices_to_compare_IN != "" ) and ( indices_to_compare_IN > 0 ) ):
        
            # loop over indices.
            for current_index in range( 1, indices_to_compare_IN + 1 ):
            
                # got an index.  Retrieve coder ID for that index.
                column_name = self.COLUMN_NAME_PREFIX_CODER + str( current_index ) + self.COLUMN_NAME_SUFFIX_CODER_ID
                
                # get user ID for this instance from first item in this column..
                user_id = reliability_names_df_IN[ column_name ].iloc[ 0 ]
                
                # retrieve user instance based on ID.
                try:
                
                    user_instance = User.objects.get( pk = user_id )
                
                except ObjectDoesNotExist as odne:
                
                    # not found.  Store None.
                    user_instance = None
                
                except MultipleObjectsReturned as mor:
                
                    # multiple match primary key.  Oh no.  Store None.
                    user_instance = None
                
                except Exception as e:
                
                    # unexpected error.  Store none.
                    user_instance = None
                
                #-- END try-except to look up user using get() --#
                
                # update the maps.
                self.update_coder_at_index( current_index, user_instance, user_id )
                
            #-- END loop over indices. --#
            
        #-- END check to see if indices count passed in --#
        
    #-- END method store_coder_info() --#
    

    def update_coder_at_index( self, index_IN, instance_IN, id_IN = -1 ):
        
        '''
        Accepts a coder index and a coder's User instance.  Associates coder
            User passed in with the index passed in.  Returns coder User.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        coder_id = -1
        coder_index_to_instance_dict = {}
        coder_index_to_id_dict = {}
        
        # got an index?
        if ( ( index_IN is not None ) and ( index_IN != "" ) and ( index_IN > -1 ) ):
        
            # use ID passed in to start.
            coder_id = id_IN

            # got a coder instance (non-None)?
            if ( instance_IN is not None ):
            
                # yes - use the ID in the instance.
                coder_id = instance_IN.id
                
            #-- END check to see if we can get coder ID. --#
            
            # get maps from instance
            coder_index_to_instance_dict = self.coder_index_to_instance_map
            coder_index_to_id_dict = self.coder_index_to_id_map
            
            # place values in maps.
            coder_index_to_instance_dict[ index_IN ] = instance_IN
            coder_index_to_id_dict[ index_IN ] = coder_id
            
            # return instance for index
            instance_OUT = self.get_coder_for_index( index_IN )
        
        else:
        
            # no index - return None. 
            instance_OUT = None

        #-- END check to see if index. --#
            
        return instance_OUT        
        
    #-- END method update_coder_at_index() --#


#-- END class ReliabilityNamesAnalyzer --#
