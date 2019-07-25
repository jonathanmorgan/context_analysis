#==============================================================================#
# Imports
#==============================================================================#

# install.packages( "sna" )
# install.packages( "statnet" )
library( "sna" )

#==============================================================================#
# Functions
#==============================================================================#


compareMatricesQAP <- function( matrix1IN, matrix2IN, outputPrefixIN = "matrix1-to-matrix2", outputPlotsIN = FALSE, debugFlagIN = FALSE ) {

    # Function compareMatricesQAP()
    #
    # Accepts two matrices with the same dimensions, and optional output prefix
    #     and flag telling if you want to output plots.  Compares matrices using
    #     graph correlation, graph covariance, and hamming distance, then
    #     outputs the resulting coefficients, along with QAP information on
    #     significance.
    #
    # preconditions: matrices passed in must have the same dimensions.  sna and
    #     statnet R packages must be installed.
    #
    # postconditions: Returns all the information it creates in a list with the
    #     following keys:
    #
    #     - graphSetArray - If debug_flag == TRUE, returns work array with each matrix as an item, 1 in position 1, 2 in position 2.
    #     - graphCorrelation - graph correlation
    #     - qapGcorResult - QAP analysis of graph correlation
    #     - graphCovariance - graph correlation
    #     - qapGcovResult - QAP analysis of graph correlation
    #     - graphHammingDist - graph correlation
    #     - qapHdistResult - QAP analysis of graph correlation    
    #


    # return reference
    matrixComparisonDetailsOUT <- list()
    
    # declare variables
    me <- "compareMatricesQAP"
    debugFlag <- FALSE
    graphSetArray <- NULL
    graphCorrelation <- NULL
    qapGcorResult <- NULL
    graphCovariance <- NULL
    qapGcovResult <- NULL
    graphHammingDist <- NULL
    qapHdistResult <- NULL

    # link to good doc on qaptest(){sna} function: http://www.inside-r.org/packages/cran/sna/docs/qaptest
    
    # First, need to load data - see (or just source() ) the file "sna-load_data.r".
    # source( "sna-load_data.r" )
    # does the following (among other things):
    # Start with loading in tab-delimited files.
    #humanNetworkData <- read.delim( "human-sourcenet_data-20150504-002453.tab", header = TRUE, row.names = 1, check.names = FALSE )
    #calaisNetworkData <- read.delim( "puter-sourcenet_data-20150504-002507.tab", header = TRUE, row.names = 1, check.names = FALSE )
    
    # remove the right-most column, which contains non-tie info on nodes.
    #humanNetworkTies <- humanNetworkData[ , -ncol( humanNetworkData ) ]
    #gw2AutomatedNetworkDF <- calaisNetworkData[ , -ncol( calaisNetworkData )]
    
    # convert each to a matrix
    #gw2HumanNetworkMatrix <- as.matrix( gw2HumanNetworkTies )
    #matrix2IN <- as.matrix( gw2AutomatedNetworkDF )
    
    # debug?
    debugFlag <- debugFlagIN
    
    message( paste( "==> Start of ", me, " at ", Sys.time(), sep = " " ) )

    # package up data for calling qaptest() - first make 3-dimensional array to hold
    #    our two matrices - this is known as a "graph set".
    graphSetArray <- array( dim = c( 2, ncol( matrix1IN ), nrow( matrix1IN ) ) )
    
    # then, place each matrix in one dimension of the array.
    graphSetArray[ 1, , ] <- matrix1IN
    graphSetArray[ 2, , ] <- matrix2IN
    
    # debug?
    if ( debugFlag == TRUE ){

        # add it to return list.
        matrixComparisonDetailsOUT$graphSetArray <- graphSetArray
        
    }
    
    # ! ==> first, try a graph correlation
    graphCorrelation <- sna::gcor( matrix1IN, matrix2IN )
    matrixComparisonDetailsOUT$graphCorrelation <- graphCorrelation
    message( paste( "---->", outputPrefixIN, "graph correlation =", graphCorrelation, "( @", Sys.time(), ")", sep = " " ) )
    
    # try a qaptest...
    qapGcorResult <- sna::qaptest( graphSetArray, sna::gcor, g1 = 1, g2 = 2 )
    matrixComparisonDetailsOUT$qapGcorResult <- qapGcorResult
    message( paste( "----> ", outputPrefixIN, " QAP correlation analysis complete at ", Sys.time(), ".  Summary:", sep = "" ) )
    message( print( summary( qapGcorResult ) ) )
    
    # output plot?
    if ( outputPlotsIN == TRUE ){

        # output plot
        plot( qapGcorResult )

    }
    
    # ! ==> graph covariance...
    graphCovariance <- sna::gcov( matrix1IN, matrix2IN )
    matrixComparisonDetailsOUT$graphCovariance <- graphCovariance
    message( paste( "---->", outputPrefixIN, "graph covariance =", graphCovariance, "( @", Sys.time(), ")", sep = " " ) )
    
    # try a qaptest...
    qapGcovResult <- sna::qaptest( graphSetArray, sna::gcov, g1 = 1, g2 = 2 )
    matrixComparisonDetailsOUT$qapGcovResult <- qapGcovResult
    message( paste( "----> ", outputPrefixIN, " QAP covariance analysis complete at ", Sys.time(), ".  Summary:", sep = "" ) )
    message( print( summary( qapGcovResult ) ) )

    # output plot?
    if ( outputPlotsIN == TRUE ){

        # output plot
        plot( qapGcovResult )

    }
    
    # ! ==> Hamming Distance
    graphHammingDist <- sna::hdist( matrix1IN, matrix2IN )
    matrixComparisonDetailsOUT$graphHammingDist <- graphHammingDist
    message( paste( "---->", outputPrefixIN, "graph hamming distance =", graphHammingDist, "( @", Sys.time(), ")", sep = " " ) )
    
    # try a qaptest...
    qapHdistResult <- sna::qaptest( graphSetArray, sna::hdist, g1 = 1, g2 = 2 )
    matrixComparisonDetailsOUT$qapHdistResult <- qapHdistResult
    message( paste( "----> ", outputPrefixIN, " QAP hamming distance analysis complete at ", Sys.time(), ".  Summary:", sep = "" ) )
    message( print( summary( qapHdistResult ) ) )

    # output plot?
    if ( outputPlotsIN == TRUE ){

        # output plot
        plot( qapHdistResult )

    }
    
    # graph structural correlation?
    #graphStructCorrelation <- gscor( matrix1IN, matrix2IN )
    #graphStructCorrelation
    
    message( paste( "==> End of ", me, " at ", Sys.time(), sep = " " ) )

    # return value
    return( matrixComparisonDetailsOUT )

} #-- END function compareMatricesQAP() --#


