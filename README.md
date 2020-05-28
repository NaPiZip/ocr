<img src="https://blog.scottlogic.com/dsmith/assets/featured/aws-logo.png" alt="AWS logo" height="42px" width="84px" align="left"><br>

# REST API OCR parser with AWS Lambda and Tesseract
<div>
    <a href="https://github.com/NaPiZip/Tipps-and-tricks">
        <img src="https://img.shields.io/badge/Document%20Version-0.0.1-brightgreen"/>
    </a>  
</div>

# Introduction
In this project I would like to improve my skills in and knowledge about the `AWS Lambda` service. I would like create a REST API which I can send an image file or in some way the raw image data. After the API requests, the invoked Lambda function should extract the text out of the image using a optical character recognition (OCR) library called Tesseract. It's important to say that I want to run tesseract as a `elf` file, since this means I could use the same approach to run any application which I can build on the EC2 instance. A pretty similar example can be found [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-example-s3.html).

The plan is to use `python 3.8` as well es the following libs:
- tesseract-ocr

The REST API endpoint should be `v1/ocr` using a POST request. I am sending data in the json format, optionally I will support compression. The json data looks as followed:

```python
{ 'name':         'some_file_name',  // The optional file name 
  'type':         'jpg',             // The raw image format type 
  'encoding':     'base64',          // The encoding scheme of the payload: {'base64'}
  'compression':  '',                // The optional compression of the payload applied before encoding: {''}
  'language':     'eng',             // The ocr language: {'eng', 'deu'}
  'payload':      'iVBORw0KGgoAAAAN...'})
```

## Prerequisite
In order to use `tesseract` in labmda there is a little bit of work needed, since its not availible inside the lambda instance. I need to build the source code and provide the binary to the lambda function. The aws documentation [link](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html), provides the following information about the python 3.8 environment:

| Name | Identifier | AWS SDK for Python | Operating System |
| :------------- | :------------- | :------------- | :------------- | 
| Python 3.8 | python3.8 |boto3-1.12.22 botocore-1.15.22 | Amazon Linux 2 |
	
In order to build everything, I am folowing this stackoverflow [post](https://stackoverflow.com/questions/33588262/tesseract-ocr-on-aws-lambda-via-virtualenv). After building an packaging all into a `.zip` file, the functionality can be tested as follow:
```
$ cd tesseract-lambda 

tesseract-lambda$ export LD_LIBRARY_PATH=$PWD/lib
tesseract-lambda$ export TESSDATA_PREFIX=/PWD/tessdata

tesseract-lambda$ ./tesseract --help
```
**Notes**
After building `leptonica` you need to make sure the linker is able to find the library files, after `make install`. I therfore made a sybolic link to the `pkgconfig` file:
```
$ cd /usr/lib64/pkgconf
$ sudo ln -s /usr/local/lib/pkgconfig/lept.pc lept.pc
```
## The Toolchain
I am using `SAM` and `localstack` for development, they can both be executed locally, this comes in handy for development, so you don't have to actually use the paid AWS service.

<p align="center">
<img src="https://image.slidesharecdn.com/09112017-serverless-local-test-92e8f092-7d1c-43e4-809c-a40335e29637-2097706900-170913194001/95/local-testing-and-deployment-best-practices-for-serverless-applications-aws-online-tech-talks-19-638.jpg?cb=1505331628" alt="SAM example"/></p>

The AWS Serverless Application Model (SAM) is an open-source framework for building serverless applications. It provides shorthand syntax to express functions, APIs, databases, and event source mappings. With just a few lines of configuration, you can define the application you want and model it." see [here](https://github.com/awslabs/aws-sam-cli).

I use `localstack` for testing purposes. `localstack` is a nice tool for running AWS services locally, see [link](https://localstack.cloud/).

## Getting it done
After getting Tesseract to run there was not much to do, just plain coding. I think it is very important to make sure the code is tested this is why I created unit tests to test the basic functionallity. The next step was running the api locally and testing the endpoints with a real post request. The followig snippet shows the local endpoint tests.
```python
def test_sending_example_image(mocker):
    data = helper.read_json_from_file('tests/local_host/resources/example.json')
    response = requests.post('http://127.0.0.1:3000/v1/ocr',data=data)

    assert(response.status_code == requests.codes.ok)
    assert(response.content == b'{"result": "G Tesseract OCR\\n\\f"}')
```
Here is an example of an image I used to test the lamda function:
<p align="center">
<img src="https://github.com/NaPiZip/Online-course-notes/raw/master/AWS_cloud/Fundational_level/s3_ocr_lambda/ocr/tests/unit/resources/phototest.tif" alt="ocr parsed text"/></p>
And the result:<br>

```python
{"statusCode":200,
"body":
"{\"result\": \"This is a lot of 12 point text to test the\\nocr code and see if it works on all types\\nof file format.\\n\\nThe quick brown dog jumped over the\\nlazy fox. The quick brown dog jumped\\nover the lazy fox. The quick brown dog\\njumped over the lazy fox. The quick\\nbrown dog jumped over the lazy fox.\\n\\f\"}"}
```

## Contributing
To get started with contributing to my GitHub repository, please contact me [Slack](https://join.slack.com/t/napi-friends/shared_invite/enQtNDg3OTg5NDc1NzUxLWU1MWNhNmY3ZTVmY2FkMDM1ODg1MWNlMDIyYTk1OTg4OThhYzgyNDc3ZmE5NzM1ZTM2ZDQwZGI0ZjU2M2JlNDU).
