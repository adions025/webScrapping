'''

Tipologia  y ciclo de la vida de los datos

'''
import requests
from bs4 import BeautifulSoup


class Scrapping:
    def __init__(self, url):
        self.__url = url
        self.__contentType = None
        self.__requestType = None
        self.__localidad = None
        self.__fMes = None
        self.__header = {}
        self.__formCombo = {}

    def get_BeautifulSoup(self):
        x = requests.post(self.__url, data=self.__formCombo, headers=self.__header)
        return BeautifulSoup(x.text, 'html.parser')

    def set_ContentType(self, contentType):
        self.__contentType = contentType

    def set_ResquestType(self, requesType):
        self.__requestType = requesType

    def get_Header(self):
        self.__header['url'] = self.__url
        self.__header['content-type'] = self.__contentType
        self.__header['requester'] = self.__requestType
        return self.__header

    def set_SelectCombo(self, place, month):
        self.__localidad = place
        self.__fMes = month

    def get_SelectCombo(self):
        self.__formCombo['Localidad'] = self.__localidad
        self.__formCombo['FMes'] = self.__fMes
        return self.__formCombo

    def set_URL(self, url):
        self.__url = url

    def get_URL(self):
        return self.__url

