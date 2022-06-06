# ReferenceClass NetworkInfo
# - for help: `help( ReferenceClasses )`
# - https://www.rdocumentation.org/packages/methods/versions/3.6.2/topics/ReferenceClasses

#==============================================================================#
# imports
#==============================================================================#

library( sna )
library( statnet )

#==============================================================================#
# class definition
#==============================================================================#

networkInfo_fields <- list(
    myAuthorCount2And4 = "numeric",
    myAuthorCountOnly2 = "numeric",
    myBetweennessCentrality = "numeric",
    myConnectedness = "numeric",
    myBetweennessVector = "vector",
    myColumnCount = "integer",
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
    calcMyAuthorCount <- function( includeBothIN = TRUE ) {

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
    calcMyAuthorMeanDegree <- function( includeBothIN = TRUE ) {

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
    calcMySourceCount <- function( includeBothIN = TRUE ) {

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
    calcMySourceMeanDegree <- function( includeBothIN = TRUE ) {

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

        'preconditions: must have already called "createDegreeVector()".'
        
        # what is the average (mean) degree?
        myDegreeAverage <<- mean( myDegreeVector )

        if ( myDebugFlag == TRUE ){
            message( paste( "average degree = ", myDegreeAverage, sep = "" ) )
        }

        # subset vector to get only those that are above mean
        #testAboveMeanVector <- testDegreeVector[ testDegreeVector > testAvgDegree ]

        # average author degree (person types 2 and 4)
        myDegreeAverageAuthor2And4 <<- calcAuthorMeanDegree( dataFrameIN = myDataDF, includeBothIN = TRUE )

        if ( myDebugFlag == TRUE ){
            message( paste( "average author degree (2 and 4) = ", myDegreeAverageAuthor2And4, sep = "" ) )
        }

        # average author degree (person type 2 only)
        myDegreeAverageAuthorOnly2 <<- calcAuthorMeanDegree( dataFrameIN = myDataDF, includeBothIN = FALSE )

        if ( myDebugFlag == TRUE ){
            message( paste( "average author degree (only 2) = ", myDegreeAverageAuthorOnly2, sep = "" ) )
        }

        # average source degree (person types 3 and 4)
        myDegreeAverageSource3And4 <<- calcSourceMeanDegree( dataFrameIN = myDataDF, includeBothIN = TRUE )
        
        if ( myDebugFlag == TRUE ){
            message( paste( "average source degree (3 and 4) = ", myDegreeAverageSource3And4, sep = "" ) )
        }

        # average source degree (person type 3 only)
        myDegreeAverageSourceOnly3 <<- calcSourceMeanDegree( dataFrameIN = myDataDF, includeBothIN = FALSE )
        
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
    createDegreeVector = function() {

        # assuming that our statnet network object is in reference myNetworkStatnet

        # Use the degree function in the sna package to create vector of degree values
        #    for each node, then compute average.  Make sure to pass the gmode parameter to tell it that the
        #    graph is not directed (gmode = "graph", instead of "digraph").
        # Doc: http://www.inside-r.org/packages/cran/sna/docs/degree
        #degree_vector <- degree( test1_statnet, gmode = "graph" )

        # If you have other libraries loaded that also implement a degree function, you
        #    can also call this with package name:
        myDegreeVector <<- sna::degree( myNetworkStatnet, gmode = "graph" )
        
        # Take the degree and associate it with each node as a node attribute.
        #    (%v% is a shortcut for the get.vertex.attribute command)
        myNetworkStatnet %v% "degree" <<- myDegreeVector

        # also add degree vector to original data frame
        myDataDF$degree <<- myDegreeVector
        
    } #-- END method createDegreeVector() --#
)


NetworkInfo$methods(
    getMyAuthorDF <- function( includeBothIN = TRUE ) {

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
    getMySourceDF <- function( includeBothIN = TRUE ) {

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
        
        createDegreeVector()
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
    beforeMatrix <- NULL
    afterMatrix <- NULL
    matrixComparison <- NULL
    graphCorrelation <- matrixComparison$graphCorrelation
    graphCorrelationQAPResult <- matrixComparison$qapGcorResult
    graphCovariance <- matrixComparison$graphCovariance
    graphCovarianceQAPResult <- matrixComparison$qapGcovResult
    graphHammingDistance <- matrixComparison$graphHammingDist
    graphHammingDistanceQAPResult <- matrixComparison$qapHdistResult
    
    # store the date, network duration, and label
    listOUT$baseDate <- dateIN
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
    
    # TODO - add before information to the list
    listOUT$beforeBetweennessCentrality = beforeNetworkInfo$myBetweennessCentrality
    listOUT$beforeConnectedness = beforeNetworkInfo$myConnectedness
    listOUT$beforeColumnCount = beforeNetworkInfo$myColumnCount
    listOUT$beforeDataFileName = beforeNetworkInfo$myDataFileName
    listOUT$beforeDataPath = beforeNetworkInfo$myDataPath
    listOUT$beforeDegreeAverage = beforeNetworkInfo$myDegreeAverage
    listOUT$beforeDegreeAverageAuthor2And4 = beforeNetworkInfo$myDegreeAverageAuthor2And4
    listOUT$beforeDegreeAverageAuthorOnly2 = beforeNetworkInfo$myDegreeAverageAuthorOnly2
    listOUT$beforeDegreeAverageSource3And4 = beforeNetworkInfo$myDegreeAverageSource3And4
    listOUT$beforeDegreeAverageSourceOnly3 = beforeNetworkInfo$myDegreeAverageSourceOnly3
    listOUT$beforeDegreeCentrality = beforeNetworkInfo$myDegreeCentrality
    listOUT$beforeDegreeMax = beforeNetworkInfo$myDegreeMax
    listOUT$beforeDegreeVariance = beforeNetworkInfo$myDegreeVariance
    listOUT$beforeDegreeStandardDeviation = beforeNetworkInfo$myDegreeStandardDeviation
    listOUT$beforeDensity = beforeNetworkInfo$myDensity
    listOUT$beforeRowCount = beforeNetworkInfo$myRowCount
    listOUT$beforeTransitivity = beforeNetworkInfo$myTransitivity
    
    #--------------------------------------------------------------------------#
    # process after network
    afterNetworkInfo <- NetworkInfo( debugFlagIN = debugFlagIN )
    afterNetworkInfo$initFromTabData(
        afterDataDirectoryIN,
        afterFileIN
    )
    afterNetworkInfo$processNetwork()
    
    # TODO - add after information to the list
    listOUT$afterBetweennessCentrality = afterNetworkInfo$myBetweennessCentrality
    listOUT$afterConnectedness = afterNetworkInfo$myConnectedness
    listOUT$afterColumnCount = afterNetworkInfo$myColumnCount
    listOUT$afterDataFileName = afterNetworkInfo$myDataFileName
    listOUT$afterDataPath = afterNetworkInfo$myDataPath
    listOUT$afterDegreeAverage = afterNetworkInfo$myDegreeAverage
    listOUT$afterDegreeAverageAuthor2And4 = afterNetworkInfo$myDegreeAverageAuthor2And4
    listOUT$afterDegreeAverageAuthorOnly2 = afterNetworkInfo$myDegreeAverageAuthorOnly2
    listOUT$afterDegreeAverageSource3And4 = afterNetworkInfo$myDegreeAverageSource3And4
    listOUT$afterDegreeAverageSourceOnly3 = afterNetworkInfo$myDegreeAverageSourceOnly3
    listOUT$afterDegreeCentrality = afterNetworkInfo$myDegreeCentrality
    listOUT$afterDegreeMax = afterNetworkInfo$myDegreeMax
    listOUT$afterDegreeVariance = afterNetworkInfo$myDegreeVariance
    listOUT$afterDegreeStandardDeviation = afterNetworkInfo$myDegreeStandardDeviation
    listOUT$afterDensity = afterNetworkInfo$myDensity
    listOUT$afterRowCount = afterNetworkInfo$myRowCount
    listOUT$afterTransitivity = afterNetworkInfo$myTransitivity
    
    #--------------------------------------------------------------------------#
    # get matrices from each and compare.
    beforeMatrix = beforeNetworkInfo$myNetworkMatrix
    afterMatrix = afterNetworkInfo$myNetworkMatrix

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

    # cleanup
    rm( beforeNetworkInfo )
    rm( afterNetworkInfo )
    rm( matrixComparison )
    gc()

    # return list
    return( listOUT )
    
} #-- END function processBeforeAfterNetworks() --#

message( paste( "Function processBeforeAfterNetworks defined @ ", date(), sep = "" ) )
