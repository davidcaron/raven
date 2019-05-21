#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 20:11:23 2019

@author: ets
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:24:45 2019

@author: ets
"""


from birdy import WPSClient
import pandas as pd
import numpy as np
import os
import time

url = "http://localhost:9099/wps"
wps = WPSClient(url, progress=True)

nbBasin=5797

area=np.zeros(nbBasin)
slope=np.zeros(nbBasin)
centroid_lat=np.zeros(nbBasin)
centroid_lon=np.zeros(nbBasin)
Forest=np.zeros(nbBasin)
Shrubs=np.zeros(nbBasin)
Wetland=np.zeros(nbBasin)
Crops=np.zeros(nbBasin)
Water=np.zeros(nbBasin)
Urban=np.zeros(nbBasin)
Grass=np.zeros(nbBasin)
SnowIce=np.zeros(nbBasin)
elevation=np.zeros(nbBasin)
slope=np.zeros(nbBasin)
gravelius=np.zeros(nbBasin)
perimeter=np.zeros(nbBasin)
aspect=np.zeros(nbBasin)
Success=np.zeros(nbBasin)
ID=nbBasin*[None]



for i in range(1, nbBasin+1):

    tmp=pd.read_csv('TerrainPropertiesList.csv')
    elevation=tmp['Elevation']
    aspect=tmp['Aspect']
    slope=tmp['Slope']
    Success=tmp['RunSuccess']

    if Success[i-1]==0:
        for attempt in range(1):
            try:
                
                print('Doing Basin: ' + str(i))
                shape2='/home/ets/SHP_ZIP/Basin_' + str(i) +'.zip'
                
                """
                Foresty=0.
                Shrubsy=0.
                Cropsy=0.
                Urbany=0.
                Watery=0.
                Wetlandy=0.
                Grassy=0.
                SnowIcey=0.
                

			# Uncomment this section for NalCMS zonal stats
                resp = wps.nalcms_zonal_stats(shape=shape2, select_all_touching=True,band=1, simple_categories=True)
                
                while resp.isNotComplete():
                    time.sleep(1)
                    
                [statistics]=resp.get(asobj=True)
                statistics=statistics['features'][0]['properties']
                if 'Forest' in statistics.keys():
                    Foresty=statistics['Forest']
                if 'Shrubs' in statistics.keys():
                    Shrubsy=statistics['Shrubs']
                if 'Grass' in statistics.keys():
                    Grassy=statistics['Grass']
                if 'Wetland' in statistics.keys():
                    Wetlandy=statistics['Wetland']
                if 'Water' in statistics.keys():
                    Watery=statistics['Water']
                if 'Urban' in statistics.keys():
                    Urbany=statistics['Urban']
                if 'Crops' in statistics.keys():
                    Cropsy=statistics['Crops']
                if 'SnowIce' in statistics.keys():
                    SnowIcey=statistics['SnowIce']
                
                Total=Foresty+Shrubsy+Grassy+Wetlandy+Watery+Urbany+Cropsy+SnowIcey
                Forest[i-1]=Foresty/Total
                Grass[i-1]=Grassy/Total
                Wetland[i-1]=Wetlandy/Total
                Water[i-1]=Watery/Total
                Urban[i-1]=Urbany/Total
                Shrubs[i-1]=Shrubsy/Total
                Crops[i-1]=Cropsy/Total
                SnowIce[i-1]=SnowIcey/Total    
                
                

			# Uncomment this section for the Shape properties
                resp = wps.shape_properties(shape=shape2, projected_crs=32198)
                while resp.isNotComplete():
                    time.sleep(1)
                [properties]=resp.get(asobj=True)
                area[i-1]=properties[0]['area']/1000000.0
                centroid_lon[i-1]=properties[0]['centroid'][0]
                centroid_lat[i-1]=properties[0]['centroid'][1]
                gravelius[i-1]=properties[0]['gravelius']
                perimeter[i-1]=properties[0]['perimeter']
                ID[i-1]=properties[0]['ID']
                """

			# This section does the terrain analysis
                resp=wps.terrain_analysis(shape=shape2, select_all_touching=True,projected_crs=3978)
                while resp.isNotComplete():
                    time.sleep(1)
                
                [properties]=resp.get(asobj=True)
                elevation[i-1]=properties[0]['elevation']
                slope[i-1]=properties[0]['slope']
                aspect[i-1]=properties[0]['aspect']
                Success[i-1]=1
    
                # For terrain_analysis
                zippedList =  list(zip(elevation, slope, aspect, Success))
                frameList=pd.DataFrame(data=zippedList, columns=['Elevation','Slope','Aspect','RunSuccess'])
                frameList.to_csv('TerrainPropertiesList.csv')
   
            except:
                print('Failed, restarting iter ' + str(attempt))# perhaps reconnect, etc.
                #if os.path.exists("/home/ets/src/raven/pywps-logs.sqlite"):
                   
                    # os.remove("/home/ets/src/raven/pywps-logs.sqlite")
                
            else:
                break
    

#zippedList =  list(zip(ID, area, centroid_lat, centroid_lon, gravelius, perimeter, Success))        
#frameList=pd.DataFrame(data=zippedList, columns=['ID', 'Area','Centroid_Lat','Centroid_Lon','Gravelius','Perimeter','RunSuccess'])
#frameList.to_csv('ShapePropertiesList.csv')