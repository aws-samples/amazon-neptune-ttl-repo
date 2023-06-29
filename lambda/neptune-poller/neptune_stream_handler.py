'''
Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
'''

import boto3
import json
import redis
import logging
import os
import lambda_function
from commons import *
from handler import AbstractHandler, HandlerResponse

logger = logging.getLogger('NeptuneStreamHandler')
logger.setLevel(logging.INFO)

def add_ttl(batch, obj_id, obj_type, ttl):
    print("Add TTL " + str(obj_id) + " " + str(obj_type) + " " + str(ttl))
    batch.put_item(
        Item = {
            'ObjectId': obj_id,
            'ObjectType': obj_type,
            'TTL': ttl,
            'source': 'neptuneStreams'
       })


class NeptuneStreamHandler(AbstractHandler):

    def handle_records(self, stream_log):
        
        params = json.loads(os.environ['AdditionalParams'])
        table = params['dynamodb_table']
        neptuneEndpoint = 'https://' + params['neptune_endpoint'] + ':8182/pg/stream'
        
        records = stream_log[RECORDS_STR]
        
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(table)
            
            with table.batch_writer() as batch: # use Dynamo batch writer
                for record in records:
                    obj_id = record[DATA_STR]['id']
                    obj_type = record[DATA_STR]['type']
                    key = record[DATA_STR]['key']
                    val = record[DATA_STR]['value']['value']
                    
                    if record[OPERATION_STR] == ADD_OPERATION:
                        print(str(obj_id) + " " + str(obj_type) + " " + str(key) + " " + str(val))
                        if obj_type == "vp" and key == "TTL":
                            add_ttl(batch, obj_id, "vertex", val)
                        elif obj_type == "ep" and key == "TTL": 
                            add_ttl(batch, obj_id, "edge", val)
                    yield HandlerResponse(
                        record[EVENT_ID_STR][OP_NUM_STR],
                        record[EVENT_ID_STR][COMMIT_NUM_STR],
                        1)
            
        except Exception as e:
            logger.error('Error occurred - {}'.format(str(e)))
            raise e

       
        
            
        

