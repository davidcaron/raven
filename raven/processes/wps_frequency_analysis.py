from . import wpsio as wio
import logging
from pywps import Process, LiteralInput, ComplexOutput, FORMATS, ComplexInput
from pathlib import Path
from raven.utilities.ffa_tools import read_flow_file, extract_maxima_series, flood_frequency_analysis
LOGGER = logging.getLogger("PYWPS")
import numpy as np
import pdb

class FrequencyAnalysisProcess(Process):
    def __init__(self):
        """
        TODO: Include a description of each method.
        Notes
        -----
        The available regionalization methods are:
            
        """
        FFA_ExtremeType = LiteralInput('FFA_ExtremeType', 'Type of extreme to consider for floods or low-flows: {"high","low"}',
                              abstract="Extremes type of interest. 'high' for floods, 'low' for low-flows",
                              data_type='string',
                              allowed_values=('high','low'),
                              default='high',
                              min_occurs=0)
    
        FFA_AnalysisPeriod = LiteralInput('FFA_AnalysisPeriod', 'Period used to calculate statistics (year, monthly, etc.)',
                               abstract="String representing the period for which the statisticas will be computed from the hydrograph.",
                               data_type='string',
                               default='year',
                               min_occurs=0)
    
        FFA_distribution= LiteralInput('FFA_distribution', 'Distribution from Scipy.stats (distribution name)',
                               abstract="Name of the distribution to be used to fit the data for frequency analysis.",
                               data_type='string',
                               allowed_values=('gamma','genextreme','gumbel_r','lognorm','pearson3'),
                               default='gumbel_r',
                               min_occurs=0)
        
        FFA_ReturnPeriods = LiteralInput('FFA_ReturnPeriods', 'Return Period array (years)',
                               data_type='string',
                               abstract="Numpy Array of Return periods for frequency analysis",
                               default='2, 5, 10, 25, 50, 100',
                               )
        
        
        FFA_Results = ComplexOutput('FFA_Results', 'Results from the FFA Analysis',
                                abstract="Text data for the FFA Analysis",
                                supported_formats=[FORMATS.TEXT],
                                as_reference=True)
        
        FFA_Pvalues = ComplexOutput('FFA_Pvalues', 'P-value from the FFA distribution fit',
                                abstract="Returns the p-value for the fitted distribution. Lower p-values (closer to 0) indicate worse fits",
                                supported_formats=[FORMATS.TEXT],
                                as_reference=True)
        
        inputs = [wio.ts, FFA_ExtremeType, FFA_AnalysisPeriod, FFA_distribution, FFA_ReturnPeriods]
    
        outputs = [FFA_Results, FFA_Pvalues]

        
    
     
        super(FrequencyAnalysisProcess, self).__init__(
             self._handler,   
             identifier = "frequency-analysis",
             title = "Compute frequency analysis on streamflow timeseries",
             abstract = "Get frequency analysis results from a hydrograph according to desired statistics and distributions",
             version = '0.1',
             inputs=inputs,
             outputs=outputs,
             keywords=["frequency analysis"],
             status_supported=True,
             store_supported=True)
            

    def _handler(self, request, response):
        response.update_status('PyWPS process {} started.'.format(self.identifier), 0)

        file_name = [e.file for e in request.inputs.pop('ts')]
        extreme_type = request.inputs.pop('FFA_ExtremeType')[0].data
        time_period = request.inputs.pop('FFA_AnalysisPeriod')[0].data
        dist = request.inputs.pop('FFA_distribution')[0].data
        T=request.inputs['FFA_ReturnPeriods'][0].data
        T = np.array(list(map(float, request.inputs['FFA_ReturnPeriods'][0].data.split(','))))
 
        
        kwds = {}
        for key, val in request.inputs.items():
            kwds[key] = request.inputs[key][0].data

        df = read_flow_file(file_name=file_name,**kwds)
        Qx = extract_maxima_series(df=df,
                               time_period=time_period,
                               extreme_type=extreme_type,**kwds)
        X, p_value = flood_frequency_analysis(Qx,
                                 dist=dist,
                                 extreme_type=extreme_type,
                                 T=T,**kwds)
        
        # Write output
        FreqPath=Path(self.workdir) / 'FreqAnalysis.txt'
        with open(FreqPath, 'w') as f:
            np.savetxt(f,X)
        response.outputs['FFA_Results'].file = str(FreqPath)
      
        PvaluePath=Path(self.workdir) / 'Pvalue.txt'
        with open(PvaluePath, 'w') as f2:
            np.savetxt(f2,np.reshape(np.array(p_value),1))
        response.outputs['FFA_Pvalues'].file = str(PvaluePath)


        return response
