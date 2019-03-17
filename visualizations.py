from utils.highcharts import Highchart


class HCStemp(Highchart):
    setup = {}

    def __init__(self, data=None, title='New Highchart', **kwargs):
        super(HCStemp, self).__init__(**kwargs)
        self.set_dict_options(self.setup)
        self.set_options('title', {'text': title})
        if data is not None:
            series_type = self.setup.get('chart').get('type')
            self.add_pandas_data_set(data=data,
                                     series_type=series_type)


class HCTimeseries(HCStemp):
    setup = {
        'chart': {
            'type': 'line',
            'backgroundColor': 'rgba(255, 255, 255, 0.0)',
            'height': str(int(9 / 16 * 100)) + '%',  # 16:9 ratio
        },
        'title': {
            'text': '',
        },
        'subtitle': {
            'text': 'in GW'
        },
        'xAxis': {
            'type': 'datetime'
        },
        'yAxis': {
            'min': 0,
            'title': {'text': 'GW'}
        },
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle'
        },
    }


class HCPiechart(HCStemp):
    setup = {
        'chart': {
            'type': 'pie',
            'backgroundColor': 'rgba(255, 255, 255, 0.0)',
            'height': str(int(9 / 16 * 100)) + '%',
        },
        'title': {
            'text': '',
        },
        'subtitle': {
            'text': 'in GW'
        },
        'tooltip': {
            'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        'xAxis': {
            'type': 'datetime'
        },
        'yAxis': {
            'min': 0,
            'title': {'text': 'GW'}
        },
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle'
        },
    }

# TODO: Proper pie chart below doesn't work. Only pie chart above works,
#  which is a line chart (even if titled 'pie' chart)
# class HCPiechart(HCStemp):
#     setup = {
#         'chart': {
#             'plotBackgroundColor': 'null',
#             'plotBorderWidth': 'null',
#             'plotShadow': 'false',
#             'type': 'pie'
#         },
#         'title': {
#             'text': '',
#         },
#         'subtitle': {
#             'text': 'in GW'
#         },
#         'tooltip': {
#             'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
#         },
#         'plotOptions': {
#             'pie': {
#                 'allowPointSelect': 'true',
#                 'cursor': 'pointer',
#                 'dataLabels': {
#                     'enabled': 'true',
#                     'format': '<b>{point.name}</b>: {point.percentage:.1f} %',
#                     'style': {
#                         'color': "(Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'"
#                     }
#                 }
#             }
#         },
#     }
