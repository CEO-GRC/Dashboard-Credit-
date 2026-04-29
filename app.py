"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AMRIZE AR INTELLIGENCE v1.3 - Global Enterprise Edition
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

# Inicializar estados si no existen
if 'theme' not in st.session_state: st.session_state.theme = 'light'
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'auth' not in st.session_state: st.session_state.auth = False

# ═══════════════════════════════════════════════════════════════════════
# DICCIONARIO DE TRADUCCIONES (US/LATAM)
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
        'chart_struct': 'Structural Analysis',
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
        'chart_struct': 'Análisis Estructural',
        'chart_aging': 'DISTRIBUCIÓN DE ANTIGÜEDAD',
        'chart_top': 'TOP 10 CUENTAS POR MONTO',
        'table_title': 'Registro Maestro de Partidas Abiertas',
        'export_btn': 'Exportar Registro a CSV',
        'footer': 'VERSIÓN CORPORATIVA'
    }
}

lang = T[st.session_state.lang]

# ═══════════════════════════════════════════════════════════════════════
# TEMAS Y CSS PROFESIONAL
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
    
    /* Header Corporativo */
    .header-container {{
        background-color: {card_bg};
        padding: 1.5rem 2rem;
        border-radius: 8px;
        border-left: 5px solid {AMZ_MIDNIGHT};
        border-right: 1px solid {border_color};
        border-top: 1px solid {border_color};
        border-bottom: 1px solid {border_color};
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
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
    
    /* File Uploader Legibility */
    [data-testid="stFileUploader"] {{
        background-color: {card_bg};
        border: 1px dashed {border_color};
        border-radius: 8px;
    }}
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] section {{
        color: {text_color} !important;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {AMZ_MIDNIGHT};
    }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{ gap: 24px; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 600; color: {text_color}; }}
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
        df = df[df['Document date'].astype(str).str.strip() != 'Result'].copy()
        num_cols = ['Open Amount', 'Credit Limit', 'Current Amount']
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        if 'SP #' in df.columns: df['SP #'] = df['SP #'].fillna("")
        df['Document date'] = pd.to_datetime(df['Document date'], errors='coerce')
        df['Net due date'] = pd.to_datetime(df['Net due date'], errors='coerce')
        return df, None
    except Exception as e:
        return None, str(e)

# ═══════════════════════════════════════════════════════════════════════
# FLUJO DE INTERFAZ
# ═══════════════════════════════════════════════════════════════════════

apply_theme()

# Login Profesional
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:{AMZ_MIDNIGHT}; letter-spacing:3px;'>AMRIZE</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:#64748B; text-transform:uppercase; letter-spacing:1px; font-size:0.8rem'>{lang['header_subtitle']}</p>", unsafe_allow_html=True)
        with st.form("login"):
            token = st.text_input(lang['login_token'], type="password")
            if st.form_submit_button(lang['login_btn'], use_container_width=True):
                if token == st.secrets["AR_PASSWORD"]:
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error(lang['auth_error'])
    st.stop()

# Barra Lateral (Controles de UI y Datos)
with st.sidebar:
    st.markdown(f"### {lang['sidebar_data']}")
    source_file = st.file_uploader(lang['sidebar_upload'], type=['csv', 'xlsx'])
    
    st.markdown("---")
    st.markdown(f"### UI SETTINGS")
    
    # Selector de Idioma
    new_lang = st.selectbox("Language", options=['EN', 'ES'], index=0 if st.session_state.lang == 'EN' else 1)
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()
        
    # Toggle de Tema
    is_dark = st.toggle("Dark Mode", value=(st.session_state.theme == 'dark'))
    new_theme = 'dark' if is_dark else 'light'
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
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
            
            if st.button(lang['sidebar_logout'], use_container_width=True):
                st.session_state.auth = False
                st.rerun()
        else:
            st.error(error)
            st.stop()
    else:
        st.stop()

# Dashboard Activo
st.markdown(f"""
    <div class="header-container">
        <h1 style='margin:0; color:{AMZ_MIDNIGHT}; font-size:1.6rem; font-weight:800;'>AMRIZE AR INTELLIGENCE</h1>
        <p style='margin:0; color:#64748B; font-size:0.85rem; font-weight:600;'>{lang['header_subtitle']} | {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
""", unsafe_allow_html=True)

# Lógica Financiera
gross_debt = dff[dff['Open Amount'] > 0]['Open Amount'].sum()
credits = abs(dff[dff['Open Amount'] < 0]['Open Amount'].sum())
current_amt = dff['Current Amount'].sum()
overdue_pct = ((gross_debt - current_amt) / gross_debt * 100) if gross_debt > 0 else 0

# Pestañas
tab_global, tab_op = st.tabs([lang['tab_portfolio'], lang['tab_ops']])

with tab_global:
    st.markdown(f"### {lang['exec_metrics']}")
    k1, k2, k3, k4 = st.columns(4)
    with k1: 
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">{lang["kpi_gross"]}</div><div class="kpi-value">{human_format(gross_debt)}</div><div style="font-size:0.7rem; color:#64748B;">{len(dff)} {lang["active_docs"]}</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">{lang["kpi_credits"]}</div><div class="kpi-value">{human_format(credits)}</div><div style="font-size:0.7rem; color:#059669;">{lang["offset_amount"]}</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">{lang["kpi_delinquency"]}</div><div class="kpi-value">{overdue_pct:.1f}%</div><div style="font-size:0.7rem; color:#DC2626;">Total Portfolio</div></div>', unsafe_allow_html=True)
    with k4:
        risk_count = len(dff[dff['Open Amount'] > dff['Credit Limit']])
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">{lang["kpi_limit"]}</div><div class="kpi-value">{risk_count}</div><div style="font-size:0.7rem; color:#D97706;">{lang["vs_entities"]}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    chart_theme = "plotly_dark" if st.session_state.theme == 'dark' else "plotly_white"
    
    with c1:
        buckets = ['1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays', '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays']
        bucket_sums = [dff[b].sum() for b in buckets if b in dff.columns]
        labels = [b.replace('\n', ' ') for b in buckets]
        fig_aging = go.Figure(go.Bar(x=labels, y=bucket_sums, marker_color=AMZ_ROYAL, text=[human_format(v) for v in bucket_sums], textposition='auto'))
        fig_aging.update_layout(title=lang['chart_aging'], height=400, template=chart_theme, margin=dict(t=80))
        st.plotly_chart(fig_aging, use_container_width=True)

    with c2:
        top_d = dff.groupby('Counterparty Name')['Open Amount'].sum().nlargest(10).sort_values()
        fig_top = px.bar(top_d, orientation='h', title=lang['chart_top'], color_discrete_sequence=[AMZ_SKY])
        fig_top.update_layout(height=400, template=chart_theme, showlegend=False, margin=dict(t=80))
        st.plotly_chart(fig_top, use_container_width=True)

with tab_op:
    st.markdown(f"### {lang['table_title']}")
    cols = ['Counterparty Name', 'Counterparty Type', 'INV # - Salesforce', 'SP #', 'Document date', 'Net due date', 'Open Amount', 'Credit Limit']
    df_view = dff[cols].copy()
    st.dataframe(df_view.sort_values('Open Amount', ascending=False), use_container_width=True, hide_index=True, height=500,
        column_config={
            "Open Amount": st.column_config.NumberColumn("Amount", format="$ %.2f"),
            "Credit Limit": st.column_config.NumberColumn("Limit", format="$ %.2f"),
            "Document date": st.column_config.DateColumn("Doc Date"),
            "Net due date": st.column_config.DateColumn("Due Date"),
            "SP #": st.column_config.TextColumn("Analyst Notes (SP)", width="large")
        })
    csv = df_view.to_csv(index=False).encode('utf-8')
    st.download_button(label=lang['export_btn'], data=csv, file_name=f"AR_Status_{datetime.now().strftime('%Y%m%d')}.csv", mime='text/csv')

st.markdown(f"<div style='text-align:center; padding:3rem; color:#94A3B8; font-size:0.7rem; border-top:1px solid #E2E8F0; margin-top:4rem;'>AMRIZE INTELLIGENCE | {lang['footer']} | © {datetime.now().year}</div>", unsafe_allow_html=True)