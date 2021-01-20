from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from helpers import SqlQueries


class LoadDimensionOperator(BaseOperator):
    """
    This class operator receives a redshift connection id, a table, an sql query and if the query should be of append or rewrite mode.
    What this class does is delete the records of a input sql table if the append mode is set to false and then loads new data using the input sql query.
    All the outputs are kept in a log.
    """

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 table = "", 
                 sql = "",
                 append_mode = False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql
        self.append_mode = append_mode

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.append_mode == False:
            self.log.info(f"Deleting records from {self.table} table")
            redshift.run(f"DELETE FROM {self.table}")
            
        load_sql_query = getattr(SqlQueries, self.sql)
        redshift.run(load_sql_query)
        self.log.info(f"Loaded {self.table} data into dimension table")
