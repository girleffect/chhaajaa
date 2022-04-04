from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import pandas as pd,sys,os,json,ast
from sqlalchemy import create_engine

def get_report_date(inp_date):
  flag = sys.argv[2]
  start_date = inp_date
  if flag == 'weekly':
    if inp_date.weekday() != 0:
      diff = 0 - inp_date.weekday()
      start_date = inp_date + datetime.timedelta(days=diff)
    end_date = start_date + datetime.timedelta(days=6)
  elif flag == 'daily':
    end_date = start_date
  elif flag == 'monthly':
    start_date = inp_date
    start_date = start_date + datetime.timedelta(days=((start_date.day * -1) + 1))
    end_date = start_date + datetime.timedelta(days=32)
    end_date = end_date + datetime.timedelta(days=((end_date.day * -1)))
  else:
    print("Invalid 2nd parameter. It should be monthly,weekly,daily")
    exit(1)
  return start_date, end_date

def initialize_analyticsreporting(SCOPES):#,KEY_FILE_LOCATION):
  credentials = ServiceAccountCredentials.from_json_keyfile_dict(
      ast.literal_eval(os.environ['service_account_dict']), SCOPES)

  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics,report_body):
  return analytics.reports().batchGet(
      body=report_body
  ).execute()


def get_data(response,prep_data,flag):
  calc_user=0
  new_users=0
  find_service_near_you=0
  service_finder=0
  tiko_explore=0
  for key in response['reports']:
    if key['columnHeader']['dimensions'][0] == 'ga:eventCategory' and \
            key['columnHeader']['metricHeader']['metricHeaderEntries'][0]['name'] == 'ga:totalEvents':
      if 'rows' in key['data']:
        for dim in key['data']['rows']:
          if dim['dimensions'][0] not in ['Scroll Interactions', 'Video Interactions']:
            calc_user = int(dim['metrics'][0]['values'][0]) + calc_user
    elif key['columnHeader']['dimensions'][0] == 'ga:channelGrouping' and \
            key['columnHeader']['metricHeader']['metricHeaderEntries'][0]['name'] == 'ga:users':
      new_users=key['data']['totals'][0]['values'][0]
    elif key['columnHeader']['dimensions'][0] == 'ga:pagePath' and \
            key['columnHeader']['metricHeader']['metricHeaderEntries'][0]['name'] == 'ga:totalEvents':
      if 'rows' in key['data']:
        for dim in key['data']['rows']:
          if dim['dimensions'][0].split('/')[-2] == 'find-service-near-you' and dim['dimensions'][0].split('/')[-1] == '':
            find_service_near_you = round((int(dim['metrics'][0]['values'][0]) / int(key['data']['totals'][0]['values'][0])) * 100)
          if dim['dimensions'][0] == '/' or ( dim['dimensions'][0].split('/')[-2] == 'service-finder' and dim['dimensions'][0].split('/')[-1] == ''):
            service_finder = service_finder + round((int(dim['metrics'][0]['values'][0]) / int(key['data']['totals'][0]['values'][0])) * 100)
          if dim['dimensions'][0].split('/')[-2] == 'tiko-explore' and dim['dimensions'][0].split('/')[-1] == '':
            tiko_explore = round((int(dim['metrics'][0]['values'][0]) / int(key['data']['totals'][0]['values'][0])) * 100)
  if flag=='m':
    prep_data['new_service_link_click']=calc_user
    prep_data['new_users']=new_users
    prep_data['find_service_near_you']=find_service_near_you
    prep_data['service_finder']=service_finder
    prep_data['tiko_explore']=tiko_explore
    prep_data['others']=100-(find_service_near_you+service_finder+tiko_explore)
    if prep_data['others'][0]==100:
      prep_data['others']=0
  elif flag=='l':
    prep_data['lifetime_users']=new_users
    prep_data['lifetime_service_link_click']=calc_user
  elif flag=='p':
    prep_data['prev_month_new_user']=new_users

