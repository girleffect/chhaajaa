import json

import pandas as pd
import numpy as np

class ContactGroupCount:
    def __init__(self, session):
        self._session = session

    def get_contact_group_count(self, **kwargs):

        params = {**kwargs}
        request = "groups.json"

        responses = self._session.get(request, params=params)

        r_n = [pd.json_normalize(response, sep="_") for response in responses]
        df = pd.concat(r_n)
        if df.shape[0]==0:
            print("No new data fetched from API")
            print("Exiting the pipeline run.")
            exit(0)
        Na = np.nan
        df['id'], df['group_id'], df['is_squashed'] = Na, Na, Na
        return df