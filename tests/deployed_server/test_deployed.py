import json
import requests
import pytest


from tests.unit import helper

def test_sending_example_image(mocker):
    headers = {'x-api-key':'dummy'}
    data = helper.read_json_from_file('tests/local_host/resources/example.json')
    response = requests.post('https://v1l6ko3n29.execute-api.eu-central-1.amazonaws.com/default/ocr',data=data, headers=headers)

    assert(response.status_code == requests.codes.ok)
    assert(response.content == b'{"result": "G Tesseract OCR\\n\\f"}')