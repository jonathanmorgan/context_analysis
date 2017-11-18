from __future__ import unicode_literals

# python package imports
import six

# django imports
from django.contrib.auth.models import User

# sourcenet imports
from sourcenet.models import Article
from sourcenet.models import Article_Data
from sourcenet.models import Person

# sourcenet_analysis imports
from sourcenet_analysis.models import Reliability_Ties
from sourcenet_analysis.reliability.reliability_names_builder import ReliabilityNamesBuilder

#-------------------------------------------------------------------------------
# class definitions
#-------------------------------------------------------------------------------


class NetworkPersonInfo( ReliabilityNamesBuilder ):
    
    '''
    Creates data structured as follows, in self.coder_index_to_data_map:

    - self.coder_index_to_data_map - map of coder index to coder data.  Data for each coder is in a dictionary with the following keys:

        - self.PROP_CODER_AUTHOR_DATA = "coder_author_data" - maps to dictionary that maps author IDs of all authors the coder found in the set of articles processed by this class to a dictionary of information on each author.  Author info dictionary includes:

            - self.PROP_AUTHOR_SHARED_SOURCE_INFO = "author_shared_source_info" - refers to dictionary that maps source ID to source information for sources quoted by the author who were also quoted by other authors.  For each source, the source info dictionary contains:

                - self.PROP_SHARED_SOURCE_ID = "shared_source_id" - ID of source.
                - self.PROP_SHARED_SOURCE_AUTHOR_LIST = "shared_source_author_list" - list of authors who quoted the source.

            - self.PROP_AUTHOR_SHARED_SOURCE_AUTHORS_LIST = "author_shared_source_authors_list" - list of authors who quoted any one or more sources that the current author also quoted.
            - self.PROP_AUTHOR_SOURCE_COUNT = "author_source_count" - count of sources for the author (length of source list above).
            - self.PROP_AUTHOR_SHARED_SOURCE_COUNT = "author_shared_source_count" - count of shared sources (length of shared source info dictionary above).
            - self.PROP_AUTHOR_ARTICLE_ID_LIST = "author_article_id_list" - list of ids of articles written by author included in analysis.

        - self.PROP_CODER_SOURCE_DATA = "coder_source_data" - maps to dictionary that maps source IDs of all sources the coder found in the set of articles processed by this class to a dictionary of information on each source.  Source info dictionary includes:
        
            - self.PROP_SOURCE_AUTHOR_LIST = "source_author_list" - for each source, a list of the authors who quoted that source.
            
        - self.PROP_CODER_AUTHOR_ID_LIST = "coder_author_id_list" - list of IDs of authors this coder found.
        - self.PROP_CODER_AUTHOR_SOURCE_COUNT_LIST = "coder_author_source_count_list" - list of source counts per author, in same order as list of author IDs.
        - self.PROP_CODER_AUTHOR_SHARED_COUNT_LIST = "coder_author_shared_count_list" - list of shared source counts per author, in same order as list of author IDs.
        - self.PROP_CODER_AUTHOR_ARTICLE_COUNT_LIST = "coder_author_article_count_list" - list of counts of articles in this analysis for each author.
    '''
        
    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    

    
    # Logger name
    LOGGER_NAME = "sourcenet_analysis.network.network_person_info"

    # retrieving reliability row fields by name
    COLUMN_NAME_PREFIX_CODER = "coder"
    COLUMN_NAME_SUFFIX_MENTION_COUNT = "_mention_count"
    COLUMN_NAME_SUFFIX_ID_LIST = "_id_list"
    
    # person types
    PERSON_TYPE_AUTHOR = Reliability_Ties.PERSON_TYPE_AUTHOR
    PERSON_TYPE_SOURCE = Reliability_Ties.PERSON_TYPE_SOURCE
    
    # information about table.
    TABLE_MAX_CODERS = 3
    
    # coder data property names
    PROP_CODER_AUTHOR_DATA = "coder_author_data"
    PROP_CODER_SOURCE_DATA = "coder_source_data"
    PROP_CODER_AUTHOR_ID_LIST = "coder_author_id_list"
    PROP_CODER_AUTHOR_SOURCE_COUNT_LIST = "coder_author_source_count_list"
    PROP_CODER_AUTHOR_SHARED_COUNT_LIST = "coder_author_shared_count_list"
    PROP_CODER_AUTHOR_ARTICLE_COUNT_LIST = "coder_author_article_count_list"

    # author property names
    PROP_AUTHOR_SOURCE_LIST = "author_source_list"
    PROP_AUTHOR_SHARED_SOURCE_INFO = "author_shared_source_info"
    PROP_AUTHOR_SHARED_SOURCE_AUTHORS_LIST = "author_shared_source_authors_list"
    PROP_AUTHOR_SOURCE_COUNT = "author_source_count"
    PROP_AUTHOR_SHARED_SOURCE_COUNT = "author_shared_source_count"
    PROP_AUTHOR_ARTICLE_ID_LIST = "author_article_id_list"
    
    # shared source property names
    PROP_SHARED_SOURCE_ID = "shared_source_id"
    PROP_SHARED_SOURCE_AUTHOR_LIST = "shared_source_author_list"

    # source property names
    PROP_SOURCE_AUTHOR_LIST = "source_author_list"
    
    # DEBUG
    DEBUG = False

    
    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # ! ==> call parent's __init__()
        super( NetworkPersonInfo, self ).__init__()
        
        # variables to filter reliability row lookup.
        self.reliability_row_label = ""
        
        # variable to hold desired automated coder type
        #self.limit_to_automated_coder_type = ""
        
        # coder index to data map.
        self.coder_index_to_data_map = {}
        
    #-- END method __init__() --#
    

    def get_article_data_for_index( self, index_IN, article_data_qs_IN ):
        
        '''
        Accepts index and article_data QuerySet. Gets prioritized coder list for
            index passed in, then goes in order through the list, returning the
            Article_Data of the first user in the list that has an Article_Data
            record.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        prioritized_coder_list = None
        got_article_data = None
        current_coder = None
        
        # get prioritized coder list for index.
        prioritized_coder_list = self.get_coders_for_index( index_IN )
        
        # loop
        got_article_data = False
        for current_coder in prioritized_coder_list:
        
            if ( got_article_data == False ):
        
                # see if coder has an Article_Data record for current article.
                try:
                
                    # try to get the article data for coder.
                    instance_OUT = article_data_qs_IN.get( coder = current_coder )
                    
                    # no exception - got it!
                    got_article_data = True
                    
                    # Now what?
                
                except Article_Data.DoesNotExist as addne:
                
                    # no article data.  Keep it false.
                    got_article_data = False
                
                #-- END try/except around .get()
                
            #-- END check to see if already have article data. --#
            
        #-- END loop over prioritized coder list. --#
        
        return instance_OUT
        
    #-- END function get_article_data_for_index --#
        
    
    def get_index_author_data( self, index_IN ):
        
        '''
        Accepts an index value.  Uses it to get author data associated with
            that index, and returns data dictionary.  If none found, creates
            empty dictionary, stores it for the index, then returns it.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        me = "get_index_author_data"

        # call method to retrieve data
        instance_OUT = self.get_index_data_property_dict( index_IN, self.PROP_CODER_AUTHOR_DATA )
        
        return instance_OUT        
        
    #-- END method get_index_author_data() --#
    
        
    def get_index_data( self, index_IN ):
        
        '''
        Accepts an index value.  Uses it to get data associated with that
            index, and returns data dictionary.  If none found, creates empty
            dictionary, stores it for the index value, then returns it.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        me = "get_index_data"
        coder_index_to_data_dict = {}
        coder_user_id = -1
        coder_id_to_index_dict = {}
        coder_index = -1
        
        # make sure we have an index value instance passed in.
        coder_index = index_IN
        if ( ( coder_index is not None ) and ( coder_index > 0 ) ):
        
            # get map from instance
            coder_index_to_data_dict = self.coder_index_to_data_map
                        
            # Get instance from coder_index_to_data_dict.
            instance_OUT = coder_index_to_data_dict.get( coder_index, None )
            
            # got one?
            if ( instance_OUT is None ):
            
                # no - need to make new dictionary, store it for user, then
                #    return it.
                instance_OUT = {}
                instance_OUT[ self.PROP_CODER_AUTHOR_DATA ] = {}
                instance_OUT[ self.PROP_CODER_SOURCE_DATA ] = {}
                coder_index_to_data_dict[ coder_index ] = instance_OUT
                
            #-- END check to see if coder already has data. --#
                
        else:
        
            # no index, should be at this point - return None.
            instance_OUT = None
            print( "ERROR - In " + me + ": no index passed in." )       
        
        # -- END check to see if index passed in. --#
            
        return instance_OUT        
        
    #-- END method get_index_data() --#
    
        
    def get_index_data_property_dict( self, index_IN, prop_name_IN ):
        
        '''
        Accepts an index number.  Uses it to get data associated with that
           index, and returns data dictionary.  If none found, creates empty
           dictionary, stores it for the index value, then returns it.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        me = "get_index_data_property_dict"
        coder_user_id = -1
        coder_data_dict = {}
        
        # make sure we have an index passed in...
        if ( index_IN is not None ):
        
            # ...and a property name.
            if ( ( prop_name_IN is not None ) and ( prop_name_IN != "" ) ):
        
                # Get index's data dictionary.
                index_data_dict = self.get_index_data( index_IN )
                
                # retrieve the index's source data.
                instance_OUT = index_data_dict.get( prop_name_IN, None )
                
                # got one?
                if ( instance_OUT is None ):
                
                    # no - need to make new dictionary, store it and return it.
                    instance_OUT = {}
                    index_data_dict[ prop_name_IN ] = instance_OUT
                    
                #-- END check to see if index already has data. --#
                    
                if ( self.DEBUG == True ):
                    print( "++++ In " + me + ": found " + prop_name_IN + " data for index " + str( index_IN ) )
                #-- END DEBUG --#
            
            #-- END check to see if we have property name passed in. --#
        
        #-- END check to see if we have a Coder instance passed in. --#
        
        return instance_OUT        
        
    #-- END method get_index_data_property_dict() --#
    
        
    def get_index_source_data( self, index_IN ):
        
        '''
        Accepts an index value.  Uses it to get source data associated with
            that index, and returns data dictionary.  If none found, creates
            empty dictionary, stores it for the index, then returns it.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        me = "get_source_data_for_index"

        # call method to retrieve data
        instance_OUT = self.get_index_data_property_dict( index_IN, self.PROP_CODER_SOURCE_DATA )
                
        return instance_OUT        
        
    #-- END method get_index_source_data() --#
    
        
    def process_articles( self, tag_list_IN = [] ):

        '''
        Grabs articles with a tag in tag_list_IN.  For each, loops through their
           Article_Data to update a dictionary that maps authors to author info,
           sources cited in articles, and counts of the number of articles in
           the selected set that mention each source, as coded by one to three
           different coders.
        '''
        
        # declare variables - retrieving reliability sample.
        me = "process_articles"
        article_qs = None
        article_count = -1
        current_article = None
        article_data_qs = None
        article_data_count = -1
        article_data_counter = -1
        
        # get article data for article and index based on priority.
        prioritized_coder_list = None
        current_coder = None
        got_article_data = None
        
        # declare variables - compiling information for articles.
        article_id = -1
        author_to_source_info_dict = None
        current_article_data = None
        coder_index = -1
        coder_1_article_data = None
        coder_2_article_data = None
        coder_3_article_data = None

        #-------------------------------------------------------------------------------
        # process articles to build data
        #-------------------------------------------------------------------------------
        
        # got a tag list?
        if ( ( tag_list_IN is not None ) and ( len( tag_list_IN ) > 0 ) ):

            # get articles with tags in list passed in.
            article_qs = Article.objects.filter( tags__name__in = tag_list_IN )
            
        #-- END check to see if tag list --#
        
        article_qs = article_qs.order_by( "id" )
        
        #article_qs = article_qs[ : 2 ]
            
        # loop over the articles.
        article_data_counter = 0
        for current_article in article_qs:
        
            # initialize variables
            article_coder_id_list = []
            author_info_dict = {}
            source_info_dict = {}
            coder_1_article_data = None
            coder_2_article_data = None
            coder_3_article_data = None
        
            # get article_id
            article_id = current_article.id
        
            # get article data for this article
            article_data_qs = current_article.article_data_set.all()
            
            # filter out certain automated coding types.
            article_data_qs = self.filter_article_data( article_data_qs )
            
            # how many Article_Data?
            article_data_count = len( article_data_qs )
        
            # DEBUG - output summary row.
            if ( self.DEBUG == True ):
                print( "- In " + me + ": Article ID = " + str( current_article.id ) + "; Article_Data count = " + str( article_data_count ) )
            #-- END DEBUG --#
            
            # for each article, make or update row in reliability table that
            #     matches the author and source, and label if one is specified
            #     in this object's instance (self.reliability_row_label).
            
            # get Article_Data for index 1
            coder_1_article_data = self.get_article_data_for_index( 1, article_data_qs )
            
            # get Article_Data for index 2
            coder_2_article_data = self.get_article_data_for_index( 2, article_data_qs )
            
            # get Article_Data for index 3
            coder_3_article_data = self.get_article_data_for_index( 3, article_data_qs )
            
            # compile information.
            
            # call process_relations for coder 1 if instance.
            if ( coder_1_article_data is not None ):

                if ( self.DEBUG == True ):
                    print( "\n\nIn " + me + ": article " + str( article_id ) + ", processing index 1\n" )
                #-- END DEBUG --#

                # call process_relations for index 1.
                self.process_relations( 1, coder_1_article_data )
                
            #-- END check to see if coder_1_article_data --#
            
            # call process_relations for coder 2 if instance.
            if ( coder_2_article_data is not None ):
            
                if ( self.DEBUG == True ):
                    print( "\n\nIn " + me + ": article " + str( article_id ) + ", processing index 2\n" )
                #-- END DEBUG --#
            
                # call process_relations for index 2.
                self.process_relations( 2, coder_2_article_data )
                
            #-- END check to see if coder_2_article_data --#
                        
            # call process_relations for coder 2 if instance.
            if ( coder_3_article_data is not None ):

                if ( self.DEBUG == True ):
                    print( "\n\nIn " + me + ": article " + str( article_id ) + ", processing index 3\n" )
                #-- END DEBUG --#

                # call process_relations for index 3.
                self.process_relations( 3, coder_3_article_data )
            
            #-- END check to see if coder_3_article_data --#
        
        #-- END loop over articles. --#
        
        # now, look over all the resulting data to update each coder's author
        #    data so it includes information on sources shared between authors.
        self.update_author_shared_sources()
        
        # finally, summarize data.
        self.summarize_data()
        
        # summary
        print( "" )

        if ( ( self.reliability_row_label is not None ) and ( self.reliability_row_label != "" ) ):
            print( "Assigned label " + self.reliability_row_label + " to created rows." )
        #-- END check to see if label set. --#
            
        article_count = article_qs.count()
        print( "Processed " + str( article_count ) + " Articles." )
        print( "Processed " + str( article_data_counter ) + " Article_Data records." )

    #-- END method process_articles() --#


    def process_relations( self, index_IN, article_data_IN ):
        
        '''
        Accepts Article_Data instance whose relations we need to process.  For
           each source, updates author and relation information.
        '''
        
        # return reference
        status_OUT = ""
        
        # declare variables
        me = "process_relations"
        article_id = -1
        article_data_coder = None
        article_author_qs = None
        article_source_qs = None
        current_author = None
        author_person = None
        author_info_dict = None
        current_source = None
        source_person = None
        
        # make sure we have an instance
        if ( article_data_IN is not None ):
        
            # get article ID.
            article_id = article_data_IN.article_id
            
            # Get coder info...
            article_data_coder = article_data_IN.coder
            
            # ... author QuerySet...
            article_author_qs = article_data_IN.article_author_set.all()
                        
            # ...and source QuerySet.
            article_source_qs = article_data_IN.get_quoted_article_sources_qs()
            
            # for each author...
            for current_author in article_author_qs:
            
                # get author person.
                author_person = current_author.person
                
                # update author article id list
                self.update_author_article_id_list( index_IN, author_person, article_id )
                    
                # update author info for each related source.
                for current_source in article_source_qs:
                
                    # get source person
                    source_person = current_source.person
                    
                    # call method to update author info.
                    self.update_author_info( author_person, source_person, index_IN )
                
                    # call method to update source info.
                    self.update_source_info( author_person, source_person, index_IN )
                    
                #-- END loop over sources --#

            #-- END check to see if QuerySet passed in. --#  
        
        #-- END check to see if Coder present --#
        
        return status_OUT
        
    #-- END method process_relations() --#


    def summarize_data( self ):
        
        '''
        Uses internal data to create summary information, for ease of analysis.
        
        Preconditions: assumes that all update_*() methods have been called
           already such that data is processed and ready to be summarized.
           
        Postconditions: updates coder, author, and source info dictionaries with
           summary information.
        '''
        
        # return reference
        status_OUT = None

        # declare variables
        me = "summarize_data"
        coder_index_to_data_dict = None
        coder_index = -1
        coder_data_dict = None
        coder_author_id_list = None
        coder_author_source_count_list = None
        coder_author_shared_count_list = None
        author_id = -1
        author_info = None
        source_list = None
        source_count = -1
        shared_source_info = None
        shared_source_count = -1
        article_count = -1
        author_article_id_list = None
        coder_author_article_count_list = None
        
        if ( self.DEBUG == True ):
            print( "" )
            print( "Start of " + me + "():" )
        #-- END DEBUG --#
        
        # get dict that holds map of coder index to coder data.
        coder_index_to_data_dict = self.coder_index_to_data_map
                
        # loop over the dictionary to process each coder/index.
        for coder_index, coder_data_dict in six.iteritems( coder_index_to_data_dict ):
        
            if ( self.DEBUG == True ):
                print( "Summarizing coder index " + str( coder_index ) )
            #-- END DEBUG --#
        
            # initialize data.
            coder_author_id_list = []
            coder_author_source_count_list = []
            coder_author_shared_count_list = []
            coder_author_article_count_list = []

            # retrieve author data dictionary.
            author_id_to_data_dict = coder_data_dict.get( self.PROP_CODER_AUTHOR_DATA, None )
            
            # loop over authors
            for author_id, author_info in six.iteritems( author_id_to_data_dict ):
        
                # initialize variables    
                source_list = None
                source_count = -1
                shared_source_info = None
                shared_source_count = -1
                
                # add id to ID list
                coder_author_id_list.append( author_id )
        
                # get source list...
                source_list = author_info.get( self.PROP_AUTHOR_SOURCE_LIST, None )
            
                # ...and shared source info from author data.
                shared_source_info = author_info.get( self.PROP_AUTHOR_SHARED_SOURCE_INFO, None )
                
                # get lengths and add to author info and appropriate lists.
                
                # source count
                source_count = 0
                if ( source_list is not None ):
                
                    # got a source list.
                    source_count = len( source_list )
                    
                #-- END check to see if list is None --#
                author_info[ self.PROP_AUTHOR_SOURCE_COUNT ] = source_count
                coder_author_source_count_list.append( source_count )
            
                # shared source count
                shared_source_count = 0
                if ( shared_source_info is not None ):

                    shared_source_count = len( shared_source_info )
                    
                #-- END check to see if dictionary is None --#
                author_info[ self.PROP_AUTHOR_SHARED_SOURCE_COUNT ] = shared_source_count
                coder_author_shared_count_list.append( shared_source_count )
                
                # get author's article count and add to coder list.
                author_article_id_list = author_info.get( self.PROP_AUTHOR_ARTICLE_ID_LIST, [] )
                article_count = len( author_article_id_list )
                coder_author_article_count_list.append( article_count )

                if ( self.DEBUG == True ):
                    print( "******** In " + me + "(): Summarizing coder index " + str( coder_index ) + "; author " + str( author_id ) + "; article ID list = " + str( author_article_id_list ) )
                #-- END DEBUG --#
            
            #-- END loop over authors. --#
            
            # add lists to coder's data.
            coder_data_dict[ self.PROP_CODER_AUTHOR_ID_LIST ] = coder_author_id_list
            coder_data_dict[ self.PROP_CODER_AUTHOR_SOURCE_COUNT_LIST ] = coder_author_source_count_list
            coder_data_dict[ self.PROP_CODER_AUTHOR_SHARED_COUNT_LIST ] = coder_author_shared_count_list
            coder_data_dict[ self.PROP_CODER_AUTHOR_ARTICLE_COUNT_LIST ] = coder_author_article_count_list
            
        #-- END loop over coders. --#
        
        return status_OUT
        
    #-- END method summarize_data --#


    def update_author_article_id_list( self, index_IN, author_person_IN, article_id_IN ):
        
        # return reference
        status_OUT = ""
        
        # declare variables
        me = "update_author_article_id_list"
        author_person_id = None
        source_person_id = None
        index_author_data_dict = None
        author_info_dict = None
        author_article_id_list = None
        
        # make sure we have an author person...
        if ( author_person_IN is not None ):
        
            # get ID
            author_person_id = author_person_IN.id
        
            # ...and an index.
            if ( ( index_IN is not None ) and ( index_IN > 0 ) ):
            
                # got everything we need.  Get data for the current index.
                index_author_data_dict = self.get_index_author_data( index_IN )
                
                # got something back?
                if ( index_author_data_dict is not None ):

                    # yes.  Get author info.
                    author_info_dict = index_author_data_dict.get( author_person_id, None )
                    
                    # got any?
                    if ( author_info_dict is None ):
                    
                        # no.  Add some.
                        author_info_dict = {}
                        author_info_dict[ self.PROP_AUTHOR_SOURCE_LIST ] = []
                        author_info_dict[ self.PROP_AUTHOR_ARTICLE_ID_LIST ] = []
                        index_author_data_dict[ author_person_id ] = author_info_dict
                        
                    #-- END check to see if author info present. --#
                    
                    # Should have one now.  Get list of articles by this author.
                    author_article_id_list = author_info_dict.get( self.PROP_AUTHOR_ARTICLE_ID_LIST, None )
                    
                    # got a list?
                    if ( author_article_id_list is None ):
                    
                        # no - first time author processed. --#
                        author_article_id_list = []
                        author_info_dict[ self.PROP_AUTHOR_ARTICLE_ID_LIST ] = author_article_id_list
                    
                    #-- END check to see if list of author's related sources is present. --#
                    
                    # Is article_id in list?
                    if ( article_id_IN not in author_article_id_list ):
                    
                        # no.  Add it.
                        author_article_id_list.append( article_id_IN )
                        
                    #-- END check to see if source in author's source list --#
                    
                else:
                
                    # error.  Should always have source info after calling
                    #    get_index_author_data().
                    pass
                
                #-- END check to see if we have author info --#
            
            #-- END check to make sure we have a coder. --#
        
        #-- END check for author person --#
        
        return status_OUT
    
    #-- END method update_author_article_id_list() --#


    def update_author_info( self, author_person_IN, source_person_IN, index_IN ):
        
        # return reference
        status_OUT = ""
        
        # declare variables
        me = "update_author_info"
        author_person_id = None
        source_person_id = None
        index_author_data_dict = None
        author_info_dict = None
        author_source_list = None
        
        # make sure we have an author person...
        if ( author_person_IN is not None ):
        
            # get ID
            author_person_id = author_person_IN.id
        
            # ...and a source person...
            if ( source_person_IN is not None ):
            
                # get ID
                source_person_id = source_person_IN.id
            
                # ...and an index.
                if ( ( index_IN is not None ) and ( index_IN > 0 ) ):
                
                    # got everything we need.  Get data for the current index.
                    index_author_data_dict = self.get_index_author_data( index_IN )
                    
                    # got something back?
                    if ( index_author_data_dict is not None ):

                        # yes.  Get author info.
                        author_info_dict = index_author_data_dict.get( author_person_id, None )
                        
                        # got any?
                        if ( author_info_dict is None ):
                        
                            # no.  Add some.
                            author_info_dict = {}
                            author_info_dict[ self.PROP_AUTHOR_SOURCE_LIST ] = []
                            author_info_dict[ self.PROP_AUTHOR_ARTICLE_ID_LIST ] = []
                            index_author_data_dict[ author_person_id ] = author_info_dict
                            
                        #-- END check to see if author info present. --#
                        
                        # Should have one now.  Get list of sources quoted by
                        #    this author.
                        author_source_list = author_info_dict.get( self.PROP_AUTHOR_SOURCE_LIST, None )
                        
                        # got a list?
                        if ( author_source_list is None ):
                        
                            # no - first time author processed. --#
                            author_source_list = []
                            author_info_dict[ self.PROP_AUTHOR_SOURCE_LIST ] = author_source_list
                        
                        #-- END check to see if list of author's related sources is present. --#
                        
                        # Is source in list?
                        if ( source_person_id not in author_source_list ):
                        
                            # no.  Add it.
                            author_source_list.append( source_person_id )
                            
                        #-- END check to see if source in author's source list --#
                        
                    else:
                    
                        # error.  Should always have source info after calling
                        #    get_index_author_data().
                        pass
                    
                    #-- END check to see if we have author info --#
                
                #-- END check to make sure we have a coder. --#
            
            #-- END check to make sure we have source person. --#
        
        #-- END check for author person --#
        
        return status_OUT
    
    #-- END method update_author_info() --#


    def update_author_shared_sources( self ):
        
        '''
        Within the data for each coder (as defined by index, rather than a coder
           ID), looks through the source data to find instances where a source
           was quoted by multiple authors, then updates the authors' data so it
           contains lists of the sources who were shared and the other authors
           who quoted each source.
           
        Preconditions: this method is invoked at the end of process_articles().
           If you invoke it on its own, you must already have called
           process_articles() such that the author and source data are populated
           for each coder, as referenced by the variable
           self.coder_index_to_data_map.
           
        Postconditions: the data for each coder is updated to include a list of
           the shared sources for the author, a list of authors to which the
           current author is related based on shared sources, and an accounting
           per source of authors who also quoted that source.
        '''
        
        # return reference
        status_OUT = ""
        
        # declare variables
        me = "update_author_shared_sources"
        coder_index_to_data_dict = None
        coder_index = -1
        coder_data_dict = None
        author_id_to_data_dict = None
        source_id_to_data_dict = None
        source_id = -1
        source_data_dict = None
        source_author_list = None
        source_author_count = -1
        
        # declare variables - processing for sources with multiple authors.
        shared_author_id = -1
        shared_author_data = None
        author_shared_sources = None
        author_related_authors = None
        shared_source_dict = None
        current_related_author_id = -1

        print( "" )
        print( "Start of " + me + "():" )

        # retrieve coder data dict.
        coder_index_to_data_dict = self.coder_index_to_data_map
        
        # loop over the dictionary to process each index.
        for coder_index, coder_data_dict in six.iteritems( coder_index_to_data_dict ):
        
            # retrieve author and source data dictionaries.
            author_id_to_data_dict = coder_data_dict.get( self.PROP_CODER_AUTHOR_DATA, None )
            source_id_to_data_dict = coder_data_dict.get( self.PROP_CODER_SOURCE_DATA, None )
            
            # start with source data - loop looking for sources with more than
            #    one author.
            for source_id, source_data_dict in six.iteritems( source_id_to_data_dict ):
            
                # get author list.
                source_author_list = source_data_dict.get( self.PROP_SOURCE_AUTHOR_LIST, None )
                
                # get count of authors for source
                source_author_count = len( source_author_list )
                
                # if greater than 1, need to process.
                if ( source_author_count > 1 ):
                
                    print( "In " + me + ": multiple authors ( " + str( source_author_list ) + " for source " + str( source_id ) )
                    
                    # for each author, need to get their data and add info on
                    #    shared source.
                    for shared_author_id in source_author_list:
                    
                        # get data for author
                        shared_author_data = author_id_to_data_dict[ shared_author_id ]
                        
                        # see if the author has anything stored for shared
                        #    sources.
                        author_shared_sources = shared_author_data.get( self.PROP_AUTHOR_SHARED_SOURCE_INFO, None )
                        author_related_authors = shared_author_data.get( self.PROP_AUTHOR_SHARED_SOURCE_AUTHORS_LIST, None )
                        if ( author_shared_sources is None ):
                        
                            # no.  Add shared source info and list of authors
                            #    with whom the current author shared sources.
                            author_shared_sources = {}
                            shared_author_data[ self.PROP_AUTHOR_SHARED_SOURCE_INFO ] = author_shared_sources
                            author_related_authors = []
                            shared_author_data[ self.PROP_AUTHOR_SHARED_SOURCE_AUTHORS_LIST ] = author_related_authors
                        
                        #-- END check to see if author has shared source information --#
                        
                        # add information on source to shared source info.
                        #   - in self.PROP_AUTHOR_SHARED_SOURCE_INFO
                        
                        # is shared source already captured?
                        if ( source_id not in author_shared_sources ):
                        
                            # no.  Populate dictionary...
                            shared_source_dict = {}
                            shared_source_dict[ self.PROP_SHARED_SOURCE_ID ] = source_id
                            shared_source_dict[ self.PROP_SHARED_SOURCE_AUTHOR_LIST ] = source_author_list

                            # ...then add it to author's shared source info.
                            author_shared_sources[ source_id ] = shared_source_dict
                            
                        else:
                        
                            # if present, output message, but also leave alone.
                            print( "In " + me + ": Source " + str( source_id ) + " already in shared sources for author " + str( shared_author_id ) + ".  This should not have happened..." )
                            
                        #-- END check to see if source is in author's list of shared sources. --#
                        
                        # make sure all related authors are in list of authors
                        #   with whom the current author shares sources.
                        for current_related_author_id in source_author_list:
                        
                            # is author in master list?
                            if ( current_related_author_id not in author_related_authors ):
                            
                                # no.  Add it.
                                author_related_authors.append( current_related_author_id )
                                
                            #-- END check to see if related author is in author's list. --#
                         
                        #-- END loop over related authors for current source --#
                    
                    #-- END loop over shared author data. --#
                
                else:
                
                    # only one author for this source - moving on.
                    pass
                
                #-- END check to see if more than one author for the current source. --#
            
            #-- END loop over sources. --#
        
        #-- END loop over coders. --#
        
        return status_OUT
    
    #-- END method update_author_shared_sources() --#


    def update_source_info( self, author_person_IN, source_person_IN, index_IN ):
        
        # return reference
        status_OUT = ""
        
        # declare variables
        me = "update_source_info"
        author_person_id = None
        source_person_id = None
        index_source_data_dict = None
        source_info_dict = None
        source_author_list = None
        
        # make sure we have an author person...
        if ( author_person_IN is not None ):
        
            # get ID
            author_person_id = author_person_IN.id
        
            # ...and a source person...
            if ( source_person_IN is not None ):
            
                # get ID
                source_person_id = source_person_IN.id
            
                # ...and an index.
                if ( ( index_IN is not None ) and ( index_IN > 0 ) ):
                                
                    # got everything we need.  Get data for the current coder.
                    index_source_data_dict = self.get_index_source_data( index_IN )
                    
                    # got something back?
                    if ( index_source_data_dict is not None ):

                        # yes.  Get source info.
                        source_info_dict = index_source_data_dict.get( source_person_id, None )
                        
                        # got any?
                        if ( source_info_dict is None ):
                        
                            # no.  Add some.
                            source_info_dict = {}
                            source_info_dict[ self.PROP_SOURCE_AUTHOR_LIST ] = []
                            index_source_data_dict[ source_person_id ] = source_info_dict
                            
                        #-- END check to see if source info present. --#
                        
                        # Should have one now.  Get list of authors who quoted
                        #    this source.
                        source_author_list = source_info_dict.get( self.PROP_SOURCE_AUTHOR_LIST, None )
                        
                        # got a list?
                        if ( source_author_list is None ):
                        
                            # no - first time source and author are related. --#
                            source_author_list = []
                            source_info_dict[ self.PROP_SOURCE_AUTHOR_LIST ] = source_author_list
                        
                        #-- END check to see if list of source's related authors is present. --#
                        
                        # Is author in list?
                        if ( author_person_id not in source_author_list ):
                        
                            # no.  Add it.
                            source_author_list.append( author_person_id )
                            
                        #-- END check to see if author in source's author list --#
                    
                    else:
                    
                        # error.  Should always have source info after calling
                        #    get_index_source_data().
                        pass
                    
                    #-- END check to see if we have source info --#
                
                #-- END check to make sure we have a coder. --#
            
            #-- END check to make sure we have source persons. --#
        
        #-- END check for author person --#
        
        return status_OUT
    
    #-- END method update_source_info() --#


#-- END class Analysis_Person_Info --#
