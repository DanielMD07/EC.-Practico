# Informe: Aplicación de Fundamentos de Big Data
## Análisis de Sensores Industriales

**Autor:** Daniel Efrén Malagón De Santiago  
**Matrícula:** 125052501  
**Grupo:** IDIA 222  
**Fecha:** Octubre 2026  
**Docente:** Javier Moya

---

## 5. Las 5 V Aplicadas al Proyecto de Sensores Industriales

| V | Descripción | Ejemplo Concreto | Presente en CSV | Futura Ampliación |
|---|-------------|------------------|-----------------|-------------------|
| **Volumen** | Cantidad masiva de datos generados | 100,000 mediciones de sensores; si se ampliara a 1,000 sensores con mediciones cada segundo = 86.4 millones de registros diarios | ✅ CSV actual tiene 100K registros | ✅ Ampliación: miles de sensores x segundos = gigabytes/día, terabytes al año |
| **Velocidad** | Rapidez con la que se generan y procesan los datos | Actualmente: 1 medición/minuto/sensor. Futura: 1 medición/segundo = 40 sensores x 86,400 segundos = 3.4M registros/día | ⚠️ Procesamiento batch (lento) | ✅ Necesitará procesamiento en tiempo real (streaming) |
| **Variedad** | Tipos y formatos distintos de datos | CSV estructurado actual; futuro: JSON de sensores, fotografías de máquinas (imágenes), reportes de mantenimiento (texto libre), videos de camaras de vigilancia | ✅ Estructurado (CSV) | ✅ Semiestructurado (JSON), No estructurado (fotos, reportes) |
| **Veracidad** | Calidad, confiabilidad e integridad de los datos | Datos simulados; en producción: sensor con calibración desajustada reportando temp. 150°C cuando es 75°C, lecturas perdidas por desconexión temporal | ✅ Datos simulados y confiables | ❓ Requiere validación en tiempo real |
| **Valor** | Beneficio económico y decisiones estratégicas que se pueden tomar | Detectar anomalías de temperatura (umbral 85°C) previene paros de máquinas; identificar planta con más alertas para mantenimiento preventivo; historial de fallos permite predicción | ✅ Alertas en análisis CSV | ✅ Predicción de fallas, optimización de mantenimiento |

---

## 6. Tipos de Datos y Procesamiento Tradicional

### Clasificación de Elementos

1. **El CSV de sensores (`sensores_industriales.csv`)**
   - **Tipo:** Estructurado
   - **Justificación:** Datos organizados en filas y columnas con esquema definido (id_registro, fecha_hora, id_sensor, planta, temperatura_c, vibracion_mm_s). Cada campo tiene tipo y posición conocida. Fácilmente indexable en SQL.

2. **Un mensaje JSON enviado por un sensor**
   - **Tipo:** Semiestructurado
   - **Justificación:** Tiene estructura (clave-valor), pero puede variar según sensor o versión de API. Ejemplo:
     ```json
     {"id":"S001", "ts":"2026-09-01T00:00:00Z", "temp":97.65, "vib":5.45, "status":"OK"}
     ```
     Nuevo campo `status` podría no existir en otro sensor.

3. **Una fotografía de una máquina**
   - **Tipo:** No estructurado
   - **Justificación:** Archivo binario (JPG/PNG). No tiene esquema ni relación entre píxeles. Requiere procesamiento especial (visión computacional) para extraer información.

4. **El texto libre de un reporte de mantenimiento**
   - **Tipo:** No estructurado
   - **Justificación:** Texto natural sin formato fijo. Ejemplo: "Se reemplazó rodamiento izquierdo. Vibración bajó de 8mm/s a 2mm/s después de cambio." Requiere procesamiento de lenguaje natural (NLP) para análisis.

### ¿Por qué 100,000 registros NO son Big Data?

**100,000 registros no constituyen Big Data porque:**

