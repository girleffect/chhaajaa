import json

import pandas as pd
import numpy as np

class Messages:
    def __init__(self, session):
        self._session = session

    def get_messages(self, **kwargs):

        params = {**kwargs}
        request = "messages.json"

        responses = self._session.get(request, params=params)

        r_n = [pd.json_normalize(response, sep="_") for response in responses]
        df = pd.concat(r_n)
        df = df[['id', 'broadcast', 'urn', 'direction', 'type', 'status', 'archived','visibility','text', 'labels', 'attachments', 'created_on', 'sent_on','modified_on', 'media', 'contact_uuid', 'contact_name', 'channel_uuid','channel_name']]
        df['created_on'] = pd.to_datetime(df['created_on'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        df['modified_on'] = pd.to_datetime(df['modified_on'], format="%Y-%m-%dT%H:%M:%S.%fZ") 
        Na = np.nan 
        df.rename(columns={'broadcast': 'broadcast_id', 'type':'msg_type'}, inplace=True)
        df['high_priority'], df['queued_on'], df['delete_reason'], df['channel_id'], df['connection_id'], df['contact_id'], df['contact_urn_id'], df['org_id'], df['response_to_id'], df['topup_id'], df['msg_count'], df['error_count'], df['next_attempt'], df['external_id'], df['metadata'], df['uuid'] = Na, Na, Na, Na, Na, Na, Na, Na, Na, Na, Na, Na, Na, Na, Na, Na

        df['queued_on'] = pd.to_datetime(df['queued_on'], errors='coerce')
        df['next_attempt'] = pd.to_datetime(df['next_attempt'], errors='coerce')
        df['text'] = df['text'].str.decode('utf8')
        df['attachments'] = df['attachments'].str.decode('utf8')
        df['contact_name'] = df['contact_name'].str.decode('utf8')

        return df