def main():
  print(str(datetime.datetime.now())+": Starting the run of script " + os.path.basename(sys.argv[0]) + " for fetching google analytics data for " +
        sys.argv[1])
  CONF_FILE = '../conf/' + os.path.basename(sys.argv[0]).split('.')[0] + '_' + sys.argv[1] + '.conf'

  print(str(datetime.datetime.now())+": Conf file for this run is " + CONF_FILE)

  # using utf-8 to read hindi text also
  with open(CONF_FILE, 'r', encoding='utf-8') as read_conf_file:
    read_conf = json.load(read_conf_file)


  SCOPES = read_conf['scopes']
  #KEY_FILE_LOCATION = read_conf['googleKeyFile']
  VIEW_ID = read_conf['view_id']

  print(str(datetime.datetime.now())+": Initializing the google analytics report")
  analytics = initialize_analyticsreporting(SCOPES)#,KEY_FILE_LOCATION)

  print(str(datetime.datetime.now())+": Setting the time dates for reports")

  print(str(datetime.datetime.now())+": Get maximum date from database upto which data is loaded")
  conn = create_engine('postgresql://' + os.environ['dbUserName'] + ':' + os.environ['dbPassword'] + '@' + os.environ['dbServer'] + '/' + os.environ['dbUserName'])
  df_dt = pd.read_sql("select max(report_end_date) max_date from  " + read_conf['targetSchemaName'] + "." + read_conf['targetTableName'], conn)

  since_inception_date=read_conf['start_dt']
  if df_dt['max_date'][0] == None:
    startDt = datetime.datetime.strptime(since_inception_date, '%Y-%m-%d').date()
  else:
    startDt = df_dt['max_date'][0] + datetime.timedelta(days=-1)

  start_dt, end_dt = get_report_date(startDt)
  if start_dt < datetime.datetime.strptime(since_inception_date, '%Y-%m-%d').date():
    start_dt=datetime.datetime.strptime(since_inception_date, '%Y-%m-%d').date()

  conf_end_dt = datetime.date.today()
  df = pd.DataFrame(columns=read_conf['apiConfig']['columns'])

  while conf_end_dt+datetime.timedelta(-1) >= end_dt:
    print(str(datetime.datetime.now())+": Get all the data for start date " + str(start_dt)+" and end date "+str(end_dt))
    lst=[[datetime.datetime.today(), "Chhaa Jaa Public Site",None,None,start_dt,end_dt,None,None,None,None,None,None,None]]
    prep_data=pd.DataFrame(lst, columns=read_conf['apiConfig']['columns'])
    report_body_monthly=dict({
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate':str(start_dt), 'endDate': str(end_dt)}],
          'metrics': [{'expression': 'ga:users'}],
          'dimensions': [{'name': 'ga:channelGrouping'}]
        },{
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': str(start_dt), 'endDate': str(end_dt)}],
          'metrics': [{'expression': 'ga:totalEvents'}],
          'dimensions': [{'name': 'ga:eventCategory'}]
        },
          {
            'viewId': VIEW_ID,
            'dateRanges': [{'startDate': str(start_dt), 'endDate': str(end_dt)}],
            'metrics': [{'expression': 'ga:totalEvents'}],
            'dimensions': [{'name': 'ga:pagePath'}]
          }
        ]})
    response = get_report(analytics,report_body_monthly)
    get_data(response,prep_data,'m')
    report_body_lifetime = dict({
    'reportRequests': [
      {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': since_inception_date, 'endDate': str(end_dt)}],
        'metrics': [{'expression': 'ga:users'}],
        'dimensions': [{'name': 'ga:channelGrouping'}]
      }, {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate':  since_inception_date, 'endDate':str(end_dt)}],
        'metrics': [{'expression': 'ga:totalEvents'}],
        'dimensions': [{'name': 'ga:eventCategory'}]
      }
    ]})
    response = get_report(analytics, report_body_lifetime)
    get_data(response, prep_data,'l')
    curr_month=int(str(end_dt).split('-')[1])
    curr_year = int(str(end_dt).split('-')[0])
    curr_day = int(str(end_dt).split('-')[2])
    if curr_month==1:
      curr_month=13
      curr_year=curr_year-1
    if curr_day==31 or (curr_month==3 and curr_day>28):
      day_of_prev_month = end_dt.replace(day=1)+datetime.timedelta(days=-1)
    else:
      day_of_prev_month = end_dt.replace(month=curr_month-1,year=curr_year)
    first_day_of_prev_month=day_of_prev_month.replace(day=1).strftime("%Y-%m-%d")
    report_body_pre_monthly = dict({
    'reportRequests': [
      {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': first_day_of_prev_month, 'endDate': day_of_prev_month.strftime("%Y-%m-%d")}],
        'metrics': [{'expression': 'ga:users'}],
        'dimensions': [{'name': 'ga:channelGrouping'}]
      }
    ]})
    response = get_report(analytics, report_body_pre_monthly)
    get_data(response, prep_data,'p')
    df=df.append(prep_data,ignore_index=True)
    start_dt=end_dt+datetime.timedelta(days=1)
    start_dt, end_dt = get_report_date(start_dt)

  print("Fetching data from database")

  df2 = pd.read_sql("select * from  " + read_conf['targetSchemaName'] + "." + read_conf['targetTableName'], conn)
  print(str(datetime.datetime.now())+": Camparing/joining data from google analytics with data in database")
  df3 = pd.merge(df, df2, right_on=read_conf['tableConfig']['joinColumns'],
                   left_on=read_conf['apiConfig']['joinColumns'], how='left', suffixes=['_gs', '_db'])

  print(str(datetime.datetime.now())+": Filter only new data, which is not present in database. Drop the old data")
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

  print(str(datetime.datetime.now())+": Rename columns to match with database")
    # renaming all columns to match with database column names
  for i in range(len(read_conf['apiConfig']['columns'])):
    if read_conf['apiConfig']['columns'][i].upper() != read_conf['tableConfig']['columns'][i].upper():
      df3.rename(columns={read_conf['apiConfig']['columns'][i]: read_conf['tableConfig']['columns'][i]}, inplace=True)
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
    print(str(datetime.datetime.now())+": No data to append. Table is in sync with google analytics")
  print(str(datetime.datetime.now())+": Finishing the run of script " + os.path.basename(sys.argv[0]) + " for fetching google analytics data for " + sys.argv[1])


if __name__ == '__main__':
  main()
