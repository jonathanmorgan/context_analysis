# ReferenceClass NetworkInfo
# - for help: `help( ReferenceClasses )`
# - https://www.rdocumentation.org/packages/methods/versions/3.6.2/topics/ReferenceClasses

#==============================================================================#
# imports
#==============================================================================#

library( irr )
library( sna )
library( statnet )

#==============================================================================#
# class definition
#==============================================================================#

networkInfo_fields <- list(
    myAuthorCount2And4 = "numeric",
    myAuthorCountOnly2 = "numeric",
    myBetweennessCentrality = "numeric",
    myBetweennessVector = "vector",
    myBinaryDegreeVector = "vector",
    myColumnCount = "integer",
    myConnectedness = "numeric",
    myDataDF = "data.frame",
    myDataFileName = "character",
    myDataPath = "character",
    myDebugFlag = "logical",
    myDegreeAverage = "numeric",
    myDegreeAverageAuthor2And4 = "numeric",
    myDegreeAverageAuthorOnly2 = "numeric",
    myDegreeAverageSource3And4 = "numeric",
    myDegreeAverageSourceOnly3 = "numeric",
    myDegreeCentrality = "numeric",
    myDegreeFrequenciesTable = "table",
    myDegreeMax = "numeric",
    myDegreeVariance = "numeric",
    myDegreeVector = "vector",
    myDegreeStandardDeviation = "numeric",
    myDensity = "numeric",
    myNetworkAttributeDF = "data.frame",
    myNetworkDF = "data.frame",
    myNetworkMatrix = "matrix",
    myNetworkStatnet = "ANY",
    myRowCount = "integer",
    mySourceCount3And4 = "numeric",
    mySourceCountOnly3 = "numeric",
    myTransitivity = "numeric"
)

NetworkInfo <- setRefClass(
    "NetworkInfo",
    fields = networkInfo_fields,
    methods = list(
        initialize=function( debugFlagIN = FALSE ) {
            myDebugFlag <<- debugFlagIN
        }
    )
)

#==============================================================================#
# instance methods
#==============================================================================#


NetworkInfo$methods(
    calcMyAuthorCount = function( includeBothIN = TRUE ) {

        # Function calcMyAuthorCount()
        #
        # Filters data frame to just authors using myDataDF$person_type (2 or 4),
        #    then counts rows and returns that count.
        #
        # preconditions: data frame passed in must have $person_type column.

        # return reference
        valueOUT <- -1

        # declare variables
        authorDF <- NULL

        # filter data frame
        authorDF <- getMyAuthorDF( includeBothIN = includeBothIN )

        # calculate mean of $degree column.
        valueOUT <- nrow( authorDF )

        # return value
        return( valueOUT )
    
    } #-- END function calcMyAuthorCount() --#
)


NetworkInfo$methods(
    calcMyAuthorMeanDegree = function( includeBothIN = TRUE ) {

        # Function calcMyAuthorMeanDegree()
        #
        # Filters data frame to just authors using dataFrameIN$person_type (2 or 4),
        #    then calculates and returns the mean of the column dataFrameIN$degree.
        #
        # preconditions: data frame passed in must have $person_type and $degree
        #    columns.

        # return reference
        valueOUT <- -1

        # declare variables
        authorDF <- NULL

        # filter data frame
        authorDF <- getMyAuthorDF( includeBothIN = includeBothIN )

        # calculate mean of $degree column.
        valueOUT <- mean( authorDF$degree )

        # return value
        return( valueOUT )

    } #-- END function calcMyAuthorMeanDegree() --#
)


NetworkInfo$methods(
    calcMySourceCount = function( includeBothIN = TRUE ) {

        # Function calcMySourceCount()
        #
        # Filters data frame to just sources using dataFrameIN$person_type (3 or 4),
        #    then calculates and returns count of rows.
        #
        # preconditions: data frame passed in must have $person_type column.

        # return reference
        valueOUT <- -1

        # declare variables
        sourceDF <- NULL

        # filter data frame
        sourceDF <- getMySourceDF( includeBothIN = includeBothIN )

        # calculate mean of $degree column.
        valueOUT <- nrow( sourceDF )

        # return value
        return( valueOUT )

    } #-- END function calcMySourceCount() --#
)


