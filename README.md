# Sample Glue script

Simple contrived example designed to illustrate:

* Python shell job for pre-glue tasks (eg: download external file to process, and perform a simple conversion)
* PySpark example to take the input json file and create an output Parquet file
* Demonstrate the pattern for sending variables from one task to another via Workflow Parameters
* Automatically execute a Glue crawler as the last task in the workflow to populate a Glue catalog table where the subsequent table can be queried via Athena

Input file is from: `https://data.gov.au/geoserver/abc-local-stations/wfs\?request\=GetFeature\&typeName\=ckan_d534c0e9_a9bf_487b_ac8f_b7877a09d162\&outputFormat\=json` 

Steps:

1) Create an output Bucket and a bucket for your Glue scripts.
2) Update parameters.json with the stack parameters (the buckets your created above)
3) Copy convert.py and glue.py into your bucket you specified under parameter: *GlueScriptsPath*
```
$ aws s3 cp convert.py s3://GlueScriptsPath/convert.py
$ aws s3 cp glue.py s3://GlueScriptsPath/glue.py
```
4) `$ aws cloudformation create-stack --stack-name gluedemo --template-body file:///path/to/cf.yaml --parameters file:///path/to/parameters.json --capabilities CAPABILITY_NAMED_IAM`
5) `$ aws cloudformation describe-stacks  --stack-name gluedemo --query "Stacks[0].StackStatus"`

Wait. :-)
Repeat step 4 until done.

When done go into the AWS Glue Console. Look under the ETL menu on the left.  Your jobs will be listed under *Jobs*. Triggers under *Triggers* and the Workflow under *Workflows*.

Go into Workflows, and select your workflow. Go to actions and click run.  Click on history at the bottom and click on the job when it starts up and you can select *View run details*. It shows a nice GUI where the job is in the process.

Cost for this workflow should only be a few cents per execution now Glue is charged by the second!


