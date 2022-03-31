from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_statement="",
                 table="",
                 truncate=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_statement = sql_query
        self.table = table
        self.truncate = truncate

    def execute(self, context):
        """
        Description : Loading data from staging table to dimension tables
        Truncating data from dimension tables before inserting new data
        """
        self.log.info(f"Loading data to {self.table} dimension table")

        redshift = PostgresHook(self.redshift_conn_id)

        if self.truncate:
            self.log.info(f"Truncating {self.table} before inserting new data...")
            redshift.run(f"truncated table {self.table}")

        redshift.run(self.sql_statement.format(self.table))
        self.log.info(f"End of loading data to {table} dimension table")
