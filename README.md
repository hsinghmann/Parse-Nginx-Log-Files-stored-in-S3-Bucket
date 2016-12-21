# Parse-Nginx-Log-Files-stored-in-S3-Bucket

This Python script parses Nginx log files stored in S3 Bucket doing some simple filtering and computes summary statistics.
Log files are stored in S3 and the script uses 'boto' to access files on it.
The files are gzip compressed Nginx Access Logs generated with the following log_format directive:

log_format proxy_combined
           '$remote_addr - $remote_user [$time_local] '
           '"$request" $status $body_bytes_sent '
           '"$http_referer" "$http_user_agent" $request_time $pipe '
           'upstream: $upstream_addr '
           '$upstream_status $upstream_response_time';

For more information on log formats see: http://nginx.org/en/docs/http/ngx_http_log_module.html#log_format

Log files are named in the format: yyyy-MM-dd-${SERVICE_NAME}-access.log.gz

This is a standalone script that takes 'Date' and 'SERVICE_NAME' as two command line arguments.

The script does preprocessing along with some filtering and generates the following statistics:

1. Average and Max response time
2. Average and Max upstream response time
3. Count of HTTP codes by endpoints
