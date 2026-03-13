"""
PRO-DESG LCA v5.0 — Professional Life Cycle Assessment Platform
Full LCI · Australian NGA · Interactive Wizard · Pedigree Matrix · Custom Data · Light Theme
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json, math
from datetime import datetime
from collections import Counter

st.set_page_config(page_title="PRO-DESG LCA v5.0", page_icon="🔬", layout="wide", initial_sidebar_state="expanded")

# ═══════════════ LIGHT THEME CSS ═══════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
:root{--bg:#f8f9fb;--bg2:#ffffff;--bg3:#f0f2f5;--bg4:#e8ebf0;--border:#d8dde6;--border2:#c5cbd6;
--accent:#0066ff;--accent2:#00b378;--accent3:#e85d04;--accent4:#7c3aed;
--text:#1a1d23;--text2:#4a5568;--text3:#8492a6;--danger:#dc2626;--warn:#d97706;--success:#059669;}
.stApp{background:var(--bg)!important}
section[data-testid="stSidebar"]{background:#ffffff!important;border-right:1px solid #e2e8f0!important}
section[data-testid="stSidebar"] *{color:#4a5568!important}
h1,h2,h3{font-family:'Inter',sans-serif!important;color:#1a1d23!important;font-weight:600!important}
h1{font-size:24px!important}h2{font-size:20px!important}h3{font-size:16px!important}
p,li,span,label,.stMarkdown{color:#4a5568!important;font-family:'Inter',sans-serif!important}
.stSelectbox>div>div,.stTextInput>div>div>input,.stTextArea>div>textarea,.stNumberInput>div>div>input{
background:#ffffff!important;border:1.5px solid #d8dde6!important;color:#1a1d23!important;border-radius:8px!important;font-family:'Inter',sans-serif!important}
.stSelectbox>div>div:focus-within,.stTextInput>div>div>input:focus{border-color:#0066ff!important;box-shadow:0 0 0 3px rgba(0,102,255,0.1)!important}
div[data-testid="stMetricValue"]{color:#0066ff!important;font-family:'JetBrains Mono',monospace!important;font-weight:600!important}
div[data-testid="stMetricLabel"]{color:#8492a6!important;font-family:'JetBrains Mono',monospace!important;text-transform:uppercase!important;font-size:10px!important;letter-spacing:0.5px!important}
div[data-testid="stMetricDelta"]{font-family:'JetBrains Mono',monospace!important}
.stButton>button{border-radius:8px!important;font-family:'Inter',sans-serif!important;font-weight:500!important;border:1.5px solid #d8dde6!important;transition:all 0.15s!important}
.stButton>button:hover{border-color:#0066ff!important;color:#0066ff!important}
.stButton>button[kind="primary"]{background:#0066ff!important;color:white!important;border-color:#0066ff!important}
.stButton>button[kind="primary"]:hover{background:#0052cc!important}
div[data-testid="stExpander"]{border:1.5px solid #e2e8f0!important;border-radius:10px!important;background:#ffffff!important;box-shadow:0 1px 3px rgba(0,0,0,0.04)!important}
div[data-testid="stExpander"] summary{color:#1a1d23!important;font-weight:500!important}
div[data-testid="stExpander"] summary:hover{color:#0066ff!important}
.stTabs [data-baseweb="tab-list"]{gap:0!important;background:#f0f2f5!important;border-radius:10px!important;padding:4px!important}
.stTabs [data-baseweb="tab"]{border-radius:8px!important;font-family:'Inter',sans-serif!important;font-weight:500!important;color:#4a5568!important;font-size:13px!important}
.stTabs [aria-selected="true"]{background:white!important;color:#0066ff!important;box-shadow:0 1px 3px rgba(0,0,0,0.08)!important}
.stDataFrame{border:1.5px solid #e2e8f0!important;border-radius:10px!important}
.tag{display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;font-family:'JetBrains Mono',monospace;font-weight:500;margin:2px}
.tg{background:#ecfdf5;color:#059669}.tb{background:#eff6ff;color:#0066ff}
.to{background:#fff7ed;color:#e85d04}.tp{background:#f5f3ff;color:#7c3aed}
.tgr{background:#f0f2f5;color:#8492a6}.tred{background:#fef2f2;color:#dc2626}
.card{background:white;border:1.5px solid #e2e8f0;border-radius:12px;padding:20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,0.04)}
.card-title{font-family:'JetBrains Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#8492a6;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid #e2e8f0}
.section-hdr{background:#f0f2f5;border:1px solid #e2e8f0;border-radius:6px;padding:8px 12px;margin:10px 0 6px;font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#8492a6}
.info-box{background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:12px 16px;font-size:13px;color:#1e40af;margin-bottom:14px}
.warn-box{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:12px 16px;font-size:13px;color:#92400e;margin-bottom:14px}
.wizard-step{background:white;border:2px solid #e2e8f0;border-radius:12px;padding:24px;margin-bottom:16px;transition:all 0.2s}
.wizard-step.active{border-color:#0066ff;box-shadow:0 0 0 4px rgba(0,102,255,0.08)}
.pfd-node{background:white;border:2px solid #d8dde6;border-radius:10px;padding:14px;display:inline-block;margin:6px;vertical-align:top;min-width:160px;box-shadow:0 2px 4px rgba(0,0,0,0.04)}
.pfd-arrow{color:#8492a6;font-size:24px;display:inline-block;margin:0 4px;vertical-align:middle;padding-top:20px}
.hotspot{background:#fef2f2;border:1.5px solid #fecaca;border-radius:10px;padding:16px;margin-bottom:10px}
.metric-row{display:flex;gap:12px;margin-bottom:16px}
.metric-box{flex:1;background:white;border:1.5px solid #e2e8f0;border-radius:10px;padding:16px;text-align:center}
.metric-box .label{font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;color:#8492a6;margin-bottom:4px}
.metric-box .value{font-size:22px;font-weight:700;font-family:'JetBrains Mono',monospace}
.pedigree-cell{text-align:center;padding:8px;border:1px solid #e2e8f0;font-size:12px}
.pedigree-cell.score5{background:#ecfdf5}.pedigree-cell.score4{background:#f0fdf4}
.pedigree-cell.score3{background:#fefce8}.pedigree-cell.score2{background:#fff7ed}
.pedigree-cell.score1{background:#fef2f2}
</style>""", unsafe_allow_html=True)

# CHARACTERIZATION FACTORS — substance-level (the heart of LCIA)
# ═══════════════════════════════════════════════════════════════
# GWP100 from IPCC AR6 (2021) — kg CO₂-eq per kg substance
CF_GWP = {
    "CO2":1,"CO2_bio":0,"CO2_luc":1,"CH4":29.8,"CH4_bio":27.0,"N2O":273,
    "SF6":25200,"CF4":7380,"C2F6":12400,"HFC134a":1530,"HFC23":14600,
    "HFC32":771,"HFC125":3740,"HFC143a":5810,"HFC152a":164,"NF3":17400,
    "R404A":3922,"R410A":2088,"CO":1.57,"NMVOC":3.4,
}
# AP from CML-IA / ReCiPe — kg SO₂-eq per kg substance
CF_AP = {"SO2":1.0,"NOx":0.36,"NO2":0.36,"NH3":1.96,"HCl":0.88,"HF":1.6,"H2S":1.88}
# EP freshwater — kg P-eq per kg substance
CF_EP = {"PO4":0.33,"P":1.0,"P_water":1.0,"NO3":0.0074,"N_water":0.042,"NH4":0.028,"COD":0.0002}
# EP marine — kg N-eq per kg substance
CF_EP_M = {"NOx":0.039,"NO3":0.226,"N_water":1.0,"NH3":0.092,"NH4":0.078}
# Particulate matter — kg PM2.5-eq
CF_PM = {"PM25":1.0,"PM10":0.6,"SO2":0.061,"NOx":0.0072,"NH3":0.024}
# Photochemical ozone — kg NMVOC-eq
CF_POCP = {"NMVOC":1.0,"NOx":0.29,"CO":0.046,"CH4":0.006,"SO2":0.048}
# Human toxicity cancer — CTUh (simplified)
CF_HTC = {"benzene":1.1e-6,"formaldehyde":2.0e-6,"1,4-DCB":0,"Cd":5.0e-5,"As":1.4e-4,"CrVI":1.6e-3,"Ni":2.7e-6}
# Freshwater ecotox — CTUe
CF_FECT = {"Cu_w":2900,"Zn_w":780,"Pb_w":3600,"Cd_w":57000,"Ni_w":2800,"Hg_w":270000,"As_w":8200}
# Abiotic depletion fossil — MJ per MJ
CF_ADF = {"crude_oil":1.0,"hard_coal":1.0,"brown_coal":1.0,"natural_gas":1.0,"peat":1.0,"uranium":1.0}
# Water consumption — m³ per m³
CF_WC = {"water":1.0}

ALL_CF = {"GWP (kg CO₂-eq)":CF_GWP,"AP (kg SO₂-eq)":CF_AP,"EP-fw (kg P-eq)":CF_EP,"EP-mar (kg N-eq)":CF_EP_M,
          "PM (kg PM2.5-eq)":CF_PM,"POCP (kg NMVOC-eq)":CF_POCP}

# ═══════════════════════════════════════════════════════════════
# ELEMENTARY FLOW COMPARTMENTS
# ═══════════════════════════════════════════════════════════════
COMPARTMENTS = {
    "CO2":"Emissions to air","CO2_bio":"Emissions to air","CO2_luc":"Emissions to air",
    "CH4":"Emissions to air","CH4_bio":"Emissions to air","N2O":"Emissions to air",
    "SO2":"Emissions to air","NOx":"Emissions to air","NO2":"Emissions to air",
    "NH3":"Emissions to air","HCl":"Emissions to air","HF":"Emissions to air",
    "PM25":"Emissions to air","PM10":"Emissions to air","CO":"Emissions to air",
    "NMVOC":"Emissions to air","benzene":"Emissions to air","formaldehyde":"Emissions to air",
    "H2S":"Emissions to air","Hg_air":"Emissions to air","Pb_air":"Emissions to air",
    "PO4":"Emissions to water","P_water":"Emissions to water","NO3":"Emissions to water",
    "N_water":"Emissions to water","NH4":"Emissions to water","COD":"Emissions to water",
    "BOD":"Emissions to water","Cu_w":"Emissions to water","Zn_w":"Emissions to water",
    "Pb_w":"Emissions to water","Cd_w":"Emissions to water","Ni_w":"Emissions to water",
    "Hg_w":"Emissions to water","As_w":"Emissions to water","Cr_w":"Emissions to water",
    "oil_w":"Emissions to water","phenol_w":"Emissions to water",
    "water":"Resources from nature","crude_oil":"Resources from nature",
    "hard_coal":"Resources from nature","natural_gas":"Resources from nature",
    "brown_coal":"Resources from nature","uranium":"Resources from nature",
    "iron_ore":"Resources from nature","bauxite":"Resources from nature",
    "copper_ore":"Resources from nature","limestone":"Resources from nature",
    "sand":"Resources from nature","wood":"Resources from nature",
    "land":"Resources from nature","peat":"Resources from nature",
}
FLOW_UNITS = {k:"kg" for k in COMPARTMENTS}
FLOW_UNITS.update({"water":"m³","land":"m²·a","crude_oil":"MJ","hard_coal":"MJ","natural_gas":"MJ","brown_coal":"MJ","uranium":"MJ","peat":"MJ"})
FLOW_NAMES = {
    "CO2":"Carbon dioxide, fossil","CO2_bio":"Carbon dioxide, biogenic","CO2_luc":"Carbon dioxide, land use change",
    "CH4":"Methane, fossil","CH4_bio":"Methane, biogenic","N2O":"Dinitrogen monoxide",
    "SO2":"Sulfur dioxide","NOx":"Nitrogen oxides (as NO₂)","NO2":"Nitrogen dioxide",
    "NH3":"Ammonia","HCl":"Hydrogen chloride","HF":"Hydrogen fluoride",
    "PM25":"Particulate matter, <2.5 µm","PM10":"Particulate matter, <10 µm",
    "CO":"Carbon monoxide, fossil","NMVOC":"NMVOC, unspecified","benzene":"Benzene",
    "formaldehyde":"Formaldehyde","H2S":"Hydrogen sulfide",
    "Hg_air":"Mercury (to air)","Pb_air":"Lead (to air)",
    "PO4":"Phosphate","P_water":"Phosphorus (to water)","NO3":"Nitrate",
    "N_water":"Nitrogen (to water)","NH4":"Ammonium (to water)","COD":"COD",
    "BOD":"BOD5","Cu_w":"Copper (to water)","Zn_w":"Zinc (to water)",
    "Pb_w":"Lead (to water)","Cd_w":"Cadmium (to water)","Ni_w":"Nickel (to water)",
    "Hg_w":"Mercury (to water)","As_w":"Arsenic (to water)","Cr_w":"Chromium (to water)",
    "oil_w":"Oils, unspecified (to water)","phenol_w":"Phenol (to water)",
    "water":"Water, unspecified","crude_oil":"Energy, from crude oil",
    "hard_coal":"Energy, from hard coal","natural_gas":"Energy, from natural gas",
    "brown_coal":"Energy, from lignite","uranium":"Energy, from uranium",
    "iron_ore":"Iron ore","bauxite":"Bauxite","copper_ore":"Copper ore",
    "limestone":"Limestone","sand":"Sand","wood":"Wood, unspecified",
    "land":"Land occupation, arable","peat":"Energy, from peat",
}

# ═══════════════════════════════════════════════════════════════
# ELECTRICITY GRID MIXES — 42 countries (IEA 2023/ecoinvent 3.11)
# Format: {country_code: {name, gwp_g_per_kwh, elementary_flows_per_kwh, ref}}
# Flows are in kg/kWh for substances
# ═══════════════════════════════════════════════════════════════
GRIDS = {
    "GLO":{"name":"World Average","g":475,"ref":"IEA (2023) WEO; ecoinvent 3.11"},
    "RER":{"name":"Europe (ENTSO-E avg)","g":295,"ref":"EEA (2024) GHG intensity; ecoinvent 3.11"},
    "EU27":{"name":"EU-27 Average","g":250,"ref":"EEA (2024); Eurostat"},
    "DE":{"name":"Germany","g":380,"ref":"UBA (2023); ecoinvent 3.11"},
    "FR":{"name":"France","g":56,"ref":"RTE (2023); ecoinvent 3.11"},
    "GB":{"name":"United Kingdom","g":207,"ref":"BEIS (2023); ecoinvent 3.11"},
    "IT":{"name":"Italy","g":315,"ref":"ISPRA (2023); ecoinvent 3.11"},
    "ES":{"name":"Spain","g":175,"ref":"REE (2023); ecoinvent 3.11"},
    "PL":{"name":"Poland","g":680,"ref":"KOBiZE (2023); ecoinvent 3.11"},
    "SE":{"name":"Sweden","g":12,"ref":"SCB (2023); ecoinvent 3.11"},
    "NO":{"name":"Norway","g":8,"ref":"NVE (2023); ecoinvent 3.11"},
    "FI":{"name":"Finland","g":78,"ref":"Statistics Finland (2023)"},
    "DK":{"name":"Denmark","g":115,"ref":"Energinet (2023)"},
    "NL":{"name":"Netherlands","g":340,"ref":"CBS (2023); ecoinvent 3.11"},
    "AT":{"name":"Austria","g":105,"ref":"E-Control (2023)"},
    "BE":{"name":"Belgium","g":155,"ref":"Elia (2023)"},
    "CH":{"name":"Switzerland","g":26,"ref":"BFE (2023); ecoinvent 3.11"},
    "CZ":{"name":"Czech Republic","g":420,"ref":"ERÚ (2023)"},
    "PT":{"name":"Portugal","g":135,"ref":"DGEG (2023)"},
    "IE":{"name":"Ireland","g":290,"ref":"EirGrid (2023)"},
    "GR":{"name":"Greece","g":305,"ref":"ADMIE (2023)"},
    "RO":{"name":"Romania","g":275,"ref":"Transelectrica (2023)"},
    "US":{"name":"United States avg","g":390,"ref":"EPA eGRID (2023); USLCI"},
    "US-CA":{"name":"California (CAISO)","g":210,"ref":"CARB (2023)"},
    "US-TX":{"name":"Texas (ERCOT)","g":380,"ref":"EPA eGRID (2023)"},
    "US-NW":{"name":"US Northwest","g":130,"ref":"EPA eGRID (2023)"},
    "CA":{"name":"Canada","g":120,"ref":"ECCC (2023); ecoinvent 3.11"},
    "CN":{"name":"China","g":580,"ref":"MEE (2023); ecoinvent 3.11"},
    "IN":{"name":"India","g":670,"ref":"CEA (2023); ecoinvent 3.11"},
    "JP":{"name":"Japan","g":450,"ref":"METI (2023); ecoinvent 3.11"},
    "KR":{"name":"South Korea","g":415,"ref":"KEPCO (2023)"},
    "AU":{"name":"Australia","g":560,"ref":"CER (2023); ecoinvent 3.11"},
    "NZ":{"name":"New Zealand","g":88,"ref":"MBIE (2023)"},
    "BR":{"name":"Brazil","g":72,"ref":"SIN (2023); ecoinvent 3.11"},
    "MX":{"name":"Mexico","g":410,"ref":"SENER (2023)"},
    "ZA":{"name":"South Africa","g":860,"ref":"Eskom (2023); ecoinvent 3.11"},
    "SA":{"name":"Saudi Arabia","g":580,"ref":"ECRA (2023)"},
    "AE":{"name":"UAE","g":410,"ref":"EWEC (2023)"},
    "IS":{"name":"Iceland","g":0.1,"ref":"Landsvirkjun (2023); 100% RE"},
    "CL":{"name":"Chile","g":330,"ref":"CNE (2023)"},
    "ID":{"name":"Indonesia","g":710,"ref":"PLN (2023)"},
    "TH":{"name":"Thailand","g":450,"ref":"EGAT (2023)"},
}
# Generate full elementary flows for each grid from GWP intensity
def grid_ef(g_per_kwh):
    """Generate approximate elementary flows per kWh from grid CO₂ intensity"""
    g=g_per_kwh
    return {
        "CO2":g*1e-3,"CH4":g*5e-7,"N2O":g*1.5e-8,
        "SO2":g*2e-6,"NOx":g*1.2e-6,"PM25":g*2.5e-7,"PM10":g*4e-7,
        "CO":g*3e-7,"NMVOC":g*8e-8,"Hg_air":g*2e-11,
        "natural_gas":g*3.5e-3,"hard_coal":g*4e-3,"crude_oil":g*5e-4,
        "uranium":g*2e-4,"water":g*3e-6,
        "N_water":g*8e-8,"PO4":g*2e-9,"COD":g*5e-8,
        "Cu_w":g*5e-10,"Zn_w":g*8e-10,"Ni_w":g*3e-10,
    }
for code,data in GRIDS.items():
    data["ef"]=grid_ef(data["g"])

