
import os
import json
from dotenv import load_dotenv
from cookie_dao_api import CookieDaoAPI

load_dotenv()
COOKIE_API_KEY = os.getenv('COOKIE_API_KEY')

# Interactive console to explore the DAO API
class CookieDaoConsole:
    def __init__(self, api_key, mode='json'):
        self.cookie_dao_api = CookieDaoAPI(api_key)
        self.options = self.cookie_dao_api.options + ['agentsFiltered']
        self.set_choice_string()
        self.mode = mode

    minimal_keys = ["agentName", "mindshare", "marketCap", "liquidity", "price", "averageEngagementsCount"]
    def get_minimal_response(self, response):
        '''
        A convenient function to reduce the number of fields in data retrieved, for analysis
        '''
        if type(response) != type({}) and type(response) != type([]):
            return response
        if('ok' in list(response.keys())):
            response = response['ok']
        if (type(response) == type({}) and 'data' in list(response.keys())):
            response=response['data']
        if(type(response) == type([])):
            responseList = list(response)
            filteredResponseList = []
            for responseElem in responseList:
                currKeys = list(responseElem.keys())
                requiredElem = {}
                for k in self.minimal_keys:
                    if not k in currKeys: # Just return the obtained response earlier
                        return list(response)
                    requiredElem[k] = responseElem[k]
                filteredResponseList.append(requiredElem)
            return filteredResponseList
        required_response = {}
        for key in self.minimal_keys:
            if not key in list(response.keys()):
                return response # Return the response as it is ...
            required_response[key] = response[key]
        return required_response

    def set_choice_string(self):
        choice_string = ''
        for (idx, option) in list(zip(range(len(self.options)), self.options)):
            choice_string += f'{idx+1}) {option}\n'
        choice_string += f'{len(self.options)+1}) Exit this prompt\n'
        choice_string += f'Select an option {1} - {len(self.options)+1} : '
        self.choice_string = choice_string

    def retrieve_user_params(self, options):
        while True:
            user_params_prompt = '0) Required parameters provided !\n'
            for (idx, option) in list(zip(range(len(options)), options)):
                user_params_prompt += f'{idx+1}) {option}={self.cookie_dao_api.params[option]}\n'
            user_params_prompt += f'Enter the choice (0-{len(options) - 1}) : '
            option = int(input(user_params_prompt))
            if option > len(options): # Ignore if incorrect option provided
                continue
            if option == 0 or option > len(options):
                break
            selected_option = options[option-1]
            self.cookie_dao_api.params[selected_option] = input(f"Enter new value for {selected_option} : ")
        # Provide the updated params as the return value
        return self.cookie_dao_api.params

    def set_endpoint_params(self, option_idx):
        '''
        Get the parameters for the endpoint selected from the user
        '''
        selected_options_list = {
            2: ['search_term', 'from', 'to'],
            3: ['user_name', 'interval'],
            4: ['address', 'interval'],
            5: ['interval', 'page', 'page_size'],
            6: ['interval', 'page', 'limit']
        }.get(option_idx, None)
        if selected_options_list is not None: # set the params relevant for option_idx
            self.retrieve_user_params(selected_options_list)
        return self.cookie_dao_api.params

    def obtain_command_response(self, command_choice):
        selected_fun = {
            1: self.cookie_dao_api.get_authorization,
            2: self.cookie_dao_api.get_hackathon_search,
            3: self.cookie_dao_api.get_twitter_username,
            4: self.cookie_dao_api.get_contract_address,
            5: self.cookie_dao_api.get_agents_paged,
            6: self.cookie_dao_api.get_agents_filtered
        }.get(command_choice, None);
        if selected_fun is None:
            return None
        response = selected_fun()
        # return selected_fun
        if self.mode == 'minimal':
            response = self.get_minimal_response(response)
        return response

    def interactive(self):
        command_choice = ''
        while True:
            if(command_choice != ""):
                print("\n")
            command_choice = int(input(self.choice_string))
            if command_choice > len(self.options):
                break
            self.set_endpoint_params(command_choice)
            response = self.obtain_command_response(command_choice)
            if response: # Ignore if response is None
                json_response = json.dumps(response, indent=2)
                print(json_response)

if __name__ == '__main__':
    mode_choice = int(input("1) Complete JSON \n2) Minimal json for cookiemaps\nTo get started, enter the mode (1-2) : "))
    mode = 'json' if mode_choice == 1 else 'minimal'
    cdc  = CookieDaoConsole(COOKIE_API_KEY, mode)
    cdc.interactive()
