import requests
import sys,json,os,pandas as pd,numpy as np
import datetime
from sqlalchemy import create_engine
import numpy as np

def get_report_date(inp_date,flag):
    if flag == 'day':
        start_dt = inp_date.split('T')[0]
        end_dt = inp_date.split('T')[0]
    elif flag == 'week':
        end_dt = datetime.datetime.strptime(inp_date.split('T')[0], '%Y-%m-%d').date()
        start_dt = end_dt + datetime.timedelta(days=-6)
    elif flag == 'days_28':
        end_dt = datetime.datetime.strptime(inp_date.split('T')[0], '%Y-%m-%d').date()
        start_dt = end_dt + datetime.timedelta(days=-27)
    else:
        print(str(datetime.datetime.now())+": Invalid 2nd parameter. It should be monthly,weekly,daily")
        exit(1)
    return str(start_dt),str(end_dt)

def get_api_data(url,input_df,parameters={}):
    object = requests.get(url, params=parameters).text.encode('utf-8')
    data = json.loads(object)
    for i in data['data']:
        flag = i['period']
        start_d, end_d = get_report_date(i['values'][0]['end_time'], flag)
        start_d1, end_d1 = get_report_date(i['values'][1]['end_time'], flag)
        if datetime.datetime.strptime(end_d,'%Y-%m-%d').date() < datetime.date.today() :
            input_df = input_df.append(pd.Series([start_d, end_d, i['values'][0]['value']['other'], flag], index=input_df.columns),
                         ignore_index=True)
            input_df = input_df.append(pd.Series([start_d1, end_d1, i['values'][1]['value']['other'], flag], index=input_df.columns),
                           ignore_index=True)
    if 'next' in  data['paging']:
        input_df=input_df.append(get_api_data(data['paging']['next'],input_df))

    input_df=input_df.drop_duplicates()
    return input_df

def load_data():
    print(str(datetime.datetime.now())+": Starting the run of script " + os.path.basename(sys.argv[0]) + " for fetching page user activity data for " + sys.argv[1])
    CONF_FILE = '../conf/' + os.path.basename(sys.argv[0]).split('.')[0] + '_' + sys.argv[1] + '.conf'

    print(str(datetime.datetime.now())+": Conf file for this run is " + CONF_FILE)

    # using utf-8 to read hindi text also
    with open(CONF_FILE, 'r', encoding='utf-8') as read_conf_file:
        read_conf = json.load(read_conf_file)

    base = read_conf['base_url']
    node = os.environ['FACEBOOK_PAGE_ID'] + '/insights/page_content_activity_by_action_type_unique'
    url = base + node
    #parameters = {'time_range':{'since':'2020-11-01','until':'2020-11-07'}, 'access_token': read_conf['access_token']}
    parameters = {'access_token': os.environ['FACEBOOK_ACCESS_TOKEN'] }

    print(str(datetime.datetime.now())+": Getting Data from the graph api.")
    df1 = pd.DataFrame(columns=read_conf['fields'])
    df =get_api_data(url,df1,parameters)
    print(str(datetime.datetime.now())+": Data from the graph api is fetched and stored in dataframe")
    print(str(datetime.datetime.now())+": Started the Cleaning of page user activity data")
    df = df.replace('', '0')
    df = df.replace(' ', '0')
    df = df.replace(np.nan, '0')
    print(str(datetime.datetime.now())+": Finished the Cleaning of user activity data")
    print(str(datetime.datetime.now())+": Modifying the column data types to match with database tables")
    for i in range(len(read_conf['apiConfig']['columnTypes'])):
        if read_conf['apiConfig']['columnTypes'][i] != 'str':
            if (read_conf['apiConfig']['columnTypes'][i] == 'int' and df.dtypes[read_conf['apiConfig']['columns'][i]]!=np.int64 ) or read_conf['apiConfig']['columnTypes'][i] == 'float':
                #df[read_conf['apiConfig']['columns'][i]] = df[read_conf['apiConfig']['columns'][i]].str.replace('$', '')
                #df[read_conf['apiConfig']['columns'][i]] = df[read_conf['apiConfig']['columns'][i]].str.replace(',', '')
                #df[read_conf['apiConfig']['columns'][i]] = df[read_conf['apiConfig']['columns'][i]].str.replace('%', '')
                #df[read_conf['apiConfig']['columns'][i]] = df[read_conf['apiConfig']['columns'][i]].str.replace(' ','0')
                df[read_conf['apiConfig']['columns'][i]] = df[read_conf['apiConfig']['columns'][i]].astype(read_conf['apiConfig']['columnTypes'][i])
            if read_conf['apiConfig']['columnTypes'][i] == 'date' :
                df[read_conf['apiConfig']['columns'][i]] = pd.Series([datetime.datetime.strptime(j, '%Y-%m-%d').date() for  j in df[read_conf['apiConfig']['columns'][i]]])

    print(str(datetime.datetime.now())+": Columns datatype modification is complete.")
    print(str(datetime.datetime.now())+": Fetching data from database")
    conn = create_engine('postgresql://' + os.environ['dbUserName'] + ':' + os.environ['dbPassword'] + '@' + os.environ['dbServer'] + '/' + os.environ['dbUserName'])

    df2 = pd.read_sql("select * from  " + read_conf['targetSchemaName'] + "." + read_conf['targetTableName'], conn)
    print(str(datetime.datetime.now())+": Camparing/joining data from facebook with data in database")
    df3 = pd.merge(df, df2, right_on=read_conf['tableConfig']['joinColumns'],left_on=read_conf['apiConfig']['joinColumns'], how='left', suffixes=['_gs', '_db'])

    print(str(datetime.datetime.now())+": Filter only new data from facebook which is not present in database. Drop the old data")
    for i in range(len(read_conf['apiConfig']['columns'])):
        # checking if column is key column or used in joins
        if read_conf['apiConfig']['columns'][i] not in read_conf['apiConfig']['joinColumns']:
            if read_conf['apiConfig']['columns'][i] != read_conf['tableConfig']['columns'][i]:
                # picking only new value. Dropping exisitng values
                df3 = df3[df3[read_conf['tableConfig']['columns'][i]].isnull()]
                # dropping the column coming from database
                df3.drop(columns=[read_conf['tableConfig']['columns'][i]], inplace=True)
            else:
                df3 = df3[df3[read_conf['tableConfig']['columns'][i] + '_db'].isnull()]
                df3.drop(columns=[read_conf['tableConfig']['columns'][i] + '_db'], inplace=True)

    print(str(datetime.datetime.now())+": Rename columns from facebook to match with database")
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
        print(str(datetime.datetime.now())+": total data to append: " + str(len(df3)))
        df3.to_sql(name=read_conf['targetTableName'], schema=read_conf['targetSchemaName'], con=conn, index=False, if_exists='append',
                   chunksize=300)
    else:
        print(str(datetime.datetime.now())+": No data to append. Table is in sync with facebook api")
    print(str(datetime.datetime.now())+": Finishing the run of script " + os.path.basename(sys.argv[0]) + " for fetching ads data for " + sys.argv[1])


if __name__=="__main__":
    # try:
        load_data()
    # except Exception as e:
    #     print("#########################################")
    #     print(e)