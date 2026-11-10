{
   'name': 'Weather Notification',
   'version': '19.0.1.0.0',
   'category': 'Tools',
   'summary': 'Systray Icon',
   'description': """  """,
   'depends': ['base','web'],
    'data':[
        'security/ir.model.access.csv',
        'views/res_config_settings.xml'],
   'assets': {
       'web.assets_backend': [
           '/weather_notifictaion/static/src/xml/systray_icon.xml',
            '/weather_notifictaion/static/src/js/systray_icon.js',
       ],
   },
   'application': True,
   'installable': True,
   'auto_install': False,
}