- **Volumen:** Es procesable en una sola máquina con Python/pandas en memoria (< 10 MB). Big Data típicamente comienza en gigabytes/terabytes.
- **Procesamiento:** Tarda segundos-minutos, no horas. No requiere paralelización.
- **Almacenamiento:** Un disco SSD moderno (500GB) guardaba 5 millones de archivos CSV así sin problema.
- **Infraestructura:** No necesita Hadoop, Spark, Kafka, ni clusters distribuidos.

### Limitaciones al Aumentar Escala

Si la empresa ampliara a **1,000 sensores** con **mediciones cada segundo**:

1. **Volumen:** ~86.4 millones registros/día ≈ 4 GB/día en CSV (≈1.5 TB/año) de almacenamiento
2. **Memoria:** Imposible cargar todo en RAM (típica: 16GB)
3. **Procesamiento:** Python secuencial tardaría semanas en analizar un día de datos
4. **I/O:** Leer/escribir disco sería cuello de botella
5. **Consultas:** "¿Qué máquina falló a las 14:32?" necesitaría índices distribuidos (no buscar en 86M registros secuencialmente)
6. **Red:** Transmitir 1.5TB diarios entre sensores → servidor → almacén requiere infraestructura de telecomunicaciones robusta

**Solución:** Pasar a arquitectura Big Data (Hadoop, Spark, Kafka, etc.)

---

## 7. Batch y Streaming

### Tipo de Procesamiento Realizado en `analisis.py`

**Procesamiento: BATCH (Procesamiento por Lotes)**

**Justificación:**
- El archivo `sensores_industriales.csv` ya está completamente guardado
- El script lee el archivo completo en memoria
- Procesa todos los datos de una sola vez
- Genera reportes después de procesar todo
- Tiempo de espera: desde que se dispara hasta completar (segundos-minutos)

**Código evidencia:**
```python
df = pd.read_csv("data/sensores_industriales.csv")  # Lee TODO el archivo
df_alertas = df[df['temperatura_c'] > 85]          # Procesa TODO
df_alertas.to_csv("resultados/alertas.csv")        # Exporta resultado
```

### Enfoque para Alerta Rápida (Tiempo Real)

**Escenario:** Detectar temperatura > 85°C **pocos segundos después** de la medición

**Enfoque: STREAMING (Procesamiento Continuo)**

Arquitectura:
```
Sensor 
  ↓
Kafka (cola de mensajes)
  ↓
Apache Flink / Spark Streaming
  ↓
Regla: IF temp > 85°C THEN ENVIAR ALERTA
  ↓
Sistema de Notificaciones (SMS, Email, Dashboard)
```

**Código conceptual (pseudocódigo):**
```python
# Stream de eventos
for evento in kafka.subscribe("sensores"):
    temp = evento['temperatura_c']
    if temp > 85:
        notificacion.enviar(f"ALERTA: Planta {evento['planta']}, Temp {temp}°C")
        # Latencia: < 1 segundo
```

**Tecnologías:** Kafka, Apache Flink, AWS Kinesis, Azure Stream Analytics

### Enfoque para Resumen Diario

**Escenario:** Generar reporte al **terminar el día** con estadísticas

**Enfoque: BATCH (Procesamiento por Lotes Programado)**

Arquitectura:
```
Datos del día (guardados)
  ↓
Apache Airflow / Cron Job (23:59 cada noche)
  ↓
PySpark / Hive
  ↓
Cálculos: alertas/planta, temp promedio, máximos
  ↓
Email con reporte
```

**Razón:**
- No necesita latencia baja (reportes nocturnos)
- Procesa volúmenes grandes eficientemente con Spark
- Menos costoso que streaming 24/7
- Cálculos complejos (agregaciones múltiples) más fáciles en batch

### Relación Tiempo-Enfoque

