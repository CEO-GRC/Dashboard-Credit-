"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AMRIZE AR INTELLIGENCE v1.2 - Enterprise Edition
Plataforma de Análisis de Cuentas por Cobrar
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
# CONFIGURACIÓN DE PÁGINA
# ═══════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Amrize AR Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colores Corporativos
AMZ_MIDNIGHT = "#011E6A"
AMZ_ROYAL = "#0047AB"
AMZ_SKY = "#00A7E1"
S_GREEN = "#059669"
S_RED = "#DC2626"
S_AMBER = "#D97706"

# ═══════════════════════════════════════════════════════════════════════
# ESTILOS E INYECCIÓN CSS (LEGIBILIDAD Y PROFESIONALISMO)
# ═══════════════════════════════════════════════════════════════════════

def inject_enterprise_css():
    st.markdown(f"""
    <style>
    /* Estética Global */
    .main {{ background-color: #F8FAFC; }}
    
    /* Encabezado Corporativo */
    .header-container {{
        background-color: white;
        padding: 1.5rem 2rem;
        border-radius: 8px;
        border-left: 5px solid {AMZ_MIDNIGHT};
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }}
    
    /* Ajuste de Contraste File Uploader */
    [data-testid="stFileUploader"] {{
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
    }}
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] section {{
        color: {AMZ_MIDNIGHT} !important;
    }}
    
    /* KPI Cards */
    .kpi-card {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
    }}
    .kpi-label {{
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .kpi-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {AMZ_MIDNIGHT};
        margin-top: 5px;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {AMZ_MIDNIGHT};
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        font-weight: 600;
        font-size: 1rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# FUNCIONES OPERATIVAS
# ═══════════════════════════════════════════════════════════════════════

def human_format(num):
    num = float(num)
    if abs(num) < 1000: return f"${num:,.0f}"
    if abs(num) < 1000000: return f"${num/1000:,.1f}K"
    return f"${num/1000000:,.1f}M"

def load_and_process_data(file):
    try:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        # Regla SAP: Eliminar "Result"
        df = df[df['Document date'].astype(str).str.strip() != 'Result'].copy()
        
        # Limpieza Numérica
        num_cols = ['Open Amount', 'Credit Limit', 'Current Amount']
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        
        # Preservar notas SP #
        if 'SP #' in df.columns:
            df['SP #'] = df['SP #'].fillna("")
            
        # Fechas
        df['Document date'] = pd.to_datetime(df['Document date'], errors='coerce')
        df['Net due date'] = pd.to_datetime(df['Net due date'], errors='coerce')
        
        return df, None
    except Exception as e:
        return None, str(e)

# ═══════════════════════════════════════════════════════════════════════
# INTERFAZ Y SEGURIDAD
# ═══════════════════════════════════════════════════════════════════════

inject_enterprise_css()

# Autenticación Segura vía Secrets
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:{AMZ_MIDNIGHT}'>AMRIZE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748B; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem'>AR Intelligence Access</p>", unsafe_allow_html=True)
        with st.form("login"):
            token = st.text_input("Credencial de Acceso", type="password")
            if st.form_submit_button("Ingresar al Sistema", use_container_width=True):
                if token == st.secrets["AR_PASSWORD"]:
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Acceso denegado")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════
# DASHBOARD PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### Administración de Datos")
    source_file = st.file_uploader("Cargar SAP Aging Report", type=['csv', 'xlsx'])
    st.markdown("---")
    
    if source_file:
        df_master, error = load_and_process_data(source_file)
        if not error:
            # Filtros dinámicos
            st.markdown("### Filtros de Cartera")
            tipo = st.multiselect("Segmento", options=sorted(df_master['Counterparty Type'].unique()))
            cliente = st.multiselect("Contraparte", options=sorted(df_master['Counterparty Name'].unique()))
            
            dff = df_master.copy()
            if tipo: dff = dff[dff['Counterparty Type'].isin(tipo)]
            if cliente: dff = dff[dff['Counterparty Name'].isin(cliente)]
            
            if st.button("Finalizar Sesión", use_container_width=True):
                st.session_state.auth = False
                st.rerun()
        else:
            st.error(f"Error en archivo: {error}")
            st.stop()
    else:
        st.info("Sistema a la espera de datos.")
        st.stop()

# Header Corporativo
st.markdown(f"""
    <div class="header-container">
        <h1 style='margin:0; color:{AMZ_MIDNIGHT}; font-size:1.6rem'>AR Intelligence Dashboard</h1>
        <p style='margin:0; color:#64748B; font-size:0.9rem'>Análisis Estructural de Cuentas por Cobrar | Corte: {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
""", unsafe_allow_html=True)

# Lógica de KPIs
gross_debt = dff[dff['Open Amount'] > 0]['Open Amount'].sum()
credits = abs(dff[dff['Open Amount'] < 0]['Open Amount'].sum())
current_amt = dff['Current Amount'].sum()
overdue_pct = ((gross_debt - current_amt) / gross_debt * 100) if gross_debt > 0 else 0

# TABS FUNCIONALES
tab_global, tab_op = st.tabs(["Visión de Portafolio", "Seguimiento Operativo"])

with tab_global:
    # Fila de KPIs
    k1, k2, k3, k4 = st.columns(4)
    with k1: 
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Deuda Bruta</div><div class="kpi-value">{human_format(gross_debt)}</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Saldos a Favor</div><div class="kpi-value">{human_format(credits)}</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Índice de Morosidad</div><div class="kpi-value">{overdue_pct:.1f}%</div></div>', unsafe_allow_html=True)
    with k4:
        risk_count = len(dff[dff['Open Amount'] > dff['Credit Limit']])
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Excesos de Límite</div><div class="kpi-value">{risk_count}</div></div>', unsafe_allow_html=True)

    # Gráficos
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        # Aging Chart
        buckets = ['1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays', '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays']
        # Clean bucket labels for chart
        bucket_sums = [dff[b].sum() for b in buckets if b in dff.columns]
        labels = [b.replace('\n', ' ') for b in buckets]
        
        fig_aging = go.Figure(go.Bar(
            x=labels, y=bucket_sums,
            marker_color=AMZ_ROYAL,
            text=[human_format(v) for v in bucket_sums],
            textposition='auto',
        ))
        fig_aging.update_layout(title="Distribución de Antigüedad", height=400, plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=50, b=50, l=20, r=20))
        st.plotly_chart(fig_aging, use_container_width=True)

    with c2:
        # Top Debtors
        top_d = dff.groupby('Counterparty Name')['Open Amount'].sum().nlargest(10).sort_values()
        fig_top = px.bar(top_d, orientation='h', title="Top 10 Cuentas por Monto", color_discrete_sequence=[AMZ_SKY])
        fig_top.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis_title="Monto Abierto")
        st.plotly_chart(fig_top, use_container_width=True)

with tab_op:
    st.markdown("### Registro Maestro de Partidas Abiertas")
    
    # Configuración de tabla profesional
    cols = ['Counterparty Name', 'Counterparty Type', 'INV # - Salesforce', 'SP #', 'Document date', 'Net due date', 'Open Amount', 'Credit Limit']
    df_view = dff[cols].copy()
    
    st.dataframe(
        df_view.sort_values('Open Amount', ascending=False),
        use_container_width=True,
        hide_index=True,
        height=600,
        column_config={
            "Open Amount": st.column_config.NumberColumn("Monto Abierto", format="$ %.2f"),
            "Credit Limit": st.column_config.NumberColumn("Límite Crédito", format="$ %.2f"),
            "Document date": st.column_config.DateColumn("Fecha Doc"),
            "Net due date": st.column_config.DateColumn("Vencimiento"),
            "SP #": st.column_config.TextColumn("Notas de Gestión (SP)", width="large")
        }
    )
    
    # Exportación
    st.markdown("---")
    csv = df_view.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Exportar Registro a CSV",
        data=csv,
        file_name=f"AR_Status_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )

st.markdown(f"<div style='text-align:center; padding:2rem; color:#94A3B8; font-size:0.7rem'>AMRIZE INTELLIGENCE | CORPORATE AR SUITE | © {datetime.now().year}</div>", unsafe_allow_html=True)