"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AMRIZE AR INTELLIGENCE v2.0 - ULTIMATE ENTERPRISE EDITION
Professional Financial Analytics Platform
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PLATAFORMA
# ═══════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Amrize AR Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colores Identitarios Amrize
AMZ_MIDNIGHT = "#011E6A"
AMZ_ROYAL = "#0047AB"
AMZ_SKY = "#00A7E1"
S_GREEN = "#059669"
S_RED = "#DC2626"
S_AMBER = "#D97706"

# Nombre del archivo de tu logo (Asegúrate de que esté en la misma carpeta)
LOGO_FILE = "image_c0ce60.png" 

# Inicialización de Estados
if 'theme' not in st.session_state: st.session_state.theme = 'light'
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'auth_ok' not in st.session_state: st.session_state.auth_ok = False

# ═══════════════════════════════════════════════════════════════════════
# DICCIONARIO GLOBAL DE TRADUCCIONES
# ═══════════════════════════════════════════════════════════════════════

LANG_DICT = {
    'EN': {
        'login_sub': 'ENTERPRISE AR ANALYTICS SUITE',
        'login_label': 'Access Token',
        'login_btn': 'Authenticate',
        'auth_error': 'Access Denied: Invalid Credentials',
        'header_title': 'AMRIZE AR INTELLIGENCE',
        'header_sub': 'Global Portfolio Analysis & Management',
        'system_wait': 'System Standby',
        'system_msg': 'Please upload the SAP Aging Report to initialize the engine.',
        'sidebar_ctrl': 'DATA CONTROLS',
        'sidebar_upload': 'Ingest SAP Report (.csv / .xlsx)',
        'sidebar_filters': 'PORTFOLIO FILTERS',
        'tab_strat': 'Executive Insights',
        'tab_ops': 'Operational Ledger',
        'kpi_gross': 'Gross Exposure',
        'kpi_ap': 'Credits (AP)',
        'kpi_delinq': 'Delinquency Rate',
        'kpi_risk': 'Credit Exceptions',
        'metrics': 'Executive Summary',
        'struct': 'Structural Analytics',
        'export': 'Export Data',
        'footer': 'CONFIDENTIAL CORPORATE DATA'
    },
    'ES': {
        'login_sub': 'SUITE EMPRESARIAL DE ANÁLISIS AR',
        'login_label': 'Token de Acceso',
        'login_btn': 'Autenticar',
        'auth_error': 'Acceso Denegado: Credenciales Inválidas',
        'header_title': 'AMRIZE AR INTELLIGENCE',
        'header_sub': 'Análisis de Cartera Global y Gestión',
        'system_wait': 'Sistema en Espera',
        'system_msg': 'Cargue el reporte de antigüedad de SAP para inicializar el motor.',
        'sidebar_ctrl': 'CONTROLES DE DATOS',
        'sidebar_upload': 'Cargar Reporte SAP (.csv / .xlsx)',
        'sidebar_filters': 'FILTROS DE CARTERA',
        'tab_strat': 'Visión Estratégica',
        'tab_ops': 'Libro Operativo',
        'kpi_gross': 'Exposición Bruta',
        'kpi_ap': 'Saldos a Favor (AP)',
        'kpi_delinq': 'Tasa de Morosidad',
        'kpi_risk': 'Excesos de Crédito',
        'metrics': 'Resumen Ejecutivo',
        'struct': 'Análisis Estructural',
        'export': 'Exportar Datos',
        'footer': 'DATOS CORPORATIVOS CONFIDENCIALES'
    }
}

L = LANG_DICT[st.session_state.lang]

# ═══════════════════════════════════════════════════════════════════════
# CAPA DE DISEÑO (CSS PRUSIANO)
# ═══════════════════════════════════════════════════════════════════════

