import os
import json

from subprocess import check_output

try:    
    import transform
except ModuleNotFoundError:
    from . import transform

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SCRIPT_DIR, 'lib')

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
   

    if not event['body']:
        return {'statusCode': 400,
                'body': json.dumps({'result': 'Bad Request!'})}

    
    decoded_payload = transform.decode_from_json(event['body'])
    
    if not decoded_payload:
        return {'statusCode': 415,
                'body': json.dumps({'result': 'Unsupported Media Type!'})}

    data = json.loads(event['body'])

    if 'language' in data:
        language = data['language']
    else:
        language = 'eng'


    image_file = '/tmp/image.{}'.format(data['type'])

    with open(image_file, 'wb') as fid:
        fid.write(decoded_payload)
    

      
    command = 'LD_LIBRARY_PATH={} TESSDATA_PREFIX={} ./tesseract {} stdout -l {}'.format(
            LIB_DIR,
            SCRIPT_DIR+'/tessdata',
            image_file,
            language
        )

    try: 
        output = check_output(command, shell=True) 
        result = str(output,'utf-8')

    except :
        result = "Failed executing: {}".format(command)
        pass

    return { 'statusCode': 200,
             'body': json.dumps({'result': result})}
