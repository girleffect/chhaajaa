import json

import pandas as pd
import numpy as np

class AuthUser:
    def __init__(self, session):
        self._session = session

    def get_auth_users(self, **kwargs):

        params = {**kwargs}
        request = "users.json"

        responses = self._session.get(request, params=params)

        r_n = [pd.json_normalize(response, sep="_") for response in responses]
        df = pd.concat(r_n)
        df.rename(columns={'created_on': 'date_joined','role': 'is_staff'}, inplace=True)
        Na = np.nan
        df['username'] = df['email']
        df['is_superuser'], df['last_login'], df['is_staff'], df['is_active'], df['id'] = Na, Na, Na, Na, Na
        df['last_login'] = pd.to_datetime(df['last_login'], errors='coerce')
        df['last_login'] = pd.to_datetime(df['last_login'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        return df
