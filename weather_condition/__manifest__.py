{
   'name': 'Weather Condition',
   'version': '19.0.1.0.0',
   'category': 'Tools',
   'summary': 'Systray Icon',
   'description': """  """,
   'depends': ['base','web'],
    'data':[
        'views/res_config_settings.xml'
    ],
   'assets': {
       'web.assets_backend': [
           '/weather_condition/static/src/xml/weather_condition.xml',
           '/weather_condition/static/src/xml/button_widget.xml',
           '/weather_condition/static/src/js/fetch_orders.js',
           '/weather_condition/static/src/js/weather_condition.js',
       ],
   },
   'application': True,
   'installable': True,
    'sequence':1,
   'auto_install': False,
}