import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import re

# ── CONFIGURACIÓN DE PÁGINA ──────────────────────────────────────────────────
st.set_page_config(
    page_title="AR Financial Intelligence | Suite",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── SISTEMA DE AUTENTICACIÓN ────────────────────────────────────────────────
if "auth_ok" not in st.session_state:
    st.session_state.auth_ok = False

def check_password():
    def validate():
        if st.session_state["pwd_input"] == st.secrets.get("APP_PASSWORD", "FINANZA2024"):
            st.session_state.auth_ok = True
            del st.session_state["pwd_input"]
        else:
            st.error("🔒 Código de acceso incorrecto.")

    if not st.session_state.auth_ok:
        st.markdown("<h1 style='text-align:center;'>AR Intelligence Dashboard</h1>", unsafe_allow_html=True)
        st.text_input("Ingrese Código de Acceso", type="password", on_change=validate, key="pwd_input")
        st.stop()

check_password()

# ── TEMA Y CSS PERSONALIZADO ────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Toggle de modo en Sidebar
with st.sidebar:
    st.title("Configuración")
    st.session_state.dark_mode = st.toggle("Modo Oscuro", value=st.session_state.dark_mode)

# Definición de Colores
if st.session_state.dark_mode:
    BG = "#0E1117"; CARD = "#1E1E1E"; TEXT = "#E0E0E0"; BORDER = "#333333"; ACCENT = "#00A7E1"
else:
    BG = "#F8F9FA"; CARD = "#FFFFFF"; TEXT = "#011E6A"; BORDER = "#DEE2E6"; ACCENT = "#0047AB"

ST_COLORS = ["#0047AB", "#00A7E1", "#059669", "#D97706", "#DC2626", "#6B7280"]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG}; color: {TEXT}; }}
    [data-testid="stMetricValue"] {{ font-size: 1.8rem !important; color: {ACCENT}; font-weight: 800; }}
    .kpi-card {{
        background-color: {CARD}; padding: 1.5rem; border-radius: 12px;
        border: 1px solid {BORDER}; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center; margin-bottom: 1rem;
    }}
    .kpi-label {{ font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: #6B7280; margin-bottom: 5px; }}
    .kpi-value {{ font-size: 1.6rem; font-weight: bold; color: {ACCENT}; }}
    </style>
""", unsafe_allow_html=True)

# ── HELPERS DE UI ──────────────────────────────────────────────────────────
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '${}{:.2f}{}'.format('-' if num < 0 else '', abs(num), ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def kpi_box(label, value):
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div></div>""", unsafe_allow_html=True)

# ── PROCESAMIENTO DE DATOS (SAP RULES) ──────────────────────────────────────
@st.cache_data
def process_ar_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    # 1. Eliminar duplicidad por subtotales SAP ("Result")
    if 'Document date' in df.columns:
        df = df[df['Document date'].astype(str).str.strip() != "Result"]

    # 2. Manejo de SP # (Notas vitales)
    if 'SP #' in df.columns:
        df['SP #'] = df['SP #'].fillna("Sin Notas")

    # 3. Limpieza Numérica Prusiana
    money_cols = ['Open Amount', 'Credit Limit', 'Current Amount', '1 - 30 days', '31 - 60 days', '61 - 90 days', '91 - 120 days', '121 - 180 days', '181 - 365 days', '> 365 days']
    for col in money_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).replace(r'[$,]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    # 4. Manejo de Fechas
    date_cols = ['Document date', 'Net due date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df

# ── CARGA DE ARCHIVO ───────────────────────────────────────────────────────
uploaded_file = st.sidebar.file_uploader("Cargar Reporte de Antigüedad (SAP)", type=["xlsx", "csv"])

if uploaded_file:
    df_raw = process_ar_data(uploaded_file)
    
    # Filtros Sidebar
    st.sidebar.markdown("---")
    cp_types = sorted(df_raw['Counterparty Type'].unique().tolist()) if 'Counterparty Type' in df_raw.columns else []
    selected_types = st.sidebar.multiselect("Tipo de Cliente", cp_types, default=cp_types)
    
    mask = df_raw['Counterparty Type'].isin(selected_types)
    df_filtered = df_raw[mask]
    
    cp_names = sorted(df_filtered['Counterparty Name'].unique().tolist()) if 'Counterparty Name' in df_filtered.columns else []
    selected_names = st.sidebar.multiselect("Filtrar por Cliente", cp_names)
    
    if selected_names:
        df_filtered = df_filtered[df_filtered['Counterparty Name'].isin(selected_names)]

    # ── LOGICA FINANCIERA ───────────────────────────────────────────────────
    deuda_bruta = df_filtered[df_filtered['Open Amount'] > 0]['Open Amount'].sum()
    saldos_favor = df_filtered[df_filtered['Open Amount'] < 0]['Open Amount'].sum()
    
    current_amt = df_filtered['Current Amount'].sum()
    vencido_amt = deuda_bruta - current_amt
    pct_vencido = (vencido_amt / deuda_bruta * 100) if deuda_bruta > 0 else 0
    
    # Riesgo de Crédito: Saldo total por cliente vs Credit Limit
    if 'Credit Limit' in df_filtered.columns:
        client_risk = df_filtered.groupby('Counterparty Name').agg({
            'Open Amount': 'sum',
            'Credit Limit': 'first'
        })
        riesgo_count = len(client_risk[client_risk['Open Amount'] > client_risk['Credit Limit']])
    else:
        riesgo_count = "N/A"

    # ── FILA 1: KPIs ────────────────────────────────────────────────────────
    st.title("💼 AR Financial Intelligence")
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_box("Deuda Bruta (AR)", human_format(deuda_bruta))
    with k2: kpi_box("Saldos a Favor (AP)", human_format(saldos_favor))
    with k3: kpi_box("% Vencido", f"{pct_vencido:.1f}%")
    with k4: kpi_box("Clientes Excedidos", f"⚠️ {riesgo_count}")

    # ── FILA 2: GRÁFICOS ────────────────────────────────────────────────────
    st.markdown("---")
    g1, g2 = st.columns([1, 1])

    with g1:
        # Gráfico de Aging (Cubetas)
        aging_labels = ['Current Amount', '1 - 30 days', '31 - 60 days', '61 - 90 days', '91 - 120 days', '121 - 180 days', '181 - 365 days', '> 365 days']
        aging_values = [df_filtered[col].sum() for col in aging_labels if col in df_filtered.columns]
        
        fig_aging = go.Figure(data=[go.Pie(
            labels=aging_labels, 
            values=aging_values, 
            hole=.5,
            marker=dict(colors=px.colors.qualitative.Bold)
        )])
        fig_aging.update_layout(title_text="Distribución de Antigüedad (Aging)", height=400, showlegend=True)
        st.plotly_chart(fig_aging, use_container_width=True)

    with g2:
        # Top 10 Deudores
        top_deudores = df_filtered.groupby('Counterparty Name')['Open Amount'].sum().nlargest(10).reset_index()
        fig_top = px.bar(
            top_deudores, 
            x='Open Amount', 
            y='Counterparty Name', 
            orientation='h',
            title="Top 10 Clientes por Deuda Abierta",
            color='Open Amount',
            color_continuous_scale='Blues'
        )
        fig_top.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
        st.plotly_chart(fig_top, use_container_width=True)

    # ── FILA 3: TABLA OPERATIVA ─────────────────────────────────────────────
    st.markdown("---")
    st.subheader("🔍 Detalle de Facturación y Notas de Analista")
    
    view_cols = [
        'Counterparty Name', 'Counterparty Type', 'INV #', 'SP #', 
        'Document date', 'Net due date', 'Open Amount', 'Credit Limit'
    ]
    
    # Asegurar que existan
    available_cols = [c for c in view_cols if c in df_filtered.columns]
    
    st.dataframe(
        df_filtered[available_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Open Amount": st.column_config.NumberColumn("Open Amount", format="$ %.2f"),
            "Credit Limit": st.column_config.NumberColumn("Credit Limit", format="$ %.2f"),
            "Document date": st.column_config.DateColumn("Doc Date"),
            "Net due date": st.column_config.DateColumn("Due Date"),
            "SP #": st.column_config.TextColumn("Notas Analista (SP)", width="large"),
        }
    )

    # Botón de Descarga
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Descargar Datos Filtrados (CSV)",
        csv,
        "ar_export.csv",
        "text/csv",
        key='download-csv'
    )

else:
    # Estado inicial sin archivo
    st.info("👆 Por favor, cargue un archivo SAP (Excel o CSV) desde la barra lateral para comenzar el análisis.")
    
    # Placeholder de UI para que no se vea vacío
    c1, c2, c3 = st.columns(3)
    c1.image("https://img.icons8.com/clouds/200/000000/data-configuration.png")
    c2.markdown("### Esperando Datos...")
    c2.write("El sistema aplicará las reglas de negocio de SAP automáticamente al cargar.")