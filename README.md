# ⚡ Abastecimiento Estratégico y Brokerage de Gas Natural y Combustibles para Generadoras en el MEM

> **Plataforma de Inteligencia de Mercado, Brokerage y Suministro de Gas Natural y Combustibles Líquidos para Centrales Térmicas en Argentina**  
> *Encuadrado en el Decreto PEN N.º 450/2025, la Resolución SE N.º 400/2025 y la Normalización del Mercado Eléctrico Mayorista (MEM).*

[![GitHub](https://img.shields.io/badge/GitHub-inventarioenergycpy-blue.svg)](https://github.com/inventarioenergycpy/abastecimiento-combustibles-gas-generadoras)
[![License](https://img.shields.io/badge/License-Proprietary-darkred.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-brightgreen.svg)]()
[![Market](https://img.shields.io/badge/MEM-CAMMESA-orange.svg)]()

---

## 📌 1. Visión General y Oportunidad de Negocio

A partir de la promulgación del **Decreto PEN N.º 450/2025** y la publicación de la **Resolución SE N.º 400/2025** de la Secretaría de Energía, el sistema eléctrico argentino inició un proceso histórico de desregulación y transición de 24 meses:
- **CAMMESA cesa paulatinamente su rol de compradora centralizada de combustibles** para las usinas generadoras, retornando estrictamente a su rol de Organismo Encargado del Despacho (OED).
- **Las empresas generadoras térmicas privadas deben asumir el aprovisionamiento directo** de su Gas Natural, Gasoil Grado 2/3 y Fuel Oil N.º 6.
- Aquellas centrales que logran reducir sus costos unitarios de combustible mejoran su **Costo Variable de Producción (CVP)**, ganando prioridad en el **despacho por orden de mérito de CAMMESA** y reteniendo el 100% del margen de ahorro generado.

**Energy CPY** estructura un servicio integral de **Brokerage, Agregación de Demanda y Optimización de Suministro**, conectando a las principales generadoras térmicas independientes del país con los productores de cuenca (Vaca Muerta / Austral) y los principales importadores portuarios de combustibles líquidos.

---

## 📊 2. Hallazgos Clave del Estudio de Mercado

- **Pool Total de Ahorro Detectado**: **USD 171.905.433 / año** para el conjunto de centrales analizadas.
- **Potencial de Honorarios para Energy CPY (Shared Savings 10%)**: **USD 17.190.543 / año**.
- **Ventaja de Importación Directa en Puerto para Líquidos**:
  - **Gasoil Grado 2 Industrial**: Ahorro neto en terminal de **USD 66,50 / m³** (-8,4%) frente a precio de refinería local.
  - **Fuel Oil N.º 6 Bajo Azufre**: Ahorro neto en terminal de **USD 29,80 / Ton** (-5,7%) frente a refinería local.
- **Gas Natural en PIST (Cuenca Neuquina)**:
  - Verano: **USD 2,15 – 2,40 / MMBtu** | Invierno: **USD 3,50 – 4,20 / MMBtu**.
  - Ahorro por contratación agregada de gas firme: **USD 0,15 a USD 0,45 / MMBtu**.

---

## 🗺️ 3. Directorio de Generadoras y Clientes Target

El relevamiento clasifica a los principales 9 grupos generadores térmicos de Argentina (más de 14.700 MW):

| Grupo Generador | Potencia (MW) | Estatus Plan Gas | Prioridad Comercial | Ahorro Potencial Estimado |
| :--- | :---: | :--- | :---: | :---: |
| **MSU Energy S.A.** | 750 MW | **SIN Plan Gas Propio** (100% expuesto a mercado) | 🎯 **MÁXIMA (Target 1)** | **USD 8,91 M / año** |
| **Grupo Albanesi** | 1.650 MW | **SIN Plan Gas Integrado** (Comprador spot/MEGSA) | 🎯 **MÁXIMA (Target 2)** | **USD 19,61 M / año** |
| **AES Argentina** | 1.050 MW | **SIN Plan Gas Upstream** (San Nicolás / Sarmiento) | 🚀 **ALTA (Target 3)** | **USD 12,48 M / año** |
| **EPEC Córdoba** | 580 MW | **SIN Plan Gas Propio** (Pilar Bicentenario) | ⚡ **ALTA (Ecosistema)** | **USD 6,89 M / año** |
| **Genneia Térmica** | 280 MW | **SIN Plan Gas Propio** (Usinas de punta) | 📈 **ALTA (Nicho Margen)** | **USD 3,32 M / año** |
| **Central Puerto S.A.** | 4.350 MW | Mixta (Demanda masiva spot y líquidos en Costanera) | 🏆 **ESTRATÉGICA (Volumen)**| **USD 51,71 M / año** |
| **Pampa Energía** | 2.400 MW | Productor Integrado (Foco en Fuel Oil Piedra Buena) | 🤝 **Medio / Alianza** | **USD 28,53 M / año** |
| **YPF Luz** | 2.500 MW | Productor Integrado (Foco en swaps de transporte) | 🤝 **Baja / Swaps** | **USD 29,72 M / año** |
| **Central Dock Sud** | 900 MW | Contratos Plan Gas indirectos | 📊 **Media (Respaldo)** | **USD 10,69 M / año** |

---

## 📁 4. Estructura del Repositorio

```text
abastecimiento-combustibles-gas-generadoras/
├── README.md                                   # Presentación ejecutiva del proyecto
├── data/
│   ├── precios_combustibles_benchmark.json     # Precios PIST, GNL, Gasoil, Fuel Oil y heat-rates
│   ├── matriz_logistica_transporte.json        # Gasoductos (TGS/TGN/GPNK), peajes, fletes y puertos
│   ├── directorio_generadoras_argentina.json   # Censo detallado de 9 grupos y 25+ centrales térmicas
│   ├── registro_licitaciones_oferentes.json    # Historial de licitaciones y catálogo de oferentes
│   └── listado_generadoras_clasificado.csv     # Exportación tabular procesable en Excel/Power BI
├── scripts/
│   ├── analisis_mercado_precios.py             # Motor cuantitativo de costos variables y ahorros
│   ├── calculadora_logistica_flete.py          # Comparativa local vs. importado puesto en planta
│   └── generador_informe_mercado.py            # Generador y exportador tabular a CSV
└── docs/
    ├── 01-Estudio-Mercado-Precios-Combustibles.md
    ├── 02-Analisis-Logistica-Interna-Importacion.md
    ├── 03-Listado-Generadoras-PlanGas-Potenciales-Clientes.md
    └── 04-Marco-Regulatorio-Decreto450-Res400-Oportunidad-Brokerage.md
```

---

## 🚀 5. Instrucciones de Ejecución

Para reproducir los modelos y cálculos deterministas en un entorno con Python 3.10+:

```bash
# Navegar a la carpeta del proyecto
cd E:\Proyectos\abastecimiento-combustibles-gas-generadoras

# Ejecutar el análisis cuantitativo de costos variables y ahorros
python scripts/analisis_mercado_precios.py

# Ejecutar la calculadora logística (local vs. importado puerto)
python scripts/calculadora_logistica_flete.py

# Exportar el listado clasificado a CSV
python scripts/generador_informe_mercado.py
```

---

## ⚖️ 6. Blindaje Legal y Contratación en 3 Capas
Energy CPY opera como intermediario comercial y agente de estructuración bajo los **Artículos 1345 a 1355 del Código Civil y Comercial de la Nación (Contrato de Corretaje)**:
1. **Capa 1**: Acuerdo de Confidencialidad y No Elusión (**NCNDA**).
2. **Capa 2**: Contrato de Corretaje y Mandato Comercial con cláusula de éxito (**Shared Savings: 8% – 12%** o comisión fija por MMBtu).
3. **Capa 3**: Contrato Principal de Suministro celebrado directamente entre el Productor Petrolero / Trader y la Generadora Térmica.

---

**Contacto & Dirección Comercial**: `inventario.energycpy@gmail.com`  
**Organización**: [Energy CPY (inventarioenergycpy)](https://github.com/inventarioenergycpy)
