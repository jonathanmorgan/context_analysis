# start to support python 3:
from __future__ import unicode_literals
from __future__ import division

#==============================================================================#
# ! imports
#==============================================================================#

# grouped by functional area, then alphabetical order by package, then
#     alphabetical order by name of thing being imported.

import numpy

# pandas
import pandas

# postgresql
import psycopg2.extensions

# integrate with R
import pyRserve

# python_utilities
from python_utilities.analysis.statistics.stats_helper import StatsHelper

# scipy
import scipy.stats.stats

# sourcenet imports
from sourcenet.article_coding.manual_coding.manual_article_coder import ManualArticleCoder

# sourcenet_analysis imports
from sourcenet_analysis.models import Reliability_Names

# import sqlalchemy for pandas database connection
import sqlalchemy

#==============================================================================#
# ! CONSTANTS-ish
#==============================================================================#

COLUMN_NAME = "column_name"
COLUMN_MEASUREMENT_LEVEL = "measurement_level"
COLUMN_VALUE_COUNT = "value_count"

#==============================================================================#
# ! functions
#==============================================================================#

def test_agreement( value_list_1_IN, value_list_2_IN, person_type_IN ):
    
    pass


'''
testAgreement <- function( codingMatrixIN, labelIN = "testAgreement", fileIN = "", corUseIN = "all.obs", corMethodIN = "pearson" ) {

    # Function: testAgreement()
    #
    # Accepts a matrix with coders as columns and observations per coder as rows.
    #    Calculates percentage agreement and Krippendorf's Alpha for the matrix,
    #    outputs the results.
    #
    # Arguments:
    # - codingMatrixIN - matrix that contains columns of values to be tested.
    # - labelIN - optional label to use when outputting the results.
    # - fileIN - optional path to file where results should be output.
    # - corUseIN - optional directive to instruct simple correlation which records to include.  Defaults to "all.obs", all rows.
    # - corMethodIN - optional directive to instruct which correlation to use to test simple correlation. Defaults to "pearson", Pearson's product-moment correlation.
    #
    # Hint: to make matrix, use cbind on vectors of coding results per coder.

    # return reference
    statusOUT <- "Success!"

    # declare variables
    codingMatrixTall <- NULL
    codingMatrixWide <- NULL
    tallColumnCount <- -1
    columnNumber <- -1
    rowNumber <- -1
    corResult <- NULL
    agreeResult <- NULL
    krippResult <- NULL

    # store matrix passed in in tall, then transpose so we have wide.
    codingMatrixTall <- codingMatrixIN
    tallColumnCount <- ncol( codingMatrixTall )
    codingMatrixWide <- t( codingMatrixTall )

    # got a file passed in?
    if ( fileIN != "" ){

        # yes - open it for output.
        sink( fileIN, append=TRUE, split=TRUE )

    }

    # output label
    cat( "\n#=============================================================================#\n" )
    cat( paste( labelIN, "\n" ) )
    cat( "#=============================================================================#\n\n" )

    # also output variance and standard deviation of each list, and a
    #    correlation coefficient, just for diagnostics.
    for( columnNumber in 1 : tallColumnCount ) {

        # output variance and standard deviation for this column.
        cat( paste( "var col", columnNumber, " = ", var( codingMatrixTall[ , columnNumber ] ), "\n", sep = "" ) )
        cat( paste( "sd col", columnNumber, " = ", sd( codingMatrixTall[ , columnNumber ] ), "\n", sep = "" ) )

    } #-- END loop over columns for variance and standard deviation --#

    # output correlations between columns.
    corResult <- cor( codingMatrixTall, use = corUseIN, method = corMethodIN )

    # loop over columns in corResult
    for( columnNumber in 1 : tallColumnCount ) {

        # then, loop through rows to to output - from 1 to columnNumber - 1.
        if ( columnNumber > 1 ) {

            for( rowNumber in 1 : ( tallColumnCount - 1 ) ) {

                # output the correlation coefficient.
                cat( paste( corMethodIN, " r[", rowNumber, ",", columnNumber, "] = ", corResult[ rowNumber, columnNumber ], "\n", sep = "" ) )

            } #-- END loop over rows. --#

        } #-- END check to make sure we aren't in first column. --#

    } #-- END loop over columns --#

    cat( "\n\n" )

    # got a file passed in?
    if ( fileIN != "" ){

        # return output to the terminal.
        sink()

    }

    # percentage agreement - wants the cbind matrix, not the rbind one.
    agreeResult <- irr::agree( codingMatrixTall )
    outputAgreeResults( agreeResult, fileIN )

    # Scott's Pi?

    # run Krippendorf's Alpha (not a good match to data - no variance)
    krippResult <- irr::kripp.alpha( codingMatrixWide, method = "nominal" )
    outputKrippResults( krippResult, fileIN )

    krippResult <- irr::kripp.alpha( codingMatrixWide, method = "ordinal" )
    outputKrippResults( krippResult, fileIN )

    krippResult <- irr::kripp.alpha( codingMatrixWide, method = "interval" )
    outputKrippResults( krippResult, fileIN )

    krippResult <- irr::kripp.alpha( codingMatrixWide, method = "ratio" )
    outputKrippResults( krippResult, fileIN )

    return( statusOUT )

} #-- END function testAgreement() --#
'''

