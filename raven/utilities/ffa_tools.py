# -*- coding: utf-8 -*-
"""
Library to perform flood frequency analysis of flood or low flow annual maxima
series (AMS).
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from netCDF4 import Dataset
import pdb

def read_flow_file(file_name,**kwds):
    """
    read_flow_file

    INPUTS:
        file_name -- Name with extension of the file to read

    Extraction of daily streamflow data with their corresponding dates from a
    Excel spreadsheet (.xlsx) or netCDF file (.nc).

    """

    file_type = file_name[0].split('.')[-1]
    if file_type == 'xlsx':  # Excel spreadsheet
        df = pd.read_excel(file_name)
        df['dates'] = pd.to_datetime(df.Year*10000 + df.Month*100 + df.Day,
                                     format='%Y%m%d')

    elif file_type == 'nc':  # netCDF file
        fh = Dataset(file_name[0], more='r')
        matlab_datenums = fh.variables['dates'][:]  # Expecting MATLAB datenums
        Q = fh.variables['Qobs'][:]
        fh.close()
        dates = pd.to_datetime(matlab_datenums-719529, unit='D')
        df = pd.DataFrame({'dates': dates, 'Q': Q})

    return df


def extract_maxima_series(df, time_period='year', extreme_type='high', **kwds):
    """
    extract_AMS

    INPUTS:
        df -- Streamflow (pandas dataframe of [n x 2] with dates and flow)
        time_period -- Time period of to extract the maxima series. Either
                       year, season (W or winter, Sp or spring, Su or summer,
                       A or Autumn) or a selected month (1 (January) to 12
                       (December))
        extreme_type -- Either 'high' for floods or 'low' for low flows

    Extraction of the annual maxima series from a pandas dataframe.
    """
 
    if extreme_type == 'high':  # Flood values
        if str(time_period).lower() == 'year':
            Qx = df.resample('Y', on='dates').agg({'Q': 'max'})['Q']

        elif str(time_period).lower() == 'winter' or \
                str(time_period).upper() == 'W':
            trimester_max = df.resample('QS-Dec', on='dates').\
                                agg({'Q': 'max'})['Q']
            Qx = trimester_max.iloc[0::4]
        elif str(time_period).lower() == 'spring' or \
                str(time_period).upper() == 'SP':
            trimester_max = df.resample('QS-Dec', on='dates').\
                                agg({'Q': 'max'})['Q']
            Qx = trimester_max.iloc[1::4]
        elif str(time_period).lower() == 'summer' or \
                str(time_period).upper() == 'SU':
            trimester_max = df.resample('QS-Dec', on='dates').\
                                agg({'Q': 'max'})['Q']
            Qx = trimester_max.iloc[2::4]
        elif str(time_period).lower() == 'autumn' or \
                str(time_period).upper() == 'A':
            trimester_max = df.resample('QS-Dec', on='dates').\
                                agg({'Q': 'max'})['Q']
            Qx = trimester_max.iloc[3::4]
        elif list(map(int, time_period))[0] in range(1, 13):  # Selected month
            month_max = df.resample('M', on='dates').agg({'Q': 'max'})['Q']
            Qx = month_max.iloc[list(map(int, time_period))[0]-1::12]
        else:
            e = 'Time period {} is not supported for the flood frequency \
                analysis. See help for accepted format.' \
                .format(str(time_period))
            raise ValueError(e)

        return Qx

    elif extreme_type == 'low':  # Low flow values
        if str(time_period).lower() == 'year':
            Qn = df.resample('Y', on='dates').agg({'Q': 'min'})['Q']

        elif str(time_period).lower() == 'winter' or \
                str(time_period).upper() == 'W':
            trimester_max = df.resample('QS-Dec', on='dates').\
                                agg({'Q': 'min'})['Q']
            Qn = trimester_max.iloc[0::4]
        elif str(time_period).lower() == 'spring' or \
                str(time_period).upper() == 'SP':
            trimester_max = df.resample('QS-Dec', on='dates').\
                                agg({'Q': 'min'})['Q']
            Qn = trimester_max.iloc[1::4]
        elif str(time_period).lower() == 'summer' or \
                str(time_period).upper() == 'SU':
            trimester_max = df.resample('QS-Dec', on='dates').\
                                agg({'Q': 'min'})['Q']
            Qn = trimester_max.iloc[2::4]
        elif str(time_period).lower() == 'autumn' or \
                str(time_period).upper() == 'A':
            trimester_max = df.resample('QS-Dec', on='dates').\
                                agg({'Q': 'min'})['Q']
            Qn = trimester_max.iloc[3::4]
        elif list(map(int, time_period))[0] in range(1, 13):  # Selected month
            month_max = df.resample('M', on='dates').agg({'Q': 'min'})['Q']
            Qn = month_max.iloc[list(map(int, time_period))[0]-1::12]
        else:
            e = 'Time period {} is not supported for the flood frequency \
                analysis. See help for accepted format.'.format(time_period)
            raise ValueError(e)

        return Qn

    else:
        e = 'Extreme type {} is not supported for the flood frequency \
            analysis.'.format(extreme_type)
        raise ValueError(e)


def flood_frequency_analysis(data,dist='genextreme',extreme_type='high',T=20,**kwds):
    """
    flood_frequency_analysis

    INPUTS:
        data -- Streamflow maxima series used for the flood frequency analysis
        dist -- Statistical distribution for the ffa. Default is Gumbel
        T -- Array or single value of the desired return period to extract

    Flood frequency analysis (FFA) of the steamflow maxima time series. In this
    version, only the Gamma ('gamma'), GEV ('genextreme'), Gumbel ('gumbel_r'),
    Log-normal ('lognorm') and Pearson-III ('pearson3') distributions are made
    available for the FFA.
    """
  
    if extreme_type == 'high':
        p = 1 - 1 / T  # Probability of non-occurence for floods
    elif extreme_type == 'low':
        p = 1 / T  # Probability of non-occurence for low flows
    else:
        e = 'Extreme type {} is not supported for the flood frequency \
            analysis.'.format(extreme_type)
        raise ValueError(e)

    supported_dist = ['gamma',
                      'genextreme',
                      'gumbel_r',
                      'lognorm',
                      'pearson3']

    # Get the distribution object
    dist_obj = getattr(stats, dist.lower(), None)
    if dist not in supported_dist or dist_obj is None:
        e = "Statistical distribution {} is not in not supported for the \
            flood frequency analysis.".format(dist)
        raise ValueError(e)

    
    parmhat = dist_obj.fit(data)  # Fit the statistical distribution parameters
    
    # Extract p_Value
    _, p_value=stats.kstest(data,dist,args=parmhat)
    
    
    if len(parmhat) == 2:  # 2-parameter distribution
        X = dist_obj.ppf(p, loc=parmhat[0], scale=parmhat[1])
    else:  # Expecting a 3-parameter distribution
        X = dist_obj.ppf(p, parmhat[0], loc=parmhat[1], scale=parmhat[2])

    return X, p_value