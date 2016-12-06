from PIL import Image
import json
import urllib
import random
import boto3
import os
import re

s3 = boto3.client('s3')

def get_styles(context):
  client = boto3.client('lambda')
  response = client.get_function_configuration(FunctionName=context.function_name)
  desc = json.loads(response['Description'])
  desc['original'] = None
  return desc

def random_string(length, seq='0123456789abcdefghijklmnopqrstuvwxyz'):
  sr = random.SystemRandom()
  return ''.join([sr.choice(seq) for i in xrange(length)])

def dest_file_path(style):
  return '%s/%s.jpg' % ('output', style)

def lambda_handler(params, context):
  bucket = params['Records'][0]['s3']['bucket']['name']
  key = urllib.unquote(params['Records'][0]['s3']['object']['key'])
  local_path = u'/tmp/' + random_string(16) + os.path.splitext(key)[1]

  s3.download_file(Bucket=bucket, Key=key, Filename=local_path)
  srcimg = Image.open(local_path, 'r')

  styles = get_styles(context)
  for style in styles:
    tmp_img = srcimg.copy()
    if styles[style] is not None:
      new_size = (styles[style], float(styles[style])/srcimg.size[0]*srcimg.size[1])
      tmp_img.thumbnail(new_size, Image.ANTIALIAS)
    tmp_img.save(local_path, 'JPEG')
    s3.upload_file(Filename=local_path, Bucket=bucket, Key=dest_file_path(style))

  s3.delete_object(Bucket=bucket, Key=key)
  return