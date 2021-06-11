#pylint: disable=all
#pylint: disable=no-member
from numpy.core.fromnumeric import size
import pandas as pd
import numpy as np
from pandas import read_csv
import datetime as dtm
from datetime import timezone, datetime
import os
import sys 
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly import subplots

date = dtm.datetime.utcnow()
timestampStr = date.strftime("%d-%b-%Y (%H:%M:%S)")

#today = dtm.date.today()
today = dtm.datetime.utcnow().date()
tomorroww = today + dtm.timedelta(days=1)
tomorrow = tomorroww.strftime('%d-%b-%Y')
two_dayss = today + dtm.timedelta(days=2)
two_days = two_dayss.strftime('%d-%b-%Y')
three_dayss = today + dtm.timedelta(days=3)
three_days = three_dayss.strftime('%d-%b-%Y')
two_dayss_ago = today - dtm.timedelta(days=2)
two_days_ago = two_dayss_ago.strftime('%d-%b-%Y')
yesterday = today - dtm.timedelta(days=1)
yesterday = yesterday.strftime('%d-%b-%Y')
today = today.strftime('%d-%b-%Y')

dfKp = pd.read_csv("data/kp.csv", sep=" ", index_col=False) #read data from csv
dfKp = dfKp.astype(str) #convert data to string


#axes for plotting
y_start = 0
y_end = 9.0

x_start = -0.6
x_end = 7.65

if dfKp.columns.str.len().all() < 2:
    dfKp['month'] = dfKp['month'].str.zfill(2) #add zero to the front of all one digit numbers
    dfKp['day'] = dfKp['day'].str.zfill(2)
    dfKp['00:00-03:00'] = dfKp['00:00-03:00'].str.zfill(2)
    dfKp['03:00-06:00'] = dfKp['03:00-06:00'].str.zfill(2)
    dfKp['06:00-09:00'] = dfKp['06:00-09:00'].str.zfill(2)
    dfKp['09:00-12:00'] = dfKp['09:00-12:00'].str.zfill(2)
    dfKp['12:00-15:00'] = dfKp['12:00-15:00'].str.zfill(2)
    dfKp['15:00-18:00'] = dfKp['15:00-18:00'].str.zfill(2)
    dfKp['18:00-21:00'] = dfKp['18:00-21:00'].str.zfill(2)
    dfKp['21:00-24:00'] = dfKp['21:00-24:00'].str.zfill(2)


dfKp["date"] = pd.to_datetime(
    dfKp["year"].astype(str) + "-" + dfKp["month"].astype(str) + "-" + dfKp["day"].astype(str),format="%y-%m-%d") #create column by merging other columns and converting it to datetime

dfKp.drop(['Unnamed: 0', 'year', 'month', 'day'], axis = 1, inplace = True)
dfKp.set_index('date', inplace=True)

for c in dfKp:
    dfKp[c] = (dfKp[c].str[:1] + '.' + dfKp[c].str[1:]).astype(float) #add '.' between numbers

dfKp = dfKp.astype(str)
#dfKp = dfKp.replace('9.9', np.nan, regex=True)
dfKp = dfKp.replace('9.9', '0', regex=True) 






#create interctive plots with plotly
#realtime
df_realtime = dfKp.tail(1)
df_realtime = df_realtime.astype(float)

df_realtime_T = df_realtime.T #transpose the dataframe (from df_realtime to df_realtime_T)

df_realtime_T.columns = ['Kp']
values = df_realtime_T.Kp #values for plotting
x = [0, 1, 2, 3, 4, 5, 6, 7]

def BarColor(vals): #function to change bar colors at specific values
    x = vals
    if x <= 3:
        return "Green"
    if x > 3 and x <= 7:
        return "Yellow"
    if x > 7 and x <= 9:
        return "Red"


data = [go.Bar(
   x = x,
   y = values.values,
   hovertext = ["KP: {}".format(x) for x in values], #custom  hover information
   hoverinfo = "text",
   name = 'KP'
)]

values = pd.DataFrame(values)
fig = go.Figure(data=data)

