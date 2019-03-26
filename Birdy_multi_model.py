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
//////////   MULTI_MODEL    ////////////
////////////////////////////////////////
"""
ts = TESTDATA['raven-hmets-nc-ts']
gr4jcn ='0.529, -3.396, 407.29, 1.072, 16.9, 0.947'
hmets = '9.5019, 0.2774, 6.3942, 0.6884, 1.2875, 5.4134, 2.3641, 0.0973, 0.0464, 0.1998, 0.0222, -1.0919, ' \
         '2.6851, 0.3740, 1.0000, 0.4739, 0.0114, 0.0243, 0.0069, 310.7211, 916.1947'

# Let's run the model
resp=wps.raven_multi_model(ts=str(ts),
     start_date=dt.datetime(2000, 1, 1),
     end_date=dt.datetime(2010, 1, 1),
     area=4250.6,
     elevation=843.0,
     latitude=54.4848,
     longitude=-123.3659,
     gr4jcn=gr4jcn,
     hmets=hmets,
     )


# Get the 4 outputs. Here the NetCDF converter seems to be amiss? Error -51 Unknown file format...
# OSError: [Errno -51] NetCDF: Unknown file format: b'/tmp/tmp2de4dfd0'
[hydrographs,storage,solution,diagnostics]=resp.get(asobj=True)

print(diagnostics)
