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
        occurrence_resource = json.loads(body)
    else:
        occurrence_resource = body
    result, status_code = create_occurrence(occurrence_resource, getAuthToken())
    return {
        'statusCode': status_code,
        'body': json.dumps(result)
        }

def create_occurrence(occurrence_resource, accessToken):
    # Create a new FHIR resource representing the occurrence
    # occurrence_resource = {
    #     "resourceType": "Observation",
    #     "status": "final",
    #     "code": {
    #         "coding": [
    #             {
    #                 "system": "http://loinc.org",
    #                 "code": observation_code,
    #                 "display": "Some Observation"
    #             }
    #         ],
    #         "text": "Some Observation"
    #     },
    #     "subject": {
    #         "reference": patient_reference
    #     },
    #     "valueQuantity": {
    #         "value": value,
    #         "unit": unit
    #     }
    # }

    # Send a POST request to create the new occurrence
    baseUrl = fhirEndpoint + 'Observation/'
    response = requests.post(baseUrl, json=occurrence_resource, headers=getHttpHeader(accessToken))

    # Check the response for success or handle any errors
    if response.status_code == 201 or response.status_code == 200:
        print("Occurrence registered successfully.")
        return response.json(), response.status_code
    else:
        print(f"Failed to register occurrence. Status code: {response.status_code}")
        print(response.text)
        return None, response.status_code

