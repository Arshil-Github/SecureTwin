# backend/mock_data/loader.py
import json
import os
from ..config import settings

def _load_json(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(file_path, 'r') as f:
        return json.load(f)

def load_user(persona_name: str):
    if settings.DATA_SOURCE != "mock":
        raise NotImplementedError("Live data source not implemented")
    users_data = _load_json('users.json')
    for user in users_data['users']:
        if persona_name.lower() in user['full_name'].lower():
            return user
    return None

def load_all_users():
    return _load_json('users.json')['users']

def load_transactions(persona_name: str):
    if settings.DATA_SOURCE != "mock":
        raise NotImplementedError("Live data source not implemented")
    return _load_json(f'transactions_{persona_name.lower()}.json')['transactions']

def load_investments(persona_name: str):
    if settings.DATA_SOURCE != "mock":
        raise NotImplementedError("Live data source not implemented")
    return _load_json(f'investments_{persona_name.lower()}.json')['investments']

def load_assets(persona_name: str):
    if settings.DATA_SOURCE != "mock":
        raise NotImplementedError("Live data source not implemented")
    return _load_json(f'assets_{persona_name.lower()}.json')['assets']