def inject_styles():
    is_dark = st.session_state.theme == 'dark'
    bg = "#0B0F19" if is_dark else "#F8FAFC"
    card = "#1E293B" if is_dark else "#FFFFFF"
    text = "#F8FAFC" if is_dark else "#0F172A"
    border = "#334155" if is_dark else "#E2E8F0"
    
    st.markdown(f"""
    <style>
    .main {{ background-color: {bg}; color: {text}; }}
    
    /* Legibilidad del File Uploader */
    [data-testid="stFileUploader"] {{
        background-color: {card};
        border: 1px dashed {border};
        border-radius: 8px;
    }}
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] section {{
        color: {text} !important;
    }}

    /* Estética de Dropdowns en Sidebar */
    [data-testid="stSidebar"] [data-baseweb="select"] * {{
        color: {text} !important;
    }}
    
    /* Header Corporativo */
    .header-box {{
        background-color: {card};
        padding: 1.5rem 2rem;
        border-radius: 6px;
        border-left: 6px solid {AMZ_MIDNIGHT};
        border-bottom: 1px solid {border};
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    /* KPI Cards */
    .kpi-container {{
        background: {card};
        border: 1px solid {border};
        border-radius: 6px;
        padding: 1.5rem;
        text-align: center;
        border-top: 4px solid {AMZ_SKY};
    }}
    
    [data-testid="stSidebar"] {{ background-color: {AMZ_MIDNIGHT}; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{ gap: 30px; border-bottom: 1px solid {border}; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 700; font-size: 1rem; color: {text}; }}
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# LÓGICA DE NEGOCIO Y SAP
# ═══════════════════════════════════════════════════════════════════════

def human_format(num):
    num = float(num)
    if abs(num) < 1000: return f"${num:,.0f}"
    if abs(num) < 1000000: return f"${num/1000:,.1f}K"
    return f"${num/1000000:,.1f}M"

def process_file(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        
        # ELIMINAR RESULTADOS PARCIALES SAP
        if 'Document date' in df.columns:
            df = df[df['Document date'].astype(str).str.strip() != 'Result'].copy()
        
        # LIMPIEZA NUMÉRICA INTEGRAL (INCLUYENDO BUCKETS DE AGING)
        buckets = ['1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays', '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays']
        num_cols = ['Open Amount', 'Credit Limit', 'Current Amount'] + buckets
        
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        
        # PRESERVACIÓN DE NOTAS SP #
        if 'SP #' in df.columns:
            df['SP #'] = df['SP #'].fillna("")
        
        if 'Document date' in df.columns:
            df['Document date'] = pd.to_datetime(df['Document date'], errors='coerce')
        if 'Net due date' in df.columns:
            df['Net due date'] = pd.to_datetime(df['Net due date'], errors='coerce')
        
        return df, None
    except Exception as e:
        return None, str(e)

# ═══════════════════════════════════════════════════════════════════════
# AUTH & BRANDING INTEGRADO
# ═══════════════════════════════════════════════════════════════════════

inject_styles()

if not st.session_state.auth_ok:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br>"*4, unsafe_allow_html=True)
        # Mostrar Logo Local en Login
        if os.path.exists(LOGO_FILE):
            st.image(LOGO_FILE, width=250)
        else:
            st.markdown(f"<h1 style='text-align:center; color:{AMZ_MIDNIGHT};'>AMRIZE</h1>", unsafe_allow_html=True)
            
        st.markdown(f"<p style='text-align:center; color:#64748B; letter-spacing:1.5px; font-weight:600;'>{L['login_sub']}</p>", unsafe_allow_html=True)
        
        with st.form("auth_form"):
            token = st.text_input(L['login_label'], type="password")
            if st.form_submit_button(L['login_btn'], use_container_width=True):
                try:
                    if token == st.secrets["APP_PASSWORD"]:
                        st.session_state.auth_ok = True
                        st.rerun()
                    else:
                        st.error(L['auth_error'])
                except KeyError:
                    st.error("Error crítico: 'APP_PASSWORD' no está configurado en los secrets de Streamlit.")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════
# DASHBOARD ACTIVO
# ═══════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(f"### {L['sidebar_ctrl']}")
    file_input = st.file_uploader(L['sidebar_upload'], type=['csv', 'xlsx'])
    
    st.markdown("---")
    st.markdown("### UI SETTINGS")
    
    # Switch Idioma
    lang_choice = st.radio("Language", ['EN', 'ES'], index=0 if st.session_state.lang == 'EN' else 1, horizontal=True)
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()
        
    # Switch Modo
    mode = st.toggle("Dark Mode", value=(st.session_state.theme == 'dark'))
    new_theme = 'dark' if mode else 'light'
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    if file_input:
        df_raw, error = process_file(file_input)
        if not error:
            st.markdown(f"### {L['sidebar_filters']}")
            seg_opts = sorted(df_raw['Counterparty Type'].dropna().unique()) if 'Counterparty Type' in df_raw.columns else []
            seg = st.multiselect(L['sidebar_segment'], options=seg_opts)
            
            ent_opts = sorted(df_raw['Counterparty Name'].dropna().unique()) if 'Counterparty Name' in df_raw.columns else []
            ent = st.multiselect(L['sidebar_entity'], options=ent_opts)
            
            dff = df_raw.copy()
            if seg: dff = dff[dff['Counterparty Type'].isin(seg)]
            if ent: dff = dff[dff['Counterparty Name'].isin(ent)]
        else:
            st.error(error)

# Pantalla de Bienvenida (Standby)
if 'dff' not in locals():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br>"*5, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center; padding: 4rem; border: 2px dashed {AMZ_MIDNIGHT}; border-radius: 12px; background: white;">
            <h2 style="color: {AMZ_MIDNIGHT}; font-weight: 800;">{L['system_wait']}</h2>
            <p style="color: #64748B; font-size: 1rem;">{L['system_msg']}</p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# Header Principal con Logo Dinámico
c_head1, c_head2 = st.columns([4, 1])
with c_head1:
    st.markdown(f"""
        <div class="header-box">
            <h1 style='margin:0; color:{AMZ_MIDNIGHT}; font-size:1.7rem; font-weight:800;'>{L['header_title']}</h1>
            <p style='margin:0; color:#64748B; font-weight:600; font-size:0.85rem;'>{L['header_sub']}</p>
        </div>
    """, unsafe_allow_html=True)
with c_head2:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=160)

# Cálculo de Métricas (Manejo de excepciones en caso de que falten columnas en el CSV)
if 'Open Amount' in dff.columns:
    gross = dff[dff['Open Amount'] > 0]['Open Amount'].sum()
    ap_credits = abs(dff[dff['Open Amount'] < 0]['Open Amount'].sum())
else:
    gross, ap_credits = 0, 0

if 'Current Amount' in dff.columns:
    current = dff['Current Amount'].sum()
else:
    current = 0

delinq = ((gross - current) / gross * 100) if gross > 0 else 0

if 'Open Amount' in dff.columns and 'Credit Limit' in dff.columns:
    risk_ex = len(dff[dff['Open Amount'] > dff['Credit Limit']])
else:
    risk_ex = 0

# Pestañas Funcionales
t1, t2 = st.tabs([L['tab_strat'], L['tab_ops']])

with t1:
    st.markdown(f"#### {L['metrics']}")
    k1, k2, k3, k4 = st.columns(4)
    
    with k1: st.markdown(f'<div class="kpi-container"><div style="font-size:0.75rem; color:#64748B; font-weight:700;">{L["kpi_gross"]}</div><div style="font-size:1.8rem; font-weight:800; color:{AMZ_MIDNIGHT};">{human_format(gross)}</div><div style="font-size:0.7rem; color:#64748B;">{len(dff)} documents</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-container"><div style="font-size:0.75rem; color:#64748B; font-weight:700;">{L["kpi_ap"]}</div><div style="font-size:1.8rem; font-weight:800; color:{S_GREEN};">{human_format(ap_credits)}</div><div style="font-size:0.7rem; color:#059669;">Balance offsets</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-container"><div style="font-size:0.75rem; color:#64748B; font-weight:700;">{L["kpi_delinq"]}</div><div style="font-size:1.8rem; font-weight:800; color:{S_RED};">{delinq:.1f}%</div><div style="font-size:0.7rem; color:#DC2626;">Portfolio at risk</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-container"><div style="font-size:0.75rem; color:#64748B; font-weight:700;">{L["kpi_risk"]}</div><div style="font-size:1.8rem; font-weight:800; color:{S_AMBER};">{risk_ex}</div><div style="font-size:0.7rem; color:#D97706;">Credit exceptions</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"#### {L['struct']}")
    g1, g2 = st.columns(2)
    chart_bg = "plotly_dark" if st.session_state.theme == 'dark' else "plotly_white"
    
    with g1:
        buckets = ['1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays', '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays']
        b_vals = [dff[b].sum() for b in buckets if b in dff.columns]
        fig_ag = go.Figure(go.Bar(x=[b.replace('\n', ' ') for b in buckets], y=b_vals, marker_color=AMZ_ROYAL, text=[human_format(v) for v in b_vals], textposition='auto'))
        fig_ag.update_layout(title="AGING DISTRIBUTION", height=400, template=chart_bg, margin=dict(t=80))
        st.plotly_chart(fig_ag, use_container_width=True)

    with g2:
        if 'Counterparty Name' in dff.columns and 'Open Amount' in dff.columns:
            top_ent = dff.groupby('Counterparty Name')['Open Amount'].sum().nlargest(10).sort_values()
            fig_top = px.bar(top_ent, orientation='h', color_discrete_sequence=[AMZ_SKY])
            fig_top.update_layout(title="TOP 10 ACCOUNTS BY OPEN AMOUNT", height=400, template=chart_bg, showlegend=False, margin=dict(t=80))
            st.plotly_chart(fig_top, use_container_width=True)

with t2:
    st.markdown(f"#### Master Open Items Registry")
    cols_to_show = ['Counterparty Name', 'Counterparty Type', 'INV # - Salesforce', 'SP #', 'Document date', 'Net due date', 'Open Amount', 'Credit Limit']
    available_cols = [c for c in cols_to_show if c in dff.columns]
    
    if available_cols:
        if 'Open Amount' in available_cols:
            df_v = dff[available_cols].sort_values('Open Amount', ascending=False)
        else:
            df_v = dff[available_cols]
            
        st.dataframe(df_v, use_container_width=True, hide_index=True, height=500,
            column_config={
                "Open Amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
                "Credit Limit": st.column_config.NumberColumn("Limit", format="$%.2f"),
                "Document date": st.column_config.DateColumn("Doc Date"),
                "Net due date": st.column_config.DateColumn("Due Date"),
                "SP #": st.column_config.TextColumn("Management Notes", width="large")
            })
        
        st.markdown("<br>", unsafe_allow_html=True)
        csv_data = df_v.to_csv(index=False).encode('utf-8')
        st.download_button(L['export'], data=csv_data, file_name=f"AR_Status_{datetime.now().strftime('%Y%m%d')}.csv", mime='text/csv')

st.markdown(f"<div style='text-align:center; padding:3rem; color:#94A3B8; font-size:0.75rem; border-top:1px solid #E2E8F0; margin-top:5rem;'>AMRIZE INTELLIGENCE | {L['footer']} | © {datetime.now().year}</div>", unsafe_allow_html=True)