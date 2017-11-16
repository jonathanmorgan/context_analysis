from __future__ import unicode_literals

# python package imports
import six

# django imports
from django.contrib.auth.models import User

# sourcenet imports
from sourcenet.models import Analysis_Reliability_Ties
from sourcenet.models import Article
from sourcenet.models import Article_Data
from sourcenet.models import Person

# sourcenet_analysis imports
from sourcenet_analysis.network.network_person_info import NetworkPersonInfo

# declare variables
my_analysis_instance = None
coder_rs = None
current_coder = None
current_coder_id = -1
coder_index = -1
coder_id_to_index_dict = {}
coder_id_to_instance_dict = {}
tag_list = None
label = ""

# get coders we want to include in analysis.
coder_rs = User.objects.filter( id__in = [ 2, 4, 6 ] )

# set up coder maps.
coder_index = 0
for current_coder in coder_rs:

    # increment coder index
    coder_index = coder_index + 1

    # get coder's user id
    current_coder_id = current_coder.id
    
    # add to ID-to-instance map
    coder_id_to_instance_dict[ current_coder_id ] = current_coder
    
    # add to ID-to-index map
    coder_id_to_index_dict[ current_coder_id ] = coder_index

#-- END loop over coders --#

# manually set up the ID to index map so the humans both map to 1, automated
#    maps to 2.
coder_id_to_index_dict[ 6 ] = 1
coder_id_to_index_dict[ 4 ] = 1
coder_id_to_index_dict[ 2 ] = 2

# make reliability instance
my_analysis_instance = NetworkPersonInfo()

# place dictionaries in instance.
my_analysis_instance.coder_id_to_instance_map = coder_id_to_instance_dict
my_analysis_instance.coder_id_to_index_map = coder_id_to_index_dict

# configure so that it limits to automated coder_type of OpenCalais_REST_API_v2.
my_reliability_instance.limit_to_automated_coder_type = "OpenCalais_REST_API_v2"

# label for reliability rows created and used in this session.
label = "prelim_network_fixed_authors"
my_analysis_instance.reliability_row_label = label

# process articles
tag_list = [ "prelim_network", ]
my_analysis_instance.process_articles( tag_list )

#output lists of counts of sources and shared source by author

# declare variables - looking at data
coder_index_to_data_dict = None
coder_index = -1
coder_data_dict = None
coder_author_id_list = None
coder_author_source_count_list = None
coder_author_shared_count_list = None
coder_author_article_count_list = None
mean_source_count = -1
mean_shared_count = -1
mean_article_count = -1
author_index = -1
shared_count = -1
temp_author_id_list = []
temp_source_count_list = []
temp_shared_count_list = []
temp_article_count_list = []

# for each coder, get authors.
coder_index_to_data_dict = my_analysis_instance.coder_index_to_data_map
        
# loop over the dictionary to process each index.
for coder_index, coder_data_dict in six.iteritems( coder_index_to_data_dict ):

    # get data for coder
    coder_author_id_list = coder_data_dict.get( NetworkPersonInfo.PROP_CODER_AUTHOR_ID_LIST, None )
    coder_author_source_count_list = coder_data_dict.get( NetworkPersonInfo.PROP_CODER_AUTHOR_SOURCE_COUNT_LIST, None )
    coder_author_shared_count_list = coder_data_dict.get( NetworkPersonInfo.PROP_CODER_AUTHOR_SHARED_COUNT_LIST, None )
    coder_author_article_count_list = coder_data_dict.get( NetworkPersonInfo.PROP_CODER_AUTHOR_ARTICLE_COUNT_LIST, None )

    # output
    print( "" )
    print( "================================================================================" )
    print( "Data for Coder index " + str( coder_index ) + ":" )

    print( "" )
    print( "==> All authors" )
    print( "- author ID list = " + str( coder_author_id_list ) )    
    print( "- author source count list = " + str( coder_author_source_count_list ) )    
    print( "- author shared count list = " + str( coder_author_shared_count_list ) )    
    print( "- author article count list = " + str( coder_author_article_count_list ) )    

    # and some computations

    # author count
    print( "- author count = " + str( len( coder_author_id_list ) ) )
    
    # mean source count per author
    mean_source_count = float( sum( coder_author_source_count_list ) ) / len( coder_author_source_count_list )
    print( "- mean source count per author = " + str( mean_source_count ) )
    
    # mean shared count per author
    mean_shared_count = float( sum( coder_author_shared_count_list ) ) / len( coder_author_shared_count_list )
    print( "- mean shared count per author = " + str( mean_shared_count ) )
    
    # mean article count per author
    mean_article_count = float( sum( coder_author_article_count_list ) ) / len( coder_author_article_count_list )
    print( "- mean article count per author = " + str( mean_article_count ) )
    
    # the same, but just for those with shared sources.
    author_index = -1
    temp_author_id_list = []
    temp_source_count_list = []
    temp_shared_count_list = []
    temp_article_count_list = []

    for shared_count in coder_author_shared_count_list:
    
        # increment index
        author_index += 1
        
        # greater than 0?
        if ( shared_count > 0 ):
        
            # yes, add info to temp lists.
            temp_author_id_list.append( coder_author_id_list[ author_index ] )
            temp_source_count_list.append( coder_author_source_count_list[ author_index ] )
            temp_shared_count_list.append( coder_author_shared_count_list[ author_index ] )
            temp_article_count_list.append( coder_author_article_count_list[ author_index ] )
            
        #-- END check to see if shared count > 0 --#
    
    #-- END loop over shared_count_list --#

    print( "" )
    print( "==> Authors with shared sources" )
    print( "- author ID list = " + str( temp_author_id_list ) )    
    print( "- author source count list = " + str( temp_source_count_list ) )    
    print( "- author shared count list = " + str( temp_shared_count_list ) )    
    print( "- author article count list = " + str( temp_article_count_list ) )    

    # and some computations

    # author count
    print( "- author count = " + str( len( temp_author_id_list ) ) )
    
    # mean source count per author with shared sources
    mean_source_count = float( sum( temp_source_count_list ) ) / len( temp_source_count_list )
    print( "- mean source count per author with shared sources = " + str( mean_source_count ) )
    
    # mean shared count per author with shared sources
    mean_shared_count = float( sum( temp_shared_count_list ) ) / len( temp_shared_count_list )
    print( "- mean shared count per author with shared sources = " + str( mean_shared_count ) )
    
    # mean article count per author
    mean_article_count = float( sum( temp_article_count_list ) ) / len( temp_article_count_list )
    print( "- mean article count per author = " + str( mean_article_count ) )
    
#-- END loop over coders. --#