import requests

aadTenant = "https://login.microsoftonline.com/"
aadTenantId = "1ed38c46-5933-4072-9caf-1e9b956330b9"

appId = "a8c9fa18-b3be-47dd-bb80-7eac4fb91fd1"
appSecret = "BW~8Q~0WKd4n9nN.M5HQ9C2BGMMNPmzOK5Ujfbtl"

fhirEndpoint = "https://fihrworkspace-fiap-challange-fhir.fhir.azurehealthcareapis.com/"

def getAuthToken():
    response = requests.post(
        aadTenant + aadTenantId + '/oauth2/token',
        data={
            'client_id': appId,
            "client_secret": appSecret,
            "grant_type": "client_credentials",
            "resource": fhirEndpoint})
    responseAsJson = response.json()

    if response.status_code != 200:
        print(response.json())
        print("\tError getting token: " + str(response.status_code))
        return None
    else:
        accessToken = responseAsJson.get('access_token')
        print("\tAAD Access Token acquired: " + accessToken[:50] + "...")
        return accessToken

def getHttpHeader(accessToken):
    return {
        "Authorization": "Bearer " + accessToken,
        "Content-type": "application/json"
    }

def printResponseResults(response):
    responseAsJson = response.json()

    if (responseAsJson.get('entry') == None):
        # Print the resource type and id of a resource. 
        printResourceData(responseAsJson)
    else:
        # Prints the resource type and ids of all resources under a bundle.
        for item in responseAsJson.get('entry'):
            resource = item['resource']
            printResourceData(resource)

def printResourceData(resource):
    resourceType = resource['resourceType']
    itemId = resource['id']
    if (resourceType == "OperationOutcome"):
        print("\t" + resource)
    else:
        itemId = resource['id']
        print("\t" + resourceType + "/" + itemId)