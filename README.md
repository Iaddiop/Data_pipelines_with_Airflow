# Data Warehouse with Amazon Redshift, S3 and Airflow
In the precedent project [Data Warehouse with Amazon Redshift](https://github.com/Iaddiop/Cloud_Data_Warehouse) we explain how to build a data warehouse with redshift and S3. In this project, we will build the same data warehouse with Airflow to manage and orchestration data pipelines.

We will build data pipelines for :
- Reusable tasks,
- Allow easy backfills,
- Play data quality after the ETL steps

Below the digram that explain the pipeline process : ![image info](./dag.png)

Different steps will be taken in this project:
- Create a [Redshift cluster for the DWH](https://github.com/Iaddiop/Cloud_Data_Warehouse/blob/master/Creating%20Redshift%20Cluster.ipynb)
- create operators for :
    * Loading staging tables in redshift DB
    * Loading fact table  : songplays
    * Loading dimension tables : users, songs, artists, time
    * Data quality checking
- Create The DAG

## Data Sources :
The data stored in 2 datasets that reside in S3 :
- [Song_data](s3://udacity-dend/song_data) : JSON files covered the main activities fo the users of the music app
- [Log_data](s3://udacity-dend/log_data) : JSON metadata about users
And the log data [json path](s3://udacity-dend/log_json_path.json)

## Data modeling :
We will use the relational database to modeling the data and the star schema concept, like we did in the [Data Warehouse with Amazon Redshift](https://github.com/Iaddiop/Cloud_Data_Warehouse) project

## How to run this project :
To run this project, please folowing the below steps :

1 - Create Redshift cluster : run the Jupyter Notebook to create [Redshift cluster](https://github.com/Iaddiop/Cloud_Data_Warehouse/blob/master/Creating%20Redshift%20Cluster.ipynb)

2 - Create operators

3 - Create DAG for the data pipelines

## Data quality checking :

**- songplays** : 333 rows

**- users** : 105 rows

**- songs** : 14896 rows

**- artists** : 10025 rows

**- time** : 333 rows
