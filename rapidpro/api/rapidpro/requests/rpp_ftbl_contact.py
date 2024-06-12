import json

import pandas as pd
import numpy as np

class Contacts:
    def __init__(self, session):
        self._session = session

    def get_contacts(self, **kwargs):

        params = {**kwargs}
        request = "contacts.json"

        responses = self._session.get(request, params=params)

        r_n = [pd.json_normalize(response, sep="_") for response in responses]
        df = pd.concat(r_n)
        if df.shape[0]==0:
            print("No new data fetched from API")
            print("Exiting the pipeline run.")
            exit(0)
        df['fields'] = pd.Series([str(response['fields']) for response in responses[0]])
        df['language']=pd.Series([response['urns'][0][0:3] for response in responses[0]])
        df = df[['uuid', 'name', 'language', 'blocked', 'stopped','created_on', 'modified_on','fields','language']]
        df['created_on'] = pd.to_datetime(df['created_on'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        df['modified_on'] = pd.to_datetime(df['modified_on'], format="%Y-%m-%dT%H:%M:%S.%fZ")
        df['name'] = df['name'].str.slice(0,255)
        Na = np.nan
        df["id"], df["created_by_id"], df["is_active"], df["is_test"], df["org_id"], df["is_active"], df["modified_by_id"] = Na,Na,Na,Na,Na,Na,Na
        try:
            df["org_id"] = params["org_id"]
        except Exception:
            pass
        
        return df
