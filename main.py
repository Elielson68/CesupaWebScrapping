from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from flask import Flask
from multiprocessing.pool import ThreadPool
import time

app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def WebScrapping(login_param, senha_param):
  driver = webdriver.Chrome(options=chrome_options)
  driver.get("http://www2.cesupa.br/TIA/aluno-on.asp")
  login_input = driver.find_element_by_id("cpf")
  senha_input = driver.find_element_by_id("senha")
  print(login_param)
  print(senha_param)
  login_input.send_keys(login_param)
  senha_input.send_keys(senha_param)
  senha_input.send_keys(Keys.RETURN)
  driver.get("http://www2.cesupa.br/TIA/bolnotafreq.asp")
  div_tabela = driver.find_element_by_class_name("conteudo2")
  tabela = div_tabela.find_element_by_tag_name("table")
  tbody = tabela.find_element_by_tag_name("tbody")
  linhas = tbody.find_elements_by_tag_name("tr")
  tabela_json = {}
  for i, linha in enumerate(linhas):
      colunas = linha.find_elements_by_tag_name("td")
      for ii, coluna in enumerate(colunas):
          if i == 0:
              titulo = coluna.text if "\n" not in coluna.text else coluna.text.replace("\n", " ")
              titulo = titulo.strip()
              tabela_json[titulo] = {}
          else:
              chaves = list(tabela_json.keys())
              titulo = chaves[ii] if "\n" not in chaves[ii] else chaves[ii].replace("\n", " ")
              if i == 1:
                  tabela_json[titulo] = []
              tabela_json[titulo].append(coluna.text.strip())
  driver.quit()
  return tabela_json
pool = ThreadPool(processes=2)


@app.route("/")
def ola():
  return "oi"

@app.route("/<string:login_param>/<string:senha_param>")
def home(login_param, senha_param):
  try:
    async_call = pool.apply_async(WebScrapping, (login_param, senha_param,))
    print('Processando....')
    return async_call.get()
  except:
    return "Houve algum erro :/"

app.run("0.0.0.0", 5000)