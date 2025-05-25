import numpy as np
import pandas as pd
from datetime import datetime

class Enricher:
    def __init__(self, logger):
        self.logger = logger
        self.meses = {
            "ene": "jan", "feb": "feb", "mar": "mar", "abr": "apr",
            "may": "may", "jun": "jun", "jul": "jul", "ago": "aug",
            "sept": "sep", "oct": "oct", "nov": "nov", "dic": "dec"
        }

    def calcular_kpi(self, df=pd.DataFrame()):
        try:
            df = df.copy()

            fechas_convertidas = []
            for fecha in df["fecha"]:
                if not fecha or fecha == '0':
                    fechas_convertidas.append(datetime.now().strftime("%Y-%m-%d"))
                else:
                    try:
                        fecha_raw = str(fecha).lower()
                        for mes_es, mes_en in self.meses.items():
                            if mes_es in fecha_raw:
                                fecha_raw = fecha_raw.replace(mes_es, mes_en)
                        fecha_dt = datetime.strptime(fecha_raw, "%d %b %Y")
                        fechas_convertidas.append(fecha_dt.strftime("%Y-%m-%d"))
                    except Exception as e:
                        self.logger.warning("Enricher", "calcular_kpi", f"Fecha malformada '{fecha}': {e}")
                        fechas_convertidas.append(datetime.now().strftime("%Y-%m-%d"))

            df["fecha"] = pd.to_datetime(fechas_convertidas)

            # Conversión de columnas numéricas
            for col in df.columns:
                if col != "fecha":
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.', regex=False), errors='coerce')

            # Cálculo de indicadores KPI
            df["media_movil_7d"] = df["cerrar"].rolling(window=7, min_periods=1).mean()
            df["tasa_variacion"] = df["cerrar"].pct_change().fillna(0)
            df["retorno_acumulado"] = (1 + df["tasa_variacion"]).cumprod() - 1
            df["std_5d"] = df["cerrar"].rolling(window=5, min_periods=1).std()
            df["volatilidad"] = df["cerrar"].rolling(window=5, min_periods=1).std()


            self.logger.info('Enricher', 'calcular_kpi', 'Indicadores KPI calculados correctamente.')
            return df

        except Exception as errores:
            self.logger.error('Enricher', 'calcular_kpi', f'Error al enriquecer el df: {errores}')
            return pd.DataFrame()
