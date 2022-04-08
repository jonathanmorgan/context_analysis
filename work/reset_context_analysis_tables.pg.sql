DROP TABLE context_analysis_field_spec_value;
DROP TABLE context_analysis_reliability_names_coder_data;
DROP TABLE context_analysis_reliability_names_eval_article_datas;
DROP TABLE context_analysis_reliability_names_eval_merged_from_ad;
DROP TABLE context_analysis_reliability_names_eval_merged_to_ad;
DROP TABLE context_analysis_reliability_names_eval_persons;
DROP TABLE context_analysis_reliability_names_eval;
DROP TABLE context_analysis_reliability_names;
DROP TABLE context_analysis_reliability_result_details;
DROP TABLE context_analysis_reliability_names_results;
DROP TABLE context_analysis_field_spec;
DROP TABLE context_analysis_reliability_ties;

-- remove migration log from django_migrations table so we can re-migrate.
DELETE FROM django_migrations WHERE app = 'context_analysis';