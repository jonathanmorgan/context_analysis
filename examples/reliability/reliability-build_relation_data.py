from __future__ import unicode_literals

# python package imports
import six

# django imports
from django.contrib.auth.models import User

# context_analysis imports
from context_analysis.reliability import ReliabilityTiesBuilder

# declare variables
my_reliability_instance = None
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
my_reliability_instance = ReliabilityTiesBuilder()

# place dictionaries in instance.
my_reliability_instance.coder_id_to_instance_map = coder_id_to_instance_dict
my_reliability_instance.coder_id_to_index_map = coder_id_to_index_dict

# configure so that it limits to automated coder_type of OpenCalais_REST_API_v2.
my_reliability_instance.limit_to_automated_coder_type = "OpenCalais_REST_API_v2"

# label for reliability rows created and used in this session.
label = "prelim_network_fixed_authors"
my_reliability_instance.reliability_row_label = label

# process articles
tag_list = [ "prelim_network", ]
my_reliability_instance.process_articles( tag_list )