import core.scenario.scenario_base as sb

import os
import datetime as dt
import numpy as np

import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import pickle

from data_read import generate_box_dataset, read_magic_timeseries, read_magic_summary, read_all_swat_timeseries, \
    read_modflow_global_balance_timeseries, read_modflow_balance_timeseries, read_modflow_timeseries, read_modflow_cube_dates

class Scenario(sb.ScenarioBase):

    def dispose(self):
        pass

    def path_for_resource(self, resource):
        return os.path.join(self.static_dir, resource)

    def init_file_system(self, working_dir):
        scenario_dir = os.path.abspath(os.path.dirname(__file__))
        self.static_dir = os.path.join(scenario_dir, 'static')
        self.layer_dir = os.path.join(scenario_dir, 'layers')
        self.data_dir = os.path.join(scenario_dir, 'data')
        self.working_dir = working_dir

    def __init__(self, working_dir):
        self.init_file_system(working_dir)
        self._define_temporal_characteristics()
        self.set_run_status(0, 'Cargando resultados...')
        self._define_inputs()
        self._define_outputs()
        self._define_static_shapefiles()
        self._define_strategy_geotiff_layers()
        self._define_static_shapefiles_with_layer_data()
        
    def _define_temporal_characteristics(self):
        start = dt.datetime(1979,4,1)
        end = dt.datetime(2017,3,1)
        timestep = sb.TimeStep.Parse('Annual')
        multi_step = True
        super().__init__(start, end, timestep, multi_step)

    def _define_inputs(self):
        # Groups
        input_group_0_id = 'input_group_0'
        input_group_0a_id = 'input_group_0_subgroup_a'
        super().add_group(sb.GroupDef(input_group_0_id,'Series Hidrológicas',None),True)
        super().add_group(sb.GroupDef(input_group_0a_id,'Series Hidrológicas',input_group_0_id,os.path.join(self.static_dir,'html/input/group_0.html')),True)

        input_group_1_id = 'input_group_1'
        input_group_1a_id = 'input_group_1_subgroup_a'
        input_group_1b_id = 'input_group_1_subgroup_b'
        input_group_1c_id = 'input_group_1_subgroup_c'
        super().add_group(sb.GroupDef(input_group_1_id,'Estrategias hidricas',None),True)
        super().add_group(sb.GroupDef(input_group_1a_id,'Mejora eficiencia de riego a nivel cuenca',input_group_1_id,os.path.join(self.static_dir,'html/input/group_1a.html')),True)
        super().add_group(sb.GroupDef(input_group_1b_id,'Construcción Embalses Bollenar y Cayanas',input_group_1_id,os.path.join(self.static_dir,'html/input/group_1b.html')),True)
        super().add_group(sb.GroupDef(input_group_1c_id,'Implementar Recarga de Acuíferos Gestionada (RAG)',input_group_1_id,os.path.join(self.static_dir,'html/input/group_1c.html')),True)

        # Controls
        hydro_options = ['Hidrología Histórica (1979-2016)',            # HYDRO-OBS
                         'Tendencia Climática (-20% PREC, +2.5°C)']     # HYDRO-PRJ
        super().add_input(sb.InputSingleSelectionDef('input_0','',input_group_0a_id,hydro_options,hydro_options[0]))

        super().add_input(sb.InputBooleanDef('input_1a_1','',input_group_1a_id,False)) # IIE

        reservoir_options = ['No Embalses',
                             'Embalses Bollenar, Las Cayanas y Claro']
        super().add_input(sb.InputSingleSelectionDef('input_1b_1','',input_group_1b_id,reservoir_options,reservoir_options[0]))

        super().add_input(sb.InputBooleanDef('input_1c_1','',input_group_1c_id,False))

    def _define_outputs(self):
        # Groups
        output_group_0_id = 'output_group_0'
        super().add_group(sb.GroupDef(output_group_0_id,'Tramos de río',None),False)
        
        output_group_1_id = 'output_group_1'
        super().add_group(sb.GroupDef(output_group_1_id,'Acuífero Alhué',None),False)
        
        output_group_2_id = 'output_group_2'
        super().add_group(sb.GroupDef(output_group_2_id,'Acuífero Cachapoal',None),False)
        
        output_group_3_id = 'output_group_3'
        super().add_group(sb.GroupDef(output_group_3_id,'Acuífero Tinguiririca',None),False)

        # Controls
        temporal_units_label = 'Fecha'
        output_decimal_places = 3

        flow_units_label = 'Caudal percolado (m3/s)'
        super().add_output(sb.OutputTimeSeriesDef('output_0_1','Tramo Cachapoal Sector El Olivar 1',output_group_0_id,sb.ChartDisplay(temporal_units_label,flow_units_label,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef('output_0_2','Tramo Cachapoal Sector El Olivar 2',output_group_0_id,sb.ChartDisplay(temporal_units_label,flow_units_label,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef('output_0_3','Tramo Rio Claro Sector Rengo',output_group_0_id,sb.ChartDisplay(temporal_units_label,flow_units_label,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef('output_0_4','Tramo Rio Claro Sector San Fernando',output_group_0_id,sb.ChartDisplay(temporal_units_label,flow_units_label,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef('output_0_5','Tramo Rio Tinguiririca Sector Palmilla-Marchigue 1',output_group_0_id,sb.ChartDisplay(temporal_units_label,flow_units_label,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef('output_0_6','Tramo Rio Tinguiririca Sector Palmilla-Marchigue 2',output_group_0_id,sb.ChartDisplay(temporal_units_label,flow_units_label,output_decimal_places)))

        self._define_aquifer_output_controls(output_group_1_id, temporal_units_label, output_decimal_places)
        self._define_aquifer_output_controls(output_group_2_id, temporal_units_label, output_decimal_places)
        self._define_aquifer_output_controls(output_group_3_id, temporal_units_label, output_decimal_places)

    def _define_aquifer_output_controls(self, group_id, temporal_units_label, output_decimal_places):
        flow_units = '(m3/s)'
        control_base_id = 'output_' + group_id[-1] + '_'
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '1','Salidas totales',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '2','Afloramiento ríos',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '3','Bombeo pozos',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '4','Conexiones subteráneas de salida',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '5','Ganancia de almacenamiento',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '6','Entradas totales',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '7','Recarga superficial',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '8','Pérdidas ríos',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '9','Entradas laterales',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '10','Conexiones subteráneas de entrada',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))
        super().add_output(sb.OutputTimeSeriesDef(control_base_id + '11','Pérdida de almacenamiento',group_id,sb.ChartDisplay(temporal_units_label,flow_units,output_decimal_places)))

    def _define_strategy_geotiff_layers(self):
        temporal_units_label = 'Fecha'
        output_decimal_places = 3

        layer_group = 'Acuíferos'

        # Layer Alhue Head (GeoTIFF)
        layer_001_geometry = sb.GeoTIFFGeometryImported(-999)
        layer_001_display = sb.GeoTIFFDisplay(['#340042','#1E7F7A','#FCE51E'],0.8)
        super().add_layer(sb.LayerGeoTIFFDef('layer_001','Alhué carga hidráulica subterránea','',layer_001_geometry,17,False,False,layer_001_display, layer_group))
        #super().add_layer_data('layer_001', sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'(msnm)',output_decimal_places)))

        # Layer Alhue Draw-down (GeoTIFF)
        layer_002_geometry = sb.GeoTIFFGeometryImported(-999)
        layer_002_display = sb.GeoTIFFDisplay(['#6D010E','#FFFFFF','#000000'],0.8)
        super().add_layer(sb.LayerGeoTIFFDef('layer_002','Alhué descensos agua subterránea','',layer_002_geometry,18,False,False,layer_002_display, layer_group))
        #super().add_layer_data('layer_002', sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'(msnm)',output_decimal_places)))

        # Layer Cachapoal Head (GeoTIFF)
        layer_003_geometry = sb.GeoTIFFGeometryImported(-999)
        layer_003_display = sb.GeoTIFFDisplay(['#340042','#1E7F7A','#FCE51E'],0.8)
        super().add_layer(sb.LayerGeoTIFFDef('layer_003','Cachapoal carga hidráulica subterránea','',layer_003_geometry,19,False,False,layer_003_display, layer_group))
        #super().add_layer_data('layer_003', sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'(msnm)',output_decimal_places)))

        # Layer Cachapoal Draw-down (GeoTIFF)
        layer_004_geometry = sb.GeoTIFFGeometryImported(-999)
        layer_004_display = sb.GeoTIFFDisplay(['#6D010E','#FFFFFF','#000000'],0.8)
        super().add_layer(sb.LayerGeoTIFFDef('layer_004','Cachapoal descensos agua subterránea','',layer_004_geometry,20,False,False,layer_004_display, layer_group))
        #super().add_layer_data('layer_004', sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'(msnm)',output_decimal_places)))

        # Layer Tinguiririca Head (GeoTIFF)
        layer_005_geometry = sb.GeoTIFFGeometryImported(-999)
        layer_005_display = sb.GeoTIFFDisplay(['#340042','#1E7F7A','#FCE51E'],0.8)
        super().add_layer(sb.LayerGeoTIFFDef('layer_005','Tinguiririca carga hidráulica subterránea','',layer_005_geometry,21,False,False,layer_005_display, layer_group))
        #super().add_layer_data('layer_005', sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'(msnm)',output_decimal_places)))

        # Layer Tinguiririca Draw-down (GeoTIFF)
        layer_006_geometry = sb.GeoTIFFGeometryImported(-999)
        layer_006_display = sb.GeoTIFFDisplay(['#6D010E','#FFFFFF','#000000'],0.8)
        super().add_layer(sb.LayerGeoTIFFDef('layer_006','Tinguiririca descensos agua subterránea','',layer_006_geometry,22,False,False,layer_006_display, layer_group))
        #super().add_layer_data('layer_006', sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'(msnm)',output_decimal_places)))
        return

    def _define_static_shapefiles_with_layer_data(self):
        output_decimal_places = 3
        temporal_units_label = 'Fecha'
        magic_months = ['ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC','ENE','FEB','MAR']
    
        layer_group = 'Capas de Resultados'
    
        # Layer A Sub-basins (Shapefile / Polygons)
        layer_A_default_polygon_display = sb.PolygonDisplay(1,1,0.3,'#000000','#e94de9')
        layer_A_display = sb.ShapefileDisplay(polygonDisplay=layer_A_default_polygon_display)
        super().add_layer(sb.LayerShapefileDef('layer_A','Subcuenca','',10,True,False,layer_A_display, layer_group))
        layer_A_data_defs = {
            'Precipitacion': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Precipitacion (mm)',output_decimal_places)),
            'Evapotranspiracion Potencial': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Evapotranspiracion Potencial (mm)',output_decimal_places)),
            'Evapotranspiracion': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Evapotranspiracion (mm)',output_decimal_places)),
            'Produccion de Agua': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Produccion de Agua (mm)',output_decimal_places)),
            'Flujo de entrada': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Flujo de entrada (m3/s)',output_decimal_places)),
            'Flujo de salida': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Flujo de salida (m3/s)',output_decimal_places))
            }
        # Add box stats for each series
        layer_A_box_defs = {}
        for ts_def in layer_A_data_defs:
            if ts_def == 'Flujo de entrada' or ts_def == 'Flujo de salida':
                units = '(m3/s)'
            else:
                units = '(mm)'
            layer_A_box_defs[ts_def + ' (Resumen)'] = sb.LayerDataBoxDef([ts_def], sb.ChartDisplay(units,'',output_decimal_places))
        layer_A_data_defs.update(layer_A_box_defs)
        super().add_layer_data('layer_A', layer_A_data_defs, 'Subbasin')

        # Layer B Irrigation zones (Shapefile / Polygons)
        layer_B_default_polygon_display = sb.PolygonDisplay(1,1,0.3,'#000000','#9be94d')
        layer_B_display = sb.ShapefileDisplay(polygonDisplay=layer_B_default_polygon_display)
        super().add_layer(sb.LayerShapefileDef('layer_B','Riego','',11,True,False,layer_B_display, layer_group))
        layer_B_data_defs = {
            'Caudal demandado zona de riego': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal demandado zona de riego (m3/s)',output_decimal_places)),
            'Caudal afluente zona de riego': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal afluente zona de riego (m3/s)',output_decimal_places)),
            'Caudal disponible en canales': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal disponible en canales (m3/s)',output_decimal_places)),
            'Caudal total disponible zona de riego': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal total disponible zona de riego (m3/s)',output_decimal_places)),
            'Caudal para riego': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal para riego (m3/s)',output_decimal_places)),
            'Caudal de derrames zona de riego': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal de derrames zona de riego (m3/s)',output_decimal_places)),
            'Demanda satisfecha zona de riego': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Demanda satisfecha zona de riego (m3/s)',output_decimal_places)),
            'Porcentage de demanda satisfecha zona de riego': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Porcentage de demanda satisfecha zona de riego (%)',output_decimal_places)),
            'Caudal percolado zona de riego': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal percolado zona de riego (m3/s)',output_decimal_places)),
            'Caudal de retorno zona de riego': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal de retorno zona de riego (m3/s)',output_decimal_places)),
            'Evapotranspiración': sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Evapotranspiración (mm)',output_decimal_places)),
            'Balance hídrico' : sb.LayerDataHistogramDef(magic_months,sb.ChartDisplay('Mes','(m3/s)',output_decimal_places))
            }
        # Add box stats for each series
        layer_B_box_defs = {}
        for ts_def in layer_B_data_defs:
            if ts_def == 'Balance hídrico':
                continue
            if ts_def == 'Evapotranspiración':
                units = '(mm)'
            elif ts_def == 'Porcentage de demanda satisfecha zona de riego':
                units = '(%)'
            else:
                units = '(m3/s)'
            layer_B_box_defs[ts_def + ' (Resumen)'] = sb.LayerDataBoxDef([ts_def], sb.ChartDisplay(units,'',output_decimal_places))
        layer_B_data_defs.update(layer_B_box_defs)
        super().add_layer_data('layer_B', layer_B_data_defs, 'Zona')

        # Layer C Aquifers (Shapefile / Polygons)
        layer_C_default_polygon_display = sb.PolygonDisplay(1,1,0.3,'#000000','#6ae0e0')
        layer_C_display = sb.ShapefileDisplay(polygonDisplay=layer_C_default_polygon_display)
        super().add_layer(sb.LayerShapefileDef('layer_C','Acuífero','',12,True,False,layer_C_display, layer_group))
        layer_C_data_defs = {
            'Salidas totales' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Salidas totales (m3/s)',output_decimal_places)),
            'Afloramiento ríos' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Afloramiento ríos (m3/s)',output_decimal_places)),
            'Bombeo pozos' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Bombeo pozos (m3/s)',output_decimal_places)),
            'Conexiones subteráneas de salida' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Conexiones subteráneas de salida (m3/s)',output_decimal_places)),
            'Ganancia de almacenamiento' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Ganancia de almacenamiento (m3/s)',output_decimal_places)),
            'Entradas totales' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Entradas totales (m3/s)',output_decimal_places)),
            'Recarga superficial' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Recarga superficial (m3/s)',output_decimal_places)),
            'Pérdidas ríos' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Pérdidas ríos (m3/s)',output_decimal_places)),
            'Entradas laterales' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Entradas laterales (m3/s)',output_decimal_places)),
            'Conexiones subteráneas de entrada' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Conexiones subteráneas de entrada (m3/s)',output_decimal_places)),
            'Pérdida de almacenamiento' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Pérdida de almacenamiento (m3/s)',output_decimal_places))
            }
        additional = ['AC-01 to AC-02','AC-02 to AC-04','AC-02 to AC-03','AC-04 to AC-02','AC-03 to AC-02','AC-03 to AC-06','AC-06 to AC-03',
                      'AC-04 to AC-06','AC-06 to AC-04','AC-06 to AC-07','AC-07 to AC-06','AC-11 to AC-13','AC-11 to AC-12','AC-13 to AC-11',
                      'AC-12 to AC-11','AC-12 to AC-13','AC-13 to AC-12','AC-13 to AC-17','AC-17 to AC-13','AC-14 to AC-15','AC-15 to AC-14',
                      'AC-15 to AC-16','AC-16 to AC-15','AC-16 to AC-17','AC-17 to AC-16']
        for a in additional:
            layer_C_data_defs[a] = sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,a+' (m3/s)',output_decimal_places))
        # Add box stats for each time series
        layer_C_box_defs = {}
        for ts_def in layer_C_data_defs:
            layer_C_box_defs[ts_def + ' (Resumen)'] = sb.LayerDataBoxDef([ts_def], sb.ChartDisplay('(m3/s)','',output_decimal_places))
        layer_C_data_defs.update(layer_C_box_defs)
        super().add_layer_data('layer_C', layer_C_data_defs, 'Codigo')

        # Layer D Nodes (Shapefile / Points)
        layer_D_default_point_display = sb.PointDisplay(4,1,1,1,'#000000','#eb5aeb')
        layer_D_display = sb.ShapefileDisplay(pointDisplay=layer_D_default_point_display)
        super().add_layer(sb.LayerShapefileDef('layer_D','Nodos','',13,True,False,layer_D_display, layer_group))
        layer_D_data_defs = {
            'Caudal afluente nodo' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal afluente nodo (m3/s)',output_decimal_places)),
            'Caudal de salida nodo' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal de salida nodo (m3/s)',output_decimal_places)),
            'Caudal de deficit nodo' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal de deficit nodo (m3/s)',output_decimal_places)),
            'Balance hídrico' : sb.LayerDataHistogramDef(magic_months,sb.ChartDisplay('Mes','(m3/s)',output_decimal_places))
            }
        # Add box stats for each series
        layer_D_box_defs = {}
        for ts_def in layer_D_data_defs:
            if ts_def == 'Balance hídrico':
                continue
            layer_D_box_defs[ts_def + ' (Resumen)'] = sb.LayerDataBoxDef([ts_def], sb.ChartDisplay('(m3/s)','',output_decimal_places))
        layer_D_data_defs.update(layer_D_box_defs)
        super().add_layer_data('layer_D', layer_D_data_defs, 'Codigo')

        # Layer E Reservoirs (Shapefile / Points)
        layer_E_default_point_display = sb.PointDisplay(4,1,1,1,'#5ae9eb','#2c2cf1')
        layer_E_display = sb.ShapefileDisplay(pointDisplay=layer_E_default_point_display)
        super().add_layer(sb.LayerShapefileDef('layer_E','Embalses','',14,True,False,layer_E_display, layer_group))
        layer_E_data_defs = {
            'Caudal demandado embalse' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal demandado embalse (m3/s)',output_decimal_places)),
            'Caudal afluente embalse' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal afluente embalse (m3/s)',output_decimal_places)),
            'Caudal rebases embalse' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal rebases embalse (m3/s)',output_decimal_places)),
            'Volúmen útil final embalse' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Volúmen útil final embalse (Mm3)',output_decimal_places))
            }
        # Add box stats for each series
        layer_E_box_defs = {}
        for ts_def in layer_E_data_defs:
            if ts_def == 'Volúmen útil final embalse':
                units = '(Mm3)'
            else:
                units = '(m3/s)'
            layer_E_box_defs[ts_def + ' (Resumen)'] = sb.LayerDataBoxDef([ts_def], sb.ChartDisplay(units,'',output_decimal_places))
        layer_E_data_defs.update(layer_E_box_defs)
        super().add_layer_data('layer_E', layer_E_data_defs, 'CODE')

        # Layer F Wells (Shapefile / Points)
        layer_F_default_point_display = sb.PointDisplay(4,1,1,1,'#6703fc','#03fcf4')
        layer_F_display = sb.ShapefileDisplay(pointDisplay=layer_F_default_point_display)
        super().add_layer(sb.LayerShapefileDef('layer_F','Pozos','',15,True,False,layer_F_display, layer_group))
        layer_F_data_defs = {
            'Carga hidráulica subterránea' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Carga hidráulica subterránea (msnm)',output_decimal_places)),
            'Descensos agua subterránea' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Descensos agua subterránea (msnm)',output_decimal_places))
            }
        # Add box stats for each series
        layer_F_box_defs = {}
        for ts_def in layer_F_data_defs:
            layer_F_box_defs[ts_def + ' (Resumen)'] = sb.LayerDataBoxDef([ts_def], sb.ChartDisplay('(msnm)','',output_decimal_places))
        layer_F_data_defs.update(layer_F_box_defs)
        super().add_layer_data('layer_F', layer_F_data_defs, 'Well Name')

        # Layer G Hydro-Electric Stations (Shapefile / Points)
        layer_G_default_point_display = sb.PointDisplay(4,2,1,1,'#000000','#f7dc6f')
        layer_G_display = sb.ShapefileDisplay(pointDisplay=layer_G_default_point_display)
        super().add_layer(sb.LayerShapefileDef('layer_G','Hidroelectricas','',16,True,False,layer_G_display, layer_group))
        layer_G_data_defs = {
            'Caudal captado central de pasada' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Caudal captado central de pasada (m3/s)',output_decimal_places)),
            'Energia' : sb.LayerDataTimeSeriesDef(sb.ChartDisplay(temporal_units_label,'Energia (GW)',output_decimal_places))
            }
        # Add box stats for each series
        layer_G_box_defs = {}
        for ts_def in layer_G_data_defs:
            if ts_def == 'Caudal captado central de pasada':
                units = '(m3/s)'
            else:
                units = '(GW)'
            layer_G_box_defs[ts_def + ' (Resumen)'] = sb.LayerDataBoxDef([ts_def], sb.ChartDisplay(units,'',output_decimal_places))
        layer_G_data_defs.update(layer_G_box_defs)
        super().add_layer_data('layer_G', layer_G_data_defs, 'Name')

    def _define_static_shapefiles(self):

        layer_group = 'Mostrar Capas'

        # Layer 01 Cuenca de Rapel (Shapefile / Polygons)
        layer_01_default_polygon_display = sb.PolygonDisplay(4,1,0.1,'#888888','#00332f')
        layer_01_display = sb.ShapefileDisplay(polygonDisplay=layer_01_default_polygon_display)
        super().add_layer(sb.LayerShapefileDef('layer_01','Cuenca de Rapel','',1,True,True,layer_01_display, layer_group))

        # Layer 02 Cuencas (Shapefile / Polygons)
        layer_02_default_polygon_display = sb.PolygonDisplay(1,1,0.3,'#000000','#00332f')
        layer_02_display = sb.ShapefileDisplay(polygonDisplay=layer_02_default_polygon_display)
        super().add_layer(sb.LayerShapefileDef('layer_02','Cuencas','',2,True,False,layer_02_display, layer_group))

        # Layer 03 Junta de Vigilancia (Shapefile / Polygons)
        layer_03_default_polygon_display = sb.PolygonDisplay(1,1,0.3,'#000000','#00332f')
        layer_03_display = sb.ShapefileDisplay(polygonDisplay=layer_03_default_polygon_display)
        super().add_layer(sb.LayerShapefileDef('layer_03','Junta de Vigilancia','',3,True,False,layer_03_display, layer_group))
        
        # Layer 04 Embalses y Lagos (Shapefile / Polygons)
        layer_04_default_polygon_display = sb.PolygonDisplay(2,1,0.3,'#000000','#0000ff')
        layer_04_display = sb.ShapefileDisplay(polygonDisplay=layer_04_default_polygon_display)
        super().add_layer(sb.LayerShapefileDef('layer_04','Embalses y Lagos','',4,True,False,layer_04_display, layer_group))
        
        # Layer 10 Canales (Shapefile / Lines)
        layer_10_default_line_display = sb.LineDisplay(1,1,'#3498db')
        layer_10_display = sb.ShapefileDisplay(lineDisplay=layer_10_default_line_display)
        super().add_layer(sb.LayerShapefileDef('layer_10','Canales','',5,True,False,layer_10_display, layer_group))

        # Layer 11 Drenaje Principal (Shapefile / Lines)
        layer_11_default_line_display = sb.LineDisplay(1,1,'#dc7633')
        layer_11_display = sb.ShapefileDisplay(lineDisplay=layer_11_default_line_display)
        super().add_layer(sb.LayerShapefileDef('layer_11','Drenaje Principal','',6,True,False,layer_11_display, layer_group))

        # Layer 21 APR (Shapefile / Points)
        layer_21_default_point_display = sb.PointDisplay(4,1,1,1,'#8e44ad','#8e44ad')
        layer_21_display = sb.ShapefileDisplay(pointDisplay=layer_21_default_point_display)
        super().add_layer(sb.LayerShapefileDef('layer_21','APR','',7,True,False,layer_21_display, layer_group))
        
        # Layer 22 Estaciones meteorológicas (Shapefile / Points)
        layer_22_default_point_display = sb.PointDisplay(4,1,1,1,'#dc7633','#dc7633')
        layer_22_display = sb.ShapefileDisplay(pointDisplay=layer_22_default_point_display)
        super().add_layer(sb.LayerShapefileDef('layer_22','Estaciones meteorológicas','',8,True,False,layer_22_display, layer_group))
        
        # Layer 23 Fluviométricas (Shapefile / Points)
        layer_23_default_point_display = sb.PointDisplay(4,2,1,1,'#808080','#00ff00')
        layer_23_display = sb.ShapefileDisplay(pointDisplay=layer_23_default_point_display)
        super().add_layer(sb.LayerShapefileDef('layer_23','Fluviométricas','',9,True,False,layer_23_display, layer_group))

    def metadata(self):
        metadata = {}
        metadata['id'] = 'scenario_rapel_1'
        metadata['name'] = 'SimRapel: visualizador de estrategias hídricas para la cuenca del río Rapel'
        metadata['description'] = 'Junio 2020'
        #metadata['view'] = { 'lat': -34.44, 'lon': -70.98, 'zoom': 10 }
        metadata['view'] = { 'lat': -34.39, 'lon': -70.93, 'zoom': 9 }
        metadata['timesteps'] = { 'steps': [39], 'unit_singular': 'año', 'unit_plural': 'años' }
        metadata['show_date_status'] = False;
        return metadata

    def load_constant_layers(self):
        shp_src_epsg_chile = 32719
        shp_src_epsg_chile2 = 32718
        shp_src_epsg_world = 4326
        
        def pickle_shapefile(lsv, fn):
            fo = open(fn, 'bw')
            pickle.dump(lsv, fo)
            fo.close()

        def unpickle_shapefile(fn):
            fi = open(fn, 'br')
            lsv = pickle.load(fi)
            fi.close()
            return lsv

        # Pickle layers

        #root = ''

        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Subbasins','Subs.shp'),shp_src_epsg_chile,['Subbasin'],['Subbasin','Area'],['Subcuenca','Metros cuadrados']), root + 'subbasin.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Irrigation zones','ZonasRiego_CuencaRapel.shp'),shp_src_epsg_chile2,['Zona'],['Zona','AREAKM2'],['Zona','Kilómetros cuadrados']), root + 'irrigation.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Aquifers','Acuiferos_CuencaRapel.shp'),shp_src_epsg_chile2,['Codigo'],['Codigo','AREAKM2'],['Codigo','Kilómetros cuadrados']), root + 'aquifer.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Nodes','Nodos_LP_v2.shp'),shp_src_epsg_chile,['Codigo'],['Codigo'],['Codigo']), root + 'node.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'New_Reservoirs','New_RESERVOIRS.shp'),shp_src_epsg_chile,['NAME'],['CODE','NAME'],['Codigo','Descripcio']), root + 'reservoir.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'OBS_WELLS','OBS_WELLS.shp'),shp_src_epsg_chile,['Well Name'],['Well Name'],['Nombre']), root + 'well.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Hidroelectrics','Hidroelectricas.shp'),shp_src_epsg_world,['Name'],['Name'],['Nombre']), root + 'hydro.pkl')

        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Basins','DGA_Cuencas_DARH_2015_Rapel.shp'),shp_src_epsg_chile,['NOM_DGA'],['NOM_DGA'],['Nombre']), root + 'basinrapel.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Basins','DGA Cuencas_DARH_2015.shp'),shp_src_epsg_chile,['NOM_DGA'],['NOM_DGA'],['Nombre']), root + 'basin.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Juntas_de_vigilancia','Juntas_de_Vigilancia.shp'),shp_src_epsg_chile,['NombreJunt'],['NombreJunt'],['Nombre']), root + 'board.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Reservoir and main lakes','Reservoirs_and_lakes.shp'),shp_src_epsg_chile,['Name'],['Name'],['Nombre']), root + 'resandlake.pkl')

        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Canals','Canales.shp'),shp_src_epsg_chile,['NOMBRESUBS'],['NOMBRESUBS'],['Nombre']), root + 'canal.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Main drainage','dren_principal_rapel_alhue.shp'),shp_src_epsg_chile,['NOMBRESUBS'],['NOMBRESUBS'],['Nombre']), root + 'drainage.pkl')
        
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'APR','APR.shp'),shp_src_epsg_chile,['LABEL'],['LABEL'],['Label']), root + 'apr.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'Meteorological stations','Meteorologicas.shp'),shp_src_epsg_chile,['NOMBRE'],['NOMBRE'],['Nombre']), root + 'met.pkl')
        #pickle_shapefile(sb.LayerShapefileVal(os.path.join(self.layer_dir,'River gauge','Fluviometricas_point.shp'),shp_src_epsg_chile,['NOMBRE'],['NOMBRE','MEDICION'],['Nombre','Medicion']), root + 'gauge.pkl')
        
        # Unpickle layers
        
        self.set_layer('layer_A', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'subbasin.pkl')))
        self.set_layer('layer_B', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'irrigation.pkl')))
        self.set_layer('layer_C', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'aquifer.pkl')))
        self.set_layer('layer_D', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'node.pkl')))
        self.set_layer('layer_E', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'reservoir.pkl')))
        self.set_layer('layer_F', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'well.pkl')))
        self.set_layer('layer_G', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'hydro.pkl')))

        self.set_layer('layer_01', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'basinrapel.pkl')))
        self.set_layer('layer_02', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'basin.pkl')))
        self.set_layer('layer_03', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'board.pkl')))
        self.set_layer('layer_04', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'resandlake.pkl')))

        self.set_layer('layer_10', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'canal.pkl')))
        self.set_layer('layer_11', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'drainage.pkl')))

        self.set_layer('layer_21', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'apr.pkl')))
        self.set_layer('layer_22', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'met.pkl')))
        self.set_layer('layer_23', unpickle_shapefile(os.path.join(self.layer_dir, 'pickled', 'gauge.pkl')))

        #self.set_layer('layer_A', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Subbasins','Subs.shp'),shp_src_epsg_chile,['Subbasin'],['Subbasin','Area'],['Subcuenca','Metros cuadrados']))
        #self.set_layer('layer_B', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Irrigation zones','ZonasRiego_CuencaRapel.shp'),shp_src_epsg_chile2,['Zona'],['Zona','AREAKM2'],['Zona','Kilómetros cuadrados']))
        #self.set_layer('layer_C', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Aquifers','Acuiferos_CuencaRapel.shp'),shp_src_epsg_chile2,['Codigo'],['Codigo','AREAKM2'],['Codigo','Kilómetros cuadrados']))
        #self.set_layer('layer_D', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Nodes','Nodos_LP_v2.shp'),shp_src_epsg_chile,['Codigo'],['Codigo'],['Codigo']))
        #self.set_layer('layer_E', sb.LayerShapefileVal(os.path.join(self.layer_dir,'New_Reservoirs','New_RESERVOIRS.shp'),shp_src_epsg_chile,['NAME'],['CODE','NAME'],['Codigo','Descripcio']))
        #self.set_layer('layer_F', sb.LayerShapefileVal(os.path.join(self.layer_dir,'OBS_WELLS','OBS_WELLS.shp'),shp_src_epsg_chile,['Well Name'],['Well Name'],['Nombre']))
        #self.set_layer('layer_G', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Hidroelectrics','Hidroelectricas.shp'),shp_src_epsg_world,['Name'],['Name'],['Nombre']))

        #self.set_layer('layer_01', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Basins','DGA_Cuencas_DARH_2015_Rapel.shp'),shp_src_epsg_chile,['NOM_DGA'],['NOM_DGA'],['Nombre']))
        #self.set_layer('layer_02', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Basins','DGA Cuencas_DARH_2015.shp'),shp_src_epsg_chile,['NOM_DGA'],['NOM_DGA'],['Nombre']))
        #self.set_layer('layer_03', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Juntas_de_vigilancia','Juntas_de_Vigilancia.shp'),shp_src_epsg_chile,['NombreJunt'],['NombreJunt'],['Nombre']))
        #self.set_layer('layer_04', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Reservoir and main lakes','Reservoirs_and_lakes.shp'),shp_src_epsg_chile,['Name'],['Name'],['Nombre']))

        #self.set_layer('layer_10', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Canals','Canales.shp'),shp_src_epsg_chile,['NOMBRESUBS'],['NOMBRESUBS'],['Nombre']))
        #self.set_layer('layer_11', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Main drainage','dren_principal_rapel_alhue.shp'),shp_src_epsg_chile,['NOMBRESUBS'],['NOMBRESUBS'],['Nombre']))

        #self.set_layer('layer_21', sb.LayerShapefileVal(os.path.join(self.layer_dir,'APR','APR.shp'),shp_src_epsg_chile,['LABEL'],['LABEL'],['Label']))
        #self.set_layer('layer_22', sb.LayerShapefileVal(os.path.join(self.layer_dir,'Meteorological stations','Meteorologicas.shp'),shp_src_epsg_chile,['NOMBRE'],['NOMBRE'],['Nombre']))
        #self.set_layer('layer_23', sb.LayerShapefileVal(os.path.join(self.layer_dir,'River gauge','Fluviometricas_point.shp'),shp_src_epsg_chile,['NOMBRE'],['NOMBRE','MEDICION'],['Nombre','Medicion']))
        
        return

    def initialise(self):
        pass

    def reset(self):
        self.set_run_status(0, 'Cargando resultados...')

    def run_time_steps(self, dt, steps):
        strategy_dir = os.path.join(self.data_dir, self._get_strategy_data_directory())
        hydro_dir = os.path.join(self.data_dir, self._get_hydro_data_directory())

        self._set_irrigation_summary_output_histogram_layer_data(strategy_dir)
        
        self._set_node_summary_output_histogram_layer_data(strategy_dir)

        self.set_run_status(0, 'Cargando resultados...')
        self._set_global_aquifer_output_time_series_data(strategy_dir)

        self.set_run_status(10, 'Cargando resultados...')
        self._set_head_and_drawdown_layers(strategy_dir)

        self.set_run_status(20, 'Cargando resultados...')
        self._set_aquifer_time_series_layer_data(strategy_dir)

        self.set_run_status(30, 'Cargando resultados...')
        self._set_well_time_series_layer_data(strategy_dir)

        self.set_run_status(40, 'Cargando resultados...')
        self._set_irrigation_time_series_layer_data(strategy_dir)

        self.set_run_status(42, 'Cargando resultados...')
        self._set_reservoir_time_series_layer_data(strategy_dir)

        self.set_run_status(45, 'Cargando resultados...')
        self._set_node_time_series_layer_data(strategy_dir)

        self.set_run_status(47, 'Cargando resultados...')
        self._set_hydro_power_time_series_layer_data(strategy_dir)

        self.set_run_status(50, 'Cargando resultados...')
        self._set_river_reach_output_time_series_data(strategy_dir)

        self.set_run_status(60, 'Cargando resultados...')
        self._set_sub_basin_time_series_layer_data(hydro_dir)

    def _set_irrigation_summary_output_histogram_layer_data(self, strategy_dir):
        zone_ids = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14]
        for z in zone_ids:
            id = 'ZR-' + str(z).zfill(2)
            pos_data, neg_data = read_magic_summary(strategy_dir, id)
            ds = sb.OutputMultipleNumericDatasetVal()
            ds.append_dataset(pos_data,'Entradas')
            ds.append_dataset(neg_data,'Salidas')
            self.set_layer_data('layer_B', id, ds, 'Balance hídrico')

    def _set_node_summary_output_histogram_layer_data(self, strategy_dir):
        node_ids = [15, 16, 19, 20, 26, 31, 34, 39, 52, 53, 54, 59, 63, 64, 66, 70, 74, 75, 80, 81, 83]
        for n in node_ids:
            id = 'NO-' + str(n).zfill(2)
            pos_data, neg_data = read_magic_summary(strategy_dir, id)
            ds = sb.OutputMultipleNumericDatasetVal()
            ds.append_dataset(pos_data,'Entradas')
            ds.append_dataset(neg_data,'Salidas')
            self.set_layer_data('layer_D', id, ds, 'Balance hídrico')

    def _set_global_aquifer_output_time_series_data(self, strategy_dir):
        aquifers = ['alhue', 'cachapoal', 'tinguiririca']
        varnames = ['TOTAL OUT', 'RIVER LEAKAGE OUT', 'WELLS OUT', 'CONSTANT HEAD OUT', 'STORAGE OUT', 'TOTAL IN', 'RECHARGE IN', 'RIVER LEAKAGE IN', 'WELLS IN', 'CONSTANT HEAD IN', 'STORAGE IN']
        for c in range(1, 4):
            control_base_id = 'output_' + str(c) + '_'
            for i in range(len(varnames)):
                self.set_output(control_base_id + str(i+1), read_modflow_global_balance_timeseries(strategy_dir, aquifers[c-1], varnames[i]))

    def _set_head_and_drawdown_layers(self, strategy_dir):
        self.set_layer('layer_001', sb.LayerGeoTIFFImportedVal(strategy_dir + '/modflow/alhue/ALHUE_HEAD.tif'))
        self.set_layer('layer_002', sb.LayerGeoTIFFImportedVal(strategy_dir + '/modflow/alhue/ALHUE_DRAWDOWN.tif'))
        self.set_layer('layer_003', sb.LayerGeoTIFFImportedVal(strategy_dir + '/modflow/cachapoal/CACHAPOAL_HEAD.tif'))
        self.set_layer('layer_004', sb.LayerGeoTIFFImportedVal(strategy_dir + '/modflow/cachapoal/CACHAPOAL_DRAWDOWN.tif'))
        self.set_layer('layer_005', sb.LayerGeoTIFFImportedVal(strategy_dir + '/modflow/tinguiririca/TINGUIRIRICA_HEAD.tif'))
        self.set_layer('layer_006', sb.LayerGeoTIFFImportedVal(strategy_dir + '/modflow/tinguiririca/TINGUIRIRICA_DRAWDOWN.tif'))

        # self._apply_modflow_layer_data(strategy_dir, 'alhue', 'head', 'layer_001')
        # self._apply_modflow_layer_data(strategy_dir, 'alhue', 'drawdown', 'layer_002')
        # self._apply_modflow_layer_data(strategy_dir, 'cachapoal', 'head', 'layer_003')
        # self._apply_modflow_layer_data(strategy_dir, 'cachapoal', 'drawdown', 'layer_004')
        # self._apply_modflow_layer_data(strategy_dir, 'tinguiririca', 'head', 'layer_005')
        # self._apply_modflow_layer_data(strategy_dir, 'tinguiririca', 'drawdown', 'layer_006')
        return

    def _set_aquifer_time_series_layer_data(self, strategy_dir):
        aquifer_ids = [1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17]
        file_ids = ['Total OUT','RIVER LEAKAGE OUT','WELLS OUT','CONSTANT HEAD OUT','STORAGE OUT',
            'Total IN','RECHARGE IN','RIVER LEAKAGE IN','WELLS IN','CONSTANT HEAD IN','STORAGE IN']
        varnames = ['Salidas totales','Afloramiento ríos','Bombeo pozos','Conexiones subteráneas de salida','Ganancia de almacenamiento',
            'Entradas totales','Recarga superficial','Pérdidas ríos','Entradas laterales','Conexiones subteráneas de entrada','Pérdida de almacenamiento']
        for a in aquifer_ids:
            id = 'AC-' + str(a).zfill(2)
            for i in range(len(file_ids)):
                file_id = file_ids[i]
                varname = varnames[i]
                ts = read_modflow_balance_timeseries(strategy_dir, id, file_id)
                self.set_layer_data('layer_C', id, ts, varname)
                bd = generate_box_dataset(ts)
                box_data = sb.OutputBoxNumericDatasetVal()
                box_data.append_dataset([bd], varname)
                self.set_layer_data('layer_C', id, box_data, varname + ' (Resumen)')

        additional = {  1 : ['AC-01 to AC-02'],
                        2 : ['AC-02 to AC-04','AC-02 to AC-03','AC-04 to AC-02','AC-03 to AC-02','AC-01 to AC-02'],
                        3 : ['AC-03 to AC-06','AC-03 to AC-02','AC-06 to AC-03','AC-02 to AC-03'],
                        4 : ['AC-04 to AC-06','AC-04 to AC-02','AC-06 to AC-04','AC-02 to AC-04'],
                        6 : ['AC-06 to AC-07','AC-06 to AC-04','AC-06 to AC-03','AC-07 to AC-06','AC-04 to AC-06','AC-03 to AC-06'],
                        7 : ['AC-07 to AC-06','AC-06 to AC-07'],
                       11 : ['AC-11 to AC-13','AC-11 to AC-12','AC-13 to AC-11','AC-12 to AC-11'],
                       12 : ['AC-12 to AC-13','AC-12 to AC-11','AC-13 to AC-12','AC-11 to AC-12'],
                       13 : ['AC-13 to AC-17','AC-13 to AC-12','AC-13 to AC-11','AC-17 to AC-13','AC-12 to AC-13','AC-11 to AC-13'],
                       14 : ['AC-14 to AC-15','AC-15 to AC-14'],
                       15 : ['AC-15 to AC-16','AC-15 to AC-14','AC-16 to AC-15','AC-14 to AC-15'],
                       16 : ['AC-16 to AC-17','AC-16 to AC-15','AC-17 to AC-16','AC-15 to AC-16'],
                       17 : ['AC-17 to AC-16','AC-17 to AC-13','AC-16 to AC-17','AC-13 to AC-17']
                     }
        for a in additional:
            id = 'AC-' + str(a).zfill(2)
            for v in additional[a]:
                ts = read_modflow_balance_timeseries(strategy_dir, id, v)
                self.set_layer_data('layer_C', id, ts, v)
                bd = generate_box_dataset(ts)
                box_data = sb.OutputBoxNumericDatasetVal()
                box_data.append_dataset([bd], v)
                self.set_layer_data('layer_C', id, box_data, v + ' (Resumen)')

    def _set_well_time_series_layer_data(self, strategy_dir):
        wells_alhue = ['OBS-9', 'OBS-8', 'OBS-7', 'OBS-3', 'OBS-14', 'OBS-13', 'OBS-12', 'OBS-11', 'OBS-10', 'OBS-1', 'LAGO 4', 'LAGO 3', 'LAGO 2', 'LAGO 1']

        wells_chacapoal = ['LA ROSA SOFRUCO 2', 'LA ROSA SOFRUCO 1', 'INDURA GRANEROS', 'FUNDO SAN PEDRO', 'FUNDO LAS JUNTAS', 'FUNDO LA GRANJA',
            'FUNDO EL BOSQUE', 'FIAT CHILENA', 'CENTRO FRUTICOLA', 'BARRIO INDUSTRIAL', 'APR ZUGNIGA', 'APR TOQUIHUA', 'APR REQUEHUA', 'APR RASTROJOS',
            'APR PUNTA DE COR', 'APR PUEBLO DE', 'APR PANQUEHUE', 'APR OLIVAR BAJO', 'APR MOLINOS QUE', 'APR LOS BOLDOS', 'APR LO DE LOBOS',
            'APR LO CARTAGENA', 'APR LA COMPAGNIA', 'APR HUILQUIO DE', 'APR EL TAMBO', 'APR EL RULO', 'APR EL ABRA', 'APR CORCOLEN', 'APR COPEQUEN',
            'APR CERRO PUEBLO', 'APR CARACOLES', 'AP ROSARIO', 'AP REQUINOA', 'AP RANCAGUA SANC', 'AP RANCAGUA MEMB', 'AP QUINTA DE TIL', 'AP PEUMO',
            'AP PELEQUEN', 'AP MALLOA', 'AP LO MIRANDA', 'AP LAS CABRAS', 'AP GRANEROS', 'AP EL OLIVAR', 'AP COINCO']

        wells_tinguiririca = ['VIGNA SANTA ELISA', 'VIGNA SAN LUIS', 'RINC DE HALCONES', 'MATADERO MARCHIG', 'INACAP SN FERNANDO', 'FUNDO TOLHUEN',
            'FUNDO TALCAREHUE', 'FUNDO STA TERESA', 'FDOSNJOSEMARCHI', 'FDO STA VIRGINIA', 'FDO STA EUGENIA', 'FDO SN JOSE_BOLDO', 'FDO SAN ENRIQUE',
            'FDO LA TUNA', 'FDO LA MACARENA', 'FDO EL RECREO', 'ENAP SN FERNANDO', 'ASENT U_CAMPESINA', 'ASENT SN CORAZON', 'ASENT SAN ISIDRO',
            'ASENT LAS GARZAS', 'ASENT LA PUERTA', 'ASENT LA PATAGUA', 'ASENT EL TRIUNFO', 'ASENT AGUA SANTA', 'ASENT 21 DE MAYO 3', 'ASENT 21 DE MAYO 2',
            'APRCUESTALOGONZAL', 'APR TRES PUENTES', 'APR TINGUIRIRICA', 'APR ROMA SN JOSE', 'APR ROMA ARRIBA', 'APR QUINAHUE', 'APR PUQUILLAY',
            'APR POLONIA', 'APR LA FINCA', 'APR CUNACO', 'APR CONVENTO VIEJO', 'APR CODEGUA', 'APR AUQUINCO', 'APR ANGOSTURA', 'APR AGUA BUENA',
            'AP SN FERNANDO', 'AP POBLACION', 'AP NANCAHUA', 'AP CHIMBARONGO']

        for wa in wells_alhue:
            id = wa
            ts_head = read_modflow_timeseries(strategy_dir, id, 'alhue', 'head')
            varname_head = 'Carga hidráulica subterránea'
            self.set_layer_data('layer_F', id, ts_head, varname_head)
            bd = generate_box_dataset(ts_head)
            box_data = sb.OutputBoxNumericDatasetVal()
            box_data.append_dataset([bd], varname_head)
            self.set_layer_data('layer_F', id, box_data, varname_head + ' (Resumen)')
            ts_drawdown = read_modflow_timeseries(strategy_dir, id, 'alhue', 'drawdown')
            varname_drawdown = 'Descensos agua subterránea'
            self.set_layer_data('layer_F', id, ts_drawdown, varname_drawdown)
            bd = generate_box_dataset(ts_drawdown)
            box_data = sb.OutputBoxNumericDatasetVal()
            box_data.append_dataset([bd], varname_drawdown)
            self.set_layer_data('layer_F', id, box_data, varname_drawdown + ' (Resumen)')

        for ca in wells_chacapoal:
            id = ca
            ts_head = read_modflow_timeseries(strategy_dir, id, 'cachapoal', 'head')
            varname_head = 'Carga hidráulica subterránea'
            self.set_layer_data('layer_F', id, ts_head, varname_head)
            bd = generate_box_dataset(ts_head)
            box_data = sb.OutputBoxNumericDatasetVal()
            box_data.append_dataset([bd], varname_head)
            self.set_layer_data('layer_F', id, box_data, varname_head + ' (Resumen)')
            ts_drawdown = read_modflow_timeseries(strategy_dir, id, 'cachapoal', 'drawdown')
            varname_drawdown = 'Descensos agua subterránea'
            self.set_layer_data('layer_F', id, ts_drawdown, varname_drawdown)
            bd = generate_box_dataset(ts_drawdown)
            box_data = sb.OutputBoxNumericDatasetVal()
            box_data.append_dataset([bd], varname_drawdown)
            self.set_layer_data('layer_F', id, box_data, varname_drawdown + ' (Resumen)')

        for wt in wells_tinguiririca:
            id = wt
            ts_head = read_modflow_timeseries(strategy_dir, id, 'tinguiririca', 'head')
            varname_head = 'Carga hidráulica subterránea'
            self.set_layer_data('layer_F', id, ts_head, varname_head)
            bd = generate_box_dataset(ts_head)
            box_data = sb.OutputBoxNumericDatasetVal()
            box_data.append_dataset([bd], varname_head)
            self.set_layer_data('layer_F', id, box_data, varname_head + ' (Resumen)')
            ts_drawdown = read_modflow_timeseries(strategy_dir, id, 'tinguiririca', 'drawdown')
            varname_drawdown = 'Descensos agua subterránea'
            self.set_layer_data('layer_F', id, ts_drawdown, varname_drawdown)
            bd = generate_box_dataset(ts_drawdown)
            box_data = sb.OutputBoxNumericDatasetVal()
            box_data.append_dataset([bd], varname_drawdown)
            self.set_layer_data('layer_F', id, box_data, varname_drawdown + ' (Resumen)')

    def _set_irrigation_time_series_layer_data(self, strategy_dir):
        zone_ids = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14]
        file_ids = ['Qddo','Qafl','Qcanal','Qtotal','Qrie','Qderr','DS','Pds','Qper','Qret','ET']
        varnames = ['Caudal demandado zona de riego','Caudal afluente zona de riego','Caudal disponible en canales',
                    'Caudal total disponible zona de riego','Caudal para riego','Caudal de derrames zona de riego',
                    'Demanda satisfecha zona de riego','Porcentage de demanda satisfecha zona de riego',
                    'Caudal percolado zona de riego','Caudal de retorno zona de riego','Evapotranspiración']
        for z in zone_ids:
            id = 'ZR-' + str(z).zfill(2)
            for i in range(len(file_ids)):
                file_id = file_ids[i]
                varname = varnames[i]
                if file_id == 'Pds':
                    ts = read_magic_timeseries(strategy_dir, id, file_id, 100.0)
                else:
                    ts = read_magic_timeseries(strategy_dir, id, file_id)
                self.set_layer_data('layer_B', id, ts, varname)
                bd = generate_box_dataset(ts)
                box_data = sb.OutputBoxNumericDatasetVal()
                box_data.append_dataset([bd], varname)
                self.set_layer_data('layer_B', id, box_data, varname + ' (Resumen)')

    def _set_reservoir_time_series_layer_data(self, strategy_dir):
        reservoir_ids = [1, 2, 3, 4, 5, 6]
        file_ids = ['Qddo', 'Qafl', 'Qrb', 'Vuf']
        varnames = ['Caudal demandado embalse', 'Caudal afluente embalse', 'Caudal rebases embalse', 'Volúmen útil final embalse']
        for r in reservoir_ids:
            id = 'EM-' + str(r).zfill(2)
            for i in range(len(file_ids)):
                file_id = file_ids[i]
                varname = varnames[i]
                ts = read_magic_timeseries(strategy_dir, id, file_id)
                if ts != None:
                    self.set_layer_data('layer_E', id, ts, varname)
                    bd = generate_box_dataset(ts)
                    box_data = sb.OutputBoxNumericDatasetVal()
                    box_data.append_dataset([bd], varname)
                    self.set_layer_data('layer_E', id, box_data, varname + ' (Resumen)')

    def _set_node_time_series_layer_data(self, strategy_dir):
        node_ids = [15, 16, 19, 20, 26, 31, 34, 39, 52, 53, 54, 59, 63, 64, 66, 70, 74, 75, 80, 81, 83]
        file_ids = ['Qafl','Qsal','Qdef']
        varnames = ['Caudal afluente nodo', 'Caudal de salida nodo', 'Caudal de deficit nodo']
        for n in node_ids:
            id = 'NO-' + str(n).zfill(2)
            for i in range(len(file_ids)):
                file_id = file_ids[i]
                varname = varnames[i]
                ts = read_magic_timeseries(strategy_dir, id, file_id)
                if ts != None:
                    self.set_layer_data('layer_D', id, ts, varname)
                    bd = generate_box_dataset(ts)
                    box_data = sb.OutputBoxNumericDatasetVal()
                    box_data.append_dataset([bd], varname)
                    self.set_layer_data('layer_D', id, box_data, varname + ' (Resumen)')

    def _set_hydro_power_time_series_layer_data(self, strategy_dir):
        power_ids = [1, 2, 4, 6, 7, 8]
        code_to_id_lookup = { 1 : 'Central Coya', 2 : 'Central Pangal', 4 : 'Central Sauzalito', 6 : 'Central La Confluencia', 7 : 'Central La Higuera', 8 : 'Central Chacayes' }
        for p in power_ids:
            code = 'CH-' + str(p).zfill(2)
            id = code_to_id_lookup[p]
            ts_Qcap = read_magic_timeseries(strategy_dir, code, 'Qcap')
            if ts_Qcap != None:
                varname = 'Caudal captado central de pasada'
                self.set_layer_data('layer_G', id, ts_Qcap, varname)
                bd = generate_box_dataset(ts_Qcap)
                box_data = sb.OutputBoxNumericDatasetVal()
                box_data.append_dataset([bd], varname)
                self.set_layer_data('layer_G', id, box_data, varname + ' (Resumen)')
            ts_Energia = read_magic_timeseries(strategy_dir, code, 'Energia', 1e-6)
            if ts_Energia != None:
                varname = 'Energia'
                self.set_layer_data('layer_G', id, ts_Energia, varname)
                bd = generate_box_dataset(ts_Energia)
                box_data = sb.OutputBoxNumericDatasetVal()
                box_data.append_dataset([bd], varname)
                self.set_layer_data('layer_G', id, box_data, varname + ' (Resumen)')

    def _set_river_reach_output_time_series_data(self, strategy_dir):
        reach_ids = [15, 16, 26, 52, 63, 64]
        code_to_id_lookup = { 15 : 'output_0_1', 16 : 'output_0_2', 26 : 'output_0_3', 52 : 'output_0_4', 63 : 'output_0_5', 64 : 'output_0_6' }
        for r in reach_ids:
            code = 'TR-' + str(r).zfill(2)
            id = code_to_id_lookup[r]
            self.set_output(id, read_magic_timeseries(strategy_dir, code, 'Qper'))

    def _set_sub_basin_time_series_layer_data(self, hydro_dir):
        dates, ts = read_all_swat_timeseries(hydro_dir)
        basin_ids = ['Precipitacion','Evapotranspiracion Potencial','Evapotranspiracion','Produccion de Agua','Flujo de entrada','Flujo de salida']
        file_ids = ['PRECIPmm','PETmm','ETmm','WYLDmm','FLOW_INcms','FLOW_OUTcms']
        def make_timeseries(dates, ts, id, varname):
            values = ts[varname][str(id)]
            return sb.TimseriesBaseVal(dates, values)
        for s in range(1, 67):
            id = s
            for i in range(len(basin_ids)):
                file_id = file_ids[i]
                basin_id = basin_ids[i]
                timeseries = make_timeseries(dates, ts, id, file_id)
                self.set_layer_data('layer_A', id, timeseries, basin_id)
                bd = generate_box_dataset(timeseries)
                box_data = sb.OutputBoxNumericDatasetVal()
                box_data.append_dataset([bd], basin_id)
                self.set_layer_data('layer_A', id, box_data, basin_id + ' (Resumen)')
            perc = 60 + int((s / 67) * 40)
            self.set_run_status(perc, 'Cargando resultados...')

    def _apply_modflow_layer_data(self, dir, model, type, prop_name):
        # Read MODFLOW cube dates
        dates = read_cube_dates(self.data_dir)
        # Read MODFLOW cube data
        if type == 'head':
            fn = os.path.join(dir, 'modflow', model, model.upper() + '_HEAD.BIN')
        else:
            fn = os.path.join(dir, 'modflow', model, model.upper() + '_DRAWDOWN.BIN')
        data = read_modflow_cube(fn)
        for r,c in data:
            self.set_layer_data(prop_name, (r,c), sb.TimseriesBaseVal(dates, data[(r,c)]))

    def _get_strategy_data_directory(self):
        hydro_option = self.get_input('input_0')
        irrigation_efficiency_option = self.get_input('input_1a_1')
        reservoir_option = self.get_input('input_1b_1')
        surface_water_apportionment_option = self.get_input('input_1c_1')

        a = hydro_option != 'Hidrología Histórica (1979-2016)'
        b = irrigation_efficiency_option
        c = reservoir_option != 'No Embalses'
        d = surface_water_apportionment_option

        n = 1
        if a:
            n += 1
        if b:
            n += 2
        if c:
            n += 4
        if d:
            n += 8

        print('SCEN-' + str(n).zfill(2))
        return 'SCEN-' + str(n).zfill(2)

    def _get_hydro_data_directory(self):
        hydro_option = self.get_input('input_0')

        if hydro_option != 'Clima Observado (1970-2016)':
            dir = 'HYDRO-OBS'
        else:
            dir = 'HYDRO-PRJ'

        return dir