NetworkInfo$methods(
    calcMySourceMeanDegree = function( includeBothIN = TRUE ) {

        # Function calcMySourceMeanDegree()
        #
        # Filters data frame to just sources using dataFrameIN$person_type (3 or 4),
        #    then calculates and returns the mean of the column dataFrameIN$degree.
        #
        # preconditions: data frame passed in must have $person_type and $degree
        #    columns.

        # return reference
        valueOUT <- -1

        # declare variables
        sourceDF <- NULL

        # filter data frame
        sourceDF <- getMySourceDF( includeBothIN = includeBothIN )

        # calculate mean of $degree column.
        valueOUT <- mean( sourceDF$degree )

        # return value
        return( valueOUT )

    } #-- END function calcMySourceMeanDegree() --#
)


NetworkInfo$methods(
    calculateDegreeAverages = function() {

        'preconditions: must have already called "createDegreeVectors()".'
        
        # what is the average (mean) degree?
        myDegreeAverage <<- mean( myDegreeVector )

        if ( myDebugFlag == TRUE ){
            message( paste( "average degree = ", myDegreeAverage, sep = "" ) )
        }

        # subset vector to get only those that are above mean
        #testAboveMeanVector <- testDegreeVector[ testDegreeVector > testAvgDegree ]

        # average author degree (person types 2 and 4)
        myDegreeAverageAuthor2And4 <<- calcMyAuthorMeanDegree( includeBothIN = TRUE )

        if ( myDebugFlag == TRUE ){
            message( paste( "average author degree (2 and 4) = ", myDegreeAverageAuthor2And4, sep = "" ) )
        }

        # average author degree (person type 2 only)
        myDegreeAverageAuthorOnly2 <<- calcMyAuthorMeanDegree( includeBothIN = FALSE )

        if ( myDebugFlag == TRUE ){
            message( paste( "average author degree (only 2) = ", myDegreeAverageAuthorOnly2, sep = "" ) )
        }

        # average source degree (person types 3 and 4)
        myDegreeAverageSource3And4 <<- calcMySourceMeanDegree( includeBothIN = TRUE )
        
        if ( myDebugFlag == TRUE ){
            message( paste( "average source degree (3 and 4) = ", myDegreeAverageSource3And4, sep = "" ) )
        }

        # average source degree (person type 3 only)
        myDegreeAverageSourceOnly3 <<- calcMySourceMeanDegree( includeBothIN = FALSE )
        
        if ( myDebugFlag == TRUE ){
            message( paste( "average source degree (only 3) = ", myDegreeAverageSourceOnly3, sep = "" ) )
        }

        # what is the standard deviation of the degrees?
        myDegreeStandardDeviation <<- sd( myDegreeVector )
        
        if ( myDebugFlag == TRUE ){
            message( paste( "degree SD = ", myDegreeStandardDeviation, sep = "" ) )
        }

        # what is the variance of the degrees?
        myDegreeVariance <<- var( myDegreeVector )

        if ( myDebugFlag == TRUE ){
            message( paste( "degree variance = ", myDegreeVariance, sep = "" ) )
        }

        # what is the max value among the degrees?
        myDegreeMax <<- max( myDegreeVector )
        
        if ( myDebugFlag == TRUE ){
            message( paste( "degree max = ", myDegreeMax, sep = "" ) )
        }

        # calculate and plot degree distributions
        myDegreeFrequenciesTable <<- table( myDegreeVector )

    } #-- END method calculateDegreeAverages() --#
)