fig.update_xaxes(showline=True, linewidth=2, mirror=True, linecolor='Black', showgrid=False, gridwidth=2, gridcolor='#DCDCDC') #custom axis
fig.update_yaxes(showline=True, linewidth=2, mirror=True, linecolor='Black', showgrid=False, gridwidth=2, gridcolor='#DCDCDC')

#custom plot layout
fig.update_layout(
    autosize=False,
    width=1400,
    height=700,
    margin=dict(
        l=150,
        r=50,
        b=100,
        t=100,
    ),
    showlegend=False,
    template='plotly_white',
    hovermode='closest',
    title={
        'text': "Planetary K-index",
        'y':0.9,
        'x':0.536,
        'font_family': 'Balto',
        'font_size': 28,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis = dict(
        tickmode = 'array',
        zeroline = False,
        range=[x_start,x_end],
        tickvals = [-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5],
        ticktext = ['0','3','6','9','12','15','18','21','24'],
        ticks="inside",
        ticklen=10,
        title=timestampStr + " UTC",
        title_font_size = 18,
    ),
    yaxis = dict(
        ticks='outside',
        range=[y_start,y_end],
        ticktext = ['0','1','2','3','4','5','6','7','8','9'],
        title='Kp index',
        title_font_size = 18,
    ),
    hoverlabel=dict(bgcolor='oldlace',
                    font=dict(family='Balto',
                    size=28,
                    color='black')),
)
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=1,
            x1=7.8,
            y1=1,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=2,
            x1=7.8,
            y1=2,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=3,
            x1=7.8,
            y1=3,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=4,
            x1=7.8,
            y1=4,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=5,
            x1=7.8,
            y1=5,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=6,
            x1=7.8,
            y1=6,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=7,
            x1=7.8,
            y1=7,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=8,
            x1=7.8,
            y1=8,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=9,
            x1=7.8,
            y1=9,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
)),

fig.update_traces(marker = dict(color=list(map(BarColor, np.ravel(values.values)))),
                  marker_line_color='black',
                  marker_line_width=2.0) #call function to change colors on bars

#fig.show()
fig.write_html('plots/current_kp.html')










#Prev
df_prev = dfKp.iloc[[-2]]
df_prev = df_prev.astype(float)

df_prev_T = df_prev.T #transpose the dataframe (from df_prev to df_prev_T)

df_prev_T.columns = ['Kp']
values = df_prev_T.Kp
x = [0, 1, 2, 3, 4, 5, 6, 7]

def BarColor(vals):
    x = vals
    if x <= 3:
        return "Green"
    if x > 3 and x <= 7:
        return "Yellow"
    if x > 7 and x <= 9:
        return "Red"


data = [go.Bar(
   x = x,
   y = values.values,
   hovertext = ["KP: {}".format(x) for x in values],
   hoverinfo = "text",
   name = 'KP'
)]

values = pd.DataFrame(values)
fig = go.Figure(data=data)

fig.update_xaxes(showline=True, linewidth=2, mirror=True, linecolor='Black', showgrid=False, gridwidth=2, gridcolor='#DCDCDC')
fig.update_yaxes(showline=True, linewidth=2, mirror=True, linecolor='Black', showgrid=False, gridwidth=2, gridcolor='#DCDCDC')

fig.update_layout(
    autosize=False,
    width=1400,
    height=700,
    margin=dict(
        l=150,
        r=50,
        b=100,
        t=100,
    ),
    showlegend=False,
    template='plotly_white',
    hovermode='closest',
    title={
        'text': "Planetary K-index",
        'y':0.9,
        'x':0.536,
        'font_family': 'Balto',
        'font_size': 28,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis = dict(
        tickmode = 'array',
        zeroline = False,
        range=[x_start,x_end],
        tickvals = [-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5],
        ticktext = ['0','3','6','9','12','15','18','21','24'],
        ticks="inside",
        ticklen=10,
        title=yesterday,
        title_font_size = 18,
    ),
    yaxis = dict(
        ticks='outside',
        range=[y_start,y_end],
        ticktext = ['0','1','2','3','4','5','6','7','8','9'],
        title='Kp index',
        title_font_size = 18,
    ),
    hoverlabel=dict(bgcolor='oldlace',
                    font=dict(family='Balto',
                    size=28,
                    color='black')),
)
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=1,
            x1=7.8,
            y1=1,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=2,
            x1=7.8,
            y1=2,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=3,
            x1=7.8,
            y1=3,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=4,
            x1=7.8,
            y1=4,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=5,
            x1=7.8,
            y1=5,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=6,
            x1=7.8,
            y1=6,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=7,
            x1=7.8,
            y1=7,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=8,
            x1=7.8,
            y1=8,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            x0=-0.6,
            y0=9,
            x1=7.8,
            y1=9,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
)),

