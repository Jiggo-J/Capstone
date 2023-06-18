
#Import the neccessary libraries 

import pandas as pd
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
from sklearn.ensemble import IsolationForest
import base64
import folium
from branca.colormap import linear
from streamlit_folium import folium_static
import plotly.graph_objects as go
import altair as alt

#We import the database

df = pd.read_excel('https://feacapstone.s3.amazonaws.com/Capstone+Database.xlsx', engine='openpyxl')



# Define the format_number function
def format_number(number):
    if isinstance(number, str):
        return number
    else:
        try:
            formatted_number = "{:,.2f}".format(float(number))
            return formatted_number
        except ValueError:
            return "Invalid Number"


#We rename all the columns as the excel is in Spanish

column_name_mapping = {
    'Nombre': 'Name',
    'Código NIF': 'Tax ID',
    'Número BvD': 'BvD Number',
    'Localidad': 'City',
    'Comunidad autónoma': 'Autonomous Community',
    'Código postal': 'Postal Code',
    'Dirección web': 'Website',
    'Provincia': 'Province',
    'País': 'Country',
    'Ultimo número empleados': 'Last Employee Count',
    'Capital social\nmil EUR': 'Share Capital (thousand EUR)',
    'Cotización Bolsa': 'Stock Market Price',
    'Ingresos de explotación\nmil EUR\n2022': 'Operating Revenues (thousand EUR) 2022',
    'Coordenadas X': 'X Coordinates',
    'Coordenadas Y': 'Y Coordinates',
    'Ingresos de explotación\nmil EUR\n2021': 'Operating Revenues (thousand EUR) 2021',
    'Ingresos de explotación\nmil EUR\n2020': 'Operating Revenues (thousand EUR) 2020',
    'Ingresos de explotación\nmil EUR\n2019': 'Operating Revenues (thousand EUR) 2019',
    'Ingresos de explotación\nmil EUR\n2018': 'Operating Revenues (thousand EUR) 2018',
    'Ingresos de explotación\nmil EUR\n2017': 'Operating Revenues (thousand EUR) 2017',
    'Ingresos de explotación\nmil EUR\n2016': 'Operating Revenues (thousand EUR) 2016',
    'Ingresos de explotación\nmil EUR\n2014': 'Operating Revenues (thousand EUR) 2014',
    'Ingresos de explotación\nmil EUR\n2015': 'Operating Revenues (thousand EUR) 2015',
    'Ingresos de explotación\nmil EUR\n2013': 'Operating Revenues (thousand EUR) 2013',
    'Ingresos de explotación\nmil EUR\n2012': 'Operating Revenues (thousand EUR) 2012',
    'Ingresos de explotación\nmil EUR\n2011': 'Operating Revenues (thousand EUR) 2011',
    'Ingresos de explotación\nmil EUR\n2010': 'Operating Revenues (thousand EUR) 2010',
    'EBITDA\nmil EUR\n2022': 'EBITDA (thousand EUR) 2022',
    'EBITDA\nmil EUR\n2021': 'EBITDA (thousand EUR) 2021',
    'EBITDA\nmil EUR\n2019': 'EBITDA (thousand EUR) 2019',
    'EBITDA\nmil EUR\n2020': 'EBITDA (thousand EUR) 2020',
    'EBITDA\nmil EUR\n2018': 'EBITDA (thousand EUR) 2018',
    'EBITDA\nmil EUR\n2017': 'EBITDA (thousand EUR) 2017',
    'EBITDA\nmil EUR\n2016': 'EBITDA (thousand EUR) 2016',
    'EBITDA\nmil EUR\n2015': 'EBITDA (thousand EUR) 2015',
    'EBITDA\nmil EUR\n2014': 'EBITDA (thousand EUR) 2014',
    'EBITDA\nmil EUR\n2013': 'EBITDA (thousand EUR) 2013',
    'EBITDA\nmil EUR\n2012': 'EBITDA (thousand EUR) 2012',
    'EBITDA\nmil EUR\n2011': 'EBITDA (thousand EUR) 2011',
    'EBITDA\nmil EUR\n2010': 'EBITDA (thousand EUR) 2010',
    "Resultado bruto\nmil EUR\n2022" : "Gross result (thousand EUR) 2022", 
    "Resultado bruto\nmil EUR\n2021" : "Gross result (thousand EUR) 2021", 
    "Resultado bruto\nmil EUR\n2020" : "Gross result (thousand EUR) 2020", 
    "Resultado bruto\nmil EUR\n2019" : "Gross result (thousand EUR) 2019", 
    "Resultado bruto\nmil EUR\n2018" : "Gross result (thousand EUR) 2018", 
    "Resultado bruto\nmil EUR\n2017" : "Gross result (thousand EUR) 2017", 
    "Resultado bruto\nmil EUR\n2016" : "Gross result (thousand EUR) 2016", 
    "Resultado bruto\nmil EUR\n2015" : "Gross result (thousand EUR) 2015", 
    "Resultado bruto\nmil EUR\n2014" : "Gross result (thousand EUR) 2014", 
    "Resultado bruto\nmil EUR\n2013" : "Gross result (thousand EUR) 2013", 
    "Resultado bruto\nmil EUR\n2012" : "Gross result (thousand EUR) 2012", 
    "Resultado bruto\nmil EUR\n2011" : "Gross result (thousand EUR) 2011", 
    "Resultado bruto\nmil EUR\n2010" : "Gross result (thousand EUR) 2010",
    "Ingresos financieros\nmil EUR\n2022": "Financial income (thousand EUR) 2022",
    "Ingresos financieros\nmil EUR\n2021": "Financial income (thousand EUR) 2021",
    "Ingresos financieros\nmil EUR\n2019": "Financial income (thousand EUR) 2019",
    "Ingresos financieros\nmil EUR\n2020": "Financial income (thousand EUR) 2020",
    "Ingresos financieros\nmil EUR\n2018": "Financial income (thousand EUR) 2018",
    "Ingresos financieros\nmil EUR\n2017": "Financial income (thousand EUR) 2017",
    "Ingresos financieros\nmil EUR\n2016": "Financial income (thousand EUR) 2016",
    "Ingresos financieros\nmil EUR\n2015": "Financial income (thousand EUR) 2015",
    "Ingresos financieros\nmil EUR\n2012": "Financial income (thousand EUR) 2012",
    "Ingresos financieros\nmil EUR\n2013": "Financial income (thousand EUR) 2013",
    "Ingresos financieros\nmil EUR\n2014": "Financial income (thousand EUR) 2014",
    "Ingresos financieros\nmil EUR\n2011": "Financial income (thousand EUR) 2011",
    "Ingresos financieros\nmil EUR\n2010": "Financial income (thousand EUR) 2010",
    "Resultado Explotación\nmil EUR\n2022": "Operating result (thousand EUR) 2022",
    "Resultado Explotación\nmil EUR\n2021": "Operating result (thousand EUR) 2021",
    "Resultado Explotación\nmil EUR\n2019": "Operating result (thousand EUR) 2019",
    "Resultado Explotación\nmil EUR\n2020": "Operating result (thousand EUR) 2020",
    "Resultado Explotación\nmil EUR\n2018": "Operating result (thousand EUR) 2018",
    "Resultado Explotación\nmil EUR\n2017": "Operating result (thousand EUR) 2017",
    "Resultado Explotación\nmil EUR\n2016": "Operating result (thousand EUR) 2016",
    "Resultado Explotación\nmil EUR\n2015": "Operating result (thousand EUR) 2015",
    "Resultado Explotación\nmil EUR\n2012": "Operating result (thousand EUR) 2012",
    "Resultado Explotación\nmil EUR\n2013": "Operating result (thousand EUR) 2013",
    "Resultado Explotación\nmil EUR\n2014": "Operating result (thousand EUR) 2014",
    "Resultado Explotación\nmil EUR\n2011": "Operating result (thousand EUR) 2011",
    "Resultado Explotación\nmil EUR\n2010": "Operating result (thousand EUR) 2010",
    "Gastos financieros\nmil EUR\n2022": "Financial expenses (thousand EUR) 2022",
    "Gastos financieros\nmil EUR\n2021": "Financial expenses (thousand EUR) 2021",
    "Gastos financieros\nmil EUR\n2019": "Financial expenses (thousand EUR) 2019",
    "Gastos financieros\nmil EUR\n2020": "Financial expenses (thousand EUR) 2020",
    "Gastos financieros\nmil EUR\n2018": "Financial expenses (thousand EUR) 2018",
    "Gastos financieros\nmil EUR\n2017": "Financial expenses (thousand EUR) 2017",
    "Gastos financieros\nmil EUR\n2016": "Financial expenses (thousand EUR) 2016",
    "Gastos financieros\nmil EUR\n2015": "Financial expenses (thousand EUR) 2015",
    "Gastos financieros\nmil EUR\n2012": "Financial expenses (thousand EUR) 2012",
    "Gastos financieros\nmil EUR\n2013": "Financial expenses (thousand EUR) 2013",
    "Gastos financieros\nmil EUR\n2014": "Financial expenses (thousand EUR) 2014",
    "Gastos financieros\nmil EUR\n2011": "Financial expenses (thousand EUR) 2011",
    "Gastos financieros\nmil EUR\n2010": "Financial expenses (thousand EUR) 2010",
    "Impuestos sobre sociedades\nmil EUR\n2022": "Corporate income tax (thousand EUR) 2022",
    "Impuestos sobre sociedades\nmil EUR\n2021": "Corporate income tax (thousand EUR) 2021",
    "Impuestos sobre sociedades\nmil EUR\n2019": "Corporate income tax (thousand EUR) 2019",
    "Impuestos sobre sociedades\nmil EUR\n2020": "Corporate income tax (thousand EUR) 2020",
    "Impuestos sobre sociedades\nmil EUR\n2018": "Corporate income tax (thousand EUR) 2018",
    "Impuestos sobre sociedades\nmil EUR\n2017": "Corporate income tax (thousand EUR) 2017",
    "Impuestos sobre sociedades\nmil EUR\n2016": "Corporate income tax (thousand EUR) 2016",
    "Impuestos sobre sociedades\nmil EUR\n2015": "Corporate income tax (thousand EUR) 2015",
    "Impuestos sobre sociedades\nmil EUR\n2012": "Corporate income tax (thousand EUR) 2012",
    "Impuestos sobre sociedades\nmil EUR\n2013": "Corporate income tax (thousand EUR) 2013",
    "Impuestos sobre sociedades\nmil EUR\n2014": "Corporate income tax (thousand EUR) 2014",
    "Impuestos sobre sociedades\nmil EUR\n2011": "Corporate income tax (thousand EUR) 2011",
    "Impuestos sobre sociedades\nmil EUR\n2010": "Corporate income tax (thousand EUR) 2010",
    "Resultado del Ejercicio\nmil EUR\n2022": "Net profit (thousand EUR) 2022",
    "Resultado del Ejercicio\nmil EUR\n2021": "Net profit (thousand EUR) 2021",
    "Resultado del Ejercicio\nmil EUR\n2019": "Net profit (thousand EUR) 2019",
    "Resultado del Ejercicio\nmil EUR\n2020": "Net profit (thousand EUR) 2020",
    "Resultado del Ejercicio\nmil EUR\n2018": "Net profit (thousand EUR) 2018",
    "Resultado del Ejercicio\nmil EUR\n2017": "Net profit (thousand EUR) 2017",
    "Resultado del Ejercicio\nmil EUR\n2016": "Net profit (thousand EUR) 2016",
    "Resultado del Ejercicio\nmil EUR\n2015": "Net profit (thousand EUR) 2015",
    "Resultado del Ejercicio\nmil EUR\n2012": "Net profit (thousand EUR) 2012",
    "Resultado del Ejercicio\nmil EUR\n2013": "Net profit (thousand EUR) 2013",
    "Resultado del Ejercicio\nmil EUR\n2014": "Net profit (thousand EUR) 2014",
    "Resultado del Ejercicio\nmil EUR\n2011": "Net profit (thousand EUR) 2011",
    "Resultado del Ejercicio\nmil EUR\n2010": "Net profit (thousand EUR) 2010",
    "Gastos de personal\nmil EUR\n2022": "Personnel expenses (thousand EUR) 2022",
    "Gastos de personal\nmil EUR\n2021": "Personnel expenses (thousand EUR) 2021",
    "Gastos de personal\nmil EUR\n2019": "Personnel expenses (thousand EUR) 2019",
    "Gastos de personal\nmil EUR\n2020": "Personnel expenses (thousand EUR) 2020",
    "Gastos de personal\nmil EUR\n2018": "Personnel expenses (thousand EUR) 2018",
    "Gastos de personal\nmil EUR\n2017": "Personnel expenses (thousand EUR) 2017",
    "Gastos de personal\nmil EUR\n2016": "Personnel expenses (thousand EUR) 2016",
    "Gastos de personal\nmil EUR\n2015": "Personnel expenses (thousand EUR) 2015",
    "Gastos de personal\nmil EUR\n2012": "Personnel expenses (thousand EUR) 2012",
    "Gastos de personal\nmil EUR\n2013": "Personnel expenses (thousand EUR) 2013",
    "Gastos de personal\nmil EUR\n2014": "Personnel expenses (thousand EUR) 2014",
    "Gastos de personal\nmil EUR\n2011": "Personnel expenses (thousand EUR) 2011",
    "Gastos de personal\nmil EUR\n2010": "Personnel expenses (thousand EUR) 2010",
    "Consumo de mercaderías y de materias\nmil EUR\n2022": "Goods and materials consumption (thousand EUR) 2022",
    "Consumo de mercaderías y de materias\nmil EUR\n2021": "Goods and materials consumption (thousand EUR) 2021",
    "Consumo de mercaderías y de materias\nmil EUR\n2019": "Goods and materials consumption (thousand EUR) 2019",
    "Consumo de mercaderías y de materias\nmil EUR\n2020": "Goods and materials consumption (thousand EUR) 2020",
    "Consumo de mercaderías y de materias\nmil EUR\n2018": "Goods and materials consumption (thousand EUR) 2018",
    "Consumo de mercaderías y de materias\nmil EUR\n2017": "Goods and materials consumption (thousand EUR) 2017",
    "Consumo de mercaderías y de materias\nmil EUR\n2016": "Goods and materials consumption (thousand EUR) 2016",
    "Consumo de mercaderías y de materias\nmil EUR\n2015": "Goods and materials consumption (thousand EUR) 2015",
    "Consumo de mercaderías y de materias\nmil EUR\n2012": "Goods and materials consumption (thousand EUR) 2012",
    "Consumo de mercaderías y de materias\nmil EUR\n2013": "Goods and materials consumption (thousand EUR) 2013",
    "Consumo de mercaderías y de materias\nmil EUR\n2014": "Goods and materials consumption (thousand EUR) 2014",
    "Consumo de mercaderías y de materias\nmil EUR\n2011": "Goods and materials consumption (thousand EUR) 2011",
    "Consumo de mercaderías y de materias\nmil EUR\n2010": "Goods and materials consumption (thousand EUR) 2010",
    "Materiales\nmil EUR\n2022": "Materials (thousand EUR) 2022",
    "Materiales\nmil EUR\n2021": "Materials (thousand EUR) 2021",
    "Materiales\nmil EUR\n2019": "Materials (thousand EUR) 2019",
    "Materiales\nmil EUR\n2020": "Materials (thousand EUR) 2020",
    "Materiales\nmil EUR\n2018": "Materials (thousand EUR) 2018",
    "Materiales\nmil EUR\n2017": "Materials (thousand EUR) 2017",
    "Materiales\nmil EUR\n2016": "Materials (thousand EUR) 2016",
    "Materiales\nmil EUR\n2015": "Materials (thousand EUR) 2015",
    "Materiales\nmil EUR\n2012": "Materials (thousand EUR) 2012",
    "Materiales\nmil EUR\n2013": "Materials (thousand EUR) 2013",
    "Materiales\nmil EUR\n2014": "Materials (thousand EUR) 2014",
    "Materiales\nmil EUR\n2011": "Materials (thousand EUR) 2011",
    "Materiales\nmil EUR\n2010": "Materials (thousand EUR) 2010",
    "Cash flow\nmil EUR\n2022": "Cash flow (thousand EUR) 2022",
    "Cash flow\nmil EUR\n2021": "Cash flow (thousand EUR) 2021",
    "Cash flow\nmil EUR\n2019": "Cash flow (thousand EUR) 2019",
    "Cash flow\nmil EUR\n2020": "Cash flow (thousand EUR) 2020",
    "Cash flow\nmil EUR\n2018": "Cash flow (thousand EUR) 2018",
    "Cash flow\nmil EUR\n2017": "Cash flow (thousand EUR) 2017",
    "Cash flow\nmil EUR\n2016": "Cash flow (thousand EUR) 2016",
    "Cash flow\nmil EUR\n2015": "Cash flow (thousand EUR) 2015",
    "Cash flow\nmil EUR\n2012": "Cash flow (thousand EUR) 2012",
    "Cash flow\nmil EUR\n2013": "Cash flow (thousand EUR) 2013",
    "Cash flow\nmil EUR\n2014": "Cash flow (thousand EUR) 2014",
    "Cash flow\nmil EUR\n2011": "Cash flow (thousand EUR) 2011",
    "Cash flow\nmil EUR\n2010": "Cash flow (thousand EUR) 2010",
    "EBIT\nmil EUR\n2022": "EBIT (thousand EUR) 2022",
    "EBIT\nmil EUR\n2021": "EBIT (thousand EUR) 2021",
    "EBIT\nmil EUR\n2019": "EBIT (thousand EUR) 2019",
    "EBIT\nmil EUR\n2020": "EBIT (thousand EUR) 2020",
    "EBIT\nmil EUR\n2018": "EBIT (thousand EUR) 2018",
    "EBIT\nmil EUR\n2017": "EBIT (thousand EUR) 2017",
    "EBIT\nmil EUR\n2016": "EBIT (thousand EUR) 2016",
    "EBIT\nmil EUR\n2015": "EBIT (thousand EUR) 2015",
    "EBIT\nmil EUR\n2012": "EBIT (thousand EUR) 2012",
    "EBIT\nmil EUR\n2013": "EBIT (thousand EUR) 2013",
    "EBIT\nmil EUR\n2014": "EBIT (thousand EUR) 2014",
    "EBIT\nmil EUR\n2011": "EBIT (thousand EUR) 2011",
    "EBIT\nmil EUR\n2010": "EBIT (thousand EUR) 2010",
    "Total activo\nmil EUR\n2022": "Total assets (thousand EUR) 2022",
    "Total activo\nmil EUR\n2021": "Total assets (thousand EUR) 2021",
    "Total activo\nmil EUR\n2019": "Total assets (thousand EUR) 2019",
    "Total activo\nmil EUR\n2020": "Total assets (thousand EUR) 2020",
    "Total activo\nmil EUR\n2018": "Total assets (thousand EUR) 2018",
    "Total activo\nmil EUR\n2017": "Total assets (thousand EUR) 2017",
    "Total activo\nmil EUR\n2016": "Total assets (thousand EUR) 2016",
    "Total activo\nmil EUR\n2015": "Total assets (thousand EUR) 2015",
    "Total activo\nmil EUR\n2012": "Total assets (thousand EUR) 2012",
    "Total activo\nmil EUR\n2013": "Total assets (thousand EUR) 2013",
    "Total activo\nmil EUR\n2014": "Total assets (thousand EUR) 2014",
    "Total activo\nmil EUR\n2011": "Total assets (thousand EUR) 2011",
    "Total activo\nmil EUR\n2010": "Total assets (thousand EUR) 2010",
    "Activo circulante\nmil EUR\n2022": "Current assets (thousand EUR) 2022",
    "Activo circulante\nmil EUR\n2021": "Current assets (thousand EUR) 2021",
    "Activo circulante\nmil EUR\n2019": "Current assets (thousand EUR) 2019",
    "Activo circulante\nmil EUR\n2020": "Current assets (thousand EUR) 2020",
    "Activo circulante\nmil EUR\n2018": "Current assets (thousand EUR) 2018",
    "Activo circulante\nmil EUR\n2017": "Current assets (thousand EUR) 2017",
    "Activo circulante\nmil EUR\n2016": "Current assets (thousand EUR) 2016",
    "Activo circulante\nmil EUR\n2015": "Current assets (thousand EUR) 2015",
    "Activo circulante\nmil EUR\n2012": "Current assets (thousand EUR) 2012",
    "Activo circulante\nmil EUR\n2013": "Current assets (thousand EUR) 2013",
    "Activo circulante\nmil EUR\n2014": "Current assets (thousand EUR) 2014",
    "Activo circulante\nmil EUR\n2011": "Current assets (thousand EUR) 2011",
    "Activo circulante\nmil EUR\n2010": "Current assets (thousand EUR) 2010",
    "Deudores\nmil EUR\n2022": "Receivables (thousand EUR) 2022",
    "Deudores\nmil EUR\n2021": "Receivables (thousand EUR) 2021",
    "Deudores\nmil EUR\n2019": "Receivables (thousand EUR) 2019",
    "Deudores\nmil EUR\n2020": "Receivables (thousand EUR) 2020",
    "Deudores\nmil EUR\n2018": "Receivables (thousand EUR) 2018",
    "Deudores\nmil EUR\n2017": "Receivables (thousand EUR) 2017",
    "Deudores\nmil EUR\n2016": "Receivables (thousand EUR) 2016",
    "Deudores\nmil EUR\n2015": "Receivables (thousand EUR) 2015",
    "Deudores\nmil EUR\n2012": "Receivables (thousand EUR) 2012",
    "Deudores\nmil EUR\n2013": "Receivables (thousand EUR) 2013",
    "Deudores\nmil EUR\n2014": "Receivables (thousand EUR) 2014",
    "Deudores\nmil EUR\n2011": "Receivables (thousand EUR) 2011",
    "Deudores\nmil EUR\n2010": "Receivables (thousand EUR) 2010",
    "Existencias\nmil EUR\n2022": "Inventory (thousand EUR) 2022",
    "Existencias\nmil EUR\n2021": "Inventory (thousand EUR) 2021",
    "Existencias\nmil EUR\n2019": "Inventory (thousand EUR) 2019",
    "Existencias\nmil EUR\n2020": "Inventory (thousand EUR) 2020",
    "Existencias\nmil EUR\n2018": "Inventory (thousand EUR) 2018",
    "Existencias\nmil EUR\n2017": "Inventory (thousand EUR) 2017",
    "Existencias\nmil EUR\n2016": "Inventory (thousand EUR) 2016",
    "Existencias\nmil EUR\n2015": "Inventory (thousand EUR) 2015",
    "Existencias\nmil EUR\n2012": "Inventory (thousand EUR) 2012",
    "Existencias\nmil EUR\n2013": "Inventory (thousand EUR) 2013",
    "Existencias\nmil EUR\n2014": "Inventory (thousand EUR) 2014",
    "Existencias\nmil EUR\n2011": "Inventory (thousand EUR) 2011",
    "Existencias\nmil EUR\n2010": "Inventory (thousand EUR) 2010",
    "Inmovilizado\nmil EUR\n2022": "Fixed assets (thousand EUR) 2022",
    "Inmovilizado\nmil EUR\n2021": "Fixed assets (thousand EUR) 2021",
    "Inmovilizado\nmil EUR\n2019": "Fixed assets (thousand EUR) 2019",
    "Inmovilizado\nmil EUR\n2020": "Fixed assets (thousand EUR) 2020",
    "Inmovilizado\nmil EUR\n2018": "Fixed assets (thousand EUR) 2018",
    "Inmovilizado\nmil EUR\n2017": "Fixed assets (thousand EUR) 2017",
    "Inmovilizado\nmil EUR\n2016": "Fixed assets (thousand EUR) 2016",
    "Inmovilizado\nmil EUR\n2015": "Fixed assets (thousand EUR) 2015",
    "Inmovilizado\nmil EUR\n2012": "Fixed assets (thousand EUR) 2012",
    "Inmovilizado\nmil EUR\n2013": "Fixed assets (thousand EUR) 2013",
    "Inmovilizado\nmil EUR\n2014": "Fixed assets (thousand EUR) 2014",
    "Inmovilizado\nmil EUR\n2011": "Fixed assets (thousand EUR) 2011",
    "Inmovilizado\nmil EUR\n2010": "Fixed assets (thousand EUR) 2010",
    "Inmovilizado inmaterial\nmil EUR\n2022": "Intangible assets (thousand EUR) 2022",
    "Inmovilizado inmaterial\nmil EUR\n2021": "Intangible assets (thousand EUR) 2021",
    "Inmovilizado inmaterial\nmil EUR\n2019": "Intangible assets (thousand EUR) 2019",
    "Inmovilizado inmaterial\nmil EUR\n2020": "Intangible assets (thousand EUR) 2020",
    "Inmovilizado inmaterial\nmil EUR\n2018": "Intangible assets (thousand EUR) 2018",
    "Inmovilizado inmaterial\nmil EUR\n2017": "Intangible assets (thousand EUR) 2017",
    "Inmovilizado inmaterial\nmil EUR\n2016": "Intangible assets (thousand EUR) 2016",
    "Inmovilizado inmaterial\nmil EUR\n2015": "Intangible assets (thousand EUR) 2015",
    "Inmovilizado inmaterial\nmil EUR\n2012": "Intangible assets (thousand EUR) 2012",
    "Inmovilizado inmaterial\nmil EUR\n2013": "Intangible assets (thousand EUR) 2013",
    "Inmovilizado inmaterial\nmil EUR\n2014": "Intangible assets (thousand EUR) 2014",
    "Inmovilizado inmaterial\nmil EUR\n2011": "Intangible assets (thousand EUR) 2011",
    "Inmovilizado inmaterial\nmil EUR\n2010": "Intangible assets (thousand EUR) 2010",
    "Inmovilizado material\nmil EUR\n2022": "Tangible assets (thousand EUR) 2022",
    "Inmovilizado material\nmil EUR\n2021": "Tangible assets (thousand EUR) 2021",
    "Inmovilizado material\nmil EUR\n2019": "Tangible assets (thousand EUR) 2019",
    "Inmovilizado material\nmil EUR\n2020": "Tangible assets (thousand EUR) 2020",
    "Inmovilizado material\nmil EUR\n2018": "Tangible assets (thousand EUR) 2018",
    "Inmovilizado material\nmil EUR\n2017": "Tangible assets (thousand EUR) 2017",
    "Inmovilizado material\nmil EUR\n2016": "Tangible assets (thousand EUR) 2016",
    "Inmovilizado material\nmil EUR\n2015": "Tangible assets (thousand EUR) 2015",
    "Inmovilizado material\nmil EUR\n2012": "Tangible assets (thousand EUR) 2012",
    "Inmovilizado material\nmil EUR\n2013": "Tangible assets (thousand EUR) 2013",
    "Inmovilizado material\nmil EUR\n2014": "Tangible assets (thousand EUR) 2014",
    "Inmovilizado material\nmil EUR\n2011": "Tangible assets (thousand EUR) 2011",
    "Inmovilizado material\nmil EUR\n2010": "Tangible assets (thousand EUR) 2010",
    "Otros pasivos fijos\nmil EUR\n2022": "Other fixed liabilities (thousand EUR) 2022",
    "Otros pasivos fijos\nmil EUR\n2021": "Other fixed liabilities (thousand EUR) 2021",
    "Otros pasivos fijos\nmil EUR\n2019": "Other fixed liabilities (thousand EUR) 2019",
    "Otros pasivos fijos\nmil EUR\n2020": "Other fixed liabilities (thousand EUR) 2020",
    "Otros pasivos fijos\nmil EUR\n2018": "Other fixed liabilities (thousand EUR) 2018",
    "Otros pasivos fijos\nmil EUR\n2017": "Other fixed liabilities (thousand EUR) 2017",
    "Otros pasivos fijos\nmil EUR\n2016": "Other fixed liabilities (thousand EUR) 2016",
    "Otros pasivos fijos\nmil EUR\n2015": "Other fixed liabilities (thousand EUR) 2015",
    "Otros pasivos fijos\nmil EUR\n2012": "Other fixed liabilities (thousand EUR) 2012",
    "Otros pasivos fijos\nmil EUR\n2013": "Other fixed liabilities (thousand EUR) 2013",
    "Otros pasivos fijos\nmil EUR\n2014": "Other fixed liabilities (thousand EUR) 2014",
    "Otros pasivos fijos\nmil EUR\n2011": "Other fixed liabilities (thousand EUR) 2011",
    "Otros pasivos fijos\nmil EUR\n2010": "Other fixed liabilities (thousand EUR) 2010",
    "Total pasivo y capital propio\nmil EUR\n2022": "Total liabilities and equity (thousand EUR) 2022",
    "Total pasivo y capital propio\nmil EUR\n2021": "Total liabilities and equity (thousand EUR) 2021",
    "Total pasivo y capital propio\nmil EUR\n2019": "Total liabilities and equity (thousand EUR) 2019",
    "Total pasivo y capital propio\nmil EUR\n2020": "Total liabilities and equity (thousand EUR) 2020",
    "Total pasivo y capital propio\nmil EUR\n2018": "Total liabilities and equity (thousand EUR) 2018",
    "Total pasivo y capital propio\nmil EUR\n2017": "Total liabilities and equity (thousand EUR) 2017",
    "Total pasivo y capital propio\nmil EUR\n2016": "Total liabilities and equity (thousand EUR) 2016",
    "Total pasivo y capital propio\nmil EUR\n2015": "Total liabilities and equity (thousand EUR) 2015",
    "Total pasivo y capital propio\nmil EUR\n2012": "Total liabilities and equity (thousand EUR) 2012",
    "Total pasivo y capital propio\nmil EUR\n2013": "Total liabilities and equity (thousand EUR) 2013",
    "Total pasivo y capital propio\nmil EUR\n2014": "Total liabilities and equity (thousand EUR) 2014",
    "Total pasivo y capital propio\nmil EUR\n2011": "Total liabilities and equity (thousand EUR) 2011",
    "Total pasivo y capital propio\nmil EUR\n2010": "Total liabilities and equity (thousand EUR) 2010",
    "Fondo de maniobra\nmil EUR\n2022": "Working capital (thousand EUR) 2022",
    "Fondo de maniobra\nmil EUR\n2021": "Working capital (thousand EUR) 2021",
    "Fondo de maniobra\nmil EUR\n2019": "Working capital (thousand EUR) 2019",
    "Fondo de maniobra\nmil EUR\n2020": "Working capital (thousand EUR) 2020",
    "Fondo de maniobra\nmil EUR\n2018": "Working capital (thousand EUR) 2018",
    "Fondo de maniobra\nmil EUR\n2017": "Working capital (thousand EUR) 2017",
    "Fondo de maniobra\nmil EUR\n2016": "Working capital (thousand EUR) 2016",
    "Fondo de maniobra\nmil EUR\n2015": "Working capital (thousand EUR) 2015",
    "Fondo de maniobra\nmil EUR\n2012": "Working capital (thousand EUR) 2012",
    "Fondo de maniobra\nmil EUR\n2013": "Working capital (thousand EUR) 2013",
    "Fondo de maniobra\nmil EUR\n2014": "Working capital (thousand EUR) 2014",
    "Fondo de maniobra\nmil EUR\n2011": "Working capital (thousand EUR) 2011",
    "Fondo de maniobra\nmil EUR\n2010": "Working capital (thousand EUR) 2010",
    "Número empleados\n2022": "Number of employees 2022",
    "Número empleados\n2021": "Number of employees 2021",
    "Número empleados\n2020": "Number of employees 2020",
    "Número empleados\n2019": "Number of employees 2019",
    "Número empleados\n2018": "Number of employees 2018",
    "Número empleados\n2017": "Number of employees 2017",
    "Número empleados\n2016": "Number of employees 2016",
    "Número empleados\n2014": "Number of employees 2014",
    "Número empleados\n2015": "Number of employees 2015",
    "Número empleados\n2013": "Number of employees 2013",
    "Número empleados\n2012": "Number of employees 2012",
    "Número empleados\n2011": "Number of employees 2011",
    "Número empleados\n2010": "Number of employees 2010",
    "Deudas financieras\nmil EUR\n2022": "Financial debts (thousand EUR) 2022",
    "Deudas financieras\nmil EUR\n2021": "Financial debts (thousand EUR) 2021",
    "Deudas financieras\nmil EUR\n2019": "Financial debts (thousand EUR) 2019",
    "Deudas financieras\nmil EUR\n2020": "Financial debts (thousand EUR) 2020",
    "Deudas financieras\nmil EUR\n2018": "Financial debts (thousand EUR) 2018",
    "Deudas financieras\nmil EUR\n2017": "Financial debts (thousand EUR) 2017",
    "Deudas financieras\nmil EUR\n2016": "Financial debts (thousand EUR) 2016",
    "Deudas financieras\nmil EUR\n2015": "Financial debts (thousand EUR) 2015",
    "Deudas financieras\nmil EUR\n2012": "Financial debts (thousand EUR) 2012",
    "Deudas financieras\nmil EUR\n2013": "Financial debts (thousand EUR) 2013",
    "Deudas financieras\nmil EUR\n2014": "Financial debts (thousand EUR) 2014",
    "Deudas financieras\nmil EUR\n2011": "Financial debts (thousand EUR) 2011",
    "Deudas financieras\nmil EUR\n2010": "Financial debts (thousand EUR) 2010",
    "Pasivo fijo\nmil EUR\n2022": "Fixed liabilities (thousand EUR) 2022",
    "Pasivo fijo\nmil EUR\n2021": "Fixed liabilities (thousand EUR) 2021",
    "Pasivo fijo\nmil EUR\n2019": "Fixed liabilities (thousand EUR) 2019",
    "Pasivo fijo\nmil EUR\n2020": "Fixed liabilities (thousand EUR) 2020",
    "Pasivo fijo\nmil EUR\n2018": "Fixed liabilities (thousand EUR) 2018",
    "Pasivo fijo\nmil EUR\n2017": "Fixed liabilities (thousand EUR) 2017",
    "Pasivo fijo\nmil EUR\n2016": "Fixed liabilities (thousand EUR) 2016",
    "Pasivo fijo\nmil EUR\n2015": "Fixed liabilities (thousand EUR) 2015",
    "Pasivo fijo\nmil EUR\n2012": "Fixed liabilities (thousand EUR) 2012",
    "Pasivo fijo\nmil EUR\n2013": "Fixed liabilities (thousand EUR) 2013",
    "Pasivo fijo\nmil EUR\n2014": "Fixed liabilities (thousand EUR) 2014",
    "Pasivo fijo\nmil EUR\n2011": "Fixed liabilities (thousand EUR) 2011",
    "Pasivo fijo\nmil EUR\n2010": "Fixed liabilities (thousand EUR) 2010",
    "Pasivo líquido\nmil EUR\n2022": "Liquid liabilities (thousand EUR) 2022",
    "Pasivo líquido\nmil EUR\n2021": "Liquid liabilities (thousand EUR) 2021",
    "Pasivo líquido\nmil EUR\n2019": "Liquid liabilities (thousand EUR) 2019",
    "Pasivo líquido\nmil EUR\n2020": "Liquid liabilities (thousand EUR) 2020",
    "Pasivo líquido\nmil EUR\n2018": "Liquid liabilities (thousand EUR) 2018",
    "Pasivo líquido\nmil EUR\n2017": "Liquid liabilities (thousand EUR) 2017",
    "Pasivo líquido\nmil EUR\n2016": "Liquid liabilities (thousand EUR) 2016",
    "Pasivo líquido\nmil EUR\n2015": "Liquid liabilities (thousand EUR) 2015",
    "Pasivo líquido\nmil EUR\n2012": "Liquid liabilities (thousand EUR) 2012",
    "Pasivo líquido\nmil EUR\n2013": "Liquid liabilities (thousand EUR) 2013",
    "Pasivo líquido\nmil EUR\n2014": "Liquid liabilities (thousand EUR) 2014",
    "Pasivo líquido\nmil EUR\n2011": "Liquid liabilities (thousand EUR) 2011",
    "Pasivo líquido\nmil EUR\n2010": "Liquid liabilities (thousand EUR) 2010",
    "Rentabilidad sobre recursos propios (%)\n%\n2022": "Return on Equity (%), 2022",
    "Rentabilidad sobre recursos propios (%)\n%\n2021": "Return on Equity (%), 2021",
    "Rentabilidad sobre recursos propios (%)\n%\n2020": "Return on Equity (%), 2020",
    "Rentabilidad sobre recursos propios (%)\n%\n2019": "Return on Equity (%), 2019",
    "Rentabilidad sobre recursos propios (%)\n%\n2018": "Return on Equity (%), 2018",
    "Rentabilidad sobre recursos propios (%)\n%\n2017": "Return on Equity (%), 2017",
    "Rentabilidad sobre recursos propios (%)\n%\n2015": "Return on Equity (%), 2015",
    "Rentabilidad sobre recursos propios (%)\n%\n2016": "Return on Equity (%), 2016",
    "Rentabilidad sobre recursos propios (%)\n%\n2014": "Return on Equity (%), 2014",
    "Rentabilidad sobre recursos propios (%)\n%\n2012": "Return on Equity (%), 2012",
    "Rentabilidad sobre recursos propios (%)\n%\n2013": "Return on Equity (%), 2013",
    "Rentabilidad sobre recursos propios (%)\n%\n2011": "Return on Equity (%), 2011",
    "Rentabilidad sobre recursos propios (%)\n%\n2010": "Return on Equity (%), 2010",
    "Rentabilidad sobre el activo total (%)\n%\n2022": "Return on Total Assets (%), 2022",
    "Rentabilidad sobre el activo total (%)\n%\n2021": "Return on Total Assets (%), 2021",
    "Rentabilidad sobre el activo total (%)\n%\n2020": "Return on Total Assets (%), 2020",
    "Rentabilidad sobre el activo total (%)\n%\n2019": "Return on Total Assets (%), 2019",
    "Rentabilidad sobre el activo total (%)\n%\n2018": "Return on Total Assets (%), 2018",
    "Rentabilidad sobre el activo total (%)\n%\n2017": "Return on Total Assets (%), 2017",
    "Rentabilidad sobre el activo total (%)\n%\n2015": "Return on Total Assets (%), 2015",
    "Rentabilidad sobre el activo total (%)\n%\n2016": "Return on Total Assets (%), 2016",
    "Rentabilidad sobre el activo total (%)\n%\n2014": "Return on Total Assets (%), 2014",
    "Rentabilidad sobre el activo total (%)\n%\n2012": "Return on Total Assets (%), 2012",
    "Rentabilidad sobre el activo total (%)\n%\n2013": "Return on Total Assets (%), 2013",
    "Rentabilidad sobre el activo total (%)\n%\n2011": "Return on Total Assets (%), 2011",
    "Rentabilidad sobre el activo total (%)\n%\n2010": "Return on Total Assets (%), 2010",
    "Margen de beneficio (%)\n%\n2022": "Profit Margin (%), 2022",
    "Margen de beneficio (%)\n%\n2021": "Profit Margin (%), 2021",
    "Margen de beneficio (%)\n%\n2020": "Profit Margin (%), 2020",
    "Margen de beneficio (%)\n%\n2019": "Profit Margin (%), 2019",
    "Margen de beneficio (%)\n%\n2018": "Profit Margin (%), 2018",
    "Margen de beneficio (%)\n%\n2017": "Profit Margin (%), 2017",
    "Margen de beneficio (%)\n%\n2015": "Profit Margin (%), 2015",
    "Margen de beneficio (%)\n%\n2016": "Profit Margin (%), 2016",
    "Margen de beneficio (%)\n%\n2014": "Profit Margin (%), 2014",
    "Margen de beneficio (%)\n%\n2012": "Profit Margin (%), 2012",
    "Margen de beneficio (%)\n%\n2013": "Profit Margin (%), 2013",
    "Margen de beneficio (%)\n%\n2011": "Profit Margin (%), 2011",
    "Margen de beneficio (%)\n%\n2010": "Profit Margin (%), 2010",
    "Ratio de solvencia\n%\n2022": "Solvency Ratio (%), 2022",
    "Ratio de solvencia\n%\n2021": "Solvency Ratio (%), 2021",
    "Ratio de solvencia\n%\n2020": "Solvency Ratio (%), 2020",
    "Ratio de solvencia\n%\n2019": "Solvency Ratio (%), 2019",
    "Ratio de solvencia\n%\n2018": "Solvency Ratio (%), 2018",
    "Ratio de solvencia\n%\n2017": "Solvency Ratio (%), 2017",
    "Ratio de solvencia\n%\n2015": "Solvency Ratio (%), 2015",
    "Ratio de solvencia\n%\n2016": "Solvency Ratio (%), 2016",
    "Ratio de solvencia\n%\n2014": "Solvency Ratio (%), 2014",
    "Ratio de solvencia\n%\n2012": "Solvency Ratio (%), 2012",
    "Ratio de solvencia\n%\n2013": "Solvency Ratio (%), 2013",
    "Ratio de solvencia\n%\n2011": "Solvency Ratio (%), 2011",
    "Ratio de solvencia\n%\n2010": "Solvency Ratio (%), 2010",
    "Ratio de liquidez\n%\n2022": "Liquidity Ratio (%), 2022",
    "Ratio de liquidez\n%\n2021": "Liquidity Ratio (%), 2021",
    "Ratio de liquidez\n%\n2020": "Liquidity Ratio (%), 2020",
    "Ratio de liquidez\n%\n2019": "Liquidity Ratio (%), 2019",
    "Ratio de liquidez\n%\n2018": "Liquidity Ratio (%), 2018",
    "Ratio de liquidez\n%\n2017": "Liquidity Ratio (%), 2017",
    "Ratio de liquidez\n%\n2015": "Liquidity Ratio (%), 2015",
    "Ratio de liquidez\n%\n2016": "Liquidity Ratio (%), 2016",
    "Ratio de liquidez\n%\n2014": "Liquidity Ratio (%), 2014",
    "Ratio de liquidez\n%\n2012": "Liquidity Ratio (%), 2012",
    "Ratio de liquidez\n%\n2013": "Liquidity Ratio (%), 2013",
    "Ratio de liquidez\n%\n2011": "Liquidity Ratio (%), 2011",
    "Ratio de liquidez\n%\n2010": "Liquidity Ratio (%), 2010",
    "Apalancamiento (%)\n%\n2022": "Leverage (%), 2022",
    "Apalancamiento (%)\n%\n2021": "Leverage (%), 2021",
    "Apalancamiento (%)\n%\n2020": "Leverage (%), 2020",
    "Apalancamiento (%)\n%\n2019": "Leverage (%), 2019",
    "Apalancamiento (%)\n%\n2018": "Leverage (%), 2018",
    "Apalancamiento (%)\n%\n2017": "Leverage (%), 2017",
    "Apalancamiento (%)\n%\n2015": "Leverage (%), 2015",
    "Apalancamiento (%)\n%\n2016": "Leverage (%), 2016",
    "Apalancamiento (%)\n%\n2014": "Leverage (%), 2014",
    "Apalancamiento (%)\n%\n2012": "Leverage (%), 2012",
    "Apalancamiento (%)\n%\n2013": "Leverage (%), 2013",
    "Apalancamiento (%)\n%\n2011": "Leverage (%), 2011",
    "Apalancamiento (%)\n%\n2010": "Leverage (%), 2010",
    "Beneficio por empleado\nmil\n2022": "Profit per Employee (thousands), 2022",
    "Beneficio por empleado\nmil\n2021": "Profit per Employee (thousands), 2021",
    "Beneficio por empleado\nmil\n2020": "Profit per Employee (thousands), 2020",
    "Beneficio por empleado\nmil\n2019": "Profit per Employee (thousands), 2019",
    "Beneficio por empleado\nmil\n2018": "Profit per Employee (thousands), 2018",
    "Beneficio por empleado\nmil\n2017": "Profit per Employee (thousands), 2017",
    "Beneficio por empleado\nmil\n2015": "Profit per Employee (thousands), 2015",
    "Beneficio por empleado\nmil\n2016": "Profit per Employee (thousands), 2016",
    "Beneficio por empleado\nmil\n2014": "Profit per Employee (thousands), 2014",
    "Beneficio por empleado\nmil\n2012": "Profit per Employee (thousands), 2012",
    "Beneficio por empleado\nmil\n2013": "Profit per Employee (thousands), 2013",
    "Beneficio por empleado\nmil\n2011": "Profit per Employee (thousands), 2011",
    "Beneficio por empleado\nmil\n2010": "Profit per Employee (thousands), 2010",
    "Coste medio de los empleados\nmil\n2022": "Average Employee Cost (thousands), 2022",
    "Coste medio de los empleados\nmil\n2021": "Average Employee Cost (thousands), 2021",
    "Coste medio de los empleados\nmil\n2020": "Average Employee Cost (thousands), 2020",
    "Coste medio de los empleados\nmil\n2019": "Average Employee Cost (thousands), 2019",
    "Coste medio de los empleados\nmil\n2018": "Average Employee Cost (thousands), 2018",
    "Coste medio de los empleados\nmil\n2017": "Average Employee Cost (thousands), 2017",
    "Coste medio de los empleados\nmil\n2015": "Average Employee Cost (thousands), 2015",
    "Coste medio de los empleados\nmil\n2016": "Average Employee Cost (thousands), 2016",
    "Coste medio de los empleados\nmil\n2014": "Average Employee Cost (thousands), 2014",
    "Coste medio de los empleados\nmil\n2012": "Average Employee Cost (thousands), 2012",
    "Coste medio de los empleados\nmil\n2013": "Average Employee Cost (thousands), 2013",
    "Coste medio de los empleados\nmil\n2011": "Average Employee Cost (thousands), 2011",
    "Coste medio de los empleados\nmil\n2010": "Average Employee Cost (thousands), 2010",
    "Total activos por empleado\nmil\n2022": "Total Assets per Employee (thousands), 2022",
    "Total activos por empleado\nmil\n2021": "Total Assets per Employee (thousands), 2021",
    "Total activos por empleado\nmil\n2020": "Total Assets per Employee (thousands), 2020",
    "Total activos por empleado\nmil\n2019": "Total Assets per Employee (thousands), 2019",
    "Total activos por empleado\nmil\n2018": "Total Assets per Employee (thousands), 2018",
    "Total activos por empleado\nmil\n2017": "Total Assets per Employee (thousands), 2017",
    "Total activos por empleado\nmil\n2015": "Total Assets per Employee (thousands), 2015",
    "Total activos por empleado\nmil\n2016": "Total Assets per Employee (thousands), 2016",
    "Total activos por empleado\nmil\n2014": "Total Assets per Employee (thousands), 2014",
    "Total activos por empleado\nmil\n2012": "Total Assets per Employee (thousands), 2012",
    "Total activos por empleado\nmil\n2013": "Total Assets per Employee (thousands), 2013",
    "Total activos por empleado\nmil\n2011": "Total Assets per Employee (thousands), 2011",
    "Total activos por empleado\nmil\n2010": "Total Assets per Employee (thousands), 2010",
    "Gastos de personal\n%\n2022": "Personnel Expenses (%), 2022",
    "Gastos de personal\n%\n2021": "Personnel Expenses (%), 2021",
    "Gastos de personal\n%\n2020": "Personnel Expenses (%), 2020",
    "Gastos de personal\n%\n2019": "Personnel Expenses (%), 2019",
    "Gastos de personal\n%\n2018": "Personnel Expenses (%), 2018",
    "Gastos de personal\n%\n2017": "Personnel Expenses (%), 2017",
    "Gastos de personal\n%\n2016": "Personnel Expenses (%), 2016",
    "Gastos de personal\n%\n2015": "Personnel Expenses (%), 2015",
    "Gastos de personal\n%\n2014": "Personnel Expenses (%), 2014",
    "Gastos de personal\n%\n2013": "Personnel Expenses (%), 2013",
    "Gastos de personal\n%\n2011": "Personnel Expenses (%), 2011",
    "Gastos de personal\n%\n2012": "Personnel Expenses (%), 2012",
    "Gastos de personal\n%\n2010": "Personnel Expenses (%), 2010",
    "Total activo\n%\n2022": "Total Assets (%), 2022",
    "Total activo\n%\n2021": "Total Assets (%), 2021",
    "Total activo\n%\n2020": "Total Assets (%), 2020",
    "Total activo\n%\n2019": "Total Assets (%), 2019",
    "Total activo\n%\n2018": "Total Assets (%), 2018",
    "Total activo\n%\n2017": "Total Assets (%), 2017",
    "Total activo\n%\n2016": "Total Assets (%), 2016",
    "Total activo\n%\n2015": "Total Assets (%), 2015",
    "Total activo\n%\n2014": "Total Assets (%), 2014",
    "Total activo\n%\n2013": "Total Assets (%), 2013",
    "Total activo\n%\n2011": "Total Assets (%), 2011",
    "Total activo\n%\n2012": "Total Assets (%), 2012",
    "Total activo\n%\n2010": "Total Assets (%), 2010",
    "Fondos propios\n%\n2022": "Equity (%), 2022",
    "Fondos propios\n%\n2021": "Equity (%), 2021",
    "Fondos propios\n%\n2020": "Equity (%), 2020",
    "Fondos propios\n%\n2019": "Equity (%), 2019",
    "Fondos propios\n%\n2018": "Equity (%), 2018",
    "Fondos propios\n%\n2017": "Equity (%), 2017",
    "Fondos propios\n%\n2016": "Equity (%), 2016",
    "Fondos propios\n%\n2015": "Equity (%), 2015",
    "Fondos propios\n%\n2014": "Equity (%), 2014",
    "Fondos propios\n%\n2013": "Equity (%), 2013",
    "Fondos propios\n%\n2011": "Equity (%), 2011",
    "Fondos propios\n%\n2012": "Equity (%), 2012",
    "Fondos propios\n%\n2010": "Equity (%), 2010",
    "Acreedores a largo plazo\n%\n2022": "Long-term Creditors (%), 2022",
    "Acreedores a largo plazo\n%\n2021": "Long-term Creditors (%), 2021",
    "Acreedores a largo plazo\n%\n2020": "Long-term Creditors (%), 2020",
    "Acreedores a largo plazo\n%\n2019": "Long-term Creditors (%), 2019",
    "Acreedores a largo plazo\n%\n2018": "Long-term Creditors (%), 2018",
    "Acreedores a largo plazo\n%\n2017": "Long-term Creditors (%), 2017",
    "Acreedores a largo plazo\n%\n2016": "Long-term Creditors (%), 2016",
    "Acreedores a largo plazo\n%\n2015": "Long-term Creditors (%), 2015",
    "Acreedores a largo plazo\n%\n2014": "Long-term Creditors (%), 2014",
    "Acreedores a largo plazo\n%\n2013": "Long-term Creditors (%), 2013",
    "Acreedores a largo plazo\n%\n2011": "Long-term Creditors (%), 2011",
    "Acreedores a largo plazo\n%\n2012": "Long-term Creditors (%), 2012",
    "Acreedores a largo plazo\n%\n2010": "Long-term Creditors (%), 2010",
    "Fondo maniobra\n%\n2022": "Working Capital (%), 2022",
    "Fondo maniobra\n%\n2021": "Working Capital (%), 2021",
    "Fondo maniobra\n%\n2020": "Working Capital (%), 2020",
    "Fondo maniobra\n%\n2019": "Working Capital (%), 2019",
    "Fondo maniobra\n%\n2018": "Working Capital (%), 2018",
    "Fondo maniobra\n%\n2017": "Working Capital (%), 2017",
    "Fondo maniobra\n%\n2016": "Working Capital (%), 2016",
    "Fondo maniobra\n%\n2015": "Working Capital (%), 2015",
    "Fondo maniobra\n%\n2014": "Working Capital (%), 2014",
    "Fondo maniobra\n%\n2013": "Working Capital (%), 2013",
    "Fondo maniobra\n%\n2011": "Working Capital (%), 2011",
    "Fondo maniobra\n%\n2012": "Working Capital (%), 2012",
    "Fondo maniobra\n%\n2010": "Working Capital (%), 2010",
    "Tesorería\n%\n2022": "Treasury (%), 2022",
    "Tesorería\n%\n2021": "Treasury (%), 2021",
    "Tesorería\n%\n2020": "Treasury (%), 2020",
    "Tesorería\n%\n2019": "Treasury (%), 2019",
    "Tesorería\n%\n2018": "Treasury (%), 2018",
    "Tesorería\n%\n2017": "Treasury (%), 2017",
    "Tesorería\n%\n2016": "Treasury (%), 2016",
    "Tesorería\n%\n2015": "Treasury (%), 2015",
    "Tesorería\n%\n2014": "Treasury (%), 2014",
    "Tesorería\n%\n2013": "Treasury (%), 2013",
    "Tesorería\n%\n2011": "Treasury (%), 2011",
    "Tesorería\n%\n2012": "Treasury (%), 2012",
    "Tesorería\n%\n2010": "Treasury (%), 2010"
}

