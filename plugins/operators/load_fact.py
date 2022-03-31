from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_statement = '',
                 table="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_statement = sql_statement
        self.table = table

    def execute(self, context):
        """
        Description : Loading data from staging table to fact table
        """
        self.log.info(f"Loading data to {self.table} fact table")

        redshift_hook = PostgresHook(self.redshift_conn_id)
        redshift_hook.run(str(self.sql_statement))

        self.log.info(f"End of loading data to {table} fact table")
