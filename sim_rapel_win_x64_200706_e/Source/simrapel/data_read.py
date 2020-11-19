import datetime as dt
import os

import core.scenario.scenario_base as sb

from data_io import read_magic_time_series, read_modflow_time_series, read_modflow_time_series_column, read_modflow_cube, read_magic_project_summary, read_swat_all, read_modflow_cube_dates_io

# DATA HELPER FUNCTIONS

def generate_box_dataset(ts):
    data = ts.values.copy()
    data.sort()

    def compute_median(lst):
        even = len(lst) % 2 == 0
        if even:
            mid_index = int(len(lst) / 2)
            median = (lst[mid_index-1] + lst[mid_index]) / 2
        else:
            mid_index = int((len(lst) - 1) / 2)
            median = lst[mid_index]
        return median

    median = compute_median(data)

    def compute_quartiles(lst, median):
        even = len(lst) % 2 == 0
        if even:
            mid_index = int(len(data) / 2)
            lower_half = data[:mid_index]
            upper_half = data[mid_index:]
        else:
            mid_index = int((len(data) - 1) / 2)
            lower_half = data[:mid_index]
            upper_half = data[mid_index+1:]
        q1 = compute_median(lower_half)
        q3 = compute_median(upper_half)
        return q1, q3

    q1, q3 = compute_quartiles(data, median)

    iqr = q3 - q1
    lower_fence = q1 - (1.5 * iqr)
    upper_fence = q3 + (1.5 * iqr)

    lower_outliers = []
    upper_outliers = []

    whiskerMin = 1.0e18
    whiskerMax = -1.0e18

    min = 1.0e18
    max = -1.0e18

    for i in range(len(data)):
        v = data[i]
        is_outlier = False
        if v < lower_fence:
            lower_outliers.append(v)
            is_outlier = True
        if v > upper_fence:
            upper_outliers.append(v)
            is_outlier = True
        if not is_outlier:
            if v > whiskerMax:
                whiskerMax = v
            if v < whiskerMin:
                whiskerMin = v
        if v > max:
            max = v
        if v < min:
            min = v

    outliers = lower_outliers + upper_outliers

    return sb.BoxNumericDatasetVal(min, whiskerMin, q1, median, q3, whiskerMax, max, outliers)

def compute_time_series_average(ts):
    total = 0
    sum = 0.0
    for i in range(len(ts.values)):
        total += 1
        sum += ts.values[i]
    if total > 1:
        return sum / total
    else:
        return 0

# READ DATA FROM FILE

def add_month(date):
    year = date.year
    month = date.month
    month = month + 1
    if month > 12:
        year = year + 1
        month = 1
    return dt.datetime(year, month, date.day)

def read_magic_timeseries(dir, id, varname, scale_factor=1.0):
    fn = os.path.join(dir, 'magic', id[:2], id + '.txt')
    # Results do not exist for all Reservoirs (EM) or Nodes (NO) or HydroPower (CH)
    if not os.path.exists(fn) and (id[:2] == 'EM' or id[:2] == 'NO' or id[:2] == 'CH'):
        return None
    values = read_magic_time_series(fn, varname)
    dates = []
    date = dt.datetime(2017, 4, 1)
    for i in range(len(values)):
        dates.append(date)
        date = add_month(date)
        values[i] = values[i] * scale_factor
    return sb.TimseriesBaseVal(dates, values)

def read_magic_summary(dir, id):
    if id[:2] == 'ZR':
        fn = os.path.join(dir, 'magic', 'Bal_ZR.txt')
    else:
        fn = os.path.join(dir, 'magic', 'Caudales.txt')
    return read_magic_project_summary(fn, id)

def read_all_swat_timeseries(dir):
    fn_sub = os.path.join(dir, 'swat', 'output.sub')
    fn_rch = os.path.join(dir, 'swat', 'output.rch')
    ts_sub = read_swat_all(fn_sub, 'SUB')
    ts_rch = read_swat_all(fn_rch, 'RCH')
    ts = {**ts_sub, **ts_rch} 
    dates = []
    date = dt.datetime(2017, 1, 1)
    name = list(ts)[0]
    id = list(ts[name])[0]
    for v in ts[name][id]:
        dates.append(date)
        date = add_month(date)
    return dates, ts

def read_modflow_global_balance_timeseries(dir, aquifer, varname):
    start_date = dt.datetime(2017, 1, 1)
    fn = os.path.join(dir, 'modflow', aquifer, 'GWBalance.TXT')
    dates, values = read_modflow_time_series(fn, varname)
    for i in range(len(values)):
        dates[i] = start_date + dt.timedelta(days=dates[i])
        values[i] = values[i] / 86400 # m3/d to m3/s
    return sb.TimseriesBaseVal(dates, values)

def read_modflow_balance_timeseries(dir, id, varname):
    start_date = dt.datetime(2017, 1, 1)
    fn = dir + '/modflow/'
    cachapoal_dir = ['AC-01','AC-02','AC-03','AC-04','AC-06','AC-07']
    alhue_dir = ['AC-08', 'AC-09', 'AC-10']
    tinguiririca_dir = ['AC-11','AC-12','AC-13','AC-14','AC-15','AC-16','AC-17']
    if id in cachapoal_dir:
        fn = fn + 'cachapoal'
    if id in alhue_dir:
        fn = fn + 'alhue'
    if id in tinguiririca_dir:
        fn = fn + 'tinguiririca'
    fn = fn + '/GWBalAC-' + id[-2:] + '.TXT'
    dates, values = read_modflow_time_series(fn, varname)
    for i in range(len(values)):
        dates[i] = start_date + dt.timedelta(days=dates[i])
        values[i] = values[i] / 86400 # m3/d to m3/s
    return sb.TimseriesBaseVal(dates, values)

def read_modflow_timeseries(dir, id, aquifer, model):
    start_date = dt.datetime(2017, 1, 1)
    fn = dir + '/modflow/' + aquifer
    if model == 'head':
        fn = fn + '/GWHeads.TXT'
    if model == 'drawdown':
        fn = fn + '/GWDrwdwns.TXT'
    varname = id
    if aquifer == 'alhue':
        varname = varname + '/AInterpolated'
    if aquifer == 'cachapoal' or aquifer == 'tinguiririca':
        varname = varname + '/1Interpolated'
    dates, values = read_modflow_time_series_column(fn, varname)
    for i in range(len(values)):
        dates[i] = start_date + dt.timedelta(days=dates[i])
        values[i] = values[i]
    return sb.TimseriesBaseVal(dates, values)

def read_modflow_cube_dates(dir):
    fn = os.path.join(dir, 'CUBE_DATES.txt')
    return read_modflow_cube_dates_io(fn)
