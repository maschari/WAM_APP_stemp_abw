from django.shortcuts import HttpResponse, render
import json

#import sqlahelper

from stemp_abw.config import io
from stemp_abw.simulation.bookkeeping import simulate_energysystem
from stemp_abw import results

from stemp_abw.views.detail_views import *
from stemp_abw.views.serial_views import *
from stemp_abw.charts_data import visualizations1, visualizations2, visualizations4
from utils.widgets import InfoButton
from wam.settings import SESSION_DATA
from stemp_abw.sessions import UserSession
import os
import stemp_abw


def check_session(func):
    def func_wrapper(self, request, *args, **kwargs):
        try:
            session = SESSION_DATA.get_session(request)
        except KeyError:
            return render(request, 'stemp_abw/session_not_found.html')
        return func(self, request, session=session, *args, **kwargs)
    return func_wrapper


class IndexView(TemplateView):
    template_name = 'stemp_abw/index.html'


class MapView(TemplateView):
    template_name = 'stemp_abw/map.html'

    def __init__(self):
        super(MapView, self).__init__()

        #self.simulation = Simulation()

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(io.prepare_layer_data())
        context.update(io.prepare_component_data())
        context.update(io.prepare_label_data())

        # TODO: Temp stuff for WS
        context['visualizations1'] = visualizations1
        context['visualizations2'] = visualizations2
        context['visualizations4'] = visualizations4

        # Trial: new info button
        # TODO: Move
        file = os.path.join(os.path.dirname(stemp_abw.__file__), 'config', 'text', 'test.md')
        f = open(file, 'r', encoding='utf-8')
        context['info'] = InfoButton(text=f.read(),
                                     tooltip='tooltip hahaha',
                                     is_markdown=True,
                                     ionicon_type='ion-help-circled',
                                     ionicon_size='medium')
        f.close()

        return context

    def get(self, request, *args, **kwargs):
        # Start session (if there's none):
        SESSION_DATA.start_session(request, UserSession)
        session = SESSION_DATA.get_session(request)

        context = self.get_context_data()
        return self.render_to_response(context)

    @check_session
    def post(self, request, session):
        print(request.POST)

        result, param_result = simulate_energysystem()

        print('Results:', results)
        print('Params:', param_result)

        return HttpResponse(json.dumps({'hallo': 'test'}))


class SourcesView(TemplateView):
    template_name = 'stemp_abw/sources.html'
