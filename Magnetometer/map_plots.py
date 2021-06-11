import pandas as pd
import numpy as np
import datetime as dtm
from datetime import timezone, datetime
import plotly.express as px
import chart_studio
chart_studio.tools.set_credentials_file(username='', api_key='') #username and api key from plotly
#chart_studio.tools.set_config_file(world_readable=False, sharing='private')
import chart_studio.plotly as py
from chart_studio.plotly import plot, iplot
import plotly.graph_objs as go
from csv import reader
import os
import bs4
import plotly.offline


yr = dtm.datetime.utcnow().year
mo = dtm.datetime.utcnow().month
today =dtm.datetime.utcnow().day
time = dtm.datetime.utcnow()
hour = time.hour
minute = time.minute
date = dtm.datetime(year=yr, month=mo, day=today, hour=hour, minute=minute)
wk = date.isocalendar()[1]
end_range = time




#Delta H
#Reads deltaH data and extracts the most recent value


try:
    dfTro = pd.read_csv("data/ai/Tro.csv", sep=" ") #read data from csv
    dfTro.columns = ['timestamp_tro', 'max', 'min', 'Tromsø'] #give column names
    dfTro.drop(['max', 'min'], axis=1, inplace=True) #drop columns
    dfTro['timestamp_tro'] = pd.to_datetime(dfTro['timestamp_tro']) #convert column to datetime

    #calculating dH/dt
    dfTro['Tromsø_dH'] = abs(dfTro.Tromsø.diff()/10) #absolute value of row difference divided by 10

    dfTro = dfTro.tail(1)
except:
    pass



try:
    dfDob = pd.read_csv("data/ai/Dob.csv", sep=" ")
    dfDob.columns = ['timestamp_dob', 'max', 'min', 'Dombås']
    dfDob.drop(['max', 'min'], axis=1, inplace=True)
    dfDob['timestamp_dob'] = pd.to_datetime(dfDob['timestamp_dob'])

    #calculating dH/dt
    dfDob['Dombås_dH'] = abs(dfDob.Dombås.diff()/10)

    dfDob = dfDob.tail(1)
except:
    pass



try:
    dfSva = pd.read_csv("data/ai/Sva.csv", sep=" ")
    dfSva.columns = ['timestamp_sva', 'max', 'min', 'Svalbard']
    dfSva.drop(['max', 'min'], axis=1, inplace=True)
    dfSva['timestamp_sva'] = pd.to_datetime(dfSva['timestamp_sva'])

    #calculating dH/dt
    dfSva['Svalbard_dH'] = abs(dfSva.Svalbard.diff()/10)

    dfSva = dfSva.tail(1)
except:
    pass



try:
    dfNal = pd.read_csv("data/ai/Nal.csv", sep=" ")
    dfNal.columns = ['timestamp_nal', 'max', 'min', 'Ny_Ålesund']
    dfNal.drop(['max', 'min'], axis=1, inplace=True)
    dfNal['timestamp_nal'] = pd.to_datetime(dfNal['timestamp_nal'])

    #calculating dH/dt
    dfNal['Ny_Ålesund_dH'] = abs(dfNal.Ny_Ålesund.diff()/10)

    dfNal = dfNal.tail(1)
except:
    pass



try:
    dfAnd = pd.read_csv("data/ai/And.csv", sep=" ")
    dfAnd.columns = ['timestamp_and', 'max', 'min', 'Andenes']
    dfAnd.drop(['max', 'min'], axis=1, inplace=True)
    dfAnd['timestamp_and'] = pd.to_datetime(dfAnd['timestamp_and'])

    #calculating dH/dt
    dfAnd['Andenes_dH'] = abs(dfAnd.Andenes.diff()/10)

    dfAnd = dfAnd.tail(1)
except:
    pass



try:
    dfHop = pd.read_csv("data/ai/Hop.csv", sep=" ")
    dfHop.columns = ['timestamp_hop', 'max', 'min', 'Hopen']
    dfHop.drop(['max', 'min'], axis=1, inplace=True)
    dfHop['timestamp_hop'] = pd.to_datetime(dfHop['timestamp_hop'])

    #calculating dH/dt
    dfHop['Hopen_dH'] = abs(dfHop.Hopen.diff()/10)

    dfHop = dfHop.tail(1)
except:
    pass



