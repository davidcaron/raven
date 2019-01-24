# -*- coding: utf-8 -*-

import pytest
from pywps import Service
from pywps.tests import assert_response_success
from raven.processes import HydroIndicatorsProcess
from .common import client_for, TESTDATA, get_output, urlretrieve, CFG_FILE
import pdb
import pandas as pd

datainputs = "ts=files@xlink:href=file://{ts};" \
             "FFA_distribution={FFA_distribution};"
        
inputs = dict(FFA_distribution='gumbel_r')

class TestHydroIndicators:

    @pytest.mark.parametrize("dist", ('gumbel_r', 'lognorm', 'pearson3', 'gamma','genextreme')) 
   
    def test_HydroIndicators(self, dist):
        client = client_for(Service(processes=[HydroIndicatorsProcess(), ], cfgfiles=CFG_FILE))
        
        inp = inputs.copy()
        inp['ts'] = TESTDATA['ind-freq']
        inp['FFA_distribution'] = dist
        
        resp = client.get(service='WPS', request='execute', version='1.0.0',
                          identifier='hydro-indicators',
                          datainputs=datainputs.format(**inp))

        assert_response_success(resp)
        
        out = get_output(resp.xml)
        
        assert 'HI_Results' in out
        
        results, _ = urlretrieve(out['HI_Results'])
        
        HydroIndicators = pd.DataFrame.from_csv(results)
        pdb.set_trace()
        assert HydroIndicators.shape[0]==28
        