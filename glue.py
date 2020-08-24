import sys
import re
import boto3
import json
import logging
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
args = getResolvedOptions(sys.argv, ['JOB_NAME','WORKFLOW_NAME', 'WORKFLOW_RUN_ID'])
job = Job(glueContext)
glue_client = boto3.client("glue")
workflow_name = args['WORKFLOW_NAME']
workflow_run_id = args['WORKFLOW_RUN_ID']
workflow_params = glue_client.get_workflow_run_properties(Name=workflow_name,
                                                RunId=workflow_run_id)["RunProperties"]

prefix = "s3://" + workflow_params['jsonlines_bucket'] + "/" + workflow_params['jsonlines_object']
output = "s3://" + workflow_params['jsonlines_bucket'] + "/abcstations"

logger = glueContext.get_logger()
logger.info("prefix: {}".format(prefix))
logger.info("output: {}".format(output))
## @params: [JOB_NAME]
job.init(args['JOB_NAME'], args)

dynamic_frame = glueContext.create_dynamic_frame_from_options(
        connection_type="s3",
        format="json",
        connection_options={
#           "paths" : ["s3://mig-test-bucket/input"]
           "paths" : [prefix]
        },
        transformation_ctx="dynamic_frame") #optional - needed if you are using bookmarks

# printSchema() doesnt save to a variable 
# myschema=dynamic_frame.printSchema()
myschema=dynamic_frame._jdf.schema().treeString()
logger.info("{}".format(myschema))

# Perform transformations here if you need
#
#

# Glue just adds a new parquet file to output with the data - in this case it leads to duplicate data so use a spark df frame with overwrite mode instead.
#finalsink=glueContext.write_dynamic_frame.from_options(
#            frame = dynamic_frame,
#            connection_type = "s3",
#            #connection_options = {"path": "s3://mig-test-bucket/parquet" },
#            connection_options = {"path": output },
#            # Optional parition key
#            #connection_options = {"path": "s3://bucket/prefix/to/parquet","partitionKeys" : ['partionkey1','paritionkey2']},
#            format = "parquet",
#            transformation_ctx = "finalsink")

spark_df = dynamic_frame.toDF()
spark_df.write.mode('overwrite').parquet(output)

job.commit()
