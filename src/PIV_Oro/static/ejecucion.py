from logger import Logger
from collector import Collector
from enricher import Enricher
import pandas as pd

nombredb="postgres"
nombre_tabla = "hist_oro"
nombre_schema = "historico"
ruta_sql="/src/PIV_Oro/static/Script_sql"


def main():
    logger = Logger()
    df = pd.DataFrame()
    logger.info('Main','main','Inicializar clase Logger')
    collector = Collector(logger=logger)
    df =collector.collector_data()
    enricher = Enricher(logger=logger)
    df.to_csv("src/PIV_Oro/static/data/Oro_datosOriginales.csv", sep=";", index=False)
    df_2=enricher.calcular_kpi(df)
    df_2.to_csv("src/PIV_Oro/static/data/Oro_datosOriginales_enricher.csv", sep=";", index=False)




if __name__ == "__main__":
    main()