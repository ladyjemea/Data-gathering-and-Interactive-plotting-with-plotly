#pylint: disable=all
#pylint: disable=no-member
import pandas as pd
import numpy as np
import subprocess
from pandas import read_csv
from csv import reader
import datetime as dtm
import time
from datetime import timezone, datetime
import json
import os
import sys
import requests
from bs4 import BeautifulSoup
from io import StringIO


yr = dtm.datetime.utcnow().year
mo = dtm.datetime.utcnow().month
today =dtm.datetime.utcnow().day
next_day = (dtm.datetime.utcnow() + dtm.timedelta(days=1)).day
time = dtm.datetime.utcnow()
hour = time.hour
minute = time.minute
date = dtm.datetime(year=yr, month=mo, day=today, hour=hour, minute=minute)
wk = date.isocalendar()[1]



''' Data collection and filtering from multiple sources'''

date = dtm.datetime.utcnow()

year = dtm.datetime.strftime(date, '%Y')
year_kp = dtm.datetime.strftime(date, '%y')
month = dtm.datetime.strftime(date, '%m')
day = dtm.datetime.strftime(date, '%d')



'''Data processing'''

#MAGNRTOMETER TROMSØ
try:
    url_tro = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=tro2a&year="+year+"&month="+month+"&day="+day+"&res=10sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+" #reading 10 second daily data
    dfTro = pd.read_csv(url_tro, skiprows = 7) #put data from url in a dataframe and skip the first 7 rows

    dfTro = dfTro.astype(str) #convert dataframe to string
    dfTro = dfTro[dfTro.columns[0]].str.split(expand=True) 

    dfTro.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot'] #give column headers for easy identification
    dfTro['timestamp'] = dfTro['Date'] + ' ' + dfTro['Time'] #create a new column from two columns
    dfTro.drop(dfTro.columns.difference(['Horiz', 'timestamp']), 1, inplace=True) #drop all columns except 'Horiz' and 'timestamp'
    dfTro = dfTro[dfTro.Horiz != '99999.9'] #remove invalid values
    dfTro.rename(columns={'Horiz':'Horiz_tro'}, inplace=True) #rename a column
    dfTro['timestamp'] = pd.to_datetime(dfTro['timestamp'], format = '%d/%m/%Y %H:%M:%S') #convert timestamp column to datetime
    dfTro.set_index('timestamp', inplace=True) #set column as index

    with open('Magnetometer/data/magnetometer_tro.csv', 'a')as f: #open csv for writing data
        if os.path.getsize('Magnetometer/data/magnetometer_tro.csv') <= 0: #check if csv is empty
            dfTro.to_csv(f, header=f.tell()==0, index =True, sep = " ") #write content of dataframe to csv
        elif os.path.getsize('Magnetometer/data/magnetometer_tro.csv') > 0: #checking if the csv has data in it
            df1 = pd.read_csv('Magnetometer/data/magnetometer_tro.csv', sep = " ") #read the content of the csv
            df1['timestamp'] = pd.to_datetime(df1['timestamp']) #convert timestamp to datetime
            df1.set_index('timestamp', inplace=True) #set timestamp as index
            if dtm.datetime.utcnow() > df1.index[-2]: #check time difference between current time and time at last value in the csv
                values = dfTro.index > df1.index[-2] #get all rows which are not in csv
                df1 = dfTro[values] #create new dataframe with these rows
                df1.to_csv('Magnetometer/data/magnetometer_tro.csv', mode='a', index =True, sep = " ", header = False) #append the rows to existing csv
    f.close()

    #ACTIVITY INDEX TROMSØ
    dfTro = pd.read_csv('Magnetometer/data/magnetometer_tro.csv', sep = " ") #read data in the csv
    dfTro = dfTro.drop_duplicates(subset=['timestamp']) #drop all duplicate rows

    dfTro['timestamp'] = pd.to_datetime(dfTro['timestamp']) #convert time column to datetime
    dfTro.set_index('timestamp', inplace=True) #set time column as index

    length_tro = len(dfTro.index)-1 #get the length of the dataframe
    for i in range(length_tro): #insert nan value if there is a data gap of more than 5 minutes between rows
        if (dfTro.index[i+1]-dfTro.index[i]).seconds >= 300:
            dfTro.loc[dfTro.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfTro.sort_index(inplace=True) #rearrange the index after inserting the nan values

    dfTro_ai = dfTro.resample('H')['Horiz_tro'].agg(['max', 'min']) #create a new dataframe with max and min values for a specific column for each hour 
    dfTro_ai['diff'] = dfTro_ai['max'].sub(dfTro_ai['min'], axis = 0) #get the difference between the max and min for each hour in a column
    dfTro_ai['diff'] = dfTro_ai['diff'].shift(1) #move the rows down by one
    dfTro_ai.to_csv('Magnetometer/data/ai/Tro.csv', sep = " ") #write the values to a csv
except:
    pass



#MAGNRTOMETER DOMBÅS
try:
    url_dob = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=dob1a&year="+year+"&month="+month+"&day="+day+"&res=10sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfDob = pd.read_csv(url_dob, skiprows = 7)

    dfDob = dfDob.astype(str)
    dfDob = dfDob[dfDob.columns[0]].str.split(expand=True)

    dfDob.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfDob['timestamp'] = dfDob['Date'] + ' ' + dfDob['Time']
    dfDob.drop(dfDob.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfDob = dfDob[dfDob.Horiz != '99999.9']
    dfDob.rename(columns={'Horiz':'Horiz_dob'}, inplace=True)
    dfDob['timestamp'] = pd.to_datetime(dfDob['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfDob.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_dob.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_dob.csv') <= 0:
            dfDob.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_dob.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_dob.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfDob.index > df1.index[-2]
                df1 = dfDob[values]
                df1.to_csv('Magnetometer/data/magnetometer_dob.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX DOMBÅS
    dfDob = pd.read_csv('Magnetometer/data/magnetometer_dob.csv', sep = " ")
    dfDob = dfDob.drop_duplicates(subset=['timestamp'])

    dfDob['timestamp'] = pd.to_datetime(dfDob['timestamp'])
    dfDob.set_index('timestamp', inplace=True)

    length_dob = len(dfDob.index)-1
    for i in range(length_dob):
        if (dfDob.index[i+1]-dfDob.index[i]).seconds >= 300:
            dfDob.loc[dfDob.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfDob.sort_index(inplace=True)

    dfDob_ai = dfDob.resample('H')['Horiz_dob'].agg(['max', 'min'])
    dfDob_ai['diff'] = dfDob_ai['max'].sub(dfDob_ai['min'], axis = 0)
    dfDob_ai['diff'] = dfDob_ai['diff'].shift(1)
    dfDob_ai.to_csv('Magnetometer/data/ai/Dob.csv', sep = " ")
except:
    pass



#MAGNRTOMETER NY ÅLESUND
try:
    url_nal = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=nal1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfNal = pd.read_csv(url_nal, skiprows = 7)

    dfNal = dfNal.astype(str)
    dfNal = dfNal[dfNal.columns[0]].str.split(expand=True)

    dfNal.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfNal['timestamp'] = dfNal['Date'] + ' ' + dfNal['Time']
    dfNal.drop(dfNal.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfNal = dfNal[dfNal.Horiz != '99999.9']
    dfNal.rename(columns={'Horiz':'Horiz_nal'}, inplace=True)
    dfNal['timestamp'] = pd.to_datetime(dfNal['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfNal.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_nal.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_nal.csv') <= 0:
            dfNal.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_nal.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_nal.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfNal.index > df1.index[-2]
                df1 = dfNal[values]
                df1.to_csv('Magnetometer/data/magnetometer_nal.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX NY ÅLESUND
    dfNal = pd.read_csv('Magnetometer/data/magnetometer_nal.csv', sep = " ")
    dfNal = dfNal.drop_duplicates(subset=['timestamp'])

    dfNal['timestamp'] = pd.to_datetime(dfNal['timestamp'])
    dfNal.set_index('timestamp', inplace=True)

    length_nal = len(dfNal.index)-1
    for i in range(length_nal):
        if (dfNal.index[i+1]-dfNal.index[i]).seconds >= 300:
            dfNal.loc[dfNal.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfNal.sort_index(inplace=True)

    dfNal_ai = dfNal.resample('H')['Horiz_nal'].agg(['max', 'min'])
    dfNal_ai['diff'] = dfNal_ai['max'].sub(dfNal_ai['min'], axis = 0)
    dfNal_ai['diff'] = dfNal_ai['diff'].shift(1)
    dfNal_ai.to_csv('Magnetometer/data/ai/Nal.csv', sep = " ")
except:
    pass



#MAGNRTOMETER SVALBARD
try:
    url_sva = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=lyr2a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfSva = pd.read_csv(url_sva, skiprows = 7)

    dfSva = dfSva.astype(str)
    dfSva = dfSva[dfSva.columns[0]].str.split(expand=True)

    dfSva.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfSva['timestamp'] = dfSva['Date'] + ' ' + dfSva['Time']
    dfSva.drop(dfSva.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfSva = dfSva[dfSva.Horiz != '99999.9']
    dfSva.rename(columns={'Horiz':'Horiz_sva'}, inplace=True)
    dfSva['timestamp'] = pd.to_datetime(dfSva['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfSva.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_sva.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_sva.csv') <= 0:
            dfSva.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_sva.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_sva.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfSva.index > df1.index[-2]
                df1 = dfSva[values]
                df1.to_csv('Magnetometer/data/magnetometer_sva.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX SVALBARD
    dfSva = pd.read_csv('Magnetometer/data/magnetometer_sva.csv', sep = " ")
    dfSva = dfSva.drop_duplicates(subset=['timestamp'])

    dfSva['timestamp'] = pd.to_datetime(dfSva['timestamp'])
    dfSva.set_index('timestamp', inplace=True)

    length_sva = len(dfSva.index)-1
    for i in range(length_sva):
        if (dfSva.index[i+1]-dfSva.index[i]).seconds >= 300:
            dfSva.loc[dfSva.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfSva.sort_index(inplace=True)

    dfSva_ai = dfSva.resample('H')['Horiz_sva'].agg(['max', 'min'])
    dfSva_ai['diff'] = dfSva_ai['max'].sub(dfSva_ai['min'], axis = 0)
    dfSva_ai['diff'] = dfSva_ai['diff'].shift(1)
    dfSva_ai.to_csv('Magnetometer/data/ai/Sva.csv', sep = " ")
except:
    pass



#MAGNRTOMETER ANDENES
try:
    url_and = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=and1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfAnd = pd.read_csv(url_and, skiprows = 7)

    dfAnd = dfAnd.astype(str)
    dfAnd = dfAnd[dfAnd.columns[0]].str.split(expand=True)

    dfAnd.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfAnd['timestamp'] = dfAnd['Date'] + ' ' + dfAnd['Time']
    dfAnd.drop(dfAnd.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfAnd = dfAnd[dfAnd.Horiz != '99999.9']
    dfAnd.rename(columns={'Horiz':'Horiz_and'}, inplace=True)
    dfAnd['timestamp'] = pd.to_datetime(dfAnd['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfAnd.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_and.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_and.csv') <= 0:
            dfAnd.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_and.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_and.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfAnd.index > df1.index[-2]
                df1 = dfAnd[values]
                df1.to_csv('Magnetometer/data/magnetometer_and.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX ANDENES
    dfAnd = pd.read_csv('Magnetometer/data/magnetometer_and.csv', sep = " ")
    dfAnd = dfAnd.drop_duplicates(subset=['timestamp'])

    dfAnd['timestamp'] = pd.to_datetime(dfAnd['timestamp'])
    dfAnd.set_index('timestamp', inplace=True)

    length_and = len(dfAnd.index)-1
    for i in range(length_and):
        if (dfAnd.index[i+1]-dfAnd.index[i]).seconds >= 300:
            dfAnd.loc[dfAnd.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfAnd.sort_index(inplace=True)

    dfAnd_ai = dfAnd.resample('H')['Horiz_and'].agg(['max', 'min'])
    dfAnd_ai['diff'] = dfAnd_ai['max'].sub(dfAnd_ai['min'], axis = 0)
    dfAnd_ai['diff'] = dfAnd_ai['diff'].shift(1)
    dfAnd_ai.to_csv('Magnetometer/data/ai/And.csv', sep = " ")
except:
    pass



#MAGNRTOMETER HOPEN
try:
    url_hop = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=hop1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfHop = pd.read_csv(url_hop, skiprows = 7)

    dfHop = dfHop.astype(str)
    dfHop = dfHop[dfHop.columns[0]].str.split(expand=True)

    dfHop.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfHop['timestamp'] = dfHop['Date'] + ' ' + dfHop['Time']
    dfHop.drop(dfHop.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfHop = dfHop[dfHop.Horiz != '99999.9']
    dfHop.rename(columns={'Horiz':'Horiz_hop'}, inplace=True)
    dfHop['timestamp'] = pd.to_datetime(dfHop['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfHop.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_hop.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_hop.csv') <= 0:
            dfHop.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_hop.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_hop.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfHop.index > df1.index[-2]
                df1 = dfHop[values]
                df1.to_csv('Magnetometer/data/magnetometer_hop.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX HOPEN
    dfHop = pd.read_csv('Magnetometer/data/magnetometer_hop.csv', sep = " ")
    dfHop = dfHop.drop_duplicates(subset=['timestamp'])

    dfHop['timestamp'] = pd.to_datetime(dfHop['timestamp'])
    dfHop.set_index('timestamp', inplace=True)

    length_hop = len(dfHop.index)-1
    for i in range(length_hop):
        if (dfHop.index[i+1]-dfHop.index[i]).seconds >= 300:
            dfHop.loc[dfHop.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfHop.sort_index(inplace=True)

    dfHop_ai = dfHop.resample('H')['Horiz_hop'].agg(['max', 'min'])
    dfHop_ai['diff'] = dfHop_ai['max'].sub(dfHop_ai['min'], axis = 0)
    dfHop_ai['diff'] = dfHop_ai['diff'].shift(1)
    dfHop_ai.to_csv('Magnetometer/data/ai/Hop.csv', sep = " ")
except:
    pass



#MAGNRTOMETER BJORNOYA
try:
    url_bjn = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=bjn1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfBjn = pd.read_csv(url_bjn, skiprows = 7)

    dfBjn = dfBjn.astype(str)
    dfBjn = dfBjn[dfBjn.columns[0]].str.split(expand=True)

    dfBjn.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfBjn['timestamp'] = dfBjn['Date'] + ' ' + dfBjn['Time']
    dfBjn.drop(dfBjn.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfBjn = dfBjn[dfBjn.Horiz != '99999.9']
    dfBjn.rename(columns={'Horiz':'Horiz_bjn'}, inplace=True)
    dfBjn['timestamp'] = pd.to_datetime(dfBjn['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfBjn.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_bjn.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_bjn.csv') <= 0:
            dfBjn.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_bjn.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_bjn.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfBjn.index > df1.index[-2]
                df1 = dfBjn[values]
                df1.to_csv('Magnetometer/data/magnetometer_bjn.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX BJORNOYA
    dfBjn = pd.read_csv('Magnetometer/data/magnetometer_bjn.csv', sep = " ")
    dfBjn = dfBjn.drop_duplicates(subset=['timestamp'])

    dfBjn['timestamp'] = pd.to_datetime(dfBjn['timestamp'])
    dfBjn.set_index('timestamp', inplace=True)

    length_bjn = len(dfBjn.index)-1
    for i in range(length_bjn):
        if (dfBjn.index[i+1]-dfBjn.index[i]).seconds >= 300:
            dfBjn.loc[dfBjn.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfBjn.sort_index(inplace=True)

    dfBjn_ai = dfBjn.resample('H')['Horiz_bjn'].agg(['max', 'min'])
    dfBjn_ai['diff'] = dfBjn_ai['max'].sub(dfBjn_ai['min'], axis = 0)
    dfBjn_ai['diff'] = dfBjn_ai['diff'].shift(1)
    dfBjn_ai.to_csv('Magnetometer/data/ai/Bjn.csv', sep = " ")
except:
    pass



#MAGNRTOMETER NORDKAPP
try:
    url_nor = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=nor1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfNor = pd.read_csv(url_nor, skiprows = 7)

    dfNor = dfNor.astype(str)
    dfNor = dfNor[dfNor.columns[0]].str.split(expand=True)

    dfNor.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfNor['timestamp'] = dfNor['Date'] + ' ' + dfNor['Time']
    dfNor.drop(dfNor.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfNor = dfNor[dfNor.Horiz != '99999.9']
    dfNor.rename(columns={'Horiz':'Horiz_nor'}, inplace=True)
    dfNor['timestamp'] = pd.to_datetime(dfNor['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfNor.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_nor.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_nor.csv') <= 0:
            dfNor.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_nor.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_nor.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfNor.index > df1.index[-2]
                df1 = dfNor[values]
                df1.to_csv('Magnetometer/data/magnetometer_nor.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX NORDKAPP
    dfNor = pd.read_csv('Magnetometer/data/magnetometer_nor.csv', sep = " ")
    dfNor = dfNor.drop_duplicates(subset=['timestamp'])

    dfNor['timestamp'] = pd.to_datetime(dfNor['timestamp'])
    dfNor.set_index('timestamp', inplace=True)

    length_nor = len(dfNor.index)-1
    for i in range(length_nor):
        if (dfNor.index[i+1]-dfNor.index[i]).seconds >= 300:
            dfNor.loc[dfNor.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfNor.sort_index(inplace=True)

    dfNor_ai = dfNor.resample('H')['Horiz_nor'].agg(['max', 'min'])
    dfNor_ai['diff'] = dfNor_ai['max'].sub(dfNor_ai['min'], axis = 0)
    dfNor_ai['diff'] = dfNor_ai['diff'].shift(1)
    dfNor_ai.to_csv('Magnetometer/data/ai/Nor.csv', sep = " ")
except:
    pass



#MAGNRTOMETER SOROYA
try:
    url_sor = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=sor1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfSor = pd.read_csv(url_sor, skiprows = 7)

    dfSor = dfSor.astype(str)
    dfSor = dfSor[dfSor.columns[0]].str.split(expand=True)

    dfSor.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfSor['timestamp'] = dfSor['Date'] + ' ' + dfSor['Time']
    dfSor.drop(dfSor.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfSor = dfSor[dfSor.Horiz != '99999.9']
    dfSor.rename(columns={'Horiz':'Horiz_sor'}, inplace=True)
    dfSor['timestamp'] = pd.to_datetime(dfSor['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfSor.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_sor.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_sor.csv') <= 0:
            dfSor.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_sor.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_sor.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfSor.index > df1.index[-2]
                df1 = dfSor[values]
                df1.to_csv('Magnetometer/data/magnetometer_sor.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX SOROYA
    dfSor = pd.read_csv('Magnetometer/data/magnetometer_sor.csv', sep = " ")
    dfSor = dfSor.drop_duplicates(subset=['timestamp'])

    dfSor['timestamp'] = pd.to_datetime(dfSor['timestamp'])
    dfSor.set_index('timestamp', inplace=True)

    length_sor = len(dfSor.index)-1
    for i in range(length_sor):
        if (dfSor.index[i+1]-dfSor.index[i]).seconds >= 300:
            dfSor.loc[dfSor.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfSor.sort_index(inplace=True)

    dfSor_ai = dfSor.resample('H')['Horiz_sor'].agg(['max', 'min'])
    dfSor_ai['diff'] = dfSor_ai['max'].sub(dfSor_ai['min'], axis = 0)
    dfSor_ai['diff'] = dfSor_ai['diff'].shift(1)
    dfSor_ai.to_csv('Magnetometer/data/ai/Sor.csv', sep = " ")
except:
    pass



#MAGNRTOMETER DONNA
try:
    url_don = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=don1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfDon = pd.read_csv(url_don, skiprows = 7)

    dfDon = dfDon.astype(str)
    dfDon = dfDon[dfDon.columns[0]].str.split(expand=True)

    dfDon.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfDon['timestamp'] = dfDon['Date'] + ' ' + dfDon['Time']
    dfDon.drop(dfDon.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfDon = dfDon[dfDon.Horiz != '99999.9']
    dfDon.rename(columns={'Horiz':'Horiz_don'}, inplace=True)
    dfDon['timestamp'] = pd.to_datetime(dfDon['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfDon.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_don.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_don.csv') <= 0:
            dfDon.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_don.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_don.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfDon.index > df1.index[-2]
                df1 = dfDon[values]
                df1.to_csv('Magnetometer/data/magnetometer_don.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX DONNA
    dfDon = pd.read_csv('Magnetometer/data/magnetometer_don.csv', sep = " ")
    dfDon = dfDon.drop_duplicates(subset=['timestamp'])

    dfDon['timestamp'] = pd.to_datetime(dfDon['timestamp'])
    dfDon.set_index('timestamp', inplace=True)

    length_don = len(dfDon.index)-1
    for i in range(length_don):
        if (dfDon.index[i+1]-dfDon.index[i]).seconds >= 300:
            dfDon.loc[dfDon.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfDon.sort_index(inplace=True)

    dfDon_ai = dfDon.resample('H')['Horiz_don'].agg(['max', 'min'])
    dfDon_ai['diff'] = dfDon_ai['max'].sub(dfDon_ai['min'], axis = 0)
    dfDon_ai['diff'] = dfDon_ai['diff'].shift(1)
    dfDon_ai.to_csv('Magnetometer/data/ai/Don.csv', sep = " ")
except:
    pass


#MAGNRTOMETER JACKVICK
try:
    url_jck = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=jck1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfJck = pd.read_csv(url_jck, skiprows = 7)

    dfJck = dfJck.astype(str)
    dfJck = dfJck[dfJck.columns[0]].str.split(expand=True)

    dfJck.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfJck['timestamp'] = dfJck['Date'] + ' ' + dfJck['Time']
    dfJck.drop(dfJck.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfJck = dfJck[dfJck.Horiz != '99999.9']
    dfJck.rename(columns={'Horiz':'Horiz_jck'}, inplace=True)
    dfJck['timestamp'] = pd.to_datetime(dfJck['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfJck.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_jck.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_jck.csv') <= 0:
            dfJck.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_jck.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_jck.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfJck.index > df1.index[-2]
                df1 = dfJck[values]
                df1.to_csv('Magnetometer/data/magnetometer_jck.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX JACKVICK
    dfJck = pd.read_csv('Magnetometer/data/magnetometer_jck.csv', sep = " ")
    dfJck = dfJck.drop_duplicates(subset=['timestamp'])

    dfJck['timestamp'] = pd.to_datetime(dfJck['timestamp'])
    dfJck.set_index('timestamp', inplace=True)

    length_jck = len(dfJck.index)-1
    for i in range(length_jck):
        if (dfJck.index[i+1]-dfJck.index[i]).seconds >= 300:
            dfJck.loc[dfJck.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfJck.sort_index(inplace=True)

    dfJck_ai = dfJck.resample('H')['Horiz_jck'].agg(['max', 'min'])
    dfJck_ai['diff'] = dfJck_ai['max'].sub(dfJck_ai['min'], axis = 0)
    dfJck_ai['diff'] = dfJck_ai['diff'].shift(1)
    dfJck_ai.to_csv('Magnetometer/data/ai/Jck.csv', sep = " ")
except:
    pass



#MAGNRTOMETER RORVIK
try:
    url_rvk = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=rvk1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfRvk = pd.read_csv(url_rvk, skiprows = 7)

    dfRvk = dfRvk.astype(str)
    dfRvk = dfRvk[dfRvk.columns[0]].str.split(expand=True)

    dfRvk.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfRvk['timestamp'] = dfRvk['Date'] + ' ' + dfRvk['Time']
    dfRvk.drop(dfRvk.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfRvk = dfRvk[dfRvk.Horiz != '99999.9']
    dfRvk.rename(columns={'Horiz':'Horiz_rvk'}, inplace=True)
    dfRvk['timestamp'] = pd.to_datetime(dfRvk['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfRvk.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_rvk.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_rvk.csv') <= 0:
            dfRvk.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_rvk.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_rvk.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfRvk.index > df1.index[-2]
                df1 = dfRvk[values]
                df1.to_csv('Magnetometer/data/magnetometer_rvk.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX RORVIK
    dfRvk = pd.read_csv('Magnetometer/data/magnetometer_rvk.csv', sep = " ")
    dfRvk = dfRvk.drop_duplicates(subset=['timestamp'])

    dfRvk['timestamp'] = pd.to_datetime(dfRvk['timestamp'])
    dfRvk.set_index('timestamp', inplace=True)

    length_rvk = len(dfRvk.index)-1
    for i in range(length_rvk):
        if (dfRvk.index[i+1]-dfRvk.index[i]).seconds >= 300:
            dfRvk.loc[dfRvk.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfRvk.sort_index(inplace=True)

    dfRvk_ai = dfRvk.resample('H')['Horiz_rvk'].agg(['max', 'min'])
    dfRvk_ai['diff'] = dfRvk_ai['max'].sub(dfRvk_ai['min'], axis = 0)
    dfRvk_ai['diff'] = dfRvk_ai['diff'].shift(1)
    dfRvk_ai.to_csv('Magnetometer/data/ai/Rvk.csv', sep = " ")
except:
    pass



#MAGNRTOMETER SOLUND
try:
    url_sol = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=sol1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfSol = pd.read_csv(url_sol, skiprows = 7)

    dfSol = dfSol.astype(str)
    dfSol = dfSol[dfSol.columns[0]].str.split(expand=True)

    dfSol.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfSol['timestamp'] = dfSol['Date'] + ' ' + dfSol['Time']
    dfSol.drop(dfSol.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfSol = dfSol[dfSol.Horiz != '99999.9']
    dfSol.rename(columns={'Horiz':'Horiz_sol'}, inplace=True)
    dfSol['timestamp'] = pd.to_datetime(dfSol['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfSol.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_sol.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_sol.csv') <= 0:
            dfSol.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_sol.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_sol.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfSol.index > df1.index[-2]
                df1 = dfSol[values]
                df1.to_csv('Magnetometer/data/magnetometer_sol.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX SOLUND
    dfSol = pd.read_csv('Magnetometer/data/magnetometer_sol.csv', sep = " ")
    dfSol = dfSol.drop_duplicates(subset=['timestamp'])

    dfSol['timestamp'] = pd.to_datetime(dfSol['timestamp'])
    dfSol.set_index('timestamp', inplace=True)

    length_sol = len(dfSol.index)-1
    for i in range(length_sol):
        if (dfSol.index[i+1]-dfSol.index[i]).seconds >= 300:
            dfSol.loc[dfSol.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfSol.sort_index(inplace=True)

    dfSol_ai = dfSol.resample('H')['Horiz_sol'].agg(['max', 'min'])
    dfSol_ai['diff'] = dfSol_ai['max'].sub(dfSol_ai['min'], axis = 0)
    dfSol_ai['diff'] = dfSol_ai['diff'].shift(1)
    dfSol_ai.to_csv('Magnetometer/data/ai/Sol.csv', sep = " ")
except:
    pass



#MAGNRTOMETER KARMOY
try:
    url_kar = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=kar1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfKar = pd.read_csv(url_kar, skiprows = 7)

    dfKar = dfKar.astype(str)
    dfKar = dfKar[dfKar.columns[0]].str.split(expand=True)

    dfKar.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfKar['timestamp'] = dfKar['Date'] + ' ' + dfKar['Time']
    dfKar.drop(dfKar.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfKar = dfKar[dfKar.Horiz != '99999.9']
    dfKar.rename(columns={'Horiz':'Horiz_kar'}, inplace=True)
    dfKar['timestamp'] = pd.to_datetime(dfKar['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfKar.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_kar.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_kar.csv') <= 0:
            dfKar.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_kar.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_kar.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfKar.index > df1.index[-2]
                df1 = dfKar[values]
                df1.to_csv('Magnetometer/data/magnetometer_kar.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX KARMOY
    dfKar = pd.read_csv('Magnetometer/data/magnetometer_kar.csv', sep = " ")
    dfKar = dfKar.drop_duplicates(subset=['timestamp'])

    dfKar['timestamp'] = pd.to_datetime(dfKar['timestamp'])
    dfKar.set_index('timestamp', inplace=True)

    length_kar = len(dfKar.index)-1
    for i in range(length_kar):
        if (dfKar.index[i+1]-dfKar.index[i]).seconds >= 300:
            dfKar.loc[dfKar.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfKar.sort_index(inplace=True)

    dfKar_ai = dfKar.resample('H')['Horiz_kar'].agg(['max', 'min'])
    dfKar_ai['diff'] = dfKar_ai['max'].sub(dfKar_ai['min'], axis = 0)
    dfKar_ai['diff'] = dfKar_ai['diff'].shift(1)
    dfKar_ai.to_csv('Magnetometer/data/ai/Kar.csv', sep = " ")
except:
    pass



#MAGNRTOMETER JAN MAYEN
try:
    url_jan = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=jan1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfJan = pd.read_csv(url_jan, skiprows = 7)

    dfJan = dfJan.astype(str)
    dfJan = dfJan[dfJan.columns[0]].str.split(expand=True)

    dfJan.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfJan['timestamp'] = dfJan['Date'] + ' ' + dfJan['Time']
    dfJan.drop(dfJan.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfJan = dfJan[dfJan.Horiz != '99999.9']
    dfJan.rename(columns={'Horiz':'Horiz_jan'}, inplace=True)
    dfJan['timestamp'] = pd.to_datetime(dfJan['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfJan.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_jan.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_jan.csv') <= 0:
            dfJan.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_jan.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_jan.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfJan.index > df1.index[-2]
                df1 = dfJan[values]
                df1.to_csv('Magnetometer/data/magnetometer_jan.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX JAN MAYEN
    dfJan = pd.read_csv('Magnetometer/data/magnetometer_jan.csv', sep = " ")
    dfJan = dfJan.drop_duplicates(subset=['timestamp'])

    dfJan['timestamp'] = pd.to_datetime(dfJan['timestamp'])
    dfJan.set_index('timestamp', inplace=True)

    length_jan = len(dfJan.index)-1
    for i in range(length_jan):
        if (dfJan.index[i+1]-dfJan.index[i]).seconds >= 300:
            dfJan.loc[dfJan.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfJan.sort_index(inplace=True)

    dfJan_ai = dfJan.resample('H')['Horiz_jan'].agg(['max', 'min'])
    dfJan_ai['diff'] = dfJan_ai['max'].sub(dfJan_ai['min'], axis = 0)
    dfJan_ai['diff'] = dfJan_ai['diff'].shift(1)
    dfJan_ai.to_csv('Magnetometer/data/ai/Jan.csv', sep = " ")
except:
    pass



#MAGNRTOMETER MASI
try:
    url_mas = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=mas1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfMas = pd.read_csv(url_mas, skiprows = 7)

    dfMas = dfMas.astype(str)
    dfMas = dfMas[dfMas.columns[0]].str.split(expand=True)

    dfMas.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfMas['timestamp'] = dfMas['Date'] + ' ' + dfMas['Time']
    dfMas.drop(dfMas.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfMas = dfMas[dfMas.Horiz != '99999.9']
    dfMas.rename(columns={'Horiz':'Horiz_mas'}, inplace=True)
    dfMas['timestamp'] = pd.to_datetime(dfMas['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfMas.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_mas.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_mas.csv') <= 0:
            dfMas.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_mas.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_mas.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfMas.index > df1.index[-2]
                df1 = dfMas[values]
                df1.to_csv('Magnetometer/data/magnetometer_mas.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX MASI
    dfMas = pd.read_csv('Magnetometer/data/magnetometer_mas.csv', sep = " ")
    dfMas = dfMas.drop_duplicates(subset=['timestamp'])

    dfMas['timestamp'] = pd.to_datetime(dfMas['timestamp'])
    dfMas.set_index('timestamp', inplace=True)

    length_mas = len(dfMas.index)-1
    for i in range(length_mas):
        if (dfMas.index[i+1]-dfMas.index[i]).seconds >= 300:
            dfMas.loc[dfMas.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfMas.sort_index(inplace=True)

    dfMas_ai = dfMas.resample('H')['Horiz_mas'].agg(['max', 'min'])
    dfMas_ai['diff'] = dfMas_ai['max'].sub(dfMas_ai['min'], axis = 0)
    dfMas_ai['diff'] = dfMas_ai['diff'].shift(1)
    dfMas_ai.to_csv('Magnetometer/data/ai/Mas.csv', sep = " ")
except:
    pass



#MAGNRTOMETER ROST
try:
    url_rst = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=rst1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfRst = pd.read_csv(url_rst, skiprows = 7)

    dfRst = dfRst.astype(str)
    dfRst = dfRst[dfRst.columns[0]].str.split(expand=True)

    dfRst.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfRst['timestamp'] = dfRst['Date'] + ' ' + dfRst['Time']
    dfRst.drop(dfRst.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfRst = dfRst[dfRst.Horiz != '99999.9']
    dfRst.rename(columns={'Horiz':'Horiz_rst'}, inplace=True)
    dfRst['timestamp'] = pd.to_datetime(dfRst['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfRst.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_rst.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_rst.csv') <= 0:
            dfRst.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_rst.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_rst.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfRst.index > df1.index[-2]
                df1 = dfRst[values]
                df1.to_csv('Magnetometer/data/magnetometer_rst.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX ROST
    dfRst = pd.read_csv('Magnetometer/data/magnetometer_rst.csv', sep = " ")
    dfRst = dfRst.drop_duplicates(subset=['timestamp'])

    dfRst['timestamp'] = pd.to_datetime(dfRst['timestamp'])
    dfRst.set_index('timestamp', inplace=True)

    length_rst = len(dfRst.index)-1
    for i in range(length_rst):
        if (dfRst.index[i+1]-dfRst.index[i]).seconds >= 300:
            dfRst.loc[dfRst.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfRst.sort_index(inplace=True)

    dfRst_ai = dfRst.resample('H')['Horiz_rst'].agg(['max', 'min'])
    dfRst_ai['diff'] = dfRst_ai['max'].sub(dfRst_ai['min'], axis = 0)
    dfRst_ai['diff'] = dfRst_ai['diff'].shift(1)
    dfRst_ai.to_csv('Magnetometer/data/ai/Rst.csv', sep = " ")
except:
    pass



#MAGNRTOMETER HARESTUA
try:
    url_har = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=har1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfHar = pd.read_csv(url_har, skiprows = 7)

    dfHar = dfHar.astype(str)
    dfHar = dfHar[dfHar.columns[0]].str.split(expand=True)

    dfHar.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfHar['timestamp'] = dfHar['Date'] + ' ' + dfHar['Time']
    dfHar.drop(dfHar.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfHar = dfHar[dfHar.Horiz != '99999.9']
    dfHar.rename(columns={'Horiz':'Horiz_har'}, inplace=True)
    dfHar['timestamp'] = pd.to_datetime(dfHar['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfHar.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_har.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_har.csv') <= 0:
            dfHar.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_har.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_har.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfHar.index > df1.index[-2]
                df1 = dfHar[values]
                df1.to_csv('Magnetometer/data/magnetometer_har.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX HARESTUA
    dfHar = pd.read_csv('Magnetometer/data/magnetometer_har.csv', sep = " ")
    dfHar = dfHar.drop_duplicates(subset=['timestamp'])

    dfHar['timestamp'] = pd.to_datetime(dfHar['timestamp'])
    dfHar.set_index('timestamp', inplace=True)

    length_har = len(dfHar.index)-1
    for i in range(length_har):
        if (dfHar.index[i+1]-dfHar.index[i]).seconds >= 300:
            dfHar.loc[dfHar.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfHar.sort_index(inplace=True)

    dfHar_ai = dfHar.resample('H')['Horiz_har'].agg(['max', 'min'])
    dfHar_ai['diff'] = dfHar_ai['max'].sub(dfHar_ai['min'], axis = 0)
    dfHar_ai['diff'] = dfHar_ai['diff'].shift(1)
    dfHar_ai.to_csv('Magnetometer/data/ai/Har.csv', sep = " ")
except:
    pass



#MAGNRTOMETER IVALO
try:
    url_iva = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=iva1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfIva = pd.read_csv(url_iva, skiprows = 7)

    dfIva = dfIva.astype(str)
    dfIva = dfIva[dfIva.columns[0]].str.split(expand=True)

    dfIva.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfIva['timestamp'] = dfIva['Date'] + ' ' + dfIva['Time']
    dfIva.drop(dfIva.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfIva = dfIva[dfIva.Horiz != '99999.9']
    dfIva.rename(columns={'Horiz':'Horiz_iva'}, inplace=True)
    dfIva['timestamp'] = pd.to_datetime(dfIva['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfIva.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_iva.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_iva.csv') <= 0:
            dfIva.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_iva.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_iva.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfIva.index > df1.index[-2]
                df1 = dfIva[values]
                df1.to_csv('Magnetometer/data/magnetometer_iva.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX IVALO
    dfIva = pd.read_csv('Magnetometer/data/magnetometer_iva.csv', sep = " ")
    dfIva = dfIva.drop_duplicates(subset=['timestamp'])

    dfIva['timestamp'] = pd.to_datetime(dfIva['timestamp'])
    dfIva.set_index('timestamp', inplace=True)

    length_iva = len(dfIva.index)-1
    for i in range(length_iva):
        if (dfIva.index[i+1]-dfIva.index[i]).seconds >= 300:
            dfIva.loc[dfIva.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfIva.sort_index(inplace=True)

    dfIva_ai = dfIva.resample('H')['Horiz_iva'].agg(['max', 'min'])
    dfIva_ai['diff'] = dfIva_ai['max'].sub(dfIva_ai['min'], axis = 0)
    dfIva_ai['diff'] = dfIva_ai['diff'].shift(1)
    dfIva_ai.to_csv('Magnetometer/data/ai/Iva.csv', sep = " ")
except:
    pass



#MAGNRTOMETER MUONIO
try:
    url_muo = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=muo1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfMuo = pd.read_csv(url_muo, skiprows = 7)

    dfMuo = dfMuo.astype(str)
    dfMuo = dfMuo[dfMuo.columns[0]].str.split(expand=True)

    dfMuo.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfMuo['timestamp'] = dfMuo['Date'] + ' ' + dfMuo['Time']
    dfMuo.drop(dfMuo.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfMuo = dfMuo[dfMuo.Horiz != '99999.9']
    dfMuo.rename(columns={'Horiz':'Horiz_muo'}, inplace=True)
    dfMuo['timestamp'] = pd.to_datetime(dfMuo['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfMuo.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_muo.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_muo.csv') <= 0:
            dfMuo.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_muo.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_muo.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfMuo.index > df1.index[-2]
                df1 = dfMuo[values]
                df1.to_csv('Magnetometer/data/magnetometer_muo.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX MUONIO
    dfMuo = pd.read_csv('Magnetometer/data/magnetometer_muo.csv', sep = " ")
    dfMuo = dfMuo.drop_duplicates(subset=['timestamp'])

    dfMuo['timestamp'] = pd.to_datetime(dfMuo['timestamp'])
    dfMuo.set_index('timestamp', inplace=True)

    length_muo = len(dfMuo.index)-1
    for i in range(length_muo):
        if (dfMuo.index[i+1]-dfMuo.index[i]).seconds >= 300:
            dfMuo.loc[dfMuo.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfMuo.sort_index(inplace=True)

    dfMuo_ai = dfMuo.resample('H')['Horiz_muo'].agg(['max', 'min'])
    dfMuo_ai['diff'] = dfMuo_ai['max'].sub(dfMuo_ai['min'], axis = 0)
    dfMuo_ai['diff'] = dfMuo_ai['diff'].shift(1)
    dfMuo_ai.to_csv('Magnetometer/data/ai/Muo.csv', sep = " ")
except:
    pass



#MAGNRTOMETER SODANYKYLA
try:
    url_sod = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=sod1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfSod = pd.read_csv(url_sod, skiprows = 7)

    dfSod = dfSod.astype(str)
    dfSod = dfSod[dfSod.columns[0]].str.split(expand=True)

    dfSod.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfSod['timestamp'] = dfSod['Date'] + ' ' + dfSod['Time']
    dfSod.drop(dfSod.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfSod = dfSod[dfSod.Horiz != '99999.9']
    dfSod.rename(columns={'Horiz':'Horiz_sod'}, inplace=True)
    dfSod['timestamp'] = pd.to_datetime(dfSod['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfSod.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_sod.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_sod.csv') <= 0:
            dfSod.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_sod.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_sod.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfSod.index > df1.index[-2]
                df1 = dfSod[values]
                df1.to_csv('Magnetometer/data/magnetometer_sod.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX SODANYKYLA
    dfSod = pd.read_csv('Magnetometer/data/magnetometer_sod.csv', sep = " ")
    dfSod = dfSod.drop_duplicates(subset=['timestamp'])

    dfSod['timestamp'] = pd.to_datetime(dfSod['timestamp'])
    dfSod.set_index('timestamp', inplace=True)

    length_sod = len(dfSod.index)-1
    for i in range(length_sod):
        if (dfSod.index[i+1]-dfSod.index[i]).seconds >= 300:
            dfSod.loc[dfSod.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfSod.sort_index(inplace=True)

    dfSod_ai = dfSod.resample('H')['Horiz_sod'].agg(['max', 'min'])
    dfSod_ai['diff'] = dfSod_ai['max'].sub(dfSod_ai['min'], axis = 0)
    dfSod_ai['diff'] = dfSod_ai['diff'].shift(1)
    dfSod_ai.to_csv('Magnetometer/data/ai/Sod.csv', sep = " ")
except:
    pass



#MAGNRTOMETER PELLO
try:
    url_pel = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=pel1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfPel = pd.read_csv(url_pel, skiprows = 7)

    dfPel = dfPel.astype(str)
    dfPel = dfPel[dfPel.columns[0]].str.split(expand=True)

    dfPel.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfPel['timestamp'] = dfPel['Date'] + ' ' + dfPel['Time']
    dfPel.drop(dfPel.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfPel = dfPel[dfPel.Horiz != '99999.9']
    dfPel.rename(columns={'Horiz':'Horiz_pel'}, inplace=True)
    dfPel['timestamp'] = pd.to_datetime(dfPel['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfPel.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_pel.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_pel.csv') <= 0:
            dfPel.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_pel.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_pel.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfPel.index > df1.index[-2]
                df1 = dfPel[values]
                df1.to_csv('Magnetometer/data/magnetometer_pel.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX PELLO
    dfPel = pd.read_csv('Magnetometer/data/magnetometer_pel.csv', sep = " ")
    dfPel = dfPel.drop_duplicates(subset=['timestamp'])

    dfPel['timestamp'] = pd.to_datetime(dfPel['timestamp'])
    dfPel.set_index('timestamp', inplace=True)

    length_pel = len(dfPel.index)-1
    for i in range(length_pel):
        if (dfPel.index[i+1]-dfPel.index[i]).seconds >= 300:
            dfPel.loc[dfPel.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfPel.sort_index(inplace=True)

    dfPel_ai = dfPel.resample('H')['Horiz_pel'].agg(['max', 'min'])
    dfPel_ai['diff'] = dfPel_ai['max'].sub(dfPel_ai['min'], axis = 0)
    dfPel_ai['diff'] = dfPel_ai['diff'].shift(1)
    dfPel_ai.to_csv('Magnetometer/data/ai/Pel.csv', sep = " ")
except:
    pass



#MAGNRTOMETER OULUJARVI
try:
    url_ouj = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=ouj1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfOuj = pd.read_csv(url_ouj, skiprows = 7)

    dfOuj = dfOuj.astype(str)
    dfOuj = dfOuj[dfOuj.columns[0]].str.split(expand=True)

    dfOuj.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfOuj['timestamp'] = dfOuj['Date'] + ' ' + dfOuj['Time']
    dfOuj.drop(dfOuj.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfOuj = dfOuj[dfOuj.Horiz != '99999.9']
    dfOuj.rename(columns={'Horiz':'Horiz_ouj'}, inplace=True)
    dfOuj['timestamp'] = pd.to_datetime(dfOuj['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfOuj.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_ouj.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_ouj.csv') <= 0:
            dfOuj.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_ouj.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_ouj.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfOuj.index > df1.index[-2]
                df1 = dfOuj[values]
                df1.to_csv('Magnetometer/data/magnetometer_ouj.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX OULUJARVI
    dfOuj = pd.read_csv('Magnetometer/data/magnetometer_ouj.csv', sep = " ")
    dfOuj = dfOuj.drop_duplicates(subset=['timestamp'])

    dfOuj['timestamp'] = pd.to_datetime(dfOuj['timestamp'])
    dfOuj.set_index('timestamp', inplace=True)

    length_ouj = len(dfOuj.index)-1
    for i in range(length_ouj):
        if (dfOuj.index[i+1]-dfOuj.index[i]).seconds >= 300:
            dfOuj.loc[dfOuj.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfOuj.sort_index(inplace=True)

    dfOuj_ai = dfOuj.resample('H')['Horiz_ouj'].agg(['max', 'min'])
    dfOuj_ai['diff'] = dfOuj_ai['max'].sub(dfOuj_ai['min'], axis = 0)
    dfOuj_ai['diff'] = dfOuj_ai['diff'].shift(1)
    dfOuj_ai.to_csv('Magnetometer/data/ai/Ouj.csv', sep = " ")
except:
    pass



#MAGNRTOMETER MEKRIJARVI
try:
    url_mek = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=mek1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfMek = pd.read_csv(url_mek, skiprows = 7)

    dfMek = dfMek.astype(str)
    dfMek = dfMek[dfMek.columns[0]].str.split(expand=True)

    dfMek.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfMek['timestamp'] = dfMek['Date'] + ' ' + dfMek['Time']
    dfMek.drop(dfMek.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfMek = dfMek[dfMek.Horiz != '99999.9']
    dfMek.rename(columns={'Horiz':'Horiz_mek'}, inplace=True)
    dfMek['timestamp'] = pd.to_datetime(dfMek['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfMek.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_mek.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_mek.csv') <= 0:
            dfMek.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_mek.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_mek.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfMek.index > df1.index[-2]
                df1 = dfMek[values]
                df1.to_csv('Magnetometer/data/magnetometer_mek.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX MEKRIJARVI
    dfMek = pd.read_csv('Magnetometer/data/magnetometer_mek.csv', sep = " ")
    dfMek = dfMek.drop_duplicates(subset=['timestamp'])

    dfMek['timestamp'] = pd.to_datetime(dfMek['timestamp'])
    dfMek.set_index('timestamp', inplace=True)

    length_mek = len(dfMek.index)-1
    for i in range(length_mek):
        if (dfMek.index[i+1]-dfMek.index[i]).seconds >= 300:
            dfMek.loc[dfMek.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfMek.sort_index(inplace=True)

    dfMek_ai = dfMek.resample('H')['Horiz_mek'].agg(['max', 'min'])
    dfMek_ai['diff'] = dfMek_ai['max'].sub(dfMek_ai['min'], axis = 0)
    dfMek_ai['diff'] = dfMek_ai['diff'].shift(1)
    dfMek_ai.to_csv('Magnetometer/data/ai/Mek.csv', sep = " ")
except:
    pass



#MAGNRTOMETER HANKASALMI
try:
    url_han = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=han1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfHan = pd.read_csv(url_han, skiprows = 7)

    dfHan = dfHan.astype(str)
    dfHan = dfHan[dfHan.columns[0]].str.split(expand=True)

    dfHan.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfHan['timestamp'] = dfHan['Date'] + ' ' + dfHan['Time']
    dfHan.drop(dfHan.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfHan = dfHan[dfHan.Horiz != '99999.9']
    dfHan.rename(columns={'Horiz':'Horiz_han'}, inplace=True)
    dfHan['timestamp'] = pd.to_datetime(dfHan['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfHan.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_han.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_han.csv') <= 0:
            dfHan.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_han.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_han.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfHan.index > df1.index[-2]
                df1 = dfHan[values]
                df1.to_csv('Magnetometer/data/magnetometer_han.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX HANKASALMI
    dfHan = pd.read_csv('Magnetometer/data/magnetometer_han.csv', sep = " ")
    dfHan = dfHan.drop_duplicates(subset=['timestamp'])

    dfHan['timestamp'] = pd.to_datetime(dfHan['timestamp'])
    dfHan.set_index('timestamp', inplace=True)

    length_han = len(dfHan.index)-1
    for i in range(length_han):
        if (dfHan.index[i+1]-dfHan.index[i]).seconds >= 300:
            dfHan.loc[dfHan.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfHan.sort_index(inplace=True)

    dfHan_ai = dfHan.resample('H')['Horiz_han'].agg(['max', 'min'])
    dfHan_ai['diff'] = dfHan_ai['max'].sub(dfHan_ai['min'], axis = 0)
    dfHan_ai['diff'] = dfHan_ai['diff'].shift(1)
    dfHan_ai.to_csv('Magnetometer/data/ai/Han.csv', sep = " ")
except:
    pass



#MAGNRTOMETER NURMIJARVI
try:
    url_nur = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=nur1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfNur = pd.read_csv(url_nur, skiprows = 7)

    dfNur = dfNur.astype(str)
    dfNur = dfNur[dfNur.columns[0]].str.split(expand=True)

    dfNur.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfNur['timestamp'] = dfNur['Date'] + ' ' + dfNur['Time']
    dfNur.drop(dfNur.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfNur = dfNur[dfNur.Horiz != '99999.9']
    dfNur.rename(columns={'Horiz':'Horiz_nur'}, inplace=True)
    dfNur['timestamp'] = pd.to_datetime(dfNur['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfNur.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_nur.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_nur.csv') <= 0:
            dfNur.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_nur.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_nur.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfNur.index > df1.index[-2]
                df1 = dfNur[values]
                df1.to_csv('Magnetometer/data/magnetometer_nur.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX NURMIJARVI
    dfNur = pd.read_csv('Magnetometer/data/magnetometer_nur.csv', sep = " ")
    dfNur = dfNur.drop_duplicates(subset=['timestamp'])

    dfNur['timestamp'] = pd.to_datetime(dfNur['timestamp'])
    dfNur.set_index('timestamp', inplace=True)

    length_nur = len(dfNur.index)-1
    for i in range(length_nur):
        if (dfNur.index[i+1]-dfNur.index[i]).seconds >= 300:
            dfNur.loc[dfNur.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfNur.sort_index(inplace=True)

    dfNur_ai = dfNur.resample('H')['Horiz_nur'].agg(['max', 'min'])
    dfNur_ai['diff'] = dfNur_ai['max'].sub(dfNur_ai['min'], axis = 0)
    dfNur_ai['diff'] = dfNur_ai['diff'].shift(1)
    dfNur_ai.to_csv('Magnetometer/data/ai/Nur.csv', sep = " ")
except:
    pass



#MAGNRTOMETER TARTU
try:
    url_tar = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=tar1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfTar = pd.read_csv(url_tar, skiprows = 7)

    dfTar = dfTar.astype(str)
    dfTar = dfTar[dfTar.columns[0]].str.split(expand=True)

    dfTar.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfTar['timestamp'] = dfTar['Date'] + ' ' + dfTar['Time']
    dfTar.drop(dfTar.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfTar = dfTar[dfTar.Horiz != '99999.9']
    dfTar.rename(columns={'Horiz':'Horiz_tar'}, inplace=True)
    dfTar['timestamp'] = pd.to_datetime(dfTar['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfTar.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_tar.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_tar.csv') <= 0:
            dfTar.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_tar.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_tar.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfTar.index > df1.index[-2]
                df1 = dfTar[values]
                df1.to_csv('Magnetometer/data/magnetometer_tar.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX TARTU
    dfTar = pd.read_csv('Magnetometer/data/magnetometer_tar.csv', sep = " ")
    dfTar = dfTar.drop_duplicates(subset=['timestamp'])

    dfTar['timestamp'] = pd.to_datetime(dfTar['timestamp'])
    dfTar.set_index('timestamp', inplace=True)

    length_tar = len(dfTar.index)-1
    for i in range(length_tar):
        if (dfTar.index[i+1]-dfTar.index[i]).seconds >= 300:
            dfTar.loc[dfTar.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfTar.sort_index(inplace=True)

    dfTar_ai = dfTar.resample('H')['Horiz_tar'].agg(['max', 'min'])
    dfTar_ai['diff'] = dfTar_ai['max'].sub(dfTar_ai['min'], axis = 0)
    dfTar_ai['diff'] = dfTar_ai['diff'].shift(1)
    dfTar_ai.to_csv('Magnetometer/data/ai/Tar.csv', sep = " ")
except:
    pass



#MAGNRTOMETER KEVO
try:
    url_kev = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=kev1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfKev = pd.read_csv(url_kev, skiprows = 7)

    dfKev = dfKev.astype(str)
    dfKev = dfKev[dfKev.columns[0]].str.split(expand=True)

    dfKev.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfKev['timestamp'] = dfKev['Date'] + ' ' + dfKev['Time']
    dfKev.drop(dfKev.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfKev = dfKev[dfKev.Horiz != '99999.9']
    dfKev.rename(columns={'Horiz':'Horiz_kev'}, inplace=True)
    dfKev['timestamp'] = pd.to_datetime(dfKev['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfKev.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_kev.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_kev.csv') <= 0:
            dfKev.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_kev.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_kev.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfKev.index > df1.index[-2]
                df1 = dfKev[values]
                df1.to_csv('Magnetometer/data/magnetometer_kev.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX KEVO
    dfKev = pd.read_csv('Magnetometer/data/magnetometer_kev.csv', sep = " ")
    dfKev = dfKev.drop_duplicates(subset=['timestamp'])

    dfKev['timestamp'] = pd.to_datetime(dfKev['timestamp'])
    dfKev.set_index('timestamp', inplace=True)

    length_kev = len(dfKev.index)-1
    for i in range(length_kev):
        if (dfKev.index[i+1]-dfKev.index[i]).seconds >= 300:
            dfKev.loc[dfKev.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfKev.sort_index(inplace=True)

    dfKev_ai = dfKev.resample('H')['Horiz_kev'].agg(['max', 'min'])
    dfKev_ai['diff'] = dfKev_ai['max'].sub(dfKev_ai['min'], axis = 0)
    dfKev_ai['diff'] = dfKev_ai['diff'].shift(1)
    dfKev_ai.to_csv('Magnetometer/data/ai/Kev.csv', sep = " ")
except:
    pass



#MAGNRTOMETER KILPISJARVI
try:
    url_kil = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=kil1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfKil = pd.read_csv(url_kil, skiprows = 7)

    dfKil = dfKil.astype(str)
    dfKil = dfKil[dfKil.columns[0]].str.split(expand=True)

    dfKil.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfKil['timestamp'] = dfKil['Date'] + ' ' + dfKil['Time']
    dfKil.drop(dfKil.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfKil = dfKil[dfKil.Horiz != '99999.9']
    dfKil.rename(columns={'Horiz':'Horiz_kil'}, inplace=True)
    dfKil['timestamp'] = pd.to_datetime(dfKil['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfKil.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_kil.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_kil.csv') <= 0:
            dfKil.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_kil.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_kil.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfKil.index > df1.index[-2]
                df1 = dfKil[values]
                df1.to_csv('Magnetometer/data/magnetometer_kil.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX KILPISJARVI
    dfKil = pd.read_csv('Magnetometer/data/magnetometer_kil.csv', sep = " ")
    dfKil = dfKil.drop_duplicates(subset=['timestamp'])

    dfKil['timestamp'] = pd.to_datetime(dfKil['timestamp'])
    dfKil.set_index('timestamp', inplace=True)

    length_kil = len(dfKil.index)-1
    for i in range(length_kil):
        if (dfKil.index[i+1]-dfKil.index[i]).seconds >= 300:
            dfKil.loc[dfKil.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfKil.sort_index(inplace=True)

    dfKil_ai = dfKil.resample('H')['Horiz_kil'].agg(['max', 'min'])
    dfKil_ai['diff'] = dfKil_ai['max'].sub(dfKil_ai['min'], axis = 0)
    dfKil_ai['diff'] = dfKil_ai['diff'].shift(1)
    dfKil_ai.to_csv('Magnetometer/data/ai/Kil.csv', sep = " ")
except:
    pass



#MAGNRTOMETER RANUA
try:
    url_ran = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=ran1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfRan = pd.read_csv(url_ran, skiprows = 7)

    dfRan = dfRan.astype(str)
    dfRan = dfRan[dfRan.columns[0]].str.split(expand=True)

    dfRan.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfRan['timestamp'] = dfRan['Date'] + ' ' + dfRan['Time']
    dfRan.drop(dfRan.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfRan = dfRan[dfRan.Horiz != '99999.9']
    dfRan.rename(columns={'Horiz':'Horiz_ran'}, inplace=True)
    dfRan['timestamp'] = pd.to_datetime(dfRan['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfRan.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_ran.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_ran.csv') <= 0:
            dfRan.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_ran.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_ran.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfRan.index > df1.index[-2]
                df1 = dfRan[values]
                df1.to_csv('Magnetometer/data/magnetometer_ran.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX RANUA
    dfRan = pd.read_csv('Magnetometer/data/magnetometer_ran.csv', sep = " ")
    dfRan = dfRan.drop_duplicates(subset=['timestamp'])

    dfRan['timestamp'] = pd.to_datetime(dfRan['timestamp'])
    dfRan.set_index('timestamp', inplace=True)

    length_ran = len(dfRan.index)-1
    for i in range(length_ran):
        if (dfRan.index[i+1]-dfRan.index[i]).seconds >= 300:
            dfRan.loc[dfRan.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfRan.sort_index(inplace=True)

    dfRan_ai = dfRan.resample('H')['Horiz_ran'].agg(['max', 'min'])
    dfRan_ai['diff'] = dfRan_ai['max'].sub(dfRan_ai['min'], axis = 0)
    dfRan_ai['diff'] = dfRan_ai['diff'].shift(1)
    dfRan_ai.to_csv('Magnetometer/data/ai/Ran.csv', sep = " ")
except:
    pass



#MAGNRTOMETER KIRUNA
try:
    url_kir = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=kir1a&year="+year+"&month="+month+"&day="+day+"&res=60sec&pwd=&format=html&comps=DHZ&getdata=+Get+Data+"
    dfKir = pd.read_csv(url_kir, skiprows = 7)

    dfKir = dfKir.astype(str)
    dfKir = dfKir[dfKir.columns[0]].str.split(expand=True)

    dfKir.columns = ['Date', 'Time', 'Dec', 'Horiz', 'Vert', 'Incl', 'Tot']
    dfKir['timestamp'] = dfKir['Date'] + ' ' + dfKir['Time']
    dfKir.drop(dfKir.columns.difference(['Horiz', 'timestamp']), 1, inplace=True)
    dfKir = dfKir[dfKir.Horiz != '99999.9']
    dfKir.rename(columns={'Horiz':'Horiz_kir'}, inplace=True)
    dfKir['timestamp'] = pd.to_datetime(dfKir['timestamp'], format = '%d/%m/%Y %H:%M:%S')
    dfKir.set_index('timestamp', inplace=True)


    with open('Magnetometer/data/magnetometer_kir.csv', 'a')as f:
        if os.path.getsize('Magnetometer/data/magnetometer_kir.csv') <= 0:
            dfKir.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Magnetometer/data/magnetometer_kir.csv') > 0:
            df1 = pd.read_csv('Magnetometer/data/magnetometer_kir.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfKir.index > df1.index[-2]
                df1 = dfKir[values]
                df1.to_csv('Magnetometer/data/magnetometer_kir.csv', mode='a', index =True, sep = " ", header = False)
    f.close()

    #ACTIVITY INDEX KIRUNA
    dfKir = pd.read_csv('Magnetometer/data/magnetometer_kir.csv', sep = " ")
    dfKir = dfKir.drop_duplicates(subset=['timestamp'])

    dfKir['timestamp'] = pd.to_datetime(dfKir['timestamp'])
    dfKir.set_index('timestamp', inplace=True)

    length_kir = len(dfKir.index)-1
    for i in range(length_kir):
        if (dfKir.index[i+1]-dfKir.index[i]).seconds >= 300:
            dfKir.loc[dfKir.index[i]+dtm.timedelta(minutes=5)] = float("nan")
    dfKir.sort_index(inplace=True)

    dfKir_ai = dfKir.resample('H')['Horiz_kir'].agg(['max', 'min'])
    dfKir_ai['diff'] = dfKir_ai['max'].sub(dfKir_ai['min'], axis = 0)
    dfKir_ai['diff'] = dfKir_ai['diff'].shift(1)
    dfKir_ai.to_csv('Magnetometer/data/ai/Kir.csv', sep = " ")
except:
    pass









'''Solar wind'''

#SOLAR WIND DENSITY AND SPEED
try:
    dfS = pd.read_json("https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json")

    dfS.drop([3], axis = 1, inplace = True)
    dfS.columns = [''] * len(dfS.columns)
    dfS = dfS.drop(dfS.index[0])
    dfS.columns = ['timestamp', 'Density', 'Speed']
    dfS['timestamp'] = pd.to_datetime(dfS['timestamp'], format = '%Y-%m-%d %H:%M:%S')
    dfS.set_index('timestamp', inplace=True)


    with open('Solar_wind/data/Speed_density.csv', 'a')as f:
        if os.path.getsize('Solar_wind/data/Speed_density.csv') <= 0:
            dfS.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Solar_wind/data/Speed_density.csv') > 0:
            df1 = pd.read_csv('Solar_wind/data/Speed_density.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfS.index > df1.index[-2]
                df1 = dfS[values]
                df1.to_csv('Solar_wind/data/Speed_density.csv', mode='a', index =True, sep = " ", header = False)
    f.close()
except:
    pass




#SOLAR WIND BX, BY, BZ
try:
    dfB = pd.read_json("https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json")
    
    dfB.drop([4, 5, 6], axis = 1, inplace = True)
    dfB.columns = [''] * len(dfB.columns)
    dfB = dfB.drop(dfB.index[0])
    dfB.columns = ['timestamp', 'Bx_gsm', 'By_gsm', 'Bz_gsm']
    dfB['timestamp'] = pd.to_datetime(dfB['timestamp'], format = '%Y-%m-%d %H:%M:%S')
    dfB.set_index('timestamp', inplace=True)
    
    
    with open('Solar_wind/data/Bx_by_bz.csv', 'a')as f:
        if os.path.getsize('Solar_wind/data/Bx_by_bz.csv') <= 0:
            dfB.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Solar_wind/data/Bx_by_bz.csv') > 0:
            df1 = pd.read_csv('Solar_wind/data/Bx_by_bz.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfB.index > df1.index[-2]
                df1 = dfB[values]
                df1.to_csv('Solar_wind/data/Bx_by_bz.csv', mode='a', index =True, sep = " ", header = False)
    f.close()
except:
    pass










'''Xrays and Protons'''

#X-RAYS
try:
    dfX = pd.read_json("https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json")
    
    dfX = dfX[dfX['energy'].str.contains("0.1-0.8nm")]
    dfX["timestamp"] = pd.to_datetime(dfX["time_tag"], format="%Y-%m-%dT%H:%M:%SZ")
    dfX.drop(dfX.columns.difference(['flux', 'timestamp']), 1, inplace=True)
    #dfX.drop(['time_tag', 'satellite', 'energy'], axis = 1, inplace = True)
    dfX.columns = ['X_rays', 'timestamp']
    dfX['X_rays'] =[float('{:.3g}'.format(x)) for x in dfX['X_rays']]
    dfX.set_index('timestamp', inplace=True)

    with open('Xrays_protons/data/Xrays.csv', 'a')as f:
        if os.path.getsize('Xrays_protons/data/Xrays.csv') <= 0:
            dfX.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Xrays_protons/data/Xrays.csv') > 0:
            df1 = pd.read_csv('Xrays_protons/data/Xrays.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfX.index > df1.index[-2]
                df1 = dfX[values]
                df1.to_csv('Xrays_protons/data/Xrays.csv', mode='a', index =True, sep = " ", header = False)
    f.close()
except:
    pass





#PROTONS
try:
    dfP = pd.read_json("https://services.swpc.noaa.gov/json/goes/primary/integral-protons-7-day.json")
    
    dfP = dfP[dfP['energy'].str.contains(">=10 MeV")]
    dfP["timestamp"] = pd.to_datetime(dfP["time_tag"], format="%Y-%m-%dT%H:%M:%SZ")
    dfP.drop(dfP.columns.difference(['flux', 'timestamp']), 1, inplace=True)
    dfP.columns = ['Protons', 'timestamp']
    dfP['Protons'] = dfP['Protons'].astype(float).round(2)
    dfP.set_index('timestamp', inplace=True)

    with open('Xrays_protons/data/Protons.csv', 'a')as f:
        if os.path.getsize('Xrays_protons/data/Protons.csv') <= 0:
            dfP.to_csv(f, header=f.tell()==0, index = True, sep = " ")
        elif os.path.getsize('Xrays_protons/data/Protons.csv') > 0:
            df1 = pd.read_csv('Xrays_protons/data/Protons.csv', sep = " ")
            df1['timestamp'] = pd.to_datetime(df1['timestamp'])
            df1.set_index('timestamp', inplace=True)
            if dtm.datetime.utcnow() > df1.index[-2]:
                values = dfP.index > df1.index[-2]
                df1 = dfP[values]
                df1.to_csv('Xrays_protons/data/Protons.csv', mode='a', index =True, sep = " ", header = False)
    f.close()
except:
    pass









''' KP '''

url = "ftp://ftp.gfz-potsdam.de/pub/home/obs/kp-nowcast-archive/wdc/kp"+year_kp+month+".wdc"
dfKp = pd.read_csv(url, header=None,  dtype=str)

dfKp = dfKp.astype(str)
dfKp.columns = ['data']

#creating columns using indexes
dfKp['year'] = dfKp['data'].str[:2]
dfKp['month'] = dfKp['data'].str.slice(2,4)
dfKp['day'] = dfKp['data'].str.slice(4,6)
dfKp['kp'] = dfKp['data'].str.slice(12,28)

dfKp['00:00-03:00'] = dfKp['kp'].str[:2]
dfKp['03:00-06:00'] = dfKp['kp'].str.slice(2,4)
dfKp['06:00-09:00'] = dfKp['kp'].str.slice(4,6)
dfKp['09:00-12:00'] = dfKp['kp'].str.slice(6,8)
dfKp['12:00-15:00'] = dfKp['kp'].str.slice(8,10)
dfKp['15:00-18:00'] = dfKp['kp'].str.slice(10,12)
dfKp['18:00-21:00'] = dfKp['kp'].str.slice(12,14)
dfKp['21:00-24:00'] = dfKp['kp'].str.slice(14,16)

dfKp.drop(['data', 'kp'], axis = 1, inplace = True)
dfKp.to_csv('Kp/data/kp.csv', index= True, sep= " ")







'''KP FORECAST'''

#using web crawling to extract data
url = "https://www.swpc.noaa.gov/products/3-day-geomagnetic-forecast"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')

test_item = soup.find_all('iframe')

data = requests.get(test_item[0]['src'])
soup2 = BeautifulSoup(data.content, 'lxml')

extracted_text = soup2.find('p')

text1 = extracted_text.text.split('NOAA')
text2 = StringIO(text1[-1])
df = pd.read_csv(text2, skiprows=1, sep='\t')


column_text = df.keys()[0].split()
column_names = [f'{column_text[(i*2)]}-{column_text[(i*2)+1]}' for i in range(3)]
df_mod = df[df.keys()[0]].str.split(expand=True)
df_mod.columns = ['time']+column_names


df_mod.to_csv('Kp/data/3_day_kp.csv', index=False, sep = " ")