NetworkInfo$methods(
    calculateNetworkLevelMetrics = function() {

        #==============================================================================#
        # NETWORK level
        #==============================================================================#

        # graph-level degree centrality
        myDegreeCentrality <<- sna::centralization( myNetworkStatnet, sna::degree, mode = "graph" )
        
        if ( myDebugFlag == TRUE ){
            message( paste( "degree centrality = ", myDegreeCentrality, sep = "" ) )
        }

        # graph-level betweenness centrality
        myBetweennessCentrality <<- sna::centralization( myNetworkStatnet, sna::betweenness, mode = "graph", cmode = "undirected" )
        
        if ( myDebugFlag == TRUE ){
            message( paste( "betweenness centrality = ", myBetweennessCentrality, sep = "" ) )
        }

        # graph-level connectedness
        myConnectedness <<- sna::connectedness( myNetworkStatnet )
        
        if ( myDebugFlag == TRUE ){
            message( paste( "connectedness = ", myConnectedness, sep = "" ) )
        }

        # graph-level transitivity
        myTransitivity <<- sna::gtrans( myNetworkStatnet, mode = "graph" )
        
        if ( myDebugFlag == TRUE ){
            message( paste( "transitivity = ", myTransitivity, sep = "" ) )
        }

        # graph-level density
        myDensity <<- sna::gden( myNetworkStatnet, mode = "graph" )
        
        if ( myDebugFlag == TRUE ){
            message( paste( "density = ", myDensity, sep = "" ) )
        }

        # author and source counts
        myAuthorCount2And4 <<- calcMyAuthorCount( includeBothIN = TRUE )
        myAuthorCountOnly2 <<- calcMyAuthorCount( includeBothIN = FALSE )
        mySourceCount3And4 <<- calcMySourceCount( includeBothIN = TRUE )
        mySourceCountOnly3 <<- calcMySourceCount( includeBothIN = FALSE )

        if ( myDebugFlag == TRUE ){
            message( paste( "AuthorCount2And4 = ", myAuthorCount2And4, sep = "" ) )
            message( paste( "AuthorCountOnly2 = ", myAuthorCountOnly2, sep = "" ) )
            message( paste( "SourceCount3And4 = ", mySourceCount3And4, sep = "" ) )
            message( paste( "SourceCountOnly3 = ", mySourceCountOnly3, sep = "" ) )
        }
    
    } #-- END method calculateNetworkLevelMetrics() --#
)


NetworkInfo$methods(
    createBetweennessVector = function() {

        # node-level undirected betweenness
        myBetweennessVector <<- sna::betweenness( myNetworkStatnet, gmode = "graph", cmode = "undirected" )

        #paste( "betweenness = ", testBetweenness, sep = "" )
        # associate with each node as a node attribute.
        #    (%v% is a shortcut for the get.vertex.attribute command)
        myNetworkStatnet %v% "betweenness" <<- myBetweennessVector

        # also add degree vector to original data frame
        myDataDF$betweenness <<- myBetweennessVector
        
    } #-- END method createBetweennessVector() --#
)
    

NetworkInfo$methods(
    createDegreeVectors = function() {
      
        # declare variables
        workDegreeVector <- NULL

        # assuming that our statnet network object is in reference myNetworkStatnet

        # Use the degree function in the sna package to create vector of degree values
        #    for each node, then compute average.  Make sure to pass the gmode parameter to tell it that the
        #    graph is not directed (gmode = "graph", instead of "digraph").
        # Doc: http://www.inside-r.org/packages/cran/sna/docs/degree
        #degree_vector <- degree( test1_statnet, gmode = "graph" )

        # If you have other libraries loaded that also implement a degree function, you
        #    can also call this with package name:
        myDegreeVector <<- sna::degree( myNetworkStatnet, gmode = "graph" )
        
        # also, convert the degree vector to binary, where degree >= 1 becomes
        #     degree of 1.
        workDegreeVector <- myDegreeVector
        workDegreeVector[ workDegreeVector > 1 ] <- 1
        myBinaryDegreeVector <<- workDegreeVector
        
        # Take the degree and associate it with each node as a node attribute.
        #    (%v% is a shortcut for the get.vertex.attribute command)
        myNetworkStatnet %v% "degree" <<- myDegreeVector

        # also add degree vector to original data frame
        myDataDF$degree <<- myDegreeVector
        
    } #-- END method createDegreeVectors() --#
)


NetworkInfo$methods(
    getBinaryNetworkMatrix = function() {
        
        # Function getBinaryNetworkMatrix()
        #
        # Filters data frame to just authors using dataFrameIN$person_type (2 or 4),
        #     returns resulting data.frame.
        #
        # preconditions: data frame passed in must have $person_type column.
        
        # return reference
        matrixOUT <- NULL
        
        # start with matrix.
        matrixOUT <- myNetworkMatrix

        # assign 1 for all values greater than 0
        matrixOUT[ matrixOUT > 0 ] <- 1
        
        # OR
        #matrixOUT <- ifelse( matrixOUT > 0, 1, 0 )
        
        # make sure it is a matrix...?
        #matrixOUT <- as.matrix( matrixOUT )

        # return value
        return( matrixOUT )
        
    } #-- END function getBinaryNetworkMatrix() --#
)


