import json
import sys
import boto3
import requests
from botocore.exceptions import ClientError
from awsglue.utils import getResolvedOptions

#logger = glueContext.get_logger()

args = getResolvedOptions(sys.argv, ['WORKFLOW_NAME', 'WORKFLOW_RUN_ID', "bucketname"])
#job = Job(glueContext)
## @params: [JOB_NAME]
#job.init(args['JOB_NAME'], args)
glue_client = boto3.client("glue",region_name="ap-southeast-2")
s3 = boto3.resource('s3', region_name='ap-southeast-2')
workflow_name = args['WORKFLOW_NAME']
workflow_run_id = args['WORKFLOW_RUN_ID']
bucket_name = args['bucketname']
workflow_params = glue_client.get_workflow_run_properties(Name=workflow_name,
                                        RunId=workflow_run_id)["RunProperties"]

r=requests.get('https://data.gov.au/geoserver/abc-local-stations/wfs?request=GetFeature&typeName=ckan_d534c0e9_a9bf_487b_ac8f_b7877a09d162&outputFormat=json')
contents=r.json()['features']
#with open("features.json", 'r') as j:
#    contents=json.loads(j.read())
#with open('output.jsonl', 'w') as outfile:
#    for entry in contents['features']:
#        json.dump(entry, outfile)
#        outfile.write('\n')
output=""
for entry in contents:
    output = output + json.dumps(entry) + "\n"

workflow_params['jsonlines_bucket'] = bucket_name
workflow_params['jsonlines_object'] = "input"
object = s3.Object(bucket_name, 'input/abcstations.jsonl')
object.put(Body=output)
glue_client.put_workflow_run_properties(Name=workflow_name, RunId=workflow_run_id, RunProperties=workflow_params)

#job.commit()
