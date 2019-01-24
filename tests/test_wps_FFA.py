# -*- coding: utf-8 -*-

import pytest
from pywps import Service
from pywps.tests import assert_response_success
from raven.processes import FrequencyAnalysisProcess
from .common import client_for, TESTDATA, get_output, urlretrieve, CFG_FILE
import numpy as np
import pdb

datainputs = "ts=files@xlink:href=file://{ts};" \
             "FFA_ExtremeType={FFA_ExtremeType};" \
             "FFA_AnalysisPeriod={FFA_AnalysisPeriod};" \
             "FFA_ReturnPeriods={FFA_ReturnPeriods};" \
             "FFA_distribution={FFA_distribution};"
        
inputs = dict(FFA_ExtremeType='high',
              FFA_AnalysisPeriod='year',
              FFA_distribution='gumbel_r',
              FFA_ReturnPeriods='2,5,10,20,25,50,100'
              )

class TestFrequencyAnalysis:

    @pytest.mark.parametrize("dist", ('gumbel_r', 'lognorm', 'pearson3', 'gamma','genextreme')) 
    @pytest.mark.parametrize("types", ('high','low'))
    @pytest.mark.parametrize("period",('year','winter','autumn','summer','spring','1','12','6'))
    def test_FrequencyAnalysis(self, dist, types, period):
        client = client_for(Service(processes=[FrequencyAnalysisProcess(), ], cfgfiles=CFG_FILE))
        
        inp = inputs.copy()
        inp['ts'] = TESTDATA['ind-freq']
        inp['FFA_ExtremeType'] = types #'high'
        inp['FFA_ReturnPeriods'] = '2,5,10,20,25,50,100,1000'
        inp['FFA_distribution'] = dist
        inp['FFA_AnalysisPeriod'] = period #'year'
        
        resp = client.get(service='WPS', request='execute', version='1.0.0',
                          identifier='frequency-analysis',
                          datainputs=datainputs.format(**inp))

        assert_response_success(resp)
        
        out = get_output(resp.xml)
        assert 'FFA_Results' in out
        assert 'FFA_Pvalues' in out
        results, _ = urlretrieve(out['FFA_Results'])
        p_values, _ = urlretrieve(out['FFA_Pvalues'])
        FFA_cms=np.loadtxt(results)
        p_value=np.loadtxt(p_values)
        assert p_value<=1.
        assert p_value>=0.
        assert len(FFA_cms)==len(np.array(list(map(float, inp['FFA_ReturnPeriods'].split(',')))))
        