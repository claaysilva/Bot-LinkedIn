from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
from random import uniform
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def digitar_devagar(campo, mensagem):
    for letra in mensagem:
        espera_aleatoria(0.1, 5 / 30)
        campo.send_keys(letra)


def espera_aleatoria(inicio=1.5, fim=3.0):
    sleep(uniform(inicio, fim))