# Rename columns using the dictionary
df.rename(columns=column_name_mapping, inplace=True)

# Calculate mean values to fill na skip non int values
mean_values = df.mean(skipna=True, numeric_only=True)

df = df.fillna(mean_values)

########## Here we start to develop the App

# Define app layout
st.title('M&A App')

# Add sidebar for navigation - The sections we will have available

menu = ['Home', 'Information Overview', 'Company Financial Efficiency Ratios','Market Analysis', 'Machine Learning Insights', 'Valuation Calculator']
choice = st.sidebar.selectbox('Select an option', menu)


if choice == 'Home':
    st.title("Home")
    st.write("""
    The M&A Financial App is a tool for analyzing investment opportunities in various sectors, industries, and locations. It uses unsupervised machine learning algorithms to cluster companies based on their financial metrics and ratios, allowing users to quickly identify potential targets for M&A activity.
    """)
    st.write("""
    Key features of the app include:
    - Access to a large database of companies with financial data
    - Calculation of financial ratios and metrics for each company
    - Clustering of companies based on their financial metrics and ratios
    - News and insights related to companies in the database
    """)
    st.write("""
    Use the navigation menu on the left to explore the different sections of the app, including:
    - Information Overview: Get a high-level overview of the companies in the database
    - Company Financial Efficiency Ratios: Analyze the financial ratios and efficiency of individual companies
    - Market Analysis: Explore trends and insights related to the market and industry
    - M&A Insights: Stay up-to-date on mergers, acquisitions, and divestitures in the industry
    - Machine Learning Insights: View insights and predictions generated by our machine learning models
    """)
    

    
    
    # Add call to action section
    st.subheader("Get Started")
    st.write("Ready to start exploring investment opportunities? Use the navigation menu on the left to get started!")
    
  
