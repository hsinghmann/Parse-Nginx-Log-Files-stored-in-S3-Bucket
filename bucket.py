'''
Name: Harshdeep Singh Mann
'''
import sys
import re
import gzip
from boto.s3.key import Key
import boto.s3.connection

AWS_ACCESS_KEY_ID = 'Your Key'   # My Key ID
AWS_SECRET_ACCESS_KEY = 'Your Secret Access'  # My secret access key
Bucketname = 'Your Bucket Name'  # Bucket Name

'''
Connecting to S3 Bucket
'''
conn = boto.s3.connect_to_region('us-west-2',
       aws_access_key_id=AWS_ACCESS_KEY_ID,
       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
       is_secure=True,
       calling_format = boto.s3.connection.OrdinaryCallingFormat(),)
bucket = conn.get_bucket(Bucketname)

'''
Downloading files from the bucket
'''
for key in bucket.list():
    try:
        res = key.get_contents_to_filename(key.name)
    except:
        logging.info(key.name+":"+"FAILED")


date = sys.argv[1] # Date
service = sys.argv[2] # Service Name
filename = date+"-"+service+"-"+"access.log.gz" # Filename
f = gzip.open(filename, 'r') # Using gzip to open .gz file
index1 = [] # list for reponse time
index2 = [] # list for upstream response time
code = []   # list for HTTP Code
for line in f:
	if '"-" 400' not in line:    # filtering lines which do NOT have "-" 400
		new_set = re.sub(r'\"(.+?)\"','',line).replace('-', '')   # removing all the elements in double quotes
		response = new_set.split(' ')[10] # response time is column 10
		upstream = new_set.split(' ')[15] # upstream time is column 15
		count = new_set.split(' ')[6]     # count is column 6
		index1.append(response.strip())   # append response time to index1
		index2.append(upstream.strip())   # append upstream time to index2
		code.append(count.strip())        # append HTTP code to code list
# print index
# print len(index)

print '------------------------------------------------------------------'
response_sum = 0  # reponse time sum
for i in index1:
	if i != '':    # filtering lines which are empty
		response_sum += float(i)  # computing sum
		avg_response = response_sum/len(index1)  # computing average
print "The sum of response time is: %s" % response_sum
print "The average of response time is: %s" % avg_response
print "The maximum value of upstream response time is: %s" % max(index1)  # computing max
print '------------------------------------------------------------------'

print '------------------------------------------------------------------'
print "Count of HTTP codes is: %s" % len(code)  # count the occurence of HTTP Code which is the total length of the list
print '------------------------------------------------------------------'
print '------------------------------------------------------------------'

upstream_sum = 0  # upstream time sum
for i in index2:
	if i != '': # filtering lines which are empty
		upstream_sum += float(i)  # computing sum
		avg_upstream = upstream_sum/len(index2) # computing average
print "The sum of upstream response time is: %s" % upstream_sum
print "The average of upstream response time is: %s" % avg_upstream
print "The maximum value of upstream response time is: %s" % max(index2)  # computing max
print '------------------------------------------------------------------'