fig.update_traces(marker = dict(color=list(map(BarColor, np.ravel(values.values)))),
                  marker_line_color='black',
                  marker_line_width=2.0)

fig.write_html('plots/previous_kp.html')











#PAST 3 DAYS
dfKp1 = dfKp.tail(1)

with open('data/combined.csv', 'a') as f:
    if os.path.getsize('data/combined.csv') <= 0: #check if csv is empty
        dfKp.to_csv(f, header=f.tell()==0, index=True, sep = " ") #write content of dataframe if csv is empty
    else:
        df1 = pd.read_csv('data/combined.csv', sep = " ") #if csv is not empty
        df1['date'] = pd.to_datetime(df1['date']) #convert column to datetime
        df1.set_index('date', inplace=True) #set date column as index
        if df1.index[-1] < dtm.date.today(): #if datafile does not have data for current date
            values = dfKp.index > df1.index[-1] #find all the missing rows
            df1 = dfKp[values]
            df1.to_csv('data/combined.csv', mode='a', index =True, sep = " ", header = False) #append the rows to the data file
        if df1.index[-1] == dtm.date.today(): #if data file has data for current date
            df1.drop(df1.tail(1).index,inplace=True) #drop the tail (row with today's data)
            df1 = df1.append(dfKp1, ignore_index=False) #add the most recent data from dataframe
            df1.to_csv('data/combined.csv', mode='w', index =True, sep = " ", header = True) #write the dataframe to csv
f.close()

#Make plot
df = pd.read_csv('data/combined.csv', sep = " ")
df = df.tail(3) #create a dataframe with the last 3 rows

df['date'] = pd.to_datetime(df['date'])
df = df.rename(columns={"date": "time"})
df.set_index('time', inplace=True)

df = df.T #transpose dataframe and change column names
df.columns = ['twodays', 'yesterday', 'today']

values = df.values

val1 = df.twodays.values #get column values in arrays
val2 = df.yesterday.values
val3 = df.today.values

all = np.concatenate((val1, val2, val3)) #create array from three separate arrays
hr  = df.index


x = [0, 1, 2, 3, 4, 5, 6, 7]

def BarColor1(val1):
    x = val1
    if x <= 3:
        return "Green"
    if x > 3 and x <= 7:
        return "Yellow"
    if x > 7 and x <= 9:
        return "Red"

def BarColor2(val2):
    x = val2
    if x <= 3:
        return "Green"
    if x > 3 and x <= 7:
        return "Yellow"
    if x > 7 and x <= 9:
        return "Red"

def BarColor3(val3):
    x = val3
    if x <= 3:
        return "Green"
    if x > 3 and x <= 7:
        return "Yellow"
    if x > 7 and x <= 9:
        return "Red"


#create custom traces
trace1 = go.Bar(
    x = x,
    y = df.twodays.values,
    hovertext = ["{} <br /> KP: {}".format(two_days_ago, x) for x in val1], hoverinfo = "text", name = 'KP',
    marker = dict(color=list(map(BarColor1, np.ravel(val1))))
)
trace2 = go.Bar(
    x = x,
    y = df.yesterday.values,
    hovertext = ["{} <br /> KP: {}".format(yesterday, x) for x in (val2)], hoverinfo = "text", name = 'KP',
    marker = dict(color=list(map(BarColor2, np.ravel(val2))))
)
trace3 = go.Bar(
    x = x,
    y = df.today.values,
    hovertext = ["{} <br /> KP: {}".format(today, x) for x in (val3)], hoverinfo = "text", name = 'KP',
    marker = dict(color=list(map(BarColor3, np.ravel(val3))))
)

