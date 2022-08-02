import platform

puname = platform.uname()[0]

if puname == u'Darwin':
    SYSTEM = u'Darwin'
    SERVICE_TYPE = u'Darwin'
elif puname == u'Windows':
    SYSTEM = u'Windows'
    SERVICE_TYPE = u'Windows'
else:
    SYSTEM = u'Linux'

    SERVICE_TYPE = u'Initd'
