import boto
from boto.s3.connection import S3Connection
import boto.s3.connection

access_key = 'AKIAI5BVKG64ZM2VUDBA'
secret_key = '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'

bucket_name = access_key.lower() + '-dump'
conn = boto.connect_s3(access_key, secret_key)

mybucket = conn.get_bucket('jordan-barber')

plans_key = mybucket.get_key('total_trigrams.csv')
plans_url = plans_key.generate_url(3600, query_auth=True, force_http=True)
print(plans_url)