# ═══════════════════════════════════════════════════════════════
# FULL PROCESS DATABASE WITH ELEMENTARY FLOWS & TECHNOSPHERE
# Each process has:
#   - "inputs": dict of {process_id: amount} (technosphere inputs)
#   - "ef": dict of {substance: amount_per_unit} (elementary flows/emissions)
#   - "outputs": list of output products
#   - standard metadata
# ═══════════════════════════════════════════════════════════════
PROCESSES = [
    # ───────────────────── ELECTRICITY (Technology-Specific) ─────────────────────
    {"id":"elec_hard_coal","name":"Electricity, hard coal, at power plant","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; IPCC AR5 Annex III",
     "inputs":{"hard_coal_supply":0.36,"water_supply":0.002,"limestone_supply":0.003},
     "ef":{"CO2":0.88,"CH4":0.00005,"N2O":0.000003,"SO2":0.002,"NOx":0.001,"PM25":0.00015,"PM10":0.00025,"CO":0.00015,"NMVOC":0.00002,"Hg_air":2.5e-8,"Pb_air":1e-7,
           "hard_coal":9.5,"water":0.0015,"N_water":0.000008,"COD":0.00005,"Cu_w":5e-9,"Zn_w":8e-9,"Ni_w":3e-9,"As_w":2e-9},
     "outputs":["electricity, high voltage"],"stages":["Coal Mining","Coal Washing","Pulverizer","Boiler (SC/USC)","ESP","FGD","SCR","Steam Turbine","Condenser","Ash Disposal"],
     "desc":"Supercritical hard coal plant. 800-1100 g CO₂/kWh. 38-42% eff."},
    {"id":"elec_lignite","name":"Electricity, lignite, at power plant","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11",
     "inputs":{"lignite_supply":0.45},
     "ef":{"CO2":1.05,"CH4":0.00006,"N2O":0.000004,"SO2":0.003,"NOx":0.0012,"PM25":0.0002,"PM10":0.0003,"CO":0.0002,"NMVOC":0.00003,"Hg_air":3e-8,
           "brown_coal":11.5,"water":0.002,"N_water":0.00001,"COD":0.00007},
     "outputs":["electricity, high voltage"],"stages":["Open-cast Mining","Drying","Pulverizer","Boiler","FGD","SCR","Steam Turbine"],
     "desc":"Lignite power — 1000-1200 g CO₂/kWh. ~33% eff. High water content in fuel."},
    {"id":"elec_ng_ccgt","name":"Electricity, natural gas, CCGT","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; IPCC AR5 Annex III; Stamford & Azapagic (2012)",
     "inputs":{"ng_supply":0.17},
     "ef":{"CO2":0.38,"CH4":0.0003,"N2O":0.000002,"SO2":0.0003,"NOx":0.0005,"PM25":0.00001,"PM10":0.00002,"CO":0.00008,"NMVOC":0.00001,
           "natural_gas":6.5,"water":0.0005,"N_water":0.000002,"COD":0.00001},
     "outputs":["electricity, high voltage"],"stages":["NG Extraction","NG Pipeline","Gas Turbine","HRSG","Steam Turbine","Condenser","Stack"],
     "desc":"Combined cycle gas — 400-500 g CO₂/kWh. ~58-62% eff."},
    {"id":"elec_ng_ocgt","name":"Electricity, natural gas, open cycle","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11",
     "inputs":{"ng_supply":0.28},
     "ef":{"CO2":0.58,"CH4":0.0005,"N2O":0.000003,"SO2":0.0005,"NOx":0.001,"PM25":0.00002,"PM10":0.00003,"CO":0.0001,"NMVOC":0.00002,
           "natural_gas":10.5,"water":0.0002},
     "outputs":["electricity, high voltage"],"stages":["NG Supply","Gas Turbine","Exhaust Stack"],
     "desc":"Open cycle gas turbine — 550-650 g CO₂/kWh. ~35% eff. Peaking."},
    {"id":"elec_oil","name":"Electricity, heavy fuel oil","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11",
     "inputs":{"hfo_supply":0.25},
     "ef":{"CO2":0.73,"CH4":0.0001,"N2O":0.000002,"SO2":0.005,"NOx":0.0015,"PM25":0.0004,"PM10":0.0006,"CO":0.00015,"NMVOC":0.00005,"Hg_air":1e-8,"Ni_w":5e-9,"V_w":8e-9,
           "crude_oil":8.5,"water":0.001},
     "outputs":["electricity, high voltage"],"stages":["Oil Refining","Fuel Storage","Oil Boiler","Steam Turbine"],
     "desc":"HFO power — 700-900 g CO₂/kWh. High SOx. Declining use."},
    {"id":"elec_solar_mono","name":"Electricity, photovoltaic, mono-Si","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Frischknecht et al. (2020) IEA PVPS Task 12; IPCC AR5",
     "inputs":{"silicon_supply":0.000004,"aluminium_supply":0.000008,"copper_supply":0.000003,"glass_supply":0.00001},
     "ef":{"CO2":0.035,"CH4":0.000025,"N2O":2e-7,"SO2":0.00018,"NOx":0.0001,"PM25":0.00002,"PM10":0.00003,"NMVOC":0.000008,
           "natural_gas":0.1,"hard_coal":0.05,"crude_oil":0.02,"water":0.00001,
           "Cu_w":3e-9,"Zn_w":5e-9,"Pb_w":2e-10,"Cd_w":1e-11},
     "outputs":["electricity, low voltage"],"stages":["Quartz Mining","MG-Si Reduction","Siemens Process","CZ Crystal Growth","Wafer Sawing","PERC/TOPCon Cell","Module Lamination","BOS/Inverter","Installation","Decommission"],
     "desc":"Mono-Si PV (rooftop+ground). 20-45 g CO₂/kWh. 25+ yr lifetime."},
    {"id":"elec_solar_cdte","name":"Electricity, photovoltaic, CdTe thin-film","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"Fthenakis et al. (2011) Renew Sustain Energy Rev; First Solar (2023)",
     "inputs":{"cadmium_telluride":0.000001,"glass_supply":0.000015},
     "ef":{"CO2":0.015,"CH4":0.00001,"N2O":1e-7,"SO2":0.00008,"NOx":0.00005,"PM25":0.00001,"NMVOC":0.000003,
           "natural_gas":0.04,"hard_coal":0.02,"water":0.000008,"Cd_w":5e-12},
     "outputs":["electricity, low voltage"],"stages":["CdTe Deposition","Module Assembly","BOS","Installation"],
     "desc":"CdTe thin-film (First Solar). 14-22 g CO₂/kWh. Lower embodied energy."},
    {"id":"elec_wind_on","name":"Electricity, wind, onshore, >3MW","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"RER","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Arvesen & Hertwich (2012) Renew Sustain Energy Rev; IPCC AR5",
     "inputs":{"steel_supply":0.00001,"concrete_supply":0.00005,"grp_supply":0.000003,"copper_supply":0.000001},
     "ef":{"CO2":0.009,"CH4":0.000008,"N2O":1e-7,"SO2":0.000055,"NOx":0.000032,"PM25":0.000005,"PM10":0.000008,"CO":0.000003,"NMVOC":0.000002,
           "natural_gas":0.02,"hard_coal":0.01,"crude_oil":0.008,"iron_ore":0.00001,"water":0.000001,"Cu_w":2e-9},
     "outputs":["electricity, high voltage"],"stages":["Steel Tower Mfg","Nacelle & Gearbox","Blade Production (GRP/CF)","Concrete Foundation","Transport & Erection","Grid Connection","O&M (20-30yr)","Decommission & Recycle"],
     "desc":"Onshore wind — 7-15 g CO₂/kWh. 30-45% CF. 25-30yr."},
    {"id":"elec_wind_off","name":"Electricity, wind, offshore, >8MW","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"RER","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Bonou et al. (2016) Appl Energy",
     "inputs":{"steel_supply":0.000015,"concrete_supply":0.00003,"copper_supply":0.000002},
     "ef":{"CO2":0.012,"CH4":0.00001,"N2O":1.5e-7,"SO2":0.00007,"NOx":0.00004,"PM25":0.000007,"PM10":0.00001,"NMVOC":0.000003,
           "natural_gas":0.03,"hard_coal":0.015,"crude_oil":0.01,"iron_ore":0.000015,"water":0.000001},
     "outputs":["electricity, high voltage"],"stages":["Monopile/Jacket Foundation","Turbine Mfg","Submarine Cable","Offshore Installation","Substation","O&M (CTV/SOV)","Decommission"],
     "desc":"Offshore wind — 12-20 g CO₂/kWh. 40-55% CF. 12-15 MW turbines."},
    {"id":"elec_nuclear","name":"Electricity, nuclear, pressure water reactor","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Warner & Heath (2012) J Ind Ecol; IPCC AR5",
     "inputs":{"uranium_supply":0.000004},
     "ef":{"CO2":0.01,"CH4":0.0000045,"N2O":1e-7,"SO2":0.000047,"NOx":0.000025,"PM25":0.000003,"PM10":0.000005,
           "uranium":0.04,"water":0.000002,"N_water":0.000001,"PO4":5e-9,"Cu_w":1e-9},
     "outputs":["electricity, high voltage"],"stages":["Uranium Mining","Milling","Conversion (UF₆)","Enrichment (Centrifuge)","Fuel Fabrication (UO₂ pellets)","Reactor Operation (PWR)","Spent Fuel Cooling","Interim Storage","Decommissioning"],
     "desc":"PWR nuclear — 5-15 g CO₂/kWh. 85-90% CF. 60yr lifetime."},
    {"id":"elec_hydro_reservoir","name":"Electricity, hydropower, reservoir","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Hertwich (2013) Environ Res Lett; IPCC AR5",
     "inputs":{"concrete_supply":0.0001,"steel_supply":0.000005},
     "ef":{"CO2":0.02,"CH4":0.00012,"CH4_bio":0.00008,"N2O":5e-7,"SO2":0.000031,"NOx":0.000025,"PM25":0.000002,
           "water":0.000003,"N_water":0.000001},
     "outputs":["electricity, high voltage"],"stages":["Dam Construction (Concrete/RCC)","Reservoir Filling","Penstock","Francis/Kaplan Turbine","Generator","Transformer","Transmission","Sediment Mgmt","Decommission"],
     "desc":"Reservoir hydro — 4-30 g CO₂/kWh. CH₄ from reservoirs varies by climate."},
    {"id":"elec_hydro_ror","name":"Electricity, hydropower, run-of-river","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11",
     "inputs":{"concrete_supply":0.00003,"steel_supply":0.000002},
     "ef":{"CO2":0.004,"CH4":0.000002,"N2O":5e-8,"SO2":0.00001,"NOx":0.000008,
           "water":0.000001},
     "outputs":["electricity, high voltage"],"stages":["Weir/Intake","Headrace","Turbine","Tailrace"],
     "desc":"Run-of-river — 2-5 g CO₂/kWh. Low CH₄. Small footprint."},
    {"id":"elec_geothermal","name":"Electricity, geothermal, flash","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Sullivan et al. (2010) Argonne; IPCC AR5",
     "inputs":{},
     "ef":{"CO2":0.03,"CH4":0.00002,"N2O":3e-7,"SO2":0.00008,"NOx":0.00004,"H2S":0.00005,
           "water":0.00001},
     "outputs":["electricity, high voltage"],"stages":["Exploration","Well Drilling","Production Well","Flash Separator","Steam Turbine","Condenser","NCG Treatment","Reinjection Well"],
     "desc":"Geothermal flash — 15-55 g CO₂/kWh. Varies by field."},
    {"id":"elec_biomass_chp","name":"Electricity, biomass CHP, wood chips","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"RER","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Cherubini et al. (2009)",
     "inputs":{"wood_chips":0.5},
     "ef":{"CO2_bio":0.4,"CO2":0.04,"CH4":0.00003,"CH4_bio":0.00001,"N2O":0.000005,"SO2":0.0004,"NOx":0.0006,"PM25":0.00015,"PM10":0.0003,"CO":0.001,"NMVOC":0.0001,
           "wood":0.5,"water":0.00003,"N_water":0.000003,"PO4":2e-8},
     "outputs":["electricity, high voltage","heat, district"],"stages":["Wood Chip Supply","Storage & Feeding","Grate/Fluidized Bed Furnace","Boiler","Flue Gas Treatment (ESP/Bag)","Steam Turbine (Backpressure)","Heat Exchanger","Ash Management"],
     "desc":"Biomass CHP — 30-80 g fossil CO₂/kWh. Biogenic CO₂ accounted separately."},
    {"id":"elec_biogas","name":"Electricity, biogas, CHP","cat":"Energy","sector":"Electricity","unit":"kWh","geo":"RER","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Møller et al. (2009)",
     "inputs":{"biogas_supply":0.35},
     "ef":{"CO2_bio":0.35,"CO2":0.015,"CH4":0.0008,"CH4_bio":0.0002,"N2O":0.000008,"SO2":0.0002,"NOx":0.0008,"PM25":0.00003,"CO":0.0003,"NMVOC":0.00008,
           "water":0.00002},
     "outputs":["electricity, low voltage","heat"],"stages":["AD Feedstock","Anaerobic Digester","Biogas Upgrading/Direct Use","Gas Engine CHP","Flue Gas","Digestate"],
     "desc":"Biogas CHP — 35-60 g fossil CO₂/kWh net. CH₄ slip from engine critical."},
    # ───────────────────── COUNTRY GRID MIXES ─────────────────────
] + [
    {"id":f"grid_{code.lower()}","name":f"Electricity, grid mix, {data['name']}","cat":"Energy","sector":"Grid Mix","unit":"kWh",
     "geo":code,"db":"IEA (2023)/ecoinvent 3.11","ref":data["ref"],
     "inputs":{},"ef":data["ef"],
     "outputs":[f"electricity, medium voltage, {code}"],
     "stages":["Generation Mix","HV Transmission (losses ~2%)","MV Transformation (losses ~1%)","LV Distribution (losses ~4%)"],
     "desc":f"National grid mix — {data['g']} g CO₂/kWh (direct+upstream lifecycle)."}
    for code,data in GRIDS.items()
] + [
    # ───────────────────── HEAT & FUELS ─────────────────────
    {"id":"heat_ng_boiler","name":"Heat, natural gas, boiler >100kW","cat":"Energy","sector":"Heat","unit":"MJ","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; IPCC (2006) EF guidelines",
     "inputs":{"ng_supply":1.11},
     "ef":{"CO2":0.0561,"CH4":5.3e-6,"N2O":1e-7,"SO2":1.5e-7,"NOx":6.1e-5,"PM25":1e-6,"CO":1.5e-5,"NMVOC":2.5e-6,
           "natural_gas":1.11,"water":2e-5},
     "outputs":["heat, central"],"stages":["NG Supply","Pre-mixing","Burner","Heat Exchanger","Flue Gas","Condensate Return"],
     "desc":"Industrial NG boiler — 56.1 g CO₂/MJ (IPCC default). 90-95% eff."},
    {"id":"heat_coal_boiler","name":"Heat, hard coal, industrial boiler","cat":"Energy","sector":"Heat","unit":"MJ","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; IPCC (2006)",
     "inputs":{"hard_coal_supply":1.15},
     "ef":{"CO2":0.0942,"CH4":2e-6,"N2O":1.5e-6,"SO2":6.4e-4,"NOx":1.8e-4,"PM25":3.5e-5,"PM10":6e-5,"CO":5e-5,
           "hard_coal":1.15,"water":5e-5},
     "outputs":["heat, central"],"stages":["Coal Feed","Grate/Stoker","Boiler","ESP","Stack","Ash Removal"],
     "desc":"Industrial coal boiler — 94.2 g CO₂/MJ. 80-88% eff."},
    {"id":"heat_oil_boiler","name":"Heat, light fuel oil, boiler","cat":"Energy","sector":"Heat","unit":"MJ","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; IPCC (2006)",
     "inputs":{"lfo_supply":1.08},
     "ef":{"CO2":0.0741,"CH4":2.5e-6,"N2O":2.7e-7,"SO2":1.3e-5,"NOx":1.9e-4,"PM25":5e-6,"CO":1e-5,
           "crude_oil":1.08,"water":1e-5},
     "outputs":["heat, central"],"stages":["Oil Supply","Atomizer/Burner","Boiler","Heat Exchanger","Flue Gas"],
     "desc":"Oil boiler — 74.1 g CO₂/MJ. 85-92% eff."},
    {"id":"heat_biomass","name":"Heat, wood chips, furnace >100kW","cat":"Energy","sector":"Heat","unit":"MJ","geo":"RER","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11",
     "inputs":{"wood_chips":0.08},
     "ef":{"CO2_bio":0.1,"CO2":0.005,"CH4":5e-6,"N2O":4e-7,"SO2":5e-5,"NOx":1.2e-4,"PM25":5e-5,"PM10":8e-5,"CO":5e-4,"NMVOC":3e-5,
           "wood":0.08,"water":5e-6},
     "outputs":["heat, central"],"stages":["Wood Chip Supply","Storage","Feeding","Grate Furnace","Heat Exchanger","Flue Gas Treatment","Ash Disposal"],
     "desc":"Biomass heat — 5 g fossil CO₂/MJ + biogenic."},
    {"id":"heat_pump_air","name":"Heat, air-source heat pump","cat":"Energy","sector":"Heat","unit":"MJ","geo":"RER","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Arpagaus et al. (2018)",
     "inputs":{"grid_rer":0.083},
     "ef":{"CO2":0.025,"CH4":4e-6,"N2O":1e-7,"SO2":8e-5,"NOx":5e-5,"PM25":8e-6,
           "natural_gas":0.09,"hard_coal":0.05,"water":3e-6},
     "outputs":["heat, central"],"stages":["Electricity Supply","Compressor","Evaporator (Air)","Condenser","Expansion Valve","Refrigerant (R410A)"],
     "desc":"Air-source HP (COP=3.3) — 25 g CO₂/MJ with EU grid. Dependent on grid CF."},
    {"id":"steam_ng","name":"Steam, from natural gas, at industrial plant","cat":"Energy","sector":"Heat","unit":"kg steam","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Worrell et al. (2008)",
     "inputs":{"ng_supply":3.2},
     "ef":{"CO2":0.18,"CH4":1.7e-5,"N2O":3.2e-7,"SO2":5e-7,"NOx":1.9e-4,"PM25":3e-6,"CO":5e-5,
           "natural_gas":3.2,"water":0.0012},
     "outputs":["steam, in chemical industry"],"stages":["NG Supply","Water Treatment","Boiler (Shell/Fire-tube)","Steam Header","Condensate Return","Blowdown Treatment"],
     "desc":"Industrial steam (10 bar, saturated) from NG boiler. ~180 g CO₂/kg steam."},
    # ───────────────────── FUELS & FEEDSTOCKS ─────────────────────
    {"id":"ng_supply","name":"Natural gas, high pressure, at consumer","cat":"Fuels","sector":"Fossil Fuels","unit":"MJ","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Alvarez et al. (2018) Science (CH₄ leakage)",
     "inputs":{},
     "ef":{"CO2":0.006,"CH4":0.00012,"SO2":3e-6,"NOx":1e-5,"NMVOC":3e-6,
           "natural_gas":1.04,"crude_oil":0.02,"water":5e-6},
     "outputs":["natural gas, high pressure"],"stages":["Well Drilling","Extraction","Processing (Acid Gas Removal)","Compression","Pipeline Transport (CH₄ leakage 0.5-3%)","Metering"],
     "desc":"NG supply including upstream. CH₄ leakage is critical — Alvarez (2018) measured 2.3% US avg."},
    {"id":"diesel_supply","name":"Diesel, at refinery","cat":"Fuels","sector":"Fossil Fuels","unit":"kg","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; JEC WTW v5",
     "inputs":{},
     "ef":{"CO2":0.45,"CH4":0.001,"N2O":5e-6,"SO2":0.002,"NOx":0.001,"PM25":0.00015,"NMVOC":0.003,
           "crude_oil":47,"water":0.003,"oil_w":5e-6,"phenol_w":1e-7},
     "outputs":["diesel"],"stages":["Crude Oil Extraction","Tanker Transport","Atmospheric Distillation","Vacuum Distillation","Hydrocracking","Hydrotreating","Blending","Storage"],
     "desc":"Diesel production at refinery — WTT ~0.45 kg CO₂/kg diesel."},
    {"id":"hfo_supply","name":"Heavy fuel oil, at refinery","cat":"Fuels","sector":"Fossil Fuels","unit":"kg","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11",
     "inputs":{},
     "ef":{"CO2":0.35,"CH4":0.0008,"SO2":0.003,"NOx":0.0008,"NMVOC":0.002,
           "crude_oil":44,"water":0.002,"oil_w":8e-6,"Ni_w":2e-8,"V_w":5e-8},
     "outputs":["heavy fuel oil"],"stages":["Crude Extraction","Transport","Distillation","Visbreaking","Storage"],
     "desc":"HFO (bunker fuel) — residual from refining. High sulfur."},
    # ───────────────────── HYDROGEN ─────────────────────
    {"id":"h2_smr","name":"Hydrogen, SMR, from natural gas","cat":"Hydrogen","sector":"Hydrogen Production","unit":"kg H₂","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"Bauer et al. (2022) Green Chem; Hydrogen Council (2021); IPHE (2022)",
     "inputs":{"ng_supply":167,"steam_ng":22,"grid_glo":1.2,"water_supply":9},
     "ef":{"CO2":10.5,"CH4":0.015,"N2O":3e-5,"SO2":0.012,"NOx":0.008,"PM25":0.0008,"CO":0.003,"NMVOC":0.001,
           "natural_gas":167,"water":0.022,"N_water":0.00005,"COD":0.0002},
     "outputs":["hydrogen, gaseous"],"stages":["NG Desulfurization (ZnO Guard Bed)","Pre-reformer","Primary Reformer (850°C, Ni catalyst)","Waste Heat Boiler","High-Temp Shift (Fe-Cr, 350°C)","Low-Temp Shift (Cu-Zn, 200°C)","CO₂ Removal (MDEA/aMDEA)","Methanation","PSA (Pressure Swing Adsorption, 99.99% H₂)","H₂ Compression (30 bar)","H₂ Storage"],
     "desc":"Conventional SMR — 9-12 kg CO₂/kg H₂ (lifecycle). NG feed (3.7 kg/kg H₂) + NG fuel (2.0 kg/kg H₂). 167 MJ NG total."},
    {"id":"h2_smr_ccs","name":"Hydrogen, SMR + CCS (Blue H₂)","cat":"Hydrogen","sector":"Hydrogen Production","unit":"kg H₂","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"Hydrogen Council (2021); IEAGHG (2017); Howarth & Jacobson (2021) Energy Sci Eng",
     "inputs":{"ng_supply":185,"steam_ng":28,"grid_glo":3.5,"water_supply":14,"mea_supply":0.002},
     "ef":{"CO2":2.8,"CH4":0.012,"N2O":3e-5,"SO2":0.01,"NOx":0.007,"PM25":0.0006,"CO":0.002,"NH3":0.0001,
           "natural_gas":185,"water":0.028,"N_water":0.00004,"COD":0.00015},
     "outputs":["hydrogen, gaseous","carbon dioxide, captured"],"stages":["NG Desulfurization","Pre-reformer","Primary Reformer","WHB","HT Shift","LT Shift","CO₂ Absorption (MEA 30 wt%)","Solvent Regeneration (120°C)","CO₂ Compression (110 bar)","CO₂ Dehydration","CO₂ Pipeline Transport","CO₂ Injection Well","PSA","H₂ Compression"],
     "desc":"Blue H₂ — SMR with 90% CO₂ capture. Residual 1.5-3.7 kg CO₂/kg H₂ including upstream CH₄ leakage. Extra 15-25% energy penalty."},
    {"id":"h2_pem_wind","name":"Hydrogen, PEM electrolysis, wind power","cat":"Hydrogen","sector":"Hydrogen Production","unit":"kg H₂","geo":"RER","db":"ecoinvent 3.11",
     "ref":"Bauer et al. (2022); IEA (2023); IRENA (2020)",
     "inputs":{"elec_wind_on":55,"water_supply":9},
     "ef":{"CO2":0.5,"CH4":0.0004,"N2O":5e-6,"SO2":0.003,"NOx":0.0018,"PM25":0.0003,"CO":0.0002,
           "iron_ore":0.00055,"copper_ore":0.00016,"water":0.009,"N_water":0.00001},
     "outputs":["hydrogen, gaseous","oxygen, gaseous"],"stages":["Wind Turbine Electricity Supply","Water Deionization (RO/EDI)","PEM Electrolyzer Stack (Nafion membrane, Ir/Pt catalyst)","Anodic O₂ Collection","Cathodic H₂ Collection","Gas-Liquid Separator","H₂ Dryer (TSA)","H₂ Compression (30-350 bar)","H₂ Storage (Type IV vessel)"],
     "desc":"Green H₂ via PEM electrolysis + wind — 0.3-1.5 kg CO₂/kg H₂. 50-55 kWh/kg H₂ (system). PEM stack: 60-70% system eff."},
    {"id":"h2_ael_solar","name":"Hydrogen, alkaline electrolysis, solar PV","cat":"Hydrogen","sector":"Hydrogen Production","unit":"kg H₂","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"IRENA (2020); Kadam & Yadav (2023)",
     "inputs":{"elec_solar_mono":55,"water_supply":9.5},
     "ef":{"CO2":1.5,"CH4":0.0012,"N2O":1e-5,"SO2":0.009,"NOx":0.005,"PM25":0.001,"NMVOC":0.0004,
           "water":0.0095,"iron_ore":0.0003},
     "outputs":["hydrogen, gaseous","oxygen, gaseous"],"stages":["Solar PV Electricity","Water Purification (RO)","KOH Electrolyte Preparation (25-30 wt%)","Alkaline Electrolyzer Cell Stack (Ni electrodes, ZrO₂ diaphragm)","Gas-Liquid Separation","Lye Reconcentration","H₂ Drying","H₂ Compression"],
     "desc":"AEL + solar PV — 1.0-2.5 kg CO₂/kg H₂. 52-58 kWh/kg H₂. Lower capex than PEM, ~65% system eff."},
    {"id":"h2_soec","name":"Hydrogen, SOEC high-temp electrolysis","cat":"Hydrogen","sector":"Hydrogen Production","unit":"kg H₂","geo":"GLO","db":"Literature",
     "ref":"Hauch et al. (2020) Science; IEA (2023); Hydrogen Council (2021)",
     "inputs":{"elec_nuclear":35,"steam_ng":10,"water_supply":8},
     "ef":{"CO2":0.4,"CH4":0.0002,"N2O":3e-6,"SO2":0.002,"NOx":0.001,"PM25":0.0001,
           "uranium":0.001,"water":0.008},
     "outputs":["hydrogen, gaseous","oxygen, gaseous"],"stages":["Electricity Supply (Nuclear/RE)","Water Deaeration","Steam Generation (700-800°C)","SOEC Stack (YSZ electrolyte, Ni-YSZ cathode, LSM anode)","O₂ Sweep Gas","H₂/Steam Separation (Condenser)","H₂ Purification","H₂ Compression"],
     "desc":"SOEC — >80% electrical eff (with heat integration). 35-40 kWh/kg H₂ (electricity) + heat. TRL 5-7. Degradation 1-2%/1000h."},
    {"id":"h2_biomass_gasif","name":"Hydrogen, biomass gasification","cat":"Hydrogen","sector":"Hydrogen Production","unit":"kg H₂","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"Susmozas et al. (2016) Int J Hydrogen Energy; ecoinvent 3.11",
     "inputs":{"wood_chips":15,"grid_glo":2,"water_supply":15},
     "ef":{"CO2":1.5,"CO2_bio":8.0,"CH4":0.003,"CH4_bio":0.001,"N2O":0.0001,"SO2":0.005,"NOx":0.004,"PM25":0.002,"PM10":0.003,"CO":0.005,"NMVOC":0.001,
           "wood":15,"water":0.015,"N_water":0.0001,"PO4":5e-7},
     "outputs":["hydrogen, gaseous"],"stages":["Biomass Sourcing & Chipping","Drying (to <15% moisture)","Feeding System","Fluidized Bed / Entrained Flow Gasifier (800-1000°C)","Cyclone & Tar Reforming","Syngas Cooling","Water-Gas Shift Reactor","Acid Gas Removal (H₂S, COS)","PSA H₂ Purification","Char/Ash Management"],
     "desc":"Biomass gasification — 2-5 kg fossil CO₂/kg H₂ + 8 kg biogenic CO₂. Could be net-negative with BECCS."},
    {"id":"h2_pyrolysis","name":"Hydrogen, methane pyrolysis (turquoise)","cat":"Hydrogen","sector":"Hydrogen Production","unit":"kg H₂","geo":"GLO","db":"Literature",
     "ref":"Schneider et al. (2020) Int J Hydrogen Energy; Parkinson et al. (2019)",
     "inputs":{"ng_supply":75,"grid_glo":10},
     "ef":{"CO2":1.0,"CH4":0.008,"N2O":1e-5,"SO2":0.003,"NOx":0.002,"PM25":0.0005,"CO":0.001,
           "natural_gas":75,"water":0.005},
     "outputs":["hydrogen, gaseous","carbon, solid"],"stages":["NG Supply","Preheating","Pyrolysis Reactor (>1000°C, molten metal/plasma/thermal)","Quench Zone","Solid Carbon Separation (Cyclone/Filter)","H₂ Purification","Carbon Pelletizing/Storage"],
     "desc":"Thermal CH₄ → H₂ + C(solid). No direct CO₂. GWP depends on CH₄ slip, energy source, and carbon fate."},
    {"id":"h2_plasma","name":"Hydrogen, plasma reforming (ex-ante)","cat":"Hydrogen","sector":"Hydrogen Production","unit":"kg H₂","geo":"GLO","db":"Literature (ex-ante)",
     "ref":"Czylkowski et al. (2016) Int J Hydrogen Energy; Tao et al. (2022)",
     "inputs":{"ng_supply":50,"grid_glo":15},
     "ef":{"CO2":1.2,"CH4":0.001,"N2O":5e-6,"SO2":0.002,"NOx":0.0015,"PM25":0.0002,
           "natural_gas":50,"water":0.006},
     "outputs":["hydrogen, gaseous","syngas"],"stages":["NG Feed","Plasma Torch/Microwave Generation","Plasma Reforming Zone (2000-5000K locally)","Product Quenching","WGS Reactor","H₂ Membrane Separation"],
     "desc":"Non-thermal plasma reforming — higher selectivity, lower bulk T. TRL 3-5. Pilot scale."},
    {"id":"h2_cucl","name":"Hydrogen, Cu-Cl thermochemical cycle, nuclear","cat":"Hydrogen","sector":"Hydrogen Production","unit":"kg H₂","geo":"GLO","db":"Literature",
     "ref":"Ozbilen et al. (2012) Int J Hydrogen Energy; Kadam & Yadav (2023)",
     "inputs":{"elec_nuclear":20,"heat_nuclear":150},
     "ef":{"CO2":0.7,"CH4":0.00008,"N2O":1e-6,"SO2":0.002,"NOx":0.001,"HCl":0.0005,
           "uranium":0.006,"water":0.015},
     "outputs":["hydrogen, gaseous","oxygen, gaseous"],"stages":["Nuclear Heat Generation (530°C)","Step 1: HCl + H₂O Electrolysis → H₂ + CuCl₂","Step 2: Cu₂OCl₂ Hydrolysis","Step 3: CuCl₂ Decomposition → Cu₂OCl₂ + Cl₂","Step 4: O₂ Recovery","H₂ Purification & Compression"],
     "desc":"Cu-Cl 4-step cycle — 0.37-0.92 kg CO₂/kg H₂. Max T = 530°C (vs 900°C for S-I). Nuclear heat."},
    # ───────────────────── AMMONIA ─────────────────────
    {"id":"nh3_hb_ng","name":"Ammonia, Haber-Bosch, from natural gas","cat":"Chemicals","sector":"Ammonia","unit":"kg NH₃","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; IEA (2021) Ammonia Roadmap; Fertilizers Europe (2019)",
     "inputs":{"ng_supply":28,"steam_ng":3,"grid_glo":0.4,"water_supply":1.5},
     "ef":{"CO2":1.6,"CH4":0.0001,"N2O":3e-6,"SO2":0.001,"NOx":0.0009,"PM25":0.00005,"CO":0.0002,"NH3":0.0005,
           "natural_gas":28,"water":0.0035,"N_water":0.00005,"NH4":0.00003},
     "outputs":["ammonia, liquid"],"stages":["NG Desulfurization (ZnO/HDS)","Primary Steam Reformer (800°C, Ni catalyst)","Secondary Reformer (Air injection, 1000°C)","HT Shift (Fe₃O₄-Cr₂O₃, 400°C)","LT Shift (Cu-ZnO-Al₂O₃, 200°C)","CO₂ Removal (MDEA/aMDEA/Benfield)","Methanation (Ni catalyst)","Syngas Compression (150-300 bar)","NH₃ Synthesis Loop (Fe catalyst, 400-500°C, 150-300 bar)","NH₃ Condensation (-33°C)","Purge Gas Recovery","NH₃ Storage (atmospheric tank)"],
     "desc":"Conventional Haber-Bosch — 1.6-2.0 t CO₂/t NH₃. 28 GJ/t NH₃ (best practice). ~180 Mt/yr globally, ~1.8% of global CO₂."},
    {"id":"nh3_green","name":"Ammonia, green, from electrolytic H₂","cat":"Chemicals","sector":"Ammonia","unit":"kg NH₃","geo":"GLO","db":"Literature",
     "ref":"IRENA (2022) Innovation Outlook Ammonia; MacFarlane et al. (2020) Joule",
     "inputs":{"h2_pem_wind":0.178,"grid_glo":0.5,"water_supply":2},
     "ef":{"CO2":0.3,"CH4":0.00005,"N2O":2e-6,"SO2":0.001,"NOx":0.0005,"PM25":0.0001,
           "water":0.005,"N_water":0.00001},
     "outputs":["ammonia, liquid"],"stages":["Renewable Electricity Supply","PEM/AEL Electrolyzer (H₂ production)","Air Separation Unit (Cryogenic N₂)","H₂ Buffer Storage","H₂/N₂ Compression (150-300 bar)","Haber-Bosch Synthesis Loop","NH₃ Condensation","Storage"],
     "desc":"Green NH₃ — 0.18 kg H₂/kg NH₃ + electricity. 9-10 MWh/t NH₃. Projects: NEOM (SA), Yara Pilbara (AU)."},
    # ───────────────────── CARBON CAPTURE ─────────────────────
    {"id":"cc_mea","name":"CO₂ capture, post-combustion, MEA","cat":"Carbon Capture","sector":"CCUS","unit":"t CO₂ captured","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"IEAGHG (2019); Rochelle (2009) Science; Pehnt & Henkel (2009)",
     "inputs":{"steam_ng":1300,"grid_glo":110,"mea_supply":1.5,"water_supply":1500},
     "ef":{"CO2":100,"CH4":0.01,"N2O":0.0005,"SO2":0.08,"NOx":0.06,"PM25":0.005,"NH3":0.02,"NMVOC":0.008,"formaldehyde":0.001,
           "natural_gas":2400,"water":1.5,"N_water":0.001,"NH4":0.0005,"COD":0.003},
     "outputs":["carbon dioxide, captured, pressurized"],"stages":["Flue Gas Cooling (DCC to 40°C)","SO₂ Polishing Scrubber (<10 ppm)","Absorber Column (MEA 30 wt%, 40-60°C)","Rich Amine Pump","Lean-Rich Heat Exchanger (cross HX, ΔT~10°C)","Stripper/Regenerator Column (120°C, 1.5-2 bar)","Reboiler (steam 3-4 GJ/t CO₂)","Reflux Condenser","Lean Amine Cooler & Recycle","MEA Reclaimer (thermal)","CO₂ Compression (multi-stage to 110 bar)","CO₂ Dehydration (TEG)"],
     "desc":"MEA scrubbing — most mature (TRL 9). Regen energy 3.2-4.0 GJ/t CO₂. 85-95% capture rate. MEA degradation → amine emissions, reclaiming needed."},
    {"id":"cc_membrane","name":"CO₂ capture, membrane separation","cat":"Carbon Capture","sector":"CCUS","unit":"t CO₂ captured","geo":"GLO","db":"Literature (ex-ante)",
     "ref":"Merkel et al. (2010) J Membr Sci; MTR Inc. pilot; Brunetti et al. (2010)",
     "inputs":{"grid_glo":200,"membrane_module":0.05},
     "ef":{"CO2":55,"CH4":0.003,"N2O":0.0002,"SO2":0.03,"NOx":0.02,"PM25":0.002,
           "natural_gas":300,"water":0.3},
     "outputs":["carbon dioxide, captured"],"stages":["Flue Gas Pre-treatment (SOx/PM removal)","1st Stage Membrane Module (Polaris™/Polyactive)","Permeate Compression","2nd Stage Membrane Module (sweep mode)","CO₂ Rich Stream Collection","Final CO₂ Compression (to 110 bar)"],
     "desc":"Polymeric membrane — TRL 5-7. 1.5-2.5 GJ/t CO₂ (electricity only, no steam). Lower footprint but lower capture rate (70-90%)."},
    # ───────────────────── DIRECT AIR CAPTURE ─────────────────────
    {"id":"dac_sdac","name":"DAC, solid sorbent (Climeworks type)","cat":"Carbon Capture","sector":"DAC","unit":"t CO₂ captured","geo":"IS","db":"Literature",
     "ref":"Deutz & Bardow (2021) Nat Energy; Madhu et al. (2021) Environ Sci Technol; Climeworks (2022)",
     "inputs":{"grid_is":1500,"heat_geothermal":5000,"water_supply":1500},
     "ef":{"CO2":70,"CH4":0.005,"N2O":0.0003,"SO2":0.05,"NOx":0.03,"PM25":0.003,
           "water":1.5,"iron_ore":0.05,"copper_ore":0.01},
     "outputs":["carbon dioxide, captured from air"],"stages":["Large Air Contactors (fans, 1800 m³ air/t CO₂)","CO₂ Adsorption on Amine-Functionalized Sorbent (cellulose/silica support)","Air Outlet (CO₂-depleted)","Chamber Sealing","Temperature Swing (80-120°C, waste heat/geothermal)","Vacuum Application (100-300 mbar)","CO₂ Desorption & Collection","Sorbent Cooling & Regeneration","CO₂ Compression (to 110 bar)","CO₂ Transport & Injection (mineralization in basalt, Carbfix)"],
     "desc":"Climeworks-type S-DAC — 1.5-2.0 MWh elec + 4-6 GJ low-T heat per t CO₂. Carbon removal eff 85-93%. Orca (4kt/yr), Mammoth (36kt/yr). Cost $600-1000/t."},
    {"id":"dac_ldac","name":"DAC, liquid solvent (1PointFive type)","cat":"Carbon Capture","sector":"DAC","unit":"t CO₂ captured","geo":"US","db":"Literature",
     "ref":"Keith et al. (2018) Joule; Ozkan et al. (2022); IEA DAC 2022",
     "inputs":{"ng_supply":5250,"grid_us":366,"water_supply":5000,"koh_supply":0.01,"caco3_supply":5},
     "ef":{"CO2":220,"CH4":0.008,"N2O":0.0004,"SO2":0.08,"NOx":0.05,"PM25":0.005,
           "natural_gas":5250,"water":5.0,"N_water":0.0005,"COD":0.002},
     "outputs":["carbon dioxide, captured from air"],"stages":["Large Cross-Flow Air Contactor (PVC structured packing)","KOH Solution Spray (1-2 M)","CO₂ Absorption → K₂CO₃ (K₂CO₃ solution)","Causticizer (Ca(OH)₂ + K₂CO₃ → CaCO₃ + 2KOH)","CaCO₃ Pellet Drying","Calciner (Oxy-fired, 900°C → CaO + CO₂)","CO₂ Release & Collection","CaO Slaker (CaO + H₂O → Ca(OH)₂)","KOH Loop Regeneration","CO₂ Compression (110 bar)","CO₂ Pipeline & Storage"],
     "desc":"L-DAC (Carbon Engineering/1PointFive) — 5.25 GJ NG + 366 kWh elec/t CO₂. 900°C calcination (NG inherently captured). 1-7 t water/t CO₂. Stratos plant 500 kt/yr."},
    # ───────────────────── METHANOL ─────────────────────
    {"id":"meoh_ng","name":"Methanol, from natural gas, at plant","cat":"Chemicals","sector":"Methanol","unit":"kg MeOH","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Pérez-Fortes et al. (2016) Appl Energy",
     "inputs":{"ng_supply":32,"steam_ng":2,"grid_glo":0.15,"water_supply":1},
     "ef":{"CO2":0.85,"CH4":0.0005,"N2O":2e-6,"SO2":0.0012,"NOx":0.0007,"PM25":0.00005,"CO":0.0002,"NMVOC":0.0003,
           "natural_gas":32,"water":0.0012,"COD":0.00003},
     "outputs":["methanol"],"stages":["NG Desulfurization","Adiabatic Pre-reformer","ATR/Steam Reformer (850-1000°C)","Syngas Cooling & Condensation","Syngas Compression (50-100 bar)","Methanol Synthesis Reactor (Cu/ZnO/Al₂O₃, 220-280°C, 50-100 bar)","Flash Separation","Light Ends Column","Topping Column (Pure MeOH)","Wastewater Treatment"],
     "desc":"Conventional NG-to-MeOH — 0.5-1.0 kg CO₂/kg MeOH (lifecycle). ~32 MJ NG/kg MeOH. 65-75% carbon eff."},
    {"id":"meoh_co2_h2","name":"Methanol, CO₂ hydrogenation (e-MeOH)","cat":"Chemicals","sector":"Methanol","unit":"kg MeOH","geo":"IS","db":"Literature",
     "ref":"Pérez-Fortes et al. (2016); Van-Dal & Bouallou (2013); CRI George Olah plant (2012)",
     "inputs":{"h2_pem_wind":0.19,"dac_sdac":0.0014,"grid_is":0.5,"water_supply":0.8},
     "ef":{"CO2":-0.5,"CO2_luc":0,"CH4":0.0001,"N2O":1e-6,"SO2":0.001,"NOx":0.0005,"PM25":0.0001,
           "water":0.002},
     "outputs":["methanol"],"stages":["CO₂ Source (DAC/Flue Gas Capture)","CO₂ Compression & Purification","Green H₂ Production (PEM Electrolysis)","H₂ Compression (50-80 bar)","CO₂/H₂ Mixing (stoichiometric ratio 1:3)","Catalytic Reactor (Cu/ZnO/Al₂O₃, 220-260°C, 50-80 bar)","Product Flash Separation","Recycle Compressor","Methanol-Water Distillation","Methanol Storage"],
     "desc":"e-MeOH via CO₂ + green H₂ — net negative if DAC CO₂ used. CRI Iceland plant: 4000 t/yr MeOH. Reaction: CO₂ + 3H₂ → CH₃OH + H₂O."},
    # ───────────────────── BATTERIES ─────────────────────
    {"id":"bat_nmc811","name":"Battery cell, Li-ion NMC811","cat":"Electronics","sector":"Batteries","unit":"kWh capacity","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"Chordia et al. (2024) Nat Commun; Dai et al. (2019) PMC; Peters et al. (2023) Appl Energy",
     "inputs":{"grid_cn":120,"lithium_carb":0.09,"nickel_class1":0.55,"cobalt_refined":0.06,"manganese":0.06,"graphite":0.45,"nmp_supply":0.3,"pvdf_supply":0.05,"electrolyte_supply":0.15,"copper_supply":0.35,"aluminium_supply":0.5},
     "ef":{"CO2":65,"CH4":0.025,"N2O":0.00025,"SO2":0.35,"NOx":0.12,"PM25":0.015,"PM10":0.025,"CO":0.008,"NMVOC":0.008,
           "hard_coal":120,"natural_gas":80,"crude_oil":20,"water":0.045,"Cu_w":5e-6,"Ni_w":3e-5,"Cd_w":2e-8,"Pb_w":1e-6,"COD":0.001,
           "copper_ore":0.35,"iron_ore":0.1,"bauxite":0.15},
     "outputs":["battery cell, Li-ion NMC811"],"stages":["Lithium Mining (Brine evaporation / Spodumene hard-rock)","Li₂CO₃ → LiOH Conversion","Nickel Mining (Laterite HPAL / Sulfide)","Ni Refining to Class 1","Cobalt Mining (Cu-Co, DRC/Indonesia)","Cobalt Refining","Mn Supply","Precursor Synthesis (pCAM, co-precipitation)","Cathode Active Material Sintering (CAM, 700-900°C)","Graphite Anode (natural/synthetic, coating)","Electrolyte Preparation (LiPF₆ in EC/DMC)","Electrode Coating (slot-die, NMP solvent)","Calendering","Electrode Slitting","Drying (NMP recovery)","Cell Assembly (Dry Room, <1% RH)","Electrolyte Filling","Formation Cycling (initial charge/discharge)","Aging (1-3 weeks, 45°C)","Grading & QC","Module Assembly (welding, BMS connection)","Pack Assembly (housing, cooling, BMS)"],
     "desc":"NMC811 — 59-115 kg CO₂/kWh (5th-95th percentile). Material sourcing dominates over production location. Ni + Li are top contributors."},
    {"id":"bat_lfp","name":"Battery cell, Li-ion LFP","cat":"Electronics","sector":"Batteries","unit":"kWh capacity","geo":"CN","db":"ecoinvent 3.11",
     "ref":"Chordia et al. (2024) Nat Commun; Hao et al. (2017); CATL (2023)",
     "inputs":{"grid_cn":95,"lithium_carb":0.11,"iron_phosphate":0.5,"graphite":0.5,"electrolyte_supply":0.15,"copper_supply":0.4,"aluminium_supply":0.6},
     "ef":{"CO2":54,"CH4":0.018,"N2O":0.0002,"SO2":0.22,"NOx":0.08,"PM25":0.01,"PM10":0.018,"CO":0.006,"NMVOC":0.006,
           "hard_coal":100,"natural_gas":50,"water":0.035,"Cu_w":4e-6,"COD":0.0008,
           "copper_ore":0.4,"iron_ore":0.5,"bauxite":0.2},
     "outputs":["battery cell, Li-ion LFP"],"stages":["Iron Phosphate Production","Li₂CO₃ Supply","LFP Cathode Synthesis (carbothermal reduction/hydrothermal)","Graphite Anode","Electrolyte Prep","Electrode Coating","Cell Assembly","Formation","Module/Pack"],
     "desc":"LFP — 54-69 kg CO₂/kWh. No Co/Ni. 170-190 Wh/kg. 3000-6000 cycles. Thermal runaway at ~270°C (safer than NMC)."},
    {"id":"bat_recycle_hydro","name":"Battery recycling, hydrometallurgical, NMC","cat":"Waste","sector":"Batteries","unit":"kg battery processed","geo":"GLO","db":"Literature",
     "ref":"Morin et al. (2025) Environ Sci Technol; Dai et al. (2019) PMC; Ciez & Whitacre (2019) Nat Sustain",
     "inputs":{"grid_glo":2,"h2so4_supply":0.3,"naoh_supply":0.1,"h2o2_supply":0.05,"water_supply":3},
     "ef":{"CO2":0.6,"CH4":0.0001,"N2O":2e-6,"SO2":0.004,"NOx":0.002,"PM25":0.0003,"NH3":0.0001,
           "natural_gas":2,"water":0.003,"Ni_w":5e-6,"Cu_w":3e-6,"Co_w":2e-6,"COD":0.005,"N_water":0.0002},
     "outputs":["nickel sulfate","cobalt sulfate","lithium carbonate","manganese","copper"],"stages":["Collection & Transport","Safe Discharge (brine/resistor)","Mechanical Disassembly","Shredding/Crushing","Screening & Magnetic Separation","Black Mass Recovery","Leaching (H₂SO₄ + H₂O₂, 60-80°C)","Impurity Removal (Fe, Al precipitation)","Solvent Extraction (Cyanex 272 for Co/Ni/Mn)","Selective Precipitation (CoSO₄, NiSO₄, MnSO₄)","Li₂CO₃ Crystallization (from Li-rich raffinate)","Cu Electrowinning","Wastewater Treatment"],
     "desc":"Hydrometallurgical recycling — recovers >95% of Li, Co, Ni, Mn, Cu. 0.6-2.24 kg CO₂/NMC pack. Chemical waste streams need treatment."},
    # ───────────────────── MATERIALS ─────────────────────
    {"id":"steel_bof","name":"Steel, unalloyed, BF-BOF route","cat":"Materials","sector":"Metals","unit":"kg","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; worldsteel (2021) LCI; Hasanbeigi et al. (2014) J Cleaner Prod",
     "inputs":{"iron_ore_supply":1.6,"coal_supply":0.6,"limestone_supply":0.3,"grid_glo":0.5,"water_supply":5},
     "ef":{"CO2":1.85,"CH4":0.00025,"N2O":3.5e-6,"SO2":0.0065,"NOx":0.0015,"PM25":0.0004,"PM10":0.0008,"CO":0.02,"NMVOC":0.0003,"Hg_air":1e-8,"Pb_air":5e-8,
           "hard_coal":13,"natural_gas":2,"crude_oil":0.5,"iron_ore":1.6,"limestone":0.3,"water":0.005,
           "N_water":0.00002,"Cu_w":5e-8,"Zn_w":1e-7,"Pb_w":3e-8,"Ni_w":2e-8,"COD":0.0003,"oil_w":5e-7},
     "outputs":["steel, unalloyed"],"stages":["Iron Ore Mining & Beneficiation","Coking (coal → coke, 1100°C)","Sintering (ore + flux + coke fines)","Blast Furnace (1500°C, hot metal)","Desulfurization (CaO injection)","Basic Oxygen Furnace (scrap + hot metal → steel)","Secondary Metallurgy (ladle)","Continuous Casting (slab/billet)","Hot Rolling Mill","Pickling & Oiling"],
     "desc":"Integrated BF-BOF — 1.8-2.2 t CO₂/t steel. ~75% of 1.9 Gt global production. Coke = reducing agent + heat."},
    {"id":"steel_eaf","name":"Steel, unalloyed, EAF route (scrap)","cat":"Materials","sector":"Metals","unit":"kg","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; worldsteel (2021)",
     "inputs":{"steel_scrap":1.05,"grid_glo":0.5,"electrode_supply":0.003,"lime_supply":0.05},
     "ef":{"CO2":0.4,"CH4":0.00008,"N2O":1e-6,"SO2":0.002,"NOx":0.0008,"PM25":0.0003,"PM10":0.0005,"CO":0.005,"NMVOC":0.0001,
           "hard_coal":1,"natural_gas":1.5,"water":0.002,
           "N_water":0.00001,"Zn_w":5e-8,"Pb_w":2e-8,"COD":0.0001},
     "outputs":["steel, unalloyed"],"stages":["Scrap Collection & Sorting","Scrap Charging","Electric Arc Furnace (1600°C, 400-500 kWh/t)","Oxygen Lancing","Slag Formation","Tapping","Ladle Furnace (refining)","Continuous Casting","Hot Rolling"],
     "desc":"EAF scrap — 0.3-0.8 t CO₂/t steel. ~25% of global production. Electricity is main driver."},
    {"id":"cement_opc","name":"Cement, Portland, at plant","cat":"Materials","sector":"Construction","unit":"kg","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; GCCA (2021) Getting Numbers Right; IEA (2018) Cement Roadmap",
     "inputs":{"limestone_supply":1.3,"grid_glo":0.11,"coal_supply":0.1,"water_supply":0.3},
     "ef":{"CO2":0.78,"CO2":0.78,"CH4":0.00008,"N2O":1.2e-6,"SO2":0.0012,"NOx":0.00085,"PM25":0.00018,"PM10":0.0005,"CO":0.0005,"NMVOC":0.00005,"Hg_air":5e-9,"Pb_air":3e-8,
           "hard_coal":3,"natural_gas":0.5,"crude_oil":0.2,"limestone":1.3,"water":0.001,
           "N_water":0.000005,"Cr_w":5e-9,"COD":0.00005},
     "outputs":["cement, Portland"],"stages":["Limestone Quarrying & Crushing","Clay/Shale Mining","Raw Meal Grinding (ball/vertical roller mill)","Blending Silo","Preheater (4-6 stage cyclone, 300-800°C)","Precalciner (calcination CaCO₃ → CaO + CO₂, 900°C)","Rotary Kiln (clinker formation, 1450°C)","Clinker Cooler (grate)","Clinker Storage","Cement Grinding (+ gypsum 3-5%)","Packing"],
     "desc":"OPC cement — 0.6-0.9 kg CO₂/kg. ~520 kg CO₂/t from calcination (process emissions) + ~330 kg CO₂/t from fuel. 8% global CO₂."},
    {"id":"aluminium_primary","name":"Aluminium, primary, ingot","cat":"Materials","sector":"Metals","unit":"kg","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; IAI (2021) LCI; Liu & Müller (2012) J Ind Ecol",
     "inputs":{"bauxite_supply":4.5,"grid_glo":15,"naoh_supply":0.1,"coke_supply":0.4,"cryolite_supply":0.02},
     "ef":{"CO2":7.9,"CH4":0.0015,"N2O":8.5e-6,"SO2":0.038,"NOx":0.0032,"PM25":0.0022,"PM10":0.004,"CO":0.01,"NMVOC":0.001,"HF":0.0005,"CF4":0.00004,"C2F6":0.000004,
           "hard_coal":30,"natural_gas":20,"crude_oil":5,"bauxite":4.5,"water":0.03,
           "N_water":0.00005,"Cu_w":1e-7,"Zn_w":2e-7,"As_w":5e-8,"COD":0.001},
     "outputs":["aluminium, primary"],"stages":["Bauxite Mining","Bayer Process (NaOH digestion, 180°C → alumina Al₂O₃)","Red Mud Disposal","Alumina Calcination (1000°C)","Anode Production (petroleum coke + pitch)","Hall-Héroult Electrolysis (960°C, ~15 kWh/kg Al)","Anode Effect Management (PFC emissions)","Hot Metal Treatment","Ingot Casting"],
     "desc":"Primary Al — 8-17 kg CO₂/kg depending on electricity source. Hall-Héroult ~15 kWh/kg. PFC (CF₄, C₂F₆) from anode effects."},
    # ───────────────────── TRANSPORT ─────────────────────
    {"id":"transport_lorry_euro6","name":"Transport, freight, lorry 16-32t, EURO6","cat":"Transport","sector":"Road","unit":"tkm","geo":"RER","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11 (Spielmann et al. 2007); EcoTransIT (2024); EN 16258",
     "inputs":{"diesel_supply":0.022},
     "ef":{"CO2":0.058,"CH4":7.5e-6,"N2O":9.5e-7,"SO2":3.8e-5,"NOx":2.5e-4,"PM25":8.5e-6,"PM10":2e-5,"CO":8e-5,"NMVOC":1e-5,
           "crude_oil":0.9,"water":0.00001},
     "outputs":["transport service"],"stages":["Vehicle Manufacturing (15yr/750,000km)","Diesel Production (refinery)","Driving (fuel combustion)","Tire & Brake Wear (PM)","Road Infrastructure (construction, maintenance)","Vehicle Maintenance","Vehicle End-of-Life"],
     "desc":"Euro 6 lorry 16-32t — ~62 g CO₂/tkm (WTW). 50% avg load. Road infra contributes ~10% of total."},
    {"id":"transport_ship_container","name":"Transport, freight, container ship","cat":"Transport","sector":"Sea","unit":"tkm","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11 (Notten et al. 2018); IMO (2020) 4th GHG Study",
     "inputs":{"hfo_supply":0.003},
     "ef":{"CO2":0.008,"CH4":1.5e-6,"N2O":1.1e-7,"SO2":8.5e-5,"NOx":8.5e-5,"PM25":8e-6,"PM10":1.2e-5,"CO":5e-6,"NMVOC":3e-6,
           "crude_oil":0.14,"water":0.000001},
     "outputs":["transport service"],"stages":["Ship Construction (25yr)","Fuel Production (VLSFO/HFO)","Sailing (main engine, slow steaming)","Port Operations","Ship Maintenance (dry dock)","Ballast Water Treatment","Ship End-of-Life (recycling)"],
     "desc":"Container ship — ~10 g CO₂/tkm. Most carbon-efficient freight mode. IMO 2020 sulfur cap: 0.5% S."},
    {"id":"transport_air_freight","name":"Transport, freight, aircraft","cat":"Transport","sector":"Air","unit":"tkm","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11 (Notten et al. 2018); STREAM (2020)",
     "inputs":{"jet_fuel_supply":0.5},
     "ef":{"CO2":0.602,"CH4":3.2e-5,"N2O":5.2e-6,"SO2":2.1e-4,"NOx":8.1e-4,"PM25":1.5e-5,"PM10":2e-5,"CO":2e-4,"NMVOC":5e-5,
           "crude_oil":9.5,"water":0.00001},
     "outputs":["transport service"],"stages":["Aircraft Manufacturing","Jet Fuel Production (Jet A-1)","Flight Operation (climb, cruise, descent)","Airport Infrastructure","Aircraft Maintenance","Aircraft End-of-Life"],
     "desc":"Air freight — ~620 g CO₂/tkm. 50x higher than sea. High-altitude NOx → additional radiative forcing (×1.7-2.7 multiplier debated)."},
    {"id":"transport_rail_electric","name":"Transport, freight, rail, electric","cat":"Transport","sector":"Rail","unit":"tkm","geo":"RER","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; CE Delft STREAM (2020); Spielmann & Scholz (2005)",
     "inputs":{"grid_rer":0.04},
     "ef":{"CO2":0.012,"CH4":2.8e-6,"N2O":3e-7,"SO2":4.5e-5,"NOx":3.2e-5,"PM25":5e-6,"PM10":1e-5,
           "natural_gas":0.05,"hard_coal":0.03,"water":0.000003},
     "outputs":["transport service"],"stages":["Locomotive Manufacturing","Rail Infrastructure (construction, ballast, sleepers)","Catenary (overhead wire)","Electricity Supply","Train Operation","Maintenance","Infrastructure Maintenance"],
     "desc":"Electric rail freight — ~22 g CO₂/tkm (EU grid). GHG depends heavily on electricity source."},
    # ───────────────────── FOOD & AGRICULTURE ─────────────────────
    {"id":"beef_herd","name":"Beef, from beef cattle, at farm gate","cat":"Food","sector":"Agriculture","unit":"kg carcass weight","geo":"GLO","db":"Poore & Nemecek (2018)",
     "ref":"Poore & Nemecek (2018) Science 360(6392); FAO FAOSTAT (2022); GLEAM",
     "inputs":{"feed_production":25,"pasture_land":35},
     "ef":{"CO2":7.2,"CO2_luc":15,"CH4":1.2,"CH4_bio":2.3,"N2O":0.148,"SO2":0.01,"NOx":0.006,"NH3":0.15,"PM25":0.005,"PM10":0.01,"NMVOC":0.002,
           "land":35,"water":1.45,"N_water":0.095,"PO4":0.005,"P_water":0.025,"NO3":0.3,"NH4":0.02,"COD":0.05},
     "outputs":["beef, carcass weight"],"stages":["Pasture Management (liming, seeding, fencing)","Feed Crop Production (soy, maize, wheat)","Feed Processing (milling, mixing)","Calf Rearing","Cow-Calf Operation","Backgrounding","Feedlot Finishing","Enteric Fermentation (CH₄ ~3.5 kg/kg beef)","Manure Management (CH₄ + N₂O)","Slaughter","Chilling","Transport to Retail"],
     "desc":"Beef (beef herd) — mean 60 kg CO₂-eq/kg (Poore: 9-105 range). Enteric CH₄ ~50% of GWP. Land use change adds 15 kg CO₂/kg mean."},
    {"id":"chicken_broiler","name":"Chicken, broiler, at farm gate","cat":"Food","sector":"Agriculture","unit":"kg carcass weight","geo":"GLO","db":"Poore & Nemecek (2018)",
     "ref":"Poore & Nemecek (2018) Science; FAO FAOSTAT (2022); Agri-footprint 5.0",
     "inputs":{"feed_production":3.5},
     "ef":{"CO2":2.55,"CO2_luc":1.5,"CH4":0.028,"CH4_bio":0.005,"N2O":0.009,"SO2":0.004,"NOx":0.003,"NH3":0.05,"PM25":0.003,"PM10":0.005,
           "land":5,"water":0.3,"N_water":0.01,"PO4":0.001,"P_water":0.004,"NO3":0.05,"NH4":0.008,"COD":0.02},
     "outputs":["chicken, carcass weight"],"stages":["Feed Production (soy, maize, wheat)","Broiler Rearing (35-42 days)","Heating/Ventilation","Manure Management","Litter Management","Slaughter","Chilling"],
     "desc":"Broiler chicken — mean 6.9 kg CO₂-eq/kg. Feed conversion ratio ~1.6-2.0 (best livestock). 35-42 day cycle."},
    {"id":"milk_cow","name":"Milk, from cow, at farm gate","cat":"Food","sector":"Agriculture","unit":"kg FPCM","geo":"GLO","db":"Poore & Nemecek (2018)",
     "ref":"Poore & Nemecek (2018) Science; FAO (2010) GHG Emissions Dairy; FAOSTAT (2022)",
     "inputs":{"feed_production":1.2,"pasture_land":1},
     "ef":{"CO2":0.7,"CH4":0.025,"CH4_bio":0.043,"N2O":0.01,"SO2":0.0008,"NOx":0.0006,"NH3":0.02,"PM25":0.0005,
           "land":1,"water":0.25,"N_water":0.008,"PO4":0.0003,"P_water":0.002,"NO3":0.04,"NH4":0.005},
     "outputs":["milk, fat and protein corrected"],"stages":["Pasture Management","Feed Production","Dairy Cow Rearing","Milking (2-3x daily)","Milk Cooling & Storage","Manure Management","Enteric Fermentation"],
     "desc":"Dairy milk — mean 3.2 kg CO₂-eq/kg FPCM (Poore). FAOSTAT: 1.0 kg/kg farm-gate. Enteric CH₄ dominant."},
    {"id":"wheat_grain","name":"Wheat grain, at farm gate","cat":"Food","sector":"Agriculture","unit":"kg","geo":"GLO","db":"Agri-footprint 5.0",
     "ref":"Agri-footprint 5.0; Poore & Nemecek (2018); IPCC (2006) EF",
     "inputs":{"n_fertilizer":0.015,"p_fertilizer":0.005,"k_fertilizer":0.005,"diesel_farm":0.003,"pesticide":0.0001},
     "ef":{"CO2":0.325,"CH4":4.5e-6,"N2O":0.0012,"SO2":0.00022,"NOx":0.00015,"NH3":0.005,"PM25":0.00003,"PM10":0.0001,
           "crude_oil":0.4,"natural_gas":0.3,"water":0.13,"land":0.8,
           "N_water":0.003,"PO4":0.00005,"P_water":0.0008,"NO3":0.015,"NH4":0.001},
     "outputs":["wheat grain"],"stages":["Soil Preparation (ploughing, harrowing)","Seeding","N/P/K Fertilization","Pesticide Application","Irrigation (where applicable)","Harvest (combine)","Drying","Storage","Transport to Mill"],
     "desc":"Wheat — 0.2-1.4 kg CO₂-eq/kg. N₂O from soil (IPCC default EF = 1% of N applied). Varies hugely by region."},
    {"id":"rice_paddy","name":"Rice, paddy, at farm gate","cat":"Food","sector":"Agriculture","unit":"kg","geo":"GLO","db":"Agri-footprint 5.0",
     "ref":"Agri-footprint 5.0; Poore & Nemecek (2018); IPCC (2006) CH₄ from rice",
     "inputs":{"n_fertilizer":0.012,"diesel_farm":0.002},
     "ef":{"CO2":0.42,"CH4":0.085,"CH4_bio":0.02,"N2O":0.003,"SO2":0.0003,"NOx":0.0003,"NH3":0.003,"PM25":0.00004,
           "water":1.4,"land":0.5,"natural_gas":0.15,"crude_oil":0.1,
           "N_water":0.002,"PO4":0.00003,"P_water":0.0009,"NO3":0.01},
     "outputs":["rice, paddy"],"stages":["Seedling Nursery","Paddy Field Preparation","Flooding/Irrigation","Transplanting/Direct Seeding","Fertilization","Flooded Anaerobic Period (CH₄ production)","Mid-season Drainage","Harvest","Drying","Milling"],
     "desc":"Paddy rice — ~4 kg CO₂-eq/kg. Flooded fields → anaerobic CH₄ (IPCC CH₄ baseline 1.3 kg CH₄/ha/day). Water intensive: ~1400 L/kg."},
    # ───────────────────── WASTE TREATMENT ─────────────────────
    {"id":"landfill_msw","name":"Landfill of municipal solid waste","cat":"Waste","sector":"Waste Treatment","unit":"kg","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; IPCC (2006) Vol 5 Waste; Manfredi et al. (2009)",
     "inputs":{},
     "ef":{"CO2":0.025,"CO2_bio":0.2,"CH4":0.022,"CH4_bio":0.003,"N2O":2.5e-6,"SO2":2.5e-5,"NOx":3.5e-5,"NH3":5e-5,"H2S":3e-5,"NMVOC":5e-5,
           "water":0.00001,"N_water":0.0005,"NH4":0.0003,"COD":0.002,"BOD":0.001,"Pb_w":5e-7,"Cd_w":1e-8,"Hg_w":5e-9,"Cu_w":2e-6,"Zn_w":5e-6,"As_w":1e-7,"Cr_w":3e-7},
     "outputs":["waste, disposed"],"stages":["Waste Collection & Transport","Weighing & Registration","Cell Construction (liner, drainage)","Waste Placement & Compaction","Daily Cover","Landfill Gas Collection (50-75% capture)","LFG Flaring or Energy Recovery","Leachate Collection","Leachate Treatment (biological/chemical)","Post-closure Monitoring (30yr+)"],
     "desc":"MSW landfill — 0.71 kg CO₂-eq/kg (CH₄ dominant). Biodegradable fraction → CH₄ over 20-50yr. LFG collection typically 50-75%."},
    {"id":"incineration_msw","name":"Incineration of MSW, with energy recovery","cat":"Waste","sector":"Waste Treatment","unit":"kg","geo":"RER","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Astrup et al. (2015) Waste Manag; BREF WI (2019)",
     "inputs":{"grid_rer":-0.3,"heat_credit":-1.5},
     "ef":{"CO2":0.6,"CO2_bio":0.35,"CH4":8.5e-6,"N2O":4e-6,"SO2":0.00025,"NOx":0.00065,"PM25":5e-6,"PM10":1e-5,"HCl":0.00005,"HF":5e-6,"CO":0.0001,"NMVOC":5e-6,"Hg_air":5e-8,"Cd_w":5e-8,"Pb_air":1e-7,
           "water":0.00005,"N_water":0.00005,"COD":0.0001,"Cu_w":5e-7,"Zn_w":2e-6,"Pb_w":1e-7},
     "outputs":["waste, incinerated","electricity","heat","bottom ash","fly ash (hazardous)"],"stages":["Waste Reception & Bunker","Grate Furnace (850-1100°C, >2s residence)","Heat Recovery (HRSG → steam)","Steam Turbine / District Heating","Flue Gas Treatment: SNCR/SCR (NOx)","Flue Gas Treatment: Activated Carbon (dioxins, Hg)","Flue Gas Treatment: Dry/Semi-dry Scrubbing (SO₂, HCl)","Flue Gas Treatment: Fabric Filter (PM)","Bottom Ash Treatment (metals recovery)","Fly Ash Stabilization (cement/vitrification → hazardous waste)","Stack"],
     "desc":"WtE incineration — 0.95 kg CO₂-eq/kg gross. Energy recovery offsets ~0.3 kWh elec + 1.5 MJ heat per kg waste. BREF BAT limits."},
    {"id":"ww_treatment","name":"Wastewater treatment, municipal, activated sludge","cat":"Waste","sector":"Water Treatment","unit":"m³","geo":"RER","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; Hospido et al. (2008) J Ind Ecol; Yoshida et al. (2014)",
     "inputs":{"grid_rer":0.4,"fecl3_supply":0.05,"polymer_supply":0.005},
     "ef":{"CO2":0.25,"CO2_bio":0.03,"CH4":0.008,"CH4_bio":0.001,"N2O":0.003,"SO2":0.0004,"NOx":0.0003,"NH3":0.0005,"PM25":0.00002,
           "natural_gas":0.5,"water":0,"N_water":0.012,"PO4":0.0001,"P_water":0.001,"NH4":0.003,"NO3":0.005,"COD":0.03,"BOD":0.005,
           "Cu_w":5e-6,"Zn_w":1e-5,"Pb_w":5e-7,"Ni_w":3e-6,"Cd_w":5e-8,"Hg_w":1e-8},
     "outputs":["treated effluent","sludge"],"stages":["Screening & Grit Removal","Primary Sedimentation","Aeration Basin (Activated Sludge, BOD removal)","Nitrification (NH₄⁺ → NO₃⁻)","Denitrification (NO₃⁻ → N₂)","Secondary Clarifier","Phosphorus Removal (chemical/biological)","Tertiary Filtration","UV Disinfection","Sludge Thickening","Anaerobic Digestion (biogas)","Sludge Dewatering (centrifuge/belt press)","Sludge Disposal (agriculture/incineration/landfill)"],
     "desc":"Municipal WWTP (activated sludge + nutrient removal) — ~1.0 kg CO₂-eq/m³. N₂O from nitrification/denitrification is significant (0.5-3% of N load). Electricity: 0.3-0.6 kWh/m³."},
    # ───────────────────── PACKAGING ─────────────────────
    {"id":"pet_bottle","name":"PET bottle, 1 liter, stretch blow moulded","cat":"Materials","sector":"Packaging","unit":"unit (28g)","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; PlasticsEurope (2014)",
     "inputs":{"pet_granulate":0.028,"grid_glo":0.08},
     "ef":{"CO2":0.07,"CH4":0.00001,"N2O":1e-7,"SO2":0.00013,"NOx":0.00006,"PM25":0.00001,"NMVOC":0.00005,
           "crude_oil":1.7,"natural_gas":0.2,"water":0.0001},
     "outputs":["PET bottle, 1L"],"stages":["PET Granulate Production","Preform Injection Moulding","Stretch Blow Moulding","Quality Control"],
     "desc":"1L PET bottle (28g) — ~70 g CO₂/bottle. Dominated by PET resin production."},
    {"id":"glass_bottle","name":"Glass bottle, 750 mL, at plant","cat":"Materials","sector":"Packaging","unit":"unit (350g)","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; FEVE (2016) Glass Recycling",
     "inputs":{"glass_supply":0.35,"grid_glo":0.2},
     "ef":{"CO2":0.3,"CH4":0.00003,"N2O":3e-7,"SO2":0.0004,"NOx":0.0003,"PM25":0.00005,"PM10":0.00008,
           "natural_gas":2,"sand":0.2,"water":0.0003},
     "outputs":["glass bottle, 750mL"],"stages":["Raw Material Supply (silica sand, soda ash, limestone)","Batch Mixing","Glass Melting Furnace (1500-1600°C)","IS Machine (forming)","Annealing Lehr","Inspection & Packing"],
     "desc":"750mL glass bottle (350g) — ~300 g CO₂/bottle. 60-90% cullet (recycled glass) reduces energy by 2.5% per 10% cullet."},
    {"id":"cardboard_box","name":"Corrugated cardboard box, at plant","cat":"Materials","sector":"Packaging","unit":"kg","geo":"GLO","db":"ecoinvent 3.11",
     "ref":"ecoinvent v3.11; CEPI (2017)",
     "inputs":{"kraft_paper":0.6,"recycled_paper":0.4,"grid_glo":0.5,"steam_ng":2},
     "ef":{"CO2":0.65,"CO2_bio":0.3,"CH4":0.0005,"N2O":3e-6,"SO2":0.002,"NOx":0.001,"PM25":0.0002,"PM10":0.0003,"CO":0.0003,
           "wood":0.6,"natural_gas":3,"water":0.005,"N_water":0.0001,"COD":0.002,"BOD":0.0005},
     "outputs":["corrugated cardboard"],"stages":["Wood Pulping (kraft process)","Waste Paper Recycling","Corrugating Medium Production","Linerboard Production","Corrugator (fluting + liner)","Box Making (printing, cutting, folding)"],
     "desc":"Corrugated box — 0.65 kg fossil CO₂/kg + 0.3 biogenic. 40-100% recycled content typical."},
]