try:
    dfBjn = pd.read_csv("data/ai/Bjn.csv", sep=" ")
    dfBjn.columns = ['timestamp_bjn', 'max', 'min', 'Bjørnøya']
    dfBjn.drop(['max', 'min'], axis=1, inplace=True)
    dfBjn['timestamp_bjn'] = pd.to_datetime(dfBjn['timestamp_bjn'])

    #calculating dH/dt
    dfBjn['Bjørnøya_dH'] = abs(dfBjn.Bjørnøya.diff()/10)

    dfBjn = dfBjn.tail(1)
except:
    pass



try:
    dfNor = pd.read_csv("data/ai/Nor.csv", sep=" ")
    dfNor.columns = ['timestamp_nor', 'max', 'min', 'Nordkapp']
    dfNor.drop(['max', 'min'], axis=1, inplace=True)
    dfNor['timestamp_nor'] = pd.to_datetime(dfNor['timestamp_nor'])

    #calculating dH/dt
    dfNor['Nordkapp_dH'] = abs(dfNor.Nordkapp.diff()/10)

    dfNor = dfNor.tail(1)
except:
    pass



try:
    dfSor = pd.read_csv("data/ai/Sor.csv", sep=" ")
    dfSor.columns = ['timestamp_sor', 'max', 'min', 'Sørøya']
    dfSor.drop(['max', 'min'], axis=1, inplace=True)
    dfSor['timestamp_nor'] = pd.to_datetime(dfSor['timestamp_sor'])

    #calculating dH/dt
    dfSor['Sørøya_dH'] = abs(dfSor.Sørøya.diff()/10)

    dfSor = dfSor.tail(1)
except:
    pass



try:
    dfDon = pd.read_csv("data/ai/Don.csv", sep=" ")
    dfDon.columns = ['timestamp_don', 'max', 'min', 'Dønna']
    dfDon.drop(['max', 'min'], axis=1, inplace=True)
    dfDon['timestamp_don'] = pd.to_datetime(dfDon['timestamp_don'])

    #calculating dH/dt
    dfDon['Dønna_dH'] = abs(dfDon.Dønna.diff()/10)

    dfDon = dfDon.tail(1)
except:
    pass



try:
    dfJck = pd.read_csv("data/ai/Jck.csv", sep=" ")
    dfJck.columns = ['timestamp_jck', 'max', 'min', 'Jackvick']
    dfJck.drop(['max', 'min'], axis=1, inplace=True)
    dfJck['timestamp_jck'] = pd.to_datetime(dfJck['timestamp_jck'])

    #calculating dH/dt
    dfJck['Jackvick_dH'] = abs(dfJck.Jackvick.diff()/10)

    dfJck = dfJck.tail(1)
except:
    pass


try:
    dfRvk = pd.read_csv("data/ai/Rvk.csv", sep=" ")
    dfRvk.columns = ['timestamp_rvk', 'max', 'min', 'Rørvik']
    dfRvk.drop(['max', 'min'], axis=1, inplace=True)
    dfRvk['timestamp_rvk'] = pd.to_datetime(dfRvk['timestamp_rvk'])

    #calculating dH/dt
    dfRvk['Rørvik_dH'] = abs(dfRvk.Rørvik.diff()/10)

    dfRvk = dfRvk.tail(1)
except:
    pass



try:
    dfSol = pd.read_csv("data/ai/Sol.csv", sep=" ")
    dfSol.columns = ['timestamp_sol', 'max', 'min', 'Solund']
    dfSol.drop(['max', 'min'], axis=1, inplace=True)
    dfSol['timestamp_sol'] = pd.to_datetime(dfSol['timestamp_sol'])

    #calculating dH/dt
    dfSol['Solund_dH'] = abs(dfSol.Solund.diff()/10)

    dfSol = dfSol.tail(1)
except:
    pass



try:
    dfKar = pd.read_csv("data/ai/Kar.csv", sep=" ")
    dfKar.columns = ['timestamp_kar', 'max', 'min', 'Karmøy']
    dfKar.drop(['max', 'min'], axis=1, inplace=True)
    dfKar['timestamp_kar'] = pd.to_datetime(dfKar['timestamp_kar'])

    #calculating dH/dt
    dfKar['Karmøy_dH'] = abs(dfKar.Karmøy.diff()/10)

    dfKar = dfKar.tail(1)
