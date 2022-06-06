#==============================================================================#
# Imports
#==============================================================================#


#==============================================================================#
# Functions
#==============================================================================#


calcAuthorCount <- function( dataFrameIN, includeBothIN = TRUE ) {

    # Function calcAuthorCount()
    #
    # Filters data frame to just authors using dataFrameIN$person_type (2 or 4),
    #    then counts rows and returns that count.
    #
    # preconditions: data frame passed in must have $person_type column.

    # return reference
    valueOUT <- -1

    # declare variables
    authorDF <- NULL

    # filter data frame
    authorDF <- getAuthorDF( dataFrameIN, includeBothIN = includeBothIN )

    # calculate mean of $degree column.
    valueOUT <- nrow( authorDF )

    # return value
    return( valueOUT )

} #-- END function calcAuthorMeanDegree() --#


calcAuthorMeanDegree <- function( dataFrameIN, includeBothIN = TRUE ) {

    # Function calcAuthorMeanDegree()
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
    authorDF <- getAuthorDF( dataFrameIN, includeBothIN = includeBothIN )

    # calculate mean of $degree column.
    valueOUT <- mean( authorDF$degree )

    # return value
    return( valueOUT )

} #-- END function calcAuthorMeanDegree() --#


calcSourceCount <- function( dataFrameIN, includeBothIN = TRUE ) {

    # Function calcSourceCount()
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
    sourceDF <- getSourceDF( dataFrameIN, includeBothIN = includeBothIN )

    # calculate mean of $degree column.
    valueOUT <- nrow( sourceDF )

    # return value
    return( valueOUT )

} #-- END function calcSourceCount() --#


calcSourceMeanDegree <- function( dataFrameIN, includeBothIN = TRUE ) {

    # Function calcSourceMeanDegree()
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
    sourceDF <- getSourceDF( dataFrameIN, includeBothIN = includeBothIN )

    # calculate mean of $degree column.
    valueOUT <- mean( sourceDF$degree )

    # return value
    return( valueOUT )

} #-- END function calcSourceMeanDegree() --#


calculateListMean <- function( listIN, minValueToIncludeIN = NULL, excludeNaNIN = TRUE ) {

    # Function: calculateListMean()
    #
    # Accepts column/vector to get mean for and optional minimum value we want
    #    included in the calculation (so you can only look at values greater
    #    than 0, for example, or 10).  Filters column/vector to just contain
    #    values that meet filter criteria, then call mean().
    #
    # Returns the mean.

    # return reference
    valueOUT <- NULL

    # declare variables
    workingList <- NULL
    listLength <- -1

    # check to see if min value is set.
    if ( !is.null( minValueToIncludeIN ) ) {

        # we have a minimum value.  Filter out all entries in column/vector that
        #    are less than that value.
        workingList <- listIN[ listIN >= minValueToIncludeIN ]

    } else {

        # no minimum value.  Just use column/vector passed in.
        workingList <- as.vector( listIN, mode = "numeric" )

    }

    # anything in list?
    listLength <- length( workingList )
    if ( listLength > 0 ) {

        # yes. calculate mean on working list.
        valueOUT <- mean( workingList, na.rm = excludeNaNIN )

    } else {

        # no - return...?
        valueOUT <- 0

    }

    # return value
    return( valueOUT )

} #-- END function calculateListMean


calculateListMax <- function( listIN, excludeNaNIN = TRUE ) {

    # Function: calculateListMean()
    #
    # Accepts column/vector to get max value from.  Filters column/vector to
    #    just contain values that meet filter criteria, then call max().
    #
    # Returns the mean.

    # return reference
    valueOUT <- NULL

    # declare variables
    workingList <- NULL
    listLength <- -1
    
    # no minimum value.  Just use column/vector passed in.
    workingList <- as.vector( listIN, mode = "numeric" )

    # anything in list?
    listLength <- length( workingList )
    if ( listLength > 0 ) {

        # yes. calculate max on working list.
        valueOUT <- max( workingList, na.rm = excludeNaNIN )

    } else {

        # no - return...?
        valueOUT <- 0

    }

    # return value
    return( valueOUT )

} #-- END function calculateListMax


getAuthorDF <- function( dataFrameIN, includeBothIN = TRUE ) {

    # Function getAuthorDF()
    #
    # Filters data frame to just authors using dataFrameIN$person_type (2 or 4),
    #     returns resulting data.frame.
    #
    # preconditions: data frame passed in must have $person_type and $degree
    #    columns.

    # return reference
    authorDFOUT <- NULL

    # filter data frame
    authorDFOUT <- dataFrameIN[ dataFrameIN$person_type == 2 | dataFrameIN$person_type == 4, ]

    # include both?
    if ( includeBothIN == FALSE ){

        # don't include both - just person_type = 2.
        authorDFOUT <- authorDFOUT[ authorDFOUT$person_type == 2, ]

    }

    # return value
    return( authorDFOUT )

} #-- END function getAuthorDF() --#


getSourceDF <- function( dataFrameIN, includeBothIN = TRUE ) {

    # Function getSourceDF()
    #
    # Filters data frame to just sources using dataFrameIN$person_type (3 or 4),
    #     returns resulting data.frame.
    #
    # preconditions: data frame passed in must have $person_type and $degree
    #    columns.

    # return reference
    sourceDFOUT <- NULL

    # filter data frame
    sourceDFOUT <- dataFrameIN[ dataFrameIN$person_type == 3 | dataFrameIN$person_type == 4, ]

    # include both?
    if ( includeBothIN == FALSE ){

        # don't include both - just person_type = 3.
        sourceDFOUT <- sourceDFOUT[ sourceDFOUT$person_type == 3, ]

    }

    # return value
    return( sourceDFOUT )

} #-- END function getSourceDF() --#
