#!/usr/bin/python3

import netCDF4 as nc
import numpy as np
from datetime import date
from marineHeatWaves import detect
import csv
f = 'Port_Hacking_site'
fn = f+'.nc'
ds = nc.Dataset(fn)
time=ds['time']
#1981-1-1
start_day=date(1981,1,1).toordinal()
dtime = [start_day + ((tt-55200)/86400) for tt in time]


#list of availablke times
#this is the processed raw data where missing time is not filled.
dates = [date.fromordinal(tt.astype(int)) for tt in dtime]


#for refference only, we arbitarrily take 1 point:
la = ds['lat']
lat = []
for i in la:
    lat.append(i.data.item(0))
lo = ds['lon']
lon = []
for i in lo:
    lon.append(i.data.item(0))


#this is the tempreture array
temp = []
#creating time array t
#this is the comnplete timne series with all missing value filled
t = []
i=dtime[0]
j = 0
while i <= dtime[-1]:
    t.append(date.fromordinal((i).astype(int)).toordinal())
    #if the data on a specific day is misisng, fill it wilth 0
    if i == dtime[j]:
        j+=1
        index = dtime.index(i)
        t_temp = 0
        t_ntemp = 0
        for latitude in range(1,6):

            for longitude in range (132,137):
                tt = ds['sea_surface_temperature'][index,latitude,longitude].data.item(0) 
                if tt != 0.0:
                    t_temp += tt
                    t_ntemp += 1
        avg_temp = 0
        if t_ntemp != 0:
            avg_temp = (t_temp / t_ntemp) - 273.16
        else:
            avg_temp = np.nan
        temp.append(avg_temp)
    else:
        temp.append(np.nan)    
    i+=1

t = np.array(t)
temp = np.array(temp)
mhws = detect(t,temp,climatologyPeriod=[1992,2020], maxPadLength=4)


start = [date.fromordinal(int(st)) for st in mhws[0]['time_start']]
end = [date.fromordinal(int(st)) for st in mhws[0]['time_end']]
duration = mhws[0]['duration']
peak_time = [date.fromordinal(int(st)) for st in mhws[0]['time_peak']]
int_max = mhws[0]['intensity_max']
int_cum = mhws[0]['intensity_cumulative']
int_mean = mhws[0]['intensity_mean']

with open(f+'_analys.csv','w',newline = '') as a_file:
    writer = csv.writer(a_file)
    writer.writerow(["index_number","time_start","time_end","duration","peak_time","max_intensity","mean_intensity","cumulative_intensity"])
    i = 0
    while i < len(start):
        writer.writerow([i+1,start[i],end[i],duration[i],peak_time[i],int_max[i],int_mean[i],int_cum[i]])
        i += 1
