from __future__ import unicode_literals

# sourcenet_analysis imports
from sourcenet_analysis.models import Reliability_Names

# declare variables
reliability_names_qs = None
label_equals = ""
record_count = -1
do_delete = False
current_instance = None
instance_counter = -1

# start with Reliability_Names.objects.all()
reliability_names_qs = Reliability_Names.objects.all()

#===============================================================================
# filter
#===============================================================================

# label?
label_equals = "prelim_reliability_combined_all"

if ( ( label_equals is not None ) and ( label_equals != "" ) ):

    # got a label.  Filter.
    reliability_names_qs = reliability_names_qs.filter( label = label_equals )
    
    print( "filtering on label \"" + label_equals + "\"" )

#-- END check to see if label set. --#


#===============================================================================
# process
#===============================================================================

# process articles
record_count = reliability_names_qs.count()

print( "Found " + str( record_count ) + " matching Reliability_Names records." )

if ( do_delete == True ):

    print( "do_delete is True.  Whacking away!" )
    
    # loop
    instance_counter = 0
    for current_instance in reliability_names_qs:
    
        # increment counter
        instance_counter += 1
    
        print( "- #" + str( instance_counter ) + " - delete()-ing record ID " + str( current_instance.id ) )
    
        # delete.
        current_instance.delete()
    
    #-- END loop over Reliability_Names instances. --#

else:

    print( "do_delete is False.  A stay for these records!" )

#-- END check to see if we actually delete. --#

# Once you are done, you can use this SQL as a template for resetting the next
#     automatically generated ID should you care about such things.
# ALTER SEQUENCE sourcenet_analysis_reliability_names_id_seq RESTART WITH 2076;
print( "Once you are done, you can use this SQL as a template for resetting the next automatically generated ID should you care about such things." )
print( "ALTER SEQUENCE sourcenet_analysis_reliability_names_id_seq RESTART WITH 2076;" )