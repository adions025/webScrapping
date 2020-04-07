from src.scrapping import Scrapping
import os
import sys
import argparse
import json

########################################################################
#                           PATH SETTINGS
########################################################################
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_DIR)
resources = os.path.join(ROOT_DIR, "../res")
'''
def get_StatsList(table):
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 6:
            pleamarMax = cells[0].find(text=True)
            pleamarMed = cells[1].find(text=True)
            bajamarBaj = cells[2].find(text=True)
            bajamarMed = cells[3].find(text=True)
            amplitudMax = cells[4].find(text=True)
            amplitudMed = cells[5].find(text=True)
    resultHeader = [pleamarMax, pleamarMed, bajamarBaj, bajamarMed, amplitudMax, amplitudMed]
    return resultHeader
'''

########################################################################
#                               MAIN
########################################################################
if __name__ == '__main__':
    location = 'BB'
    parser = argparse.ArgumentParser(description='_Set Harbour to get data_')
    parser.add_argument('--location', required=True,
                        default=location,
                        metavar="nameHarbour",
                        help='ATAL')
    args = parser.parse_args()

    scrap = Scrapping('http://www.hidro.gob.ar')
    scrap.set_ContentType('application/x-www-form-urlencoded')
    scrap.set_ResquestType('XMLHttpRequest')
    scrap.set_Response('http://www.hidro.gob.ar/oceanografia/Tmareas/Form_Tmareas.asp')
    scrap.fill_Header()

    scrap.set_SelectCombo("", "")
    result = scrap.get_BeautifulSoup()
    items = result.select('option[value]')

    harbor, month = [], []
    for item in items:
        if (len(item.get('value')) == 2):
            month.append(item.get('value'))
        else:
            harbor.append(item.get('value'))

    scrap.set_Response('http://www.hidro.gob.ar/oceanografia/Tmareas/RE_Mareas.asp')
    month = ['01']
    for i in month:
        scrap.set_SelectCombo('ATAL', i)
        #print ("====="*10)
        result = scrap.get_BeautifulSoup()
        #table = result.find('table')
        #resultList = get_StatsList(table)
        #print(resultList)
        data = result.find_all('div', attrs={'class': 'row panels-row'})[0]
        map = scrap.get_ValuesMap(data)

    parsed = json.loads('\"' + str(map) + '\"')
    scrap.save_AsMap(resources, parsed)


