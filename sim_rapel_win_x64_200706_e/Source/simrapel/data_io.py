import io
import struct

# COMMON CSV

def get_non_empty_cols(line, delim_char):
    all_cols = line[:-1].split(delim_char)
    cols = []
    for c in all_cols:
        if c != '':
            cols.append(c.strip())
    return cols

def index_for_name(header, column_name, delim_char):
    cols = get_non_empty_cols(header, delim_char)
    return cols.index(column_name)

def read_time_series(fn, column_name, delim_char, data_start_row, data_column_offset=0):
    fo = open(fn, 'r')
    lines = fo.readlines()
    fo.close()
    header = lines[0]
    data_column_index = index_for_name(header, column_name, delim_char)
    values = []
    for i in range(data_start_row, len(lines)):
        l = lines[i]
        cols = get_non_empty_cols(l, delim_char)
        if len(cols) == 0: # Handle empty lines within data rows
            continue
        val = float(cols[data_column_index + data_column_offset])
        values.append(val)
    return values

# READ MAGIC TEXT FILES

def read_magic_time_series(fn, column_name):
    return read_time_series(fn, column_name, ' ', 3)

# READ SWAT TEXT FILES (ALL IN ONE READ FOR SPEED)

def read_swat_all(fn, type):
    key_column_index = 1
    data_start_column_index = 5
    fi = open(fn, 'r')
    lines = fi.readlines();
    fi.close()
    timeseries = {}
    header = lines[0].split('\t')
    head_to_index_lookup = {}
    if type == 'SUB':
        for i in range(data_start_column_index, len(header) - 1):
            name = header[i].strip()
            timeseries[name] = {}
            head_to_index_lookup[name] = i
    else:
        for i in range(data_start_column_index, len(header)):
            name = header[i].strip()
            if name.endswith('\n'):
                name = name[:-1]
            timeseries[name] = {}
            head_to_index_lookup[name] = i
    for i in range(1, len(lines)):
        line = lines[i]
        parts = line.split('\t')
        id = parts[key_column_index]
        for name in timeseries:
            index = head_to_index_lookup[name]
            if id not in timeseries[name]:
                timeseries[name][id] = []
            value = float(parts[index])
            timeseries[name][id].append(value)
    return timeseries

# READ MAGIC SUMMARY TEXT FILES

def read_magic_project_summary(fn, name):
    fi = open(fn, 'r')
    lines = fi.readlines()
    fi.close()
    pos_data = []
    neg_data = []
    for m in range(12):
        pos_data.append(0)
        neg_data.append(0)
    for i in range(len(lines)):
        if i > 2: # Ignore header lines
            line = lines[i]
            if line != '\n':
                parts = line.split(' ')
                if parts[0] == name:
                    real_parts = []
                    for p in parts:
                        if p != '' and p != '\n':
                            real_parts.append(p)
                    if len(real_parts) != 16:
                        raise ValueError('ERROR PARSING FILE')
                    offset = 4
                    for m in range(12):
                        v = float(real_parts[m+offset])
                        if v >= 0:
                            pos_data[m] = pos_data[m] + v
                        else:
                            neg_data[m] = neg_data[m] + v
    return pos_data, neg_data

# READ MODFLOW TEXT FILES

def read_modflow_time_series(fn, name):
    fi = open(fn, 'r')
    all = fi.readlines()
    fi.close()
    times = []
    values = []
    ln = 0
    capture=False
    while ln < len(all):
        line = all[ln]
        if line.startswith(name):
            capture = True
            ln += 2
            line = all[ln]
        if line == '\n' and capture:
            capture = False
            break
        if capture:
            parts = line.split('\t')
            time = int(parts[0])
            value = float(parts[1][0:-1])
            times.append(time)
            values.append(value)
        ln += 1
    return (times, values)

def read_modflow_time_series_column(fn, name, null_value=-9999.0):
    fi = open(fn, 'r')
    all = fi.readlines()
    fi.close()
    header = all[0]
    all = all[1:]
    column_names = header.split('\t')
    column_index = -1
    for ci in range(len(column_names)):
        if column_names[ci] == name:
            column_index = ci
            break
    if column_index == -1:
        raise ValueError('Column name not found in file!')
    times = []
    values = []
    for r in range(len(all)):
        line = all[r]
        parts = line.split('\t')
        time = float(parts[0])# first one is not an int for some reason
        if parts[column_index] == 'none':
            value = null_value
        else:
            value = float(parts[column_index])
        times.append(time)
        values.append(value)
    return (times, values)

# READ MODFLOW BINARY CUBE

def read_modflow_cube(fn):
    fi = open(fn, 'br')
    bnrecords = fi.read(4)
    nrecords = struct.unpack('i', bnrecords)[0]
    data = {}
    for i in range(nrecords):
        brow = fi.read(4)
        row = struct.unpack('i', brow)[0]
        bcol = fi.read(4)
        col = struct.unpack('i', bcol)[0]
        index = (row,col)
        data[index] = []
        for j in range(152):
            bf = fi.read(4)
            f = struct.unpack('f', bf)[0]
            data[index].append(f)
    fi.close()
    return data

def read_modflow_cube_dates_io(fn):
    fi = open(fn, 'r')
    start = dt.datetime(2017, 1, 1)
    dates = []
    for i in range(152):
        line = fi.readline()
        if line[-1] == '\n':
            line = line[0:-1]
        num_days = int(float(line))
        date = start + dt.timedelta(days=num_days)
        dates.append(date)
    fi.close()
    return dates