#==============================================================================#
# ! logic
#==============================================================================#

# declare variables - set up database credentials
db_username = ""
db_password = ""
pandas_db_engine = None
selected_label = ""

# declare variables - use django to verify selected label.
reliability_qs = None
label_in_list = []
coder_index = -1

# declare variables - SQLAlchemy lookup.
reliability_names_sql = ""
reliability_names_df = None

# declare variables - split into subjects and authors
author_df = None
subject_df = None

# declare variables - set up comparisons
indices_to_compare = -1
columns_to_compare = []
current_index = -1
compare_index = -1
current_column_info = {}
current_column_name_suffix = ""
current_column_level = ""
current_column_value_count = -1
compare_column_name_1 = ""
compare_column_name_2 = ""
compare_values_1 = ""
compare_values_2 = ""
percentage_agreement = -1
value_df = None
value_array = None
kripp_alpha_result = None
kripp_alpha = -1

# declare variables - R connection
r_conn = None

# configuration - filter on a specific label.
selected_label = "prelim_training_002"

# configuration - configure analysis
indices_to_compare = 3
columns_to_compare = []
columns_to_compare.append( { COLUMN_NAME: "_person_id", COLUMN_MEASUREMENT_LEVEL: StatsHelper.MEASUREMENT_LEVEL_NOMINAL, COLUMN_VALUE_COUNT: "-1" } )
columns_to_compare.append( { COLUMN_NAME: "_person_type_int", COLUMN_MEASUREMENT_LEVEL: StatsHelper.MEASUREMENT_LEVEL_NOMINAL, COLUMN_VALUE_COUNT: "4" } )
columns_to_compare.append( { COLUMN_NAME: "_detected", COLUMN_MEASUREMENT_LEVEL: StatsHelper.MEASUREMENT_LEVEL_NOMINAL, COLUMN_VALUE_COUNT: "2" } )

# configuration - init R connection
r_conn = pyRserve.connect()
r_conn.eval( "library( irr )" )

