import json

import pandas as pd
import numpy as np

class FlowStart:
    def __init__(self, session):
        self._session = session

    def get_flowstart(self, **kwargs):

        params = {**kwargs}
        request = "flow_starts.json"

        responses = self._session.get(request, params=params)

        r_n = [pd.json_normalize(response, sep="_") for response in responses]
        df = pd.concat(r_n)
        if df.shape[0]==0:
            print("No new data fetched from API")
            print("Exiting the pipeline run.")
            exit(0)
        df = df[['id', 'uuid', 'status', 'restart_participants','exclude_active', 'created_on', 'modified_on']]
        df['created_on'] = pd.to_datetime(df['created_on'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        df['modified_on'] = pd.to_datetime(df['modified_on'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        Na = np.nan
        df['is_active'], df['contact_count'], df['extra'], df['created_by_id'], df['flow_id'], df['modified_by_id'], df['include_active']= Na, Na, Na, Na, Na, Na, Na
        return df