# ═══════════════════════════════════════════════════════════════
# IMPACT METHODS
# ═══════════════════════════════════════════════════════════════
METHODS = {
    "recipe_h":{"name":"ReCiPe 2016 Midpoint (H)","cats":["GWP","AP","EP-fw","EP-mar","PM","POCP","WC","ADF"],
        "cf_map":{"GWP":CF_GWP,"AP":CF_AP,"EP-fw":CF_EP,"EP-mar":CF_EP_M,"PM":CF_PM,"POCP":CF_POCP},
        "units":{"GWP":"kg CO₂-eq","AP":"kg SO₂-eq","EP-fw":"kg P-eq","EP-mar":"kg N-eq","PM":"kg PM2.5-eq","POCP":"kg NMVOC-eq","WC":"m³","ADF":"MJ"},
        "ref":"Huijbregts et al. (2017) ReCiPe2016. RIVM Report 2016-0104."},
    "ipcc_ar6":{"name":"IPCC AR6 GWP100","cats":["GWP"],
        "cf_map":{"GWP":CF_GWP},"units":{"GWP":"kg CO₂-eq"},
        "ref":"IPCC (2021) AR6, Chapter 7 Supplementary Material."},
    "cml_ia":{"name":"CML-IA Baseline 2016","cats":["GWP","AP","EP-fw"],
        "cf_map":{"GWP":CF_GWP,"AP":CF_AP,"EP-fw":CF_EP},"units":{"GWP":"kg CO₂-eq","AP":"kg SO₂-eq","EP-fw":"kg PO₄-eq"},
        "ref":"CML, Leiden University, v4.8. Guinée et al. (2002)."},
    "ef31":{"name":"EF 3.1 (EU PEF)","cats":["GWP","AP","EP-fw","PM","WC"],
        "cf_map":{"GWP":CF_GWP,"AP":CF_AP,"EP-fw":CF_EP,"PM":CF_PM},"units":{"GWP":"kg CO₂-eq","AP":"mol H⁺-eq","EP-fw":"kg P-eq","PM":"disease incid.","WC":"m³"},
        "ref":"JRC Technical Report. EU PEF method."},
}

