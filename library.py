import requests
import jwt

apiURL = ''
rsession = requests.Session()

def is_token_exp(token):
    now = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    decode = jwt.decode(token, verify=False)
    exp = decode['exp']
    if (exp - now) < 600:
        return True
    else:
        return False


def session_key(api_key):
    head = {'Content-Type': 'application/json'}
    body = '{"data": {"api_key":"' + api_key + '"} }'
    url = apiURL + '/v2/api_auth'
    response = rsession.put(url, headers=head, data=body, timeout=10)
    if response.json()['status'] == 'success':
        sk = response.json()['auth_token']
        return sk
    else:
        raise RuntimeError(
            'An error occurred: ' +
            response.json()['error'] +
            ', ' +
            response.json()['data']['message']
        )


def validate_token(api_key, token):
    head = {
        'Accept': 'application/json',
        'X-Auth-Token': token,
    }
    url = apiURL + '/v2/token_auth'
    response = rsession.get(url, headers=head, timeout=10)
    if response.json()['status'] == 'success':
        return token
    else:
        new_token = session_key(api_key)
        return new_token


def GetAccounts(
    token,
    accID,
):
    head = {
        'Accept': 'application/json',
        'X-Auth-Token': token,
    }
    url = apiURL + '/v2/accounts/' + accID + '/descendants'
    # ?auth_token=' + token
    response = rsession.get(url, headers=head, timeout=10)
    accounts = []
    i = 0
    while i < response.json()['page_size']:
        accounts.append(
            {
                'account_id':response.json()['data'][i]['id'],
                'account_name':response.json()['data'][i]['name'],
                'account_realm':response.json()['data'][i]['realm'],
                'parent_id':response.json()['data'][i]['tree'][-1],
            }
        )
        i += 1

    return accounts


def GetNumbers(
    token,
    accID,
    numberStatus='in_service',
):
    head = {
        'Accept': 'application/json',
        'X-Auth-Token': token,
    }
    url = apiURL + '/v2/accounts/' + accID + '/phone_numbers'
    response = rsession.get(url, headers=head, timeout=10)
    numbers = []
    try:
        for x in response.json()['data']['numbers']:
            numbers.append(x)
        return numbers
    except KeyError:
        return None
