"""
Python script 'process_NCEI_05.py'
by Matthew Garcia, PhD student
Dept. of Forest and Wildlife Ecology
University of Wisconsin - Madison
matt.e.garcia@gmail.com

Copyright (C) 2015-2016 by Matthew Garcia
Licensed Gnu GPL v3; see 'LICENSE_GnuGPLv3.txt' for complete terms
Send questions, bug reports, any related requests to matt.e.garcia@gmail.com
See also 'README.md', 'DISCLAIMER.txt', 'CITATION.txt', 'ACKNOWLEDGEMENTS.txt'
Treat others as you would be treated. Pay it forward. Valar dohaeris.

PURPOSE: Summarizing several T/P seasonal and cold/warm gridded season
         statistics, grid-mean annual time series (and their statistics),
         and cross-indicator/season correlations and their p-values, including
         autumn-to-winter (to close the annual cycle of potential season-to-
         season correlations)

DEPENDENCIES: h5py, numpy, scipy.stats
              'Date_Convert' module has no external requirements

USAGE: '$ python process_NCEI_05.py 1984 2013 ./analyses'

INPUT: '.h5' output file from process_NCEI_04b.py
       (with the naming convention
        'analyses/[YYYY]-[YYYY]_derived_clim_grids.h5')

OUTPUT: Several '.csv' files with aggregated seasonal statistics
        (with the naming convention
         'analyses/[YYYY]-[YYYY]_[XXXX]_season[al]_stats.csv')
"""


import sys
import datetime
import glob
import h5py as hdf
import numpy as np
from scipy.stats import linregress, pearsonr


def message(char_string):
    """
    prints a string to the terminal and flushes the buffer
    """
    print char_string
    sys.stdout.flush()
    return


def getgridstats(grid):
    sts = np.zeros((4))
    sts[0] = np.mean(grid)
    sts[1] = np.std(grid)
    sts[2] = np.min(grid)
    sts[3] = np.max(grid)
    return sts


def getstats(grid_mean):
    nyrs = len(grid_mean)
    sts = np.zeros((9))
    sts[0] = np.mean(grid_mean)
    sts[1] = np.std(grid_mean)
    sts[2] = np.min(grid_mean)
    sts[3] = np.max(grid_mean)
    xvals = np.arange(0, nyrs)
    sts[4:9] = linregress(xvals, grid_mean)
    return sts


message(' ')
message('process_NCEI_05.py started at %s' %
        datetime.datetime.now().isoformat())
message(' ')
#
if len(sys.argv) < 4:
    message('input warning: no input directory indicated, using ./analyses')
    path = './analyses'
else:
    path = sys.argv[3]
#
if len(sys.argv) < 3:
    year_begin = 1984
    year_end = 2013
else:
    year_begin = int(sys.argv[1])
    year_end = int(sys.argv[2])
doy_begin = 1
doy_end = 365
#
years = np.arange(year_begin, year_end + 1).astype(int)
nyears = len(years)
doys = np.arange(doy_begin, doy_end + 1).astype(int)
ndoys = len(doys)
#
infile = ''
fnames = glob.glob('%s/*_derived_clim_grids.h5' % path)
for fname in fnames:
    if (str(year_begin) in fname) or (str(year_end) in fname):
        infile = fname
        break
if infile == '':
    message('required derived climatological grids file for %d-%d not found' %
            (year_begin, year_end))
    message('stopping')
    sys.exit(1)