displayCompareMatricesQAPOutput <- function( qapOutputIN, outputPrefixIN = "matrix1-to-matrix2", outputPlotsIN = FALSE, debugFlagIN = FALSE ) {

    # Function displayCompareMatricesQAPOutput()
    #
    # Accepts return reference from call to compareMatricesQAP().  Outputs the
    #     resulting coefficients, along with QAP information on significance and
    #     optional QAP value distribution plots.
    #
    # preconditions: must have called compareMatricesQAP() and stored the
    #     result.
    #
    # postconditions: Outputs information, doesn't change anything.

    # declare variables
    me <- "displayCompareMatricesQAPOutput"
    debugFlag <- FALSE
    graphSetArray <- NULL
    graphCorrelation <- NULL
    qapGcorResult <- NULL
    graphCovariance <- NULL
    qapGcovResult <- NULL
    graphHammingDist <- NULL
    qapHdistResult <- NULL

    # debug?
    debugFlag <- debugFlagIN
    
    # ! ==> output graph correlation
    graphCorrelation <- qapOutputIN$graphCorrelation
    message( paste( "---->", outputPrefixIN, "graph correlation =", graphCorrelation, sep = " " ) )
    
    # QAP
    qapGcorResult <- qapOutputIN$qapGcorResult
    message( paste( "----> ", outputPrefixIN, " QAP correlation analysis summary:", sep = "" ) )
    message( print( summary( qapGcorResult ) ) )
    
    # output plot?
    if ( outputPlotsIN == TRUE ){

        # output plot
        plot( qapGcorResult )

    }
    
    # ! ==> output graph covariance...
    graphCovariance <- qapOutputIN$graphCovariance
    message( paste( "---->", outputPrefixIN, "graph covariance =", graphCovariance, sep = " " ) )
    
    # try a qaptest...
    qapGcovResult <- qapOutputIN$qapGcovResult
    message( paste( "----> ", outputPrefixIN, " QAP covariance analysis summary:", sep = "" ) )
    message( print( summary( qapGcovResult ) ) )

    # output plot?
    if ( outputPlotsIN == TRUE ){

        # output plot
        plot( qapGcovResult )

    }
    
    # ! ==> Hamming Distance
    graphHammingDist <- qapOutputIN$graphHammingDist
    message( paste( "---->", outputPrefixIN, "graph hamming distance =", graphHammingDist, sep = " " ) )
    
    # try a qaptest...
    qapHdistResult <- qapOutputIN$qapHdistResult
    message( paste( "----> ", outputPrefixIN, " QAP hamming distance analysis summary:", sep = "" ) )
    message( print( summary( qapHdistResult ) ) )

    # output plot?
    if ( outputPlotsIN == TRUE ){

        # output plot
        plot( qapHdistResult )

    }
    
} #-- END function displayCompareMatricesQAPOutput() --#