# ═══════════════════════════════════════════════════════════════


AU_ELEC_FACTORS = {
    # State/Grid: {scope2, scope3, total, notes, year, ref}
    "NSW_ACT": {
        "name": "New South Wales / ACT",
        "scope2": 0.66, "scope3": 0.08, "total": 0.74,
        "notes": "NEM grid. Coal + growing solar/wind share.",
        "year": "2024 (FY2023-24)", "grid": "NEM",
        "ref": "DCCEEW NGA Factors 2024, Table 1"
    },
    "VIC": {
        "name": "Victoria",
        "scope2": 0.79, "scope3": 0.12, "total": 0.91,
        "notes": "NEM grid. Dominated by Latrobe Valley brown coal (Loy Yang, Yallourn). Highest in NEM.",
        "year": "2024 (FY2023-24)", "grid": "NEM",
        "ref": "DCCEEW NGA Factors 2024, Table 1"
    },
    "QLD": {
        "name": "Queensland",
        "scope2": 0.73, "scope3": 0.08, "total": 0.81,
        "notes": "NEM grid. Black coal dominated. Growing solar/wind.",
        "year": "2024 (FY2023-24)", "grid": "NEM",
        "ref": "DCCEEW NGA Factors 2024, Table 1"
    },
    "SA": {
        "name": "South Australia",
        "scope2": 0.19, "scope3": 0.06, "total": 0.25,
        "notes": "NEM grid. ~72% renewables (wind+solar). Lowest NEM state. Imports from VIC via Heywood.",
        "year": "2024 (FY2023-24)", "grid": "NEM",
        "ref": "DCCEEW NGA Factors 2024, Table 1"
    },
    "TAS": {
        "name": "Tasmania",
        "scope2": 0.13, "scope3": 0.03, "total": 0.16,
        "notes": "NEM grid. ~99% hydro. Uses VIC factors when importing via Basslink. Methane from hydro dams included.",
        "year": "2024 (FY2023-24)", "grid": "NEM",
        "ref": "DCCEEW NGA Factors 2024, Table 1 (note: DCCEEW suggests VIC factors for TAS)"
    },
    "WA_SWIS": {
        "name": "Western Australia (SWIS)",
        "scope2": 0.51, "scope3": 0.07, "total": 0.58,
        "notes": "South West Interconnected System. Gas + coal + growing renewables.",
        "year": "2024 (FY2023-24)", "grid": "SWIS",
        "ref": "DCCEEW NGA Factors 2024, Table 1"
    },
    "WA_NWIS": {
        "name": "Western Australia (NWIS)",
        "scope2": 0.58, "scope3": 0.08, "total": 0.66,
        "notes": "North West Interconnected System. Gas dominated (Pilbara).",
        "year": "2024 (FY2023-24)", "grid": "NWIS",
        "ref": "DCCEEW NGA Factors 2024, Table 1"
    },
    "NT_DKIS": {
        "name": "Northern Territory (DKIS)",
        "scope2": 0.54, "scope3": 0.07, "total": 0.61,
        "notes": "Darwin-Katherine Interconnected System. Gas dominated. DCCEEW suggests WA factors.",
        "year": "2024 (FY2023-24)", "grid": "DKIS",
        "ref": "DCCEEW NGA Factors 2024, Table 1"
    },
    "AU_NEM_AVG": {
        "name": "Australia NEM Average",
        "scope2": 0.63, "scope3": 0.09, "total": 0.72,
        "notes": "Weighted average across all NEM states.",
        "year": "2024 (FY2023-24)", "grid": "NEM",
        "ref": "DCCEEW NGA Factors 2024, derived from Table 1"
    },
    "AU_NATIONAL": {
        "name": "Australia National Average",
        "scope2": 0.60, "scope3": 0.09, "total": 0.69,
        "notes": "All grids combined. Declining trend (~4% per year).",
        "year": "2024 (FY2023-24)", "grid": "All",
        "ref": "DCCEEW NGA Factors 2024"
    },
}

