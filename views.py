from django.views.generic import TemplateView, DetailView
from djgeojson.views import GeoJSONLayerView
from django.shortcuts import HttpResponse
import json
import sqlahelper
from stemp_abw import oep_models
from .oep_models import WnAbwEgoDpHvmvSubstation
import stemp_abw.models as models
from stemp_abw.forms import LayerSelectForm
from stemp_abw.app_settings import LAYER_METADATA, LAYER_DEFAULT_STYLES
from collections import OrderedDict
from stemp_abw.simulation import Simulation
from stemp_abw import results


class IndexView(TemplateView):
    template_name = 'stemp_abw/index.html'


# def map(request):
#     #question = get_object_or_404(Question, pk=question_id)
#
#     session = sqlahelper.get_session()
#     query = session.query(oep_models.WnAbwEgoDpHvmvSubstation)
#     data = query.all()
#     # for id, row in data.iterrows():
#     #     HvMvSubstation(
#     #         subst_id=row['subst_id'],
#     #         geom=row['geom']
#     #     )#.save()
#
#     return render(request, 'stemp_abw/map.html', {'data': data}, )


class MapView(TemplateView):
    template_name = 'stemp_abw/map.html'
    layer_data = {}

    def __init__(self):
        super(MapView, self).__init__()
        self.prepare_layer_data()

        self.simulation = Simulation()

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(self.layer_data)
        # context['label'] = self.label

        # TODO: Temp stuff for WS
        labels1 = OrderedDict((
            ('Windenergie Erzeugung', ['Wind']),
            ('Photovoltaik Erzeugung', ['PV']),
            ('Bioenergie Erzeugung', ['Biomasse', 'Biogas'])
        ))
        visualizations1 = [results.ResultAnalysisVisualization(title=t, captions=c).visualize()
                          for t, c in labels1.items()]
        labels2 = {'Erzeugung': ['Strom', 'Wärme'],
                  'Bedarf': ['Strom', 'Wärme'],
                  'Erneuerbare Energien': ['Wind', 'Solar']
                  }
        visualizations2 = [results.ResultAnalysisVisualization(title=t, captions=c).visualize()
                          for t, c in labels2.items()]
        context['visualizations1'] = visualizations1
        context['visualizations2'] = visualizations2

        return context

    def post(self, request):
        print(request.POST)

        results = self.simulation.run()
        print(results)

        return HttpResponse(json.dumps({'hallo': 'test'}))

    def prepare_layer_data(self):

        #groups = {grp:{lay for lay in lays.keys()} for grp, lays in LAYER_METADATA.items()}

        # create layer list for AJAX data urls
        layer_list = {l:d['show'] for ls in LAYER_METADATA.values() for l, d in ls.items()}
        self.layer_data['layer_list'] = layer_list

        # create JSON for layer styles
        layer_style = {l:a['style'] for v in LAYER_METADATA.values() for l, a in v.items()}
        layer_style.update(LAYER_DEFAULT_STYLES)
        self.layer_data['layer_style'] = json.dumps(layer_style)

        # create layer groups for layer menu
        layer_groups = OrderedDict()
        for grp, layers in LAYER_METADATA.items():
            layer_groups[grp] = [LayerSelectForm(layers=layers)]
        self.layer_data['layer_groups'] = layer_groups


    # def get_data(self):
    #     return 'result'


    # class Meta:
    #
    #     model = MushroomSpot
    #model = WnAbwEgoDpHvmvSubstation

    # session = sqlahelper.get_session()
    # query = session.query(oep_models.WnAbwEgoDpHvmvSubstation)
    # data = query.all()
    # for id, row in data.iterrows():
    #     HvMvSubstation(
    #         subst_id=row['subst_id'],
    #         geom=row['geom']
    #     )#.save()

#########################
### GeoJSONLayerViews ###
#########################
class SubstData(GeoJSONLayerView):
    model = models.HvMvSubst
    # TODO: 'name' is used to load popup content in JS from view (build url).
    # TODO: Find smarter approach!
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class OsmPowerGenData(GeoJSONLayerView):
    model = models.OsmPowerGen
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RpAbwBoundData(GeoJSONLayerView):
    model = models.RpAbwBound
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegPrioAreaResData(GeoJSONLayerView):
    model = models.RegPrioAreaRes
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegWaterProtAreaData(GeoJSONLayerView):
    model = models.RegWaterProtArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegBirdProtAreaData(GeoJSONLayerView):
    model = models.RegBirdProtArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegBirdProtAreaB200Data(GeoJSONLayerView):
    model = models.RegBirdProtAreaB200
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegNatureProtAreaData(GeoJSONLayerView):
    model = models.RegNatureProtArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegLandscProtAreaData(GeoJSONLayerView):
    model = models.RegLandscProtArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegResidAreaData(GeoJSONLayerView):
    model = models.RegResidArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegResidAreaB500Data(GeoJSONLayerView):
    model = models.RegResidAreaB500
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegPrioAreaFloodProtData(GeoJSONLayerView):
    model = models.RegPrioAreaFloodProt
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


####################
### Detail Views ### for popups
####################
class SubstDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.HvMvSubst
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(SubstDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some substation content'

        return context


class OsmPowerGenDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.OsmPowerGen
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(OsmPowerGenDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some generator content'

        return context


class RpAbwBoundDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RpAbwBound
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RpAbwBoundDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegPrioAreaResDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegPrioAreaRes
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegPrioAreaResDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegWaterProtAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegWaterProtArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegWaterProtAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegBirdProtAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegBirdProtArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegBirdProtAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegBirdProtAreaB200DetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegBirdProtAreaB200
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegBirdProtAreaB200DetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegNatureProtAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegNatureProtArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegNatureProtAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegLandscProtAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegLandscProtArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegLandscProtAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegResidAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegResidArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegResidAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegResidAreaB500DetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegResidAreaB500
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegResidAreaB500DetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context

class RegPrioAreaFloodProtDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegPrioAreaFloodProt
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegPrioAreaFloodProtDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context

### OLD STUFF ###
class HvMvSubstDetailView(DetailView):
    template_name = 'stemp_abw/subst_detail.html'
    model = models.HvMvSubst
    context_object_name = 'subst'


class HvMvSubstView(TemplateView):
    template_name = 'stemp_abw/subst.html'
    model = models.HvMvSubst
    context_object_name = 'subst'

    #queryset = qs_results

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['data'] = HvMvSubst.objects.all()
    #     return context


# class LayerPopupView(TemplateView):
#     template_name = 'stemp_abw/layer_popup.html'
#     context_object_name = 'obj'
#
#     def __init__(self, xxx, **kwargs):
#         super(LayerPopupView, self).__init__(**kwargs)


