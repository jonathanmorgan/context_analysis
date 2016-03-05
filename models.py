# start to support python 3:
from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet_analysis.

sourcenet_analysis is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

sourcenet_analysis is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with http://github.com/jonathanmorgan/sourcenet_analysis.  If not, see
<http://www.gnu.org/licenses/>.
'''

# django imports
from django.contrib.auth.models import User
from django.db import models

# django encoding imports (for supporting 2 and 3).
import django.utils.encoding
from django.utils.encoding import python_2_unicode_compatible

# sourcenet imports
from sourcenet.models import Article
from sourcenet.models import Person

#==============================================================================#
# !Analysis models
#==============================================================================#


@python_2_unicode_compatible
class Reliability_Names( models.Model ):

    '''
    Class to hold information on name detection choices within a given article
        across coders, for use in inter-coder reliability testing.  Intended to
        be read or exported for use by statistical analysis packages (numpy, R, 
        etc.).  Example of how to populate this table:
       
        sourcenet_analysis/examples/reliability/reliability-build_name_data.py
       
        Examples of calculating reliability TK.
       
        Includes columns for ten coders.  If you need more, add more sets of
        coder columns.
    '''

    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    


    # property names for building disagreement output (if ues this elsewhere,
    #     make Disagreement and DisagreementDetail objects).
    PROP_NAME_INSTANCE = "instance"
    PROP_NAME_ID = "id"
    PROP_NAME_LABEL = "label"
    PROP_NAME_ARTICLE_ID = "article_id"
    PROP_NAME_PERSON_NAME = "person_name"
    PROP_NAME_PERSON_ID = "person_id"
    PROP_NAME_PERSON_TYPE = "person_type"
    PROP_NAME_CODER_DETAILS_LIST = "coder_details_list"
    PROP_NAME_CODER_ID = "coder_id"
    PROP_NAME_CODER_DETECTED = "coder_detected"
    PROP_NAME_CODER_PERSON_ID = "coder_person_id"
    PROP_NAME_CODER_PERSON_TYPE = "coder_person_type"

    #----------------------------------------------------------------------
    # model fields
    #----------------------------------------------------------------------

    article = models.ForeignKey( Article, blank = True, null = True )
    person = models.ForeignKey( Person, blank = True, null = True )
    person_name = models.CharField( max_length = 255, blank = True, null = True )
    person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder1 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder1_set" )
    coder1_coder_id = models.IntegerField( blank = True, null = True )
    coder1_detected = models.IntegerField( blank = True, null = True )
    coder1_person_id = models.IntegerField( blank = True, null = True )
    coder1_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder1_person_type_int = models.IntegerField( blank = True, null = True )
    coder1_article_data_id = models.IntegerField( blank = True, null = True )
    coder1_article_person_id = models.IntegerField( blank = True, null = True )
    coder2 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder2_set" )
    coder2_coder_id = models.IntegerField( blank = True, null = True )
    coder2_detected = models.IntegerField( blank = True, null = True )
    coder2_person_id = models.IntegerField( blank = True, null = True )
    coder2_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder2_person_type_int = models.IntegerField( blank = True, null = True )
    coder2_article_data_id = models.IntegerField( blank = True, null = True )
    coder2_article_person_id = models.IntegerField( blank = True, null = True )
    coder3 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder3_set" )
    coder3_coder_id = models.IntegerField( blank = True, null = True )
    coder3_detected = models.IntegerField( blank = True, null = True )
    coder3_person_id = models.IntegerField( blank = True, null = True )
    coder3_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder3_person_type_int = models.IntegerField( blank = True, null = True )
    coder3_article_data_id = models.IntegerField( blank = True, null = True )
    coder3_article_person_id = models.IntegerField( blank = True, null = True )
    coder4 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder4_set" )
    coder4_coder_id = models.IntegerField( blank = True, null = True )
    coder4_detected = models.IntegerField( blank = True, null = True )
    coder4_person_id = models.IntegerField( blank = True, null = True )
    coder4_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder4_person_type_int = models.IntegerField( blank = True, null = True )
    coder4_article_data_id = models.IntegerField( blank = True, null = True )
    coder4_article_person_id = models.IntegerField( blank = True, null = True )
    coder5 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder5_set" )
    coder5_coder_id = models.IntegerField( blank = True, null = True )
    coder5_detected = models.IntegerField( blank = True, null = True )
    coder5_person_id = models.IntegerField( blank = True, null = True )
    coder5_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder5_person_type_int = models.IntegerField( blank = True, null = True )
    coder5_article_data_id = models.IntegerField( blank = True, null = True )
    coder5_article_person_id = models.IntegerField( blank = True, null = True )
    coder6 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder6_set" )
    coder6_coder_id = models.IntegerField( blank = True, null = True )
    coder6_detected = models.IntegerField( blank = True, null = True )
    coder6_person_id = models.IntegerField( blank = True, null = True )
    coder6_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder6_person_type_int = models.IntegerField( blank = True, null = True )
    coder6_article_data_id = models.IntegerField( blank = True, null = True )
    coder6_article_person_id = models.IntegerField( blank = True, null = True )
    coder7 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder7_set" )
    coder7_coder_id = models.IntegerField( blank = True, null = True )
    coder7_detected = models.IntegerField( blank = True, null = True )
    coder7_person_id = models.IntegerField( blank = True, null = True )
    coder7_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder7_person_type_int = models.IntegerField( blank = True, null = True )
    coder7_article_data_id = models.IntegerField( blank = True, null = True )
    coder7_article_person_id = models.IntegerField( blank = True, null = True )
    coder8 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder8_set" )
    coder8_coder_id = models.IntegerField( blank = True, null = True )
    coder8_detected = models.IntegerField( blank = True, null = True )
    coder8_person_id = models.IntegerField( blank = True, null = True )
    coder8_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder8_person_type_int = models.IntegerField( blank = True, null = True )
    coder8_article_data_id = models.IntegerField( blank = True, null = True )
    coder8_article_person_id = models.IntegerField( blank = True, null = True )
    coder9 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder9_set" )
    coder9_coder_id = models.IntegerField( blank = True, null = True )
    coder9_detected = models.IntegerField( blank = True, null = True )
    coder9_person_id = models.IntegerField( blank = True, null = True )
    coder9_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder9_person_type_int = models.IntegerField( blank = True, null = True )
    coder9_article_data_id = models.IntegerField( blank = True, null = True )
    coder9_article_person_id = models.IntegerField( blank = True, null = True )
    coder10 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_coder10_set" )
    coder10_coder_id = models.IntegerField( blank = True, null = True )
    coder10_detected = models.IntegerField( blank = True, null = True )
    coder10_person_id = models.IntegerField( blank = True, null = True )
    coder10_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder10_person_type_int = models.IntegerField( blank = True, null = True )
    coder10_article_data_id = models.IntegerField( blank = True, null = True )
    coder10_article_person_id = models.IntegerField( blank = True, null = True )
    label = models.CharField( max_length = 255, blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )


    #----------------------------------------------------------------------------
    # Meta class
    #----------------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:
        ordering = [ 'article', 'person_type', 'person' ]


    #----------------------------------------------------------------------------
    # class methods
    #----------------------------------------------------------------------------


    @classmethod
    def lookup_disagreements( cls, label_IN = "", coder_count_IN = -1 ):
        
        # return reference
        qs_OUT = None
        
        # declare variables
        my_label = ""
        my_coder_count = -1
        current_outer_index = -1
        current_inner_index = -1

        # declare variables - building up SQL statement.
        sql_string = ""
        sql_temp_string = ""
        sql_detected_list = []
        sql_person_id_list = []
        sql_person_type_list = []
        sql_raw_params_list = []
        
        # do we have a label?
        if ( ( label_IN is not None ) and ( label_IN != "" ) ):

            # yes - use it.
            my_label = label_IN
        
        #-- END check to see if label --#
        
        # got coder_count_IN?
        if ( ( coder_count_IN is not None ) and ( coder_count_IN != "" ) and ( coder_count_IN > 2 ) ):
        
            # yes, and is at least 2.  Use it.
            my_coder_count = int( coder_count_IN )
        
        else:
        
            # no, or not at least 2.  Default to 2.
            my_coder_count = 2
            
        #-- END check to see if coder count passed in. --#
        
        # loop over coders we've been asked to compare
        sql_detected_list = []
        sql_person_id_list = []
        sql_person_type_list = []
        for current_outer_index in range( 1, my_coder_count + 1 ):
        
            # loop over indices past the current one, adding SQL fragments to
            #     our SQL lists for comparison of current to subsequent.
            for current_inner_index in range( current_outer_index + 1, my_coder_count + 1 ):

                # add inequality comparison for detected.
                column_name_suffix = "_detected"
                sql_temp_string = "( coder" + str( current_outer_index ) + column_name_suffix + " != coder" + str( current_inner_index ) + column_name_suffix + " )"
                sql_detected_list.append( sql_temp_string )
                
                # add inequality comparison for lookup.
                column_name_suffix = "_person_id"
                sql_temp_string = "( coder" + str( current_outer_index ) + column_name_suffix + " != coder" + str( current_inner_index ) + column_name_suffix + " )"
                sql_person_id_list.append( sql_temp_string )
                
                # add inequality comparison for type.
                column_name_suffix = "_person_type"
                sql_temp_string = "( coder" + str( current_outer_index ) + column_name_suffix + " != coder" + str( current_inner_index ) + column_name_suffix + " )"
                sql_person_type_list.append( sql_temp_string )

            #-- END loop over rest of indices past current --#
        
        #-- END loop over coders to compare --#
        
        # build SQL string
        sql_string = "SELECT * FROM sourcenet_analysis_reliability_names WHERE "
        
        # got a label?
        if ( ( my_label is not None ) and ( my_label != "" ) ):

            # yes.  Add to WHERE clause.
            sql_string += " label = %s AND ( "
            
            # and add value to params list.
            sql_raw_params_list.append( my_label )

        #-- END check to see if label set --#
        
        # append detected comparisons
        sql_temp_string = " OR ".join( sql_detected_list )
        sql_string += " ( " + sql_temp_string + " )"
        
        # append person id comparisons
        sql_temp_string = " OR ".join( sql_person_id_list )
        sql_string += " OR ( " + sql_temp_string + " )"

        # append person type comparisons
        sql_temp_string = " OR ".join( sql_person_type_list )
        sql_string += " OR ( " + sql_temp_string + " )"
        
        # got a label?
        if ( ( my_label is not None ) and ( my_label != "" ) ):

            # yes.  Close parentheses.
            sql_string += " )"

        #-- END check to see if label set --#
        
        # execute raw query
        qs_OUT = cls.objects.raw( sql_string, sql_raw_params_list )

        return qs_OUT        
    
    #-- END class method lookup_disagreements() --#


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        temp_string = ""
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got a label?
        if ( self.label ):
        
            # got a label
            string_OUT += " - label: " + self.label
            
        #-- END check for label --#
        
        # got an article?
        if ( self.article ):
        
            # yes - output ID.
            string_OUT += " - article ID: " + str( self.article.id )
            
        #-- END check to see if article. --#
        
        # got person_name?
        if ( self.person_name ):
        
            # yes, append it
            string_OUT += " - " + self.person_name
            
        #-- END check to see if person_name --#
            
        # got person?
        if ( self.person ):
        
            # yes, append ID in parens.
            string_OUT += " ( " + str( self.person.id ) + " )"
            
        #-- END check to see if we have a person. --#
        
        # got coder details?
        if ( ( self.coder1 ) or ( self.coder2 ) or ( self.coder3 ) ):
        
            # yes.  Output a summary of coding.
            string_OUT += " - coders: "
            
            temp_string = ""
            
            if ( self.coder1 ):
            
                # output details for coder 1
                string_OUT += "1"
                temp_string += " ====> 1 - " + str( self.coder1.id ) + "; " + str( self.coder1_detected ) + "; " + str( self.coder1_person_id )
                
            #-- END check to see if coder1 --#

            if ( self.coder2 ):
            
                # output details for coder 2
                string_OUT += "2"
                temp_string += " ====> 2 - " + str( self.coder2.id ) + "; " + str( self.coder2_detected ) + "; " + str( self.coder2_person_id )
                
            #-- END check to see if coder2 --#
        
            if ( self.coder3 ):
            
                # output details for coder 3
                string_OUT += "3"
                temp_string += " ====> 3 - " + str( self.coder3.id ) + "; " + str( self.coder3_detected ) + "; " + str( self.coder3_person_id )
                
            #-- END check to see if coder3 --#
            
            string_OUT += temp_string
        
        return string_OUT

    #-- END method __str__() --#
     

#= END Reliability_Names model ===============================================#


@python_2_unicode_compatible
class Reliability_Names_Results( models.Model ):

    '''
    Class to hold agreement scores for comparisons between pairs of coders whose
        coding data is captured in Reliability_Names.  To start, holds results
        of agreement on detecting and looking up authors and subjects, and for 
        subjects, on deciding if subject was source or simply mentioned.
        For each, calculates percentage agreement and Krippendorff's Alpha.  If
        desired, can also calculate a modified version of Scott's Pi for nominal
        variables where there is little variation in the data (lots of 1s,
        almost no 0s, for example) - this is only implemented for author and
        subject detect (1 or 0), and subject type (0 through 3).

        sourcenet_analysis/examples/reliability/reliability-assess_name_data.py
    '''

    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    

 
    #----------------------------------------------------------------------
    # model fields
    #----------------------------------------------------------------------

    label = models.CharField( max_length = 255, blank = True, null = True )
    coder1 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_results_coder1_set" )
    coder1_coder_index = models.IntegerField( blank = True, null = True )
    coder2 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_names_results_coder2_set" )
    coder2_coder_index = models.IntegerField( blank = True, null = True )
    author_count = models.IntegerField( blank = True, null = True )
    author_detect_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    author_detect_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_detect_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_lookup_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    author_lookup_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_lookup_count = models.IntegerField( blank = True, null = True )
    author_combined_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    author_combined_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_type_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    author_type_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_type_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_type_non_zero_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    author_type_non_zero_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_type_non_zero_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    author_type_non_zero_count = models.IntegerField( blank = True, null = True )
    subject_count = models.IntegerField( blank = True, null = True )
    subject_detect_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_detect_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_detect_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_lookup_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_lookup_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_lookup_count = models.IntegerField( blank = True, null = True )
    subject_combined_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_combined_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_type_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_type_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_type_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_type_non_zero_percent = models.DecimalField( blank = True, null = True, max_digits=13, decimal_places=10 )
    subject_type_non_zero_alpha = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_type_non_zero_pi = models.DecimalField( blank = True, null = True, max_digits=11, decimal_places=10 )
    subject_type_non_zero_count = models.IntegerField( blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )


    #----------------------------------------------------------------------------
    # Meta class
    #----------------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:
        ordering = [ 'label', 'coder1', 'coder2' ]


    #----------------------------------------------------------------------------
    # class methods
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        temp_string = ""
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got a label?
        if ( self.label ):
        
            # got a label
            string_OUT += " - label: " + self.label
            
        #-- END check for label --#
        
        # got coder details?
        if ( ( self.coder1 ) or ( self.coder2 ) ):
        
            # yes.  Output a summary of coding.
            string_OUT += " - coders: "
            
            temp_string = ""
            
            if ( self.coder1 ):
            
                # output details for coder 1
                string_OUT += "1"
                temp_string += " ====> 1 - " + str( self.coder1.id ) + "; " + str( self.coder1_detected ) + "; " + str( self.coder1_person_id )
                
            #-- END check to see if coder1 --#

            if ( self.coder2 ):
            
                # output details for coder 2
                string_OUT += "2"
                temp_string += " ====> 2 - " + str( self.coder2.id ) + "; " + str( self.coder2_detected ) + "; " + str( self.coder2_person_id )
                
            #-- END check to see if coder2 --#
        
            string_OUT += temp_string
        
        return string_OUT

    #-- END method __str__() --#
     

#= END Reliability_Names_Results model ========================================#


@python_2_unicode_compatible
class Reliability_Ties( models.Model ):

    '''
    Class to hold information on name detection choices within a given article
        across coders, for use in inter-coder reliability testing.  Intended to
        be read or exported for use by statistical analysis packages (numpy, R, 
        etc.).  Example of how to populate this table:
       
        sourcenet_analysis/examples/reliability/reliability-build_relation_data.py
       
        Examples of calculating reliability TK.
       
        Includes columns for three coders.  If you need more, add more sets of
        coder columns.
    '''

    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------


    # person types
    PERSON_TYPE_AUTHOR = "author"
    PERSON_TYPE_SOURCE = "source"
    
    # relation types
    RELATION_AUTHOR_TO_SOURCE = "author_to_source"
    RELATION_AUTHOR_TO_AUTHOR = "author_to_author"
    RELATION_SOURCE_TO_SOURCE = "source_to_source"
    

    #----------------------------------------------------------------------
    # model fields
    #----------------------------------------------------------------------

    person = models.ForeignKey( Person, blank = True, null = True, related_name = "reliability_ties_from_set" )
    person_name = models.CharField( max_length = 255, blank = True, null = True )
    person_type = models.CharField( max_length = 255, blank = True, null = True )
    relation_type = models.CharField( max_length = 255, blank = True, null = True )
    relation_person = models.ForeignKey( Person, blank = True, null = True, related_name = "reliability_ties_to_set" )
    relation_person_name = models.CharField( max_length = 255, blank = True, null = True )
    relation_person_type = models.CharField( max_length = 255, blank = True, null = True )
    coder1 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder1_set" )
    coder1_mention_count = models.IntegerField( blank = True, null = True )
    coder1_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder2 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder2_set" )
    coder2_mention_count = models.IntegerField( blank = True, null = True )
    coder2_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder3 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder3_set" )
    coder3_mention_count = models.IntegerField( blank = True, null = True )
    coder3_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder4 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder4_set" )
    coder4_mention_count = models.IntegerField( blank = True, null = True )
    coder4_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder5 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder5_set" )
    coder5_mention_count = models.IntegerField( blank = True, null = True )
    coder5_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder6 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder6_set" )
    coder6_mention_count = models.IntegerField( blank = True, null = True )
    coder6_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder7 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder7_set" )
    coder7_mention_count = models.IntegerField( blank = True, null = True )
    coder7_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder8 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder8_set" )
    coder8_mention_count = models.IntegerField( blank = True, null = True )
    coder8_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder9 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder9_set" )
    coder9_mention_count = models.IntegerField( blank = True, null = True )
    coder9_id_list = models.CharField( max_length = 255, blank = True, null = True )
    coder10 = models.ForeignKey( User, blank = True, null = True, related_name = "reliability_ties_coder10_set" )
    coder10_mention_count = models.IntegerField( blank = True, null = True )
    coder10_id_list = models.CharField( max_length = 255, blank = True, null = True )
    label = models.CharField( max_length = 255, blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )


    #----------------------------------------------------------------------------
    # Meta class
    #----------------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:
        ordering = [ 'person_type', 'person', 'relation_person' ]


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __str__( self ):

        # return reference
        string_OUT = ""
        
        # declare variables
        temp_string = ""
        
        # start with stuff we should always have.
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if ID. --#
        
        # got a label?
        if ( self.label ):
        
            # got a label
            string_OUT += " - label: " + self.label
            
        #-- END check for label --#
        
        # got person_name?
        if ( self.person_name ):
        
            # yes, append it
            string_OUT += " - from " + self.person_name
            
        #-- END check to see if person_name --#
            
        # got person?
        if ( self.person ):
        
            # yes, append ID in parens.
            string_OUT += " ( " + str( self.person.id ) + " )"
            
        #-- END check to see if we have a person. --#
        
        # got relation_person?
        if ( self.relation_person ):
        
            # yes.  add information.
            string_OUT += " to " + self.relation_person.get_name_string() + " ( " + str( self.relation_person.id ) + " )"
        
        #-- END check to see if relation_person --#
        
        # got coder details?
        if ( ( self.coder1 ) or ( self.coder2 ) or ( self.coder3 ) ):
        
            # yes.  Output a summary of coding.
            string_OUT += " - coders: "
            
            temp_string = ""
            
            if ( self.coder1 ):
            
                # output details for coder 1
                string_OUT += "1"
                temp_string += " ====> 1 - " + str( self.coder1.id ) + "; mentions: " + str( self.coder1_mention_count )
                
            #-- END check to see if coder1 --#

            if ( self.coder2 ):
            
                # output details for coder 2
                string_OUT += "2"
                temp_string += " ====> 2 - " + str( self.coder2.id ) + "; mentions: " + str( self.coder2_mention_count )
                
            #-- END check to see if coder2 --#
        
            if ( self.coder3 ):
            
                # output details for coder 3
                string_OUT += "3"
                temp_string += " ====> 3 - " + str( self.coder3.id ) + "; mentions: " + str( self.coder3_mention_count )
                
            #-- END check to see if coder3 --#
            
            string_OUT += temp_string
        
        return string_OUT

    #-- END method __str__() --#
     

#= END Reliability_Ties model ===============================================#