except:
    pass



try:
    dfJan = pd.read_csv("data/ai/Jan.csv", sep=" ")
    dfJan.columns = ['timestamp_jan', 'max', 'min', 'Jan_Mayen']
    dfJan.drop(['max', 'min'], axis=1, inplace=True)
    dfJan['timestamp_jan'] = pd.to_datetime(dfJan['timestamp_jan'])

    #calculating dH/dt
    dfJan['Jan_Mayen_dH'] = abs(dfJan.Jan_Mayen.diff()/10)

    dfJan = dfJan.tail(1)
except:
    pass



try:
    dfMas = pd.read_csv("data/ai/Mas.csv", sep=" ")
    dfMas.columns = ['timestamp_mas', 'max', 'min', 'Masi']
    dfMas.drop(['max', 'min'], axis=1, inplace=True)
    dfMas['timestamp_mas'] = pd.to_datetime(dfMas['timestamp_mas'])

    #calculating dH/dt
    dfMas['Masi_dH'] = abs(dfMas.Masi.diff()/10)

    dfMas = dfMas.tail(1)
except:
    pass



try:
    dfRst = pd.read_csv("data/ai/Rst.csv", sep=" ")
    dfRst.columns = ['timestamp_rst', 'max', 'min', 'Røst']
    dfRst.drop(['max', 'min'], axis=1, inplace=True)
    dfRst['timestamp_rst'] = pd.to_datetime(dfRst['timestamp_rst'])

    #calculating dH/dt
    dfRst['Røst_dH'] = abs(dfRst.Røst.diff()/10)

    dfRst = dfRst.tail(1)
except:
    pass



try:
    dfHar = pd.read_csv("data/ai/Har.csv", sep=" ")
    dfHar.columns = ['timestamp_har', 'max', 'min', 'Harestua']
    dfHar.drop(['max', 'min'], axis=1, inplace=True)
    dfHar['timestamp_har'] = pd.to_datetime(dfHar['timestamp_har'])

    #calculating dH/dt
    dfHar['Harestua_dH'] = abs(dfHar.Harestua.diff()/10)

    dfHar = dfHar.tail(1)
except:
    pass



try:
    dfIva = pd.read_csv("data/ai/Iva.csv", sep=" ")
    dfIva.columns = ['timestamp_iva', 'max', 'min', 'Ivalo']
    dfIva.drop(['max', 'min'], axis=1, inplace=True)
    dfIva['timestamp_iva'] = pd.to_datetime(dfIva['timestamp_iva'])

    #calculating dH/dt
    dfIva['Ivalo_dH'] = abs(dfIva.Ivalo.diff()/10)

    dfIva = dfIva.tail(1)
except:
    pass



try:
    dfMuo = pd.read_csv("data/ai/Muo.csv", sep=" ")
    dfMuo.columns = ['timestamp_muo', 'max', 'min', 'Muonio']
    dfMuo.drop(['max', 'min'], axis=1, inplace=True)
    dfMuo['timestamp_muo'] = pd.to_datetime(dfMuo['timestamp_muo'])

    #calculating dH/dt
    dfMuo['Muonio_dH'] = abs(dfMuo.Muonio.diff()/10)

    dfMuo = dfMuo.tail(1)
except:
    pass



try:
    dfSod = pd.read_csv("data/ai/Sod.csv", sep=" ")
    dfSod.columns = ['timestamp_sod', 'max', 'min', 'Sodankyla']
    dfSod.drop(['max', 'min'], axis=1, inplace=True)
    dfSod['timestamp_sod'] = pd.to_datetime(dfSod['timestamp_sod'])

    #calculating dH/dt
    dfSod['Sodankyla_dH'] = abs(dfSod.Sodankyla.diff()/10)

    dfSod = dfSod.tail(1)
except:
    pass



try:
    dfPel = pd.read_csv("data/ai/Pel.csv", sep=" ")
    dfPel.columns = ['timestamp_pel', 'max', 'min', 'Pello']
    dfPel.drop(['max', 'min'], axis=1, inplace=True)
    dfPel['timestamp_pel'] = pd.to_datetime(dfPel['timestamp_pel'])

    #calculating dH/dt
    dfPel['Pello_dH'] = abs(dfPel.Pello.diff()/10)

    dfPel = dfPel.tail(1)
