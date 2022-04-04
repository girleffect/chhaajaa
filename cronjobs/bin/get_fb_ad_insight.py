#from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adaccount import AdAccount
#from facebook_business.adobjects.campaign import Campaign
#from facebookads.adobjects.adset import AdSet
from facebook_business.api import FacebookAdsApi
import sys,json,os,pandas as pd,numpy as np
import datetime
from sqlalchemy import create_engine
import numpy as np
import requests

def get_report_date(inp_date):
    flag=sys.argv[2]
    start_date=inp_date
    if flag=='weekly':
        if inp_date.weekday() != 0:
            diff = 0 - inp_date.weekday()
            start_date = inp_date + datetime.timedelta(days=diff)
        end_date = start_date + datetime.timedelta(days=6)
    elif flag=='daily':
        end_date=start_date
    elif flag=='monthly':
        start_date=inp_date
        start_date=start_date+datetime.timedelta(days=((start_date.day*-1)+1))
        end_date=start_date+datetime.timedelta(days=32)
        end_date = end_date + datetime.timedelta(days=((end_date.day*-1)))
    else:
        print("Invalid 2nd parameter. It should be monthly,weekly,daily")
        exit(1)
    return start_date,end_date

def load_data():
    print(str(datetime.datetime.now())+": Starting the run of script "+os.path.basename(sys.argv[0])+" for fetching ads data for "+sys.argv[1])
    CONF_FILE='../conf/'+os.path.basename(sys.argv[0]).split('.')[0]+'_'+sys.argv[1]+'.conf'
    TOKEN_FILE = '../conf/' + os.path.basename(sys.argv[0]).split('.')[0] + '_' + sys.argv[1] + '_token.conf'

    print(str(datetime.datetime.now())+": Conf file for this run is "+CONF_FILE)

    #using utf-8 to read hindi text also
    with open(CONF_FILE,'r',encoding='utf-8') as read_conf_file:
        read_conf=json.load(read_conf_file)

    conn = create_engine('postgresql://' + os.environ['dbUserName'] + ':' + os.environ['dbPassword'] + '@' + os.environ[
        'dbServer'] + '/' + os.environ['dbUserName'])
    if sys.argv[2] == 'weekly':
        table_name = read_conf['weeklyTargetTableName']
    elif sys.argv[2] == 'daily':
        table_name = read_conf['dailyTargetTableName']
    elif sys.argv[2] == 'monthly':
        table_name = read_conf['monthlyTargetTableName']

    print(str(datetime.datetime.now()) + ": Getting the token for FB API call" + TOKEN_FILE + " to get app configuration")
    # with open(TOKEN_FILE,'r',encoding='utf-8') as read_token_file:
    #     read_token=json.load(read_token_file)
    # expiring_on=datetime.datetime.strptime(read_token['start_dt'], '%Y-%m-%d').date()+ datetime.timedelta(days=int(read_token['expires_in']/86400)-5)
    # if expiring_on<=datetime.datetime.strptime(str(datetime.datetime.today()).split(' ')[0],'%Y-%m-%d').date():
    #     token_refresh_url=read_token['token_refresh_url']+read_token['access_token']
    #     r=requests.get(token_refresh_url)
    #     print(r.text)
    #     token_conf=json.loads(r.text)
    #     token_conf['start_dt']=str(datetime.datetime.strptime(str(datetime.datetime.today()).split(' ')[0],'%Y-%m-%d').date())
    #     token_conf['token_refresh_url']=read_token['token_refresh_url']
    #     access_token = token_conf['access_token']
    #     print(str(token_conf))
    #     f = open(TOKEN_FILE, "w")
    #     f.write(json.dumps(token_conf))
    #     f.close()
    # else:
    #     access_token = read_token['access_token']
    access_token = os.environ['FACEBOOK_ACCESS_TOKEN']
    #app_id = settings.FACEBOOK_APP_ID
    #app_secret= settings.FACEBOOK_APP_SECRET
    print(str(datetime.datetime.now()) + ": Reading conf file " + CONF_FILE + " to get app configuration")
    id= os.environ['FACEBOOK_ADD_ACCOUNT_ID']
    FacebookAdsApi.init(access_token= access_token)

    #level=ad provides until ad level data
    #params={'time_range': {'since': '2020-06-01', 'until': '2020-06-10'},'level': 'ad', 'limit': '20000'}

    print(str(datetime.datetime.now())+": Modifying the report date to start from Monday and end at sunday")

    conf_start_dt=datetime.datetime.strptime(read_conf['start_dt'], '%Y-%m-%d').date()
    df_get_max_date = pd.read_sql("select max(date_start) start_dt from  " + read_conf['targetSchemaName'] + "." + table_name, conn)

    if df_get_max_date['start_dt'][0] == None:
        print("Unable to find max modified date in existing table. Table is empty")
        start_dt = datetime.datetime.strptime(read_conf['start_dt'], '%Y-%m-%d').date()
    else:
        start_dt = datetime.datetime.strptime(str(df_get_max_date['start_dt'][0]).split(' ')[0],
                                              '%Y-%m-%d') + datetime.timedelta(days=-7)
        start_dt=datetime.datetime.strptime(str(start_dt).split(' ')[0], '%Y-%m-%d').date()

    if conf_start_dt > start_dt:
        start_dt=conf_start_dt
    conf_end_dt=datetime.datetime.strptime(str(datetime.datetime.today()).split(' ')[0],'%Y-%m-%d').date()
    start_dt,end_dt=get_report_date(start_dt)

    df=pd.DataFrame(columns=read_conf['fields'])
    print(str(datetime.datetime.now())+": Started fetching "+sys.argv[2]+" ads data from facebook")
    while conf_end_dt>=end_dt:
      params = {'time_range': {'since': str(start_dt), 'until': str(end_dt)},'level': 'ad', 'limit': '20000'}
      k=AdAccount(id).get_insights(fields=read_conf['fields'],params=params)
      df=df.append(pd.DataFrame(k),ignore_index=True)
      start_dt = end_dt + datetime.timedelta(days=1)
      start_dt,end_dt=get_report_date(start_dt)

    print(str(datetime.datetime.now())+": Finished fetching "+ sys.argv[2] +" ads data from facebook")
    #df=df[df['ad_name'].str.contains('FB_') | df['ad_name'].str.contains('FB ') | df['campaign_name'].str.contains('Big Sis')]
    #df.reset_index(inplace=True)
    #preparing data for inserting it into table
    print(str(datetime.datetime.now())+": Started the Cleaning of ads data")
    print(df.shape)
    # exit(0)
    df=df.replace('','0')
    df=df.replace(' ','0')
    df=df.replace(np.nan,'0')
    #df.fillna('hello',inplace=True)
    for i in range(len(df)):
        if df['outbound_clicks'][i]!='0':
            df['outbound_clicks'][i]=dict(df['outbound_clicks'][i][0])
            df['outbound_clicks'][i]=df['outbound_clicks'][i]['value']
        if df['unique_outbound_clicks'][i]!='0':
            df['unique_outbound_clicks'][i]=dict(df['unique_outbound_clicks'][i][0])
            df['unique_outbound_clicks'][i]=df['unique_outbound_clicks'][i]['value']
    print(str(datetime.datetime.now())+": Finished the Cleaning of ads data")

    print(str(datetime.datetime.now())+": Modifying the column data types to match with database tables")
    for i in range(len(read_conf['apiConfig']['columnTypes'])):
        if read_conf['apiConfig']['columnTypes'][i]!='str':
            if read_conf['apiConfig']['columnTypes'][i]=='int' or read_conf['apiConfig']['columnTypes'][i]=='float' :
                df[read_conf['apiConfig']['columns'][i]]=df[read_conf['apiConfig']['columns'][i]].str.replace('$','')
                df[read_conf['apiConfig']['columns'][i]]=df[read_conf['apiConfig']['columns'][i]].str.replace(',','')
                df[read_conf['apiConfig']['columns'][i]]=df[read_conf['apiConfig']['columns'][i]].str.replace('%','')
                df[read_conf['apiConfig']['columns'][i]] = df[read_conf['apiConfig']['columns'][i]].str.replace(' ', '0')
                df[read_conf['apiConfig']['columns'][i]]=df[read_conf['apiConfig']['columns'][i]].astype(read_conf['apiConfig']['columnTypes'][i])
            if read_conf['apiConfig']['columnTypes'][i]=='date':
                df[read_conf['apiConfig']['columns'][i]]=pd.Series([datetime.datetime.strptime(i.split(' ')[0], '%Y-%m-%d').date() for i in df[read_conf['apiConfig']['columns'][i]]])

    print(str(datetime.datetime.now())+": Columns datatype modification is complete.")
    print(str(datetime.datetime.now())+": Fetching data from database")
    df2=pd.read_sql("select * from  "+read_conf['targetSchemaName']+"."+table_name,conn)
    print(str(datetime.datetime.now())+": Camparing/joining data from facebook with data in database")
    df3=pd.merge(df,df2,right_on=read_conf['tableConfig']['joinColumns'],left_on=read_conf['apiConfig']['joinColumns'],how='left',suffixes=['_gs','_db'])
    print(str(datetime.datetime.now())+": Filter only new data from facebook which is not present in database. Drop the old data")
    for i in range(len(read_conf['apiConfig']['columns'])):
        #checking if column is key column or used in joins
        if read_conf['apiConfig']['columns'][i] not in read_conf['apiConfig']['joinColumns']:
            if read_conf['apiConfig']['columns'][i]!=read_conf['tableConfig']['columns'][i]:
                #picking only new value. Dropping exisitng values
                if read_conf['tableConfig']['columns'][i] in read_conf['apiConfig']['notNullColumns']:
                    df3=df3[df3[read_conf['tableConfig']['columns'][i]].isnull()]
                #dropping the column coming from database
                df3.drop(columns=[read_conf['tableConfig']['columns'][i]], inplace=True)
            else:
                if read_conf['tableConfig']['columns'][i] in read_conf['apiConfig']['notNullColumns']:
                    df3=df3[df3[read_conf['tableConfig']['columns'][i]+'_db'].isnull()]
                df3.drop(columns=[read_conf['tableConfig']['columns'][i]+'_db'], inplace=True)

    print(str(datetime.datetime.now())+": Rename columns from facebook to match with database")
    #renaming all columns to match with database column names
    for i in range(len(read_conf['apiConfig']['columns'])):
        if read_conf['apiConfig']['columns'][i].upper()!=read_conf['tableConfig']['columns'][i].upper():
            df3.rename(columns={read_conf['apiConfig']['columns'][i]:read_conf['tableConfig']['columns'][i]},inplace=True)
        else:
            df3.rename(columns={read_conf['apiConfig']['columns'][i]+"_gs": read_conf['tableConfig']['columns'][i]},inplace=True)

    df3=df3[read_conf['tableConfig']['columns']]

    print(str(datetime.datetime.now())+": Inserting data into database")
    if df3.shape[0]>0:
        print("total data to append: "+str(len(df3)))
        df3.to_sql(name=table_name, schema=read_conf['targetSchemaName'],con=conn, index=False, if_exists='append',chunksize=300)
    else:
        print(str(datetime.datetime.now())+": No data to append. Table is in sync with facebook api")
    print(str(datetime.datetime.now())+": Finishing the run of script "+os.path.basename(sys.argv[0])+" for fetching ads data for "+sys.argv[1])

if __name__=="__main__":
    try:
        load_data()
    except Exception as e:
        print("#########################################")
        print(e)