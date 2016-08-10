from __future__ import unicode_literals

# django imports
from django.contrib.auth.models import User

# sourcenet imports
from sourcenet.shared.sourcenet_base import SourcenetBase

# sourcenet_analysis imports
from sourcenet_analysis.reliability.reliability_names_builder import ReliabilityNamesBuilder

# declare variables
my_reliability_instance = None
tag_list = None
label = ""

# declare variables - user setup
current_coder = None
current_coder_id = -1
current_index = -1

# declare variables - Article_Data filtering.
coder_type = ""

# make reliability instance
my_reliability_instance = ReliabilityNamesBuilder()

#===============================================================================
# configure
#===============================================================================

# list of tags of articles we want to process.
#tag_list = [ "prelim_reliability_combined", ]
tag_list = [ "prelim_reliability_test", ]

# label to associate with results, for subsequent lookup.
#label = "prelim_reliability_combined_human"
#label = "prelim_reliability_combined_all"
#label = "prelim_reliability_test_human"
label = "prelim_reliability_test_all"

'''
# ====> old way

# declare variables - user setup
current_coder = None
current_coder_id = -1
current_index = -1
coder_id_to_instance_map = {}
coder_id_to_index_map = {}
limit_to_user_ids = []

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

# ...and 2 is index 4
current_coder_id = 2
current_index = 4
current_coder = User.objects.get( id = current_coder_id )
coder_id_to_instance_map[ current_coder_id ] = current_coder
coder_id_to_index_map[ current_coder_id ] = current_index
limit_to_user_ids.append( current_coder_id )

# store configuration in instance.
my_reliability_instance.coder_id_to_instance_map = coder_id_to_instance_map
my_reliability_instance.coder_id_to_index_map = coder_id_to_index_map
my_reliability_instance.limit_to_user_ids = limit_to_user_ids
'''

# ====> new way

# set it up so that...

# ...coder ID 8 is index 1...
current_coder_id = 8
current_index = 1
my_reliability_instance.add_coder_at_index( current_coder_id, current_index )

# ...coder ID 9 is index 2...
current_coder_id = 9
current_index = 2
my_reliability_instance.add_coder_at_index( current_coder_id, current_index )

# ...coder ID 10 is index 3...
current_coder_id = 10
current_index = 3
my_reliability_instance.add_coder_at_index( current_coder_id, current_index )

# ...and automated coder (2) is index 4
current_coder = SourcenetBase.get_automated_coding_user()
current_coder_id = current_coder.id
current_index = 4
my_reliability_instance.add_coder_at_index( current_coder_id, current_index )

# and only look at coding by those users.  And...

# configure so that it limits to automated coder_type of OpenCalais_REST_API_v2.
coder_type = "OpenCalais_REST_API_v2"
#my_reliability_instance.limit_to_automated_coder_type = "OpenCalais_REST_API_v2"
my_reliability_instance.automated_coder_type_include_list.append( coder_type )

# output debug JSON to file
#my_reliability_instance.debug_output_json_file_path = "/home/jonathanmorgan/" + label + ".json"

#===============================================================================
# process
#===============================================================================

# process articles
my_reliability_instance.process_articles( tag_list )

# output to database.
my_reliability_instance.output_reliability_data( label )