#create plots from traces
fig = subplots.make_subplots(rows=1, cols=3,
                          shared_xaxes=True, shared_yaxes=True,
                          vertical_spacing=0,
                          horizontal_spacing=0)

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig.append_trace(trace3, 1, 3)

fig.update_xaxes(showline=True, linewidth=2, mirror=True, linecolor='Black', showgrid=False, gridcolor='white', matches = None)
fig.update_yaxes(showgrid=False, gridcolor='#DCDCDC', linecolor='#808080', matches = None)

#add custom annotations on each subplot
fig.add_annotation(text=two_days_ago,
                  xref="paper", yref="paper",
                  x=-0.042, y=-0.05, font=dict(size=16), showarrow=False)
fig.add_annotation(text=yesterday,
                  xref="paper", yref="paper",
                  x=0.292, y=-0.05, font=dict(size=16), showarrow=False)
fig.add_annotation(text=today,
                  xref="paper", yref="paper",
                  x=0.708, y=-0.05, font=dict(size=16), showarrow=False)
fig.add_annotation(text=tomorrow,
                  xref="paper", yref="paper",
                  x=1.040, y=-0.05, font=dict(size=16), showarrow=False)

fig.add_annotation(text="06:00",
                  xref="paper", yref="paper",
                  x=0.073, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="12:00",
                  xref="paper", yref="paper",
                  x=0.153, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="18:00",
                  xref="paper", yref="paper",
                  x=0.234, y=-0.04, font=dict(size=10), showarrow=False)

fig.add_annotation(text="06:00",
                  xref="paper", yref="paper",
                  x=0.418, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="12:00",
                  xref="paper", yref="paper",
                  x=0.5, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="18:00",
                  xref="paper", yref="paper",
                  x=0.58, y=-0.04, font=dict(size=10), showarrow=False)

fig.add_annotation(text="06:00",
                  xref="paper", yref="paper",
                  x=0.764, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="12:00",
                  xref="paper", yref="paper",
                  x=0.846, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="18:00",
                  xref="paper", yref="paper",
                  x=0.926, y=-0.04, font=dict(size=10), showarrow=False)

fig.add_annotation(text="Three hour data",
                  xref="paper", yref="paper",
                  x=0.5, y=-0.1, font=dict(size=18), showarrow=False)


#customize layout
fig.update_layout(
    autosize=False,
    width=1400,
    height=700,
    margin=dict(
        l=150,
        r=50,
        b=100,
        t=100,
    ),
    showlegend=False,
    template='plotly_white',
    hovermode='closest',
    title={
        'text': f"Kp Index ({two_days_ago} \u2014 {today})",
        'y':0.9,
        'x':0.536,
        'font_family': 'Balto',
        'font_size': 28,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis = dict(
        tickmode = 'array',
        zeroline = False,
        range=[x_start,x_end],
        tickvals = [0,1,2,3,4,5,6,7,8,9],
        ticktext = ['','','','','','','','',''],
        ticks="inside",
        ticklen=10,
    ),
    xaxis2 = dict(
        tickmode = 'array',
        zeroline = False,
        range=[x_start,x_end],
        tickvals = [0,1,2,3,4,5,6,7,8,9],
        ticktext = ['','','','','','','','',''],
        ticks="inside",
        ticklen=10,
    ),
    xaxis3 = dict(
        tickmode = 'array',
        zeroline = False,
        range=[x_start,x_end],
        tickvals = [0,1,2,3,4,5,6,7,8,9],
        ticktext = ['','','','','','','','',''],
        ticks="inside",
        ticklen=10,
    ),
    yaxis = dict(
        ticks='outside',
        range=[y_start,y_end],
        ticktext = ['0','1','2','3','4','5','6','7','8','9'],
        title='Kp index',
        title_font_size = 18,
    ),
    yaxis2 = dict(
        range=[y_start,y_end],
        title_font_size = 18,
    ),
    yaxis3 = dict(
        range=[y_start,y_end],
        title_font_size = 18,
    ),
    hoverlabel=dict(bgcolor='oldlace',
                    font=dict(family='Balto',
                    size=28,
                    color='black')),
)

fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=-0.59,
        y0=-0.6,
        x1=-0.59,
        y1=9,
        line=dict(color="Black", width=5),
    ),row=1,col=1)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=7.63,
        y0=-0.6,
        x1=7.63,
        y1=9,
        line=dict(color="Black", width=3),
    ),row=1,col=3)

fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=1.5,
        y0=0.0,
        x1=1.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=1)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=3.5,
        y0=0.0,
        x1=3.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=1)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=5.5,
        y0=0.0,
        x1=5.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=1)

fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=1.5,
        y0=0.0,
        x1=1.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=2)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=3.5,
        y0=0.0,
        x1=3.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=2)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=5.5,
        y0=0.0,
        x1=5.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=2)

fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=1.5,
        y0=0.0,
        x1=1.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=3)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=3.5,
        y0=0.0,
        x1=3.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=3)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=5.5,
        y0=0.0,
        x1=5.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=3)


fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=1,
            x1=7.8,
            y1=1,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=2,
            x1=7.8,
            y1=2,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=3,
            x1=7.8,
            y1=3,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=4,
            x1=7.8,
            y1=4,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=5,
            x1=7.8,
            y1=5,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=6,
            x1=7.8,
            y1=6,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=7,
            x1=7.8,
            y1=7,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=8,
            x1=7.8,
            y1=8,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=9,
            x1=7.8,
            y1=9,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
)),



fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=1,
            x1=7.8,
            y1=1,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=2,
            x1=7.8,
            y1=2,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=3,
            x1=7.8,
            y1=3,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=4,
            x1=7.8,
            y1=4,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=5,
            x1=7.8,
            y1=5,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=6,
            x1=7.8,
            y1=6,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=7,
            x1=7.8,
            y1=7,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=8,
            x1=7.8,
            y1=8,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=9,
            x1=7.8,
            y1=9,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
)),

fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=1,
            x1=7.8,
            y1=1,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=2,
            x1=7.8,
            y1=2,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=3,
            x1=7.8,
            y1=3,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=4,
            x1=7.8,
            y1=4,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=5,
            x1=7.8,
            y1=5,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=6,
            x1=7.8,
            y1=6,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=7,
            x1=7.8,
            y1=7,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=8,
            x1=7.8,
            y1=8,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=9,
            x1=7.8,
            y1=9,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
)),


fig.update_traces(marker_line_color='black',
                  marker_line_width=2.0)

fig.write_html('plots/past_3days_kp.html')











#3 DAY FORECAST
df_3day = pd. read_csv('data/3_day_kp.csv', sep = " ")

df_3day["time"].replace({"00-03UT": "00:00-03:00", "03-06UT": "03:00-06:00", "06-09UT": "06:00-09:00", "09-12UT": "09:00-12:00",
                         "12-15UT": "12:00-15:00", "15-18UT": "15:00-18:00", "18-21UT": "18:00-21:00", "21-00UT": "21:00-24:00"}, inplace=True) #edit row names
df_3day.columns = ['time', 'day1', 'day2', 'day3']

df_3day.set_index('time', inplace=True)

values = df_3day.values

val1 = df_3day.day1.values
val2 = df_3day.day2.values
val3 = df_3day.day3.values

all = np.concatenate((val1, val2, val3)) #make a new array by combining all 3 arrays
hr  = df_3day.index #time, used for hover information
#for h in hr:
    #print(h)

x = [0, 1, 2, 3, 4, 5, 6, 7]

def BarColor1(val1):
    x = val1
    if x <= 3:
        return "Green"
    if x > 3 and x <= 7:
        return "Yellow"
    if x > 7 and x <= 9:
        return "Red"

def BarColor2(val2):
    x = val2
    if x <= 3:
        return "Green"
    if x > 3 and x <= 7:
        return "Yellow"
    if x > 7 and x <= 9:
        return "Red"

