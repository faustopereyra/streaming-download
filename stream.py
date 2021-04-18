from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import time
import json
import m3u8

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

# driver = webdriver.Chrome()
# driver.get('https://twitch.tv')

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument('headless')
driver = webdriver.Chrome(desired_capabilities=caps, options=options)

button = driver.find_elements_by_xpath("//*[@id='close_entrance_terms']")[0]

button.click()


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']

    return response


while True:
    #print("in2")
    browser_log = driver.get_log('performance')
    events = [process_browser_log_entry(entry) for entry in browser_log]
    events = [
        event for event in events if 'Network.response' in event['method']
    ]

    for e in events:

        if not "response" in e['params']:
            break

        # if e['params']['response']['url'].endswith('.m3u8'):
        #     url = e['params']['response']['url']
        #     r1 = requests.get(url, stream=True)
        #     if (r1.status_code == 200):
        #         print("in", r1)
        #         master = m3u8.loads(r1.text)
        #         print(master.data["playlist"])
        # with open('./vid/testvod.txt', 'w') as f:
        #     for chunk in r1.iter_content(chunk_size=1024):
        #         f.write(chunk)

        if e['params']['response']['url'].endswith('.ts'):
            url = e['params']['response']['url']
            r1 = requests.get(url, stream=True)
            if (r1.status_code == 200):
                print("in")
                with open('./vid/testvod.mpeg', 'ab') as f:
                    for chunk in r1.iter_content(chunk_size=1024):
                        f.write(chunk)
            else:
                print("Received unexpected status code {}".format(
                    r1.status_code))

time.sleep(6)

driver.quit()