import json

import pandas as pd
import numpy as np

class Flows:
    def __init__(self, session):
        self._session = session

    def get_flows(self, **kwargs):

        params = {**kwargs}
        request = "flows.json"

        responses = self._session.get(request, params=params)

        r_n = [pd.json_normalize(response, sep="_") for response in responses]
        df = pd.concat(r_n)
        df = df[['uuid', 'name', 'type', 'archived','created_on', 'modified_on', 'runs_expired']]
        df['created_on'] = pd.to_datetime(df['created_on'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        df['modified_on'] = pd.to_datetime(df['modified_on'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        Na = np.nan 
        df.rename(columns={'type': 'flow_type', 'runs_expired': 'expires_after_minutes'}, inplace=True)
        df["id"], df['entry_uuid'], df['entry_type'], df["created_by_id"], df["version_number"], df["is_test"], df["org_id"], df["is_active"], df["fields"], df["modified_by_id"], df['ignore_triggers'], df['saved_on'], df['flow_type'], df['base_language'], df['metadata'], df['saved_by_id'], df['is_archived'] = Na,Na,Na,Na,Na,Na,Na,Na,Na,Na,Na,Na,Na,Na,Na,Na, Na
        df['saved_on'] = pd.to_datetime(df['saved_on'], errors='coerce')
        return df