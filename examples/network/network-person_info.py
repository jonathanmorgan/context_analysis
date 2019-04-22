from __future__ import unicode_literals

# python package imports
import six

# django imports
from django.contrib.auth.models import User

# sourcenet imports
from sourcenet.models import Article
from sourcenet.models import Article_Data
from sourcenet.models import Person

# context_analysis imports
from context_analysis.models import Reliability_Ties
from context_analysis.network.network_person_info import NetworkPersonInfo

# declare variables
my_info_instance = None
tag_list = None
label = ""

# declare variables - user setup
current_coder = None
current_coder_id = -1
current_index = -1
current_priority = -1

# declare variables - Article_Data filtering.
coder_type = ""

# make info instance
my_info_instance = NetworkPersonInfo()

#===============================================================================
# configure
#===============================================================================

# list of tags of articles we want to process.
tag_list = [ "grp_month", ]

# label to associate with results, for subsequent lookup.
label = "prelim_month"

# ! ====> map coders to indices

# set it up so that...

# ...the ground truth user has highest priority (4) for index 1...
current_coder = SourcenetBase.get_ground_truth_coding_user()
current_coder_id = current_coder.id
current_index = 1
current_priority = 4
my_info_instance.add_coder_at_index( current_coder_id, current_index, priority_IN = current_priority )

# ...coder ID 8 is priority 3 for index 1...
current_coder_id = 8
current_index = 1
current_priority = 3
my_info_instance.add_coder_at_index( current_coder_id, current_index, priority_IN = current_priority )

# ...coder ID 9 is priority 2 for index 1...
current_coder_id = 9
current_index = 1
current_priority = 2
my_info_instance.add_coder_at_index( current_coder_id, current_index, priority_IN = current_priority )

# ...coder ID 10 is priority 1 for index 1...
current_coder_id = 10
current_index = 1
current_priority = 1
my_info_instance.add_coder_at_index( current_coder_id, current_index, priority_IN = current_priority )

# ...and automated coder (2) is index 2
current_coder = SourcenetBase.get_automated_coding_user()
current_coder_id = current_coder.id
current_index = 2
current_priority = 1
my_info_instance.add_coder_at_index( current_coder_id, current_index, priority_IN = current_priority )

# and only look at coding by those users.  And...

# configure so that it limits to automated coder_type of OpenCalais_REST_API_v2.
coder_type = "OpenCalais_REST_API_v2"
#my_reliability_instance.limit_to_automated_coder_type = "OpenCalais_REST_API_v2"
my_info_instance.automated_coder_type_include_list.append( coder_type )

#===============================================================================
# process articles
#===============================================================================

# process articles
my_info_instance.process_articles( tag_list )

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

# for each index, get authors.
coder_index_to_data_dict = my_info_instance.coder_index_to_data_map
        
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