# ═══════════════════════════════════════════════════════════════
# MODULE 1B: AUSTRALIAN NGA 2024 FUEL FACTORS
# Source: DCCEEW National Greenhouse Accounts Factors 2024
# ═══════════════════════════════════════════════════════════════
AU_FUEL_FACTORS = {
    # Stationary Energy — kg CO₂-e per GJ (scope 1: CO₂ + CH₄ + N₂O combined)
    "natural_gas_stationary": {
        "name": "Natural Gas (stationary)", "unit": "GJ",
        "scope1_co2": 51.2, "scope1_ch4": 0.03, "scope1_n2o": 0.03,
        "scope1_total": 51.26, "scope3": 8.6,
        "energy_content": "0.03723 GJ/m³",
        "ref": "DCCEEW NGA 2024, Table 3 & 4"
    },
    "black_coal_stationary": {
        "name": "Black Coal (stationary)", "unit": "GJ",
        "scope1_co2": 88.2, "scope1_ch4": 0.03, "scope1_n2o": 0.04,
        "scope1_total": 88.27, "scope3": 5.3,
        "energy_content": "27.0 GJ/t",
        "ref": "DCCEEW NGA 2024, Table 3 & 4"
    },
    "brown_coal_stationary": {
        "name": "Brown Coal / Lignite (stationary)", "unit": "GJ",
        "scope1_co2": 93.0, "scope1_ch4": 0.01, "scope1_n2o": 0.04,
        "scope1_total": 93.05, "scope3": 3.9,
        "energy_content": "10.2 GJ/t",
        "ref": "DCCEEW NGA 2024, Table 3 & 4"
    },
    "lpg_stationary": {
        "name": "LPG (stationary)", "unit": "GJ",
        "scope1_co2": 60.2, "scope1_ch4": 0.05, "scope1_n2o": 0.18,
        "scope1_total": 60.43, "scope3": 5.8,
        "energy_content": "25.7 GJ/kL",
        "ref": "DCCEEW NGA 2024, Table 3 & 4"
    },
    "diesel_stationary": {
        "name": "Diesel Oil (stationary)", "unit": "GJ",
        "scope1_co2": 69.2, "scope1_ch4": 0.01, "scope1_n2o": 0.08,
        "scope1_total": 69.29, "scope3": 6.5,
        "energy_content": "38.6 GJ/kL",
        "ref": "DCCEEW NGA 2024, Table 6 & 5"
    },
    # Transport fuels — kg CO₂-e per GJ
    "petrol_transport": {
        "name": "Petrol (transport)", "unit": "GJ",
        "scope1_co2": 66.7, "scope1_ch4": 0.22, "scope1_n2o": 0.51,
        "scope1_total": 67.43, "scope3": 6.7,
        "energy_content": "34.2 GJ/kL",
        "ref": "DCCEEW NGA 2024, Table 7 & 8"
    },
    "diesel_transport": {
        "name": "Diesel (transport)", "unit": "GJ",
        "scope1_co2": 69.2, "scope1_ch4": 0.06, "scope1_n2o": 1.49,
        "scope1_total": 70.75, "scope3": 6.5,
        "energy_content": "38.6 GJ/kL",
        "ref": "DCCEEW NGA 2024, Table 7 & 8"
    },
    "jet_kerosene": {
        "name": "Jet Kerosene (aviation)", "unit": "GJ",
        "scope1_co2": 68.4, "scope1_ch4": 0.01, "scope1_n2o": 0.31,
        "scope1_total": 68.72, "scope3": 6.0,
        "energy_content": "36.8 GJ/kL",
        "ref": "DCCEEW NGA 2024, Table 7"
    },
    "biodiesel": {
        "name": "Biodiesel", "unit": "GJ",
        "scope1_co2": 0, "scope1_ch4": 0.06, "scope1_n2o": 1.49,
        "scope1_total": 1.55, "scope3": 1.2,
        "energy_content": "34.6 GJ/kL",
        "ref": "DCCEEW NGA 2024 (biogenic CO₂ excluded from scope 1)"
    },
    # Waste — kg CO₂-e per tonne
    "msw_landfill": {
        "name": "Municipal Solid Waste (landfill)", "unit": "tonne",
        "scope1_total": 1200, "scope3": 0,
        "notes": "Highly variable. Depends on waste composition and LFG capture.",
        "ref": "DCCEEW NGA 2024, Table 17 (waste sector); EPA Victoria (2012)"
    },
    "paper_landfill": {
        "name": "Paper/Cardboard (landfill)", "unit": "tonne",
        "scope1_total": 1200, "scope3": 0,
        "ref": "DCCEEW NGA 2024; EPA Victoria (2012)"
    },
    "food_landfill": {
        "name": "Food Waste (landfill)", "unit": "tonne",
        "scope1_total": 1400, "scope3": 0,
        "ref": "DCCEEW NGA 2024; EPA Victoria (2012)"
    },
    "wood_landfill": {
        "name": "Wood/Timber (landfill)", "unit": "tonne",
        "scope1_total": 800, "scope3": 0,
        "ref": "DCCEEW NGA 2024"
    },
    # Water — kg CO₂-e per kL
    "water_supply": {
        "name": "Mains Water Supply", "unit": "kL",
        "scope3": 1.3,
        "notes": "Pumping + treatment energy. Varies by utility.",
        "ref": "Water Services Association of Australia (WSAA 2022)"
    },
    "wastewater_treatment": {
        "name": "Wastewater Treatment", "unit": "kL",
        "scope1_total": 0.55, "scope3": 0.3,
        "ref": "WSAA (2022); EPA Victoria (2012)"
    },
}


# ═══════════════════════════════════════════════════════════════
# MODULE 2: PEDIGREE MATRIX (Weidema & Wesnaes 1996)
# Source: As per user's Image 1
# ═══════════════════════════════════════════════════════════════
PEDIGREE_MATRIX = {
    "dimensions": ["Reliability", "Completeness", "Temporal", "Geographical", "Technological"],
    "weights": [0.30, 0.25, 0.15, 0.10, 0.20],
    "scores": {
        5: {
            "Reliability": "Measured, verified data",
            "Completeness": "Representative data from all relevant sites over a sufficient period",
            "Temporal": "Current data",
            "Geographical": "Data from the study area",
            "Technological": "Identical to the actual production technology"
        },
        4: {
            "Reliability": "Verified (partly assumed) or unverified measured data",
            "Completeness": "Representative data from >50% of sites over a sufficient period",
            "Temporal": "Within 2 years",
            "Geographical": "Data from a larger region including the study area",
            "Technological": "Same product, similar technology"
        },
        3: {
            "Reliability": "Calculated value using a reasonable method",
            "Completeness": "Data from <50% of sites or from >50% but over a short period",
            "Temporal": "2-4 years",
            "Geographical": "Data from a region with similar conditions",
            "Technological": "Data from a related process or material"
        },
        2: {
            "Reliability": "Estimated value based on partial assumptions",
            "Completeness": "Data from a single site or multiple sites over a very short period",
            "Temporal": "4-6 years",
            "Geographical": "Data from a region with slightly similar conditions",
            "Technological": "Data from a related process at laboratory scale"
        },
        1: {
            "Reliability": "Non-qualifying estimate",
            "Completeness": "Unknown representativeness; very limited data",
            "Temporal": "Unknown or >6 years",
            "Geographical": "Data from an unknown or different region",
            "Technological": "Different technology"
        }
    },
    "ref": "Weidema B.P. & Wesnæs M.S. (1996) Data quality management for life cycle inventories. J Cleaner Prod 4(3-4):167-174."
}

def calculate_dqi(scores):
    """Calculate weighted Data Quality Indicator from pedigree scores.
    scores: dict of {dimension: score(1-5)}
    Returns: weighted DQI (1=worst, 5=best)
    """
    w = dict(zip(PEDIGREE_MATRIX["dimensions"], PEDIGREE_MATRIX["weights"]))
    total = sum(scores.get(dim, 3) * w.get(dim, 0) for dim in PEDIGREE_MATRIX["dimensions"])
    return round(total, 2)

def dqi_to_uncertainty(dqi):
    """Convert DQI to approximate geometric standard deviation (GSD²) per ecoinvent.
    Based on: Frischknecht et al. (2007) ecoinvent overview.
    """
    # Approximate mapping: DQI 5→GSD²=1.02, 4→1.05, 3→1.1, 2→1.2, 1→1.5
    if dqi >= 4.5: return 1.02
    if dqi >= 3.5: return 1.05
    if dqi >= 2.5: return 1.10
    if dqi >= 1.5: return 1.20
    return 1.50


