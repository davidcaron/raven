from . import wpsio as wio
import logging
from pywps import Process, LiteralInput, ComplexOutput, FORMATS, ComplexInput
from pathlib import Path
from raven.utilities.ffa_tools import read_flow_file, extract_maxima_series, flood_frequency_analysis
from raven.utilities.indicators import extract_all_indicators
LOGGER = logging.getLogger("PYWPS")
import numpy as np
import pdb

class HydroIndicatorsProcess(Process):
    def __init__(self):
        """
        TODO: Include a description of each method.
        Notes
        -----
        The available regionalization methods are:
            
        """    
        HI_distribution= LiteralInput('HI_distribution', 'Distribution from Scipy.stats (distribution name)',
                               abstract="Name of the distribution to be used to fit the data for certain indicators.",
                               data_type='string',
                               allowed_values=('gamma','genextreme','gumbel_r','lognorm','pearson3'),
                               default='gumbel_r',
                               min_occurs=0)
        
        
        HI_Results = ComplexOutput('HI_Results', 'Results from the Hydro Indicators Analysis',
                                abstract="Results of the 28 indicators computed by the function",
                                supported_formats=[FORMATS.TEXT],
                                as_reference=True)
        
        
        inputs = [wio.ts, HI_distribution]
    
        outputs = [HI_Results]

        
    
     
        super(HydroIndicatorsProcess, self).__init__(
             self._handler,   
             identifier = "hydro-indicators",
             title = "Compute 28 usual indicaors on streamflow timeseries from the Atlas Hydroclimatique du Québec",
             abstract = "Get 28 indicators from a hydrograph according to desired statistics and distributions",
             version = '0.1',
             inputs=inputs,
             outputs=outputs,
             keywords=["hydro indicators", "indicators", "ATLAS"],
             status_supported=True,
             store_supported=True)
            

    def _handler(self, request, response):
        response.update_status('PyWPS process {} started.'.format(self.identifier), 0)

        file_name = [e.file for e in request.inputs.pop('ts')]
        dist = request.inputs.pop('HI_distribution')[0].data
        
        kwds = {}
        for key, val in request.inputs.items():
            kwds[key] = request.inputs[key][0].data

        df = read_flow_file(file_name=file_name,**kwds)
        s = extract_all_indicators(df=df, dist=dist, **kwds)

        
        # Write output
        HIPath=Path(self.workdir) / 'HydroIndicatorsAnalysis.txt'
        with open(HIPath, 'w') as f:
            s.to_csv(f,header=['Streamflow'])
        response.outputs['HI_Results'].file = str(HIPath)

        return response
