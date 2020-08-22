# Sample Glue script

Quick n dirty script to take a json lines input file (or all files from the prefix specified in the script) and creates a parquet output file for demo purposes.  Create a glue crawler on the output file to query in Athena.

Input file from: 

`$ http --download https://data.gov.au/geoserver/abc-local-stations/wfs\?request\=GetFeature\&typeName\=ckan_d534c0e9_a9bf_487b_ac8f_b7877a09d162\&outputFormat\=json`

`$ cat features.json| jq .features> out.json`

`$ python3 convert.py`

`$ aws s3 cp output.jsonl s3://mig-test-bucket/output.json1`

The above could all be done with a python job in a workflow. (TODO!)

Create a Glue job with the glue.py as the script.
Ensure the Glue IAM service role has the AWSGlueServiceRole attached as well as a custom policy to read/write your s3 bucket.