# got a label?
if ( ( selected_label is not None ) and ( selected_label != "" ) ):

    # first, use django to retrieve rows, to see if it is a valid label.

    # start with all Reliability_Names rows.
    reliability_qs = Reliability_Names.objects.all()
    
    # filter
    reliability_qs = reliability_qs.filter( label__in = [ selected_label, ] )

    # got anything back?
    if ( reliability_qs.count() > 0 ):
    
        # yes - switch over to SQLAlchemy and pandas.

        # escape out any illegal characters (PostgreSQL-specific).
        selected_label = psycopg2.extensions.adapt( selected_label ).getquoted()
    
        # yes - set up database credentials
        db_username = "jonathanmorgan"
        db_password = "mt75ebMHFCncuWBuA3uZqj"
        db_host = "localhost"
        db_name = "sourcenet"
        
        # Create SQLAlchemy database engine for pandas.
        pandas_db = sqlalchemy.create_engine( "postgresql://%s:%s@%s/%s" % ( db_username, db_password, db_host, db_name ) )
        
        # create SQL to load data from database into pandas data frame.
        reliability_names_sql = "SELECT * FROM sourcenet_analysis_reliability_names WHERE label = %s" % ( selected_label )
        
        # load the data
        reliability_names_df = pandas.read_sql_query( reliability_names_sql, pandas_db, parse_dates = [ 'create_date', 'last_modified' ] )
        
        # break out into author and subject.
        author_df = reliability_names_df[ reliability_names_df[ "person_type" ] == ManualArticleCoder.PERSON_TYPE_AUTHOR ]
        subject_df = reliability_names_df[ reliability_names_df[ "person_type" ] == ManualArticleCoder.PERSON_TYPE_SUBJECT ]
        
        # loop over indices to compare
        for current_index in range( 1, indices_to_compare + 1 ):
        
            print( "==> current index = " + str( current_index ) )
        
            # now, get comparison index
            for comparison_index in range( current_index + 1, indices_to_compare + 1 ):
            
                print( "====> comparison index = " + str( comparison_index ) )
        
                # loop over columns_to_compare
                for current_column_info in columns_to_compare:
                
                    # unpack column info
                    current_column_name_suffix = current_column_info[ COLUMN_NAME ]
                    current_column_level = current_column_info[ COLUMN_MEASUREMENT_LEVEL ]
                    current_column_value_count = current_column_info[ COLUMN_VALUE_COUNT ]
                    print( "======> current_column_name_suffix = " + str( current_column_name_suffix ) )

                    # build comparison column names from indices and column
                    #     name.
                    compare_column_name_1 = "coder" + str( current_index ) + current_column_name_suffix
                    compare_column_name_2 = "coder" + str( comparison_index ) + current_column_name_suffix
                    
                    print( "======> compare_column_name_1 = " + str( compare_column_name_1 ) )
                    print( "======> compare_column_name_2 = " + str( compare_column_name_2 ) )

                    # retrieve numpy arrays of column values.
                    compare_values_1 = author_df[ compare_column_name_1 ]
                    compare_values_2 = author_df[ compare_column_name_2 ]
                    
                    #print( "======> compare_values_1 = " + str( compare_values_1 ) )
                    #print( "======> compare_values_2 = " + str( compare_values_2 ) )

                    # for each type, get columns/numpy arrays for fields we want to check, then:

                    # ==> Pearson correlation coefficient
                    #correlation_result = scipy.stats.stats.pearsonr( compare_values_1, compare_values_2 )
                    #print( "========> correlation = " + str( correlation_result ) )
                    
                    # ==> percent agreement
                    percentage_agreement = StatsHelper.percentage_agreement( compare_values_1, compare_values_2 )
                    print( "========> percentage_agreement = " + str( percentage_agreement ) )
                    
                    # ==> krippendorff's alpha at appropriate measurement level.
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
                    print( "========> R irr::kripp.alpha = " + str( R_kripp_alpha ) )
                    
                    # ==> if necessary, modified Scott's Pi.
                    # see if there is a count of values.
                    if ( ( current_column_value_count is not None ) and ( current_column_value_count != "" ) and ( current_column_value_count > 0 ) ):
                    
                        # got a value count.  Make sure we are nominal, as well.
                        if ( ( current_column_level is not None ) and ( current_column_level == StatsHelper.MEASUREMENT_LEVEL_NOMINAL ) ):
                        
                            # and we are nominal.  Potter's Pi!
                            potter_pi = StatsHelper.potter_pi( compare_values_1, compare_values_2, coder_count_IN = int( indices_to_compare ), option_count_IN = int( current_column_value_count ) )
                            print( "========> Potter's Pi = " + str( potter_pi ) )
                            
                        #-- END check to see if nominal variable --#
                        
                    #-- END check to see if value count is non-zero. --#


                    # ==> build row(s) in database results table.
                    # ==> optionally, use pandas to output Excel.

                #-- END loop over column names --#
                
            #-- END loop over comparison indices --#
            
        #-- END loop over indices --#
        
    else:
    
        # no matches - either hack attack, or unknown label. Assume the latter.
        print( "No matches for label " + selected_label )
    
    #-- END check to see if anything to filter on --#

else:

    # no matches - either hack attack, or unknown label. Assume the latter.
    print( "No label passed in - nothing to see here." )
    
#-- END check to make sure we have a label.

r_conn.close()
