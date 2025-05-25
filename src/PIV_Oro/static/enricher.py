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

            # Limpiar nombres de columnas
            df.columns = df.columns.str.strip().str.lower()

            # Procesamiento personalizado de fechas
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
            df["fecha"] = pd.to_datetime(fechas_convertidas, errors="coerce")

            # Ordenar por fecha
            df = df.sort_values("fecha")

            # Conversión de columnas numéricas (excepto fecha)
            for col in df.columns:
                if col != "fecha":
                    df[col] = (
                        df[col]
                        .astype(str)
                        .str.replace('.', '', regex=False)  # eliminar separador de miles
                        .str.replace(',', '.', regex=False)  # cambiar decimal
                    )
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Validar existencia de columna clave
            if "cerrar" not in df.columns or not pd.api.types.is_numeric_dtype(df["cerrar"]):
                raise ValueError("La columna 'cerrar' no existe o no es numérica.")

            # Cálculo de indicadores KPI
            df["media_movil_7d"] = df["cerrar"].rolling(window=7).mean()
            df["tasa_variacion"] = df["cerrar"].pct_change()
            df["retorno_acumulado"] = (1 + df["tasa_variacion"]).cumprod() - 1
            df["volatilidad_anualizada"] = df["tasa_variacion"].rolling(window=21).std() * np.sqrt(252)
            df["volatilidad"] = df["cerrar"].rolling(window=5).std()

            # Rellenar y redondear KPIs
            columnas_kpi = ["media_movil_7d", "tasa_variacion", "retorno_acumulado", "volatilidad_anualizada", "volatilidad"]
            df[columnas_kpi] = df[columnas_kpi].fillna(0).round(4)

            self.logger.info('Enricher', 'calcular_kpi', 'Indicadores KPI calculados correctamente.')
            return df

        except Exception as errores:
            self.logger.error('Enricher', 'calcular_kpi', f'Error al enriquecer el df: {errores}')
            return pd.DataFrame()