elif choice == 'Information Overview':

        st.title("Information Overview")

        # Sidebar for selecting a country
        country_names = df['Country'].unique()
        selected_country = st.sidebar.selectbox("Select a Country:", country_names)

        # Filter dataframe for the selected country
        country_data = df[df['Country'] == selected_country]

        # Sidebar for selecting a company
        company_names = country_data['Name'].unique()
        selected_company = st.sidebar.selectbox("Select a Company:", company_names)

        # Filter dataframe for the selected company
        company_data = df[df['Name'] == selected_company]

        # Sidebar for selecting a year
        year_list = ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
        selected_year = st.sidebar.selectbox("Select a Year for Information Overview:", year_list)


        filtered_data = company_data[['Name', 'Tax ID', 'City', 'BvD Number', 'Autonomous Community', 'Postal Code', 'Website', 'Province', 'Country', 'Share Capital (thousand EUR)', 'Stock Market Price'] +
                                    ['Operating Revenues (thousand EUR) ' + selected_year,
                                     'EBITDA (thousand EUR) ' + selected_year,
                                     'Gross result (thousand EUR) ' + selected_year,
                                     'Financial income (thousand EUR) ' + selected_year,
                                     'Operating result (thousand EUR) ' + selected_year,
                                     'Financial expenses (thousand EUR) ' + selected_year,
                                     'Corporate income tax (thousand EUR) ' + selected_year,
                                     'Net profit (thousand EUR) ' + selected_year,
                                     'Personnel expenses (thousand EUR) ' + selected_year,
                                     'Goods and materials consumption (thousand EUR) ' + selected_year,
                                     'Materials (thousand EUR) ' + selected_year,
                                     'Cash flow (thousand EUR) ' + selected_year,
                                     'EBIT (thousand EUR) ' + selected_year,
                                     'Total assets (thousand EUR) ' + selected_year,
                                     'Current assets (thousand EUR) ' + selected_year,
                                     'Receivables (thousand EUR) ' + selected_year,
                                     'Inventory (thousand EUR) ' + selected_year,
                                     'Fixed assets (thousand EUR) ' + selected_year,
                                     'Intangible assets (thousand EUR) ' + selected_year,
                                     'Tangible assets (thousand EUR) ' + selected_year,
                                     'Other fixed liabilities (thousand EUR) ' + selected_year,
                                     'Total liabilities and equity (thousand EUR) ' + selected_year,
                                     'Working capital (thousand EUR) ' + selected_year,
                                     'Number of employees ' + selected_year,
                                     'Financial debts (thousand EUR) ' + selected_year,
                                     'Fixed liabilities (thousand EUR) ' + selected_year,
                                     'Liquid liabilities (thousand EUR) ' + selected_year,
                                     'Return on Equity (%), ' + selected_year,
                                     'Return on Total Assets (%), ' + selected_year,
                                     'Profit Margin (%), ' + selected_year,
                                     'Solvency Ratio (%), ' + selected_year,
                                     'Liquidity Ratio (%), ' + selected_year,
                                     'Leverage (%), ' + selected_year,
                                     'Profit per Employee (thousands), ' + selected_year,
                                     'Average Employee Cost (thousands), ' + selected_year,
                                     'Total Assets per Employee (thousands), ' + selected_year,
                                     'Personnel Expenses (%), ' + selected_year,
                                     'Total Assets (%), ' + selected_year,
                                     'Equity (%), ' + selected_year,
                                     'Long-term Creditors (%), ' + selected_year,
                                     'Working Capital (%), ' + selected_year,
                                     'Treasury (%), ' + selected_year]]

        # Add the 'Year' column to filtered_data
        filtered_data['Year'] = selected_year


        # Get the column names for the selected year
        revenue_column = 'Operating Revenues (thousand EUR) ' + selected_year
        ebitda_column = 'EBITDA (thousand EUR) ' + selected_year
        gross_profit_column = 'Gross result (thousand EUR) ' + selected_year
        
        financial_income_column = 'Financial income (thousand EUR) ' + selected_year
        operating_result_column = 'Operating result (thousand EUR) ' + selected_year
        financial_expenses_column = 'Financial expenses (thousand EUR) ' + selected_year
        corporate_income_tax_column = 'Corporate income tax (thousand EUR) ' + selected_year
        net_profit_column = 'Net profit (thousand EUR) ' + selected_year
        personnel_expenses_column = 'Personnel expenses (thousand EUR) ' + selected_year
        goods_consumption_column = 'Goods and materials consumption (thousand EUR) ' + selected_year
        
        materials_column = 'Materials (thousand EUR) ' + selected_year
        cash_flow_column = 'Cash flow (thousand EUR) ' + selected_year
        ebit_column = 'EBIT (thousand EUR) ' + selected_year
        total_assets_column = 'Total assets (thousand EUR) ' + selected_year
        current_assets_column = 'Current assets (thousand EUR) ' + selected_year
        receivables_column = 'Receivables (thousand EUR) ' + selected_year
        inventory_column = 'Inventory (thousand EUR) ' + selected_year
        fixed_assets_column = 'Fixed assets (thousand EUR) ' + selected_year
        
        intangible_assets_column = 'Intangible assets (thousand EUR) ' + selected_year
        tangible_assets_column = 'Tangible assets (thousand EUR) ' + selected_year
        other_fixed_liabilities_column = 'Other fixed liabilities (thousand EUR) ' + selected_year
        total_liabilities_equity_column = 'Total liabilities and equity (thousand EUR) ' + selected_year
        working_capital_column = 'Working capital (thousand EUR) ' + selected_year
        number_employees_column = 'Number of employees ' + selected_year
        financial_debts_column = 'Financial debts (thousand EUR) ' + selected_year
        
        fixed_liabilities_column = 'Fixed liabilities (thousand EUR) ' + selected_year
        liquid_liabilities_column = 'Liquid liabilities (thousand EUR) ' + selected_year
        return_equity_column = 'Return on Equity (%), ' + selected_year
        return_assets_column = 'Return on Total Assets (%), ' + selected_year
        profit_margin_column = 'Profit Margin (%), ' + selected_year
        solvency_ratio_column = 'Solvency Ratio (%), ' + selected_year
        liquidity_ratio_column = 'Liquidity Ratio (%), ' + selected_year
        
        leverage_column = 'Leverage (%), ' + selected_year
        profit_per_employee_column = 'Profit per Employee (thousands), ' + selected_year
        average_employee_cost_column = 'Average Employee Cost (thousands), ' + selected_year
        total_assets_per_employee_column = 'Total Assets per Employee (thousands), ' + selected_year
        personnel_expenses_column = 'Personnel Expenses (%) ' + selected_year
        total_assets_column = 'Total Assets (%), ' + selected_year
        equity_column = 'Equity (%), ' + selected_year
        long_term_creditors_column = 'Long-term Creditors (%), ' + selected_year
        working_capital_ratio_column = 'Working Capital (%), ' + selected_year
        treasury_column = 'Treasury (%), ' + selected_year


        

        # Check if the columns exist in the company_data DataFrame
        if revenue_column in company_data.columns:
            filtered_data[revenue_column] = company_data[revenue_column]
        if ebitda_column in company_data.columns:
            filtered_data[ebitda_column] = company_data[ebitda_column]
        if gross_profit_column in company_data.columns:
            filtered_data[gross_profit_column] = company_data[gross_profit_column]
        if financial_income_column in company_data.columns:
            filtered_data[financial_income_column] = company_data[financial_income_column]
        if operating_result_column in company_data.columns:
            filtered_data[operating_result_column] = company_data[operating_result_column]
        if financial_expenses_column in company_data.columns:
            filtered_data[financial_expenses_column] = company_data[financial_expenses_column]
        if corporate_income_tax_column in company_data.columns:
            filtered_data[corporate_income_tax_column] = company_data[corporate_income_tax_column]
        if net_profit_column in company_data.columns:
            filtered_data[net_profit_column] = company_data[net_profit_column]
        if personnel_expenses_column in company_data.columns:
            filtered_data[personnel_expenses_column] = company_data[personnel_expenses_column]
        if goods_consumption_column in company_data.columns:
            filtered_data[goods_consumption_column] = company_data[goods_consumption_column]
        if materials_column in company_data.columns:
            filtered_data[materials_column] = company_data[materials_column]
        if cash_flow_column in company_data.columns:
            filtered_data[cash_flow_column] = company_data[cash_flow_column]
        if ebit_column in company_data.columns:
            filtered_data[ebit_column] = company_data[ebit_column]
        if total_assets_column in company_data.columns:
            filtered_data[total_assets_column] = company_data[total_assets_column]
        if current_assets_column in company_data.columns:
            filtered_data[current_assets_column] = company_data[current_assets_column]
        if receivables_column in company_data.columns:
            filtered_data[receivables_column] = company_data[receivables_column]
        if inventory_column in company_data.columns:
            filtered_data[inventory_column] = company_data[inventory_column]
        if fixed_assets_column in company_data.columns:
            filtered_data[fixed_assets_column] = company_data[fixed_assets_column]          
        if intangible_assets_column in company_data.columns:
            filtered_data[intangible_assets_column] = company_data[intangible_assets_column]
        if tangible_assets_column in company_data.columns:
            filtered_data[tangible_assets_column] = company_data[tangible_assets_column]
        if other_fixed_liabilities_column in company_data.columns:
            filtered_data[other_fixed_liabilities_column] = company_data[other_fixed_liabilities_column]
        if total_liabilities_equity_column in company_data.columns:
            filtered_data[total_liabilities_equity_column] = company_data[total_liabilities_equity_column]
        if working_capital_column in company_data.columns:
            filtered_data[working_capital_column] = company_data[working_capital_column]
        if number_employees_column in company_data.columns:
            filtered_data[number_employees_column] = company_data[number_employees_column]
        if financial_debts_column in company_data.columns:
            filtered_data[financial_debts_column] = company_data[financial_debts_column]         
        if fixed_liabilities_column in company_data.columns:
            filtered_data[fixed_liabilities_column] = company_data[fixed_liabilities_column]
        if liquid_liabilities_column in company_data.columns:
            filtered_data[liquid_liabilities_column] = company_data[liquid_liabilities_column]
        if return_equity_column in company_data.columns:
            filtered_data[return_equity_column] = company_data[return_equity_column]
        if return_assets_column in company_data.columns:
            filtered_data[return_assets_column] = company_data[return_assets_column]
        if profit_margin_column in company_data.columns:
            filtered_data[profit_margin_column] = company_data[profit_margin_column]
        if solvency_ratio_column in company_data.columns:
            filtered_data[solvency_ratio_column] = company_data[solvency_ratio_column]
        if liquidity_ratio_column in company_data.columns:
            filtered_data[liquidity_ratio_column] = company_data[liquidity_ratio_column]           
        if leverage_column in company_data.columns:
            filtered_data[leverage_column] = company_data[leverage_column]
        if profit_per_employee_column in company_data.columns:
            filtered_data[profit_per_employee_column] = company_data[profit_per_employee_column]
        if average_employee_cost_column in company_data.columns:
            filtered_data[average_employee_cost_column] = company_data[average_employee_cost_column]
        if total_assets_per_employee_column in company_data.columns:
            filtered_data[total_assets_per_employee_column] = company_data[total_assets_per_employee_column]
        if personnel_expenses_column in company_data.columns:
            filtered_data[personnel_expenses_column] = company_data[personnel_expenses_column]
        if total_assets_column in company_data.columns:
            filtered_data[total_assets_column] = company_data[total_assets_column]
        if equity_column in company_data.columns:
            filtered_data[equity_column] = company_data[equity_column]
        if long_term_creditors_column in company_data.columns:
            filtered_data[long_term_creditors_column] = company_data[long_term_creditors_column]
        if working_capital_ratio_column in company_data.columns:
            filtered_data[working_capital_ratio_column] = company_data[working_capital_ratio_column]
        if treasury_column in company_data.columns:
            filtered_data[treasury_column] = company_data[treasury_column]

        # Display the filtered data
        st.table(filtered_data)

        col1, col2 = st.columns(2)
        # Display operating revenue and gross profit
        with col1:
            st.write(f"**Operating Revenue (in thousand EUR):** {format_number(company_data['Operating Revenues (thousand EUR) ' + selected_year].values[0])}")
        with col2:
            st.write(f"**Gross Profit (in thousand EUR):** {format_number(company_data['Gross result (thousand EUR) ' + selected_year].values[0])}")

        # Display EBITDA and net income
        with col1:
            st.write(f"**EBITDA (in thousand EUR):** {format_number(company_data['EBITDA (thousand EUR) ' + selected_year].values[0])}")
        with col2:
            st.write(f"**Net Income (in thousand EUR):** {format_number(company_data['Net profit (thousand EUR) ' + selected_year].values[0])}")

        # Display return on equity and return on total assets
        with col1:
            st.write(f"**Return on Equity (%):** {format_number(company_data['Return on Equity (%), ' + selected_year].values[0])}")
        with col2:
            st.write(f"**Return on Total Assets (%):** {format_number(company_data['Return on Total Assets (%), ' + selected_year].values[0])}")

        # Display profit margin and solvency ratio
        with col1:
            st.write(f"**Profit Margin (%):** {format_number(company_data['Profit Margin (%), ' + selected_year].values[0])}")
        with col2:
            st.write(f"**Solvency Ratio (%):** {format_number(company_data['Solvency Ratio (%), ' + selected_year].values[0])}")

        # Display liquidity ratio and leverage ratio
        with col1:
            st.write(f"**Liquidity Ratio (%):** {format_number(company_data['Liquidity Ratio (%), ' + selected_year].values[0])}")
        with col2:
            st.write(f"**Leverage Ratio (%):** {format_number(company_data['Leverage (%), ' + selected_year].values[0])}")
            

        import pandas as pd
        import plotly.graph_objects as go
        import streamlit as st


 


        # Get the list of variables
        variables = [
            'Operating Revenues (thousand EUR)',
            'EBITDA (thousand EUR)',
            'Gross result (thousand EUR)',
            'Financial income (thousand EUR)',
            'Operating result (thousand EUR)',
            'Financial expenses (thousand EUR)',
            'Corporate income tax (thousand EUR)',
            'Net profit (thousand EUR)',
            'Personnel expenses (thousand EUR)',
            'Goods and materials consumption (thousand EUR)',
            'Materials (thousand EUR)',
            'Cash flow (thousand EUR)',
            'EBIT (thousand EUR)',
            'Total assets (thousand EUR)',
            'Current assets (thousand EUR)',
            'Receivables (thousand EUR)',
            'Inventory (thousand EUR)',
            'Fixed assets (thousand EUR)',
            'Intangible assets (thousand EUR)',
            'Tangible assets (thousand EUR)',
            'Other fixed liabilities (thousand EUR)',
            'Total liabilities and equity (thousand EUR)',
            'Working capital (thousand EUR)',
            'Number of employees',
            'Financial debts (thousand EUR)',
            'Fixed liabilities (thousand EUR)',
            'Liquid liabilities (thousand EUR)',
            'Return on Equity (%)',
            'Return on Total Assets (%)',
            'Profit Margin (%)',
            'Solvency Ratio (%)',
            'Liquidity Ratio (%)',
            'Leverage (%)',
            'Profit per Employee (thousands)',
            'Average Employee Cost (thousands)',
            'Total Assets per Employee (thousands)',
            'Personnel Expenses (%)',
            'Total Assets (%)',
            'Equity (%)',
            'Long-term Creditors (%)',
            'Working Capital (%)',
            'Treasury (%)'
        ]
        

        # Sidebar for selecting a variable
        selected_variable = st.sidebar.selectbox("Select a Variable for Plotting th Hisogram:", variables)

        # Extract the corresponding column names from the DataFrame
        column_names = [column for column in df.columns if selected_variable in column]

        # Extract the years from the column names
        years = [column.split()[-1] for column in column_names]

        # Filter the DataFrame to include only the selected variable columns
        filtered_df = df[column_names]

        # Prepare the data for plotting
        data = [go.Bar(x=years, y=filtered_df.iloc[0].values)]

        # Create the layout for the plot
        layout = go.Layout(title=f"{selected_variable} - Evolution Over the Years")

        # Create the figure
        fig = go.Figure(data=data, layout=layout)
        
        st.title("Histogram Plot")
        
        st.write("Variable Chosen : ")

        # Plot the bar chart
        st.plotly_chart(fig)
        
        
       # ...

        # Additional visualizations
        st.subheader("Additional Visualizations")

        # Sidebar for selecting the visualization type
        visualization_type = st.selectbox("Select Visualization Type:", ["Line Plot", "Pie Chart", "Scatter Plot"])

        # Display the graph based on the selected visualization type
        if visualization_type == "Line Plot":
            # Create a line plot
            line_data = filtered_df.iloc[0].values
            line_fig = go.Figure(data=go.Scatter(x=years, y=line_data, mode='lines'))
            line_fig.update_layout(title=f"{selected_variable} - Line Plot")
            st.plotly_chart(line_fig)

        elif visualization_type == "Pie Chart":
            # Create a pie chart
            pie_data = filtered_df.iloc[0].values
            pie_fig = go.Figure(data=go.Pie(labels=years, values=pie_data))
            pie_fig.update_layout(title=f"{selected_variable} - Pie Chart")
            st.plotly_chart(pie_fig)

        elif visualization_type == "Scatter Plot":
            # Create a scatter plot
            scatter_data = filtered_df.iloc[0].values
            scatter_fig = go.Figure(data=go.Scatter(x=years, y=scatter_data, mode='markers'))
            scatter_fig.update_layout(title=f"{selected_variable} - Scatter Plot")
            st.plotly_chart(scatter_fig)





