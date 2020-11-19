import copy

from abc import ABC, abstractmethod

class TreeEntry():

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class GlobalDataBase(ABC):

    def __init__(self):
        self.strategy_info = []
        self.data_info = []

    def add_strategy_info(self, name, id):
        self.strategy_info.append({'name':name,'id':id})

    def add_data_info(self, tree):
        self.data_info = tree.copy()

    # Called by API
    def get_data_info(self):
        info = {}
        info['strategies'] = self.strategy_info
        def make_dict(te):
            d = {'name':te.name,'id':te.id,'children':[]}
            for c in te.children:
                d['children'].append(make_dict(c))
            return d
        di = []
        for te in self.data_info:
            di.append(make_dict(te))
        info['data'] = di
        return info

    # Called by API
    def get_data(self, strategy_ids, data_id):
        data = self.get_data_for_id(strategy_ids, data_id)

        if data is None:
            raise ValueError('No global data found for ID!')

        type = data['type']
        if type == 'TimeSeries':
            # { 'type' : 'TimeSeries',
            #   'display': ChartDisplay,
            #   'data': OutputMultipleNumericDatasetVal,
            #   'description' : '' }
            display = data['display'].to_dict()
            raw = data['data'].get()
            out = []
            for i in range(len(raw)):
                name = raw[i]['name']
                ts = raw[i]['values']
                values = ts.get()
                for j in range(len(values['dates'])):
                    d = values['dates'][j]
                    values['dates'][j] = d.strftime('%Y-%m-%d')
                out.append({ 'id' : name, 'name' : name, 'data' : values } )
            json = { 'type' : type, 'display' : display, 'data' : out }
            if 'description' in data:
                json['description'] = data['description']
            return json

        if type == 'Radar':
            # { 'type' : 'Radar',
            #   'variables' : [],
            #   'data' : OutputMultipleNumericDatasetVal,
            #   'description' : '' }
            variables = data['variables']
            raw = data['data'].get()
            out = []
            for i in range(len(raw)):
                name = raw[i]['name']
                values = raw[i]['values']
                out.append({ 'id' : name, 'name' : name, 'data' : values } )
            json = { 'type' : type, 'variables' : variables, 'data' : out }
            if 'description' in data:
                json['description'] = data['description']
            return json

        if type == 'Histogram':
            # { 'type' : 'Histogram',
            #   'display' : ChartDisplay,
            #   'intervals' : [],
            #   'data' : OutputMultipleNumericDatasetVal,
            #   'description' : '' }
            display = data['display'].to_dict()
            intervals = data['intervals']
            raw = data['data'].get()
            out = []
            for i in range(len(raw)):
                name = raw[i]['name']
                values = raw[i]['values']
                out.append({ 'id' : name, 'name' : name, 'data' : values } )
            json = { 'type' : type, 'display': display, 'intervals' : intervals, 'data' : out }
            if 'description' in data:
                json['description'] = data['description']
            return json

        if type == 'Doughnut':
            # { 'type' : 'Doughnut',
            #   'variables' : [],
            #   'data' : OutputMultipleNumericDatasetVal,
            #   'description' : '' }
            variables = data['variables']
            raw = data['data'].get()
            out = []
            for i in range(len(raw)):
                name = raw[i]['name']
                values = raw[i]['values']
                out.append({ 'id' : name, 'name' : name, 'data' : values } )
            json = { 'type' : type, 'variables' : variables, 'data' : out }
            if 'description' in data:
                json['description'] = data['description']
            return json

        if type == 'Box':
            # { 'type' : 'Box',
            #   'display' : ChartDisplay,
            #   'variables' : [],
            #   'data' : OutputBoxNumericDatasetVal,
            #   'description' : '' }
            display = data['display'].to_dict()
            variables = data['variables']
            raw = data['data'].get()
            out = []
            for i in range(len(raw)):
                name = raw[i]['name']
                values = raw[i]['values']
                out.append({ 'id' : name, 'name' : name, 'data' : values } )
            json = { 'type' : type, 'display': display, 'variables' : variables, 'data' : out }
            if 'description' in data:
                json['description'] = data['description']
            return json

        raise ValueError('Unknown type!')
