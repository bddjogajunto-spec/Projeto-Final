# Behave para leitura do BDD
from behave import given, when, then
# Imports do selenium para acessar o site
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
# importa a exceção lançada quando o WebDriverWait expira (timeout)
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
# importa time para fazer esperas relacionadas ao relógio do computador
import time
# importa faker para realizar cadastros com dados falsos
from faker import Faker as fk
# importa pandas para demonstar dados de forma organizada no terminal
import pandas as pd
# importa os para acessar a pasta de evidencias
import os
# importa json para abrir arquivos de utilidade
import json
# acessa a pasta de funções comuns para importar a evidencia
from utils.utilitarios import evidencia, capturar_estado, verificar_mudanca



    print("🌐 Acessando página de login...")
    options=Options()
    options.add_argument("--Start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches",["enable-logging"])

    context.driver = Edge(options=options)
    context.driver.get("https://projetofinal.jogajuntoinstituto.org/")
    print("✅ Página carregada!")
    time.sleep(3)
