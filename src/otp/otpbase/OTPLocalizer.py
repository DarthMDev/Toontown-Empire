import string
import types

try:
    language = settings['language']
except:
    language = 'English'
#    language = 'Spanish'
#    language = 'Portuguese'

print 'OTPLocalizer: Running in language: %s' % language

from otp.otpbase.OTPLocalizerEnglish import *
#from otp.otpbase.OTPLocalizerSpanish import *
#from otp.otpbase.OTPLocalizerPortuguese import *

if language != 'English':
    l = {}
    g = {}
    module = 'otp.otpbase.OTPLocalizer' + language
    englishModule = __import__('otp.otpbase.OTPLocalizerEnglish', g, l)
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

'''
if language != 'Spanish':
    l = {}
    g = {}
    module = 'otp.otpbase.OTPLocalizer' + language
    spanishModule = __import__('otp.otpbase.OTPLocalizerSpanish', g, l)
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

    for key in foreignModule.__dict__.keys():
        if key not in spanishModule.__dict__:
            print 'WARNING: Foreign module: %s extra key: %s' % (module, key)


if language != 'Portuguese':
    l = {}
    g = {}
    module = 'otp.otpbase.OTPLocalizer' + language
    portugueseModule = __import__('otp.otpbase.OTPLocalizerPortuguese', g, l)
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

    for key in foreignModule.__dict__.keys():
        if key not in portugueseModule.__dict__:
            print 'WARNING: Foreign module: %s extra key: %s' % (module, key)
'''
