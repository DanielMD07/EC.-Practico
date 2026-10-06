# Análisis de Sensores Industriales - Examen Manejo Masivo de Datos

## Objetivo

Este proyecto analiza datos de sensores industriales de 4 plantas para detectar anomalías de temperatura y vibración. El análisis procesa 100,000 mediciones simuladas, identifica alertas cuando la temperatura excede 85°C y genera reportes.

## Descripción de Datos

El archivo `sensores_industriales.csv` contiene:

| Columna | Descripción |
|---------|------------|
| `id_registro` | Identificador único de cada medición |
| `fecha_hora` | Marca de tiempo de la lectura |
| `id_sensor` | Identificador del sensor que tomó la medición |
| `planta` | Planta industrial donde está instalado el sensor |
| `temperatura_c` | Temperatura en grados Celsius |
| `vibracion_mm_s` | Vibración en milímetros por segundo |

**Nota:** Los datos en este archivo son **completamente simulados** para fines didácticos del examen.

## Instalación y Ejecución

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos para instalar y ejecutar

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd manejo-datos-sensor
   ```

2. **Crear entorno virtual:**
   ```bash
   # En Windows:
   python -m venv .venv
   .venv\Scripts\activate

   # En macOS/Linux:
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el análisis:**
   ```bash
   python analisis.py
   ```

### Salida esperada

El programa mostrará en consola:
- Total de registros y sensores distintos
- Temperatura promedio por planta
- Temperatura máxima con detalles del sensor
- Cantidad de alertas (temp > 85°C)
- Planta(s) con más alertas

Además, creará un archivo `resultados/alertas.csv` con todas las mediciones que superaron el umbral.

## Estructura del Proyecto

```
manejo-datos-sensor/
├── data/
│   └── sensores_industriales.csv    # Datos de entrada
├── resultados/
│   └── alertas.csv                  # Salida: mediciones con alerta
├── evidencias/
│   └── reproducibilidad.png         # Captura de ejecución en clon
├── analisis.py                      # Script principal
├── informe.md                       # Informe de Big Data
├── README.md                        # Este archivo
├── requirements.txt                 # Dependencias
├── .gitignore                       # Archivos ignorados por Git
└── .git/                            # Repositorio Git
```

## Dependencias

El proyecto usa solo la librería **pandas**. Consulta `requirements.txt` para versiones específicas.

Si deseas ejecutar sin instalar dependencias externas, es posible usar solo la librería estándar de Python, aunque con rendimiento reducido para 100,000 registros.

## Características del Análisis

✅ Lectura de archivos CSV con rutas relativas  
✅ Cálculo de estadísticas descriptivas  
✅ Identificación de anomalías (alertas de temperatura)  
✅ Exportación de resultados en formato CSV  
✅ Código documentado y reproducible  

## Reproducibilidad

Este proyecto fue diseñado para ser completamente reproducible:

1. Todas las rutas son relativas (independientes de directorios)
2. Las dependencias están especificadas en `requirements.txt`
3. El script lee datos desde archivos, no de código compilado
4. La ejecución es determinista (sin componentes aleatorios)

Para verificar: clona el repositorio en otra carpeta, crea un nuevo entorno virtual y ejecuta según los pasos anteriores.

## Autor

**Daniel Efrén Malagón De Santiago**  
Matrícula: 125052501  
Grupo: IDIA 222  
Universidad Politécnica de Querétaro (UPQ)

**Docente:** Javier Moya  
**Materia:** Manejo Masivo de Datos  
**Fecha:** Octubre 2026

---

*Proyecto desarrollado como parte del primer parcial del curso de Manejo Masivo de Datos.*
