from PIL import Image
import urllib
import boto3
import os
import re

s3 = boto3.client('s3')

def get_sizes():
  p = re.compile('(\w+)=(\d+)')
  dict = {}
  for s in os.environ['STYLES'].split(';'):
    m = p.match(s)
    if m is not None:
      dict[m.group(1)] = int(m.group(2))
  return dict

def extract_hash(key):
  p = re.compile('\/([0-9a-z]{40})\/')
  return p.search(key).group(1)

def lambda_handler(params, context):

  for record in params['Records']:
    bucket = record['s3']['bucket']['name']
    src_key = record['s3']['object']['key']
    hash_key = extract_hash(src_key)
    local_path = u'/tmp/tmp' + os.path.splitext(src_key)[1]

    s3.download_file(Bucket=bucket, Key=src_key, Filename=local_path)
    srcimg = Image.open(local_path, 'r')

    sizes = get_sizes()
    for style in sizes:
      new_size = (sizes[style], float(sizes[style])/srcimg.size[0]*srcimg.size[1])

      destimg = srcimg.copy()
      destimg.thumbnail(new_size, Image.ANTIALIAS)
      destimg.save(local_path, 'JPEG')

      dest_key = '/thumbnails/%s/%s.jpg' % (hash_key, style)
      s3.upload_file(Filename=local_path, Bucket=bucket, Key=dest_key)

  return