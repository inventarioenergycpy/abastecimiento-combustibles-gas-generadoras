"""
Calculadora de Costos Logisticos de Combustibles y Gas Natural en Argentina
Proyecto: Abastecimiento y Brokerage de Combustibles y Gas para Generadoras
Holding: Energy CPY / inventarioenergycpy
"""

import json
from pathlib import Path

def load_data():
    base_dir = Path(__file__).resolve().parent.parent / "data"
    with open(base_dir / "precios_combustibles_benchmark.json", "r", encoding="utf-8") as f:
        precios = json.load(f)
    with open(base_dir / "matriz_logistica_transporte.json", "r", encoding="utf-8") as f:
        logistica = json.load(f)
    with open(base_dir / "directorio_generadoras_argentina.json", "r", encoding="utf-8") as f:
        generadoras = json.load(f)
    return precios, logistica, generadoras

def evaluar_costo_puesto_en_planta_liquidos(precios, logistica):
    """
    Compara para cada destino relevante:
    Opcion A: Compra en Refineria Local + Flete Camion Cisterna
    Opcion B: Importacion CIF Puerto (Dock Sud/Campana/San Nicolas) + Costos Portuarios + Flete Camion
    """
    costo_ref_gasoil = precios["precios_combustibles_liquidos"]["gasoil_grado_2_industrial"]["precio_refineria_local_usd_m3"]
    costo_cif_gasoil = precios["precios_combustibles_liquidos"]["gasoil_grado_2_industrial"]["precio_cif_importacion_puerto_usd_m3"]
    
    costo_ref_fueloil = precios["precios_combustibles_liquidos"]["fuel_oil_n6_bajo_azufre"]["precio_refineria_local_usd_ton"]
    costo_cif_fueloil = precios["precios_combustibles_liquidos"]["fuel_oil_n6_bajo_azufre"]["precio_cif_importacion_puerto_usd_ton"]
    
    # Costos portuarios promedio de internacion en USD/m3 para Gasoil y USD/ton para Fuel Oil
    # Almacenamiento 1 mes (USD 6.20) + Tasa despacho (USD 2.80) + Peaje hidrovía y praticaje (~USD 4.50)
    costo_portuario_gasoil_usd_m3 = 6.20 + 2.80 + 4.50 # USD 13.50/m3
    costo_portuario_fueloil_usd_ton = 7.00 + 3.20 + 5.00 # USD 15.20/ton
    
    destinos = logistica["logistica_interna_flete_carretero"]["distancias_y_costos_testigo"]
    
    comparativa = []
    for d in destinos:
        dist_km = d["distancia_km"]
        flete_gasoil_m3 = d["costo_flete_usd_m3"]
        flete_fueloil_ton = d["costo_flete_usd_ton_fueloil"]
        
        # Opcion Local
        puesto_local_gasoil = costo_ref_gasoil + flete_gasoil_m3
        puesto_local_fueloil = costo_ref_fueloil + flete_fueloil_ton
        
        # Opcion Importada
        puesto_import_gasoil = costo_cif_gasoil + costo_portuario_gasoil_usd_m3 + flete_gasoil_m3
        puesto_import_fueloil = costo_cif_fueloil + costo_portuario_fueloil_usd_ton + flete_fueloil_ton
        
        spread_gasoil = puesto_local_gasoil - puesto_import_gasoil
        spread_fueloil = puesto_local_fueloil - puesto_import_fueloil
        
        comparativa.append({
            "destino": d["destino"],
            "distancia_km": dist_km,
            "gasoil_local_usd_m3": round(puesto_local_gasoil, 2),
            "gasoil_importado_usd_m3": round(puesto_import_gasoil, 2),
            "ventaja_importacion_gasoil_usd_m3": round(spread_gasoil, 2),
            "fueloil_local_usd_ton": round(puesto_local_fueloil, 2),
            "fueloil_importado_usd_ton": round(puesto_import_fueloil, 2),
            "ventaja_importacion_fueloil_usd_ton": round(spread_fueloil, 2),
            "estrategia_optima": "Importacion Directa Portuaria" if spread_gasoil > 20 else "Negociacion Refineria Local con Descuento"
        })
        
    return comparativa

def main():
    precios, logistica, generadoras = load_data()
    comp = evaluar_costo_puesto_en_planta_liquidos(precios, logistica)
    
    print("=" * 90)
    print("COMPARATIVA DE LOGISTICA Y COSTO PUESTO EN PLANTA: LOCAL VS. IMPORTADO")
    print("=" * 90)
    for c in comp:
        print(f"\nDestino: {c['destino']} ({c['distancia_km']} km de puerto/terminal)")
        print(f"  • Gasoil Grado 2:")
        print(f"    - Compra Refineria Local + Flete:  USD {c['gasoil_local_usd_m3']}/m3")
        print(f"    - Importacion CIF + Terminal + Fl: USD {c['gasoil_importado_usd_m3']}/m3")
        print(f"    - Ahorro Importacion:              USD {c['ventaja_importacion_gasoil_usd_m3']}/m3")
        print(f"  • Fuel Oil N6:")
        print(f"    - Compra Refineria Local + Flete:  USD {c['fueloil_local_usd_ton']}/ton")
        print(f"    - Importacion CIF + Terminal + Fl: USD {c['fueloil_importado_usd_ton']}/ton")
        print(f"    - Ahorro Importacion:              USD {c['ventaja_importacion_fueloil_usd_ton']}/ton")
        print(f"  ==> Estrategia Recomendada: {c['estrategia_optima']}")

if __name__ == "__main__":
    main()
