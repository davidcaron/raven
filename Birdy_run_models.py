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
from urllib.request import urlretrieve
 
wps = WPSClient("http://localhost:9099/wps")

# Common data for the four models
config = dict(
    start_date=dt.datetime(2000, 1, 1),
    end_date=dt.datetime(2002, 1, 1),
    area=4250.6,
    elevation=843.0,
    latitude=54.4848,
    longitude=-123.3659,
    )


"""
////////////////////////////////////////
//////////   RAVEN HMETS    ////////////
////////////////////////////////////////
"""

params = '9.5019, 0.2774, 6.3942, 0.6884, 1.2875, 5.4134, 2.3641, 0.0973, 0.0464, 0.1998, 0.0222, -1.0919, ' \
                 '2.6851, 0.3740, 1.0000, 0.4739, 0.0114, 0.0243, 0.0069, 310.7211, 916.1947'
ts=TESTDATA['raven-hmets-nc-ts']

# Let's call the model
resp = wps.raven_hmets(ts=str(ts), params=params, **config)

# Get the 4 outputs
[hydrograph,storage,solution,diagnostics]=resp.get(asobj=True)

print(diagnostics)

"""
tmp_file, _ = urlretrieve(diagnostics)
tmp_content = open(tmp_file).readlines()
idx_diag = tmp_content[0].split(',').index("DIAG_NASH_SUTCLIFFE")
diag = np.float(tmp_content[1].split(',')[idx_diag])
print(diag)

# Hydrograph
tmp_file, _ = urlretrieve(hydrograph,'hydrograph_hmets_raven.nc')
# ds = xr.open_dataset(tmp_file)
"""


"""
////////////////////////////////////////
//////////   RAVEN GR4JCN   ////////////
////////////////////////////////////////
"""
params = '0.529, -3.396, 407.29, 1.072, 16.9, 0.947'
ts=TESTDATA['raven-gr4j-cemaneige-nc-ts']

# Let's call the model
resp = wps.raven_gr4j_cemaneige(ts=str(ts), params=params, **config)

# Get the 4 outputs
[hydrograph_gr4j,storage,solution,diagnostics]=resp.get(asobj=True)

print(diagnostics)

# Prepare for the ObjFun calc
[hydrograph_gr4j,storage,solution,diagnostics]=resp.get(asobj=False)


"""
////////////////////////////////////////
//////////   RAVEN MOHYSE   ////////////
////////////////////////////////////////
"""
params = '1.00, 0.0468, 4.2952, 2.6580, 0.4038, 0.0621, 0.0273, 0.0453'
hrus = '0.9039, 5.6179775'
        
ts=TESTDATA['raven-mohyse-nc-ts']

# Let's call the model
resp = wps.raven_mohyse(ts=str(ts), params=params, hrus=hrus, **config)

# Get the 4 outputs
[hydrograph,storage,solution,diagnostics]=resp.get(asobj=True)

print(diagnostics)



"""
////////////////////////////////////////
//////////   RAVEN HBV-EC   ////////////
////////////////////////////////////////
"""
params = '0.05984519, 4.072232, 2.001574, 0.03473693, 0.09985144, 0.5060520, 3.438486, 38.32455, ' \
                 '0.4606565, 0.06303738, 2.277781, 4.873686, 0.5718813, 0.04505643, 0.877607, 18.94145,  ' \
                 '2.036937, 0.4452843, 0.6771759, 1.141608, 1.024278'

ts=TESTDATA['raven-hbv-ec-nc-ts']

# Let's call the model
resp = wps.raven_hbv_ec(ts=str(ts), params = params, **config)

# Get the 4 outputs
[hydrograph_hbv,storage,solution,diagnostics]=resp.get(asobj=True)

print(diagnostics)

# Get the 4 outputs for ObjFun calc
[hydrograph_hbv,storage,solution,diagnostics]=resp.get(asobj=False)

"""
////////////////////////////////////////
////////  OBJETIVE FUNCTION   //////////
////////////////////////////////////////
"""

# TODO: RUNNING, BUT USES q_obs VARIABLE NAME BY DEFAULT FOR OBSERVED. SO THE 
# COMPARISON IS NOT EQUAL TO 0 NSE EVEN IF WE USE THE SAME FILE TWICE. 

#obs=TESTDATA['hbv_hydrograph']
#sim=TESTDATA['gr4j_hydrograph']
#resp=wps.objective_function(obs=str(obs), sim=str(obs))

# Other more simple method based on what was calculated earlier:
resp = wps.objective_function(obs=hydrograph_hbv, sim=hydrograph_gr4j)
# Get the 4 outputs

[results]=resp.get(asobj=True)

print(results)      
             
             