#########################################################################                                  
:FileType          rvp ASCII Raven 2.8.2                                                                              
:WrittenBy         Juliane Mai & James Craig                                                                             
:CreationDate      Sep 2018
#
# Emulation of MOHYSE simulation of Salmon River near Prince George                                                             
#------------------------------------------------------------------------

#-----------------------------------------------------------------
# Raven Properties file Template. Created by Raven v2.8.1 w/ netCDF
#-----------------------------------------------------------------
# all expressions of format *xxx* need to be specified by the user 
# all parameter values of format ** need to be specified by the user 
# soil, land use, and vegetation classes should be made consistent with user-generated .rvh file 
#-----------------------------------------------------------------

#-----------------------------------------------------------------
# Soil Classes
#-----------------------------------------------------------------
:SoilClasses
  :Attributes,
  :Units,
  TOPSOIL
  GWSOIL 
:EndSoilClasses

#-----------------------------------------------------------------
# Land Use Classes
#-----------------------------------------------------------------
:LandUseClasses, 
  :Attributes,        IMPERM,    FOREST_COV, 
  :Units,             frac,      frac, 
  LU_ALL,             0.0,       1.0          
:EndLandUseClasses

#-----------------------------------------------------------------
# Vegetation Classes
#-----------------------------------------------------------------
:VegetationClasses, 
  :Attributes,        MAX_HT,       MAX_LAI,    MAX_LEAF_COND, 
  :Units,             m,            none,       mm_per_s, 
 VEG_ALL,             0.0,          0.0,        0.0         
:EndVegetationClasses

#-----------------------------------------------------------------
# Soil Profiles
#-----------------------------------------------------------------
:SoilProfiles
         LAKE, 0
         ROCK, 0
       # DEFAULT_P,      2, TOPSOIL, MOHYSE_PARA_5, GWSOIL, 10.0
         DEFAULT_P,      2, TOPSOIL,       par_x05, GWSOIL, 10.0
:EndSoilProfiles

#-----------------------------------------------------------------
# Global Parameters
#-----------------------------------------------------------------
#:GlobalParameter      RAINSNOW_TEMP              -2.0           
:GlobalParameter       TOC_MULTIPLIER              1.0           
# :GlobalParameter     MOHYSE_PET_COEFF  MOHYSE_PARA_1        
:GlobalParameter       MOHYSE_PET_COEFF        par_x01 

#-----------------------------------------------------------------
# Soil Parameters
#-----------------------------------------------------------------
:SoilParameterList
  :Parameters,        POROSITY,  PET_CORRECTION,        HBV_BETA,  BASEFLOW_COEFF,      PERC_COEFF, 
       :Units,               -,               -,               -,             1/d,             1/d, # (units not generated by .rvp template)
    # TOPSOIL,            1.0 ,             1.0,             1.0,   MOHYSE_PARA_7,   MOHYSE_PARA_6,
    #  GWSOIL,            1.0 ,             1.0,             1.0,   MOHYSE_PARA_8,             0.0,
      TOPSOIL,            1.0 ,             1.0,             1.0,         par_x07,         par_x06,
       GWSOIL,            1.0 ,             1.0,             1.0,         par_x08,             0.0,
:EndSoilParameterList

#-----------------------------------------------------------------
# Land Use Parameters
#-----------------------------------------------------------------
:LandUseParameterList
  :Parameters,     MELT_FACTOR,       AET_COEFF, FOREST_SPARSENESS, DD_MELT_TEMP,
       :Units,          mm/d/K,            mm/d,                 -,         degC,
  # [DEFAULT],   MOHYSE_PARA_3,   MOHYSE_PARA_2,               0.0,MOHYSE_PARA_4, 
    [DEFAULT],         par_x03,         par_x02,               0.0,      par_x04,
:EndLandUseParameterList

#-----------------------------------------------------------------
# Vegetation Parameters
#-----------------------------------------------------------------
:VegetationParameterList
  :Parameters,    SAI_HT_RATIO,  RAIN_ICEPT_PCT,  SNOW_ICEPT_PCT, 
       :Units,               -,               -,               -, 
    [DEFAULT],             0.0,             0.0,             0.0,   
:EndVegetationParameterList
