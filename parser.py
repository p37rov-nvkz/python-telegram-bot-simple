from bs4 import BeautifulSoup
import requests


AVR_URL = 'http://10.99.99.238/netmon/?city=Новокузнецк'
def get_alarm(url: str) -> list:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    row_3ddown = soup.findAll('tr', id='row_3ddown')
    row_down = soup.findAll('tr', id='row_down')
    alarms = row_3ddown + row_down
    results = []
    for alarm in alarms:
        rows = alarm.find_all('td')
        model = rows[2].text
        address = rows[3].text
        time = rows[5].text
        results.append([model, address, time])
    return results