# Company Financial Efficiency Ratios


elif choice == 'Company Financial Efficiency Ratios':
    st.title("Company Financial Efficiency Ratios")
    
    
    
    menu = ['Individual Information', 'Global Information']
    choice = st.sidebar.selectbox("Select a Section:", menu)
    
    if choice == 'Individual Information':

        # Company and year selection
        selected_companies = st.multiselect("Select Companies", df["Name"].unique())
        year_range = range(2010, 2023)  # Update to include 2022

        st.write("Metric Selected : ")

        # Calculate ratios for all years
        ratios_data = []
        for company_name in selected_companies:
            for year in year_range:
                year_column = str(year)

                filtered_df = df[df['Name'] == company_name]
                filtered_df = filtered_df.filter(regex=f'.*{year_column}$')

                if filtered_df.empty:
                    continue

                # Convert columns to numeric values
                numeric_columns = [
                    f'Operating Revenues (thousand EUR) {year_column}',
                    f'Gross result (thousand EUR) {year_column}',
                    f'Operating result (thousand EUR) {year_column}',
                    f'Net profit (thousand EUR) {year_column}',
                    f'Total assets (thousand EUR) {year_column}',
                    f'Current assets (thousand EUR) {year_column}',
                    f'Inventory (thousand EUR) {year_column}'
                ]
                filtered_df[numeric_columns] = filtered_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

                operating_revenues = filtered_df[f'Operating Revenues (thousand EUR) {year_column}']
                gross_result = filtered_df[f'Gross result (thousand EUR) {year_column}']
                operating_result = filtered_df[f'Operating result (thousand EUR) {year_column}']
                net_profit = filtered_df[f'Net profit (thousand EUR) {year_column}']
                total_assets = filtered_df[f'Total assets (thousand EUR) {year_column}']
                current_assets = filtered_df[f'Current assets (thousand EUR) {year_column}']
                inventory = filtered_df[f'Inventory (thousand EUR) {year_column}']

                gross_margin = (gross_result / operating_revenues) * 100
                operating_margin = (operating_result / operating_revenues) * 100
                roa = (net_profit / total_assets) * 100
                net_profit_margin = (net_profit / operating_revenues) * 100
                current_ratio = current_assets / total_assets
                quick_ratio = (current_assets - inventory) / total_assets

                ratios_data.append({
                    "Company": company_name,
                    "Year": year,
                    "Gross Margin": gross_margin.values[0],
                    "Operating Margin": operating_margin.values[0],
                    "Return on Assets (ROA)": roa.values[0],
                    "Net Profit Margin": net_profit_margin.values[0],
                    "Current Ratio": current_ratio.values[0],
                    "Quick Ratio": quick_ratio.values[0]
                })

        # Create a new DataFrame for ratios
        ratios_df = pd.DataFrame(ratios_data)

        # Sidebar for selecting a variable
        selected_variable = st.sidebar.selectbox("Select a Variable:", ratios_df.columns[2:])

        # Prepare the data for plotting
        data = []
        for company in selected_companies:
            company_data = ratios_df[ratios_df["Company"] == company]
            data.append(go.Bar(x=company_data["Year"], y=company_data[selected_variable], name=company))

        # Create the layout for the plot
     
        layout = go.Layout(title=f"{selected_variable} - Evolution Over the Years", width=800)


        # Create the figure
        fig = go.Figure(data=data, layout=layout)

        # Plot the bar chart
        st.plotly_chart(fig, use_container_width=False)

        # Trend Analysis
        st.subheader("Trend Analysis")

        # Prepare the data for plotting
        trend_data = []
        for company in selected_companies:
            company_data = ratios_df[ratios_df["Company"] == company]
            trend_data.append(go.Scatter(x=company_data["Year"], y=company_data[selected_variable], mode="lines", name=company))

        # Create the layout for the trend plot
        trend_layout = go.Layout(title=f"{selected_variable} - Trend Over the Years",
                                 xaxis=dict(title="Year"),
                                 yaxis=dict(title=selected_variable))



        # Create the figure for the trend plot
        trend_fig = go.Figure(data=trend_data, layout=trend_layout)

        # Plot the trend line chart
        st.plotly_chart(trend_fig)

       




        
        
    elif choice == 'Global Information':

        st.header("Global Information")

         # Create a list of all available ratios
        ratios = [
            "Gross Margin",
            "Operating Margin",
            "Return on Assets (ROA)",
            "Net Profit Margin",
            "Current Ratio",
            "Quick Ratio"
        ]

        # Company and year selection
        selected_companies = st.multiselect("Select Companies", df["Name"].unique())
        year_range = range(2010, 2023)  # Update to include 2022
        selected_year = st.selectbox("Select a Year", year_range)

        ratios_data = []
        for company_name in selected_companies:
            filtered_df = df[df['Name'] == company_name]
            filtered_df = filtered_df.filter(regex=f'.*{selected_year}$')

            if filtered_df.empty:
                continue

            operating_revenues = filtered_df[f'Operating Revenues (thousand EUR) {selected_year}']
            gross_result = filtered_df[f'Gross result (thousand EUR) {selected_year}']
            operating_result = filtered_df[f'Operating result (thousand EUR) {selected_year}']
            net_profit = filtered_df[f'Net profit (thousand EUR) {selected_year}']
            total_assets = filtered_df[f'Total assets (thousand EUR) {selected_year}']
            current_assets = filtered_df[f'Current assets (thousand EUR) {selected_year}']
            inventory = filtered_df[f'Inventory (thousand EUR) {selected_year}']

            # Convert 'n.d.' values to NaN
            gross_result = gross_result.replace('n.d.', np.nan)
            operating_result = operating_result.replace('n.d.', np.nan)
            net_profit = net_profit.replace('n.d.', np.nan)
            total_assets = total_assets.replace('n.d.', np.nan)
            current_assets = current_assets.replace('n.d.', np.nan)
            inventory = inventory.replace('n.d.', np.nan)

            # Convert columns to float
            gross_result = gross_result.astype(float)
            operating_result = operating_result.astype(float)
            net_profit = net_profit.astype(float)
            total_assets = total_assets.astype(float)
            current_assets = current_assets.astype(float)
            inventory = inventory.astype(float)

            # Calculate ratios
            gross_margin = (gross_result / operating_revenues) * 100
            operating_margin = (operating_result / operating_revenues) * 100
            roa = (net_profit / total_assets) * 100
            net_profit_margin = (net_profit / operating_revenues) * 100
            current_ratio = current_assets / total_assets
            quick_ratio = (current_assets - inventory) / total_assets

            ratios_data.append({
                "Company": company_name,
                "Gross Margin": gross_margin.values[0],
                "Operating Margin": operating_margin.values[0],
                "Return on Assets (ROA)": roa.values[0],
                "Net Profit Margin": net_profit_margin.values[0],
                "Current Ratio": current_ratio.values[0],
                "Quick Ratio": quick_ratio.values[0]
            })

        ratios_df = pd.DataFrame(ratios_data)
        ratios_df.set_index("Company", inplace=True)

        # Sidebar for selecting variables
        x_ratio, y_ratio = st.columns(2)
        with x_ratio:
            x_axis_ratio = st.selectbox("Select a ratio/margin for the X axis", ratios)
        with y_ratio:
            y_axis_ratio = st.selectbox("Select a ratio/margin for the Y axis", ratios)

        # Prepare the data for plotting
        data = []
        for i, company in enumerate(ratios_df.index):
            x_values = [ratios_df.loc[company, x_axis_ratio]]
            y_values = [ratios_df.loc[company, y_axis_ratio]]
            text = [company]
            data.append(go.Scatter(x=x_values, y=y_values, mode='markers',
                                   text=text, marker=dict(size=10),
                                   hovertemplate="Company: %{text}<br>" + x_axis_ratio + ": %{x}<br>" +
                                   y_axis_ratio + ": %{y}", name=company))

        # Create the layout for the plot
        layout = go.Layout(title=f"{x_axis_ratio} vs {y_axis_ratio} - Global Information",
                           xaxis=dict(title=x_axis_ratio),
                           yaxis=dict(title=y_axis_ratio))

        # Create the figure
        fig = go.Figure(data=data, layout=layout)

        # Plot the scatter chart
        st.plotly_chart(fig, use_container_width=True)
        
        
        # Calculate correlation coefficient
        x_values = ratios_df[x_axis_ratio].values
        y_values = ratios_df[y_axis_ratio].values
        correlation_coefficient = np.corrcoef(x_values, y_values)[0, 1]

        # Display correlation analysis
        st.subheader("Correlation Analysis")
        st.write(f"The correlation coefficient between {x_axis_ratio} and {y_axis_ratio} is: {correlation_coefficient:.2f}")

        






        
      



