import json
import requests
import pytest


from tests.unit import helper

def test_sending_example_image(mocker):
    data = helper.read_json_from_file('tests/local_host/resources/example.json')
    response = requests.post('http://127.0.0.1:3000/v1/ocr',data=data)

    assert(response.status_code == requests.codes.ok)
    assert(response.content == b'{"result": "G Tesseract OCR\\n\\f"}')