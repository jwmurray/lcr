#!/usr/bin/env python3

import logging
import requests
import json
import re
### New
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import time
import io
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

_LOGGER = logging.getLogger(__name__)
HOST = "churchofjesuschrist.org"
BETA_HOST = "beta.churchofjesuschrist.org"
LCR_DOMAIN = "lcr.churchofjesuschrist.org"


if _LOGGER.getEffectiveLevel() <= logging.DEBUG:
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1

class ChurchLogin():
    def __init__(self, username, password, browser='Chrome'):
        church_login_url = 'https://id.churchofjesuschrist.org/'
        # Store credentials for login
        self.username = username
        self.password = password
        if browser == 'Chrome':
            # Use chrome
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        elif browser == 'Firefox':
            # Set it to Firefox
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        
        self.driver.implicitly_wait(100)
        
        self.driver.get(church_login_url)
 
    def login(self):
        username_element = self.driver.find_element_by_id('okta-signin-username')
        username_element.send_keys(self.username) # Give keyboard input
 
        login_button = self.driver.find_element_by_id('okta-signin-submit')
        login_button.click() # Send mouse click
 
        password_element = self.driver.find_element_by_class_name('password-with-toggle')
        password_element.send_keys(self.password) # Give password as input too
        time.sleep(2)
        verify_button = self.driver.find_element_by_class_name("button.button-primary")

        self.driver.implicitly_wait(100)
        verify_button.click()
        # url = "https://lcr.churchofjesuschrist.org/services/report/members-moved-in/unit/259950/5?lang=eng"
        # response = self.driver.get(url)
        # footerLink = self.driver.find_element_by_class_name("footerLink")
        # Need better way to wait for page to load then the sleep in case internet is slower
        time.sleep(4)
    
    def get(self, url):
        # self.driver.implicitly_wait(100)
        self.driver.get(url)
        time.sleep(4)
        response_str = self.driver.find_element_by_xpath("//body").get_attribute('outerHTML')

        html_str = re.compile("\'?<body.*>(\[{.*}\]).*<\/body>\'?", re.DOTALL)
        matches = html_str.search(response_str)

        json_str = matches.group(1)
        return json_str

class InvalidCredentialsError(Exception):
    pass

class API():
    def __init__(self, username, password, unit_number, beta=False):
        self.unit_number = unit_number
        self.session = requests.Session()
        self.beta = beta
        self.host = BETA_HOST if beta else HOST

        self._login(username, password)


    def _login(self, user, password):
        _LOGGER.info("Logging in")

        request = self.session.get('https://{}'.format(LCR_DOMAIN))

        # Get authState parameter.
        text = request.text

        self.ch_login = ChurchLogin(username = user, password = password, browser = 'Chrome')
        self.ch_login.login()

        time.sleep(2)

        # authState = re.search('"authState":"([A-Za-z0-9]+)"', text).group(1)

        # request = self.session.post('https://login.churchofjesuschrist.org/api/authenticate/credentials',
        #                             json={
        #                                 'password': password,
        #                                 'username': user,
        #                                 'authState': authState
        #                             })

        # response = json.loads(request.text)
        # obssocookie = response['output']['cookies']['ObSSOCookie']
        # churchcookie = response['output']['cookies']['ChurchSSO']

        # self.session.cookies['ObSSOCookie'] = obssocookie
        # self.session.cookies['ChurchSSO'] = churchcookie

        # request = self.session.get('https://signin.churchofjesuschrist.org/login.html')
    def _make_request(self, request):
        if self.beta:
            request['cookies'] = {'clerk-resources-beta-terms': '4.1',
                                  'clerk-resources-beta-eula': '4.2'}

        url = request['url']
        # response = self.session.get(**request)
        response = self.ch_login.get(request['url'])
        # response = self.session.get(**request)
        # response = self.driver.get(**request)
        # url = "https://lcr.churchofjesuschrist.org/services/report/members-moved-in/unit/259950/5?lang=eng"
        # response =self.ch_login.get(url)
        # time.sleep(2)

        # response.raise_for_status() # break on any non 200 status
        # io.TextIOWrapper(response, encoding=response.headers.get_content_charset('utf-8')) as file:
        # result = json.load(file)
        time.sleep(2)
        return response

    def birthday_list(self, month, months=1):
        _LOGGER.info("Getting birthday list")
        request = {'url': 'https://{}/services/report/birthday-list'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng',
                              'month': month,
                              'months': months}}

        result = self._make_request(request)
        return result.json()


    def members_moved_in(self, months):
        _LOGGER.info("Getting members moved in")
        request = {'url': 'https://{}/services/report/members-moved-in/unit/{}/{}'.format(LCR_DOMAIN,
                                                                                                  self.unit_number,
                                                                                                  months),
                   'params': {'lang': 'eng'}}

        # result = self.ch_login
        result = self._make_request(request)
        pyList = json.loads(result)
        pyDict = pyList[0]
        return pyList


    def members_moved_out(self, months):
        _LOGGER.info("Getting members moved out")
        request = {'url': 'https://{}/services/report/members-moved-out/unit/{}/{}'.format(LCR_DOMAIN,
                                                                                                   self.unit_number,
                                                                                                   months),
                   'params': {'lang': 'eng'}}

        result = self._make_request(request)
        return result.json()


    def member_list(self):
        _LOGGER.info("Getting member list")
        request = {'url': 'https://{}/services/report/member-list'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng',
                              'unitNumber': self.unit_number}}

        result = self._make_request(request)
        return result.json()


    def individual_photo(self, member_id):
        """
        member_id is not the same as Mrn
        """
        _LOGGER.info("Getting photo for {}".format(member_id))
        request = {'url': 'https://{}/individual-photo/{}'.format(LCR_DOMAIN, member_id),
                   'params': {'lang': 'eng',
                              'status': 'APPROVED'}}

        result = self._make_request(request)
        scdn_url = result.json()['tokenUrl']
        return self._make_request({'url': scdn_url}).content


    def callings(self):
        _LOGGER.info("Getting callings for all organizations")
        request = {'url': 'https://{}/services/orgs/sub-orgs-with-callings'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng'}}

        result = self._make_request(request)
        return result.json()


    def members_alt(self):
        _LOGGER.info("Getting member list")
        request = {'url': 'https://{}/services/umlu/report/member-list'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng',
                              'unitNumber': self.unit_number}}

        result = self._make_request(request)
        return result.json()


    def ministering(self):
        """
        API parameters known to be accepted are lang type unitNumber and quarter.
        """
        _LOGGER.info("Getting ministering data")
        request = {'url': 'https://{}/services/umlu/v1/ministering/data-full'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng',
                              'unitNumber': self.unit_number}}

        result = self._make_request(request)
        return result.json()


    def access_table(self):
        """
        Once the users role id is known this table could be checked to selectively enable or disable methods for API endpoints.
        """
        _LOGGER.info("Getting info for data access")
        request = {'url': 'https://{}/services/access-table'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng'}}

        result = self._make_request(request)
        return result.json()

    def recommend_status(self):
        """
        Obtain member information on recommend status
        """
        _LOGGER.info("Getting recommend status")
        request = {
                'url': 'https://{}/services/recommend/recommend-status'.format(LCR_DOMAIN),
                'params': {
                    'lang': 'eng',
                    'unitNumber': self.unit_number
                    }
                }
        result = self._make_request(request)
        return result.json()