def BarColor3(val3):
    x = val3
    if x <= 3:
        return "Green"
    if x > 3 and x <= 7:
        return "Yellow"
    if x > 7 and x <= 9:
        return "Red"



trace1 = go.Bar(
    x = x,
    y = df_3day.day1.values,
    hovertext = ["{} <br /> KP: {}".format(today, x) for x in val1], hoverinfo = "text", name = 'KP',
    marker = dict(color=list(map(BarColor1, np.ravel(val1))))
)
trace2 = go.Bar(
    x = x,
    y = df_3day.day2.values,
    hovertext = ["{} <br /> KP: {}".format(tomorrow, x) for x in (val2)], hoverinfo = "text", name = 'KP',
    marker = dict(color=list(map(BarColor2, np.ravel(val2))))
)
trace3 = go.Bar(
    x = x,
    y = df_3day.day3.values,
    hovertext = ["{} <br /> KP: {}".format(two_days, x) for x in (val3)], hoverinfo = "text", name = 'KP',
    marker = dict(color=list(map(BarColor3, np.ravel(val3))))
)

fig = subplots.make_subplots(rows=1, cols=3,
                          shared_xaxes=True, shared_yaxes=True,
                          vertical_spacing=0,
                          horizontal_spacing=0)

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig.append_trace(trace3, 1, 3)

fig.update_xaxes(showline=True, linewidth=2, mirror=True, linecolor='Black', showgrid=False, gridcolor='white', matches = None)
fig.update_yaxes(showgrid=False, gridcolor='#DCDCDC', linecolor='#808080', matches = None)

fig.add_annotation(text=today,
                  xref="paper", yref="paper",
                  x=-0.042, y=-0.05, font=dict(size=16), showarrow=False)
fig.add_annotation(text=tomorrow,
                  xref="paper", yref="paper",
                  x=0.292, y=-0.05, font=dict(size=16), showarrow=False)
fig.add_annotation(text=two_days,
                  xref="paper", yref="paper",
                  x=0.708, y=-0.05, font=dict(size=16), showarrow=False)
fig.add_annotation(text=three_days,
                  xref="paper", yref="paper",
                  x=1.040, y=-0.05, font=dict(size=16), showarrow=False)

fig.add_annotation(text="06:00",
                  xref="paper", yref="paper",
                  x=0.073, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="12:00",
                  xref="paper", yref="paper",
                  x=0.153, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="18:00",
                  xref="paper", yref="paper",
                  x=0.234, y=-0.04, font=dict(size=10), showarrow=False)

fig.add_annotation(text="06:00",
                  xref="paper", yref="paper",
                  x=0.418, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="12:00",
                  xref="paper", yref="paper",
                  x=0.5, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="18:00",
                  xref="paper", yref="paper",
                  x=0.58, y=-0.04, font=dict(size=10), showarrow=False)

fig.add_annotation(text="06:00",
                  xref="paper", yref="paper",
                  x=0.764, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="12:00",
                  xref="paper", yref="paper",
                  x=0.846, y=-0.04, font=dict(size=10), showarrow=False)
fig.add_annotation(text="18:00",
                  xref="paper", yref="paper",
                  x=0.926, y=-0.04, font=dict(size=10), showarrow=False)

fig.add_annotation(text="Three hour data",
                  xref="paper", yref="paper",
                  x=0.5, y=-0.1, font=dict(size=18), showarrow=False)


