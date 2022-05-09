import json

import pandas as pd
import numpy as np

class Runs:
    def __init__(self, session):
        self._session = session

    def get_runs(self, **kwargs):

        params = {**kwargs}
        request = "runs.json"

        responses = self._session.get(request, params=params)

        r_n = [pd.json_normalize(response, sep="_") for response in responses]
        df = pd.concat(r_n)
        Na = np.nan
        df = df[['id', 'uuid', 'start','responded','created_on', 'modified_on','exited_on', 'exit_type', 'flow_uuid','contact_uuid']]
        df['timeout_on'], df['flowlabel_id'], df['current_node_uuid'], df['message_ids'], df['path'], df['results'], df['session_id'], df['submitted_by_id'], df['is_active'], df['fields'], df['expires_on'], df['contact_id'], df['flow_id'], df['org_id'], df['parent_id'], df['connection_id']= Na, Na,Na, Na,Na, Na,Na, Na,Na, Na,Na, Na,Na, Na,Na, Na
        df['created_on'] = pd.to_datetime(df['created_on'], format="%Y-%m-%dT%H:%M:%S.%fZ")
        if df.shape[0] > 0:
            df['modified_on']=df['modified_on'].apply(lambda k: ':'.join(k.split(':')[:-1]) + ':' + k.split(':')[-1][:2] + '.00Z' if len(k.split(':')[-1]) < 6 else k)
        df['modified_on'] = pd.to_datetime(df['modified_on'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        df['expires_on'] = pd.to_datetime(df['expires_on'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        df['timeout_on'] = pd.to_datetime(df['timeout_on'], format="%Y-%m-%dT%H:%M:%S.%fZ")
        if df.shape[0] > 0:
            df['exited_on']=df['exited_on'].apply(lambda k: ':'.join(k.split(':')[:-1]) + ':' + k.split(':')[-1][:2] + '.00Z' if len(k.split(':')[-1]) and k.notnull() < 6 else k)
        df['exited_on'] = pd.to_datetime(df['exited_on'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        df.rename(columns={'start': 'start_id', 'flow_uuid':'uuid'}, inplace=True)

        try:
            df["org_id"] = params["org_id"]
        except Exception:
            pass
        
        return df