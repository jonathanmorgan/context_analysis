# postgresql
import psycopg2.extensions

# import sqlalchemy for pandas database connection
import sqlalchemy

# pandas
import pandas

# sourcenet imports
from sourcenet.article_coding.manual_coding.manual_article_coder import ManualArticleCoder

# sourcenet_analysis imports
from sourcenet_analysis.models import Reliability_Names

# functions

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

# filter on a specific label.
selected_label = "prelim_training_002"

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
        
        # for each type, get columns/numpy arrays for fields we want to check, then:
        # - percent agreement
        # - krippendorff's alpha at appropriate measurement level.
        # - if necessary, modified Scott's Pi.
        # - build row(s) in database results table.
        # - optionally, use pandas to output Excel.
        
    else:
    
        # no matches - either hack attack, or unknown label. Assume the latter.
        print( "No matches for label " + selected_label )
    
    #-- END check to see if anything to filter on --#

else:

    # no matches - either hack attack, or unknown label. Assume the latter.
    print( "No label passed in - nothing to see here." )
    
#-- END check to make sure we have a label.
