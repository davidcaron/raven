#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 09:30:38 2019

@author: ets
"""

"""

BIRDY TEST

"""
from BirdyTestdata import TESTDATA
from birdy import WPSClient
import datetime as dt

 
wps = WPSClient("http://localhost:9099/wps")

# Common data for the four models



"""
////////////////////////////////////////
/////////   OSTRICH HMETS    ///////////
////////////////////////////////////////
"""
lowerBounds = '0.3, 0.01, 0.5, 0.15, 0.0, 0.0, -2.0, 0.01, 0.0, 0.01, 0.005, -5.0, \
                      0.0, 0.0, 0.0, 0.0, 0.00001, 0.0, 0.00001, 0.0, 0.0'
upperBounds = '20.0, 5.0, 13.0, 1.5, 20.0, 20.0, 3.0, 0.2, 0.1, 0.3, 0.1, 2.0, 5.0, \
                      1.0, 3.0, 1.0, 0.02, 0.1, 0.01, 0.5, 2.0'
                      
ts=TESTDATA['ostrich-hmets-nc-ts']
config = dict(
    algorithm='DDS',
    max_iterations=10,
    area=4250.6,
    elevation=843.0,
    latitude=54.4848,
    longitude=-123.3659,
    lowerbounds=lowerBounds,
    upperbounds=upperBounds,
    start_date=dt.datetime(1954, 1, 1),
    duration=208,
    )

# Let's call the model
resp = wps.ostrich_hmets(ts=str(ts), **config)

# Get the 4 outputs
[calibrationTXT,CalibrationResults,calibrated_params]=resp.get(asobj=True)

print(calibrationTXT)
