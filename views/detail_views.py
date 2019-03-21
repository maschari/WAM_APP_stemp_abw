import stemp_abw.models as models
from django.views.generic import DetailView, TemplateView
from stemp_abw.app_settings import LABELS
from stemp_abw import visualizations
from wam.settings import SESSION_DATA
import pandas as pd


class MasterDetailView(DetailView):
    mode = None
    template_name = 'stemp_abw/popups/base_layer_popup.html'
    context_object_name = 'layer'

    def get_context_data(self, **kwargs):
        context = super(MasterDetailView, self).get_context_data(**kwargs)

        context['title'] = LABELS['layers'][self.model.name]['title']
        context['text'] = LABELS['layers'][self.model.name]['text']

        return context


####################
### Detail Views ### for popups
####################
class RpAbwBoundDetailView(MasterDetailView):
    model = models.RpAbwBound


class RegMunDetailView(MasterDetailView):
    model = models.RegMun


class RegMunPopMasterDetailView(MasterDetailView):

    def get_context_data(self, **kwargs):
        context = super(RegMunPopMasterDetailView, self).get_context_data(**kwargs)

        # backup current HC to session if view for html is requested,
        # load from session if subsequent view for js is requested.
        session = SESSION_DATA.get_session(self.request)
        if session.highcharts_temp is None:
            context['chart'] = self.build_chart()
            session.highcharts_temp = context['chart']
        else:
            context['chart'] = session.highcharts_temp
            session.highcharts_temp = None

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        pop_2017 = mun_data.pop_2017
        pop_2030 = mun_data.pop_2030
        pop_2050 = mun_data.pop_2050
        index = ['2017', '2030', '2050']
        data = pd.DataFrame(index=index, data={'Personen': [pop_2017, pop_2030, pop_2050]})
        setup_labels = {
            'title': {'text': 'Bevölkerungsentwicklung'},
            'subtitle': {'text': 'Prognose'},
            'yAxis': {'title': {'text': 'Personen'}}
        }
        vis_line_chart = visualizations.HCTimeseries(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block'
        )
        return vis_line_chart


class RegMunPopDetailView(RegMunPopMasterDetailView):
    model = models.RegMunPop
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_pop.html'


class RegMunPopDetailJsView(RegMunPopMasterDetailView):
    model = models.RegMunPop
    template_name = 'stemp_abw/popups/js_popup.html'


class RegMunPopDensityDetailView(MasterDetailView):
    model = models.RegMunPopDensity
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_pop_density.html'