except:
    pass



try:
    dfOuj = pd.read_csv("data/ai/Ouj.csv", sep=" ")
    dfOuj.columns = ['timestamp_ouj', 'max', 'min', 'Oulujarvi']
    dfOuj.drop(['max', 'min'], axis=1, inplace=True)
    dfOuj['timestamp_ouj'] = pd.to_datetime(dfOuj['timestamp_ouj'])

    #calculating dH/dt
    dfOuj['Oulujarvi_dH'] = abs(dfOuj.Oulujarvi.diff()/10)

    dfOuj = dfOuj.tail(1)
except:
    pass



try:
    dfMek = pd.read_csv("data/ai/Mek.csv", sep=" ")
    dfMek.columns = ['timestamp_mek', 'max', 'min', 'Mekrijarvi']
    dfMek.drop(['max', 'min'], axis=1, inplace=True)
    dfMek['timestamp_mek'] = pd.to_datetime(dfMek['timestamp_mek'])

    #calculating dH/dt
    dfMek['Mekrijarvi_dH'] = abs(dfMek.Mekrijarvi.diff()/10)

    dfMek = dfMek.tail(1)
except:
    pass



try:
    dfHan = pd.read_csv("data/ai/Han.csv", sep=" ")
    dfHan.columns = ['timestamp_han', 'max', 'min', 'Hankasalmi']
    dfHan.drop(['max', 'min'], axis=1, inplace=True)
    dfHan['timestamp_han'] = pd.to_datetime(dfHan['timestamp_han'])

    #calculating dH/dt
    dfHan['Hankasalmi_dH'] = abs(dfHan.Hankasalmi.diff()/10)

    dfHan = dfHan.tail(1)
except:
    pass



try:
    dfNur = pd.read_csv("data/ai/Nur.csv", sep=" ")
    dfNur.columns = ['timestamp_nur', 'max', 'min', 'Nurmijarvi']
    dfNur.drop(['max', 'min'], axis=1, inplace=True)
    dfNur['timestamp_nur'] = pd.to_datetime(dfNur['timestamp_nur'])

    #calculating dH/dt
    dfNur['Nurmijarvi_dH'] = abs(dfNur.Nurmijarvi.diff()/10)

    dfNur = dfNur.tail(1)
except:
    pass



try:
    dfTar = pd.read_csv("data/ai/Tar.csv", sep=" ")
    dfTar.columns = ['timestamp_tar', 'max', 'min', 'Tartu']
    dfTar.drop(['max', 'min'], axis=1, inplace=True)
    dfTar['timestamp_tar'] = pd.to_datetime(dfTar['timestamp_tar'])

    #calculating dH/dt
    dfTar['Tartu_dH'] = abs(dfTar.Tartu.diff()/10)

    dfTar = dfTar.tail(1)
except:
    pass



try:
    dfKev = pd.read_csv("data/ai/Kev.csv", sep=" ")
    dfKev.columns = ['timestamp_pel', 'max', 'min', 'Kevo']
    dfKev.drop(['max', 'min'], axis=1, inplace=True)
    dfKev['timestamp_pel'] = pd.to_datetime(dfKev['timestamp_pel'])

    #calculating dH/dt
    dfKev['Kevo_dH'] = abs(dfKev.Kevo.diff()/10)

    dfKev = dfKev.tail(1)
except:
    pass



try:
    dfKil = pd.read_csv("data/ai/Kil.csv", sep=" ")
    dfKil.columns = ['timestamp_kil', 'max', 'min', 'Kilpisjarvi']
    dfKil.drop(['max', 'min'], axis=1, inplace=True)
    dfKil['timestamp_kil'] = pd.to_datetime(dfKil['timestamp_kil'])

    #calculating dH/dt
    dfKil['Kilpisjarvi_dH'] = abs(dfKil.Kilpisjarvi.diff()/10)

    dfKil = dfKil.tail(1)
except:
    pass



try:
    dfRan = pd.read_csv("data/ai/Ran.csv", sep=" ")
    dfRan.columns = ['timestamp_ran', 'max', 'min', 'Ranua']
    dfRan.drop(['max', 'min'], axis=1, inplace=True)
    dfRan['timestamp_ran'] = pd.to_datetime(dfRan['timestamp_ran'])

    #calculating dH/dt
    dfRan['Ranua_dH'] = abs(dfRan.Ranua.diff()/10)

    dfRan = dfRan.tail(1)
