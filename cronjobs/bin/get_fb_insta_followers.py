import os,sys,numpy as np
import pandas as pd
from sqlalchemy import create_engine
from instascrape import *
#import instascrape
#from datetime import datetime

def load_data():
    print(str(datetime.datetime.now())+": Starting the run of script " + os.path.basename(sys.argv[0]) + " for fetching page user activity data for " + sys.argv[1])
    CONF_FILE = '../conf/' + os.path.basename(sys.argv[0]).split('.')[0] + '_' + sys.argv[1] + '.conf'

    print(str(datetime.datetime.now())+": Conf file for this run is " + CONF_FILE)

    # using utf-8 to read hindi text also
    with open(CONF_FILE, 'r', encoding='utf-8') as read_conf_file:
        read_conf = json.load(read_conf_file)

    print(str(datetime.datetime.now())+": Getting the instagram followers")
    url=read_conf['insta_url']
    instagram = Profile(read_conf['insta_url'])


    # Scrape their respective data
    instagram.scrape()

    r = requests.get(url)

    #metatag1 = soup.find('title')

    insta_followers=instagram.followers

    print(str(datetime.datetime.now())+": Getting the facebook followers and likes")
    url=read_conf['fb_url']
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    divclass = soup.find_all('div', {'class': '_3xom'})
    fb_followers=str(divclass[1]).split('>')[1].split('<')[0]
    fb_likes=str(divclass[0]).split('>')[1].split('<')[0]
    as_on_date=str(datetime.date.today())

    print(str(datetime.datetime.now())+": Preparing data for database insertion")
    df = pd.DataFrame(columns=read_conf['fields'])
    df = df.append(pd.Series([as_on_date, 'fb_followers', fb_followers], index=df.columns),
                   ignore_index=True)
    df = df.append(pd.Series([as_on_date, 'insta_followers', insta_followers], index=df.columns),
                   ignore_index=True)
    df = df.append(pd.Series([as_on_date, 'fb_likes', fb_likes], index=df.columns),
                   ignore_index=True)

    df = df.replace('', 0)
    df = df.replace(' ', 0)
    df = df.replace(np.nan, 0)

    print(str(datetime.datetime.now())+": Modifying column datatypes to  match with database column types")
    for i in range(len(read_conf['tableConfig']['columnTypes'])):
        if read_conf['tableConfig']['columnTypes'][i]!='str':
            df[read_conf['apiConfig']['columns'][i]] = df[read_conf['apiConfig']['columns'][i]].astype(str)
            if read_conf['tableConfig']['columnTypes'][i]=='int' or read_conf['tableConfig']['columnTypes'][i] == 'float':
                df[read_conf['apiConfig']['columns'][i]]=df[read_conf['apiConfig']['columns'][i]].str.replace('$','')
                df[read_conf['apiConfig']['columns'][i]]=df[read_conf['apiConfig']['columns'][i]].str.replace(',','')
                df[read_conf['apiConfig']['columns'][i]]=df[read_conf['apiConfig']['columns'][i]].str.replace('%','')
                df[read_conf['apiConfig']['columns'][i]] = df[read_conf['apiConfig']['columns'][i]].str.replace(' ', '0')
                df[read_conf['apiConfig']['columns'][i]]=df[read_conf['apiConfig']['columns'][i]].astype(read_conf['tableConfig']['columnTypes'][i])
            if read_conf['tableConfig']['columnTypes'][i]=='date':
                df[read_conf['apiConfig']['columns'][i]]=pd.Series([datetime.datetime.strptime(i.split(' ')[0], '%Y-%m-%d').date() for i in df[read_conf['apiConfig']['columns'][i]]])

    print(str(datetime.datetime.now())+": Columns datatype modification is complete.")
    print(str(datetime.datetime.now())+": Fetching data from database")
    conn = create_engine('postgresql://' + os.environ['dbUserName'] + ':' + os.environ['dbPassword'] + '@' + os.environ['dbServer'] + '/' + os.environ['dbUserName'])

    df2 = pd.read_sql("select * from  " + read_conf['targetSchemaName'] + "." + read_conf['targetTableName'], conn)
    print(str(datetime.datetime.now())+": Camparing/joining data from facebook/insta with data in database")
    df3 = pd.merge(df, df2, right_on=read_conf['tableConfig']['joinColumns'],
                   left_on=read_conf['apiConfig']['joinColumns'], how='left', suffixes=['_gs', '_db'])


    print(str(datetime.datetime.now())+": Filter only new data from facebook/insta which is not present in database. Drop the old data")
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

    print(str(datetime.datetime.now())+": Rename columns from facebook/insta to match with database")
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
        df3.to_sql(name=read_conf['targetTableName'], schema=read_conf['targetSchemaName'], con=conn, index=False, if_exists='append',
                   chunksize=300)
    else:
        print(str(datetime.datetime.now())+": No data to append. Table is in sync with pages")
    print(str(datetime.datetime.now())+": Finishing the run of script " + os.path.basename(sys.argv[0]) + " for fetching page followers data for " + sys.argv[1])


if __name__=="__main__":
    try:
        load_data()
    except Exception as e:
        print(str(datetime.datetime.now())+": #########################################")
        print(e)

