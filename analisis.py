#!/usr/bin/env python3
"""
Script de análisis de datos de sensores industriales.
Lee sensores_industriales.csv y realiza análisis requeridos.
Autor: Daniel Efrén Malagón De Santiago
Fecha: 2026-10-05
"""

import pandas as pd
import os
from pathlib import Path

def main():
    # Configurar rutas relativas
    data_dir = Path("data")
    results_dir = Path("resultados")

    # Crear directorio de resultados si no existe
    results_dir.mkdir(exist_ok=True)

    # Leer el CSV
    csv_path = data_dir / "sensores_industriales.csv"

    if not csv_path.exists():
        print(f"❌ Error: No se encontró {csv_path}")
        return

    print(f"📂 Leyendo datos desde: {csv_path}")
    df = pd.read_csv(csv_path)

    # ==================== ANÁLISIS ====================
    print("\n" + "="*60)
    print("ANÁLISIS DE SENSORES INDUSTRIALES")
    print("="*60)

    # 1. Cantidad de registros y sensores distintos
    num_registros = len(df)
    num_sensores = df['id_sensor'].nunique()
    print(f"\n1️⃣  CANTIDAD DE REGISTROS Y SENSORES:")
    print(f"   • Total de registros: {num_registros:,}")
    print(f"   • Cantidad de sensores distintos: {num_sensores}")

    # 2. Temperatura promedio de cada planta
    temp_promedio_planta = df.groupby('planta')['temperatura_c'].mean()
    print(f"\n2️⃣  TEMPERATURA PROMEDIO POR PLANTA:")
    for planta, temp in temp_promedio_planta.items():
        print(f"   • Planta {planta}: {temp:.2f}°C")

    # 3. Temperatura máxima e identificar sensor y fecha
    temp_max_idx = df['temperatura_c'].idxmax()
    temp_max = df.loc[temp_max_idx]
    print(f"\n3️⃣  TEMPERATURA MÁXIMA:")
    print(f"   • Valor: {temp_max['temperatura_c']}°C")
    print(f"   • Sensor: {temp_max['id_sensor']}")
    print(f"   • Fecha/Hora: {temp_max['fecha_hora']}")
    print(f"   • Planta: {temp_max['planta']}")

    # 4. Contar lecturas con temperatura > 85°C
    umbral = 85
    alertas = df[df['temperatura_c'] > umbral]
    num_alertas = len(alertas)
    print(f"\n4️⃣  LECTURAS CON ALERTA (Temperatura > {umbral}°C):")
    print(f"   • Total de alertas: {num_alertas}")

    # 5. Planta con más alertas
    alertas_por_planta = alertas['planta'].value_counts()
    if not alertas_por_planta.empty:
        max_alertas = alertas_por_planta.max()
        plantas_max = alertas_por_planta[alertas_por_planta == max_alertas].index.tolist()
        print(f"\n5️⃣  PLANTA(S) CON MÁS ALERTAS:")
        for planta in plantas_max:
            print(f"   • Planta {planta}: {max_alertas} alertas")
    else:
        print(f"\n5️⃣  PLANTA(S) CON MÁS ALERTAS:")
        print(f"   • No hay alertas registradas")

    # 6. Exportar alertas a CSV
    alertas_path = results_dir / "alertas.csv"
    alertas.to_csv(alertas_path, index=False)
    print(f"\n6️⃣  ALERTAS EXPORTADAS:")
    print(f"   • Archivo: {alertas_path}")
    print(f"   • Total de registros exportados: {len(alertas)}")

    print("\n" + "="*60)
    print("✅ Análisis completado exitosamente")
    print("="*60 + "\n")

    # Resumen para el informe
    print("\nRESUMEN DE DATOS PARA EL INFORME:")
    print(f"- Total de registros: {num_registros:,}")
    print(f"- Cantidad de sensores: {num_sensores}")
    print(f"- Temperatura máxima: {temp_max['temperatura_c']}°C")
    print(f"- Temperaturas promedio por planta:")
    for planta, temp in temp_promedio_planta.items():
        print(f"  - Planta {planta}: {temp:.2f}°C")
    print(f"- Total de alertas (>85°C): {num_alertas}")

if __name__ == "__main__":
    main()
