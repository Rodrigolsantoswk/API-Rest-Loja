import os
import urllib
from dotenv import load_dotenv, dotenv_values, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from middleware import Middleware
import pyodbc

# Carrega e atribui os valores obtidos nas variáveis de ambiente
load_dotenv(find_dotenv())

# Requisita os valores das variáveis de ambiente do arquivo .env
config = dotenv_values(".env")

# Requisita as variáveis de ambiente
db_host = os.environ.get('server', default='localhost')
db_name = os.environ.get('database', default='notes')
db_port = os.environ.get('port', default='1433')
midd_user = os.environ.get('midduser', default='none')
midd_password = os.environ.get('middpassword', default='none')

app = Flask("appLoja")  # Inicia um novo Web Service
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Rastreio de models_committed e before_models_committed

# Formata a URI como uma string de consulta para URL
params = urllib.parse.quote_plus('Driver={SQL Server Native Client 11.0};Server=' + db_host + ';Database=' \
                                 + db_name + \
                                 ';Trusted_Connection=yes')

# Configura a URI da conexão com o MSSQLServer
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params

# Configura o Middleware enviando as variáveis de ambiente e o geteway da aplicação Flaks
app.wsgi_app = Middleware(midd_user, midd_password, app.wsgi_app)

# Carrega a variável db com o modelo da conexão iniciada anteriormente
db = SQLAlchemy(app)
