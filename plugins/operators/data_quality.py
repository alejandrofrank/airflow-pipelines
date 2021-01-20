from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
    This class operator checks the amount of rows inside of tables passed as a list when called.
    For every table inside the input list, it will log if there are errors inside the table or if everything is ok.
    """

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 tables = [],
                 dq_checks = [],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables
        self.dq_checks = dq_checks

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        for table in self.tables:
            for test in self.dq_checks:
                self.log.info(f"Checking: {table} table")
                query = test.get('check_sql')
                records = redshift.get_records(query.format(table))
                if len(records) == query.get('expected_result') or len(records[0]) == query.get('expected_result'):
                    raise ValueError(f"ERROR no records: {table} table")
                if records[0][0] == query.get('expected_result'):
                    raise ValueError(f"ERROR no rows: {table} table")
                self.log.info(f"Table {table} passed the test with {records[0][0]} records")