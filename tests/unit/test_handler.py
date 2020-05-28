import json
import os
import base64

import pytest

from tests.unit import helper

from main import app
from main import transform


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    image_file = "tests/unit/resources/example.png"
    json_payload = transform.encode_to_json(image_file)

    return {
        "body": json_payload,
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "GET",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }

def test_image_to_json_and_back(apigw_event, mocker):
    image_file = "tests/unit/resources/example.png"

    with open(image_file, 'rb') as fid:
        raw_image_data = fid.read()

    json_payload = transform.encode_to_json(image_file)
    decoded_data = transform.decode_from_json(json_payload)        
    assert(raw_image_data == decoded_data)

def test_trivial_write_and_read(apigw_event, mocker):
    image_file  = "tests/unit/resources/example.png"
    json_file   = "tests/unit/resources/example.json"

    json_payload = transform.encode_to_json(image_file)
    helper.save_json_to_file(json_payload , json_file)

    json_file_content = helper.read_json_from_file(json_file)

    assert(json_file_content == json_payload)

def lambda_handler(apigw_event, mocker):
    app.check_output = mocker.MagicMock(return_value=b'G Tesseract OCR')

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret['body'])

    assert ret["statusCode"] == 200
    assert "result" in ret['body']    
    assert("Tesseract" in data['result'])

def test_bad_request(apigw_event):
    apigw_event['body'] = ''
    ret = app.lambda_handler(apigw_event, "")

    assert(ret['statusCode'] == 400)
    assert 'Bad Request!' in ret['body']

def test_unsupported_media_type(apigw_event, mocker):
    app.check_output = mocker.MagicMock(return_value=b'G Tesseract OCR')

    apigw_event['body'] = 'encoding'
    ret = app.lambda_handler(apigw_event, "")

    assert(ret['statusCode'] == 415)
    assert 'Unsupported Media Type!' in ret['body']

    apigw_event['body'] =  json.dumps({'encoding':'', 'payload':'PUks1Q1lJST0iCn0='})
    ret = app.lambda_handler(apigw_event, "")

    assert(ret['statusCode'] == 415)
    assert 'Unsupported Media Type!' in ret['body']

    apigw_event['body'] =  json.dumps({ 'encoding':'base64',
                                        'type' : 'png',
                                        'payload':'PUks1Q1lJST0iCn0='})
    ret = app.lambda_handler(apigw_event, "")   
    assert(ret['statusCode'] == 200)

def test_dev(apigw_event, mocker):
    helper.covert_image_to_json('tests/unit/resources/phototest.tif','tests/unit/resources/phototest.json')