| Necesidad | Latencia Requerida | Enfoque | Tecnología |
|-----------|------------------|---------|------------|
| Alerta de anomalía | < 5 segundos | **Streaming** | Kafka + Flink |
| Dashboard en vivo | < 1 minuto | **Micro-batch** (Spark 30s) | Spark Structured Streaming |
| Reporte nocturno | 12-24 horas | **Batch** | Spark SQL, Hive |
| Análisis histórico mensual | N/A (offline) | **Batch** | Python, Spark |

---

## 8. Arquitecturas Lambda y Kappa

### Escenario A: Recalcular Historial + Procesar Reciente Rápidamente

**Enfoque: LAMBDA**

**Justificación:**
- Una ruta "batch" recalcula el historial completo (ayer y años atrás) → reportes precisos
- Una ruta "speed" procesa lo nuevo en tiempo real → alertas inmediatas
- Se combinan al final

**Diagrama:**

```
                    Sistema de Sensores
                            ↓
                    ┌───────┴───────┐
                    ↓               ↓
            [BATCH LAYER]     [SPEED LAYER]
                    ↓               ↓
         Spark SQL historial   Kafka streaming
         (archivos viejos)    (mediciones vivas)
                    ↓               ↓
            Almacén historical  Resultados
            (BD agregada)       en tiempo real
                    ↓               ↓
                    └───────┬───────┘
                            ↓
                    [SERVING LAYER]
                    (Combina ambas
                     para dashboard)
```

**Implementación:**
- **Batch:** Cada noche, recalcula temp promedio de últimos 30 días
- **Speed:** Cada segundo, emite alertas si temp > 85°C
- **Serving:** Dashboard muestra ambas (promedio histórico + alertas vivas)

**Ventaja:** Precisión histórica + Latencia baja actual  
**Desventaja:** Código duplicado en dos lenguajes/sistemas

---

### Escenario B: Una Sola Lógica + Replay de Datos

**Enfoque: KAPPA**

**Justificación:**
- Usa streaming para TODO (batch y tiempo real)
- Si necesita recalcular, "reproduce" el evento histórico en el streaming
- Un solo código, un solo sistema

**Diagrama:**

```
        Sistema de Sensores
                ↓
        Kafka Topic
        (log inmutable)
        ┌───────┬───────┐
        ↓               ↓
    [Nuevo evento]  [Replay histórico]
        ↓               ↓
    Kafka Streams
    (lógica única)
        ↓
    Cálculos (alertas, promedios)
        ↓
    Almacén (actualizaciones)
```

**Implementación:**
```python
# Una sola lógica en Kafka Streams
def procesar_evento(evento):
    temp = evento['temperatura_c']
    almacenar_en_BD(evento)
    if temp > 85:
        generar_alerta(evento)
    actualizar_promedio(evento)

# Para recalcular histórico:
# kafka-console-consumer --from-beginning --topic sensores | procesar_evento
```

**Ventaja:** Código limpio, un solo sistema, fácil auditoría ("qué pasó el 15-ago?")  
**Desventaja:** Más lento que batch para cálculos complejos históricos

---

## 9. Analítica Descriptiva, Predictiva y Prescriptiva

### Analítica Descriptiva: "¿Qué pasó?"

Dos hallazgos REALES del análisis del CSV:

**Hallazgo 1: Alertas distribuidas de forma casi uniforme, con Planta_3 ligeramente arriba**
- Total de alertas (temp > 85°C) en el CSV: **6,954 alertas** de 100,000 registros (6.95%)
- Planta_3: 25.6% de alertas (1,777 registros)
- Planta_1: 25.0% de alertas (1,737 registros)
- Planta_4: 24.9% de alertas (1,732 registros)
- Planta_2: 24.6% de alertas (1,708 registros)
- Sensor con más alertas: **S027 (Planta_3), 211 alertas**

**Conclusión:** Ninguna planta concentra las anomalías de forma desproporcionada; Planta_3 es la que más alertas tiene, pero con una diferencia pequeña (69 alertas más que Planta_2).

