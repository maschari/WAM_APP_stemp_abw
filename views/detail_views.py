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
            context['chart'] = self.build_chart(context['layer'])
            session.highcharts_temp = context['chart']
        else:
            context['chart'] = session.highcharts_temp
            session.highcharts_temp = None

        return context

    def build_chart(self, context):
        pop_2017 = context.mundata.pop_2017
        pop_2030 = context.mundata.pop_2030
        pop_2050 = context.mundata.pop_2050
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
    template_name = 'stemp_abw/popups/js_layer_popup_reg_mun_pop.html'


class RegMunPopDensityDetailView(MasterDetailView):
    model = models.RegMunPopDensity
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_pop_density.html'


class RegMunEnergyReElDemShareDetailView(MasterDetailView):
    model = models.RegMunEnergyReElDemShare
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_energy_re_el_dem_share.html'


class RegMunGenEnergyReDetailView(MasterDetailView):
    model = models.RegMunGenEnergyRe
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_gen_energy_re.html'


class RegMunGenEnergyRePerCapitaDetailView(MasterDetailView):
    model = models.RegMunGenEnergyRePerCapita
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_gen_energy_re_per_capita.html'


class RegMunGenEnergyReDensityDetailView(MasterDetailView):
    model = models.RegMunGenEnergyReDensity
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_gen_energy_re_density.html'


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