NetworkInfo$methods(
    getMyAuthorDF = function( includeBothIN = TRUE ) {

        # Function getMyAuthorDF()
        #
        # Filters data frame to just authors using dataFrameIN$person_type (2 or 4),
        #     returns resulting data.frame.
        #
        # preconditions: data frame passed in must have $person_type column.

        # return reference
        authorDFOUT <- NULL

        # filter data frame
        authorDFOUT <- myDataDF[ myDataDF$person_type == 2 | myDataDF$person_type == 4, ]

        # include both?
        if ( includeBothIN == FALSE ){

            # don't include both - just person_type = 2.
            authorDFOUT <- authorDFOUT[ authorDFOUT$person_type == 2, ]

        }

        # return value
        return( authorDFOUT )

    } #-- END function getMyAuthorDF() --#
)


NetworkInfo$methods(
    getMySourceDF = function( includeBothIN = TRUE ) {

        # Function getMySourceDF()
        #
        # Filters data frame to just sources using dataFrameIN$person_type (3 or 4),
        #     returns resulting data.frame.
        #
        # preconditions: data frame passed in must have $person_type column.

        # return reference
        sourceDFOUT <- NULL

        # filter data frame
        sourceDFOUT <- myDataDF[ myDataDF$person_type == 3 | myDataDF$person_type == 4, ]

        # include both?
        if ( includeBothIN == FALSE ){

            # don't include both - just person_type = 3.
            sourceDFOUT <- sourceDFOUT[ sourceDFOUT$person_type == 3, ]

        }

        # return value
        return( sourceDFOUT )

    } #-- END method getMySourceDF() --#
)


NetworkInfo$methods(
    initFromTabData = function( dataDirPathIN, fileNameIN ) {

        'Accepts data directory and file name, combines them into path,
         loads them into data frame, then makes all the other objects
         we need.'

        # declare variables
        myDataFolder <- NULL
        
        # initialize variables
        myDataFolder <- dataDirPathIN
        myDataFileName <<- fileNameIN
        myDataPath <<- paste( myDataFolder, "/", myDataFileName, sep = "" )

        # tab-delimited:
        myDataDF <<- read.delim( myDataPath, header = TRUE, row.names = 1, check.names = FALSE )

        # get row and column count
        myRowCount <<- nrow( myDataDF )
        myColumnCount <<- ncol( myDataDF )

        # get just the network part (no attributes)
        # - just as many columns as there are rows.
        myNetworkDF <<- myDataDF[ , 1 : myRowCount ]

        # convert to a matrix
        myNetworkMatrix <<- as.matrix( myNetworkDF )
        
        # If you have a data frame of attributes (each attribute is a column, with
        #     attribute name the column name), you can associate those attributes
        #     when you create the network.
        # attribute help: http://www.inside-r.org/packages/cran/network/docs/loading.attributes

        # load attributes from a file:
        #tab_attribute_test1 <- read.delim( "tab-test1-attribute_data.txt", header = TRUE, row.names = 1, check.names = FALSE )

        # or create DataFrame of just the attribute columns (right-most 2 columns)
        myNetworkAttributeDF <<- myDataDF[ , ( myColumnCount - 1 ) : myColumnCount ]

        # convert matrix to statnet network object instance.
        myNetworkStatnet <<- network( myNetworkMatrix, matrix.type = "adjacency", directed = FALSE, vertex.attr = myNetworkAttributeDF )

    } #-- END method initFromTabData() --#
)


NetworkInfo$methods(
    processNetwork = function() {

        'Call all of the create*() and calculate*() methods.
         - preconditions: assumes you have already called initFromTabData().'
        
        createDegreeVectors()
        createBetweennessVector()
        calculateDegreeAverages()
        calculateNetworkLevelMetrics()
        
    } #-- END method createBetweennessVector() --#
)
    
message( paste( "ReferenceClass NetworkInfo defined @ ", date(), sep = "" ) )

