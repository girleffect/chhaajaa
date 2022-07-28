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
        if df.shape[0]==0:
            print("No new data fetched from API")
            print("Exiting the pipeline run.")
            exit(0)

        df['metadata'] = df['labels'].apply(lambda x:','.join([ dict(i)['name'] for i in x  if len(i)>0]))
        df = df[['uuid', 'name', 'type', 'archived','created_on', 'modified_on', 'runs_expired','metadata']]
        df['created_on'] = pd.to_datetime(df['created_on'], format="%Y-%m-%dT%H:%M:%S.%fZ")
        df['modified_on'] = pd.to_datetime(df['modified_on'], format="%Y-%m-%dT%H:%M:%S.%fZ")
        Na = np.nan
        df.rename(columns={'type': 'flow_type', 'runs_expired': 'expires_after_minutes'}, inplace=True)
        df["id"], df['entry_uuid'], df['entry_type'], df["created_by_id"], df["version_number"], df["is_test"], df["org_id"],df["modified_by_id"], df['ignore_triggers'], df['saved_on'], df['flow_type'], df['base_language'],df['saved_by_id']= Na,Na,Na,Na,Na,Na,Na,Na,Na,Na,Na,Na,Na
        df['saved_on'] = pd.to_datetime(df['saved_on'], errors='coerce')
        df.rename({'archived':'is_archived'},axis=1,inplace=True)
        df['is_active']=df['is_archived'].apply(lambda x: False if x else True)

        try:
            df["org_id"] = params["org_id"]
        except Exception:
            pass
        
        return df