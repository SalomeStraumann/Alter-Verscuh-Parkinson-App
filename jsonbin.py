import requests

BIN_API_URL = r'https://api.jsonbin.io/v3/b'

# Funktionen für den "todo"-Teil

def load_data(api_key_todo, bin_id_todo):
    """
    Lädt den gesamten Bin
    """
    url_todo = BIN_API_URL + '/' + bin_id_todo + '/latest'
    headers_todo = {'X-Master-Key': api_key_todo}
    response_todo = requests.get(url_todo, headers=headers_todo).json()
    return response_todo['record']


def save_data(api_key_todo, bin_id_todo, data_todo):
    """
    Speichert den gesamten Bin
    """
    url_todo = BIN_API_URL + '/' + bin_id_todo
    headers_todo = {'X-Master-Key': api_key_todo, 'Content-Type': 'application/json'}
    response_todo = requests.put(url_todo, headers=headers_todo, json=data_todo).json()
    return response_todo


def load_key(api_key_todo, bin_id_todo, key_todo, empty_value=[]):
    """
    Lädt den Wert für einen bestimmten Schlüssel aus dem Bin
    """
    url_todo = BIN_API_URL + '/' + bin_id_todo + '/latest'
    headers_todo = {'X-Master-Key': api_key_todo}
    response_todo = requests.get(url_todo, headers=headers_todo).json()
    record_todo = response_todo['record']
    if key_todo in record_todo:
        return record_todo[key_todo]
    else:
        return empty_value


def save_key(api_key_todo, bin_id_todo, key_todo, data_todo):
    """
    Speichert den Wert für einen bestimmten Schlüssel im Bin
    """
    url_todo = BIN_API_URL + '/' + bin_id_todo
    headers_todo = {'X-Master-Key': api_key_todo, 'Content-Type': 'application/json'}
    response_todo = requests.get(url_todo, headers=headers_todo).json()
    record_todo = response_todo['record']
    if type(record_todo) != dict:
        record_todo = {key_todo: data_todo}  # erzeuge ein neues Dictionary
    else:
        record_todo[key_todo] = data_todo
    response_todo = requests.put(url_todo, headers=headers_todo, json=record_todo).json()
    return response_todo


# Funktionen für den "budge"-Teil

def load_data(api_key_budge, bin_id_budge):
    """
    Lädt den gesamten Bin
    """
    url_budge = BIN_API_URL + '/' + bin_id_budge + '/latest'
    headers_budge = {'X-Master-Key': api_key_budge}
    response_budge = requests.get(url_budge, headers=headers_budge).json()
    return response_budge['record']


def save_data(api_key_budge, bin_id_budge, data_budge):
    """
    Speichert den gesamten Bin
    """
    url_budge = BIN_API_URL + '/' + bin_id_budge
    headers_budge = {'X-Master-Key': api_key_budge, 'Content-Type': 'application/json'}
    response_budge = requests.put(url_budge, headers=headers_budge, json=data_budge).json()
    return response_budge


def load_key(api_key_budge, bin_id_budge, key_budge, empty_value=[]):
    """
    Lädt den Wert für einen bestimmten Schlüssel aus dem Bin
    """
    url_budge = BIN_API_URL + '/' + bin_id_budge + '/latest'
    headers_budge = {'X-Master-Key': api_key_budge}
    response_budge = requests.get(url_budge, headers=headers_budge).json()
    record_budge = response_budge['record']
    if key_budge in record_budge:
        return record_budge[key_budge]
    else:
        return empty_value


def save_key(api_key_budge, bin_id_budge, key_budge, data_budge):
    """
    Speichert den Wert für einen bestimmten Schlüssel im Bin
    """
    url_budge = BIN_API_URL + '/' + bin_id_budge
    headers_budge = {'X-Master-Key': api_key_budge, 'Content-Type': 'application/json'}
    response_budge = requests.get(url_budge, headers=headers_budge).json()
    record_budge = response_budge['record']
    if type(record_budge) != dict:
        record_budge = {key_budge: data_budge}  # generate new dict
    else:
        record_budge[key_budge] = data_budge
    response_budge = requests.put(url_budge, headers=headers_budge, json=record_budge).json()
    return response_budge
