import requests
import lxml.html as lh

from FuelPoint import FuelPoint

def parse(config):

    BASE_URL = 'https://netservice.iqcard.at/'
    LOGIN_POST_URL = BASE_URL + 'de/Kunden?handler=SignInDb'
    LOGOUT_GET_URL = BASE_URL + 'de/logout'
    PREISINFO_GET_URL = BASE_URL + 'de/netservice/Preisinfo'

    # Create session to keep cookies
    sess = requests.Session()

    # Update User-Agent
    sess.headers.update({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})

    # Initial GET request to base URL to get cookies
    resp = sess.get(BASE_URL)

    if(resp.status_code != 200):
        print(f'Initial GET request returned status code {resp.status_code}')
        return []

    req_verif_token = None

    # Parse RequestVerificationToken
    for line in resp.iter_lines(decode_unicode=True):
        if '__RequestVerificationToken' in line:
            line_parts = line.split('"')
            for i in range(len(line_parts)):
                if 'value' in line_parts[i]:
                    req_verif_token = line_parts[i+1]
                    break
            if req_verif_token:
                break

    if not req_verif_token:
        print('Could not parse RequestVerificationToken!')
        return []

    # POST request with login credentials
    login_data = {
        'Username': config['username'],
        'Password': config['password'],
        '__RequestVerificationToken': req_verif_token
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