except:
    pass



try:
    dfKir = pd.read_csv("data/ai/Kir.csv", sep=" ")
    dfKir.columns = ['timestamp_kir', 'max', 'min', 'Kiruna']
    dfKir.drop(['max', 'min'], axis=1, inplace=True)
    dfKir['timestamp_kir'] = pd.to_datetime(dfKir['timestamp_kir'])

    #calculating dH/dt
    dfKir['Kiruna_dH'] = abs(dfKir.Kiruna.diff()/10)

    dfKir = dfKir.tail(1)
except:
    pass




#Get the calculated activity indices for each station in variables
deltaHTro = dfTro.iloc[0]['Tromsø']
deltaHDob = dfDob.iloc[0]['Dombås']
deltaHSva = dfSva.iloc[0]['Svalbard']
deltaHNal = dfNal.iloc[0]['Ny_Ålesund']
deltaHAnd = dfAnd.iloc[0]['Andenes']
deltaHHop = dfHop.iloc[0]['Hopen']
deltaHBjn = dfBjn.iloc[0]['Bjørnøya']
deltaHNor = dfNor.iloc[0]['Nordkapp']
deltaHSor = dfSor.iloc[0]['Sørøya']
deltaHDon = dfDon.iloc[0]['Dønna']
deltaHJck = dfJck.iloc[0]['Jackvick']
deltaHRvk = dfRvk.iloc[0]['Rørvik']
deltaHSol = dfSol.iloc[0]['Solund']
deltaHKar = dfKar.iloc[0]['Karmøy']
deltaHJan = dfJan.iloc[0]['Jan_Mayen']
deltaHMas = dfMas.iloc[0]['Masi']
deltaHRst = dfRst.iloc[0]['Røst']
deltaHHar = dfHar.iloc[0]['Harestua']
deltaHIva = dfIva.iloc[0]['Ivalo']
deltaHMuo = dfMuo.iloc[0]['Muonio']
deltaHSod = dfSod.iloc[0]['Sodankyla']
deltaHPel = dfPel.iloc[0]['Pello']
deltaHOuj = dfOuj.iloc[0]['Oulujarvi']
deltaHMek = dfMek.iloc[0]['Mekrijarvi']
deltaHHan = dfHan.iloc[0]['Hankasalmi']
deltaHNur = dfNur.iloc[0]['Nurmijarvi']
deltaHTar = dfTar.iloc[0]['Tartu']
deltaHKev = dfKev.iloc[0]['Kevo']
deltaHKil = dfKil.iloc[0]['Kilpisjarvi']
deltaHRan = dfRan.iloc[0]['Ranua']
deltaHKir = dfKir.iloc[0]['Kiruna']




#Get the calculated dH/dt indices for each station in variables
dHTro = dfTro.iloc[0]['Tromsø_dH']
dHDob = dfDob.iloc[0]['Dombås_dH']
dHSva = dfSva.iloc[0]['Svalbard_dH']
dHNal = dfNal.iloc[0]['Ny_Ålesund_dH']
dHAnd = dfAnd.iloc[0]['Andenes_dH']
dHHop = dfHop.iloc[0]['Hopen_dH']
dHBjn = dfBjn.iloc[0]['Bjørnøya_dH']
dHNor = dfNor.iloc[0]['Nordkapp_dH']
dHSor = dfSor.iloc[0]['Sørøya_dH']
dHDon = dfDon.iloc[0]['Dønna_dH']
dHJck = dfJck.iloc[0]['Jackvick_dH']
dHRvk = dfRvk.iloc[0]['Rørvik_dH']
dHSol = dfSol.iloc[0]['Solund_dH']
dHKar = dfKar.iloc[0]['Karmøy_dH']
dHJan = dfJan.iloc[0]['Jan_Mayen_dH']
dHMas = dfMas.iloc[0]['Masi_dH']
dHRst = dfRst.iloc[0]['Røst_dH']
dHHar = dfHar.iloc[0]['Harestua_dH']
dHIva = dfIva.iloc[0]['Ivalo_dH']
dHMuo = dfMuo.iloc[0]['Muonio_dH']
dHSod = dfSod.iloc[0]['Sodankyla_dH']
dHPel = dfPel.iloc[0]['Pello_dH']
dHOuj = dfOuj.iloc[0]['Oulujarvi_dH']
dHMek = dfMek.iloc[0]['Mekrijarvi_dH']
dHHan = dfHan.iloc[0]['Hankasalmi_dH']
dHNur = dfNur.iloc[0]['Nurmijarvi_dH']
dHTar = dfTar.iloc[0]['Tartu_dH']
dHKev = dfKev.iloc[0]['Kevo_dH']
dHKil = dfKil.iloc[0]['Kilpisjarvi_dH']
dHRan = dfRan.iloc[0]['Ranua_dH']
dHKir = dfKir.iloc[0]['Kiruna_dH']




