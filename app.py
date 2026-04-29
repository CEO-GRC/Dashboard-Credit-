"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AMRIZE AR INTELLIGENCE v1.4 - Global Enterprise Edition
Professional Accounts Receivable Analytics Platform
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN Y ESTADO DE SESIÓN
# ═══════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Amrize AR Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'theme' not in st.session_state: st.session_state.theme = 'light'
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'auth' not in st.session_state: st.session_state.auth = False

# ═══════════════════════════════════════════════════════════════════════
# TRADUCCIONES
# ═══════════════════════════════════════════════════════════════════════

T = {
    'EN': {
        'login_title': 'AR INTELLIGENCE ACCESS',
        'login_token': 'Access Token',
        'login_btn': 'Authenticate System',
        'auth_error': 'Access denied.',
        'header_subtitle': 'GLOBAL AR ANALYTICS PLATFORM',
        'sidebar_data': 'DATA ADMINISTRATION',
        'sidebar_upload': 'Upload SAP Aging Report',
        'sidebar_filters': 'GLOBAL FILTERS',
        'sidebar_segment': 'Segment',
        'sidebar_entity': 'Counterparty',
        'sidebar_logout': 'End Session',
        'system_ready': 'System Ready',
        'system_msg': 'Please upload the SAP Aging Report in the sidebar to initialize the analytical engine.',
        'tab_portfolio': 'Portfolio Vision',
        'tab_ops': 'Operational Tracking',
        'kpi_gross': 'Gross Debt',
        'kpi_credits': 'Credits (AP)',
        'kpi_delinquency': 'Overdue Index',
        'kpi_limit': 'Limit Excess',
        'exec_metrics': 'Executive Metrics',
        'active_docs': 'active documents',
        'offset_amount': 'Offset amount',
        'vs_entities': 'Against unique entities',
        'total_entities': 'Total Entities',
        'avg_ticket': 'Avg. Ticket',
        'exp_vencida': 'Overdue Exposure',
        'dso': 'Estimated DSO',
        'days': 'days',
        'chart_aging': 'AGING DISTRIBUTION',
        'chart_top': 'TOP 10 DEBTORS BY AMOUNT',
        'table_title': 'Master Open Items Registry',
        'export_btn': 'Export to CSV',
        'footer': 'CORPORATE AR SUITE'
    },
    'ES': {
        'login_title': 'ACCESO AR INTELLIGENCE',
        'login_token': 'Token de Acceso',
        'login_btn': 'Autenticar Sistema',
        'auth_error': 'Acceso denegado.',
        'header_subtitle': 'PLATAFORMA GLOBAL DE ANÁLISIS AR',
        'sidebar_data': 'ADMINISTRACIÓN DE DATOS',
        'sidebar_upload': 'Cargar SAP Aging Report',
        'sidebar_filters': 'FILTROS GLOBALES',
        'sidebar_segment': 'Segmento',
        'sidebar_entity': 'Contraparte',
        'sidebar_logout': 'Finalizar Sesión',
        'system_ready': 'Sistema Listo',
        'system_msg': 'Por favor, cargue el reporte de antigüedad de SAP en el panel lateral para inicializar el motor analítico.',
        'tab_portfolio': 'Visión de Portafolio',
        'tab_ops': 'Seguimiento Operativo',
        'kpi_gross': 'Deuda Bruta',
        'kpi_credits': 'Saldos a Favor',
        'kpi_delinquency': 'Índice de Morosidad',
        'kpi_limit': 'Excesos de Límite',
        'exec_metrics': 'Métricas Ejecutivas',
        'active_docs': 'documentos activos',
        'offset_amount': 'Monto a compensar',
        'vs_entities': 'Sobre entidades únicas',
        'total_entities': 'Total Entidades',
        'avg_ticket': 'Ticket Promedio',
        'exp_vencida': 'Exposición Vencida',
        'dso': 'DSO Estimado',
        'days': 'días',
        'chart_aging': 'DISTRIBUCIÓN DE ANTIGÜEDAD',
        'chart_top': 'TOP 10 CUENTAS POR MONTO',
        'table_title': 'Registro Maestro de Partidas Abiertas',
        'export_btn': 'Exportar Registro a CSV',
        'footer': 'VERSIÓN CORPORATIVA'
    }
}

