import numpy as np
import pandas as pd




class Enricher:
    def __init__(self,logger):
        self.logger = logger

    def calcular_kpi(self,df=pd.DataFrame()): #mínimo 5 KPI (tasa de variación, media móvil, volatilidad, retorno acumulado, desviación estándar, etc.).
        try:
          df = df.copy()
          # ordenar
          df = df.sort_values('fecha')
          for col in df.columns:
             if col != "fecha":
                df[col]= pd.to_numeric(df[col].str.replace(',', '.',regex=False),errors='coerce')
          # 1er indicador volatilidad (desviacion de los ult. 5 dias)
          df['volatilidad']=df['cerrar'].rolling(window=5).std().fillna(0)
          self.logger.info('Enricher','calcular_kpi','agregar indicadores KPI')
          return df
        except Exception as errores:
          self.logger.error(f'Enricher','calcular_kpi','Error al enriquecer el df{errores}')
          df=pd.DataFrame()
          return df