parts = infile.split('/')
f_year_begin = int(parts[-1][0:4])
f_year_end = int(parts[-1][5:9])
ybegin = year_begin - f_year_begin
yend = f_year_end - year_end
ny = f_year_end - f_year_begin + 1
#
inputgridvars = ['grids_tmin_90d_avg_at_veq',
                 'grids_tmin_90d_var_at_veq',
                 'grids_tmin_90d_avg_at_ssol',
                 'grids_tmin_90d_var_at_ssol',
                 'grids_tmin_90d_avg_at_aeq',
                 'grids_tmin_90d_var_at_aeq',
                 'grids_tmin_90d_avg_at_wsol',
                 'grids_tmin_90d_var_at_wsol',
                 'grids_tmax_90d_avg_at_veq',
                 'grids_tmax_90d_var_at_veq',
                 'grids_tmax_90d_avg_at_ssol',
                 'grids_tmax_90d_var_at_ssol',
                 'grids_tmax_90d_avg_at_aeq',
                 'grids_tmax_90d_var_at_aeq',
                 'grids_tmax_90d_avg_at_wsol',
                 'grids_tmax_90d_var_at_wsol',
                 'grids_tavg_90d_avg_at_veq',
                 'grids_tavg_90d_var_at_veq',
                 'grids_tavg_90d_avg_at_ssol',
                 'grids_tavg_90d_var_at_ssol',
                 'grids_tavg_90d_avg_at_aeq',
                 'grids_tavg_90d_var_at_aeq',
                 'grids_tavg_90d_avg_at_wsol',
                 'grids_tavg_90d_var_at_wsol',
                 'grids_prcp_90d_sum_at_veq',
                 'grids_prcp_90d_nd0_sum_at_veq',
                 'grids_prcp_90d_sum_at_ssol',
                 'grids_prcp_90d_nd0_sum_at_ssol',
                 'grids_prcp_90d_sum_at_aeq',
                 'grids_prcp_90d_nd0_sum_at_aeq',
                 'grids_prcp_90d_sum_at_wsol',
                 'grids_prcp_90d_nd0_sum_at_wsol',
                 'grids_prcp_365d_at_eoy',
                 'grids_intensity_winter',
                 'grids_doy_last_spring_tmin_frz',
                 'grids_chill_d_at_ssol',
                 'grids_tmin_frz_days_at_ssol',
                 'grids_doy_first_autumn_tmin_frz',
                 'grids_frost_free_season_days',
                 'grids_gdd_last_spring_tmin_frz',
                 'grids_doy_plateau_begin',
                 'grids_gdd_plateau_begin',
                 'grids_doy_plateau_end',
                 'grids_gdd_plateau_end',
                 'grids_days_plateau_length',
                 'grids_gdd_plateau_length',
                 'grids_intensity_plateau']
ninputgridvars = len(inputgridvars)
#
message('getting seasonal grids from %s' % infile)
with hdf.File(infile, 'r') as h5infile:
    nrows = np.copy(h5infile['grid/nrows'])
    ncols = np.copy(h5infile['grid/ncols'])
    seasonal_grids = np.zeros((ninputgridvars, nyears, nrows, ncols))
    for i, inputgridvar in enumerate(inputgridvars):
        message('- %s' % inputgridvar)
        tmpvar = np.copy(h5infile[inputgridvar])
        seasonal_grids[i, :, :, :] = tmpvar[ybegin:(ny - yend), :, :]
message(' ')
#
message('calculating annual average T grids')
tavg_annual_avg_grids = np.zeros((nyears, nrows, ncols))
for j in range(nyears):
    tavg_annual_avg_grids[j, :, :] = \
        (seasonal_grids[16, j, :, :] + seasonal_grids[18, j, :, :] +
         seasonal_grids[20, j, :, :] + seasonal_grids[22, j, :, :]) / 4.0
#
tmin_seasonal = np.zeros((nyears, 32))
tmax_seasonal = np.zeros((nyears, 32))
tavg_seasonal = np.zeros((nyears, 36))
prcp_seasonal = np.zeros((nyears, 36))
cold_season = np.zeros((nyears, 28))
warm_season = np.zeros((nyears, 28))
message('calculating other annual average grids')
for j in range(nyears):
    for i in range(8):
        idx1 = 4 * i
        idx2 = idx1 + 4
        tmin_seasonal[j, idx1:idx2] = getgridstats(seasonal_grids[i, j, :, :])
    for i in range(8, 16):
        idx1 = 4 * (i - 8)
        idx2 = idx1 + 4
        tmax_seasonal[j, idx1:idx2] = getgridstats(seasonal_grids[i, j, :, :])
    for i in range(16, 24):
        idx1 = 4 * (i - 16)
        idx2 = idx1 + 4
        tavg_seasonal[j, idx1:idx2] = getgridstats(seasonal_grids[i, j, :, :])
    tavg_seasonal[j, 32:36] = getgridstats(tavg_annual_avg_grids[j, :, :])
    for i in range(24, 33):
        idx1 = 4 * (i - 24)
        idx2 = idx1 + 4
        prcp_seasonal[j, idx1:idx2] = getgridstats(seasonal_grids[i, j, :, :])
    for i in range(33, 40):
        idx1 = 4 * (i - 33)
        idx2 = idx1 + 4
        cold_season[j, idx1:idx2] = getgridstats(seasonal_grids[i, j, :, :])
    for i in range(40, 47):
        idx1 = 4 * (i - 40)
        idx2 = idx1 + 4
        warm_season[j, idx1:idx2] = getgridstats(seasonal_grids[i, j, :, :])
