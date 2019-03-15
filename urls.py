from collections import namedtuple

from django.urls import path, re_path
from djgeojson.views import GeoJSONLayerView
from django.views.decorators.cache import cache_page
from stemp_abw.app_settings import MAP_DATA_CACHE_TIMEOUT

from . import views
import inspect
from meta.models import Source
from meta.views import AppListView, AssumptionsView

app_name = 'stemp_abw'

# regular URLs
urlpatterns = [
    path('', views.IndexView.as_view(),
         name='index'),
    path('app/', views.MapView.as_view(),
         name='map'),
    path('imprint/', views.ImprintView.as_view(),
         name='imprint'),
    path('privacy_policy/', views.PrivacyPolicyView.as_view(),
         name='privacy_policy'),
    path('sources_old/', views.SourcesView.as_view(),
         name='sources_old'),
    # Source views from WAM with highlighting
    path('sources/', AppListView.as_view(app_name='stemp_abw',
                                         model=Source),
         name='sources'),
    path('assumptions/', AssumptionsView.as_view(app_name='stemp_abw'),
         name='assumptions'),
    ]

# search detail views classes and append to URLs
detail_views = {}
for name, obj in inspect.getmembers(views.detail_views):
    if inspect.isclass(obj):
        if issubclass(obj, views.detail_views.MasterDetailView):
            if obj.model is not None:
                detail_views[obj.model.name] = obj
urlpatterns.extend(
    path('popup/{}/<int:pk>/'.format(name), dview.as_view(),
         name='{}-detail'.format(name))
    for name, dview in detail_views.items()
)

# Test JS template view
# TODO: Generalize like above!
urlpatterns.extend(
    [path('popupjs/reg_mun/', views.RegMunDetailJsView.as_view(), name='reg_mun_popupjs'),
     path('popupjs/reg_mun_pop/', views.RegMunPopDetailJsView.as_view(), name='reg_mun_pop_popupjs'),
     path('popupjs/reg_mun_pop_density/', views.RegMunPopDensityDetailJsView.as_view(), name='reg_mun_pop_density_popupjs')]
)

# search JSON data views classes and append to URLs
data_views = {}
for name, obj in inspect.getmembers(views.serial_views):
    if inspect.isclass(obj):
        if issubclass(obj, GeoJSONLayerView):
            if obj.model is not None:
                data_views[obj.model.name] = obj
urlpatterns.extend(
    re_path(r'^{}.data/'.format(name),
            cache_page(MAP_DATA_CACHE_TIMEOUT)(sview.as_view()),
            name='{}.data'.format(name))
    for name, sview in data_views.items()
)
