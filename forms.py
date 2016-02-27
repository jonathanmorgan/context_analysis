from __future__ import unicode_literals

'''
Copyright 2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet.

sourcenet is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet. If not, see http://www.gnu.org/licenses/.
'''

# import django form object.
from django import forms

class ReliabilityNamesFilterForm( forms.Form ):

    '''
    form to hold variables used in looking up Reliability_Names instances.
    '''

    # label
    reliability_names_label = forms.CharField( required = True, label = "Label" )
    reliability_names_coder_count = forms.CharField( required = True, label = "Coders to compare (1 through ==>)" )
    #reliability_names_coder_id_list = forms.CharField( required = True, label = "Coders to compare (separated by commas)" )

#-- END ReliabilityNamesFilterForm --#
