import os,sys,json,requests,pandas as pd,datetime
from sqlalchemy import create_engine

def get_yt_data():
    print(str(datetime.datetime.now())+": Starting the run of script " + os.path.basename(sys.argv[0]) + " for fetching youtube analytics data for " + sys.argv[1])
    CONF_FILE = '../conf/' + os.path.basename(sys.argv[0]).split('.')[0] + '_' + sys.argv[1] + '.conf'
    print(str(datetime.datetime.now())+": Conf file for this run is " + CONF_FILE)

    # using utf-8 to read hindi text also
    with open(CONF_FILE, 'r', encoding='utf-8') as read_conf_file:
        read_conf = json.load(read_conf_file)

    #KEY_FILE_LOCATION = read_conf['googleKeyFile']

    #print(str(datetime.datetime.now())+": Reading Key file for this run.")
    #with open(KEY_FILE_LOCATION, 'r', encoding='utf-8') as read_conf_file:
    #    key_file_conf = json.load(read_conf_file)

    print(str(datetime.datetime.now())+": Generating body for access token request")
    access_token_body={}
    access_token_body['client_id']=os.environ['YOUTUBE_CLIENT_ID']
    access_token_body['client_secret']=os.environ['YOUTUBE_CLIENT_SECRET']
    access_token_url=read_conf['accessTokenUrl']
    access_token_body['refresh_token']=os.environ['YOUTUBE_REFRESH_TOKEN']
    access_token_body['grant_type']=read_conf['grantType']

    res = requests.post(url=access_token_url, data=access_token_body)
    if res.status_code == 200:
        json_repsonse = json.loads(res.text)
    else:
        print(str(datetime.datetime.now())+": Post request failed for url: " + access_token_url + " with body " + str(access_token_body))
        print(str(datetime.datetime.now())+": Response is below \n" + res.text)
        exit(0)

    print(str(datetime.datetime.now())+": Access token generated successfully. Now preparing param for report request")
    report_params={}
    report_params['access_token']=json_repsonse['access_token']

    conn = create_engine('postgresql://' + os.environ['dbUserName'] + ':' + os.environ['dbPassword'] + '@' + os.environ[
        'dbServer'] + '/' + os.environ['dbUserName'])
    df_dt = pd.read_sql("select max(report_date) max_date from  " + read_conf['targetSchemaName'] + "." + read_conf[
        'targetTableName'], conn)

    if df_dt['max_date'][0] == None:
        startDt = read_conf["startDate"]
    else:
        startDt = df_dt['max_date'][0] + datetime.timedelta(days=-1)

    report_params['endDate']=datetime.date.today()+datetime.timedelta(days=-1)
    report_params['startDate'] =startDt
    report_params['ids'] ="channel=="+read_conf["channelId"]
    report_params['metrics'] =read_conf["metrics"]
    report_params['dimensions']=read_conf["dimensions"]

    res = requests.get(url=read_conf['reportUrl'], params=report_params)
    if res.status_code == 200:
        repsonse = json.loads(res.text)
    else:
        print(str(datetime.datetime.now())+": Get request failed for url: " + read_conf['reportUrl'] + " with params " + str(report_params))
        print(str(datetime.datetime.now())+": Response is below \n" + res.text)
        exit(0)


    df = pd.DataFrame(repsonse['rows'], columns=read_conf['apiConfig']['columns'])

    print(str(datetime.datetime.now())+": Youtube report is fetched successfully for start date "+ str(report_params['startDate'])+ " and end date "+ str(report_params['endDate']))
    print(str(datetime.datetime.now())+": Fetching database data to do delta")

    df['report_date']=pd.Series([datetime.datetime.strptime(i.split(' ')[0], '%Y-%m-%d').date() for i in df['report_date']])

    df2 = pd.read_sql("select * from  " + read_conf['targetSchemaName'] + "." + read_conf['targetTableName'], conn)


    print(str(datetime.datetime.now())+": Camparing/joining data from youtube with data in database")
    df3 = pd.merge(df, df2, right_on=read_conf['tableConfig']['joinColumns'],
                   left_on=read_conf['apiConfig']['joinColumns'], how='left', suffixes=['_gs', '_db'])
    print(str(datetime.datetime.now())+": Filter only new data from youtube which is not present in database. Drop the old data")

    for i in range(len(read_conf['apiConfig']['columns'])):
        if read_conf['apiConfig']['columns'][i] not in read_conf['apiConfig']['joinColumns']:
            if read_conf['apiConfig']['columns'][i] != read_conf['tableConfig']['columns'][i]:
                # picking only new value. Dropping exisitng values
                df3 = df3[df3[read_conf['tableConfig']['columns'][i]].isnull()]
                # dropping the column coming from database
                df3.drop(columns=[read_conf['tableConfig']['columns'][i]], inplace=True)
            else:
                df3 = df3[df3[read_conf['tableConfig']['columns'][i] + '_db'].isnull()]
                #print(df3)
                df3.drop(columns=[read_conf['tableConfig']['columns'][i] + '_db'], inplace=True)

    print(str(datetime.datetime.now())+": Rename columns from youtube to match with database")
    # renaming all columns to match with database column names
    for i in range(len(read_conf['apiConfig']['columns'])):
        if read_conf['apiConfig']['columns'][i].upper() != read_conf['tableConfig']['columns'][i].upper():
            df3.rename(columns={read_conf['apiConfig']['columns'][i]: read_conf['tableConfig']['columns'][i]},
                       inplace=True)
        else:
            df3.rename(columns={read_conf['apiConfig']['columns'][i] + "_gs": read_conf['tableConfig']['columns'][i]},
                       inplace=True)

    df3 = df3[read_conf['tableConfig']['columns']]
    print(str(datetime.datetime.now())+": Inserting data into database")
    if df3.shape[0] > 0:
        print(str(datetime.datetime.now())+": Total data to append: " + str(len(df3)))
        df3.to_sql(name=read_conf['targetTableName'], schema=read_conf['targetSchemaName'], con=conn, index=False,
                   if_exists='append',
                   chunksize=300)
    else:
        print(str(datetime.datetime.now())+": No data to append. Table is in sync with facebook api")
    print(str(datetime.datetime.now())+": Finishing the run of script " + os.path.basename(sys.argv[0]) + " for fetching youtube analytics data for " + sys.argv[1])


if __name__ == '__main__':
    get_yt_data()