# ═══════════════════════════════════════════════════════════════
# MODULE 3: ADDITIONAL LCIA METHODS
# ═══════════════════════════════════════════════════════════════
LCIA_METHODS_EXTENDED = {
    "ef_v103": {
        "name": "EF Method (adapted) V1.03",
        "version": "V1.03", "scope": "Global (2010)", "with_tox": True,
        "categories": [
            {"id": "cc_total", "name": "Climate change, total", "unit": "kg CO₂-eq", "cf_key": "GWP"},
            {"id": "cc_fossil", "name": "Climate change, fossil", "unit": "kg CO₂-eq", "cf_key": "GWP"},
            {"id": "cc_bio", "name": "Climate change, biogenic", "unit": "kg CO₂-eq"},
            {"id": "cc_luc", "name": "Climate change, land use change", "unit": "kg CO₂-eq"},
            {"id": "od", "name": "Ozone depletion", "unit": "kg CFC-11-eq"},
            {"id": "ir", "name": "Ionising radiation", "unit": "kBq U235-eq"},
            {"id": "pof", "name": "Photochemical ozone formation", "unit": "kg NMVOC-eq", "cf_key": "POCP"},
            {"id": "pm", "name": "Particulate matter", "unit": "disease incidence", "cf_key": "PM"},
            {"id": "ht_nc", "name": "Human toxicity, non-cancer", "unit": "CTUh"},
            {"id": "ht_c", "name": "Human toxicity, cancer", "unit": "CTUh"},
            {"id": "ac", "name": "Acidification", "unit": "mol H⁺-eq", "cf_key": "AP"},
            {"id": "eu_fw", "name": "Eutrophication, freshwater", "unit": "kg P-eq", "cf_key": "EP"},
            {"id": "eu_mar", "name": "Eutrophication, marine", "unit": "kg N-eq"},
            {"id": "eu_terr", "name": "Eutrophication, terrestrial", "unit": "mol N-eq"},
            {"id": "et_fw", "name": "Ecotoxicity, freshwater", "unit": "CTUe"},
            {"id": "lu", "name": "Land use", "unit": "pt"},
            {"id": "wu", "name": "Water use", "unit": "m³ world-eq", "cf_key": "WC"},
            {"id": "ru_mm", "name": "Resource use, minerals and metals", "unit": "kg Sb-eq"},
            {"id": "ru_ff", "name": "Resource use, fossils", "unit": "MJ", "cf_key": "ADF"},
        ],
        "ref": "European Commission JRC (2018). Product Environmental Footprint."
    },
    "impact2002_v215": {
        "name": "IMPACT 2002+ V2.15",
        "version": "V2.15", "scope": "Global",
        "categories": [
            {"id": "cc", "name": "Global warming", "unit": "kg CO₂-eq", "cf_key": "GWP"},
            {"id": "hh_c", "name": "Human toxicity (carcinogens)", "unit": "kg C₂H₃Cl-eq"},
            {"id": "hh_nc", "name": "Human toxicity (non-carcinogens)", "unit": "kg C₂H₃Cl-eq"},
            {"id": "ri", "name": "Respiratory inorganics", "unit": "kg PM2.5-eq", "cf_key": "PM"},
            {"id": "ir", "name": "Ionizing radiation", "unit": "Bq C-14-eq"},
            {"id": "od", "name": "Ozone layer depletion", "unit": "kg CFC-11-eq"},
            {"id": "ro", "name": "Respiratory organics", "unit": "kg C₂H₄-eq"},
            {"id": "ae", "name": "Aquatic ecotoxicity", "unit": "kg TEG water"},
            {"id": "te", "name": "Terrestrial ecotoxicity", "unit": "kg TEG soil"},
            {"id": "aa", "name": "Aquatic acidification", "unit": "kg SO₂-eq", "cf_key": "AP"},
            {"id": "lo", "name": "Land occupation", "unit": "m²org.arable"},
            {"id": "aeu", "name": "Aquatic eutrophication", "unit": "kg PO₄-eq", "cf_key": "EP"},
            {"id": "nre", "name": "Non-renewable energy", "unit": "MJ primary", "cf_key": "ADF"},
            {"id": "me", "name": "Mineral extraction", "unit": "MJ surplus"},
        ],
        "damage_categories": [
            {"id": "hh", "name": "Human Health", "unit": "DALY"},
            {"id": "eq", "name": "Ecosystem Quality", "unit": "PDF·m²·yr"},
            {"id": "ccda", "name": "Climate Change", "unit": "kg CO₂-eq"},
            {"id": "res", "name": "Resources", "unit": "MJ primary"},
        ],
        "ref": "Jolliet et al. (2003) IMPACT 2002+. Int J LCA 8(6):324-330."
    },
    "cml2001_nl2016": {
        "name": "CML 2001 (all) V2.05 / Netherlands, 2016",
        "version": "V2.05", "normalization": "Netherlands, 2016",
        "categories": [
            {"id": "gwp100", "name": "Global warming (GWP100a)", "unit": "kg CO₂-eq", "cf_key": "GWP"},
            {"id": "odp", "name": "Ozone layer depletion (ODP steady-state)", "unit": "kg CFC-11-eq"},
            {"id": "htp", "name": "Human toxicity", "unit": "kg 1,4-DB-eq"},
            {"id": "faetp", "name": "Freshwater aquatic ecotoxicity", "unit": "kg 1,4-DB-eq"},
            {"id": "maetp", "name": "Marine aquatic ecotoxicity", "unit": "kg 1,4-DB-eq"},
            {"id": "tetp", "name": "Terrestrial ecotoxicity", "unit": "kg 1,4-DB-eq"},
            {"id": "pocp", "name": "Photochemical oxidation", "unit": "kg C₂H₄-eq", "cf_key": "POCP"},
            {"id": "ap", "name": "Acidification", "unit": "kg SO₂-eq", "cf_key": "AP"},
            {"id": "ep", "name": "Eutrophication", "unit": "kg PO₄³⁻-eq", "cf_key": "EP"},
            {"id": "adp_elements", "name": "Abiotic depletion (elements)", "unit": "kg Sb-eq"},
            {"id": "adp_fossil", "name": "Abiotic depletion (fossil fuels)", "unit": "MJ", "cf_key": "ADF"},
        ],
        "ref": "Guinée et al. (2002) Handbook on LCA. Kluwer. CML, Leiden University."
    },
    "cml2001_nl2014": {
        "name": "CML 2001 (all) V2.05 / Netherlands, 2014",
        "version": "V2.05", "normalization": "Netherlands, 2014",
        "categories": "Same as CML 2001 NL 2016",
        "ref": "CML, Leiden University."
    },
    "cml2001_nl2015": {
        "name": "CML 2001 (all) V2.05 / Netherlands, 2015",
        "version": "V2.05", "normalization": "Netherlands, 2015",
        "categories": "Same as CML 2001 NL 2016",
        "ref": "CML, Leiden University."
    },
    "cml2001_nl2013": {
        "name": "CML 2001 (all) V2.05 / Netherlands, 2013",
        "version": "V2.05", "normalization": "Netherlands, 2013",
        "categories": "Same as CML 2001 NL 2016",
        "ref": "CML, Leiden University."
    },
    "cml2001_nl2040": {
        "name": "CML 2001 (all) V2.05 / Netherlands, 2040",
        "version": "V2.05", "normalization": "Netherlands, 2040 (projected)",
        "categories": "Same as CML 2001 NL 2016",
        "ref": "CML, Leiden University."
    },
    "cml2001_nl2043": {
        "name": "CML 2001 (all) V2.05 / Netherlands, 2043",
        "version": "V2.05", "normalization": "Netherlands, 2043 (projected)",
        "categories": "Same as CML 2001 NL 2016",
        "ref": "CML, Leiden University."
    },
    "usetox_eu2004": {
        "name": "USEtox (default) V1.03 / Europe 2004",
        "version": "V1.03", "scope": "Europe 2004",
        "categories": [
            {"id": "ht_c", "name": "Human toxicity, cancer", "unit": "CTUh (comparative toxic units for humans)"},
            {"id": "ht_nc", "name": "Human toxicity, non-cancer", "unit": "CTUh"},
            {"id": "et_fw", "name": "Ecotoxicity, freshwater", "unit": "CTUe (comparative toxic units for ecosystems)"},
        ],
        "ref": "Rosenbaum et al. (2008) Int J LCA 13(7):532-546. USEtox model."
    },
    "usetox_eu2005": {
        "name": "USEtox (default) V1.03 / Europe 2005",
        "version": "V1.03", "scope": "Europe 2005",
        "categories": "Same as USEtox EU 2004",
        "ref": "Rosenbaum et al. (2008). USEtox."
    },
    "recipe2016_endpoint_ea": {
        "name": "ReCiPe 2016 Endpoint (E) V1.07",
        "version": "V1.07", "scope": "World (2010) E/A",
        "categories": [
            {"id": "hh", "name": "Damage to Human Health", "unit": "DALY"},
            {"id": "ed", "name": "Damage to Ecosystems", "unit": "species·yr"},
            {"id": "ra", "name": "Damage to Resource Availability", "unit": "USD2013"},
        ],
        "ref": "Huijbregts et al. (2017) ReCiPe2016. RIVM Report 2016-0104."
    },
    "impactworld_endpoint": {
        "name": "IMPACT World+ Endpoint V1.02",
        "version": "V1.02", "scope": "IMPACT World+ (Stepwise 2006 values)",
        "categories": [
            {"id": "hh", "name": "Human Health", "unit": "DALY"},
            {"id": "eq", "name": "Ecosystem Quality", "unit": "PDF·m²·yr"},
        ],
        "ref": "Bulle et al. (2019) IMPACT World+. Int J LCA 24:1653-1674."
    },
}


# ═══════════════════════════════════════════════════════════════
# MODULE 4: INTERACTIVE LCA WIZARD / GUIDANCE SYSTEM
# ═══════════════════════════════════════════════════════════════
LCA_WIZARD_STEPS = [
    {
        "step": 1,
        "title": "What are you trying to assess?",
        "question": "Describe your product, process, or service in plain language.",
        "examples": [
            "I'm making green hydrogen using electrolysis powered by solar panels in South Australia",
            "I want to compare the carbon footprint of a PET bottle vs glass bottle",
            "We're producing methanol from captured CO₂ and green hydrogen",
            "I need the LCA of our lithium-ion battery recycling process",
        ],
        "help": "Don't worry about technical LCA language — just describe what you want to assess. I'll help you structure it properly.",
    },
    {
        "step": 2,
        "title": "What's the purpose of this LCA?",
        "options": [
            {"label": "Internal decision-making", "desc": "Identify hotspots, compare options within your organisation", "type": "internal"},
            {"label": "External comparison (EPD/PCR)", "desc": "Publish results, compare with competitors — requires critical review", "type": "external"},
            {"label": "Policy or regulation", "desc": "EU PEF, Australian NGER, carbon reporting", "type": "policy"},
            {"label": "Academic research", "desc": "Publication, thesis, or technology assessment", "type": "academic"},
            {"label": "Investment / feasibility", "desc": "Is this technology worth pursuing?", "type": "investment"},
        ],
        "help": "The purpose determines the level of detail, data quality requirements, and whether you need a critical review panel.",
    },
    {
        "step": 3,
        "title": "Let's define your Functional Unit",
        "question": "The functional unit defines WHAT your product does, not what it IS. It should answer: what function, how much, for how long, and at what quality?",
        "templates": {
            "Energy": "1 kWh of electricity delivered to the grid at medium voltage",
            "Hydrogen": "1 kg of hydrogen gas at 99.97% purity, 30 bar, at plant gate",
            "Fuel": "1 MJ of energy content (LHV) delivered to vehicle tank",
            "Chemical": "1 kg of [chemical] at [purity]%, at plant gate, [packaging]",
            "Material": "1 kg of [material] at [grade/specification], at plant gate",
            "Battery": "1 kWh of battery storage capacity, BOL, at pack level",
            "Transport": "1 tonne-kilometre of freight transported by [mode]",
            "Building": "1 m² of floor area, meeting [standard], over [years] lifetime",
            "Packaging": "1 unit of packaging containing [volume] of [product], at point of sale",
            "Waste treatment": "Treatment of 1 kg / 1 tonne of [waste type]",
        },
        "help": "A good FU is specific, measurable, and comparable. Bad: '1 battery'. Good: '1 kWh of NMC811 Li-ion battery cell capacity at BOL (beginning of life), 250 Wh/kg, 1000 cycle warranty.'",
    },
    {
        "step": 4,
        "title": "Where does your system start and end?",
        "options": [
            {"label": "Cradle-to-Gate", "desc": "From raw materials to your factory gate. Most common for B2B.", "includes": [True, True, False, False, False]},
            {"label": "Cradle-to-Grave", "desc": "Full life cycle including use and end-of-life. Required for EPDs.", "includes": [True, True, True, True, True]},
            {"label": "Cradle-to-Cradle", "desc": "Includes recycling back into production. Circular economy.", "includes": [True, True, True, True, True]},
            {"label": "Gate-to-Gate", "desc": "Just your manufacturing process. For internal hotspot analysis.", "includes": [False, True, False, False, False]},
            {"label": "Well-to-Wheel", "desc": "For fuels: from extraction to combustion in vehicle.", "includes": [True, True, True, True, False]},
        ],
        "help": "For comparing products, both must use the same system boundary.",
    },
    {
        "step": 5,
        "title": "Now let's build your product system",
        "question": "What are the main stages / unit processes in your product's life cycle?",
        "help": "Think of each step in production as a 'unit process' with inputs (materials, energy, water) and outputs (product, emissions, waste). I'll help you identify what data you need for each stage.",
    },
]

# ═══════════════════════════════════════════════════════════════
# MODULE 5: PRODUCT STAGE TEMPLATES
# Standard life cycle stages with typical processes needed
# ═══════════════════════════════════════════════════════════════
PRODUCT_STAGE_TEMPLATES = {
    "general_manufacturing": {
        "name": "General Manufacturing Product",
        "stages": [
            {
                "stage": "A1 — Raw Material Supply",
                "description": "Extraction and processing of raw materials",
                "typical_processes": ["Mining/extraction", "Beneficiation", "Primary processing", "Transport to factory"],
                "typical_inputs": ["Raw materials (from nature)", "Energy (electricity, heat)", "Water", "Chemicals/reagents"],
                "typical_outputs": ["Processed materials", "Emissions to air (CO₂, PM, NOx)", "Wastewater", "Solid waste", "Co-products"],
            },
            {
                "stage": "A2 — Transport to Manufacturer",
                "description": "Transport of raw materials to manufacturing site",
                "typical_processes": ["Road transport (lorry)", "Rail transport", "Sea freight", "Pipeline"],
                "typical_inputs": ["Fuel (diesel, HFO)", "Electricity (for rail/pipeline)"],
                "typical_outputs": ["Emissions to air (CO₂, NOx, PM)"],
            },
            {
                "stage": "A3 — Manufacturing",
                "description": "Manufacturing/assembly of the product",
                "typical_processes": ["Processing", "Assembly", "Quality control", "Packaging"],
                "typical_inputs": ["Electricity (grid or onsite)", "Heat/steam", "Water", "Auxiliary materials", "Packaging materials"],
                "typical_outputs": ["Product", "Manufacturing scrap/waste", "Emissions to air", "Wastewater", "Solid waste"],
            },
            {
                "stage": "A4 — Distribution",
                "description": "Transport of finished product to customer",
                "typical_processes": ["Warehousing", "Distribution transport"],
                "typical_inputs": ["Fuel", "Electricity (warehousing)"],
                "typical_outputs": ["Emissions to air"],
            },
            {
                "stage": "B1-B7 — Use Phase",
                "description": "Product use, maintenance, repair, replacement",
                "typical_processes": ["Energy consumption during use", "Maintenance", "Replacement of parts"],
                "typical_inputs": ["Electricity", "Fuel", "Replacement materials", "Water"],
                "typical_outputs": ["Emissions during use", "Waste from maintenance"],
            },
            {
                "stage": "C1-C4 — End of Life",
                "description": "Deconstruction, transport, waste processing, disposal",
                "typical_processes": ["Deconstruction/disassembly", "Transport to waste facility", "Recycling", "Incineration", "Landfill"],
                "typical_inputs": ["Energy for deconstruction", "Transport fuel"],
                "typical_outputs": ["Recycled materials (credit)", "Energy recovery (credit)", "Emissions from waste treatment", "Final disposal residues"],
            },
            {
                "stage": "D — Beyond System Boundary",
                "description": "Benefits and loads from recycling, reuse, energy recovery",
                "typical_processes": ["Material recycling (avoided virgin production)", "Energy recovery (avoided electricity/heat)"],
                "typical_inputs": [],
                "typical_outputs": ["Net environmental benefit (credit) or burden"],
            },
        ],
        "ref": "EN 15804:2012+A2:2019 (construction products); ISO 14040/44"
    },
    "chemical_process": {
        "name": "Chemical Process / Industrial Plant",
        "stages": [
            {"stage": "Feedstock Supply", "description": "Raw material acquisition and pre-processing",
             "typical_inputs": ["Feedstock (NG, naphtha, biomass, CO₂, H₂, etc.)", "Catalysts", "Solvents", "Water"],
             "typical_outputs": ["Prepared feedstock"]},
            {"stage": "Reaction / Conversion", "description": "Main chemical conversion step(s)",
             "typical_inputs": ["Electricity", "Steam/Heat", "Catalysts", "Reagents"],
             "typical_outputs": ["Crude product", "By-products", "Emissions to air (CO₂, VOCs)", "Wastewater"]},
            {"stage": "Separation & Purification", "description": "Distillation, absorption, membrane, etc.",
             "typical_inputs": ["Electricity", "Cooling water", "Solvents"],
             "typical_outputs": ["Purified product", "Waste streams", "Recovered solvents"]},
            {"stage": "Product Storage & Handling", "description": "Storage tanks, loading",
             "typical_inputs": ["Electricity (pumps, compressors)", "Packaging"],
             "typical_outputs": ["Final product", "Fugitive emissions (VOCs)"]},
            {"stage": "Utilities", "description": "Steam, cooling water, compressed air, N₂",
             "typical_inputs": ["Natural gas (boilers)", "Electricity", "Water"],
             "typical_outputs": ["Steam", "Cooling water", "Emissions from combustion"]},
            {"stage": "Waste Treatment", "description": "On-site waste processing",
             "typical_inputs": ["Waste streams", "Chemicals for treatment"],
             "typical_outputs": ["Treated effluent", "Solid waste to landfill", "Emissions"]},
        ],
        "ref": "Standard chemical engineering practice; adapted from SimaPro chemical industry templates"
    },
    "hydrogen_production": {
        "name": "Hydrogen Production System",
        "stages": [
            {"stage": "Energy Supply", "typical_inputs": ["Electricity (grid/RE)", "Natural gas", "Biomass", "Nuclear heat"]},
            {"stage": "Water Treatment", "typical_inputs": ["Raw water", "Chemicals (NaOH, HCl, anti-scalant)", "Electricity"]},
            {"stage": "Hydrogen Generation", "typical_inputs": ["Treated water", "Energy", "Catalysts", "Membranes/electrodes"]},
            {"stage": "Gas Purification", "typical_inputs": ["Electricity", "Adsorbents (PSA)"]},
            {"stage": "Compression & Storage", "typical_inputs": ["Electricity (compressor)", "Storage vessels"]},
            {"stage": "CO₂ Management (if applicable)", "typical_inputs": ["Solvents (MEA)", "Energy for regeneration"]},
        ],
        "ref": "IEA (2023) Global Hydrogen Review; Hydrogen Council (2021)"
    },
    "battery_lifecycle": {
        "name": "Battery Life Cycle (Cradle-to-Grave)",
        "stages": [
            {"stage": "Raw Material Mining", "typical_inputs": ["Lithium ore/brine", "Nickel ore", "Cobalt ore", "Graphite", "Copper", "Aluminium"]},
            {"stage": "Material Processing", "typical_inputs": ["Energy", "Chemicals", "Water"]},
            {"stage": "Cell Manufacturing", "typical_inputs": ["CAM", "Anode", "Electrolyte", "Separator", "Electricity (dry room)", "NMP solvent"]},
            {"stage": "Pack Assembly", "typical_inputs": ["Cells", "BMS", "Housing (Al/steel)", "Cooling system", "Electricity"]},
            {"stage": "Use Phase (EV)", "typical_inputs": ["Electricity (charging)", "Replacement (if applicable)"]},
            {"stage": "End of Life", "typical_inputs": ["Collection", "Disassembly energy", "Recycling chemicals"]},
            {"stage": "Recycling (credit)", "typical_inputs": [], "typical_outputs": ["Recovered Li, Ni, Co, Cu (avoided primary)"]},
        ],
        "ref": "Dai et al. (2019) PMC; Chordia et al. (2024) Nat Commun"
    },
}


# ═══════════════════════════════════════════════════════════════
# MODULE 6: CUSTOM DATA ENTRY TEMPLATE
# For users to add their own process data
# ═══════════════════════════════════════════════════════════════
CUSTOM_PROCESS_TEMPLATE = {
    "id": "",          # auto-generated
    "name": "",        # user enters
    "cat": "Custom",   # user selects category
    "sector": "",      # user selects sector
    "unit": "",        # user selects (kg, kWh, MJ, m³, tkm, unit, etc.)
    "geo": "",         # user selects country/region
    "db": "User-defined",
    "ref": "",         # user enters their source/reference
    # Scope-based emission factors (simplified entry)
    "scope1_co2": 0,   # kg CO₂-e per unit (direct emissions)
    "scope2_co2": 0,   # kg CO₂-e per unit (purchased electricity)
    "scope3_co2": 0,   # kg CO₂-e per unit (upstream/downstream)
    "gwp_total": 0,    # Total GWP = scope1 + scope2 + scope3
    # Optional: detailed elementary flows
    "ef": {},          # user can add substance-level data
    # Technosphere inputs
    "inputs": {},      # user can link to other processes
    # Data quality
    "pedigree": {"Reliability": 3, "Completeness": 3, "Temporal": 3, "Geographical": 3, "Technological": 3},
}

VALID_UNITS = ["kg", "t", "kWh", "MWh", "MJ", "GJ", "m³", "L", "kL", "ML", 
               "tkm", "pkm", "unit", "m²", "m²·yr", "kg CO₂ captured"]

VALID_SECTORS = [
    "Electricity Generation", "Heat & Steam", "Fuels & Feedstocks",
    "Hydrogen Production", "Ammonia Production", "Methanol Production",
    "Carbon Capture & Storage", "Direct Air Capture",
    "Battery Manufacturing", "Battery Recycling",
    "Iron & Steel", "Aluminium", "Cement & Concrete", "Copper & Metals",
    "Polymers & Plastics", "Basic Chemicals", "Specialty Chemicals",
    "Food & Agriculture", "Forestry & Wood",
    "Road Transport", "Rail Transport", "Sea Transport", "Air Transport", "Pipeline",
    "Building & Construction", "Mining & Extraction",
    "Water Supply & Treatment", "Waste Management & Recycling",
    "Electronics & ICT", "Textiles",
    "Other / Custom",
]


# ═══════════════════════════════════════════════════════════════
# MODULE 7: DYNAMIC PFD / SANKEY VISUALIZATION
# ═══════════════════════════════════════════════════════════════
def create_sankey(inventory, processes_db):
    """Create a Sankey diagram from inventory using Plotly."""
    import plotly.graph_objects as go
    
    nodes = []
    links_source = []
    links_target = []
    links_value = []
    links_color = []
    
    # Collect all processes and their connections
    node_ids = {}
    
    for proc_id, amount in inventory.items():
        proc = next((p for p in processes_db if p["id"] == proc_id), None)
        if not proc:
            continue
        
        # Add main process node
        if proc_id not in node_ids:
            node_ids[proc_id] = len(nodes)
            nodes.append(proc["name"][:25])
        
        # Add input nodes and links
        for inp_id, inp_amt in proc.get("inputs", {}).items():
            if inp_id not in node_ids:
                node_ids[inp_id] = len(nodes)
                inp_proc = next((p for p in processes_db if p["id"] == inp_id), None)
                inp_name = inp_proc["name"][:25] if inp_proc else inp_id.replace("_", " ").title()[:25]
                nodes.append(inp_name)
            
            links_source.append(node_ids[inp_id])
            links_target.append(node_ids[proc_id])
            links_value.append(max(abs(inp_amt * amount), 0.001))
            links_color.append("rgba(0,212,170,0.3)")
    
    if not nodes:
        return None
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15, thickness=20,
            line=dict(color="#1e2d40", width=0.5),
            label=nodes,
            color="#0090ff",
        ),
        link=dict(
            source=links_source, target=links_target,
            value=links_value, color=links_color,
        )
    )])
    
    fig.update_layout(
        title_text="Process Flow (Sankey)",
        font=dict(size=10, color="#8499b0"),
        plot_bgcolor="#0a0d12",
        paper_bgcolor="#0a0d12",
        height=350,
    )
    
    return fig


def create_boundary_visual(stages_active, stage_names):
    """Create a visual boundary diagram showing included/excluded stages."""
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    colors = ["#4ade80", "#0090ff", "#ff6b35", "#c084fc", "#f59e0b"]
    icons = ["🌱", "🏭", "🚛", "🛒", "♻️"]
    
    for i, (name, active) in enumerate(zip(stage_names, stages_active)):
        x = i * 2
        opacity = 1.0 if active else 0.2
        border_color = colors[i] if active else "#506070"
        fill_color = f"rgba({int(colors[i][1:3],16)},{int(colors[i][3:5],16)},{int(colors[i][5:7],16)},{0.2 if active else 0.05})"
        
        # Box
        fig.add_shape(type="rect", x0=x-0.8, y0=-0.5, x1=x+0.8, y1=0.5,
                     line=dict(color=border_color, width=2),
                     fillcolor=fill_color, opacity=opacity)
        
        # Text
        fig.add_annotation(x=x, y=0, text=f"{icons[i]}<br>{name}",
                          showarrow=False, font=dict(color=border_color if active else "#506070", size=11),
                          opacity=opacity)
        
        # Arrow between stages
        if i < len(stage_names) - 1:
            next_active = stages_active[i+1]
            arrow_color = "#00d4aa" if (active and next_active) else "#1e2d40"
            fig.add_annotation(x=x+1, y=0, ax=x+0.9, ay=0,
                              arrowhead=2, arrowsize=1.5, arrowwidth=2,
                              arrowcolor=arrow_color, showarrow=True)
    
    # System boundary box
    first_active = next((i for i, a in enumerate(stages_active) if a), 0)
    last_active = len(stages_active) - 1 - next((i for i, a in enumerate(reversed(stages_active)) if a), 0)
    
    fig.add_shape(type="rect",
                 x0=first_active*2-1, y0=-0.8, x1=last_active*2+1, y1=0.8,
                 line=dict(color="#00d4aa", width=2, dash="dash"),
                 fillcolor="rgba(0,212,170,0.03)")
    fig.add_annotation(x=(first_active+last_active), y=0.9, text="SYSTEM BOUNDARY",
                      showarrow=False, font=dict(color="#00d4aa", size=10))
    
    fig.update_layout(
        showlegend=False, height=180,
        plot_bgcolor="#0a0d12", paper_bgcolor="#0a0d12",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.5, 9.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.2, 1.2]),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    
    return fig


