from __future__ import unicode_literals

# sourcenet_analysis imports
from sourcenet_analysis.reliability.reliability_names_builder import ReliabilityNamesBuilder

# declare variables
my_reliability_instance = None
tag_list = None
label = ""

# make reliability instance
my_reliability_instance = ReliabilityNamesBuilder()

# configure so that it limits to automated coder_type of OpenCalais_REST_API_v2.
#my_reliability_instance.limit_to_automated_coder_type = "OpenCalais_REST_API_v2"

# process articles
#tag_list = [ "prelim_reliability", ]
tag_list = [ "prelim_training_002", ]
my_reliability_instance.process_articles( tag_list )

# output to database.
label = "prelim_training_002"
my_reliability_instance.output_reliability_data( label )