# Market Analysis
elif choice == 'Market Analysis':
    st.title("Market Analysis")

    # Sidebar for selecting a country
    country_names = df['Country'].unique()
    selected_country = st.sidebar.selectbox("Select a Country:", country_names)

    # Filter dataframe for the selected country
    country_data = df[df['Country'] == selected_country]

    # Sidebar for selecting a company
    company_names = country_data['Name'].unique()
    selected_company = st.sidebar.selectbox("Select a Company:", company_names)

    # Filter dataframe for the selected company
    company_data = country_data[country_data['Name'] == selected_company]

    st.write(f"**Selected Company:** {selected_company}")

    # Market Size
    st.subheader("Market Size")
    try:
        if 'Operating Revenue (in thousand EUR)' not in company_data.columns:
            raise KeyError("Operating Revenue (in thousand EUR) column is missing")

        # Replace 'n.d.' values with NaN
        company_data = company_data.replace('n.d.', np.nan)

        # Calculate total operating revenue for the country
        country_revenue = country_data['Operating Revenue (in thousand EUR)'].astype(float).sum()

        # Calculate market share for the selected company
        company_revenue = company_data['Operating Revenue (in thousand EUR)'].astype(float).sum()
        market_share = 100 * company_revenue / country_revenue

        market_size = company_revenue / market_share
        st.write(f"Market Size: {f'{market_size:,.2f}'} million EUR")
    except (KeyError, ValueError) as e:
        st.warning(f"Cannot calculate Market Size: {str(e)}")

    # Growth Potential
    st.subheader("Growth Potential")
    try:
        if 'Operating Revenue (in thousand EUR)' not in company_data.columns:
            raise KeyError("Operating Revenue (in thousand EUR) column is missing")

        # Replace 'n.d.' values with NaN
        company_data = company_data.replace('n.d.', np.nan)

        # Calculate revenue growth rate for the last 3 years
        revenue_data = company_data[['Operating Revenue (in thousand EUR)', 'Country']].sort_values(by='Country')
        revenue_data['Operating Revenue (in thousand EUR)'] = revenue_data['Operating Revenue (in thousand EUR)'].astype(float)
        revenue_data = revenue_data.groupby('Country').apply(lambda x: (x['Operating Revenue (in thousand EUR)'].iloc[-1] / x['Operating Revenue (in thousand EUR)'].iloc[0])**(1/3) - 1)
        revenue_growth_rate = revenue_data.mean() * 100

        st.write(f"Revenue Growth Rate (3-year average): {format(revenue_growth_rate, '.2f')}%")

    except (KeyError, ValueError) as e:
        st.warning(f"Cannot calculate Growth Potential: {str(e)}")

        # Competitive Landscape
    # Competitive Landscape
    try:
        st.subheader("Competitive Landscape")

        if 'Operating Revenue (in thousand EUR)' not in df.columns:
            raise KeyError("Operating Revenue (in thousand EUR) column is missing")

        # Replace 'n.d.' values with NaN
        df = df.replace('n.d.', np.nan)

        # Filter dataframe for the selected country
        country_data = df[df['Country'] == selected_country]

        # Calculate total operating revenue for the country
        country_revenue = country_data['Operating Revenue (in thousand EUR)'].sum()

        # Calculate market share for all companies in the country
        total_revenue = country_data['Operating Revenue (in thousand EUR)'].sum()
        country_data['Market Share'] = country_data['Operating Revenue (in thousand EUR)'] / total_revenue

        # Display top 10 companies by market share
        top_10_companies = country_data.sort_values('Market Share', ascending=False).head(10)
        st.subheader("Top 10 Companies by Market Share")
        st.dataframe(top_10_companies[['Name', 'Market Share']].reset_index(drop=True))

        # Calculate market concentration
        market_concentration = 100 * top_10_companies['Market Share'].sum()
        st.write(f"Market Concentration: {format(market_concentration, '.2f')}%")

    except (KeyError, ValueError) as e:
        st.warning(f"Cannot calculate Competitive Landscape: {str(e)}")




                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
        
