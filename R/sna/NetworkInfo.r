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
    myBetweennessCentrality = "numeric",
    myConnectedness = "numeric",
    myBetweennessVector = "vector",
    myColumnCount = "integer",
    myDataDF = "data.frame",
    myDataFileName = "character",
    myDataPath = "character",
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
    myTransitivity = "numeric"
)

NetworkInfo <- setRefClass(
    "NetworkInfo",
    fields = networkInfo_fields
)

NetworkInfo$methods(
    calculateDegreeAverages = function() {

        'preconditions: must have already called "createDegreeVector()".'
        
        # what is the average (mean) degree?
        myDegreeAverage <<- mean( myDegreeVector )
        message( paste( "average degree = ", myDegreeAverage, sep = "" ) )

        # subset vector to get only those that are above mean
        #testAboveMeanVector <- testDegreeVector[ testDegreeVector > testAvgDegree ]

        # average author degree (person types 2 and 4)
        myDegreeAverageAuthor2And4 <<- calcAuthorMeanDegree( dataFrameIN = myDataDF, includeBothIN = TRUE )
        message( paste( "average author degree (2 and 4) = ", myDegreeAverageAuthor2And4, sep = "" ) )

        # average author degree (person type 2 only)
        myDegreeAverageAuthorOnly2 <<- calcAuthorMeanDegree( dataFrameIN = myDataDF, includeBothIN = FALSE )
        message( paste( "average author degree (only 2) = ", myDegreeAverageAuthorOnly2, sep = "" ) )

        # average source degree (person types 3 and 4)
        myDegreeAverageSource3And4 <<- calcSourceMeanDegree( dataFrameIN = myDataDF, includeBothIN = TRUE )
        message( paste( "average source degree (3 and 4) = ", myDegreeAverageSource3And4, sep = "" ) )

        # average source degree (person type 3 only)
        myDegreeAverageSourceOnly3 <<- calcSourceMeanDegree( dataFrameIN = myDataDF, includeBothIN = FALSE )
        message( paste( "average source degree (only 3) = ", myDegreeAverageSourceOnly3, sep = "" ) )

        # what is the standard deviation of the degrees?
        myDegreeStandardDeviation <<- sd( myDegreeVector )
        message( paste( "degree SD = ", myDegreeStandardDeviation, sep = "" ) )

        # what is the variance of the degrees?
        myDegreeVariance <<- var( myDegreeVector )
        message( paste( "degree variance = ", myDegreeVariance, sep = "" ) )

        # what is the max value among the degrees?
        myDegreeMax <<- max( myDegreeVector )
        message( paste( "degree max = ", myDegreeMax, sep = "" ) )

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
        message( paste( "degree centrality = ", myDegreeCentrality, sep = "" ) )

        # graph-level betweenness centrality
        myBetweennessCentrality <<- sna::centralization( myNetworkStatnet, sna::betweenness, mode = "graph", cmode = "undirected" )
        message( paste( "betweenness centrality = ", myBetweennessCentrality, sep = "" ) )

        # graph-level connectedness
        myConnectedness <<- sna::connectedness( myNetworkStatnet )
        message( paste( "connectedness = ", myConnectedness, sep = "" ) )

        # graph-level transitivity
        myTransitivity <<- sna::gtrans( myNetworkStatnet, mode = "graph" )
        message( paste( "transitivity = ", myTransitivity, sep = "" ) )

        # graph-level density
        myDensity <<- sna::gden( myNetworkStatnet, mode = "graph" )
        message( paste( "density = ", myDensity, sep = "" ) )

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
    initFromTabData = function( dataDirPathIN, fileNameIN ) {

        'Accepts data directory and file name, combines them into path,
         loads them into data frame, then makes all the other objects
         we need.'

        # declare variables
        myDataFolder <- NULL
        
        # initialize variables
        myDataFolder <- dataDirPathIN
        myDataFileName <<- fileNameIN
        myDataPath <<- paste( myDataFolder, "/", myDataFile, sep = "" )

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