fig.update_layout(
    autosize=False,
    width=1400,
    height=700,
    margin=dict(
        l=150,
        r=50,
        b=100,
        t=100,
    ),
    showlegend=False,
    template='plotly_white',
    hovermode='closest',
    title={
        'text': f"Kp Index Forecast ({today} \u2014 {two_days})",
        'y':0.9,
        'x':0.536,
        'font_family': 'Balto',
        'font_size': 28,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis = dict(
        tickmode = 'array',
        zeroline = False,
        range=[x_start,x_end],
        tickvals = [0,1,2,3,4,5,6,7,8,9],
        ticktext = ['','','','','','','','',''],
        ticks="inside",
        ticklen=10,
    ),
    xaxis2 = dict(
        tickmode = 'array',
        zeroline = False,
        range=[x_start,x_end],
        tickvals = [0,1,2,3,4,5,6,7,8,9],
        ticktext = ['','','','','','','','',''],
        ticks="inside",
        ticklen=10,
    ),
    xaxis3 = dict(
        tickmode = 'array',
        zeroline = False,
        range=[x_start,x_end],
        tickvals = [0,1,2,3,4,5,6,7,8,9],
        ticktext = ['','','','','','','','',''],
        ticks="inside",
        ticklen=10,
    ),
    yaxis = dict(
        ticks='outside',
        range=[y_start,y_end],
        ticktext = ['0','1','2','3','4','5','6','7','8','9'],
        title='Kp index',
        title_font_size = 18,
    ),
    yaxis2 = dict(
        range=[y_start,y_end],
        title_font_size = 18,
    ),
    yaxis3 = dict(
        range=[y_start,y_end],
        title_font_size = 18,
    ),
    hoverlabel=dict(bgcolor='oldlace',
                    font=dict(family='Balto',
                    size=28,
                    color='black')),
)

fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=-0.59,
        y0=-0.6,
        x1=-0.59,
        y1=9,
        line=dict(color="Black", width=5),
    ),row=1,col=1)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=7.63,
        y0=-0.6,
        x1=7.63,
        y1=9,
        line=dict(color="Black", width=3),
    ),row=1,col=3)

fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=1.5,
        y0=0.0,
        x1=1.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=1)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=3.5,
        y0=0.0,
        x1=3.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=1)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=5.5,
        y0=0.0,
        x1=5.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=1)

fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=1.5,
        y0=0.0,
        x1=1.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=2)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=3.5,
        y0=0.0,
        x1=3.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=2)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=5.5,
        y0=0.0,
        x1=5.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=2)

fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=1.5,
        y0=0.0,
        x1=1.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=3)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=3.5,
        y0=0.0,
        x1=3.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=3)
fig.add_shape(
    go.layout.Shape(
        type="line",
        yref="paper",
        xref="x",
        x0=5.5,
        y0=0.0,
        x1=5.5,
        y1=0.1,
        line=dict(color="Black", width=1),
    ),row=1,col=3)


fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=1,
            x1=7.8,
            y1=1,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=2,
            x1=7.8,
            y1=2,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=3,
            x1=7.8,
            y1=3,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=4,
            x1=7.8,
            y1=4,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=5,
            x1=7.8,
            y1=5,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=6,
            x1=7.8,
            y1=6,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=7,
            x1=7.8,
            y1=7,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=8,
            x1=7.8,
            y1=8,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x", 
            yref="y",
            x0=-0.6,
            y0=9,
            x1=7.8,
            y1=9,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
)),



fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=1,
            x1=7.8,
            y1=1,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=2,
            x1=7.8,
            y1=2,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=3,
            x1=7.8,
            y1=3,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=4,
            x1=7.8,
            y1=4,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=5,
            x1=7.8,
            y1=5,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=6,
            x1=7.8,
            y1=6,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=7,
            x1=7.8,
            y1=7,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=8,
            x1=7.8,
            y1=8,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x2", 
            yref="y2",
            x0=-0.6,
            y0=9,
            x1=7.8,
            y1=9,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
)),

fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=1,
            x1=7.8,
            y1=1,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=2,
            x1=7.8,
            y1=2,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=3,
            x1=7.8,
            y1=3,
            layer='below',
            line=dict(
                color="green",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=4,
            x1=7.8,
            y1=4,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=5,
            x1=7.8,
            y1=5,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=6,
            x1=7.8,
            y1=6,
            layer='below',
            line=dict(
                color="yellow",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=7,
            x1=7.8,
            y1=7,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=8,
            x1=7.8,
            y1=8,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
))
fig.add_shape(
        dict(
            type="line",
            xref="x3", 
            yref="y3",
            x0=-0.6,
            y0=9,
            x1=7.8,
            y1=9,
            layer='below',
            line=dict(
                color="red",
                width=2,
            )
)),


fig.update_traces(marker_line_color='black',
                  marker_line_width=2.0)

fig.write_html('plots/3day_forecast_kp.html')