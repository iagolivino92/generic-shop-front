import json

import requests


def call_ask_mb(request=None):
    args = dict(request.args)
    shop = args['shop']
    # add transaction id to the args
    args['transaction_id'] = get_transaction_id(shop)
    # call mb service with the args
    response = requests.get(f'http://localhost:8082/mb_request?{args}')
    return response.text, response.status_code


def get_transaction_id(shop=None):
    # search shop in database to check if it exists
    # create and save a new transaction id on trdb (save shop, client number, amount)
    # return the created transaction_id
    transaction_id = 'blabla'
    return transaction_id


def parse_response(response=None):
    if response:
        return 'ok man'
    return 'error man'


def parse_args(args):
    parsed_args = ''
    for arg in args:
        json_args = json.loads(arg.replace("'", '"'))
        for new_arg in json_args:
            parsed_args += f'{new_arg}={json_args[new_arg]}'
            if not list(json_args).index(new_arg) == len(json_args)-1:
                parsed_args += '&'
    return parsed_args
