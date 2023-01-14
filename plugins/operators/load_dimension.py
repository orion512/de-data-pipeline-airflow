from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    """ Custom operator to transform data for into a DIM table """

    ui_color = '#80BD9E'
    insert_sql = "INSERT INTO {} ({})"
    truncate_sql = "TRUNCATE TABLE {}"

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 select_sql="",
                 dest_table="",
                 truncate=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.select_sql = select_sql
        self.dest_table = dest_table
        self.truncate = truncate

    def execute(self, context):
        """ applies SQL transformations on staging tables and writes into a new table """
        self.log.info('LoadDimensionOperator Starting')

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.truncate:
            sql_stmt = LoadDimensionOperator.truncate_sql.format(self.dest_table)
            redshift.run(sql_stmt)

        sql_stmt = LoadDimensionOperator.insert_sql.format(
            self.dest_table,
            self.select_sql)

        redshift.run(sql_stmt)

        self.log.info('LoadDimensionOperator Done')