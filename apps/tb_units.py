import pymel.core as pm

# linear unit conversion
def unit_conversion():
    conversion = { 'mm': 0.1, 'cm': 1.0, 'm': 100.0, 'in': 2.54, 'ft': 30.48, 'yd': 91.44 }
    return conversion[pm.currentUnit(query=True, linear=True)]

# time unit conversion
def time_conversion():
    conversion = { 'game': 15, 'film': 24, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60 }
    return float(conversion[pm.currentUnit( query=True, time=True )])