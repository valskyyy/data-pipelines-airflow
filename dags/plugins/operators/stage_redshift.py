from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    template_fields=("s3_key",)
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key

    def execute(self, context):
    # Étape 1 - Connexion AWS
        self.log.info("Connecting to AWS")
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()

    # Étape 2 - Connexion Redshift
        self.log.info("Connecting to Redshift")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

    # Étape 3 - Vider la table
        self.log.info(f"Clearing data from {self.table}")
        redshift.run(f"DELETE FROM {self.table}")

    # Étape 4 - Copier les données depuis S3
        self.log.info(f"Copying data from S3 to Redshift table {self.table}")
        s3_path = f"s3://{self.s3_bucket}/{self.s3_key}"
        sql = f"""
            COPY {self.table}
            FROM '{s3_path}'
            ACCESS_KEY_ID '{credentials.access_key}'
            SECRET_ACCESS_KEY '{credentials.secret_key}'
            FORMAT AS JSON 'auto'
    """
        redshift.run(sql)





