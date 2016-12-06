from PIL import Image
import urllib
import boto3
import os
import re

s3 = boto3.client('s3')

def get_styles:
  p = re.compile('(\w+)=(\d+)')
  dict = {}
  for s in os.environ['STYLES'].split(';'):
    m = p.match(s)
    if m is not None:
      dict[m.group(1)] = int(m.group(2))
  return dict

def dest_key(style):
  key = urllib.unquote(params['Records'][0]['s3']['object']['key']).replace('original', style)
  print key
  return key 

def lambda_handler(params, context):
  bucket = params['Records'][0]['s3']['bucket']['name']
  src_key = urllib.unquote(params['Records'][0]['s3']['object']['key'])
  local_path = u'/tmp/tmp' + os.path.splitext(src_key)[1]

  s3.download_file(Bucket=bucket, Key=src_key, Filename=local_path)
  srcimg = Image.open(local_path, 'r')

  styles = get_styles()
  for style in styles:
    destimg = srcimg.copy()
    new_size = (styles[style], float(styles[style])/srcimg.size[0]*srcimg.size[1])
    destimg.thumbnail(new_size, Image.ANTIALIAS)
    destimg.save(local_path, 'JPEG')
    s3.upload_file(Filename=local_path, Bucket=bucket, Key=dest_key(style))

  return