#
# write seasonal variables to csv files
fname = '%s/%d-%d_tmin_seasonal_stats.csv' % (path, year_begin, year_end)
np.savetxt(fname, tmin_seasonal, delimiter=',')
message('wrote %s' % fname)
fname = '%s/%d-%d_tmax_seasonal_stats.csv' % (path, year_begin, year_end)
np.savetxt(fname, tmax_seasonal, delimiter=',')
message('wrote %s' % fname)
fname = '%s/%d-%d_tavg_seasonal_stats.csv' % (path, year_begin, year_end)
np.savetxt(fname, tavg_seasonal, delimiter=',')
message('wrote %s' % fname)
fname = '%s/%d-%d_prcp_seasonal_stats.csv' % (path, year_begin, year_end)
np.savetxt(fname, prcp_seasonal, delimiter=',')
message('wrote %s' % fname)
fname = '%s/%d-%d_cold_season_stats.csv' % (path, year_begin, year_end)
np.savetxt(fname, cold_season, delimiter=',')
message('wrote %s' % fname)
fname = '%s/%d-%d_warm_season_stats.csv' % (path, year_begin, year_end)
np.savetxt(fname, warm_season, delimiter=',')
message('wrote %s' % fname)
#
# get grid-mean time series
nvars = ninputgridvars + 1
allts = np.zeros((nvars, nyears))
for i in range(8):
    allts[i, :] = tmin_seasonal[:, 4 * i]
for i in range(8, 16):
    ii = i - 8
    allts[i, :] = tmax_seasonal[:, 4 * ii]
for i in range(16, 25):
    ii = i - 16
    allts[i, :] = tavg_seasonal[:, 4 * ii]
for i in range(25, 34):
    ii = i - 25
    allts[i, :] = prcp_seasonal[:, 4 * ii]
for i in range(34, 41):
    ii = i - 34
    allts[i, :] = cold_season[:, 4 * ii]
for i in range(41, 48):
    ii = i - 41
    allts[i, :] = warm_season[:, 4 * ii]
#
# write time series to csv file
fname = '%s/%d-%d_overall_timeseries.csv' % (path, year_begin, year_end)
np.savetxt(fname, allts, delimiter=',')
message('wrote %s' % fname)
#
# get full-record stats, including trends
allstats = np.zeros((nvars, 9))
for i in range(nvars):
    allstats[i, :] = getstats(allts[i, :])
#
# write statistics to csv file
# statistics order: [mean  std  min  max  slope  intercept  corr  sig  stderr]
fname = '%s/%d-%d_overall_stats.csv' % (path, year_begin, year_end)
np.savetxt(fname, allstats, delimiter=',')
message('wrote %s' % fname)
#
# get cross-indicator correlations and significance values
correl_matrix = np.zeros((nvars, nvars))
sig_matrix = np.zeros((nvars, nvars))
for j in range(nvars):
    for i in range(j, nvars):
        if i == j:
            correl_matrix[j, i] = 1.0
        else:
            corr, sig = pearsonr(allts[j, :], allts[i, :])
            correl_matrix[j, i] = corr
            sig_matrix[j, i] = sig
#
# write time series correlations and significance values to csv files
fname = '%s/%d-%d_overall_timeseries_correl.csv' % \
    (path, year_begin, year_end)
np.savetxt(fname, correl_matrix, delimiter=',')
message('wrote %s' % fname)
fname = '%s/%d-%d_overall_timeseries_corrsig.csv' % \
    (path, year_begin, year_end)
np.savetxt(fname, sig_matrix, delimiter=',')
message('wrote %s' % fname)
#
# get autumn-to-winter cross-indicator correlations and significance values
awvars = 6
awts = np.zeros((awvars, nyears - 1))
awts[0, :] = allts[22, :nyears - 1]  # autumn temperature
awts[1, :] = allts[16, 1:nyears]   # next winter temperature
awts[2, :] = allts[31, :nyears - 1]  # autumn precip
awts[3, :] = allts[32, :nyears - 1]  # autumn precip days
awts[4, :] = allts[25, 1:nyears]   # next winter precip
awts[5, :] = allts[26, 1:nyears]   # next winter precip days
correl_matrix = np.zeros((awvars, awvars))
sig_matrix = np.zeros((awvars, awvars))
for j in range(awvars):
    for i in range(j, awvars):
        if i == j:
            correl_matrix[j, i] = 1.0
        else:
            corr, sig = pearsonr(awts[j, :], awts[i, :])
            correl_matrix[j, i] = corr
            sig_matrix[j, i] = sig
fname = '%s/%d-%d_autumn-to-winter_timeseries_correl.csv' % \
    (path, year_begin, year_end)
np.savetxt(fname, correl_matrix, delimiter=',')
message('wrote %s' % fname)
fname = '%s/%d-%d_autumn-to-winter_timeseries_corrsig.csv' % \
    (path, year_begin, year_end)
np.savetxt(fname, sig_matrix, delimiter=',')
message('wrote %s' % fname)
#
message(' ')
message('process_NCEI_05.py completed at %s' %
        datetime.datetime.now().isoformat())
message(' ')
sys.exit(0)

# end process_NCEI_05.py