elif choice == "Machine Learning Insights":
    st.title("Machine Learning Insights")
    st.write("Select a machine learning algorithm to explore insights:")
    ml_algorithm = st.selectbox("", ["Clustering Analysis",'Random Forest Classifier', 'PCA', 'Support Vector Machine (SVM)', 'Isolation Forest - Anomaly Detection'])

    if ml_algorithm == "Clustering Analysis":
        st.title("Clustering Analysis")
        st.write("Use unsupervised machine learning algorithms such as K-Means or DBSCAN to group companies based on their financial metrics and ratios. This can help you identify clusters of companies that share similar financial characteristics and may be good M&A targets.")

        # Select the columns to use for clustering
        cluster_cols = ['Operating Revenue (in thousand EUR)', 'Gross Profit (in thousand EUR)', 'EBITDA (in thousand EUR)', 'Operating Income (in thousand EUR)', 'Financial Income (in thousand EUR)', 'Financial Expenses (in thousand EUR)', 'Corporate Taxes (in thousand EUR)', 'Net Income (in thousand EUR)', 'Personnel Expenses (in thousand EUR)', 'Cost of Goods Sold (in thousand EUR)']

        # Normalize the data
        scaler = StandardScaler()
        X = df[cluster_cols].values
        X = scaler.fit_transform(X)

        # Set the number of clusters
        n_clusters = 5

        # Fit the K-Means model
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(X)

        # Add the cluster labels to the DataFrame
        df['Cluster'] = kmeans.labels_

        # Display the number of companies in each cluster
        cluster_counts = df['Cluster'].value_counts()
        st.write(f"There are {len(cluster_counts)} clusters:")
        for i, count in cluster_counts.iteritems():
            st.write(f"- Cluster {i}: {count} companies")

        # Display a scatter plot of the clusters
        fig = px.scatter(df, x='Operating Revenue (in thousand EUR)', y='Net Income (in thousand EUR)', color='Cluster', hover_data=['Name'])
        st.plotly_chart(fig)

    elif ml_algorithm == "Random Forest Classifier":
        st.title("Random Forest Classifier")
        st.write("Use a supervised machine learning algorithm such as Random Forest to classify companies as good or bad M&A targets based on their financial metrics and ratios.")

        # Create a new column called 'M&A Target' and set the values based on net income
        df['M&A Target'] = np.where(df['Net Income (in thousand EUR)'] > 0, 'Good', 'Bad')

        # Set the columns to use for classification
        classifier_cols = ['Operating Revenue (in thousand EUR)', 'Gross Profit (in thousand EUR)', 'EBITDA (in thousand EUR)', 'Operating Income (in thousand EUR)', 'Financial Income (in thousand EUR)', 'Financial Expenses (in thousand EUR)', 'Corporate Taxes (in thousand EUR)', 'Personnel Expenses (in thousand EUR)', 'Cost of Goods Sold (in thousand EUR)']

        # Define the input and output variables
        X = df[classifier_cols].values
        y = df['M&A Target'].values

        # Create a Random Forest Classifier with 100 trees
        rfc = RandomForestClassifier(n_estimators=100, random_state=0)

        # Fit the classifier to the data
        rfc.fit(X, y)

        # Get the feature importances
        importances = rfc.feature_importances_

        # Create a DataFrame with the feature names and their importances
        feature_importances = pd.DataFrame({'feature': classifier_cols, 'importance': importances})

        # Sort the DataFrame by the importance in descending order
        feature_importances = feature_importances.sort_values('importance', ascending=False)

        # Display the feature importances
        st.write("Feature Importances:")
        st.write(feature_importances)

        # Create a dropdown menu to select a company
        selected_company = st.selectbox("Select a company:", df['Name'])

        # Get the financial metrics for the selected company
        company_metrics = df[df['Name'] == selected_company][classifier_cols].values

        # Predict the M&A target for the selected company
        target = rfc.predict(company_metrics)[0]

        # Display whether the selected company is a good or bad M&A target
        st.write(f"{selected_company} is a {target} M&A target.")

        # Add an "Explanation" dropdown
        if st.checkbox("Explanation"):
            st.write("The Random Forest Classifier predicts whether a company is a good or bad M&A target based on its financial metrics and ratios. The classifier was trained on a dataset of companies that were labeled as either 'Good' or 'Bad' M&A targets based on whether they had positive or negative net income. The classifier uses the input financial metrics and ratios to make a prediction on whether a given company is a 'Good' or 'Bad' M&A target, based on how similar its financials are to the companies in the training set.")

        # Calculate the precision, recall, and F1-score
        y_pred = rfc.predict(X)
        report = classification_report(y, y_pred, output_dict=True)
        df_report = pd.DataFrame(report).transpose()
        st.write("Classification Report:")
        st.write(df_report)
        
        
    elif ml_algorithm == "PCA":
        st.title("Principal Component Analysis (PCA)")
        st.write("Use PCA to identify patterns and relationships in high-dimensional data and reduce the number of variables in your dataset.")

        # Set the columns to use for PCA
        pca_cols = ['Operating Revenue (in thousand EUR)', 'Gross Profit (in thousand EUR)', 'EBITDA (in thousand EUR)', 'Operating Income (in thousand EUR)', 'Financial Income (in thousand EUR)', 'Financial Expenses (in thousand EUR)', 'Corporate Taxes (in thousand EUR)', 'Personnel Expenses (in thousand EUR)', 'Cost of Goods Sold (in thousand EUR)']

        # Define the input variables
        X = df[pca_cols].values

        # Perform PCA on the input data
        pca = PCA(n_components=2)
        principal_components = pca.fit_transform(X)

        # Create a DataFrame with the principal components
        principal_df = pd.DataFrame(data = principal_components, columns = ['principal component 1', 'principal component 2'])

        # Concatenate the principal components with the company names
        final_df = pd.concat([principal_df, df[['Name']]], axis = 1)

        # Plot the principal components
        fig = px.scatter(final_df, x='principal component 1', y='principal component 2', hover_name='Name')
        st.plotly_chart(fig)
        
        # Add an "Explanation" dropdown
        if st.checkbox("Explanation"):
            st.write("Principal Component Analysis (PCA) is a dimensionality reduction technique that can be used to identify patterns and relationships in high-dimensional data. It works by finding new dimensions, called principal components, that capture as much of the variability in the data as possible. The first principal component captures the most variability in the data, the second principal component captures the second most variability, and so on. By reducing the number of dimensions, PCA can help simplify your analysis and improve the accuracy of your predictions, while still capturing as much of the variability in the data as possible.")
            
            
            
            
    elif ml_algorithm == "Support Vector Machine (SVM)":
        st.title("Support Vector Machine (SVM)")
        st.write("Use a supervised machine learning algorithm such as SVM to classify companies as good or bad M&A targets based on their financial metrics and ratios.")

        # Create a new column called 'M&A Target' and set the values based on net income
        df['M&A Target'] = np.where(df['Net Income (in thousand EUR)'] > 0, 'Good', 'Bad')

        from sklearn.model_selection import train_test_split

        # Set the columns to use for classification
        classifier_cols = ['Operating Revenue (in thousand EUR)', 'Gross Profit (in thousand EUR)', 'EBITDA (in thousand EUR)', 'Operating Income (in thousand EUR)', 'Financial Income (in thousand EUR)', 'Financial Expenses (in thousand EUR)', 'Corporate Taxes (in thousand EUR)', 'Personnel Expenses (in thousand EUR)', 'Cost of Goods Sold (in thousand EUR)']

        # Define the input and output variables
        X = df[classifier_cols].values
        y = df['M&A Target'].values

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Encode the labels
        le = LabelEncoder()
        y_train_encoded = le.fit_transform(y_train)

        # Fit the PCA to the training data
        pca = PCA(n_components=2)
        X_train_reduced = pca.fit_transform(X_train)

        # Create a Support Vector Machine with a linear kernel
        svm = SVC(kernel='linear', C=1, random_state=0)

        # Fit the SVM to the training data
        svm.fit(X_train_reduced, y_train_encoded)

        # Create a dropdown menu to select a company
        selected_company = st.selectbox("Select a company:", df['Name'])

        # Get the financial metrics for the selected company
        company_metrics = df[df['Name'] == selected_company][classifier_cols].values

        # Predict the M&A target for the selected company
        target = svm.predict(pca.transform(company_metrics))[0]
        target = le.inverse_transform([target])[0]

        # Display whether the selected company is a good or bad M&A target
        st.write(f"{selected_company} is a {target} M&A target.")

        # Generate a meshgrid of points for plotting the decision boundary
        h = 0.0001  # step size in the mesh
        x_min, x_max = X_train_reduced[:, 0].min() - 1, X_train_reduced[:, 0].max() + 1
        y_min, y_max = X_train_reduced[:, 1].min() - 1, X_train_reduced[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        X_mesh = np.c_[xx.ravel(), yy.ravel()]

        # Predict the M&A targets for the meshgrid points
        Z = svm.predict(X_mesh)

        # Reshape the predicted targets into a meshgrid
        Z = Z.reshape(xx.shape)

        # Plot the decision boundary and the data points
        fig, ax = plt.subplots()
        scatter = ax.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y_encoded, cmap='bwr')
        ax.contour(xx, yy, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])
        ax.set_xlabel('Principal Component 1')
        ax.set_ylabel('Principal Component 2')
        ax.set_title('Support Vector Machine')
        st.write(fig)



    elif ml_algorithm == "Isolation Forest - Anomaly Detection":
        st.title("Isolation Forest - Anomaly Detection")

        # Select the numerical columns for analysis
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        selected_columns = st.multiselect("Select the numerical columns to analyze:", numerical_cols)
        if not selected_columns:
            st.warning("Please select at least one column for analysis.")
            st.stop()

        # Filter the data to only include selected columns
        filtered_data = df[selected_columns]

        # Replace 'n.d.' values with NaN
        filtered_data = filtered_data.replace('n.d.', np.nan)

        # Remove rows with missing data
        filtered_data = filtered_data.dropna()

        # Create isolation forest model and fit to data
        iso_forest = IsolationForest(n_estimators=100, contamination='auto', random_state=42)
        iso_forest.fit(filtered_data)

        # Predict outliers using isolation forest model
        outlier_preds = iso_forest.predict(filtered_data)

        # Create dataframe of outliers
        outliers = filtered_data[outlier_preds == -1]

        # Merge outliers with company_data to show company name
        company_names = df['Name']
        outlier_names = company_names[outlier_preds == -1]
        outliers = pd.concat([outliers, outlier_names], axis=1)

        # Display number of outliers found
        st.write(f"Number of outliers found: {len(outliers)}")

        # Display table of outlier data
        st.write(outliers)
        
        if st.button("Extra Information"):
            st.write("Isolation Forest is an unsupervised learning algorithm used for anomaly detection. It works by isolating observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature. The number of splits required to isolate the observation is counted, and the anomaly score is given by the average of the number of splits over all trees. The algorithm is efficient and can work well even in high-dimensional spaces.")


