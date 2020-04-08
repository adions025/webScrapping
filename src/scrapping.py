'''
Tipologia  y ciclo de la vida de los datos

@Author: Adonis Gonzalez Godoy y Eduard Tremps
----------------------------------------------

usage:
$python main.py [--h] [--location]

argumentos opcionales
--h: ayuda
--location: nombre del puerto
'''

import requests
import logging
from bs4 import BeautifulSoup
import re
import json
import time

class Scrapping:
    """"Clase Scrapping, contiene los metodos necesarios
        para la extracción de datos del estudio de mareas
        a lo largo de la vida fluvial. Esta clase permite
        la configuración del header, de los componentes
        de selección de la página como selectOptions, se
        encarga de devolver el objeto beautiful soup con
        los datos sin los tags html. Y permite guardar
        los datos en formato .CSV.
    """

    def __init__(self, url):
        """"Constructor, necesita una url, para crearse
            el objeto scrapping, se definen las variables
            y las estructras que se usaran.
        """
        self.__url = url
        self.__contentType = None
        self.__userAgent = None
        self.__response = None
        self.__localidad = None
        self.__fMes = None
        self.__delayRequest = None
        self.__header = {}
        self.__formCombo = {}
        self.__logger = logging.getLogger()

    def get_BeautifulSoup(self):
        """"Realiza la request a la url, con los dos mapas
            necesarios, el header y la informacion del
            comboselected. Devuelve un objeto Beatifulsoup.
        """
        if not self.__formCombo:
            self.__logger.warning('No data in combo selection')
            return None
        else:
            start_time = time.time()
            x = requests.get(self.__response, data=self.__formCombo, headers=self.__header)
            self.calc_DelayRequest(start_time)
            return BeautifulSoup(x.text, 'html.parser')

    def set_ContentType(self, contentType):
        """"Configura el tipo contenido para las solicitudes
            HTTP que los navegadores deben soportar en el
            header.
        """
        self.__contentType = contentType

    def set_UserAgent(self, userAgent):
        """"Configura el objeto para solicitar datos de un
            servidor web.
            :param userAgent
        """
        self.__userAgent = userAgent

    def set_Response(self, response):
        """Configura la url que devolvera los datos.
           :param response
        """
        self.__response = response

    def fill_Header(self):
        """Configura  estructura tipo map {} del encabezado
           de la solicutud HTTP.
        """
        self.__header['Content-Type'] = self.__contentType
        self.__header['User-Agent'] = self.__userAgent
        return self.__header

    def set_SelectCombo(self, place, month):
        """Configura la estructura tipo map {} del combo
           de la pagina web.
           :param place
           :param month
        """
        self.__localidad = place
        self.__fMes = month
        self.__formCombo['Localidad'] = self.__localidad
        self.__formCombo['FMes'] = self.__fMes

    def get_SelectCombo(self):
        """Devuelve la estructura tipo map {} del combo
           de la pagina web.
        """
        self.__formCombo['Localidad'] = self.__localidad
        self.__formCombo['FMes'] = self.__fMes
        return self.__formCombo

    def save_AsMap(self, path, map):
        """Guarda los datos en formato JSON, a partir de un
           diccionario compuesto por los datos, en el path
           especificado.
           :param path
           :param map
        """
        with open(path + '/' + "dataset.json", "w") as outfile:
            json.dump(map, outfile)

    def save_AsCSV(self, path, map, month, stats):
        """Guarda los datos en formato CSV, a partir de un
           diccionario compuesto por los datos, en el path
           especificado.
           :param path
           :param map
           :param month
           :param stats
        """
        with open(path + '/' + "dataset.csv", "a") as outfile:
            outfile.write(str('mes'+':'+month)+' '+str('h:m')+' '+str('altura')+' '+str('h:m')+' '+str('altura')
                          +' '+str('h:m')+' '+str('altura')+' '+str('h:m')+' '+str('altura'))
            outfile.write("\n")
            outfile.write("estadisticas"+" "+str('pleamar-maxima')+ " "+str('pleamar-media')+" "+str('bajamar-baja')
                          +" "+str('bajamar-media')+" "+str('ampl-maxima')+" "+str('ampl-media'))
            outfile.write("\n")
            outfile.write(" "+re.sub('[^A-Za-z0-9-:.]+', " ", str(stats)))
            outfile.write("\n")
            for i in map:
                a = (str(i) + str(re.sub('[^A-Za-z0-9-:.]+', " ", str(map[i]))))
                outfile.write(a.replace(" : ", " "))
                outfile.write("\n")
            outfile.write("\n")

    def get_ValuesMap(self, data):
        """Devuelve un map con los datos mejor organizados
           para guardarlos de la forma adecuada.
           :param data
        """
        listValues, all = [], []
        a, result = {}, {}

        for row in data.find_all('tr'):
            for x in row.find_all('td'):
                listValues.append(re.sub("[^A-Za-z0-9-:.]+", "", str(x.string)))

        for i in listValues:
            if (i == " "):
                listValues.remove(i)

        for i in listValues:
            if (len(i) == 2):
                value = i
                all = []
            else:
                all.append(i)
                a[value] = all
                result.update(a)
        return result

    def get_StatsList(self, table):
        """Devuelve una lista limpia a partir de los de las
           tablas de estadisticas HTML.
           :param table
        """
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

    def is_RobotsFile(self):
        """Comprueba si contiene el fichero robots.txt en la
           raiz.
        """
        response = requests.get(self.__url+"/robots.txt").status_code
        if (str(response) == "200"):
            contains = True
        else:
            contains = False
            self.__logger.warning("No contiene robots.txt")
        return contains

    def check_RobotsFile(self):
        """Devuelve el contenido del fichero robots.txt.
           No hace falta pasarlo a beatiful object ya que
           es un fichero txt.
        """
        response = requests.get(self.__url+"/robots.txt")
        return response.text

    def get_Disallowed(self):
        """Devuelve un map con el contenido desabilitado
           del fichero robots.txt.
        """
        resultMap = {"Disallowed": []}
        result = self.check_RobotsFile()
        for i in result.split("\n"):
            if i.startswith('Disallow'):
                resultMap["Disallowed"].append(i.split(': ')[1].split(' ')[0])
        return resultMap

    def calc_DelayRequest(self, startTimeRequest):
        """Se calcula el tiempo en que tarda en completar
           la request y se añade un valor proporcional al
           50% adicional de lo que tarda la peticion.
           Este valor puede ser modificado
           :param startTimeRequest
        """
        endTimeRequest = time.time() - startTimeRequest
        tmpTime = endTimeRequest * 0.5
        endTimeRequest = endTimeRequest + tmpTime
        self.__delayRequest = endTimeRequest

    def get_DelayRequest(self):
        """Devuelve el tiempo de retardo de la request
           que debe tomar entre peticiones masivas.
        """
        return self.__delayRequest

    def set_URL(self, url):
        """Configura la url
           :param url
        """
        self.__url = url