**Hallazgo 2: Temperatura máxima registrada**
- Máxima detectada: **104.99°C** (Sensor S023, Planta_3, 01/09/26 22:23)
- Promedio general: 66.65°C (promedios por planta entre 66.53°C y 66.77°C)
- Rango: 45.00–104.99°C (~60°C de amplitud)

**Conclusión:** Las temperaturas promedio son muy similares entre plantas, pero existen picos aislados que superan los 100°C, por lo que conviene vigilar sensores individuales y no solo promedios por planta.

---

### Analítica Predictiva: "¿Qué podría ocurrir?"

**Pregunta:** ¿Qué máquinas en Planta_3 tienen riesgo de falla crítica en las próximas 2 semanas?

**Datos Adicionales Necesarios:**
1. **Historial de fallas:** "Sensor S027 ha fallado 3 veces en 6 meses cuando temp promedio semanal > 90°C"
2. **Mantenimiento preventivo:** "Después de mantenimiento, vibración desciende 40%, durabilidad aumenta 6 meses"
3. **Edad del equipo:** "Sensor S027 tiene 4 años; fabricante garantiza 5 años a temp < 85°C promedio"
4. **Patrón temporal:** "Las máquinas fallan más en lunes (carga de fin de semana sin vigilancia)"
5. **Correlación multivariable:** ¿Temperatura + vibración + humedad simultáneamente altas predicen falla?

**Modelo Predictivo Propuesto:**
```
Riesgo = f(temperatura promedio semanal, vibración_max, edad, freq_alertas_pasadas)
Si Riesgo > 0.8 → Falla esperada en 14 días → Programar mantenimiento
```

---

### Analítica Prescriptiva: "¿Qué debemos hacer?"

**Riesgo Previsto:** Planta_3 tiene el mayor número de alertas (1,777); el sensor S027 acumula 211 alertas y el S023 registró el máximo de 104.99°C

**Acción Propuesta:** Ejecutar mantenimiento preventivo en los sensores S027 y S023 (Planta_3) esta semana

**Información a Revisar Antes de Decidir:**

1. **Costo-Beneficio:**
   - Costo de mantenimiento preventivo: $500
   - Costo de paro por falla: $50,000 (producción perdida en un paro de 12 horas)
   - **Decisión:** Si probabilidad de falla > 2%, vale la pena

2. **Disponibilidad de Recursos:**
   - ¿Técnico disponible esta semana?
   - ¿Pieza de reemplazo en almacén?
   - ¿Puedo parar Planta_3 2 horas sin afectar producción?

3. **Datos de Confiabilidad:**
   - ¿Qué % de sensores con patrón similar a S027 fallaron en 30 días? (Si 0%, es falsa alarma; si 80%, es crítico)
   - ¿Cuántos días más puedo esperar sin riesgo?

4. **Impacto Operacional:**
   - Si no hago mantenimiento: parada emergente a las 3am (peor), falta de personal
   - Si hago mantenimiento HOY: parada planificada con equipo completo (mejor)

**Conclusión de la Prescripción:**
> "**Ejecutar mantenimiento preventivo en los sensores S027 y S023 (Planta_3) mañana a las 14:00.** 
> Razón: Planta_3 tiene más alertas (1,777); S027 acumula 211 alertas y S023 alcanzó 104.99°C. 
> Costo previsto ($500) << Costo de falla ($50,000). 
> Revisar tasa de falla histórica de sensores con patrón similar para validar urgencia."

---

## Conclusión General

Este proyecto demuestra el ciclo completo del análisis de datos masivos:
- **Descriptiva:** Identificar problemas (alertas en Planta_3 y sensores S027 y S023)
- **Predictiva:** Proyectar consecuencias (posible falla en 2 semanas)
- **Prescriptiva:** Recomendar acción (mantenimiento preventivo hoy)

La ampliación a miles de sensores requeriría transición de batch → streaming + arquitecturas Lambda/Kappa para mantener precisión histórica y latencia baja simultáneamente.

---

*Documento completado: 5 de octubre de 2026*
