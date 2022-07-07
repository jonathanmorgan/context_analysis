# ReferenceClass NetworkInfo
# - for help: `help( ReferenceClasses )`
# - https://www.rdocumentation.org/packages/methods/versions/3.6.2/topics/ReferenceClasses

# NOTE: this is only necessary if you have old data that doesn't include
#     binary comparison. if you are making new data, binary comparison is
#     included in processBeforeAfterNetworks().
beforeAfterBinaryNetworks <- function(
        beforeDataDirectoryIN,
        beforeFileIN,
        afterDataDirectoryIN,
        afterFileIN,
        dateIN,
        networkDurationIN,
        labelIN,
        debugFlagIN = FALSE ) {
    
    # Accepts path info for before and after network data. Loads each then
    #     gets binary network matrices and compares them
    #     to create correlation and other information about how the pair of
    #     networks compare, then packages all in a list with common column names
    #     to be included in a data.frame of information about a series of
    #     pairs of data.
    # NOTE: this only needs to be called if you just want binary network
    #     analysis - this binary network analysis is also included in
    #     processBeforeAfterNetworks().
    
    # return reference
    listOUT <- list()
    
    # declare variables
    beforeNetworkInfo <- NULL
    beforeBinMatrix <- NULL
    afterNetworkInfo <- NULL
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

    # add before information to the list
    listOUT$beforeColumnCount <- beforeNetworkInfo$myColumnCount
    listOUT$beforeDataFileName <- beforeNetworkInfo$myDataFileName
    listOUT$beforeDataPath <- beforeNetworkInfo$myDataPath
    listOUT$beforeRowCount <- beforeNetworkInfo$myRowCount

    #--------------------------------------------------------------------------#
    # process after network
    afterNetworkInfo <- NetworkInfo( debugFlagIN = debugFlagIN )
    afterNetworkInfo$initFromTabData(
        afterDataDirectoryIN,
        afterFileIN
    )

    # add after information to the list
    listOUT$afterColumnCount <- afterNetworkInfo$myColumnCount
    listOUT$afterDataFileName <- afterNetworkInfo$myDataFileName
    listOUT$afterDataPath <- afterNetworkInfo$myDataPath
    listOUT$afterRowCount <- afterNetworkInfo$myRowCount

    #--------------------------------------------------------------------------#
    # get binary matrices from each and compare.
    beforeBinMatrix <- beforeNetworkInfo$getBinaryNetworkMatrix()
    afterBinMatrix <- afterNetworkInfo$getBinaryNetworkMatrix()
    
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
    
    # cleanup
    rm( beforeNetworkInfo )
    rm( afterNetworkInfo )
    rm( binMatrixComparison )
    gc()
    
    # return list
    return( listOUT )
    
} #-- END function beforeAfterBinaryNetworks() --#

message( paste( "Function beforeAfterBinaryNetworks defined @ ", date(), sep = "" ) )
