{
   'name': 'Weather Notification',
   'version': '19.0.1.0.0',
   'category': 'Tools',
   'summary': 'Systray Icon',
   'description': """  """,
   'depends': ['web'],
   'assets': {
       'web.assets_backend': [
           'systray_icon/static/src/js/systray_icon.js',
           'systray_icon/static/src/xml/systray_icon.xml',
       ],
   },
   'application': True,
   'installable': True,
   'auto_install': False,
}