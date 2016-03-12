# start to support python 3:
from __future__ import unicode_literals
from __future__ import division

#==============================================================================#
# ! imports
#==============================================================================#

# grouped by functional area, then alphabetical order by package, then
#     alphabetical order by name of thing being imported.

# sourcenet_analysis imports
from sourcenet_analysis.reliability.reliability_names_analyzer import ReliabilityNamesAnalyzer

#==============================================================================#
# ! logic
#==============================================================================#

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
label = "prelim_training_003"
indices_to_process = 3
result_status = my_analysis_instance.analyze_reliability_names( label, indices_to_process )
