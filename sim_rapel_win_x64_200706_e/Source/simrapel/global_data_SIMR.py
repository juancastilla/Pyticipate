import core.scenario.global_data_base as gd
import core.scenario.scenario_base as sb

import datetime as dt
import os

import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from data_read import read_magic_timeseries, compute_time_series_average, generate_box_dataset, \
    read_modflow_balance_timeseries, read_modflow_global_balance_timeseries, read_modflow_timeseries

class GlobalData(gd.GlobalDataBase):

    def _set1_precanned_results(self, strategy_id):
        if strategy_id == 'HidroHist+IrriActual':
            data = { 'gw_heads_alhue' : 0.974478514008657, 'gw_heads_cachapoal' : 0.9991773002135914, 'gw_heads_tinguiririca' : 1.0115681333925854,
                     'irr_discharge' : 0.84177, 'basin_efficiency' : 1.10 }
        if strategy_id == 'TendClima+IrriActual':
            data = { 'gw_heads_alhue' : 0.9600536895891906, 'gw_heads_cachapoal' : 0.9793746680085386, 'gw_heads_tinguiririca' : 0.9738456269291834,
                     'irr_discharge' : 0.64811, 'basin_efficiency' : 1.03 }
        if strategy_id == 'HidroHist+IrriMejorada':
            data = { 'gw_heads_alhue' : 0.9752561411442218, 'gw_heads_cachapoal' : 0.9967494379039785, 'gw_heads_tinguiririca' : 1.0104035562925573,
                     'irr_discharge' : 0.97437, 'basin_efficiency' : 1.14 }
        if strategy_id == 'TendClima+IrriMejorada':
            data = { 'gw_heads_alhue' : 0.9614581651657276, 'gw_heads_cachapoal' : 0.9778171394284454, 'gw_heads_tinguiririca' : 0.9728601143662967,
                     'irr_discharge' : 0.79573, 'basin_efficiency' : 1.07 }
        if strategy_id == 'HidroHist+IrriActual+Embalses':
            data = { 'gw_heads_alhue' : 0.9749407423394947, 'gw_heads_cachapoal' : 1.0000523711849783, 'gw_heads_tinguiririca' : 1.0141497510098583,
                     'irr_discharge' : 0.86200, 'basin_efficiency' : 1.10 }
        if strategy_id == 'TendClima+IrriActual+Embalses':
            data = { 'gw_heads_alhue' : 0.9609645766368863, 'gw_heads_cachapoal' : 0.9810460959443308, 'gw_heads_tinguiririca' : 0.9770305338435439,
                     'irr_discharge' : 0.67993, 'basin_efficiency' : 1.03 }
        if strategy_id == 'HidroHist+IrriMejorada+Embalses':
            data = { 'gw_heads_alhue' : 0.9757090398615944, 'gw_heads_cachapoal' : 0.9979414464712494, 'gw_heads_tinguiririca' : 1.0130376553365399,
                     'irr_discharge' : 1.00000, 'basin_efficiency' : 1.14 }
        if strategy_id == 'TendClima+IrriMejorada+Embalses':
            data = { 'gw_heads_alhue' : 0.9626779874478131, 'gw_heads_cachapoal' : 0.9799377476168245, 'gw_heads_tinguiririca' : 0.9766483657208658,
                     'irr_discharge' : 0.83813, 'basin_efficiency' : 1.07 }
        if strategy_id == 'HidroHist+IrriActual+RAG':
            data = { 'gw_heads_alhue' : 0.9756187724522315, 'gw_heads_cachapoal' : 1.0289628594356928, 'gw_heads_tinguiririca' : 1.0916833805199688,
                     'irr_discharge' : 0, 'basin_efficiency' : 0.82 }
        if strategy_id == 'TendClima+IrriActual+RAG':
            data = { 'gw_heads_alhue' : 0.9681962687346591, 'gw_heads_cachapoal' : 1.0167660417778748, 'gw_heads_tinguiririca' : 1.0636182439483481,
                     'irr_discharge' : 0, 'basin_efficiency' : 0.72 }
        if strategy_id == 'HidroHist+IrriMejorada+RAG':
            data = { 'gw_heads_alhue' : 0.9731110280649806, 'gw_heads_cachapoal' : 1.0193350352744504, 'gw_heads_tinguiririca' : 1.0706830296501368,
                     'irr_discharge' : 0, 'basin_efficiency' : 0.92 }
        if strategy_id == 'TendClima+IrriMejorada+RAG':
            data = { 'gw_heads_alhue' : 0.9663541819061062, 'gw_heads_cachapoal' : 1.009179078191568, 'gw_heads_tinguiririca' : 1.0506067658410392,
                     'irr_discharge' : 0, 'basin_efficiency' : 0.83 }
        if strategy_id == 'HidroHist+IrriActual+Embalses+RAG':
            data = { 'gw_heads_alhue' : 0.9757425232863589, 'gw_heads_cachapoal' : 1.0286940343743005, 'gw_heads_tinguiririca' : 1.0919804871094603,
                     'irr_discharge' : 0, 'basin_efficiency' : 0.81 }
        if strategy_id == 'TendClima+IrriActual+Embalses+RAG':
            data = { 'gw_heads_alhue' : 0.9683242420553962, 'gw_heads_cachapoal' : 1.0168655222632923, 'gw_heads_tinguiririca' : 1.0638575525947056,
                     'irr_discharge' : 0, 'basin_efficiency' : 0.72 }
        if strategy_id == 'HidroHist+IrriMejorada+Embalses+RAG':
            data = { 'gw_heads_alhue' : 0.9727028515323372, 'gw_heads_cachapoal' : 1.0192334037673578, 'gw_heads_tinguiririca' : 1.0714154917638632,
                     'irr_discharge' : 0, 'basin_efficiency' : 0.92 }
        if strategy_id == 'TendClima+IrriMejorada+Embalses+RAG':
            data = { 'gw_heads_alhue' : 0.9664959813909274, 'gw_heads_cachapoal' : 1.0095131035609677, 'gw_heads_tinguiririca' : 1.0515352464687824,
                     'irr_discharge' : 0, 'basin_efficiency' : 0.82 }
        return data

    def _compute_indicator(self, ts):
        # Is (avg/min)/(max-min)
        total = 0
        sum = 0.0
        min = 1.0e18
        max = -1.0e18
        for i in range(len(ts.values)):
            v = ts.values[i]
            total += 1
            sum += v
            if v > max:
                max = v
            if v < min:
                min = v
        if total > 1:
            avg = sum / total
        else:
            avg = 0
        return (avg-min)/(max-min)

    def _init_filepaths(self):
        scenario_dir = os.path.abspath(os.path.dirname(__file__))
        self.data_dir = os.path.join(scenario_dir, 'data')

    def _define_strategy_info(self):
        strategy_info = {
            'HidroHist+IrriActual' : 'HidroHist + IrriActual',
            'TendClima+IrriActual' : 'TendClima + IrriActual',
            'HidroHist+IrriMejorada' : 'HidroHist + IrriMejorada',
            'TendClima+IrriMejorada' : 'TendClima + IrriMejorada',
            'HidroHist+IrriActual+Embalses' : 'HidroHist + IrriActual + Embalses',
            'TendClima+IrriActual+Embalses' : 'TendClima + IrriActual + Embalses',
            'HidroHist+IrriMejorada+Embalses' : 'HidroHist + IrriMejorada + Embalses',
            'TendClima+IrriMejorada+Embalses' : 'TendClima + IrriMejorada + Embalses',
            'HidroHist+IrriActual+RAG' : 'HidroHist + IrriActual + RAG',
            'TendClima+IrriActual+RAG' : 'TendClima + IrriActual + RAG',
            'HidroHist+IrriMejorada+RAG' : 'HidroHist + IrriMejorada + RAG',
            'TendClima+IrriMejorada+RAG' : 'TendClima + IrriMejorada + RAG',
            'HidroHist+IrriActual+Embalses+RAG' : 'HidroHist + IrriActual + Embalses + RAG',
            'TendClima+IrriActual+Embalses+RAG' : 'TendClima + IrriActual + Embalses + RAG',
            'HidroHist+IrriMejorada+Embalses+RAG' : 'HidroHist + IrriMejorada + Embalses + RAG',
            'TendClima+IrriMejorada+Embalses+RAG' : 'TendClima + IrriMejorada + Embalses + RAG'
            }
        for s in strategy_info:
            super().add_strategy_info(strategy_info[s], s)

    def _define_data_info(self):
        tree = []

        # Set 1
        st1 = gd.TreeEntry('Indicadores de impacto global para la Cuenca Rapel', 'st1')
        tree.append(st1)

        # Irrigation
        irr = gd.TreeEntry('Riego', 'irr')
        irr_pds = gd.TreeEntry('Porcentage de demanda satisfecha zona de riego', 'irr.pds')
        irr.add_child(irr_pds)
        irr_ids = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14]
        irr_vars = ['Qddo', 'Qafl', 'Qcanal', 'Qtotal', 'Qrie', 'Qderr', 'DS', 'Pds', 'Qper', 'Qret', 'ET']
        irr_var_names = ['Caudal demandado zona de riego', 'Caudal afluente zona de riego', 'Caudal disponible en canales',
                         'Caudal total disponible zona de riego', 'Caudal para riego', 'Caudal de derrames zona de riego',
                         'Demanda satisfecha zona de riego', 'Porcentage de demanda satisfecha zona de riego',
                         'Caudal percolado zona de riego', 'Caudal de retorno zona de riego', 'Evapotranspiración']
        for i in irr_ids:
            iid = 'ZR-' + str(i).zfill(2)
            irr_id = gd.TreeEntry(iid, 'irr.' + str(i))
            for j in range(len(irr_vars)):
                var = irr_vars[j]
                var_name = irr_var_names[j]
                irr_id_var = gd.TreeEntry(var_name, 'irr.' + str(i) + '.' + var)
                irr_id_var_ts = gd.TreeEntry('Series de tiempo', 'irr.' + str(i) + '.' + var + '.ts')
                irr_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'irr.' + str(i) + '.' + var + '.bx')
                irr_id_var.add_child(irr_id_var_ts)
                irr_id_var.add_child(irr_id_var_bx)
                irr_id.add_child(irr_id_var)
            irr.add_child(irr_id)
        tree.append(irr)

        # Node
        nod = gd.TreeEntry('Nodos', 'nod')
        nod_ids = [15, 16, 19, 20, 26, 31, 34, 39, 52, 53, 54, 59, 63, 64, 66, 70, 74, 75, 80, 81, 83]
        nod_vars = ['Qafl', 'Qsal', 'Qdef']
        nod_var_names = ['Caudal afluente nodo', 'Caudal de salida nodo', 'Caudal de deficit nodo']
        for n in nod_ids:
            nid = 'NO-' + str(n).zfill(2)
            nod_id = gd.TreeEntry(nid, 'nod.' + str(n))
            for j in range(len(nod_vars)):
                var = nod_vars[j]
                var_name = nod_var_names[j]
                nod_id_var = gd.TreeEntry(var_name, 'nod.' + str(n) + '.' + var)
                nod_id_var_ts = gd.TreeEntry('Series de tiempo', 'nod.' + str(n) + '.' + var + '.ts')
                nod_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'nod.' + str(n) + '.' + var + '.bx')
                nod_id_var.add_child(nod_id_var_ts)
                nod_id_var.add_child(nod_id_var_bx)
                nod_id.add_child(nod_id_var)
            nod.add_child(nod_id)
        tree.append(nod)

        # Hydro-electric
        hyd = gd.TreeEntry('Hidroelectricas', 'hydro')
        hyd_ids = [1, 2, 4, 6, 7, 8]
        hyd_id_names = {1: 'Coya', 2:'Pangal', 4:'Sauzalito', 6:'La Confluencia', 7:'La Higuera', 8:'Chacayes'}
        hyd_vars = ['Qcap', 'Energia']
        hyd_var_names = ['Caudal captado central de pasada', 'Energia']
        for h in hyd_ids:
            id_name = hyd_id_names[h]
            hyd_id = gd.TreeEntry(id_name, 'hyd.' + str(h))
            for j in range(len(hyd_vars)):
                var = hyd_vars[j]
                var_name = hyd_var_names[j]
                hyd_id_var = gd.TreeEntry(var_name, 'hyd.' + str(h) + '.' + var)
                hyd_id_var_ts = gd.TreeEntry('Series de tiempo', 'hyd.' + str(h) + '.' + var + '.ts')
                hyd_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'hyd.' + str(h) + '.' + var + '.bx')
                hyd_id_var.add_child(hyd_id_var_ts)
                hyd_id_var.add_child(hyd_id_var_bx)
                hyd_id.add_child(hyd_id_var)
            hyd.add_child(hyd_id)
        tree.append(hyd)

        # Reservoirs
        res = gd.TreeEntry('Embalse', 'res')
        res_ids = [1, 2, 3, 4, 5, 6]
        res_id_names = {1: 'Sauzal', 2:'Rapel', 3:'Convento Viejo', 4:'Bollenar', 5:'Las Cayanas', 6:'Rio Claro'}
        res_vars = ['Qddo', 'Qafl', 'Qrb', 'Vuf']
        res_var_names = ['Caudal demandado embalse', 'Caudal afluente embalse', 'Caudal rebases embalse', 'Volúmen útil final embalse']
        for r in res_ids:
            rname = res_id_names[r]
            res_id = gd.TreeEntry(rname, 'res.' + str(r))
            for j in range(len(res_vars)):
                var = res_vars[j]
                var_name = res_var_names[j]
                res_id_var = gd.TreeEntry(var_name, 'res.' + str(r) + '.' + var)
                res_id_var_ts = gd.TreeEntry('Series de tiempo', 'res.' + str(r) + '.' + var + '.ts')
                res_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'res.' + str(r) + '.' + var + '.bx')
                res_id_var.add_child(res_id_var_ts)
                res_id_var.add_child(res_id_var_bx)
                res_id.add_child(res_id_var)
            res.add_child(res_id)
        tree.append(res)

        # River Reaches
        rch = gd.TreeEntry('Tramos de río', 'rch')
        rch_ids = [15, 16, 26, 52, 63, 64]
        rch_id_names = {15: 'Tramo Cachapoal Sector El Olivar 1', 16:'Tramo Cachapoal Sector El Olivar 2', 26:'Tramo Rio Claro Sector Rengo',
                       52:'Tramo Rio Claro Sector San Fernando', 63:'Tramo Rio Tinguiririca Sector Palmilla-Marchigue 1', 64:'Tramo Rio Tinguiririca Sector Palmilla-Marchigue 2'}
        rch_vars = ['Qper']
        rch_var_names = ['Caudal percolado tramo de río']
        for r in rch_ids:
            rname = rch_id_names[r]
            rch_id = gd.TreeEntry(rname, 'rch.' + str(r))
            for j in range(len(rch_vars)):
                var = rch_vars[j]
                var_name = rch_var_names[j]
                rch_id_var = gd.TreeEntry(var_name, 'rch.' + str(r) + '.' + var)
                rch_id_var_ts = gd.TreeEntry('Series de tiempo', 'rch.' + str(r) + '.' + var + '.ts')
                rch_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'rch.' + str(r) + '.' + var + '.bx')
                rch_id_var.add_child(rch_id_var_ts)
                rch_id_var.add_child(rch_id_var_bx)
                rch_id.add_child(rch_id_var)
            rch.add_child(rch_id)
        tree.append(rch)

        # Aquifers
        aqu = gd.TreeEntry('Acuíferos', 'aqu')
        aqu_glob_ids = ['Alhué', 'Cachapoal', 'Tinguiririca']
        aqu_ids = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        aqu_vars = ['Total Out', 'River Leakage Out', 'Wells Out', 'Constant Head Out', 'Storage Out',
                    'Total In', 'Recharge In', 'River Leakage In', 'Wells In', 'Constant Head In', 'Storage In']
        aqu_var_names = ['Salidas totales', 'Afloramiento ríos', 'Bombeo pozos', 'Conexiones subteráneas de salida',
                         'Ganancia de almacenamiento', 'Entradas totales', 'Recarga superficial', 'Pérdidas ríos',
                         'Entradas laterales', 'Conexiones subteráneas de entrada', 'Pérdida de almacenamiento']
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
        for a in aqu_glob_ids:
            aqu_id = gd.TreeEntry(str(a), 'aqu.' + str(a))
            for j in range(len(aqu_vars)):
                var = aqu_vars[j]
                var_name = aqu_var_names[j]
                aqu_id_var = gd.TreeEntry(var_name, 'aqu.' + str(a) + '.' + var)
                aqu_id_var_ts = gd.TreeEntry('Series de tiempo', 'aqu.' + str(a) + '.' + var + '.ts')
                aqu_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'aqu.' + str(a) + '.' + var + '.bx')
                aqu_id_var.add_child(aqu_id_var_ts)
                aqu_id_var.add_child(aqu_id_var_bx)
                aqu_id.add_child(aqu_id_var)
            aqu.add_child(aqu_id)
        for a in aqu_ids:
            aid = 'AC-' + str(a).zfill(2)
            aqu_id = gd.TreeEntry(aid, 'aqu.' + str(a))
            for j in range(len(aqu_vars)):
                var = aqu_vars[j]
                var_name = aqu_var_names[j]
                aqu_id_var = gd.TreeEntry(var_name, 'aqu.' + str(a) + '.' + var)
                aqu_id_var_ts = gd.TreeEntry('Series de tiempo', 'aqu.' + str(a) + '.' + var + '.ts')
                aqu_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'aqu.' + str(a) + '.' + var + '.bx')
                aqu_id_var.add_child(aqu_id_var_ts)
                aqu_id_var.add_child(aqu_id_var_bx)
                aqu_id.add_child(aqu_id_var)
            if a in additional:
                for v in additional[a]:
                    aqu_id_var = gd.TreeEntry(v, 'aqu.' + str(a) + '.' + v)
                    aqu_id_var_ts = gd.TreeEntry('Series de tiempo', 'aqu.' + str(a) + '.' + v + '.ts')
                    aqu_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'aqu.' + str(a) + '.' + v + '.bx')
                    aqu_id_var.add_child(aqu_id_var_ts)
                    aqu_id_var.add_child(aqu_id_var_bx)
                    aqu_id.add_child(aqu_id_var)
            aqu.add_child(aqu_id)
        tree.append(aqu)

        # Wells
        wel = gd.TreeEntry('Pozos', 'wel')
        wel_alhue = ['OBS-9', 'OBS-8', 'OBS-7', 'OBS-3', 'OBS-14', 'OBS-13', 'OBS-12', 'OBS-11', 'OBS-10', 'OBS-1', 'LAGO 4', 'LAGO 3', 'LAGO 2', 'LAGO 1']
        wel_chacapoal = ['LA ROSA SOFRUCO 2', 'LA ROSA SOFRUCO 1', 'INDURA GRANEROS', 'FUNDO SAN PEDRO', 'FUNDO LAS JUNTAS', 'FUNDO LA GRANJA',
            'FUNDO EL BOSQUE', 'FIAT CHILENA', 'CENTRO FRUTICOLA', 'BARRIO INDUSTRIAL', 'APR ZUGNIGA', 'APR TOQUIHUA', 'APR REQUEHUA', 'APR RASTROJOS',
            'APR PUNTA DE COR', 'APR PUEBLO DE', 'APR PANQUEHUE', 'APR OLIVAR BAJO', 'APR MOLINOS QUE', 'APR LOS BOLDOS', 'APR LO DE LOBOS',
            'APR LO CARTAGENA', 'APR LA COMPAGNIA', 'APR HUILQUIO DE', 'APR EL TAMBO', 'APR EL RULO', 'APR EL ABRA', 'APR CORCOLEN', 'APR COPEQUEN',
            'APR CERRO PUEBLO', 'APR CARACOLES', 'AP ROSARIO', 'AP REQUINOA', 'AP RANCAGUA SANC', 'AP RANCAGUA MEMB', 'AP QUINTA DE TIL', 'AP PEUMO',
            'AP PELEQUEN', 'AP MALLOA', 'AP LO MIRANDA', 'AP LAS CABRAS', 'AP GRANEROS', 'AP EL OLIVAR', 'AP COINCO']
        wel_tinguiririca = ['VIGNA SANTA ELISA', 'VIGNA SAN LUIS', 'RINC DE HALCONES', 'MATADERO MARCHIG', 'INACAP SN FERNANDO', 'FUNDO TOLHUEN',
            'FUNDO TALCAREHUE', 'FUNDO STA TERESA', 'FDOSNJOSEMARCHI', 'FDO STA VIRGINIA', 'FDO STA EUGENIA', 'FDO SN JOSE_BOLDO', 'FDO SAN ENRIQUE',
            'FDO LA TUNA', 'FDO LA MACARENA', 'FDO EL RECREO', 'ENAP SN FERNANDO', 'ASENT U_CAMPESINA', 'ASENT SN CORAZON', 'ASENT SAN ISIDRO',
            'ASENT LAS GARZAS', 'ASENT LA PUERTA', 'ASENT LA PATAGUA', 'ASENT EL TRIUNFO', 'ASENT AGUA SANTA', 'ASENT 21 DE MAYO 3', 'ASENT 21 DE MAYO 2',
            'APRCUESTALOGONZAL', 'APR TRES PUENTES', 'APR TINGUIRIRICA', 'APR ROMA SN JOSE', 'APR ROMA ARRIBA', 'APR QUINAHUE', 'APR PUQUILLAY',
            'APR POLONIA', 'APR LA FINCA', 'APR CUNACO', 'APR CONVENTO VIEJO', 'APR CODEGUA', 'APR AUQUINCO', 'APR ANGOSTURA', 'APR AGUA BUENA',
            'AP SN FERNANDO', 'AP POBLACION', 'AP NANCAHUA', 'AP CHIMBARONGO']
        wel_vars = ['Carga hidráulica subterránea', 'Descensos agua subterránea']
        wel_al = gd.TreeEntry('Alhué', 'wel.al')
        for w in wel_alhue:
            wel_id = gd.TreeEntry(w, 'wel.al.' + str(w))
            for v in wel_vars:
                wel_id_var = gd.TreeEntry(v, 'wel.al.' + str(w) + '.' + v)
                wel_id_var_ts = gd.TreeEntry('Series de tiempo', 'wel.al.' + str(w) + '.' + v + '.ts')
                wel_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'wel.al.' + str(w) + '.' + v + '.bx')
                wel_id_var.add_child(wel_id_var_ts)
                wel_id_var.add_child(wel_id_var_bx)
                wel_id.add_child(wel_id_var)
            wel_al.add_child(wel_id)
        wel.add_child(wel_al)
        wel_ch = gd.TreeEntry('Chacapoal', 'wel.ch')
        for w in wel_chacapoal:
            wel_id = gd.TreeEntry(w, 'wel.ch.' + str(w))
            for v in wel_vars:
                wel_id_var = gd.TreeEntry(v, 'wel.ch.' + str(w) + '.' + v)
                wel_id_var_ts = gd.TreeEntry('Series de tiempo', 'wel.ch.' + str(w) + '.' + v + '.ts')
                wel_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'wel.ch.' + str(w) + '.' + v + '.bx')
                wel_id_var.add_child(wel_id_var_ts)
                wel_id_var.add_child(wel_id_var_bx)
                wel_id.add_child(wel_id_var)
            wel_ch.add_child(wel_id)
        wel.add_child(wel_ch)
        wel_ti = gd.TreeEntry('Tinguiririca', 'wel.ti')
        for w in wel_tinguiririca:
            wel_id = gd.TreeEntry(w, 'wel.ti.' + str(w))
            for v in wel_vars:
                wel_id_var = gd.TreeEntry(v, 'wel.ti.' + str(w) + '.' + v)
                wel_id_var_ts = gd.TreeEntry('Series de tiempo', 'wel.ti.' + str(w) + '.' + v + '.ts')
                wel_id_var_bx = gd.TreeEntry('Diagrama de caja (resumen 5 puntos)', 'wel.ti.' + str(w) + '.' + v + '.bx')
                wel_id_var.add_child(wel_id_var_ts)
                wel_id_var.add_child(wel_id_var_bx)
                wel_id.add_child(wel_id_var)
            wel_ti.add_child(wel_id)
        wel.add_child(wel_ti)
        tree.append(wel)

        super().add_data_info(tree)

    def __init__(self):
        super().__init__()
        self._init_filepaths()
        self._define_strategy_info()
        self._define_data_info()

    def get_data_for_id(self, strategy_ids, data_id):

        id_parts = data_id.split('.')

        if len(id_parts) > 0:
            if id_parts[0] == 'st1':
                return self._set1(strategy_ids)
            if id_parts[0] == 'irr':
                return self._irr(strategy_ids, id_parts[1:])
            if id_parts[0] == 'nod':
                return self._nod(strategy_ids, id_parts[1:])
            if id_parts[0] == 'hyd':
                return self._hyd(strategy_ids, id_parts[1:])
            if id_parts[0] == 'res':
                return self._res(strategy_ids, id_parts[1:])
            if id_parts[0] == 'rch':
                return self._rch(strategy_ids, id_parts[1:])
            if id_parts[0] == 'aqu':
                return self._aqu(strategy_ids, id_parts[1:])
            if id_parts[0] == 'wel':
                return self._wel(strategy_ids, id_parts[1:])

        return None

    def _set1(self, strategy_ids):
        type = 'Radar'

        # Special case: Only have variable 'Tasa de cambio caudales de riego' for non-MAR strategies
        # so we remove this variable from plot when non_MAR strategies comparison is attempted.
        contains_mar = False
        for sid in strategy_ids:
            if sid.endswith('RAG'):
                contains_mar = True
        if contains_mar:
            include_irr_discharge = False
        else:
            include_irr_discharge = True

        variables = ['Recarga Total Acuífero de Cachapoal', 'Recarga Total Acuífero de Tinguiririca',
                     'Energía producida en la cuenca Rapel (Centrales de pasada)', 'Cota espejo de agua Embalse Rapel',
                     'Tasa de cambio (espacial) nivel freático ALHUE', 'Tasa de cambio (espacial) nivel freático CACHAPOAL',
                     'Tasa de cambio (espacial) nivel freático TINGUIRIRICA', 'Eficiencia hídrica de la cuenca (salidas/entradas)']
        if include_irr_discharge:
            variables.append('Tasa de cambio caudales de riego')

        description = ('Los indicadores de impacto han sido normalizados para calcular la razón promedia de cambio en el tiempo en la simulación de cada escenario.<br>' +
            'El indicador de caudales de riego se refiere a cambios en las caudales totales que llegan a las zonas de riego de la cuenca.<br>' +
            'El indicador de eficiencia hídrica refiere a la diferencia entre las entradas y las salidas de la cuenca.')

        data = sb.OutputMultipleNumericDatasetVal()

        for sid in strategy_ids:
            strategy_dir = self._get_strategy_directory(sid)
            arr = []
            # Recharge Cachapoal
            rc_ts = read_modflow_global_balance_timeseries(strategy_dir, 'cachapoal', 'RECHARGE IN')
            rc_av = self._compute_indicator(rc_ts)
            arr.append(rc_av)
            # Recharge Tinguiririca
            rt_ts = read_modflow_global_balance_timeseries(strategy_dir, 'tinguiririca', 'RECHARGE IN')
            rt_av = self._compute_indicator(rt_ts)
            arr.append(rt_av)
            # Energy in basin
            power_ids = [1, 2, 4, 6, 7, 8]
            energy_avs = []
            for p in power_ids:
                code = 'CH-' + str(p).zfill(2)
                eb_ts = read_magic_timeseries(strategy_dir, code, 'Energia', 1e-6)# kW -> GW
                eb_av = self._compute_indicator(eb_ts)
                energy_avs.append(eb_av)
            arr.append(sum(energy_avs) / len(energy_avs))
            # Elevation in Rapel Reservior
            er_ts = read_magic_timeseries(strategy_dir, 'EM-03', 'Cota', 1e-1)# m -> 1/10m
            er_av = self._compute_indicator(er_ts)
            arr.append(er_av)
            # Get pre-canned results:
            results = self._set1_precanned_results(sid)
            # Delta GW Heads Alhue
            arr.append(results['gw_heads_alhue'])
            # Delta GW Heads Cachapoal
            arr.append(results['gw_heads_cachapoal'])
            # Delta GW Heads Tinguiririca
            arr.append(results['gw_heads_tinguiririca'])
            # Basin Efficiency
            arr.append(results['basin_efficiency'])
            if include_irr_discharge:
                # Delta Irrigation Discharges
                arr.append(results['irr_discharge'])            
            name = sid
            data.append_dataset(arr, name)
        return {
            'type' : type,
            'variables' : variables,
            'data' : data,
            'description' : description
            }

    def _irr(self, strategy_ids, id_parts):
        if len(id_parts) > 0:
            if id_parts[0] == 'pds':
                return self._irr_pds(strategy_ids)
            else:
                return self._irr_zones(strategy_ids, id_parts)

        return None

    def _irr_pds(self, strategy_ids):
        type = 'Radar'
        zone_numbers = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14]
        variables = []
        for zn in zone_numbers:
            zone_id = 'ZR-' + str(zn).zfill(2)
            variables.append(zone_id)
        data = sb.OutputMultipleNumericDatasetVal()
        
        # Special case: Cannot compare across MAR & non-MAR strategies
        # so we prevent direct comparison when attempted.
        contains_mar = False
        contains_non_mar = False
        for sid in strategy_ids:
            if sid.endswith('RAG'):
                contains_mar = True
            else:
                contains_non_mar = True
        if contains_mar and contains_non_mar:
            include_mar = False
        else:
            include_mar = True
        
        for sid in strategy_ids:
            if sid.endswith('RAG') and not include_mar:
                continue;
            strategy_dir = self._get_strategy_directory(sid)
            arr = []
            for zid in variables:
                ts = read_magic_timeseries(strategy_dir, zid, 'Pds', 100.0)
                av = compute_time_series_average(ts)
                arr.append(av)
            name = sid
            data.append_dataset(arr, name)
        return {
            'type' : type,
            'variables' : variables,
            'data' : data
            }

    def _irr_zones(self, strategy_ids, id_parts):
        if len(id_parts) < 3:
            return None

        irr_ids = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14]
        if int(id_parts[0]) not in irr_ids:
            return None
        irr_id = 'ZR-' + str(int(id_parts[0])).zfill(2)

        irr_var = id_parts[1]
        irr_type = id_parts[2]

        irr_var_names = {'Qddo': 'Caudal demandado zona de riego', 'Qafl': 'Caudal afluente zona de riego', 'Qcanal': 'Caudal disponible en canales',
                         'Qtotal': 'Caudal total disponible zona de riego', 'Qrie': 'Caudal para riego', 'Qderr': 'Caudal de derrames zona de riego',
                         'DS': 'Demanda satisfecha zona de riego', 'Pds': 'Porcentage de demanda satisfecha zona de riego',
                         'Qper': 'Caudal percolado zona de riego', 'Qret': 'Caudal de retorno zona de riego', 'ET': 'Evapotranspiración'}

        title = irr_id + ' - ' + irr_var_names[irr_var]

        if irr_type == 'ts':
            type = 'TimeSeries'
            units = '(m3/s)'
            if irr_var == 'Pds':
                units = '(%)'
            if irr_var == 'ET':
                units = '(mm)'
            display = sb.ChartDisplay('Fecha',units,3,title)
            data = sb.OutputMultipleNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                ts = read_magic_timeseries(strategy_dir, irr_id, irr_var)
                name = sid
                data.append_dataset(ts, name)
            return {
                'type' : type,
                'display': display,
                'data': data
            }

        if irr_type == 'bx':
            type = 'Box'
            units = '(m3/s)'
            if irr_var == 'Pds':
                units = '(%)'
            if irr_var == 'ET':
                units = '(mm)'
            display = sb.ChartDisplay(units, '',3,title)
            variables = []
            data = sb.OutputBoxNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                arr = []
                ts = read_magic_timeseries(strategy_dir, irr_id, irr_var)
                ds = generate_box_dataset(ts)
                arr.append(ds)
                name = str(sid)
                data.append_dataset(arr, name)
            return {
                'type' : type,
                'display' : display,
                'variables' : variables,
                'data' : data
            }

    def _nod(self, strategy_ids, id_parts):
        if len(id_parts) < 3:
            return None

        nod_ids = [15, 16, 19, 20, 26, 31, 34, 39, 52, 53, 54, 59, 63, 64, 66, 70, 74, 75, 80, 81, 83]
        if int(id_parts[0]) not in nod_ids:
            return None
        nod_id = 'NO-' + str(int(id_parts[0])).zfill(2)

        nod_var = id_parts[1]
        nod_type = id_parts[2]

        nod_var_names = {'Qafl': 'Caudal afluente nodo', 'Qsal': 'Caudal de salida nodo', 'Qdef': 'Caudal de deficit nodo'}

        title = nod_id + ' - ' + nod_var_names[nod_var]

        if nod_type == 'ts':
            type = 'TimeSeries'
            display = sb.ChartDisplay('Fecha','(m3/s)',3,title)
            data = sb.OutputMultipleNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                ts = read_magic_timeseries(strategy_dir, nod_id, nod_var)
                name = sid
                data.append_dataset(ts, name)
            return {
                'type' : type,
                'display': display,
                'data': data
            }

        if nod_type == 'bx':
            type = 'Box'
            display = sb.ChartDisplay('(m3/s)','',3,title)
            variables = []
            data = sb.OutputBoxNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                arr = []
                ts = read_magic_timeseries(strategy_dir, nod_id, nod_var)
                ds = generate_box_dataset(ts)
                arr.append(ds)
                name = str(sid)
                data.append_dataset(arr, name)
            return {
                'type' : type,
                'display' : display,
                'variables' : variables,
                'data' : data
            }

    def _hyd(self, strategy_ids, id_parts):
        if len(id_parts) < 3:
            return None

        hyd_ids = [1, 2, 4, 6, 7, 8]
        hyd_names = {1: 'Coya', 2:'Pangal', 4:'Sauzalito', 6:'La Confluencia', 7:'La Higuera', 8:'Chacayes'}
        if int(id_parts[0]) not in hyd_ids:
            return None
        hyd_id = 'CH-' + str(int(id_parts[0])).zfill(2)
        hyd_name = hyd_names[int(id_parts[0])]

        hyd_var = id_parts[1]
        hyd_type = id_parts[2]

        hyd_var_names = {'Qcap': 'Caudal captado central de pasada', 'Energia': 'Energia'}

        title = hyd_name + ' - ' + hyd_var_names[hyd_var]

        if hyd_type == 'ts':
            type = 'TimeSeries'
            units = '(m3/s)'
            if hyd_var == 'Energia':
                units = '(GW)'
            display = sb.ChartDisplay('Fecha',units,3,title)
            data = sb.OutputMultipleNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                if hyd_var == 'Energia':
                    ts = read_magic_timeseries(strategy_dir, hyd_id, hyd_var, 1e-6)
                else:
                    ts = read_magic_timeseries(strategy_dir, hyd_id, hyd_var)
                name = sid
                data.append_dataset(ts, name)
            return {
                'type' : type,
                'display': display,
                'data': data
            }

        if hyd_type == 'bx':
            type = 'Box'
            units = '(m3/s)'
            if hyd_var == 'Energia':
                units = '(GW)'
            display = sb.ChartDisplay(units, '',3,title)
            variables = []
            data = sb.OutputBoxNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                arr = []
                if hyd_var == 'Energia':
                    ts = read_magic_timeseries(strategy_dir, hyd_id, hyd_var, 1e-6)
                else:
                    ts = read_magic_timeseries(strategy_dir, hyd_id, hyd_var)
                ds = generate_box_dataset(ts)
                arr.append(ds)
                name = str(sid)
                data.append_dataset(arr, name)
            return {
                'type' : type,
                'display' : display,
                'variables' : variables,
                'data' : data
            }

    def _res(self, strategy_ids, id_parts):
        if len(id_parts) < 3:
            return None

        res_ids = [1, 2, 3, 4, 5, 6]
        res_names = {1: 'Sauzal', 2:'Rapel', 3:'Convento Viejo', 4:'Bollenar', 5:'Las Cayanas', 6:'Rio Claro'}
        if int(id_parts[0]) not in res_ids:
            return None
        res_id = 'EM-' + str(int(id_parts[0])).zfill(2)
        res_name = res_names[int(id_parts[0])]

        res_var = id_parts[1]
        res_type = id_parts[2]

        res_var_names = {'Qddo': 'Caudal demandado embalse', 'Qafl': 'Caudal afluente embalse', 'Qrb': 'Caudal rebases embalse', 'Vuf': 'Volúmen útil final embalse'}

        title = res_name + ' - ' + res_var_names[res_var]

        if res_type == 'ts':
            type = 'TimeSeries'
            units = '(m3/s)'
            if res_var == 'Vuf':
                units = '(Mm3)'
            display = sb.ChartDisplay('Fecha',units,3,title)
            data = sb.OutputMultipleNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                ts = read_magic_timeseries(strategy_dir, res_id, res_var)
                if ts != None:
                    name = sid
                    data.append_dataset(ts, name)
            return {
                'type' : type,
                'display': display,
                'data': data
            }

        if res_type == 'bx':
            type = 'Box'
            units = '(m3/s)'
            if res_var == 'Vuf':
                units = '(Mm3)'
            display = sb.ChartDisplay(units,'',3,title)
            variables = []
            data = sb.OutputBoxNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                arr = []
                ts = read_magic_timeseries(strategy_dir, res_id, res_var)
                if ts != None:
                    ds = generate_box_dataset(ts)
                    arr.append(ds)
                    name = str(sid)
                    data.append_dataset(arr, name)
            return {
                'type' : type,
                'display' : display,
                'variables' : variables,
                'data' : data
            }

    def _rch(self, strategy_ids, id_parts):
        if len(id_parts) < 3:
            return None

        rch_ids = [15, 16, 26, 52, 63, 64]
        rch_names = {15: 'Tramo Cachapoal Sector El Olivar 1', 16:'Tramo Cachapoal Sector El Olivar 2', 26:'Tramo Rio Claro Sector Rengo',
                       52:'Tramo Rio Claro Sector San Fernando', 63:'Tramo Rio Tinguiririca Sector Palmilla-Marchigue 1', 64:'Tramo Rio Tinguiririca Sector Palmilla-Marchigue 2'}
        if int(id_parts[0]) not in rch_ids:
            return None
        rch_id = 'TR-' + str(int(id_parts[0])).zfill(2)
        rch_name = rch_names[int(id_parts[0])]

        rch_var = id_parts[1]
        rch_type = id_parts[2]

        rch_var_names = {'Qper': 'Caudal percolado tramo de río'}
        title = rch_name + ' - ' + rch_var_names[rch_var]

        if rch_type == 'ts':
            type = 'TimeSeries'
            display = sb.ChartDisplay('Fecha','(m3/s)',3,title)
            data = sb.OutputMultipleNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                ts = read_magic_timeseries(strategy_dir, rch_id, rch_var)
                name = sid
                data.append_dataset(ts, name)
            return {
                'type' : type,
                'display': display,
                'data': data
            }

        if rch_type == 'bx':
            type = 'Box'
            display = sb.ChartDisplay('(m3/s)','',3,title)
            variables = []
            data = sb.OutputBoxNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                arr = []
                ts = read_magic_timeseries(strategy_dir, rch_id, rch_var)
                ds = generate_box_dataset(ts)
                arr.append(ds)
                name = str(sid)
                data.append_dataset(arr, name)
            return {
                'type' : type,
                'display' : display,
                'variables' : variables,
                'data' : data
            }

    def _aqu(self, strategy_ids, id_parts):
        if len(id_parts) < 3:
            return None

        aqu_glob_ids = ['Alhué', 'Cachapoal', 'Tinguiririca']
        if id_parts[0] in aqu_glob_ids:
            return self._aqu_gbl(strategy_ids, id_parts)

        aqu_ids = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        if int(id_parts[0]) in aqu_ids:
            return self._aqu_ind(strategy_ids, id_parts)

        return None

    def _aqu_gbl(self, strategy_ids, id_parts):
        aqu_dir_names = { 'Alhué' : 'alhue', 'Cachapoal' : 'cachapoal', 'Tinguiririca' : 'tinguiririca' }
        aqu_vars = ['Total Out', 'River Leakage Out', 'Wells Out', 'Constant Head Out', 'Storage Out',
                    'Total In', 'Recharge In', 'River Leakage In', 'Wells In', 'Constant Head In', 'Storage In']
        aqu_cols = ['TOTAL OUT', 'RIVER LEAKAGE OUT', 'WELLS OUT', 'CONSTANT HEAD OUT', 'STORAGE OUT',
                    'TOTAL IN', 'RECHARGE IN', 'RIVER LEAKAGE IN', 'WELLS IN', 'CONSTANT HEAD IN', 'STORAGE IN']
        aqu_id = id_parts[0]
        aqu_dir = aqu_dir_names[aqu_id]
        aqu_var = id_parts[1]
        index = aqu_vars.index(aqu_var)
        aqu_col = aqu_cols[index]
        aqu_type = id_parts[2]

        aqu_var_names = {'Total Out': 'Salidas totales', 'River Leakage Out': 'Afloramiento ríos', 'Wells Out': 'Bombeo pozos', 'Constant Head Out': 'Conexiones subteráneas de salida',
                         'Storage Out': 'Ganancia de almacenamiento', 'Total In': 'Entradas totales', 'Recharge In': 'Recarga superficial', 'River Leakage In': 'Pérdidas ríos',
                         'Wells In': 'Entradas laterales', 'Constant Head In': 'Conexiones subteráneas de entrada', 'Storage In': 'Pérdida de almacenamiento'}
        title = aqu_id + ' - ' + aqu_var_names[aqu_var]

        if aqu_type == 'ts':
            type = 'TimeSeries'
            display = sb.ChartDisplay('Fecha','(m3/s)',3,title)
            data = sb.OutputMultipleNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                ts = read_modflow_global_balance_timeseries(strategy_dir, aqu_dir, aqu_col)
                name = sid
                data.append_dataset(ts, name)
            return {
                'type' : type,
                'display': display,
                'data': data
            }

        if aqu_type == 'bx':
            type = 'Box'
            display = sb.ChartDisplay('(m3/s)','',3,title)
            variables = []
            data = sb.OutputBoxNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                arr = []
                ts = read_modflow_global_balance_timeseries(strategy_dir, aqu_dir, aqu_col)
                ds = generate_box_dataset(ts)
                arr.append(ds)
                name = str(sid)
                data.append_dataset(arr, name)
            return {
                'type' : type,
                'display' : display,
                'variables' : variables,
                'data' : data
            }

    def _aqu_ind(self, strategy_ids, id_parts):
        aqu_vars = ['Total Out', 'River Leakage Out', 'Wells Out', 'Constant Head Out', 'Storage Out',
                    'Total In', 'Recharge In', 'River Leakage In', 'Wells In', 'Constant Head In', 'Storage In']
        aqu_cols = ['Total OUT', 'RIVER LEAKAGE OUT', 'WELLS OUT', 'CONSTANT HEAD OUT', 'STORAGE OUT',
                    'Total IN', 'RECHARGE IN', 'RIVER LEAKAGE IN', 'WELLS IN', 'CONSTANT HEAD IN', 'STORAGE IN']
        aqu_id = 'AC-' + str(int(id_parts[0])).zfill(2)
        if id_parts[1] in aqu_vars:
            index = aqu_vars.index(id_parts[1])
            aqu_var = aqu_cols[index]
        else:
            aqu_var = id_parts[1]
        aqu_type = id_parts[2]

        aqu_var_names = {'Total OUT': 'Salidas totales', 'RIVER LEAKAGE OUT': 'Afloramiento ríos', 'WELLS OUT': 'Bombeo pozos', 'CONSTANT HEAD OUT': 'Conexiones subteráneas de salida',
                         'STORAGE OUT': 'Ganancia de almacenamiento', 'Total IN': 'Entradas totales', 'RECHARGE IN': 'Recarga superficial', 'RIVER LEAKAGE IN': 'Pérdidas ríos',
                         'WELLS IN': 'Entradas laterales', 'CONSTANT HEAD IN': 'Conexiones subteráneas de entrada', 'STORAGE IN': 'Pérdida de almacenamiento'}
        if aqu_var in aqu_var_names:
            title = aqu_id + ' - ' + aqu_var_names[aqu_var]
        else:
            title = aqu_id + ' - ' + aqu_var

        if aqu_type == 'ts':
            type = 'TimeSeries'
            display = sb.ChartDisplay('Fecha','(m3/s)',3,title)
            data = sb.OutputMultipleNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                ts = read_modflow_balance_timeseries(strategy_dir, aqu_id, aqu_var)
                name = sid
                data.append_dataset(ts, name)
            return {
                'type' : type,
                'display': display,
                'data': data
            }

        if aqu_type == 'bx':
            type = 'Box'
            display = sb.ChartDisplay('(m3/s)','',3,title)
            variables = []
            data = sb.OutputBoxNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                arr = []
                ts = read_modflow_balance_timeseries(strategy_dir, aqu_id, aqu_var)
                ds = generate_box_dataset(ts)
                arr.append(ds)
                name = str(sid)
                data.append_dataset(arr, name)
            return {
                'type' : type,
                'display' : display,
                'variables' : variables,
                'data' : data
            }

    def _wel(self, strategy_ids, id_parts):
        if len(id_parts) < 4:
            return None

        wel_names = { 'al' : 'Alhué', 'ch' : 'Cachapoal', 'ti' : 'Tinguiririca' } 
        wel_dirs = { 'al' : 'alhue', 'ch' : 'cachapoal', 'ti' : 'tinguiririca' }
        wel_varnames = { 'Carga hidráulica subterránea' : 'head', 'Descensos agua subterránea' : 'drawdown' }
        wel_aqu = id_parts[0]
        wel_id = id_parts[1]
        wel_var = id_parts[2]
        wel_type = id_parts[3]
        wel_name = wel_names[wel_aqu]
        wel_dir = wel_dirs[wel_aqu]
        wel_varname = wel_varnames[wel_var]

        title = wel_name + ' - ' + wel_id + ' - ' + wel_var

        if wel_type == 'ts':
            type = 'TimeSeries'
            display = sb.ChartDisplay('Fecha','(msnm)',3,title)
            data = sb.OutputMultipleNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                ts = read_modflow_timeseries(strategy_dir, wel_id, wel_dir, wel_varname)
                name = sid
                data.append_dataset(ts, name)
            return {
                'type' : type,
                'display': display,
                'data': data
            }

        if wel_type == 'bx':
            type = 'Box'
            display = sb.ChartDisplay('(msnm)','',3,title)
            variables = []
            data = sb.OutputBoxNumericDatasetVal()
            for sid in strategy_ids:
                strategy_dir = self._get_strategy_directory(sid)
                arr = []
                ts = read_modflow_timeseries(strategy_dir, wel_id, wel_dir, wel_varname)
                ds = generate_box_dataset(ts)
                arr.append(ds)
                name = str(sid)
                data.append_dataset(arr, name)
            return {
                'type' : type,
                'display' : display,
                'variables' : variables,
                'data' : data
            }

    def _get_strategy_directory(self, strategy_id):
        if strategy_id == 'HidroHist+IrriActual':
            id = '01'
        if strategy_id == 'TendClima+IrriActual':
            id = '02'
        if strategy_id == 'HidroHist+IrriMejorada':
            id = '03'
        if strategy_id == 'TendClima+IrriMejorada':
            id = '04'
        if strategy_id == 'HidroHist+IrriActual+Embalses':
            id = '05'
        if strategy_id == 'TendClima+IrriActual+Embalses':
            id = '06'
        if strategy_id == 'HidroHist+IrriMejorada+Embalses':
            id = '07'
        if strategy_id == 'TendClima+IrriMejorada+Embalses':
            id = '08'
        if strategy_id == 'HidroHist+IrriActual+RAG':
            id = '09'
        if strategy_id == 'TendClima+IrriActual+RAG':
            id = '10'
        if strategy_id == 'HidroHist+IrriMejorada+RAG':
            id = '11'
        if strategy_id == 'TendClima+IrriMejorada+RAG':
            id = '12'
        if strategy_id == 'HidroHist+IrriActual+Embalses+RAG':
            id = '13'
        if strategy_id == 'TendClima+IrriActual+Embalses+RAG':
            id = '14'
        if strategy_id == 'HidroHist+IrriMejorada+Embalses+RAG':
            id = '15'
        if strategy_id == 'TendClima+IrriMejorada+Embalses+RAG':
            id = '16'
        return os.path.join(self.data_dir, 'SCEN-' + id)
