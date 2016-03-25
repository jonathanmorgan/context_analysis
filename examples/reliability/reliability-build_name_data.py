from __future__ import unicode_literals

# django imports
from django.contrib.auth.models import User

# sourcenet_analysis imports
from sourcenet_analysis.reliability.reliability_names_builder import ReliabilityNamesBuilder

# declare variables
my_reliability_instance = None
tag_list = None
label = ""
current_coder = None
coder_id_to_instance_map = {}
coder_id_to_index_map = {}
limit_to_user_ids = []

# make reliability instance
my_reliability_instance = ReliabilityNamesBuilder()

#===============================================================================
# configure
#===============================================================================

# set it up so that...

# ...8 is index 1...
current_coder_id = 8
current_index = 1
current_coder = User.objects.get( id = current_coder_id )
coder_id_to_instance_map[ current_coder_id ] = current_coder
coder_id_to_index_map[ current_coder_id ] = current_index
limit_to_user_ids.append( current_coder_id )

# ...9 is index 2...
current_coder_id = 9
current_index = 2
current_coder = User.objects.get( id = current_coder_id )
coder_id_to_instance_map[ current_coder_id ] = current_coder
coder_id_to_index_map[ current_coder_id ] = current_index
limit_to_user_ids.append( current_coder_id )

# ...and 10 is index 3
current_coder_id = 10
current_index = 3
current_coder = User.objects.get( id = current_coder_id )
coder_id_to_instance_map[ current_coder_id ] = current_coder
coder_id_to_index_map[ current_coder_id ] = current_index
limit_to_user_ids.append( current_coder_id )

# configure so that it limits to automated coder_type of OpenCalais_REST_API_v2.
#my_reliability_instance.limit_to_automated_coder_type = "OpenCalais_REST_API_v2"

# store configuration in instance.
my_reliability_instance.coder_id_to_instance_map = coder_id_to_instance_map
my_reliability_instance.coder_id_to_index_map = coder_id_to_index_map
my_reliability_instance.limit_to_user_ids = limit_to_user_ids

#===============================================================================
# process
#===============================================================================

# process articles
#tag_list = [ "prelim_reliability", ]
tag_list = [ "prelim_reliability_test", ]
my_reliability_instance.process_articles( tag_list )

# output to database.
label = "prelim_reliability_test_001"
my_reliability_instance.output_reliability_data( label )
