'''
    * File author: Ibrahima DIOP (iad).
    * License: For non commercial use only.
'''
from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

start_date = datetime(2018, 01, 1)
end_date = datetime(2019, 02, 10)

default_args = {
    'owner': 'iad',
    'start_date': start_date,
    'end_date': end_date,
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

# DAG Setup
dag = DAG('sparkify_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

# Create staging event table operator to Redshift
stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_events",
    s3_bucket="udacity-dend",
    s3_key="log_data",
    json_path="s3://udacity-dend/log_json_path.json",
    region="us-west-2",
    file_format="JSON",

    execution_date=start_date,
    provide_context=True,
)

# Create staging songs table operator to Redshift
stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_songs",
    s3_bucket="udacity-dend",
    s3_key="song_data/A/A/A",
    region="us-west-2",
    file_format="JSON",
    execution_date=start_date,
    provide_context=True,
)

# Load songplays fact table
load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    provide_context=True,
    redshift_conn_id="redshift",
    sql_query=SqlQueries.songplay_table_insert
)

# Load user dimension table
load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="users",
    truncate_table=True,
    select_query=SqlQueries.user_table_insert
)

# Load song dimension table
load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag
)

# Load artist dimension table
load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table='artists',
    sql_stmt=SqlQueries.artist_table_insert
)

# Load time dimension table
load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table='time',
    sql_stmt=SqlQueries.time_table_insert
)

# Data quality checking
run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tables=['songplays', 'users', 'songs', 'artists', 'time']
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# DAG diagram

start_operator >> stage_songs_to_redshift
start_operator >> stage_events_to_redshift

stage_songs_to_redshift >> load_songplays_table
stage_events_to_redshift >> load_songplays_table

load_songplays_table >> load_song_dimension_table
load_songplays_table >> load_user_dimension_table
load_songplays_table >> load_artist_dimension_table
load_songplays_table >> load_time_dimension_table

load_user_dimension_table >> run_quality_checks
load_song_dimension_table >> run_quality_checks
load_artist_dimension_table >> run_quality_checks
load_time_dimension_table >> run_quality_checks

run_quality_checks >> end_operator