class RegMunEnergyReElDemShareMasterDetailView(MasterDetailView):

    def get_context_data(self, **kwargs):
        context = super(RegMunEnergyReElDemShareMasterDetailView, self).get_context_data(**kwargs)

        # backup current HC to session if view for html is requested,
        # load from session if subsequent view for js is requested.
        session = SESSION_DATA.get_session(self.request)
        if session.highcharts_temp is None:
            context['chart'] = self.build_chart()
            session.highcharts_temp = context['chart']
        else:
            context['chart'] = session.highcharts_temp
            session.highcharts_temp = None

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        reg_mun_dem_el_energy = models.RegMunDemElEnergy.objects.get(pk=self.kwargs['pk'])
        wind = round(((mun_data.gen_el_energy_wind / 1e3) / reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        pv_roof = round(((mun_data.gen_el_energy_pv_roof / 1e3) / reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        pv_ground = round(((mun_data.gen_el_energy_pv_ground / 1e3) / reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        hydro = round(((mun_data.gen_el_energy_hydro / 1e3) / reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        data = pd.DataFrame(data={'EE-Träger': {'Wind': wind, 'PV Dach': pv_roof, 'PV Boden': pv_ground, 'Hydro': hydro}})
        setup_labels = {
            'title': {'text': 'EE-Erzeugung'},
            'subtitle': {'text': 'in Prozent zum Strombedarf'},
            'yAxis': {'title': {'text': 'Prozent'}},
            'tooltip': {
                'pointFormat': 'Bedarf: {point.stackTotal} %'
            }
        }
        vis_column_chart = visualizations.HCStackedColumn(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block'
        )
        return vis_column_chart


class RegMunEnergyReElDemShareDetailView(RegMunEnergyReElDemShareMasterDetailView):
    model = models.RegMunEnergyReElDemShare
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_energy_re_el_dem_share.html'


class RegMunEnergyReElDemShareDetailJsView(RegMunEnergyReElDemShareMasterDetailView):
    model = models.RegMunEnergyReElDemShare
    template_name = 'stemp_abw/popups/js_popup.html'




class RegMunGenEnergyReMasterDetailView(MasterDetailView):

    def get_context_data(self, **kwargs):
        context = super(RegMunGenEnergyReMasterDetailView, self).get_context_data(**kwargs)

        # backup current HC to session if view for html is requested,
        # load from session if subsequent view for js is requested.
        session = SESSION_DATA.get_session(self.request)
        if session.highcharts_temp is None:
            context['chart'] = self.build_chart()
            session.highcharts_temp = context['chart']
        else:
            context['chart'] = session.highcharts_temp
            session.highcharts_temp = None

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round((mun_data.gen_el_energy_wind / 1e3), 1)
        pv_roof = round((mun_data.gen_el_energy_pv_roof / 1e3), 1)
        pv_ground = round((mun_data.gen_el_energy_pv_ground / 1e3), 1)
        hydro = round((mun_data.gen_el_energy_hydro / 1e3), 1)
        data = pd.DataFrame({
            'name': ['Wind', 'PV Dach', 'PV Boden', 'Hydro'],
            'y': [wind, pv_roof, pv_ground, hydro]
        })
        data.set_index('name', inplace=True)
        # convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': 'Gewonnene Energie aus EE'},
            'subtitle': {'text': 'nach Quelle'},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} GWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} GWh<br>({point.percentage:.1f} %)'
            }
        }
        vis_column_chart = visualizations.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block'
        )
        return vis_column_chart


class RegMunGenEnergyReDetailView(RegMunGenEnergyReMasterDetailView):
    model = models.RegMunGenEnergyRe
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_gen_energy_re.html'


class RegMunGenEnergyReDetailJsView(RegMunGenEnergyReMasterDetailView):
    model = models.RegMunGenEnergyRe
    template_name = 'stemp_abw/popups/js_popup.html'




class RegMunGenEnergyRePerCapitaMasterDetailView(MasterDetailView):

    def get_context_data(self, **kwargs):
        context = super(RegMunGenEnergyRePerCapitaMasterDetailView, self).get_context_data(**kwargs)

        # backup current HC to session if view for html is requested,
        # load from session if subsequent view for js is requested.
        session = SESSION_DATA.get_session(self.request)
        if session.highcharts_temp is None:
            context['chart'] = self.build_chart()
            session.highcharts_temp = context['chart']
        else:
            context['chart'] = session.highcharts_temp
            session.highcharts_temp = None

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round((mun_data.gen_el_energy_wind / mun_data.pop_2017), 1)
        pv_roof = round((mun_data.gen_el_energy_pv_roof / mun_data.pop_2017), 1)
        pv_ground = round((mun_data.gen_el_energy_pv_ground / mun_data.pop_2017), 1)
        hydro = round((mun_data.gen_el_energy_hydro / mun_data.pop_2017), 1)
        data = pd.DataFrame({
            'name': ['Wind', 'PV Dach', 'PV Boden', 'Hydro'],
            'y': [wind, pv_roof, pv_ground, hydro]
        })
        data.set_index('name', inplace=True)
        # convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': 'Gewonnene Energie aus EE'},
            'subtitle': {'text': 'je EinwohnerIn'},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} MWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} MWh<br>({point.percentage:.1f} %)'
            }
        }
        vis_column_chart = visualizations.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block'
        )
        return vis_column_chart


class RegMunGenEnergyRePerCapitaDetailView(RegMunGenEnergyRePerCapitaMasterDetailView):
    model = models.RegMunGenEnergyRePerCapita
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_gen_energy_re_per_capita.html'


class RegMunGenEnergyRePerCapitaDetailJsView(RegMunGenEnergyRePerCapitaMasterDetailView):
    model = models.RegMunGenEnergyRePerCapita
    template_name = 'stemp_abw/popups/js_popup.html'




class RegMunGenEnergyReDensityMasterDetailView(MasterDetailView):

    def get_context_data(self, **kwargs):
        context = super(RegMunGenEnergyReDensityMasterDetailView, self).get_context_data(**kwargs)

        # backup current HC to session if view for html is requested,
        # load from session if subsequent view for js is requested.
        session = SESSION_DATA.get_session(self.request)
        if session.highcharts_temp is None:
            context['chart'] = self.build_chart()
            session.highcharts_temp = context['chart']
        else:
            context['chart'] = session.highcharts_temp
            session.highcharts_temp = None

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round((mun_data.gen_el_energy_wind / mun_data.area), 1)
        pv_roof = round((mun_data.gen_el_energy_pv_roof / mun_data.area), 1)
        pv_ground = round((mun_data.gen_el_energy_pv_ground / mun_data.area), 1)
        hydro = round((mun_data.gen_el_energy_hydro / mun_data.area), 1)
        data = pd.DataFrame({
            'name': ['Wind', 'PV Dach', 'PV Boden', 'Hydro'],
            'y': [wind, pv_roof, pv_ground, hydro]
        })
        data.set_index('name', inplace=True)
        # convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': 'Gewonnene Energie aus EE'},
            'subtitle': {'text': 'je km²'},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} MWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} MWh<br>({point.percentage:.1f} %)'
            }
        }
        vis_column_chart = visualizations.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block'
        )
        return vis_column_chart