# ═══════════════════════════════════════════════════════════════════════
# CSS CORPORATIVO (CORRECCIÓN DE CONTRASTE Y LOGO)
# ═══════════════════════════════════════════════════════════════════════

AMZ_MIDNIGHT = "#011E6A"
AMZ_ROYAL = "#0047AB"
AMZ_SKY = "#00A7E1"

def apply_theme():
    is_dark = st.session_state.theme == 'dark'
    bg_main = "#0B0F19" if is_dark else "#F8FAFC"
    card_bg = "#1E293B" if is_dark else "#FFFFFF"
    text_color = "#F8FAFC" if is_dark else "#0F172A"
    border_color = "#334155" if is_dark else "#E2E8F0"
    
    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_main}; color: {text_color}; }}
    
    /* Header Container */
    .header-container {{
        background-color: {card_bg};
        padding: 1.5rem 2rem;
        border-radius: 8px;
        border-bottom: 2px solid {AMZ_MIDNIGHT};
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    /* Sidebar Fix for Visibility */
    [data-testid="stSidebar"] {{ background-color: {AMZ_MIDNIGHT}; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    /* Multiselect and Selectbox contrast fix in Sidebar */
    [data-testid="stSidebar"] [data-baseweb="select"] * {{
        color: {text_color} !important; /* Forces readable text based on current theme */
    }}
    
    /* Uploader visibility fix */
    [data-testid="stFileUploader"] {{
        background-color: rgba(255,255,255,0.1);
        border: 1px dashed rgba(255,255,255,0.3);
        border-radius: 8px;
    }}
    
    /* KPI Cards */
    .kpi-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        border-top: 4px solid {AMZ_SKY};
    }}
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# LÓGICA DE NEGOCIO
# ═══════════════════════════════════════════════════════════════════════

def human_format(num):
    num = float(num)
    if abs(num) < 1000: return f"${num:,.0f}"
    if abs(num) < 1000000: return f"${num/1000:,.1f}K"
    return f"${num/1000000:,.1f}M"

def load_and_process_data(file):
    try:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        df = df[df['Document date'] != 'Result'].copy()
        num_cols = ['Open Amount', 'Credit Limit', 'Current Amount']
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        if 'SP #' in df.columns: df['SP #'] = df['SP #'].fillna("")
        df['Document date'] = pd.to_datetime(df['Document date'], errors='coerce')
        df['Net due date'] = pd.to_datetime(df['Net due date'], errors='coerce')
        return df, None
    except Exception as e: return None, str(e)

# ═══════════════════════════════════════════════════════════════════════
# FLUJO DE INTERFAZ
# ═══════════════════════════════════════════════════════════════════════

apply_theme()
lang = T[st.session_state.lang]

# Login Profesional
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        # Nota: Asegúrate de que el logo esté en la misma carpeta o usa una URL
        st.markdown(f"<h1 style='text-align:center; color:{AMZ_MIDNIGHT};'>AMRIZE</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:#64748B; letter-spacing:1px;'>{lang['header_subtitle']}</p>", unsafe_allow_html=True)
        with st.form("login"):
            token = st.text_input(lang['login_token'], type="password")
            if st.form_submit_button(lang['login_btn'], use_container_width=True):
                if token == st.secrets["APP_PASSWORD"]: # Usa tu secret de Streamlit
                    st.session_state.auth = True
                    st.rerun()
                else: st.error(lang['auth_error'])
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown(f"### {lang['sidebar_data']}")
    source_file = st.file_uploader(lang['sidebar_upload'], type=['csv', 'xlsx'])
    
    st.markdown("---")
    new_lang = st.selectbox("Language / Idioma", options=['EN', 'ES'], index=0 if st.session_state.lang == 'EN' else 1)
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()
        
    is_dark = st.toggle("Dark Mode", value=(st.session_state.theme == 'dark'))
    if (is_dark and st.session_state.theme == 'light') or (not is_dark and st.session_state.theme == 'dark'):
        st.session_state.theme = 'dark' if is_dark else 'light'
        st.rerun()

    if source_file:
        df_master, error = load_and_process_data(source_file)
        if not error:
            st.markdown(f"### {lang['sidebar_filters']}")
            tipo = st.multiselect(lang['sidebar_segment'], options=sorted(df_master['Counterparty Type'].unique()))
            cliente = st.multiselect(lang['sidebar_entity'], options=sorted(df_master['Counterparty Name'].unique()))
            dff = df_master.copy()
            if tipo: dff = dff[dff['Counterparty Type'].isin(tipo)]
            if cliente: dff = dff[dff['Counterparty Name'].isin(cliente)]
        else: st.error(error); st.stop()

# Dashboard Content
if 'dff' not in locals():
    st.markdown(f"""
    <div style="text-align:center; margin-top: 10rem; padding: 4rem; border: 1px dashed {AMZ_MIDNIGHT}; border-radius: 8px;">
        <h2 style="color: {AMZ_MIDNIGHT}; font-weight: 800;">{lang['system_ready']}</h2>
        <p style="color: #64748B;">{lang['system_msg']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Header Corporativo con Logo
st.markdown(f"""
    <div class="header-container">
        <div>
            <h1 style='margin:0; color:{AMZ_MIDNIGHT}; font-size:1.8rem; font-weight:800;'>AMRIZE INTELLIGENCE</h1>
            <p style='margin:0; color:#64748B; font-weight:600;'>{lang['header_subtitle']}</p>
        </div>
        <div style='text-align:right'>
            <p style='margin:0; color:#94A3B8; font-size:0.8rem;'>{datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# KPIs y Gráficos (Basado en lógica previa pero con traducciones y temas)
gross_debt = dff[dff['Open Amount'] > 0]['Open Amount'].sum()
credits = abs(dff[dff['Open Amount'] < 0]['Open Amount'].sum())
current_amt = dff['Current Amount'].sum()
overdue_pct = ((gross_debt - current_amt) / gross_debt * 100) if gross_debt > 0 else 0

tab1, tab2 = st.tabs([lang['tab_portfolio'], lang['tab_ops']])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1: kpi_card(lang["kpi_gross"], human_format(gross_debt), f"{len(dff)} {lang['active_docs']}")
    with col2: kpi_card(lang["kpi_credits"], human_format(credits), lang["offset_amount"], 'positive')
    with col3: kpi_card(lang["kpi_delinquency"], f"{overdue_pct:.1f}%", "Portfolio Health")
    with col4: kpi_card(lang["kpi_limit"], str(len(dff[dff['Open Amount'] > dff['Credit Limit']])), lang["vs_entities"])

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    chart_theme = "plotly_dark" if st.session_state.theme == 'dark' else "plotly_white"
    
    with c1:
        buckets = ['1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays', '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays']
        bucket_sums = [dff[b].sum() for b in buckets if b in dff.columns]
        fig_aging = go.Figure(go.Bar(x=[b.replace('\n', ' ') for b in buckets], y=bucket_sums, marker_color=AMZ_ROYAL))
        fig_aging.update_layout(title=lang['chart_aging'], template=chart_theme)
        st.plotly_chart(fig_aging, use_container_width=True)

    with c2:
        top_d = dff.groupby('Counterparty Name')['Open Amount'].sum().nlargest(10).sort_values()
        fig_top = px.bar(top_d, orientation='h', title=lang['chart_top'], color_discrete_sequence=[AMZ_SKY])
        fig_top.update_layout(template=chart_theme)
        st.plotly_chart(fig_top, use_container_width=True)

with tab2:
    st.markdown(f"### {lang['table_title']}")
    cols = ['Counterparty Name', 'Counterparty Type', 'INV # - Salesforce', 'SP #', 'Document date', 'Net due date', 'Open Amount', 'Credit Limit']
    st.dataframe(dff[cols].sort_values('Open Amount', ascending=False), use_container_width=True, hide_index=True,
        column_config={
            "Open Amount": st.column_config.NumberColumn("Amount", format="$ %.2f"),
            "Credit Limit": st.column_config.NumberColumn("Limit", format="$ %.2f"),
            "Document date": st.column_config.DateColumn("Doc Date"),
            "Net due date": st.column_config.DateColumn("Due Date")
        })

st.markdown(f"<div style='text-align:center; padding:3rem; color:#94A3B8; font-size:0.7rem; border-top:1px solid #E2E8F0;'>AMRIZE INTELLIGENCE | {lang['footer']} | © {datetime.now().year}</div>", unsafe_allow_html=True)