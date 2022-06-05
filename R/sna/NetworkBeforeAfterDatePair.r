# ReferenceClass NetworkBeforeAfterDatePair
# - for help: `help( ReferenceClasses )`
# - https://www.rdocumentation.org/packages/methods/versions/3.6.2/topics/ReferenceClasses

# Dependencies:
# - Depends on NetworkInfo ReferenceClass.
# - Depends on functions-statnet.r

# Usage:
# testNetworkPair <- NetworkBeforeAfterDatePair()
# testNetworkPair$myBaseDate <<- "2009-05-12"
# testNetworkPair$myLabel <<- paste( testNetworkPair$myBaseDate, "-6mos", sep = "" )


#==============================================================================#
# imports
#==============================================================================#

#==============================================================================#
# class definition
#==============================================================================#

networkBeforeAfterDatePair_fields <- list(
    myAfterNetwork = "ANY",
    myAfterNetworkMatrix = "matrix",
    myBaseDate = "character",
    myBeforeNetwork = "ANY",
    myBeforeNetworkMatrix = "matrix",
    myGraphCorrelation = "numeric",
    myGraphCorrelationQAPResult = "ANY",
    myGraphCovariance = "numeric",
    myGraphCovarianceQAPResult = "ANY",
    myGraphHammingDistance = "numeric",
    myGraphHammingDistanceQAPResult = "ANY",
    myLabel = "character",
    myMatrixComparison = "ANY"
)

NetworkBeforeAfterDatePair <- setRefClass(
    "NetworkBeforeAfterDatePair",
    fields = networkBeforeAfterDatePair_fields
)

#==============================================================================#
# instance methods
#==============================================================================#

NetworkBeforeAfterDatePair$methods(
    compareMatrices = function( outputPlotsIN = FALSE,
                                debugFlagIN = FALSE,
                                repsIN = 10,
                                doQapIN = FALSE ) {

        # declare variables
        outputPrefix <- NULL
        beforeMatrix <- NULL
        afterMatrix <- NULL
        
        # set output prefix to the file name.
        outputPrefix <- myLabel
        
        # retrieve matrices
        beforeMatrix <- myBeforeNetworkMatrix
        afterMatrix <- myAfterNetworkMatrix

        myMatrixComparison <<- compareMatricesQAP(
            beforeMatrix,
            afterMatrix,
            outputPrefixIN = outputPrefix,
            outputPlotsIN = outputPlotsIN,
            debugFlagIN = debugFlagIN,
            repsIN = repsIN,
            doQapIN = doQapIN )
        
        # retrieve and store individual values.
        myGraphCorrelation <<- myMatrixComparison$graphCorrelation
        myGraphCorrelationQAPResult <<- myMatrixComparison$qapGcorResult
        myGraphCovariance <<- myMatrixComparison$graphCovariance
        myGraphCovarianceQAPResult <<- myMatrixComparison$qapGcovResult
        myGraphHammingDistance <<- myMatrixComparison$graphHammingDist
        myGraphHammingDistanceQAPResult <<- myMatrixComparison$qapHdistResult

        if ( doQapIN == TRUE ){
            
            # also output plots of distributions of QAP values?
            if ( outputPlotsIN == TRUE ){
                
                # yes, output those plots, also, I guess.
                displayCompareMatricesQAPOutput( myMatrixComparisonData, outputPrefix, TRUE )
            
            }
            
        }
        
    } #-- END method compareMatrices() --#
    
)

NetworkBeforeAfterDatePair$methods(
    loadAfterNetwork = function( dataDirPathIN, fileNameIN ) {
        
        'Accepts data directory and file name, combines them into path,
         loads the network, then processes it so we are ready to compare.'

        # declare variables
        workNetwork <- NULL
        
        # create NetworkInfo instance
        workNetwork <- NetworkInfo()
        
        # init using file information passed in.
        workNetwork$initFromTabData( dataDirPathIN, fileNameIN )
        
        # process the network.
        workNetwork$processNetwork()
        
        # store matrix
        myAfterNetworkMatrix <<- workNetwork$myNetworkMatrix
        
        # store inside
        myAfterNetwork <<- workNetwork
        
    } #-- END method loadAfterNetwork() --#
)

NetworkBeforeAfterDatePair$methods(
    loadBeforeNetwork = function( dataDirPathIN, fileNameIN ) {
        
        'Accepts data directory and file name, combines them into path,
         loads them into data frame, then makes all the other objects
         we need.'

        # declare variables
        workNetwork <- NULL
        
        # create NetworkInfo instance
        workNetwork <- NetworkInfo()
        
        # init using file information passed in.
        workNetwork$initFromTabData( dataDirPathIN, fileNameIN )
        
        # process the network.
        workNetwork$processNetwork()
        
        # store matrix
        myBeforeNetworkMatrix <<- workNetwork$myNetworkMatrix
        
        # store inside
        myBeforeNetwork <<- workNetwork
        
    } #-- END method loadBeforeNetwork() --#
)

message( paste( "ReferenceClass NetworkBeforeAfterDatePair defined @ ", date(), sep = "" ) )
