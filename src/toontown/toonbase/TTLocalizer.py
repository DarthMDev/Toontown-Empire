import string
import types

try:
    language = settings['language']
except:
    language = 'English'
#    language = 'Spanish'
#    language = 'Portuguese'

def getLanguage():
    return language

print 'TTLocalizer: Running in language: %s' % language
from toontown.toonbase.TTLocalizerEnglish import *
#from toontown.toonbase.TTLocalizerSpanish import *
#from toontown.toonbase.TTLocalizerPortuguese import *

if language != 'English':
    l = {}
    g = {}
    module = 'toontown.toonbase.TTLocalizer' + language
    englishModule = __import__('toontown.toonbase.TTLocalizerEnglish', g, l)
    foreignModule = __import__(module, g, l)
    for key, val in englishModule.__dict__.items():
        if key not in foreignModule.__dict__:
            print 'WARNING: Foreign module: %s missing key: %s' % (module, key)
            locals()[key] = val
        elif isinstance(val, types.DictType):
            fval = foreignModule.__dict__.get(key)
            for dkey, dval in val.items():
                if dkey not in fval:
                    print 'WARNING: Foreign module: %s missing key: %s.%s' % (module, key, dkey)
                    fval[dkey] = dval

            for dkey in fval.keys():
                if dkey not in val:
                    print 'WARNING: Foreign module: %s extra key: %s.%s' % (module, key, dkey)

    for key in foreignModule.__dict__.keys():
        if key not in englishModule.__dict__:
            print 'WARNING: Foreign module: %s extra key: %s' % (module, key)

'''
if language != 'Spanish':
    l = {}
    g = {}
    module = 'toontown.toonbase.TTLocalizer' + language
    spanishModule = __import__('toontown.toonbase.TTLocalizerSpanish', g, l)
    foreignModule = __import__(module, g, l)
    for key, val in spanishModule.__dict__.items():
        if key not in foreignModule.__dict__:
            print 'WARNING: Foreign module: %s missing key: %s' % (module, key)
            locals()[key] = val
        elif isinstance(val, types.DictType):
            fval = foreignModule.__dict__.get(key)
            for dkey, dval in val.items():
                if dkey not in fval:
                    print 'WARNING: Foreign module: %s missing key: %s.%s' % (module, key, dkey)
                    fval[dkey] = dval

            for dkey in fval.keys():
                if dkey not in val:
                    print 'WARNING: Foreign module: %s extra key: %s.%s' % (module, key, dkey)

    for key in foreignModule.__dict__.keys():
        if key not in spanishModule.__dict__:
            print 'WARNING: Foreign module: %s extra key: %s' % (module, key)


if language != 'Portuguese':
    l = {}
    g = {}
    module = 'toontown.toonbase.TTLocalizer' + language
    portugueseModule = __import__('toontown.toonbase.TTLocalizerPortuguese', g, l)
    foreignModule = __import__(module, g, l)
    for key, val in portugueseModule.__dict__.items():
        if key not in foreignModule.__dict__:
            print 'WARNING: Foreign module: %s missing key: %s' % (module, key)
            locals()[key] = val
        elif isinstance(val, types.DictType):
            fval = foreignModule.__dict__.get(key)
            for dkey, dval in val.items():
                if dkey not in fval:
                    print 'WARNING: Foreign module: %s missing key: %s.%s' % (module, key, dkey)
                    fval[dkey] = dval

            for dkey in fval.keys():
                if dkey not in val:
                    print 'WARNING: Foreign module: %s extra key: %s.%s' % (module, key, dkey)

    for key in foreignModule.__dict__.keys():
        if key not in portugueseModule.__dict__:
            print 'WARNING: Foreign module: %s extra key: %s' % (module, key)
'''
