import requests

class APIConnectorService:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def get_response_for(self, endpoint, endpoint_params=''):
        headers = {'x-api-key': self.api_key}
        response = requests.get(
            f'{self.base_url}/{endpoint}',
            headers=headers,
            params=endpoint_params
        )
        return response

    def get_json_response(self, endpoint, params=''):
        response = self.get_response_for(endpoint, params)
        if response.status_code == 200:
            json = response.json()
            return json
        raise Exception(f'Error raised for {self.base_url}/{endpoint}', response)

    def get_typed_response_cookiemaps_01(self, endpoint, params=''):
        response = self.get_json_response(endpoint, params)
        if(response['success'] != True or type(response) != type({})):
            return response
        if('ok' in list(response.keys())):
            response = response['ok']
        if ('data' in list(response.keys())):
            response=response['data']
        required_keys = [
            "agentName","mindshare", "marketCap", "liquidity", "price", "averageEngagementsCount"
        ]
        if(type(response) == type([])):
            responseList = list(response)
            filteredResponseList = []
            for responseElem in responseList:
                currKeys = list(responseElem.keys())
                requiredElem = {}
                for k in required_keys:
                    if not k in currKeys: # Just return the obtained response earlier
                        return list(response)
                    requiredElem[k] = responseElem[k]
                filteredResponseList.append(requiredElem)
            return filteredResponseList
        required_response = {}
        for key in required_keys:
            if not key in list(response.keys()):
                return response # Return the response as it is ...
            required_response[key] = response[key]
        return required_response