# LCIA ENGINE — proper characterization from elementary flows
# ═══════════════════════════════════════════════════════════════
def run_lcia(inventory_items, method_id):
    """
    Proper LCIA: aggregate elementary flows from all processes × amounts,
    then multiply by characterization factors.
    Returns: {category: {score, unit, flows: {substance: contribution}}}
    """
    m = METHODS[method_id]
    # Step 1: Aggregate elementary flows
    total_ef = {}
    for proc_id, amount in inventory_items.items():
        proc = next((p for p in PROCESSES if p["id"]==proc_id), None)
        if not proc: continue
        for substance, value in proc.get("ef",{}).items():
            total_ef[substance] = total_ef.get(substance,0) + value * amount

    # Step 2: Characterize
    results = {}
    for cat in m["cats"]:
        cf_dict = m["cf_map"].get(cat, {})
        score = 0
        flows = {}
        if cat == "WC":
            score = total_ef.get("water",0)
            flows = {"water": total_ef.get("water",0)}
        elif cat == "ADF":
            for res in ["crude_oil","hard_coal","natural_gas","brown_coal","uranium","peat"]:
                v = total_ef.get(res,0)
                score += v
                if v > 0: flows[res] = v
        else:
            for substance, cf in cf_dict.items():
                ef_val = total_ef.get(substance,0)
                if ef_val > 0:
                    contribution = ef_val * cf
                    score += contribution
                    flows[substance] = contribution
        results[cat] = {"score":score, "unit":m["units"].get(cat,""), "flows":flows}
    return results, total_ef

# ═══════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════
if "inv" not in st.session_state: st.session_state.inv = {}
if "approach" not in st.session_state: st.session_state.approach = "attributional"
if "method" not in st.session_state: st.session_state.method = "recipe_h"
if "pfd" not in st.session_state: st.session_state.pfd = []
if "stages" not in st.session_state: st.session_state.stages = [True,True,True,True,True]
if "custom_procs" not in st.session_state: st.session_state.custom_procs = []
if "wizard_step" not in st.session_state: st.session_state.wizard_step = 0
if "project" not in st.session_state: st.session_state.project = {"name":"","fu":"","goal":"","type":"Cradle-to-Gate"}

def gp(pid):
    all_p = PROCESSES + st.session_state.custom_procs
    return next((p for p in all_p if p["id"]==pid), None)

def fs(v):
    if v==0: return "0"
    if abs(v)>=1000: return f"{v:,.0f}"
    if abs(v)>=0.01: return f"{v:.4g}"
    return f"{v:.3e}"

def boundary_fig():
    """Dynamic boundary visualization that updates with stage selection"""
    fig = go.Figure()
    names = ["Raw Material","Manufacturing","Distribution","Use Phase","End of Life"]
    icons = ["🌱","🏭","🚛","🛒","♻️"]
    colors = ["#059669","#0066ff","#e85d04","#7c3aed","#d97706"]
    for i,(n,ic,c) in enumerate(zip(names,icons,colors)):
        active = st.session_state.stages[i]
        x = i*2.2
        op = 1.0 if active else 0.15
        fc = f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},{0.12 if active else 0.03})"
        fig.add_shape(type="rect",x0=x-0.9,y0=-0.5,x1=x+0.9,y1=0.5,
            line=dict(color=c if active else "#d8dde6",width=2.5 if active else 1),
            fillcolor=fc,opacity=op)
        fig.add_annotation(x=x,y=0.05,text=f"<b>{ic}</b><br><span style='font-size:10px'>{n}</span>",
            showarrow=False,font=dict(color=c if active else "#c5cbd6",size=12),opacity=op)
        if i<4:
            na = st.session_state.stages[i+1]
            fig.add_annotation(x=x+1.1,y=0,ax=x+0.95,ay=0,arrowhead=2,arrowsize=1.5,arrowwidth=2,
                arrowcolor="#0066ff" if (active and na) else "#e2e8f0",showarrow=True)
    # System boundary dashed box
    first = next((i for i,a in enumerate(st.session_state.stages) if a),0)
    last = len(st.session_state.stages)-1-next((i for i,a in enumerate(reversed(st.session_state.stages)) if a),0)
    if any(st.session_state.stages):
        fig.add_shape(type="rect",x0=first*2.2-1.1,y0=-0.75,x1=last*2.2+1.1,y1=0.75,
            line=dict(color="#0066ff",width=2,dash="dash"),fillcolor="rgba(0,102,255,0.02)")
        fig.add_annotation(x=(first*2.2+last*2.2)/2,y=0.9,text="<b>System Boundary</b>",
            showarrow=False,font=dict(color="#0066ff",size=11))
    fig.update_layout(showlegend=False,height=160,
        plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-1.5,10]),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-1.1,1.15]),
        margin=dict(l=5,r=5,t=5,b=5))
    return fig

