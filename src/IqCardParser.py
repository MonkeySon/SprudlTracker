import requests
import lxml.html as lh

from FuelPoint import FuelPoint

def parse(config):

    BASE_URL = 'https://netservice.iqcard.at/'
    LOGIN_POST_URL = BASE_URL + 'de/login'
    LOGOUT_GET_URL = BASE_URL + 'de/logout'
    PREISINFO_GET_URL = BASE_URL + 'de/netservice_preisinfo'

    # Create session to keep cookies
    sess = requests.Session()

    # Update User-Agent
    sess.headers.update({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})

    # Initial GET request to base URL to get cookies
    resp = sess.get(BASE_URL)

    if(resp.status_code != 200):
        print(f'Initial GET request returned status code {resp.status_code}')
        return []

    # POST request with login credentials
    login_data = {
        'BENUID': config['username'],
        'PASSWT': config['password'],
        'login-form-submit': 'login'
    }
    resp = sess.post(LOGIN_POST_URL, data=login_data)

    # Check if login was correct and we landed on expected page
    if not resp.url.endswith('netservice'):
        print('Login failed!')
        return []

    # Go to "Preisinfo"
    resp = sess.get(PREISINFO_GET_URL)

    # Check Preismast
    tree = lh.fromstring(resp.content.decode('UTF-8'))
    diesel = float(tree.find_class('preismastDieselPreis')[0].text_content().replace(',', '.'))
    super = float(tree.find_class('preismastSuperPreis')[0].text_content().replace(',', '.'))
    super_plus = float(tree.find_class('preismastSuperplusPreis')[0].text_content().replace(',', '.'))
    points = [
        FuelPoint('IQ Card', 'Diesel', diesel),
        FuelPoint('IQ Card', 'Super', super),
        FuelPoint('IQ Card', 'Super Plus', super_plus)
    ]
    
    # Logout
    resp = sess.get(LOGOUT_GET_URL)

    # Return fuel points
    return points