#Extracts the station names
deltaHTro_name = dfTro.columns[1]
deltaHDob_name = dfDob.columns[1]
deltaHSva_name = dfSva.columns[1]
deltaHNal_name = dfNal.columns[1]
deltaHAnd_name = dfAnd.columns[1]
deltaHHop_name = dfHop.columns[1]
deltaHBjn_name = dfBjn.columns[1]
deltaHNor_name = dfNor.columns[1]
deltaHSor_name = dfSor.columns[1]
deltaHDon_name = dfDon.columns[1]
deltaHJck_name = dfJck.columns[1]
deltaHRvk_name = dfRvk.columns[1]
deltaHSol_name = dfSol.columns[1]
deltaHKar_name = dfKar.columns[1]
deltaHJan_name = dfJan.columns[1]
deltaHMas_name = dfMas.columns[1]
deltaHRst_name = dfRst.columns[1]
deltaHHar_name = dfHar.columns[1]
deltaHIva_name = dfIva.columns[1]
deltaHMuo_name = dfMuo.columns[1]
deltaHSod_name = dfSod.columns[1]
deltaHPel_name = dfPel.columns[1]
deltaHOuj_name = dfOuj.columns[1]
deltaHMek_name = dfMek.columns[1]
deltaHHan_name = dfHan.columns[1]
deltaHNur_name = dfNur.columns[1]
deltaHTar_name = dfTar.columns[1]
deltaHKev_name = dfKev.columns[1]
deltaHKil_name = dfKil.columns[1]
deltaHRan_name = dfRan.columns[1]
deltaHKir_name = dfKir.columns[1]



#Make a dataframe with column names and deltaH values

deltaH_dH = pd.DataFrame()

deltaH_dH['Lat'] = [69.6617, 62.07, 78.2, 78.92, 69.2953, 76.51, 74.5039, 71.0917, 70.5414, 66.11, 66.4000, 64.9469, 61.08, 59.21, 70.9000,
                 69.46, 67.5300, 60.21, 68.56, 68.02, 67.37, 66.90, 64.52, 62.77, 62.25, 60.50, 58.26, 69.76, 69.02, 65.54, 67.83]

deltaH_dH['Lon'] = [18.94, 9.11, 15.83, 11.93, 16.0381, 25.01, 19.0014, 25.7856, 22.2247, 12.50, 16.9833, 10.9872, 4.84, 5.24, -8.7000,
                 23.70, 12.0986, 10.75, 27.29, 23.53, 26.63, 24.08, 27.23, 30.97, 26.60, 24.65, 26.46, 27.01, 20.79, 26.25, 20.42]

deltaH_dH['stations'] = [deltaHTro_name, deltaHDob_name, deltaHSva_name, deltaHNal_name, deltaHAnd_name, deltaHHop_name, deltaHBjn_name, deltaHNor_name, deltaHSor_name, 
                      deltaHDon_name, deltaHJck_name, deltaHRvk_name, deltaHSol_name, deltaHKar_name, deltaHJan_name, deltaHMas_name, deltaHRst_name, deltaHHar_name, 
                      deltaHIva_name, deltaHMuo_name, deltaHSod_name, deltaHPel_name, deltaHOuj_name, deltaHMek_name, deltaHHan_name, deltaHNur_name, deltaHTar_name, 
                      deltaHKev_name, deltaHKil_name, deltaHRan_name, deltaHKir_name]

