'''

Tipologia  y ciclo de la vida de los datos

'''
import requests
import logging
from bs4 import BeautifulSoup
import re
import json


class Scrapping:
    def __init__(self, url):
        self.__url = url
        self.__contentType = None
        self.__requestType = None
        self.__response = None
        self.__localidad = None
        self.__fMes = None
        self.__header = {}
        self.__formCombo = {}
        self.__logger = logging.getLogger()

    def get_BeautifulSoup(self):
        if not self.__formCombo:
            self.__logger.warning('No data in combo selection')
            return None
        else:
            x = requests.post(self.__response, data=self.__formCombo, headers=self.__header)
            return BeautifulSoup(x.text, 'html.parser')

    def set_ContentType(self, contentType):
        self.__contentType = contentType

    def set_ResquestType(self, requesType):
        self.__requestType = requesType

    def set_Response(self, response):
        self.__response = response

    def fill_Header(self):
        self.__header['Origin'] = self.__url
        self.__header['Content-Type'] = self.__contentType
        self.__header['X-Requested-With'] = self.__requestType
        self.__header['x-elastica_gw'] = '2.43.0'
        return self.__header

    def set_SelectCombo(self, place, month):
        self.__localidad = place
        self.__fMes = month
        self.__formCombo['Localidad'] = self.__localidad
        self.__formCombo['FMes'] = self.__fMes

    def get_SelectCombo(self):
        self.__formCombo['Localidad'] = self.__localidad
        self.__formCombo['FMes'] = self.__fMes
        return self.__formCombo

    def save_AsMap(self, path, map):
        with open(path + '/' + "dataset.json", "w") as outfile:
            # outfile.write(str(map))
            json.dump(map, outfile)
            print("File was saved in: ", path)
        print('saving')

    def get_ValuesMap(self, data):
        time, height, days, listValues = [], [], [], []

        for row in data.find_all('tr'):
            for x in row.find_all('td'):
                listValues.append(re.sub('[^A-Za-z0-9]+', "", str(x.string)))

        for i in listValues:
            if (len(i) == 2):
                days.append(i)
            if (len(i) == 3):
                height.append(i)
            if (len(i) == 4):
                time.append(i)

        return self.create_Map(time, height, days)

    def create_Map(self, time, height, days):
        a, b = {}, {}
        counter = 0
        index = 0
        dias = 1
        for i in days:
            for j in time:
                if (days.index(i) % 4 == 0):
                    a = ({str(time[counter]): str(height[counter])})
                    b.update(a.copy())
                    counter += 1
            break

        g, mapResult, t = {}, {}, {}
        for key in b:
            if (index < 4):
                g = {key: b[key]}
                t.update(g)
                index += 1

            if (index == 4):
                mapResult[str(dias)] = t.copy()
                g.clear()
                t.clear()
                dias += 1
                index = 0

        return mapResult

    def set_URL(self, url):
        self.__url = url

    def get_URL(self):
        return self.__url
