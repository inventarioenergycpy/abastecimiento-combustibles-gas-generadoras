"""
Generador de Informes Consolidados y Exportacion Tabular
Proyecto: Abastecimiento y Brokerage de Combustibles y Gas para Generadoras
Holding: Energy CPY / inventarioenergycpy
"""

import json
import csv
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    
    with open(data_dir / "directorio_generadoras_argentina.json", "r", encoding="utf-8") as f:
        directorio = json.load(f)
        
    csv_path = data_dir / "listado_generadoras_clasificado.csv"
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Grupo Generador",
            "Central Termica",
            "Ubicacion",
            "Capacidad MW",
            "Tecnologia",
            "Combustibles",
            "Estatus Plan Gas",
            "Prioridad Brokerage Energy CPY",
            "Consumo Gas Pico (dam3/dia)",
            "Situacion Combustible y Oportunidad"
        ])
        
        for g in directorio["grupos_generadores"]:
            grupo = g["grupo"]
            plan_gas = g["participacion_plan_gas"]
            prioridad = g["prioridad_comercial_brokerage"]
            
            for c in g["centrales"]:
                writer.writerow([
                    grupo,
                    c["nombre"],
                    c["ubicacion"],
                    c["capacidad_MW"],
                    c["tecnologia"],
                    " / ".join(c["combustibles"]),
                    plan_gas,
                    prioridad,
                    c["consumo_gas_pico_dam3_dia"],
                    c["situacion_combustible"]
                ])
                
    print(f"Archivo CSV consolidado exportado exitosamente en: {csv_path}")

if __name__ == "__main__":
    main()