# Define the list of variables
variables = [
    'Operating Revenues (thousand EUR)',
    'EBITDA (thousand EUR)',
    'Gross result (thousand EUR)',
    'Financial income (thousand EUR)',
    'Operating result (thousand EUR)',
    'Financial expenses (thousand EUR)',
    'Corporate income tax (thousand EUR)',
    'Net profit (thousand EUR)',
    'Personnel expenses (thousand EUR)',
    'Goods and materials consumption (thousand EUR)',
    'Materials (thousand EUR)',
    'Cash flow (thousand EUR)',
    'EBIT (thousand EUR)',
    'Total assets (thousand EUR)',
    'Current assets (thousand EUR)',
    'Receivables (thousand EUR)',
    'Inventory (thousand EUR)',
    'Fixed assets (thousand EUR)',
    'Intangible assets (thousand EUR)',
    'Tangible assets (thousand EUR)',
    'Other fixed liabilities (thousand EUR)',
    'Total liabilities and equity (thousand EUR)',
    'Working capital (thousand EUR)',
    'Number of employees',
    'Financial debts (thousand EUR)',
    'Fixed liabilities (thousand EUR)',
    'Liquid liabilities (thousand EUR)',
    'Return on Equity (%)',
    'Return on Total Assets (%)',
    'Profit Margin (%)',
    'Solvency Ratio (%)',
    'Liquidity Ratio (%)',
    'Leverage (%)',
    'Profit per Employee (thousands)',
    'Average Employee Cost (thousands)',
    'Total Assets per Employee (thousands)',
    'Personnel Expenses (%)',
    'Total Assets (%)',
    'Equity (%)',
    'Long-term Creditors (%)',
    'Working Capital (%)',
    'Treasury (%)'
]

if choice == "Valuation Calculator":
    st.title("Valuation Calculator")

    # Company selection
    company_name = st.selectbox("Select Company", df["Name"].unique())

    # Discount rate input
    discount_rate = st.number_input("Discount Rate (%)", value=10.0)

    # Free Cash Flow input
    free_cash_flow = st.number_input("Free Cash Flow (thousand EUR)")

    # Calculate the discounted cash flow
    dcf = free_cash_flow / (1 + discount_rate/100)  # Adjust the formula based on your specific calculation

    # Display the DCF result
    st.subheader("DCF Valuation Result")
    st.write(f"The discounted cash flow (DCF) for {company_name} is: {dcf:.2f} thousand EUR")

    


































       



