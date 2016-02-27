# sourcenet imports
from sourcenet.article_coding.manual_coding.manual_article_coder import ManualArticleCoder

# sourcenet_analysis imports
from sourcenet_analysis.models import Reliability_Names

# functions

def test_agreement( value_list_1_IN, value_list_2_IN, person_type_IN,  )

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

# declare variables
reliability_qs = None
label_in_list = []
author_qs = None
subject_qs = None
coder_index = -1

# start with all Reliability_Names rows.
reliability_qs = Reliability_Names.objects.all()

# filter on label?
filter_in_list = [ "prelim_training_002", ]
if ( ( filter_in_list is not None ) and ( len( filter_in_list ) > 0 ) ):

    # filter
    reliability_qs = reliability_qs.filter( label__in = filter_in_list )
    
#-- END check to see if anything to filter on --#

# how many coders, and in which indices (1 through 10)?


# break out into authors and subjects (very different, can't just lump together)
#    based on person_type - "author" or "subject".
author_qs = reliability_qs.filter( person_type = ManualArticleCoder.PERSON_TYPE_AUTHOR )
subject_qs = reliability_qs.filter( person_type = ManualArticleCoder.PERSON_TYPE_SUBJECT )

# first, work with author information
