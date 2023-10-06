import json
import requests
from utils import getAuthToken, getHttpHeader

aadTenant = "https://login.microsoftonline.com/"
aadTenantId = "1ed38c46-5933-4072-9caf-1e9b956330b9"

appId = "a8c9fa18-b3be-47dd-bb80-7eac4fb91fd1"
appSecret = "BW~8Q~0WKd4n9nN.M5HQ9C2BGMMNPmzOK5Ujfbtl"

fhirEndpoint = "https://fihrworkspace-fiap-challange-fhir.fhir.azurehealthcareapis.com/"


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

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    print(event)
    body = event.get('body')
    if isinstance(body, str):
        patient_data = json.loads(body)
    else:
        patient_data = body
    result, status_code = postPatient(getAuthToken(), patient_data)
    return {
        'statusCode': status_code,
        'body': json.dumps(result)
        }

def postPatient(accessToken, patientData):
    if isinstance(patientData, str):
        patientData = json.loads(patientData)

    response = requests.post(
        url= fhirEndpoint + 'Patient',
        json= patientData,
        headers= getHttpHeader(accessToken))
    responseAsJson = response.json()
    
    if response.status_code == 200 or response.status_code == 201:
        resourceId = responseAsJson.get('id')
        print("\tPatient ingested: " + resourceId + ". HTTP " + str(response.status_code))
        return resourceId, response.status_code
    else:
        print("\tError persisting patient: " + str(response.status_code))
        return None, response.status_code

