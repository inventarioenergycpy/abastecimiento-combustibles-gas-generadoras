"""
Script de Analisis Cuantitativo de Precios y Costos de Generacion Termica en el MEM
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

def calcular_costo_generacion_variable(precios, logistica):
    """
    Calcula el Costo Variable de Produccion (USD/MWh) para distintas tecnologias
    segun el combustible utilizado y el costo de transporte.
    Formula: CVP (USD/MWh) = Heat Rate (MMBtu/MWh) * Costo Combustible Puesto en Planta (USD/MMBtu)
    """
    heat_rates = precios["rendimiento_termico_heat_rate"]
    
    # Costos de combustible puesto en planta (promedio anual)
    # Gas Neuquino puesto en GBA: PIST USD 2.83 + Peaje TGS USD 0.72 = USD 3.55/MMBtu
    costo_gas_puesto_gba = precios["precios_gas_natural_pist"]["cuenca_neuquina"]["promedio_anual_ponderado_usd_MMBtu"] + 0.72
    # Gas puesto en Interior (Cordoba/Santa Fe via TGN): PIST USD 2.83 + Peaje TGN USD 0.94 = USD 3.77/MMBtu
    costo_gas_puesto_interior = precios["precios_gas_natural_pist"]["cuenca_neuquina"]["promedio_anual_ponderado_usd_MMBtu"] + 0.94
    # GNL Escobar puesto en red: USD 9.20 + USD 0.50 transporte = USD 9.70/MMBtu
    costo_gnl_puesto = precios["precios_gnl_importado"]["terminal_escobar"]["precio_total_cif_regasificado_usd_MMBtu"] + 0.50
    # Gasoil puesto en planta (USD/MMBtu) = USD 22.07 + Flete (USD 1.00/MMBtu) = USD 23.07/MMBtu
    costo_gasoil_puesto = precios["precios_combustibles_liquidos"]["gasoil_grado_2_industrial"]["equivalente_usd_MMBtu"] + 1.00
    # Fuel Oil puesto en planta (USD/MMBtu) = USD 13.37 + Flete (USD 0.80/MMBtu) = USD 14.17/MMBtu
    costo_fueloil_puesto = precios["precios_combustibles_liquidos"]["fuel_oil_n6_bajo_azufre"]["equivalente_usd_MMBtu"] + 0.80

    resultados = {}
    for tec, data in heat_rates.items():
        hr = data["heat_rate_MMBtu_MWh"]
        resultados[tec] = {
            "heat_rate_MMBtu_MWh": hr,
            "rendimiento_pct": data["rendimiento_porcentual"],
            "cvp_gas_natural_gba_usd_MWh": round(hr * costo_gas_puesto_gba, 2),
            "cvp_gas_natural_interior_usd_MWh": round(hr * costo_gas_puesto_interior, 2),
            "cvp_gnl_invierno_usd_MWh": round(hr * costo_gnl_puesto, 2),
            "cvp_gasoil_respaldo_usd_MWh": round(hr * costo_gasoil_puesto, 2),
            "cvp_fueloil_respaldo_usd_MWh": round(hr * costo_fueloil_puesto, 2)
        }
    return resultados

def estimar_ahorros_potenciales_por_grupo(generadoras, precios):
    """
    Estima el volumen anual de consumo y el ahorro economico potencial que Energy CPY
    puede generar al conseguir un spread de descuento promedio de:
    - Gas Natural: USD 0.25 / MMBtu
    - Gasoil: USD 45.0 / m3
    - Fuel Oil: USD 35.0 / ton
    """
    ahorro_gas_usd_mmbtu = 0.25
    ahorro_gasoil_usd_m3 = 45.0
    ahorro_fueloil_usd_ton = 35.0
    
    resumen_grupos = []
    
    for grupo in generadoras["grupos_generadores"]:
        nombre_grupo = grupo["grupo"]
        mw_total = grupo["capacidad_total_termica_MW"]
        prioridad = grupo["prioridad_comercial_brokerage"]
        plan_gas = grupo["participacion_plan_gas"]
        
        # Estimacion de consumo anual asumiendo factor de capacidad medio del 55%
        # Generacion anual estimada = MW * 8760 horas * 0.55
        gen_mwh_anual = mw_total * 8760 * 0.55
        
        # MMBtu de gas requeridos (asumiendo 6.5 MMBtu/MWh promedio de parque)
        mmbtu_gas_anual = gen_mwh_anual * 6.5 * 0.85 # 85% a gas
        # 15% restante operado a liquidos en invierno o picos
        mmbtu_liquidos_anual = gen_mwh_anual * 6.5 * 0.15
        
        m3_gasoil_anual = (mmbtu_liquidos_anual * 0.6) / 35.8
        ton_fueloil_anual = (mmbtu_liquidos_anual * 0.4) / 38.9
        
        # Ahorros potenciales
        ahorro_gas_usd = mmbtu_gas_anual * ahorro_gas_usd_mmbtu
        ahorro_gasoil_usd = m3_gasoil_anual * ahorro_gasoil_usd_m3
        ahorro_fueloil_usd = ton_fueloil_anual * ahorro_fueloil_usd_ton
        ahorro_total_usd = ahorro_gas_usd + ahorro_gasoil_usd + ahorro_fueloil_usd
        
        resumen_grupos.append({
            "grupo": nombre_grupo,
            "potencia_termica_MW": mw_total,
            "estatus_plan_gas": plan_gas,
            "prioridad_comercial": prioridad,
            "consumo_gas_estimado_MMBtu_ano": round(mmbtu_gas_anual, 0),
            "consumo_gasoil_estimado_m3_ano": round(m3_gasoil_anual, 0),
            "consumo_fueloil_estimado_ton_ano": round(ton_fueloil_anual, 0),
            "ahorro_potencial_gas_USD_ano": round(ahorro_gas_usd, 0),
            "ahorro_potencial_liquidos_USD_ano": round(ahorro_gasoil_usd + ahorro_fueloil_usd, 0),
            "ahorro_total_anual_USD": round(ahorro_total_usd, 0)
        })
        
    return resumen_grupos

def main():
    precios, logistica, generadoras = load_data()
    cvp = calcular_costo_generacion_variable(precios, logistica)
    ahorros = estimar_ahorros_potenciales_por_grupo(generadoras, precios)
    
    print("=" * 80)
    print("ANALISIS CUANTITATIVO DE COSTOS VARIABLES DE GENERACION (USD/MWh)")
    print("=" * 80)
    for tec, data in cvp.items():
        print(f"\nTecnologia: {tec.upper()} (Rendimiento: {data['rendimiento_pct']}%)")
        print(f"  • CVP Gas Natural (Nodo GBA):     USD {data['cvp_gas_natural_gba_usd_MWh']}/MWh")
        print(f"  • CVP Gas Natural (Nodo Interior):USD {data['cvp_gas_natural_interior_usd_MWh']}/MWh")
        print(f"  • CVP GNL Escobar (Invierno):     USD {data['cvp_gnl_invierno_usd_MWh']}/MWh")
        print(f"  • CVP Fuel Oil N6 (Respaldo):     USD {data['cvp_fueloil_respaldo_usd_MWh']}/MWh")
        print(f"  • CVP Gasoil Grado 2 (Punta):     USD {data['cvp_gasoil_respaldo_usd_MWh']}/MWh")
        
    print("\n" + "=" * 80)
    print("POTENCIAL DE AHORRO ECONOMICO POR GRUPO GENERADOR (USD/ANO)")
    print("=" * 80)
    total_ahorro_mercado = 0
    for g in ahorros:
        print(f"\nGrupo: {g['grupo']} ({g['potencia_termica_MW']} MW) - Prioridad: {g['prioridad_comercial']}")
        print(f"  - Estatus Plan Gas: {g['estatus_plan_gas']}")
        print(f"  - Ahorro Potencial en Gas:      USD {g['ahorro_potencial_gas_USD_ano']:,.0f} / ano")
        print(f"  - Ahorro Potencial en Liquidos: USD {g['ahorro_potencial_liquidos_USD_ano']:,.0f} / ano")
        print(f"  - AHORRO TOTAL COMBINADO:       USD {g['ahorro_total_anual_USD']:,.0f} / ano")
        total_ahorro_mercado += g['ahorro_total_anual_USD']
        
    print("\n" + "*" * 80)
    print(f"POOL TOTAL DE AHORRO DE MERCADO DISPONIBLE: USD {total_ahorro_mercado:,.0f} / ano")
    print(f"Potencial de Fee Energy CPY (10% Shared Savings): USD {total_ahorro_mercado * 0.10:,.0f} / ano")
    print("*" * 80)

if __name__ == "__main__":
    main()
