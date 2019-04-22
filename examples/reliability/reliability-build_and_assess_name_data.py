# start to support python 3:
from __future__ import unicode_literals
from __future__ import division

#==============================================================================#
# ! imports
#==============================================================================#


# grouped by functional area, then alphabetical order by package, then
#     alphabetical order by name of thing being imported.

# context_analysis imports
from context_analysis.reliability.reliability_names_analyzer import ReliabilityNamesAnalyzer
from context_analysis.reliability.reliability_names_builder import ReliabilityNamesBuilder


#==============================================================================#
# ! logic
#==============================================================================#

# declare variables
shared_identifier = ""

# shared identifier used as label for both data building and analysis.
shared_identifier = "prelim_training_003"

#------------------------------------------------------------------------------#
# ! build Reliability_Names data
#------------------------------------------------------------------------------#

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
tag_list = [ shared_identifier, ]
my_reliability_instance.process_articles( tag_list )

# output to database.
label = shared_identifier
my_reliability_instance.output_reliability_data( label )

#------------------------------------------------------------------------------#
# ! build Reliability_Names_Results data
#------------------------------------------------------------------------------#

# declare variables
my_analysis_instance = None
label = ""
indices_to_process = -1
result_status = ""

# make reliability instance
my_analysis_instance = ReliabilityNamesAnalyzer()

# database connection information:
my_analysis_instance.db_username = ""
my_analysis_instance.db_password = ""
my_analysis_instance.db_host = "localhost"
my_analysis_instance.db_name = "sourcenet"

# run the analyze method, see what happens.
label = shared_identifier
indices_to_process = 3
result_status = my_analysis_instance.analyze_reliability_names( label, indices_to_process )