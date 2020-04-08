'''
Tipologia  y ciclo de la vida de los datos

@Author: Adonis Gonzalez Godoy y Eduard Tremps
------------------------------------------------
'''

from scrapping import *
from agents import *
import time
import sys
import argparse
import random
import os

# configuración de paths
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_DIR)
resources = os.path.join(ROOT_DIR, "../res")

# argument default
location = 'ATAL'

# Lista completa de puertos
#['ATAL', 'AGUI', 'SUCE', 'CROS', 'SANB', 'SSEB', 'SCOT', 'THET', 'USHU', 'BROW', 'CAMA',
# 'JUBA', 'ESPE', 'CBRE', 'LAMI', 'CPAU', 'SPAB', 'BBLA', 'OYAR', 'PCOL', 'EMAG', 'SROM',
# 'CALD', 'MAGA', 'NENY', 'ANUE', 'MAJO', 'MHER', 'TURB', 'PINA', 'PARG', 'BELG', 'BSAS',
# 'COMO', 'CHAR', 'PDES', 'FOST', 'IWHI', 'LPLA', 'MADR', 'MARD', 'MELC', 'NEKO', 'QUEQ',
# 'RAWS', 'RIOG', 'ROSA', 'SANT', 'SJUA', 'SJUL', 'SELE', 'VANC', 'LOYO', 'QUIL', 'RION',
# 'SCLE', 'SANF', 'STER']

if __name__ == '__main__':
    """"Funcion principal del programa, necesita como
        argumento el puerto del cual se quiere extraer
        la informacion. Los puertos se los identifica 
        por sus siglas.
     """
    parser = argparse.ArgumentParser(description='_Set Harbour to get data_')
    parser.add_argument('--location', required=False,
                        default=location,
                        metavar="nameHarbour",
                        help='ATAL')
    args = parser.parse_args()

    scrap = Scrapping('http://www.hidro.gob.ar')
    if (scrap.is_RobotsFile() == True):
        mapDisabled = scrap.get_Disallowed()
        for i in mapDisabled["Disallowed"]:
            if (str(i) == str('\'')):
                allowedScrapp = False
            else:
                allowedScrapp = True
    else:
        allowedScrapp = True

    if (allowedScrapp == True):
        scrap.set_ContentType('application/x-www-form-urlencoded')
        scrap.set_UserAgent('Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
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
        user_agent = Agents()
        user_agent_list = user_agent.get_UserAgentList()
        for i in month:
            scrap.set_SelectCombo(args.location, i)
            scrap.set_UserAgent(random.choice(user_agent_list))
            scrap.fill_Header()
            time.sleep(scrap.get_DelayRequest())
            result = scrap.get_BeautifulSoup()
            table = result.find('table')
            stats = scrap.get_StatsList(table)
            data = result.find_all('div', attrs={'class': 'row panels-row'})[0]
            map = scrap.get_ValuesMap(data)
            scrap.save_AsCSV(resources, map, i, stats)