def sankey_fig():
    """Create Sankey flow diagram from inventory"""
    if not st.session_state.inv: return None
    nodes,src,tgt,val,clr=[],[],[],[],[]
    nmap={}
    all_p=PROCESSES+st.session_state.custom_procs
    for pid,amt in st.session_state.inv.items():
        pr=gp(pid)
        if not pr: continue
        if pid not in nmap: nmap[pid]=len(nodes);nodes.append(pr["name"][:28])
        for iid,ia in pr.get("inputs",{}).items():
            if iid not in nmap:
                ip=gp(iid)
                nmap[iid]=len(nodes);nodes.append((ip["name"] if ip else iid.replace("_"," ").title())[:28])
            src.append(nmap[iid]);tgt.append(nmap[pid]);val.append(max(abs(ia*amt),0.001));clr.append("rgba(0,102,255,0.2)")
    if not nodes: return None
    fig=go.Figure(go.Sankey(node=dict(pad=15,thickness=20,line=dict(color="#d8dde6",width=0.5),label=nodes,color="#0066ff"),
        link=dict(source=src,target=tgt,value=val,color=clr)))
    fig.update_layout(font=dict(size=10,color="#4a5568",family="Inter"),
        plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",height=300,margin=dict(l=10,r=10,t=30,b=10))
    return fig

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid #e2e8f0;">
        <div style="width:38px;height:38px;background:#0066ff;border-radius:10px;display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono';font-size:13px;color:white;font-weight:700;">PD</div>
        <div><span style="font-size:17px;font-weight:700;color:#1a1d23!important;">PRO-DESG</span><span style="font-size:17px;color:#0066ff!important;font-weight:700;"> LCA</span><br>
        <span style="font-size:10px;color:#8492a6!important;font-family:'JetBrains Mono';">v5.0 · """+str(len(PROCESSES)+len(st.session_state.custom_procs))+""" processes</span></div>
    </div>""", unsafe_allow_html=True)

    ac = "#0066ff" if st.session_state.approach=="attributional" else "#7c3aed"
    al = "ALCA" if st.session_state.approach=="attributional" else "CLCA"
    st.markdown(f'<span class="tag tb">{al}</span><span class="tag tgr">ISO 14040/44</span>', unsafe_allow_html=True)

    st.markdown("---")
    panel = st.radio("Navigation", [
        "🧙 LCA Wizard",
        "01 — Goal & Scope",
        "02 — LCA Approach",
        "03 — System Boundary",
        "04 — Process Flow",
        "05 — Inventory (LCI)",
        "06 — LCIA Results",
        "07 — Interpretation",
        "─────────────",
        "📊 Process Database",
        "🇦🇺 Australian NGA",
        "🔬 Characterization",
        "📐 Pedigree Matrix",
        "➕ Add Custom Data",
    ], label_visibility="collapsed")

    st.markdown("---")
    ni = len(st.session_state.inv)
    st.markdown(f"""<div style="background:#f0f2f5;border-radius:10px;padding:14px;margin-top:8px;">
        <div style="font-family:'JetBrains Mono';font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#8492a6!important;">Inventory</div>
        <div style="font-size:24px;font-weight:700;color:#0066ff!important;font-family:'JetBrains Mono';">{ni}</div>
    </div>""", unsafe_allow_html=True)

    if ni > 0:
        results, _ = run_lcia(st.session_state.inv, st.session_state.method)
        gwp = results.get("GWP",{}).get("score",0)
        st.markdown(f"""<div style="background:#fff7ed;border-radius:10px;padding:14px;margin-top:8px;">
            <div style="font-family:'JetBrains Mono';font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#8492a6!important;">Total GWP</div>
            <div style="font-size:16px;font-weight:700;color:#e85d04!important;font-family:'JetBrains Mono';">{fs(gwp)} kg CO₂-eq</div>
        </div>""", unsafe_allow_html=True)

    # Always show boundary mini-visual in sidebar
    if any(st.session_state.stages):
        st.plotly_chart(boundary_fig(), use_container_width=True, key="sb_sidebar")

# ═══════════════════════════════════════════════════════════════
# MAIN PANELS
# ═══════════════════════════════════════════════════════════════

# ─── WIZARD ──────────────────────────────────────────────────
if panel == "🧙 LCA Wizard":
    st.markdown("## 🧙 LCA Setup Wizard")
    st.markdown("*I'll guide you through setting up your LCA study step by step. Perfect if you're new to LCA.*")

    steps = LCA_WIZARD_STEPS
    step = st.session_state.wizard_step

    # Progress bar
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            color = "#0066ff" if i <= step else "#e2e8f0"
            st.markdown(f'<div style="text-align:center;padding:6px;background:{"#eff6ff" if i<=step else "#f8f9fb"};border:2px solid {color};border-radius:8px;font-size:11px;font-weight:600;color:{color};">Step {i+1}</div>', unsafe_allow_html=True)

    s = steps[min(step, len(steps)-1)]
    st.markdown(f"### Step {s['step']}: {s['title']}")
    st.markdown(f'<div class="info-box">💡 {s["help"]}</div>', unsafe_allow_html=True)

    if step == 0:
        desc = st.text_area("Describe your product/process:", placeholder="e.g. I'm producing green hydrogen using PEM electrolysis powered by solar PV in South Australia...", height=100)
        st.markdown("**Examples:**")
        for ex in s["examples"]:
            st.markdown(f"- _{ex}_")

    elif step == 1:
        for opt in s["options"]:
            if st.button(f"**{opt['label']}** — {opt['desc']}", use_container_width=True, key=f"wiz_{opt['type']}"):
                st.session_state.project["audience"] = opt["label"]

    elif step == 2:
        st.markdown("**Templates by product type:**")
        for cat, template in s["templates"].items():
            with st.expander(f"📋 {cat}"):
                st.code(template)
                if st.button(f"Use this template", key=f"fu_{cat}"):
                    st.session_state.project["fu"] = template
        fu = st.text_input("Your Functional Unit:", value=st.session_state.project.get("fu",""))
        st.session_state.project["fu"] = fu

    elif step == 3:
        for opt in s["options"]:
            if st.button(f"**{opt['label']}** — {opt['desc']}", use_container_width=True, key=f"bnd_{opt['label']}"):
                st.session_state.stages = opt["includes"]
                st.session_state.project["type"] = opt["label"]
        st.plotly_chart(boundary_fig(), use_container_width=True)

    elif step == 4:
        st.markdown("Now go to **05 — Inventory** to add your processes. You can also use the **Process Database** to find relevant datasets.")
        if st.session_state.project.get("fu"):
            st.success(f"✅ FU: {st.session_state.project['fu']}")
        if st.session_state.project.get("type"):
            st.success(f"✅ Boundary: {st.session_state.project['type']}")

    c1, c2 = st.columns(2)
    with c1:
        if step > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.wizard_step -= 1; st.rerun()
    with c2:
        if step < 4:
            if st.button("Next →", use_container_width=True, type="primary"):
                st.session_state.wizard_step += 1; st.rerun()


# ─── 01 GOAL & SCOPE ────────────────────────────────────────
elif panel == "01 — Goal & Scope":
    col_main, col_pfd = st.columns([3, 1])
    with col_pfd:
        st.markdown("##### 📐 System Overview")
        st.plotly_chart(boundary_fig(), use_container_width=True, key="sb_gs")
        sf = sankey_fig()
        if sf: st.plotly_chart(sf, use_container_width=True, key="sk_gs")

    with col_main:
        st.markdown("## Goal & Scope Definition")
        st.caption("ISO 14041 — Purpose, functional unit, system boundaries")
        with st.expander("📋 Project Information", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                pn = st.text_input("Project Name", st.session_state.project.get("name",""), key="gs_pn")
                st.session_state.project["name"] = pn
                fu = st.text_input("Functional Unit", st.session_state.project.get("fu",""), key="gs_fu")
                st.session_state.project["fu"] = fu
            with c2:
                st.selectbox("Study Type", ["Cradle-to-Gate","Cradle-to-Grave","Cradle-to-Cradle","Gate-to-Gate","Well-to-Wheel","Well-to-Wake"], key="gs_st")
                st.text_input("Reference Flow", key="gs_rf")
            st.text_area("Goal Statement", st.session_state.project.get("goal",""), placeholder="Describe the goal...", key="gs_goal")

        with st.expander("🎯 Scope & Standards", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.selectbox("Audience", ["Internal","External (comparative)","Academic","EPD/PCR","EU PEF","Policy"], key="gs_aud")
                st.selectbox("Allocation", ["System Expansion","Mass","Economic","Energy","Exergy","Substitution"], key="gs_alloc")
            with c2:
                st.selectbox("Cut-off", ["1% mass+energy","5%","0.1% (EPD)","Custom"], key="gs_co")
                st.selectbox("Background DB", ["ecoinvent 3.11 cutoff","ecoinvent 3.11 consequential","USLCI","GaBi 2023","AusLCI","Built-in"], key="gs_db")
            with c3:
                st.selectbox("Geography", ["Australia","Global","Europe","North America","China","Site-Specific"], key="gs_geo")
                st.selectbox("Temporal", ["Current (2024)","2020-2024","2015-2020","Prospective 2030","Prospective 2050"], key="gs_temp")


# ─── 02 LCA APPROACH ────────────────────────────────────────
elif panel == "02 — LCA Approach":
    st.markdown("## LCA Approach Selection")
    c1, c2 = st.columns(2)
    with c1:
        sel = st.session_state.approach == "attributional"
        if st.button(f"{'✅ ' if sel else ''}Attributional (ALCA)", use_container_width=True, type="primary" if sel else "secondary"):
            st.session_state.approach = "attributional"; st.rerun()
        st.markdown("""**Attributional LCA** describes flows *to and from* a product. Uses **average** data.
- *"What share of burdens belongs to this product?"*
- Allocation: mass, economic, energy, or system expansion
- Data: ecoinvent cutoff/APOS, market mix
- Standards: ISO 14040/44, PEF/OEF, GHG Protocol""")
    with c2:
        sel = st.session_state.approach == "consequential"
        if st.button(f"{'✅ ' if sel else ''}Consequential (CLCA)", use_container_width=True, type="primary" if sel else "secondary"):
            st.session_state.approach = "consequential"; st.rerun()
        st.markdown("""**Consequential LCA** describes how flows *change* with a decision. Uses **marginal** data.
- *"What happens if we make this choice?"*
- Allocation: system expansion only
- Data: ecoinvent consequential, marginal suppliers
- Standards: ISO 14040/44, Weidema (2003)""")


# ─── 03 SYSTEM BOUNDARY ─────────────────────────────────────
elif panel == "03 — System Boundary":
    col_main, col_viz = st.columns([2, 1])
    with col_viz:
        st.markdown("##### Boundary Visualization")
        st.plotly_chart(boundary_fig(), use_container_width=True, key="sb_main")

    with col_main:
        st.markdown("## System Boundary")
        names = ["🌱 Raw Material","🏭 Manufacturing","🚛 Distribution","🛒 Use Phase","♻️ End of Life"]
        cols = st.columns(5)
        for i, (col, n) in enumerate(zip(cols, names)):
            with col:
                st.session_state.stages[i] = st.checkbox(n, value=st.session_state.stages[i], key=f"stg_{i}")

        st.markdown("---")
        st.markdown("### Process Browser")
        search = st.text_input("🔍 Search processes", key="sb_search")
        sectors = sorted(set(p.get("sector","") for p in PROCESSES))
        sec_f = st.selectbox("Sector", ["All"] + sectors, key="sb_sec")
        all_p = PROCESSES + st.session_state.custom_procs
        fp = all_p
        if search:
            q = search.lower()
            fp = [p for p in fp if q in p["name"].lower() or q in p.get("desc","").lower() or q in p.get("sector","").lower()]
        if sec_f != "All":
            fp = [p for p in fp if p.get("sector","") == sec_f]

        for p in fp[:10]:
            with st.expander(f"**{p['name']}** — {p['unit']} ({p.get('geo','')})"):
                st.markdown(f"_{p.get('desc','')}_")
                st.markdown(f"📖 **Ref:** {p.get('ref','')}")
                # I/O view
                inp = p.get("inputs", {})
                if inp:
                    st.markdown('<div class="section-hdr">⬇ Inputs from Technosphere</div>', unsafe_allow_html=True)
                    for iid, ia in inp.items():
                        ip = gp(iid)
                        st.markdown(f"&nbsp;&nbsp;`{fs(ia)}` — {ip['name'] if ip else iid}")
                ef = p.get("ef", {})
                if ef:
                    for comp_name, comp_filter in [("💨 Emissions to Air", "Emissions to air"), ("💧 Emissions to Water", "Emissions to water"), ("⛏️ Resources", "Resources from nature")]:
                        flows = [(k,v) for k,v in ef.items() if COMPARTMENTS.get(k,"") == comp_filter and v > 0]
                        if flows:
                            st.markdown(f'<div class="section-hdr">{comp_name}</div>', unsafe_allow_html=True)
                            st.dataframe(pd.DataFrame([{"Substance": FLOW_NAMES.get(k,k), "Amount": fs(v), "Unit": FLOW_UNITS.get(k,"kg")} for k,v in sorted(flows, key=lambda x:-x[1])]),
                                use_container_width=True, hide_index=True, height=min(35*len(flows)+38, 200))
                stages = p.get("stages", [])
                if stages:
                    st.markdown('<div class="section-hdr">🔄 Process Stages</div>', unsafe_allow_html=True)
                    st.markdown(" → ".join([f"`{s}`" for s in stages]))
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("➕ Add to Inventory", key=f"sb_add_{p['id']}"):
                        st.session_state.inv[p["id"]] = st.session_state.inv.get(p["id"], 0) + 1; st.rerun()
                with c2:
                    if st.button("📐 Add to PFD", key=f"sb_pfd_{p['id']}"):
                        st.session_state.pfd.append(p["id"]); st.rerun()


# ─── 04 PROCESS FLOW ────────────────────────────────────────
elif panel == "04 — Process Flow":
    st.markdown("## Process Flow Diagram")
    sectors = sorted(set(p.get("sector","") for p in PROCESSES))
    sec = st.selectbox("Add from sector:", ["(Select)"] + sectors, key="pf_sec")
    if sec != "(Select)":
        sp = [p for p in PROCESSES if p.get("sector","") == sec]
        cols = st.columns(4)
        for i, p in enumerate(sp[:16]):
            with cols[i%4]:
                if st.button(f"+ {p['name'][:20]}", key=f"pfa_{p['id']}"):
                    st.session_state.pfd.append(p["id"]); st.rerun()

    st.markdown("---")
    # Sankey diagram
    sf = sankey_fig()
    if sf:
        st.plotly_chart(sf, use_container_width=True)

    if not st.session_state.pfd:
        st.info("Add processes above to build your flow diagram.")
    else:
        h = '<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:flex-start;padding:20px;background:white;border:1.5px solid #e2e8f0;border-radius:12px;">'
        for ni, nid in enumerate(st.session_state.pfd):
            pr = gp(nid)
            if not pr: continue
            if ni > 0: h += '<div class="pfd-arrow">→</div>'
            r,_ = run_lcia({nid:1}, "recipe_h")
            gwp = r.get("GWP",{}).get("score",0)
            h += f'<div class="pfd-node"><div style="font-size:9px;color:#0066ff;text-transform:uppercase;font-weight:600;">{pr.get("sector","")}</div><div style="font-size:12px;font-weight:600;color:#1a1d23;">{pr["name"][:26]}</div><div style="font-size:10px;color:#4a5568;">GWP: <b style="color:#e85d04;">{fs(gwp)}</b> CO₂-eq/{pr["unit"]}</div></div>'
        h += '</div>'
        st.markdown(h, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Transfer to Inventory", type="primary"):
                for nid in st.session_state.pfd:
                    st.session_state.inv[nid] = st.session_state.inv.get(nid,0) + 1
                st.success(f"Added {len(st.session_state.pfd)} processes!")
        with c2:
            if st.button("🗑️ Clear Canvas"):
                st.session_state.pfd = []; st.rerun()


# ─── 05 INVENTORY ───────────────────────────────────────────
elif panel == "05 — Inventory (LCI)":
    col_main, col_pfd = st.columns([3, 1])
    with col_pfd:
        st.markdown("##### Flow Diagram")
        sf = sankey_fig()
        if sf: st.plotly_chart(sf, use_container_width=True, key="sk_inv")
        st.plotly_chart(boundary_fig(), use_container_width=True, key="sb_inv")

    with col_main:
        st.markdown("## Life Cycle Inventory")
        cl, cr = st.columns([1, 1])
        with cl:
            st.markdown("### 📚 Process Library")
            sr = st.text_input("🔍 Search", key="inv_s")
            sectors = sorted(set(p.get("sector","") for p in PROCESSES))
            sf = st.selectbox("Sector", ["All"] + sectors, key="inv_f")
            all_p = PROCESSES + st.session_state.custom_procs
            fp = all_p
            if sr: q=sr.lower(); fp=[p for p in fp if q in p["name"].lower() or q in p.get("desc","").lower()]
            if sf != "All": fp=[p for p in fp if p.get("sector","")==sf]
            for p in fp[:12]:
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{p['name'][:32]}**  \n<span style='font-size:10px;color:#8492a6;'>{p.get('sector','')} · {p['geo']}</span>", unsafe_allow_html=True)
                with c2:
                    in_inv = p["id"] in st.session_state.inv
                    if st.button("✅" if in_inv else "➕", key=f"il_{p['id']}"):
                        st.session_state.inv[p["id"]] = st.session_state.inv.get(p["id"],0)+1; st.rerun()

        with cr:
            st.markdown(f"### 📋 Inventory ({len(st.session_state.inv)})")
            if not st.session_state.inv:
                st.info("Select processes from the library →")
            else:
                for pid, amt in list(st.session_state.inv.items()):
                    pr = gp(pid)
                    if not pr: continue
                    c1, c2, c3 = st.columns([3, 1.2, 0.5])
                    with c1: st.markdown(f"**{pr['name'][:28]}** `{pr['unit']}`")
                    with c2:
                        na = st.number_input("", value=float(amt), min_value=0.0, step=0.1, key=f"n_{pid}", label_visibility="collapsed")
                        st.session_state.inv[pid] = na
                    with c3:
                        if st.button("✕", key=f"r_{pid}"): del st.session_state.inv[pid]; st.rerun()

                st.markdown("---")
                # Aggregated flows
                _, tef = run_lcia(st.session_state.inv, "recipe_h")
                air = [(k,v) for k,v in tef.items() if COMPARTMENTS.get(k,"")=="Emissions to air" and v>0]
                if air:
                    st.markdown("**Aggregated Air Emissions:**")
                    st.dataframe(pd.DataFrame([{"Substance":FLOW_NAMES.get(k,k),"Total":fs(v),"Unit":"kg"} for k,v in sorted(air,key=lambda x:-x[1])[:10]]),
                        use_container_width=True, hide_index=True, height=200)


# ─── 06 LCIA ────────────────────────────────────────────────
elif panel == "06 — LCIA Results":
    col_main, col_pfd = st.columns([3, 1])
    with col_pfd:
        sf = sankey_fig()
        if sf: st.plotly_chart(sf, use_container_width=True, key="sk_lcia")

    with col_main:
        st.markdown("## Life Cycle Impact Assessment")
        all_methods = {**METHODS, **{k:v for k,v in LCIA_METHODS_EXTENDED.items()}}
        ms = st.selectbox("LCIA Method", list(METHODS.keys()), format_func=lambda x: METHODS[x]["name"], key="lcia_m")
        st.session_state.method = ms
        st.caption(f"📖 {METHODS[ms].get('ref','')}")

        if not st.session_state.inv:
            st.warning("⏳ Add processes in Inventory first.")
        else:
            results, tef = run_lcia(st.session_state.inv, ms)
            # Metric cards
            ncols = min(len(results), 4)
            cols = st.columns(ncols)
            colors = ["#0066ff","#059669","#e85d04","#7c3aed","#d97706","#dc2626"]
            for i, (cat, data) in enumerate(results.items()):
                with cols[i % ncols]:
                    st.metric(cat, fs(data["score"]), data["unit"])

            # Bar chart
            rows = [{"Category":cat,"Score":data["score"],"Unit":data["unit"]} for cat,data in results.items()]
            df = pd.DataFrame(rows)
            if not df.empty and df["Score"].sum() > 0:
                mx = df["Score"].max()
                df["Normalized"] = df["Score"] / mx * 100 if mx > 0 else 0
                fig = px.bar(df, x="Normalized", y="Category", orientation="h", color="Normalized",
                    color_continuous_scale=["#eff6ff","#0066ff","#e85d04"], height=300)
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#4a5568", family="Inter"), coloraxis_showscale=False,
                    xaxis=dict(gridcolor="#e2e8f0"), yaxis=dict(gridcolor="#e2e8f0"))
                st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df[["Category","Score","Unit"]], use_container_width=True, hide_index=True)

            # Substance contributions
            gwp_flows = results.get("GWP",{}).get("flows",{})
            if gwp_flows:
                st.markdown("### GWP Substance Contributions")
                gwp_total = results["GWP"]["score"]
                gdf = pd.DataFrame([{"Substance":FLOW_NAMES.get(k,k),"kg CO₂-eq":round(v,4),"% of Total":round(v/gwp_total*100,1) if gwp_total>0 else 0}
                    for k,v in sorted(gwp_flows.items(),key=lambda x:-x[1])])
                st.dataframe(gdf, use_container_width=True, hide_index=True)


# ─── 07 INTERPRETATION ──────────────────────────────────────
elif panel == "07 — Interpretation":
    st.markdown("## Interpretation")
    tab1,tab2,tab3,tab4 = st.tabs(["📊 Contribution","🔥 Hotspots","📈 Sensitivity","📝 Export"])

    with tab1:
        if st.session_state.inv:
            results,_ = run_lcia(st.session_state.inv, st.session_state.method)
            gwp_total = results.get("GWP",{}).get("score",0)
            rows = []
            for pid,amt in st.session_state.inv.items():
                pr = gp(pid)
                if not pr: continue
                r,_ = run_lcia({pid:amt},"recipe_h")
                gwp = r.get("GWP",{}).get("score",0)
                pct = (gwp/gwp_total*100) if gwp_total>0 else 0
                rows.append({"Process":pr["name"],"Amount":amt,"Unit":pr["unit"],"GWP":round(gwp,4),"Contribution %":round(pct,1),"Reference":pr.get("ref","")[:60]})
            df = pd.DataFrame(rows).sort_values("Contribution %",ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)
            if len(df)>1:
                fig = px.pie(df, names="Process", values="GWP", hole=0.4,
                    color_discrete_sequence=["#0066ff","#059669","#e85d04","#7c3aed","#d97706","#dc2626","#06b6d4","#8b5cf6"])
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#4a5568"),height=350)
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if st.session_state.inv:
            results,_ = run_lcia(st.session_state.inv, st.session_state.method)
            gwp_total = results.get("GWP",{}).get("score",0)
            found = False
            for pid,amt in st.session_state.inv.items():
                pr = gp(pid)
                if not pr: continue
                r,_ = run_lcia({pid:amt},"recipe_h")
                gwp = r.get("GWP",{}).get("score",0)
                pct = (gwp/gwp_total*100) if gwp_total>0 else 0
                if pct > 15:
                    found = True
                    st.markdown(f'<div class="hotspot"><b style="color:#dc2626;">{pr["name"]}</b> — <span style="font-family:JetBrains Mono;color:#dc2626;">{pct:.1f}% of GWP</span><br><span style="font-size:12px;color:#4a5568;">{pr.get("desc","")}</span><br><span style="font-size:11px;color:#8492a6;">📖 {pr.get("ref","")}</span></div>',unsafe_allow_html=True)
            if not found: st.success("✅ No single process dominates >15%. Well-distributed system.")

    with tab3:
        if st.session_state.inv:
            st.markdown('<div class="info-box">Adjust multipliers (0.5x–1.5x) to test parameter sensitivity.</div>', unsafe_allow_html=True)
            for pid,amt in list(st.session_state.inv.items())[:6]:
                pr = gp(pid)
                if pr: st.slider(f"{pr['name'][:30]}",0.5,1.5,1.0,0.05,key=f"se_{pid}")

    with tab4:
        results,tef = run_lcia(st.session_state.inv, st.session_state.method)
        csv_rows = []
        for pid,amt in st.session_state.inv.items():
            pr=gp(pid)
            if pr:
                r,_=run_lcia({pid:amt},"recipe_h")
                csv_rows.append({"Process":pr["name"],"Amount":amt,"Unit":pr["unit"],"GWP":r.get("GWP",{}).get("score",0),"Reference":pr.get("ref","")})
        if csv_rows:
            df=pd.DataFrame(csv_rows)
            c1,c2=st.columns(2)
            with c1: st.download_button("⬇ CSV",df.to_csv(index=False),"lca_results.csv")
            with c2:
                export={"project":st.session_state.project,"method":st.session_state.method,"approach":st.session_state.approach,
                    "inventory":csv_rows,"elementary_flows":{k:v for k,v in tef.items() if v>0},
                    "results":{k:{"score":v["score"],"unit":v["unit"]} for k,v in results.items()},
                    "generated":datetime.now().isoformat()}
                st.download_button("⬇ JSON",json.dumps(export,indent=2),"lca_data.json")


# ─── PROCESS DATABASE ────────────────────────────────────────
elif panel == "📊 Process Database":
    all_p = PROCESSES + st.session_state.custom_procs
    st.markdown(f"## Process Database — {len(all_p)} Datasets")
    ds = st.text_input("🔍 Search", key="dbs")
    sectors = sorted(set(p.get("sector","") for p in all_p))
    df_sec = st.selectbox("Sector", ["All"] + sectors, key="dbf")

    # Sector overview
    sec_counts = Counter(p.get("sector","") for p in all_p)
    cols = st.columns(5)
    for i,(sec,cnt) in enumerate(sec_counts.most_common()):
        with cols[i%5]:
            st.markdown(f'<div style="background:white;border:1.5px solid #e2e8f0;border-radius:8px;padding:8px;margin:3px;text-align:center;"><b style="color:#0066ff;font-size:11px;">{sec}</b><br><span style="font-size:10px;color:#8492a6;">{cnt}</span></div>',unsafe_allow_html=True)

    fp = all_p
    if ds: q=ds.lower();fp=[p for p in fp if q in p["name"].lower() or q in p.get("desc","").lower() or q in p.get("sector","").lower()]
    if df_sec!="All": fp=[p for p in fp if p.get("sector","")==df_sec]

    db_rows = []
    for p in fp:
        r,_=run_lcia({p["id"]:1},"recipe_h")
        db_rows.append({"Process":p["name"],"Sector":p.get("sector",""),"Unit":p["unit"],"Geo":p.get("geo",""),
            "GWP (CO₂-eq)":round(r.get("GWP",{}).get("score",0),4),"# EF":len([v for v in p.get("ef",{}).values() if v>0]),
            "DB":p.get("db",""),"Reference":p.get("ref","")[:70]})
    st.dataframe(pd.DataFrame(db_rows),use_container_width=True,hide_index=True,height=500)

    if df_sec!="All":
        sp=[r for r in db_rows if r["Sector"]==df_sec]
        if sp:
            fig=px.bar(pd.DataFrame(sp).sort_values("GWP (CO₂-eq)"),x="GWP (CO₂-eq)",y="Process",orientation="h",
                color="GWP (CO₂-eq)",color_continuous_scale=["#eff6ff","#0066ff","#e85d04"],height=max(250,len(sp)*25))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#4a5568"),coloraxis_showscale=False)
            st.plotly_chart(fig,use_container_width=True)


# ─── AUSTRALIAN NGA ──────────────────────────────────────────
elif panel == "🇦🇺 Australian NGA":
    st.markdown("## 🇦🇺 Australian NGA Factors 2024")
    st.caption("Source: DCCEEW National Greenhouse Accounts Factors 2024")

    st.markdown("### Electricity Grid Emission Factors (kg CO₂-e/kWh)")
    elec_rows = []
    for code, data in AU_ELEC_FACTORS.items():
        elec_rows.append({"State/Grid":data["name"],"Scope 2":data["scope2"],"Scope 3":data["scope3"],
            "Total (S2+S3)":data["total"],"Grid":data.get("grid",""),"Notes":data.get("notes","")[:50],"Year":data.get("year","")})
    df_elec = pd.DataFrame(elec_rows)
    st.dataframe(df_elec, use_container_width=True, hide_index=True)

    fig = px.bar(df_elec, x="State/Grid", y=["Scope 2","Scope 3"], barmode="stack",
        color_discrete_sequence=["#0066ff","#e85d04"], height=350, title="Scope 2+3 by State")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#4a5568"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Fuel Emission Factors (kg CO₂-e/GJ)")
    fuel_rows = []
    for code, data in AU_FUEL_FACTORS.items():
        fuel_rows.append({"Fuel":data["name"],"Unit":data["unit"],"Scope 1 (total)":data.get("scope1_total",0),
            "Scope 3":data.get("scope3",0),"Ref":data.get("ref","")[:50]})
    st.dataframe(pd.DataFrame(fuel_rows), use_container_width=True, hide_index=True)

    st.markdown('<div class="info-box">📖 All factors from DCCEEW NGA Factors 2024 (released September 2024). NSW scope 2 = 0.66 kg CO₂-e/kWh. Victoria highest at 0.79 (brown coal). SA lowest NEM at 0.19 (~72% renewables).</div>', unsafe_allow_html=True)


# ─── CHARACTERIZATION ────────────────────────────────────────
elif panel == "🔬 Characterization":
    st.markdown("## Characterization Factors")
    tab1,tab2 = st.tabs(["Substance CFs","LCIA Methods"])
    with tab1:
        cf_sel = st.selectbox("Category", list(ALL_CF.keys()))
        cf = ALL_CF[cf_sel]
        st.dataframe(pd.DataFrame([{"Substance":FLOW_NAMES.get(k,k),"CF":v,"Unit":cf_sel} for k,v in sorted(cf.items(),key=lambda x:-x[1])]),
            use_container_width=True, hide_index=True)
        st.markdown("### IPCC AR6 GWP")
        ipcc = [["CO₂",1,1,1,"~1000"],["CH₄ fossil",82.5,29.8,10,"11.8"],["CH₄ biogenic",79.7,27.0,9,"11.8"],["N₂O",273,273,130,"109"],
            ["SF₆",18300,25200,32600,"3200"],["CF₄",4880,7380,11100,"50000"],["HFC-23",13400,14600,10500,"228"],["HFC-134a",4140,1530,436,"14"],["NF₃",13400,17400,20700,"569"]]
        st.dataframe(pd.DataFrame(ipcc,columns=["Substance","GWP20","GWP100","GWP500","Lifetime (yr)"]),use_container_width=True,hide_index=True)
    with tab2:
        st.markdown("### Available LCIA Methods")
        for mid,m in {**METHODS, **LCIA_METHODS_EXTENDED}.items():
            with st.expander(f"**{m['name']}**"):
                st.markdown(f"📖 {m.get('ref','')}")
                cats = m.get("cats") or m.get("categories")
                if isinstance(cats, list):
                    st.dataframe(pd.DataFrame([{"Category":c.get("name",c.get("n","")),"Unit":c.get("unit",c.get("u",""))} for c in cats if isinstance(c,dict)]),
                        use_container_width=True, hide_index=True)
                elif isinstance(cats, str):
                    st.markdown(f"Categories: {cats}")


# ─── PEDIGREE MATRIX ────────────────────────────────────────
elif panel == "📐 Pedigree Matrix":
    st.markdown("## Data Quality — Pedigree Matrix")
    st.caption("Weidema & Wesnaes (1996). Weights: Reliability 0.30, Completeness 0.25, Temporal 0.15, Geography 0.10, Technology 0.20")

    pm = PEDIGREE_MATRIX
    # Interactive scoring
    st.markdown("### Score Your Data Quality")
    scores = {}
    cols = st.columns(5)
    for i, (col, dim) in enumerate(zip(cols, pm["dimensions"])):
        with col:
            st.markdown(f"**{dim}**  \nWeight: {pm['weights'][i]}")
            scores[dim] = st.selectbox(f"Score", [5,4,3,2,1], key=f"ped_{dim}", index=2,
                format_func=lambda x: f"{x} — {pm['scores'][x][dim][:30]}...")

    dqi = calculate_dqi(scores)
    gsd = dqi_to_uncertainty(dqi)
    c1,c2,c3 = st.columns(3)
    c1.metric("Weighted DQI", f"{dqi}/5.0")
    c2.metric("Quality Level", "Excellent" if dqi>=4.5 else "Good" if dqi>=3.5 else "Fair" if dqi>=2.5 else "Poor" if dqi>=1.5 else "Very Poor")
    c3.metric("GSD² (uncertainty)", f"{gsd}")

    # Full matrix display
    st.markdown("### Reference Matrix")
    for score in [5,4,3,2,1]:
        cols = st.columns([0.3] + [1]*5)
        with cols[0]:
            st.markdown(f"**{score}**")
        for i, dim in enumerate(pm["dimensions"]):
            with cols[i+1]:
                bg = ["#ecfdf5","#f0fdf4","#fefce8","#fff7ed","#fef2f2"][5-score]
                st.markdown(f'<div style="background:{bg};padding:8px;border-radius:6px;font-size:11px;border:1px solid #e2e8f0;">{pm["scores"][score][dim]}</div>', unsafe_allow_html=True)


# ─── ADD CUSTOM DATA ─────────────────────────────────────────
elif panel == "➕ Add Custom Data":
    st.markdown("## Add Custom Process Data")
    st.markdown("*Add your own processes when database values aren't available. You can enter scope-based emission factors or detailed elementary flows.*")

    with st.expander("📝 New Process Entry", expanded=True):
        c1,c2,c3 = st.columns(3)
        with c1:
            cp_name = st.text_input("Process Name", placeholder="e.g. Electricity, 100% renewable PPA")
            cp_sector = st.selectbox("Sector", VALID_SECTORS)
        with c2:
            cp_unit = st.selectbox("Unit", VALID_UNITS)
            cp_geo = st.selectbox("Geography", ["AU-NSW","AU-VIC","AU-QLD","AU-SA","AU-TAS","AU-WA","AU-NT","AU","GLO","RER","US","CN","IN","JP","Other"])
        with c3:
            cp_ref = st.text_input("Reference/Source", placeholder="e.g. DCCEEW NGA 2024; Company data")

        st.markdown("### Emission Factors")
        st.markdown('<div class="info-box">Enter as kg CO₂-e per unit. You can enter Scope 1 (direct), Scope 2 (purchased electricity), and/or Scope 3 (upstream/downstream), OR just the total GWP.</div>', unsafe_allow_html=True)

        c1,c2,c3,c4 = st.columns(4)
        with c1: s1 = st.number_input("Scope 1 (kg CO₂-e)", 0.0, step=0.001, format="%.4f")
        with c2: s2 = st.number_input("Scope 2 (kg CO₂-e)", 0.0, step=0.001, format="%.4f")
        with c3: s3 = st.number_input("Scope 3 (kg CO₂-e)", 0.0, step=0.001, format="%.4f")
        with c4: total_gwp = st.number_input("OR Total GWP", 0.0, step=0.001, format="%.4f")

        gwp_val = total_gwp if total_gwp > 0 else s1 + s2 + s3

        st.markdown("### Additional Emission Factors (optional)")
        c1,c2,c3 = st.columns(3)
        with c1: cp_ap = st.number_input("AP (kg SO₂-eq)", 0.0, step=0.0001, format="%.6f")
        with c2: cp_ep = st.number_input("EP (kg PO₄-eq)", 0.0, step=0.0001, format="%.6f")
        with c3: cp_water = st.number_input("Water (m³)", 0.0, step=0.01, format="%.3f")

        st.markdown("### Data Quality (Pedigree)")
        pc = st.columns(5)
        ped = {}
        for i, dim in enumerate(PEDIGREE_MATRIX["dimensions"]):
            with pc[i]:
                ped[dim] = st.selectbox(dim[:8], [5,4,3,2,1], index=2, key=f"cp_ped_{dim}")

        if st.button("➕ Add Process to Database", type="primary"):
            if cp_name and gwp_val > 0:
                new_proc = {
                    "id": f"custom_{len(st.session_state.custom_procs)}_{int(datetime.now().timestamp())}",
                    "name": cp_name, "cat": "Custom", "sector": cp_sector,
                    "unit": cp_unit, "geo": cp_geo, "db": "User-defined",
                    "ref": cp_ref,
                    "inputs": {},
                    "ef": {"CO2": gwp_val, "SO2": cp_ap, "PO4": cp_ep * 3, "water": cp_water},
                    "outputs": [cp_name], "stages": ["User-defined process"],
                    "desc": f"Custom process. Scope 1: {s1}, Scope 2: {s2}, Scope 3: {s3}. DQI: {calculate_dqi(ped):.1f}/5.",
                    "pedigree": ped,
                }
                st.session_state.custom_procs.append(new_proc)
                st.success(f"✅ Added '{cp_name}' to database! ({len(st.session_state.custom_procs)} custom processes)")
                st.rerun()
            else:
                st.error("Please enter a name and at least one emission factor.")

    # Show existing custom processes
    if st.session_state.custom_procs:
        st.markdown("### Your Custom Processes")
        cp_df = pd.DataFrame([{"Name":p["name"],"Sector":p["sector"],"Unit":p["unit"],"GWP":p["ef"].get("CO2",0),"Geo":p["geo"],"Ref":p.get("ref","")} for p in st.session_state.custom_procs])
        st.dataframe(cp_df, use_container_width=True, hide_index=True)


# ─── SEPARATOR ───────────────────────────────────────────────
elif panel == "─────────────":
    st.markdown("## PRO-DESG LCA v5.0")
    st.markdown("Select a panel from the sidebar to continue.")


# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
all_p = PROCESSES + st.session_state.custom_procs
st.markdown(f'<p style="text-align:center;font-size:11px;color:#8492a6;font-family:JetBrains Mono;">PRO-DESG LCA v5.0 · {len(all_p)} processes · {len(GRIDS)} country grids · {len(FLOW_NAMES)} elementary flows · {len(METHODS)+len(LCIA_METHODS_EXTENDED)} LCIA methods · ISO 14040/44 · {datetime.now().strftime("%Y-%m-%d")}</p>', unsafe_allow_html=True)
