from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """ Custom operator to transform data for into a FACT table """

    ui_color = '#F98866'
    insert_sql = "INSERT INTO {} ({})"

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 select_sql="",
                 dest_table="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.select_sql = select_sql
        self.dest_table = dest_table

    def execute(self, context):
        """ applies SQL transformations on staging tables and writes into a new table """
        self.log.info('LoadFactOperator started')

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        sql_stmt = LoadFactOperator.insert_sql.format(
            self.dest_table,
            self.select_sql)

        redshift.run(sql_stmt)

        self.log.info('LoadFactOperator Done')
