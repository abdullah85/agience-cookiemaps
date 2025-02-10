import requests
from fastapi import HTTPException

# The backend to connect to the API endpoint
class APIConnectorService:
    def __init__(self, api_key, base_url):
        '''
        Provide API key and base_url for making the request.
        '''
        self.api_key = api_key
        self.base_url = base_url

    def get_json_response(self, endpoint, endpoint_params=''):
        '''
        Return the json response for the endpoint with endpoint_params as parameters.
        '''
        headers = {'x-api-key': self.api_key}
        try:
            response = requests.get(f'{self.base_url}/{endpoint}', headers=headers, params=endpoint_params)
            response.raise_for_status()
            # TODO: Perform appropriate logging
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            raise HTTPException(status_code=response.status_code, detail=f"HTTP error: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
            raise HTTPException(status_code=500, detail="An error occurred while fetching data from the Cookie API.")
