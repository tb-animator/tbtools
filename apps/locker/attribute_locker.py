__author__ = 'Tom'
import pymel.core as pm

def lockDrivers():
    allDrivers = pm.ls('*driver*', type='joint')

    for driver in allDrivers:
        print "locking", driver
        if "end" in driver.name():
            print "end"
            driver.rotate.lock()
            pm.setAttr(driver.rotate, channelBox = False)
            pm.setAttr(driver.rotate, keyable = False)
        driver.translate.lock()
        pm.setAttr(driver.translate, channelBox = False)
        pm.setAttr(driver.translate, keyable = False)
