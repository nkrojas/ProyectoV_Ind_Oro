# ProyectoV_Ind_Oro
Autores:
Katherine rojas
 Hugo A. Carvajal


  Análisis y Predicción del Precio del Oro
Este proyecto tiene como objetivo analizar series temporales del precio del oro e implementar un modelo de predicción usando scikit-learn, junto con una visualización interactiva de KPIs financieros mediante Streamlit.



├── docs/                               # Documentacion.
│   └── entrega1.pdf
├── src/
    ├── data/                           # Datos originales del oro (CSV descargado)
│   └── Oro_datosOriginales_enricher.csv
│   ├── collector.py                    # Carga datos desde CSV local
│   ├── enricher.py                     # Calcula variables técnicas y KPIs
│   ├── modeller.py                     # Entrenamiento y predicción con RandomForest
│   ├── dashboard.py                    # Interfaz Streamlit con KPIs y predicciones
│   └── workflows/                      # (Opcional) flujos automatizados
├── static/models/
│   └── model.pkl                       # Modelo entrenado
├── requirements.txt                    # Dependencias del proyecto
└── README.md                           # Documentación general




Clonar el repositorio desde https://github.com/nkrojas/ProyectoV_Ind_Oro.git


Ejecutar  pasos
paso1 - Crear entorno virtual
         python -m venv venv
paso2 - Activar entorno virtual
        ./venv/Scripts/activate
paso3 - Actualizar pip
        pip install --upgrade pip
paso4 - instalar dependencias
        pip install -e .
paso5 - Ejecutar Script
        python src/PIV_Oro/static/ejecucion.py


requeriments.txt
pandas>=1.5.0
numpy>=1.22.0
scikit-learn>=1.2.0
joblib>=1.2.0
streamlit>=1.20.0
matplotlib>=3.6.0
plotly>=5.11.0
openpyxl>=3.1.0



         Referencias útiles
 Yahoo Finance

 Documentación oficial de Python

scikit-learn: Machine Learning
 statsmodels: Series temporales
 GitHub Docs
 GitHub Action