processBeforeAfterNetworks <- function(
    beforeDataDirectoryIN,
    beforeFileIN,
    afterDataDirectoryIN,
    afterFileIN,
    dateIN,
    networkDurationIN,
    labelIN,
    debugFlagIN = FALSE ) {

    # Accepts path info for before and after network data. Loads and processes
    #     each to create individual network information, then compares them
    #     to create correlation and other information about how the pair of
    #     networks compare, then packages all in a list with common column names
    #     to be included in a data.frame of information about a series of
    #     pairs of data.
    
    # return reference
    listOUT <- list()
    
    # declare variables
    beforeNetworkInfo <- NULL
    afterNetworkInfo <- NULL
    
    # declare variables - degree vector correlations
    workMatrix <- NULL
    agreeOutput <- NULL
    beforeDegreeVector <- NULL
    afterDegreeVector <- NULL
    degreeCorrelation <- NULL
    degreePercentAgree <- NULL
    beforeBinaryDegreeVector <- NULL
    afterBinaryDegreeVector <- NULL
    binaryDegreeCorrelation <- NULL
    binaryDegreePercentAgree <- NULL
    
    # declare variables - network comparisons
    beforeMatrix <- NULL
    afterMatrix <- NULL
    matrixComparison <- NULL
    graphCorrelation <- NULL
    graphCorrelationQAPResult <- NULL
    graphCovariance <- NULL
    graphCovarianceQAPResult <- NULL
    graphHammingDistance <- NULL
    graphHammingDistanceQAPResult <- NULL
    beforeBinMatrix <- NULL
    afterBinMatrix <- NULL
    binMatrixComparison <- NULL
    binGraphCorrelation <- NULL
    binGraphCorrelationQAPResult <- NULL
    binGraphCovariance <- NULL
    binGraphCovarianceQAPResult <- NULL
    binGraphHammingDistance <- NULL
    binGraphHammingDistanceQAPResult <- NULL
    
    # store the date, network duration, and label
    listOUT$baseDate <- as.Date( dateIN )
    listOUT$networkDuration <- networkDurationIN
    listOUT$label <- labelIN
    
    #--------------------------------------------------------------------------#
    # load and process before network.
    beforeNetworkInfo <- NetworkInfo( debugFlagIN = debugFlagIN )
    beforeNetworkInfo$initFromTabData(
        beforeDataDirectoryIN,
        beforeFileIN
    )
    beforeNetworkInfo$processNetwork()
    
    # add before information to the list
    listOUT$beforeAuthorCount2And4 <- beforeNetworkInfo$myAuthorCount2And4
    listOUT$beforeAuthorCountOnly2 <- beforeNetworkInfo$myAuthorCountOnly2
    listOUT$beforeBetweennessCentrality <- beforeNetworkInfo$myBetweennessCentrality
    listOUT$beforeConnectedness <- beforeNetworkInfo$myConnectedness
    listOUT$beforeColumnCount <- beforeNetworkInfo$myColumnCount
    listOUT$beforeDataFileName <- beforeNetworkInfo$myDataFileName
    listOUT$beforeDataPath <- beforeNetworkInfo$myDataPath
    listOUT$beforeDegreeAverage <- beforeNetworkInfo$myDegreeAverage
    listOUT$beforeDegreeAverageAuthor2And4 <- beforeNetworkInfo$myDegreeAverageAuthor2And4
    listOUT$beforeDegreeAverageAuthorOnly2 <- beforeNetworkInfo$myDegreeAverageAuthorOnly2
    listOUT$beforeDegreeAverageSource3And4 <- beforeNetworkInfo$myDegreeAverageSource3And4
    listOUT$beforeDegreeAverageSourceOnly3 <- beforeNetworkInfo$myDegreeAverageSourceOnly3
    listOUT$beforeDegreeCentrality <- beforeNetworkInfo$myDegreeCentrality
    listOUT$beforeDegreeMax <- beforeNetworkInfo$myDegreeMax
    listOUT$beforeDegreeVariance <- beforeNetworkInfo$myDegreeVariance
    listOUT$beforeDegreeStandardDeviation <- beforeNetworkInfo$myDegreeStandardDeviation
    listOUT$beforeDensity <- beforeNetworkInfo$myDensity
    listOUT$beforeRowCount <- beforeNetworkInfo$myRowCount
    listOUT$beforeSourceCount3And4 <- beforeNetworkInfo$mySourceCount3And4
    listOUT$beforeSourceCountOnly3 <- beforeNetworkInfo$mySourceCountOnly3
    listOUT$beforeTransitivity <- beforeNetworkInfo$myTransitivity
    
    #--------------------------------------------------------------------------#
    # process after network
    afterNetworkInfo <- NetworkInfo( debugFlagIN = debugFlagIN )
    afterNetworkInfo$initFromTabData(
        afterDataDirectoryIN,
        afterFileIN
    )
    afterNetworkInfo$processNetwork()
    
    # add after information to the list
    listOUT$afterAuthorCount2And4 <- afterNetworkInfo$myAuthorCount2And4
    listOUT$afterAuthorCountOnly2 <- afterNetworkInfo$myAuthorCountOnly2
    listOUT$afterBetweennessCentrality <- afterNetworkInfo$myBetweennessCentrality
    listOUT$afterConnectedness <- afterNetworkInfo$myConnectedness
    listOUT$afterColumnCount <- afterNetworkInfo$myColumnCount
    listOUT$afterDataFileName <- afterNetworkInfo$myDataFileName
    listOUT$afterDataPath <- afterNetworkInfo$myDataPath
    listOUT$afterDegreeAverage <- afterNetworkInfo$myDegreeAverage
    listOUT$afterDegreeAverageAuthor2And4 <- afterNetworkInfo$myDegreeAverageAuthor2And4
    listOUT$afterDegreeAverageAuthorOnly2 <- afterNetworkInfo$myDegreeAverageAuthorOnly2
    listOUT$afterDegreeAverageSource3And4 <- afterNetworkInfo$myDegreeAverageSource3And4
    listOUT$afterDegreeAverageSourceOnly3 <- afterNetworkInfo$myDegreeAverageSourceOnly3
    listOUT$afterDegreeCentrality <- afterNetworkInfo$myDegreeCentrality
    listOUT$afterDegreeMax <- afterNetworkInfo$myDegreeMax
    listOUT$afterDegreeVariance <- afterNetworkInfo$myDegreeVariance
    listOUT$afterDegreeStandardDeviation <- afterNetworkInfo$myDegreeStandardDeviation
    listOUT$afterDensity <- afterNetworkInfo$myDensity
    listOUT$afterRowCount <- afterNetworkInfo$myRowCount
    listOUT$afterSourceCount3And4 <- afterNetworkInfo$mySourceCount3And4
    listOUT$afterSourceCountOnly3 <- afterNetworkInfo$mySourceCountOnly3
    listOUT$afterTransitivity <- afterNetworkInfo$myTransitivity
    
    #--------------------------------------------------------------------------#
    # correlate before and after degree and binary degree vectors

    # degree vector correlation
    beforeDegreeVector <- beforeNetworkInfo$myDegreeVector
    afterDegreeVector <- afterNetworkInfo$myDegreeVector
    degreeCorrelation <- cor( beforeDegreeVector, afterDegreeVector )
    
    # degree vector percent agreement
    # - for irr::agree(), each column is a set of values that you want to
    #     compare (so, create matrix using cbind to combine lists as columns).
    workMatrix <- cbind( beforeDegreeVector, afterDegreeVector )
    agreeOutput <- irr::agree( workMatrix )
    degreePercentAgree <- agreeOutput$value

    # binary degree vector correlation
    beforeBinaryDegreeVector <- beforeNetworkInfo$myBinaryDegreeVector
    afterBinaryDegreeVector <- afterNetworkInfo$myBinaryDegreeVector
    binaryDegreeCorrelation <- cor( beforeBinaryDegreeVector, afterBinaryDegreeVector )
    
    # binary degree vector percent agreement
    # - for irr::agree(), each column is a set of values that you want to
    #     compare (so, create matrix using cbind to combine lists as columns).
    workMatrix <- cbind( beforeBinaryDegreeVector, afterBinaryDegreeVector )
    agreeOutput <- irr::agree( workMatrix )
    binaryDegreePercentAgree <- agreeOutput$value
    
    # add them to list.
    listOUT$degreeCorrelation <- degreeCorrelation
    listOUT$degreePercentAgree <- degreePercentAgree
    listOUT$binaryDegreeCorrelation <- binaryDegreeCorrelation
    listOUT$binaryDegreePercentAgree <- binaryDegreePercentAgree
    
    #--------------------------------------------------------------------------#
    # get matrices from each and compare.
    beforeMatrix <- beforeNetworkInfo$myNetworkMatrix
    afterMatrix <- afterNetworkInfo$myNetworkMatrix

    # call compare method
    matrixComparison <- compareMatricesQAP(
        beforeMatrix,
        afterMatrix,
        outputPrefixIN = labelIN,
        outputPlotsIN = FALSE,
        debugFlagIN = debugFlagIN,
        repsIN = 10,
        doQapIN = FALSE )

    # retrieve and store individual values.
    graphCorrelation <- matrixComparison$graphCorrelation
    graphCorrelationQAPResult <- matrixComparison$qapGcorResult
    graphCovariance <- matrixComparison$graphCovariance
    graphCovarianceQAPResult <- matrixComparison$qapGcovResult
    graphHammingDistance <- matrixComparison$graphHammingDist
    graphHammingDistanceQAPResult <- matrixComparison$qapHdistResult
    
    # add them to list.
    listOUT$graphCorrelation <- graphCorrelation
    listOUT$graphCovariance <- graphCovariance
    listOUT$graphHammingDistance <- graphHammingDistance

    #--------------------------------------------------------------------------#
    # get binary matrices from each and compare.
    beforeBinMatrix = beforeNetworkInfo$getBinaryNetworkMatrix()
    afterBinMatrix = afterNetworkInfo$getBinaryNetworkMatrix()
    
    # call compare method
    binMatrixComparison <- compareMatricesQAP(
        beforeBinMatrix,
        afterBinMatrix,
        outputPrefixIN = labelIN,
        outputPlotsIN = FALSE,
        debugFlagIN = debugFlagIN,
        repsIN = 10,
        doQapIN = FALSE )
    
    # retrieve and store individual values.
    binGraphCorrelation <- binMatrixComparison$graphCorrelation
    binGraphCorrelationQAPResult <- binMatrixComparison$qapGcorResult
    binGraphCovariance <- binMatrixComparison$graphCovariance
    binGraphCovarianceQAPResult <- binMatrixComparison$qapGcovResult
    binGraphHammingDistance <- binMatrixComparison$graphHammingDist
    binGraphHammingDistanceQAPResult <- binMatrixComparison$qapHdistResult
    
    # add them to list.
    listOUT$binGraphCorrelation <- binGraphCorrelation
    listOUT$binGraphCovariance <- binGraphCovariance
    listOUT$binGraphHammingDistance <- binGraphHammingDistance

    # debug?
    if ( debugFlagIN == TRUE ){
        
        # DEBUG - push the before and after NetworkInfo instances up into
        #     parent environment.
        #myTimeStamp <- format( Sys.time(), format = "%Y-%m-%d_%H-%M-%S" )
        debugLatestBeforeNetInfo <<- beforeNetworkInfo
        debugLatestAfterNetInfo <<- afterNetworkInfo
        
    } else {
        
        # not DEBUG - cleanup
        rm( beforeNetworkInfo )
        rm( afterNetworkInfo )
        rm( matrixComparison )
        rm( binMatrixComparison )
        gc()
    
    }

    # return list
    return( listOUT )
    
} #-- END function processBeforeAfterNetworks() --#

message( paste( "Function processBeforeAfterNetworks defined @ ", date(), sep = "" ) )


# NOTE: this function is moved to NetworkInfoOuttakes.r. It is only necessary if
#     you have old data that doesn't include binary comparison. if you are
#     making new data, binary comparison is included in
#     processBeforeAfterNetworks().
#beforeAfterBinaryNetworks <- function(
#        beforeDataDirectoryIN,
#        beforeFileIN,
#        afterDataDirectoryIN,
#        afterFileIN,
#        dateIN,
#        networkDurationIN,
#        labelIN,
#        debugFlagIN = FALSE ) {
    
    # Accepts path info for before and after network data. Loads each then
    #     gets binary network matrices and compares them
    #     to create correlation and other information about how the pair of
    #     networks compare, then packages all in a list with common column names
    #     to be included in a data.frame of information about a series of
    #     pairs of data.
    # NOTE: this only needs to be called if you just want binary network
    #     analysis - this binary network analysis is also included in
    #     processBeforeAfterNetworks().
