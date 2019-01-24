from .wps_raven import RavenProcess
from .wps_gr4j_cemaneige import GR4JCemaNeigeProcess
from .wps_raven_gr4j_cemaneige import RavenGR4JCemaNeigeProcess
from .wps_raven_mohyse import RavenMOHYSEProcess
from .wps_raven_hmets import RavenHMETSProcess
from .wps_raven_hbv_ec import RavenHBVECProcess
from .wps_objective_functions import ObjectiveFunctionProcess
#from .wps_regionalisation import RegionalisationProcess
from .wps_frequency_analysis import FrequencyAnalysisProcess
from .wps_hydro_indicators import HydroIndicatorsProcess
processes = [
    RavenProcess(),
    GR4JCemaNeigeProcess(),
    RavenGR4JCemaNeigeProcess(),
    RavenMOHYSEProcess(),
    RavenHMETSProcess(),
    RavenHBVECProcess(),
    ObjectiveFunctionProcess(),
    FrequencyAnalysisProcess(),
    HydroIndicatorsProcess(),
    # RegionalisationProcess(),
    
]
