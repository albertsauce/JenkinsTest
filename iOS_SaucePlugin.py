#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""This test assumes SAUCE_USERNAME and SAUCE_ACCESS_KEY are environment variables
set to your Sauce Labs username and access key."""

#importing the unittest python module that provides classes for test automation. 
import unittest 
#importing the time python module that supports time related functions.
import time
#importing the os module which provides a portable way of using operating system dependent functionality.
import os
#importing the sys module which provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
import sys
#importing the Appium Python bindings for Selenium Webdriver from the python Appium module.
from appium import webdriver
#importing the Selenium Python bindings for Selenium Webdriver from the python Selenium module.
from selenium import webdriver
#importing  the sauceclient which is a Python client library, used for accessing the Sauce Labs REST API to retrieve and update information about resources. 
import sauceclient
import json
import new

#Retreiving enviroment variables
SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')

#Credentials for SauceClient
test_result = sauceclient.SauceClient(SAUCE_USERNAME, SAUCE_ACCESS_KEY)

#Retreiving enviroment variables from Jenkins Plugin
host = os.environ.get('SELENIUM_HOST')
port = os.environ.get('SELENIUM_PORT')
platform = os.environ.get('SELENIUM_PLATFORM')
version = os.environ.get('SELENIUM_VERSION')
browser = os.environ.get('SELENIUM_BROWSER')
device = os.environ.get('SELENIUM_DEVICE')
deviceType = os.environ.get('SELENIUM_DEVICE_TYPE')
driver = os.environ.get('SELENIUM_DRIVER')
onDemandBrowsers = os.environ.get('SAUCE_ONDEMAND_BROWSERS')
url = os.environ.get('SELENIUM_URL')
userName = os.environ.get('SAUCE_USER_NAME')
apiKey = os.environ.get('SAUCE_API_KEY')
startingUrl = os.environ.get('SELENIUM_STARTING_URL')

print (host,port,platform,version,browser,device,deviceType,driver,onDemandBrowsers,url,userName,apiKey,startingUrl)

class AppiumMobileWebAppTest(unittest.TestCase):
    def setUp(self):

# When you select the platforms/browser in the plugin the plugin will set those values to a series of environment variables.
# You need to point your desired capabilities to these enviroment variables. Be careful, some of them can't be properly set by the plugin, so you will have to set it yourself.

# SELENIUM_HOST - The hostname of the Selenium server
# SELENIUM_PORT - The port of the Selenium server
# SELENIUM_PLATFORM - The operating system of the selected browser
# SELENIUM_VERSION - The version number of the selected browser
# SELENIUM_BROWSER - The browser name of the selected browser.
# SELENIUM_DEVICE - The device name of the selected browser (only available for mobile browsers)
# SELENIUM_DEVICE_TYPE - The device type of the selected browser (only available for Appium browsers)
# SELENIUM_DRIVER - Contains the operating system, version and browser name of the selected browser, in a format designed for use by the Selenium Client Factory
# SAUCE_ONDEMAND_BROWSERS - A JSON-formatted string representing the selected browsers
# SELENIUM_URL - The initial URL to load when the test begins
# SAUCE_USER_NAME - The user name used to invoke Sauce OnDemand
# SAUCE_API_KEY - The access key for the user used to invoke Sauce OnDemand
# SELENIUM_STARTING_URL - The value of the Starting URL field

        self.desired_capabilities = {}
        self.desired_capabilities['platformName'] = 'iOS' #This desired capability can't be properly set by the Jenkins Sauce OnDemand Plugin"
        self.desired_capabilities['platformVersion'] = os.environ.get('SELENIUM_VERSION')
        self.desired_capabilities['deviceName'] = os.environ.get('SELENIUM_DEVICE')
        self.desired_capabilities['browserName'] = 'Safari' #This desired capability can't be properly set by the Jenkins Sauce OnDemand Plugin"
        self.desired_capabilities['appium-version'] = '1.3.6' #This desired capability can't be properly set by the Jenkins Sauce OnDemand Plugin"
        self.desired_capabilities['name'] = 'iOS Example from Jenkins with Sauce OnDemand Plugin'

        self.driver = webdriver.Remote(command_executor = ('http://' + SAUCE_USERNAME + ':' + SAUCE_ACCESS_KEY + '@ondemand.saucelabs.com:80/wd/hub'), desired_capabilities = self.desired_capabilities) 
        self.driver.implicitly_wait(30)    

    def test_https(self):
        self.driver.get('https://www.saucelabs.com')
        title = self.driver.title
        self.assertEquals("Sauce Labs: Selenium Testing, Mobile Testing, JS Unit Testing and More", title) 
        time.sleep(10)
        self.driver.get('http://www.theuselessweb.com/')
        title = self.driver.title
        self.assertEquals("The Useless Web", title) 
        time.sleep(10) 

    def tearDown(self):
        print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
        #using the sauce client to set the pass or fail flags for this test according to the assertions results.
        try:
            if sys.exc_info() == (None, None, None):
                test_result.jobs.update_job(self.driver.session_id, passed=True)
            else:
                test_result.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()

if __name__ == '__main__':
        unittest.main()
