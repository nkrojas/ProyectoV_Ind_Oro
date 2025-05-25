import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


class Modelador:
    def __init__(self, path_csv='src/PIV_Oro/static/data/Oro_datosOriginales_enricher.csv'):
        self.path_csv = path_csv
        self.model_path = 'static/models/model.pkl'
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def cargar_datos(self):
        df = pd.read_csv(self.path_csv, sep=';', parse_dates=['fecha'])
        df = df.sort_values(by='fecha')  # ordena por tiempo
        df = df.dropna()  # elimina filas con valores faltantes
        return df

    def entrenar(self):
        df = self.cargar_datos()

        # Seleccionamos características predictoras
        X = df[['abrir', 'max', 'min', 'volumen', 'media_movil_7d',
                'tasa_variacion', 'retorno_acumulado', 'std_5d', 'volatilidad']]
        y = df['cerrar']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrena el modelo
        self.model.fit(X_train, y_train)

        # Validación
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        print(f'RMSE del modelo: {rmse:.2f}')

        # Justificación:
        # Usamos RMSE porque penaliza más fuertemente los errores grandes, lo cual es útil en series financieras
        # donde un error de 100 puede ser mucho peor que 10 errores de 10.

        # Guarda el modelo
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)

        print(f"Modelo guardado en {self.model_path}")

    def predecir(self, nuevos_datos: pd.DataFrame):
        # Carga el modelo entrenado
        with open(self.model_path, 'rb') as f:
            modelo = pickle.load(f)

        # Asegúrate de que los datos tengan las mismas columnas que en entrenamiento
        columnas = ['abrir', 'max', 'min', 'volumen', 'media_movil_7d',
                    'tasa_variacion', 'retorno_acumulado', 'std_5d', 'volatilidad']
        predicciones = modelo.predict(nuevos_datos[columnas])
        return predicciones


# Solo para prueba rápida desde consola
if __name__ == '__main__':
    modelo = Modelador()
    modelo.entrenar()