deltaH_dH['deltaH'] = [deltaHTro, deltaHDob, deltaHSva, deltaHNal, deltaHAnd, deltaHHop, deltaHBjn, deltaHNor, deltaHSor, deltaHDon, deltaHJck, deltaHRvk, deltaHSol, 
                    deltaHKar, deltaHJan, deltaHMas, deltaHRst, deltaHHar, deltaHIva, deltaHMuo, deltaHSod, deltaHPel, deltaHOuj, deltaHMek, deltaHHan, deltaHNur, 
                    deltaHTar, deltaHKev, deltaHKil, deltaHRan, deltaHKir]

deltaH_dH['dH/dt'] = [dHTro, dHDob, dHSva, dHNal, dHAnd, dHHop, dHBjn, dHNor, dHSor, dHDon, dHJck, dHRvk, dHSol, 
                    dHKar, dHJan, dHMas, dHRst, dHHar, dHIva, dHMuo, dHSod, dHPel, dHOuj, dHMek, dHHan, dHNur, 
                    dHTar, dHKev, dHKil, dHRan, dHKir]

deltaH_dH['deltaH'] = deltaH_dH['deltaH'].astype(float).round(2).abs()
deltaH_dH['dH/dt'] = deltaH_dH['dH/dt'].astype(float).round(2).abs()

deltaH_dH = deltaH_dH.replace(np.nan, '0', regex=True)
deltaH_dH[["deltaH", "dH/dt"]] = deltaH_dH[["deltaH", "dH/dt"]].apply(pd.to_numeric)




#DeltaH Plot
mapbox_access_token = "" #map box token from plotly

fig = px.scatter_mapbox(deltaH_dH,
    lat='Lat',
    lon='Lon',
    color='deltaH',
    size='deltaH',
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=15, zoom=2.5, opacity=0.8,
    hover_data={'Lon':False},
    hover_name='stations',   
)
fig.update_layout(
    autosize=False,
    width=1000,
    height=950,
    title={
        'text': "Ground disturbance deltaH",
        'y':0.97,
        'x':0.536,
        'font_family': 'Balto',
        'font_size': 28,
        'xanchor': 'center',
        'yanchor': 'top'},
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=70.6,
            lon=15.8
        ),
        pitch=0,
        zoom=3.1
    ),
)
fig.write_html('plots/deltaH.html', auto_open=False)


dir = os.path.dirname(os.path.realpath(__file__))
filename = 'plots/deltaH.html'
htmldir = os.path.join(dir, filename)

htmltext = plotly.offline.plot(fig, include_plotlyjs=True,
                               auto_open=False,
                               filename = htmldir)
with open(htmldir) as inf:
    txt = inf.read()
    soup = bs4.BeautifulSoup(txt, features="lxml")

initialStyle = soup.div.div['style']

soup.div.div['style'] = initialStyle+ "position:absolute; left:50%; transform:translate(-50%);"
with open(htmldir, "w") as outf:
    outf.write(str(soup))

py.plot(fig, filename = 'deltaH.html', auto_open=False, sharing='public')







#dH/dt Plot

fig = px.scatter_mapbox(deltaH_dH,
    lat='Lat',
    lon='Lon',
    color='dH/dt',
    size='dH/dt',
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=15, zoom=2.5, opacity=0.8,
    hover_data={'Lon':False},
    hover_name='stations',   
)
fig.update_layout(
    autosize=False,
    width=1000,
    height=950,
    title={
        'text': "Ground disturbance dH/dt",
        'y':0.97,
        'x':0.536,
        'font_family': 'Balto',
        'font_size': 28,
        'xanchor': 'center',
        'yanchor': 'top'},
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=70.6,
            lon=15.8
        ),
        pitch=0,
        zoom=3.1
    ),
)
#fig.write_html('plots/dH_dt.html', auto_open=False)

dir = os.path.dirname(os.path.realpath(__file__))
filename = 'plots/dH_dt.html'
htmldir = os.path.join(dir, filename)

htmltext = plotly.offline.plot(fig, include_plotlyjs=True,
                               auto_open=False,
                               filename = htmldir)
with open(htmldir) as inf:
    txt = inf.read()
    soup = bs4.BeautifulSoup(txt, features="lxml")

initialStyle = soup.div.div['style']

soup.div.div['style'] = initialStyle+ "position:absolute; left:50%; transform:translate(-50%);"
with open(htmldir, "w") as outf:
    outf.write(str(soup))

py.plot(fig, filename = 'dH_dt.html', auto_open=False, sharing='public')






#Tromsø Hcom and deltaH