class RegMunGenEnergyReDensityDetailView(RegMunGenEnergyReDensityMasterDetailView):
    model = models.RegMunGenEnergyReDensity
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_gen_energy_re_density.html'


class RegMunGenEnergyReDensityDetailJsView(RegMunGenEnergyReDensityMasterDetailView):
    model = models.RegMunGenEnergyReDensity
    template_name = 'stemp_abw/popups/js_popup.html'




class RegMunGenCapReDetailView(MasterDetailView):
    model = models.RegMunGenCapRe
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_gen_cap_re.html'


class RegMunGenCapReDensityDetailView(MasterDetailView):
    model = models.RegMunGenCapReDensity
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_gen_cap_re_density.html'


class RegMunGenCountWindDensityDetailView(MasterDetailView):
    model = models.RegMunGenCountWindDensity
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_gen_count_wind_density.html'


class RegMunDemElEnergyDetailView(MasterDetailView):
    model = models.RegMunDemElEnergy
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_dem_el_energy.html'


class RegMunDemElEnergyPerCapitaDetailView(MasterDetailView):
    model = models.RegMunDemElEnergyPerCapita
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_dem_el_energy_per_capita.html'


class RegMunDemThEnergyDetailView(MasterDetailView):
    model = models.RegMunDemThEnergy
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_dem_th_energy.html'


class RegMunDemThEnergyPerCapitaDetailView(MasterDetailView):
    model = models.RegMunDemThEnergyPerCapita
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_dem_th_energy_per_capita.html'


class RegWaterProtAreaDetailView(MasterDetailView):
    model = models.RegWaterProtArea


class RegBirdProtAreaDetailView(MasterDetailView):
    model = models.RegBirdProtArea


class RegBirdProtAreaB200DetailView(MasterDetailView):
    model = models.RegBirdProtAreaB200


class RegNatureProtAreaDetailView(MasterDetailView):
    model = models.RegNatureProtArea


class RegLandscProtAreaPartsDetailView(MasterDetailView):
    model = models.RegLandscProtAreaParts


class RegResidAreaDetailView(MasterDetailView):
    model = models.RegResidArea


class RegResidAreaB500DetailView(MasterDetailView):
    model = models.RegResidAreaB500


class RegPrioAreaFloodProtDetailView(MasterDetailView):
    model = models.RegPrioAreaFloodProt


class RegPrioAreaCultDetailView(MasterDetailView):
    model = models.RegPrioAreaCult


class RegForestDetailView(MasterDetailView):
    model = models.RegForest


class RegFFHProtAreaDetailView(MasterDetailView):
    model = models.RegFFHProtArea


class RegResidAreaB1000DetailView(MasterDetailView):
    model = models.RegResidAreaB1000


class GenWECDetailView(MasterDetailView):
    model = models.GenWEC


class GenPVGroundDetailView(MasterDetailView):
    model = models.GenPVGround


class RegPrioAreaWECDetailView(MasterDetailView):
    model = models.RegPrioAreaWEC


class RegDeadZoneHardDetailView(MasterDetailView):
    model = models.RegDeadZoneHard


class RegDeadZoneSoftDetailView(MasterDetailView):
    model = models.RegDeadZoneSoft


class RegFFHProtAreaBDetailView(MasterDetailView):
    model = models.RegFFHProtAreaB


class RegLandscProtAreaDetailView(MasterDetailView):
    model = models.RegLandscProtArea


class RegNatureParkDetailView(MasterDetailView):
    model = models.RegNaturePark


class RegBioReserveDetailView(MasterDetailView):
    model = models.RegBioReserve


class RegRetentAreaEcosysDetailView(MasterDetailView):
    model = models.RegRetentAreaEcosys


class RegPrioAreaNatureDetailView(MasterDetailView):
    model = models.RegPrioAreaNature


class RegNatureMonumDetailView(MasterDetailView):
    model = models.RegNatureMonum


class RegPrioAreaWaterDetailView(MasterDetailView):
    model = models.RegPrioAreaWater


class RegPrioAreaAgriDetailView(MasterDetailView):
    model = models.RegPrioAreaAgri


class RegRetentAreaAgriDetailView(MasterDetailView):
    model = models.RegRetentAreaAgri


class RegPrioAreaResDetailView(MasterDetailView):
    model = models.RegPrioAreaRes


class RegInfrasRailwayDetailView(MasterDetailView):
    model = models.RegInfrasRailway


class RegInfrasRoadDetailView(MasterDetailView):
    model = models.RegInfrasRoad


class RegInfrasHvgridDetailView(MasterDetailView):
    model = models.RegInfrasHvgrid


class RegInfrasAviationDetailView(MasterDetailView):
    model = models.RegInfrasAviation
