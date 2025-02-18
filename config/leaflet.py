# Leaflet config: variable "LEAFLET_CONFIG" moved from settings.py to here
# since it conflicts with other apps using django-leaflet package.
# The leaflet config is now served via views.MapView() (uses settings override
# feature of django-leaflet)
# Related issue: https://github.com/rl-institut/WAM/issues/74

LEAFLET_CONFIG = {
    'TILES': [('Streets', 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoid2FtLXJsaSIsImEiOiJjanlpbTdsdXgwMHljM2JueGNrODZtbjB5In0.A7X6_rpw7hRehkulqMjpXw',
               {'attribution': 'Tiles: &copy; <a href="https://www.mapbox.com/about/maps/" target="_blank" rel="noopener noreferrer">mapbox</a>, Data: &copy; <a href="http://openstreetmap.org" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors (<a href="https://www.mapbox.com/map-feedback/#/-74.5/40/10" target="_blank" rel="noopener noreferrer">improve this map</a>), <a href="http://creativecommons.org/licenses/by-sa/2.0/" target="_blank" rel="noopener noreferrer">CC-BY-SA</a>',
                'id': 'mapbox.streets',
                'minZoom': 9,
                'maxZoom': 12,
                }
               ),
              ('OSM B&W', 'http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png',
               {'attribution': '&copy; <a href="http://openstreetmap.org" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/" target="_blank" rel="noopener noreferrer">CC-BY-SA</a>',
                'minZoom': 9,
                'maxZoom': 12,
                }
               ),
              ('OSM', 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
               {'attribution': '&copy; <a href="http://openstreetmap.org" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/" target="_blank" rel="noopener noreferrer">CC-BY-SA</a>',
                'minZoom': 9,
                'maxZoom': 12,
                }),
              ('OpenTopoMap', 'http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
               {'attribution': 'Tiles: &copy <a href="http://opentopomap.org" target="_blank" rel="noopener noreferrer">OpenTopoMap</a>, Data: &copy; <a href="http://openstreetmap.org" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/" target="_blank" rel="noopener noreferrer">CC-BY-SA</a>',
                'minZoom': 9,
                'maxZoom': 12,
                })
              ],
    'DEFAULT_CENTER': (51.834167, 12.237778),
    'DEFAULT_ZOOM': 10,
    'RESET_VIEW': False,
    'NO_GLOBALS': False
}
