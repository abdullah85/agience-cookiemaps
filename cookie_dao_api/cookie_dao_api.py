
from dotenv import load_dotenv
from api_connecter_service import APIConnectorService

# Organized for accessing the DAO API
class CookieDaoAPI:
    def __init__(self, api_key, cached=False):
        self.endpoints = {
            'auth'              : 'authorization',
            'search'            : 'v1/hackathon/search',
            'twitterUserName'   : 'v2/agents/twitterUsername',
            'contractAddress'   : 'v2/agents/contractAddress',
            'agentsPaged'       : 'v2/agents/agentsPaged'
        }
        self.options = list(self.endpoints.keys())        
        # Start out with default params initialized within this object and modified as needed
        self.params = {
            'address'       : '0xc0041ef357b183448b235a8ea73ce4e4ec8c265f',            
            'from'          : "2025-01-01",
            'interval'      : 7,
            'limit'         : 5,
            'page'          : 1,
            'page_size'     : 25,
            'search_term'   : "cookie%20token%20utility",
            'to'            : "2025-01-20",
            'user_name'     :'cookiedotfun',
        }
        self.connector = APIConnectorService(api_key, 'https://api.cookie.fun')

    def get_authorization(self):
        auth_endpoint = self.endpoints['auth']
        response = self.connector.get_json_response(auth_endpoint)
        return response

    def get_hackathon_search(self):
        search_endpoint = self.endpoints['search'] +'/' + self.params['search_term']
        params = {
            'from': self.params['from'],
            'to'  : self.params['to']
        }
        response = self.connector.get_json_response(search_endpoint, params)
        return response

    def get_twitter_username(self):
        twitter_endpoint = self.endpoints['twitterUserName'] + '/' + self.params['user_name']
        params = { 'interval': f'_{self.params['interval']}days'}
        response = self.connector.get_json_response(twitter_endpoint, params)
        return response

    def get_contract_address(self):
        ca_endpoint = self.endpoints['contractAddress'] + '/' + self.params['address']
        params = { 'interval': f'_{self.params['interval']}days'}
        response = self.connector.get_json_response(ca_endpoint, params)
        return response

    def get_agents_paged(self):
        '''
        Obtain the agents for a particular page, pagesize from the endpoint provided
        '''
        agents_endpoint = self.endpoints['agentsPaged']
        params = { 'interval': f'_{self.params['interval']}days', 'page': self.params['page'], 'pageSize': self.params['page_size']}
        response = self.connector.get_json_response(agents_endpoint, params)
        return response

    def extract_agents_data(self, response):
        data = []
        if(type(response) == type({}) and 'ok' in response.keys()):
            if(type(response['ok']) == type({}) and 'data' in response['ok'].keys()):
                data = response['ok']['data']
            else:
                raise Exception('data attribute not present in response')
        else:
            raise Exception('response provided is not correct')
        return data

    def get_agents_filtered(self):
        '''
        Obtain the list of agents upto the limit (by collating multiple pages)
        '''
        agents_endpoint     = self.endpoints['agentsPaged']
        page_size           = self.params['page_size']
        limit               = int(self.params['limit'])
        if(limit < 25):
            page_size = limit
        current_page  = 1
        params = { 'interval': f'_{self.params['interval']}days', 'page': current_page, 'pageSize': page_size}
        response    = self.connector.get_json_response(agents_endpoint, params)
        totalPages  = int(response['ok']['totalPages'])
        while(len(response['ok']['data']) < limit and current_page <= totalPages):
            current_page += 1
            remaining = limit - len(response)
            if(remaining < 25 ):
                page_size = remaining
            params = { 'interval': f'_{self.params['interval']}days', 'page': current_page, 'pageSize': page_size}
            currentResponse = self.connector.get_json_response(agents_endpoint, params)
            currentData     = self.extract_agents_data(currentResponse)
            response['ok']['data'] += currentData 
        return response
