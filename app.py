"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AMRIZE AR DASHBOARD v1.0
Dashboard Financiero de Cuentas por Cobrar (AR)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Desarrollado con Streamlit + Pandas + Plotly
Tema Dual: Light/Dark Mode
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
    page_title="Amrize AR Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════
# COLORES AMRIZE
# ═══════════════════════════════════════════════════════════════════════

AMZ_MIDNIGHT = "#011E6A"
AMZ_SKY = "#00A7E1"
AMZ_ROYAL = "#0047AB"
AMZ_GOLD = "#FFB800"
S_GREEN = "#059669"
S_RED = "#DC2626"
S_AMBER = "#D97706"
S_YELLOW = "#F59E0B"
S_GRAY = "#6B7280"

# ═══════════════════════════════════════════════════════════════════════
# FUNCIONES DE UTILIDAD
# ═══════════════════════════════════════════════════════════════════════

def human_format(num):
    """Formatear números grandes en K, M, B"""
    try:
        num = float(num)
        if abs(num) < 1000:
            return f"${num:,.0f}"
        elif abs(num) < 1000000:
            return f"${num/1000:,.1f}K"
        elif abs(num) < 1000000000:
            return f"${num/1000000:,.1f}M"
        else:
            return f"${num/1000000000:,.1f}B"
    except:
        return "$0"


def fmt_currency(value):
    """Formatear como moneda USD"""
    try:
        num = float(value)
        if pd.isna(num):
            return "$0.00"
        return f"${num:,.2f}"
    except:
        return "$0.00"


def fmt_pct(value):
    """Formatear como porcentaje"""
    try:
        num = float(value)
        if pd.isna(num):
            return "0.0%"
        return f"{num:.1f}%"
    except:
        return "0.0%"


def get_color_scheme(theme='light'):
    """Retornar esquema de colores según tema"""
    if theme == 'dark':
        return {
            'bg_primary': '#0F172A',
            'bg_secondary': '#1E293B',
            'bg_card': '#334155',
            'text_primary': '#F1F5F9',
            'text_secondary': '#94A3B8',
            'border': '#475569',
            'accent': AMZ_SKY
        }
    else:  # light
        return {
            'bg_primary': '#FFFFFF',
            'bg_secondary': '#F8FAFC',
            'bg_card': '#FFFFFF',
            'text_primary': '#0F172A',
            'text_secondary': '#64748B',
            'border': '#E2E8F0',
            'accent': AMZ_ROYAL
        }


# ═══════════════════════════════════════════════════════════════════════
# ESTILOS CSS DINÁMICOS
# ═══════════════════════════════════════════════════════════════════════

def inject_css(theme='light'):
    """Inyectar CSS personalizado según tema"""
    colors = get_color_scheme(theme)
    
    css = f"""
    <style>
    /* ===== RESET & GLOBAL ===== */
    .main {{
        background-color: {colors['bg_secondary']};
        color: {colors['text_primary']};
    }}
    
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }}
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {AMZ_MIDNIGHT} 0%, {AMZ_ROYAL} 100%);
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    /* ===== KPI CARDS ===== */
    .kpi-card {{
        background: {colors['bg_card']};
        border: 1px solid {colors['border']};
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        height: 100%;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }}
    
    .kpi-label {{
        font-size: 0.85rem;
        font-weight: 600;
        color: {colors['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }}
    
    .kpi-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {colors['text_primary']};
        margin: 0.5rem 0;
        line-height: 1;
    }}
    
    .kpi-delta {{
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }}
    
    .kpi-delta.positive {{
        color: {S_GREEN};
    }}
    
    .kpi-delta.negative {{
        color: {S_RED};
    }}
    
    .kpi-delta.neutral {{
        color: {colors['text_secondary']};
    }}
    
    /* ===== BUTTONS ===== */
    .stButton > button {{
        background: linear-gradient(135deg, {AMZ_ROYAL}, {AMZ_SKY});
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,71,171,0.3);
    }}
    
    /* ===== DATAFRAME ===== */
    .dataframe {{
        border: 1px solid {colors['border']} !important;
        border-radius: 8px;
        overflow: hidden;
    }}
    
    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {{
        background: {colors['bg_card']};
        border: 2px dashed {colors['border']};
        border-radius: 12px;
        padding: 2rem;
    }}
    
    /* ===== DIVIDER ===== */
    hr {{
        border: none;
        border-top: 2px solid {colors['border']};
        margin: 2rem 0;
    }}
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {{
        background: {colors['bg_card']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        font-weight: 600;
    }}
    
    /* ===== METRICS ===== */
    [data-testid="stMetric"] {{
        background: {colors['bg_card']};
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid {colors['border']};
    }}
    
    /* ===== HEADER GRADIENT ===== */
    .header-gradient {{
        background: linear-gradient(135deg, {AMZ_MIDNIGHT}, {AMZ_ROYAL});
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(1,30,106,0.2);
    }}
    
    .header-title {{
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    
    .header-subtitle {{
        color: {AMZ_SKY};
        font-size: 1.1rem;
        margin: 0.5rem 0 0;
        opacity: 0.9;
    }}
    
    /* ===== SECTION HEADERS ===== */
    .section-header {{
        font-size: 1.4rem;
        font-weight: 700;
        color: {colors['text_primary']};
        margin: 2rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid {AMZ_SKY};
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def kpi_card(label, value, delta=None, delta_type='neutral', icon='📊'):
    """Renderizar KPI card personalizado"""
    delta_class = f'kpi-delta {delta_type}'
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ''
    
    html = f"""
    <div class="kpi-card">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem">
            <span style="font-size:1.5rem">{icon}</span>
            <div class="kpi-label">{label}</div>
        </div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# AUTENTICACIÓN
# ═══════════════════════════════════════════════════════════════════════

def check_authentication():
    """Sistema de autenticación con secrets o fallback"""
    
    # Obtener contraseña de secrets o usar fallback
    try:
        correct_password = st.secrets.get("AR_PASSWORD", "AMRIZE2024")
    except:
        correct_password = "AMRIZE2024"
    
    # Inicializar estado de autenticación
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Si ya está autenticado, retornar True
    if st.session_state.authenticated:
        return True
    
    # Pantalla de login
    st.markdown(f"""
    <div style='text-align:center;padding:3rem;
                background:linear-gradient(135deg,{AMZ_MIDNIGHT},{AMZ_ROYAL});
                border-radius:20px;margin:4rem auto;max-width:500px;
                box-shadow:0 10px 30px rgba(1,30,106,0.3)'>
        <div style='font-size:4rem;margin-bottom:1.5rem'>🔐</div>
        <h1 style='color:white;margin:0;font-weight:700;font-size:2rem'>
            AMRIZE AR DASHBOARD
        </h1>
        <p style='color:{AMZ_SKY};margin:1rem 0 0;font-size:1.1rem'>
            Accounts Receivable Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulario de login
    with st.form("login_form", clear_on_submit=False):
        st.markdown("### 🔑 Acceso Seguro")
        password = st.text_input(
            "Ingrese la contraseña:",
            type="password",
            placeholder="Contraseña de acceso..."
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚀 Acceder al Dashboard",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            if password == correct_password:
                st.session_state.authenticated = True
                st.success("✅ Acceso concedido. Redirigiendo...")
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta. Intente nuevamente.")
    
    st.info("💡 **Nota:** Contacte al administrador si no tiene credenciales de acceso.")
    
    return False


# ═══════════════════════════════════════════════════════════════════════
# PROCESAMIENTO DE DATOS
# ═══════════════════════════════════════════════════════════════════════

def load_and_process_data(uploaded_file):
    """
    Cargar y procesar el archivo AR de SAP
    
    REGLAS CRÍTICAS:
    1. Eliminar filas donde Document date == "Result"
    2. Convertir fechas a datetime
    3. Limpiar valores numéricos (remover comas)
    4. Preservar SP # con nulos
    """
    
    try:
        # Leer archivo
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # ─────────────────────────────────────────────────────────────────
        # PASO 1: ELIMINAR FILAS "Result" (Subtotales de SAP)
        # ─────────────────────────────────────────────────────────────────
        initial_rows = len(df)
        df = df[df['Document date'] != 'Result'].copy()
        removed_rows = initial_rows - len(df)
        
        if removed_rows > 0:
            st.info(f"ℹ️ Se eliminaron {removed_rows} filas de subtotales SAP ('Result')")
        
        # ─────────────────────────────────────────────────────────────────
        # PASO 2: CONVERTIR FECHAS
        # ─────────────────────────────────────────────────────────────────
        df['Document date'] = pd.to_datetime(df['Document date'], errors='coerce')
        df['Net due date'] = pd.to_datetime(df['Net due date'], errors='coerce')
        
        # ─────────────────────────────────────────────────────────────────
        # PASO 3: LIMPIAR COLUMNAS NUMÉRICAS
        # ─────────────────────────────────────────────────────────────────
        numeric_columns = [
            'Open Amount',
            'Credit Limit',
            'Current Amount',
            '1 - 30\ndays',
            '31 - 60\ndays',
            '61 - 90\ndays',
            '91 - 120\ndays',
            '121 - 180\ndays',
            '181 - 365\ndays',
            '> 365\ndays'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                # Convertir a string, remover comas, convertir a float
                df[col] = df[col].astype(str).str.replace(',', '').replace('nan', '0')
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # ─────────────────────────────────────────────────────────────────
        # PASO 4: PRESERVAR SP # (CRUCIAL PARA ANALISTAS)
        # ─────────────────────────────────────────────────────────────────
        # SP # puede tener valores nulos - preservarlos como están
        if 'SP #' in df.columns:
            df['SP #'] = df['SP #'].astype(str).replace('nan', '').replace('None', '')
        
        # ─────────────────────────────────────────────────────────────────
        # PASO 5: CREAR COLUMNAS CALCULADAS
        # ─────────────────────────────────────────────────────────────────
        
        # Clasificar deuda vs saldo a favor
        df['Debt_Type'] = df['Open Amount'].apply(
            lambda x: 'Deuda' if x > 0 else ('Saldo a Favor' if x < 0 else 'Cero')
        )
        
        # Calcular días vencidos
        today = pd.Timestamp.now()
        df['Days_Overdue'] = (today - df['Net due date']).dt.days
        df['Days_Overdue'] = df['Days_Overdue'].fillna(0).astype(int)
        
        # Clasificar estado de vencimiento
        df['Status'] = df.apply(lambda row: 
            'Vencida' if row['Days_Overdue'] > 0 and row['Open Amount'] > 0
            else 'Al Día' if row['Open Amount'] > 0
            else 'Saldo a Favor',
            axis=1
        )
        
        # Detectar riesgo de crédito
        df['Over_Credit_Limit'] = (df['Open Amount'] > df['Credit Limit']) & (df['Credit Limit'] > 0)
        
        return df, None
        
    except Exception as e:
        return None, f"Error procesando archivo: {str(e)}"


# ═══════════════════════════════════════════════════════════════════════
# CÁLCULO DE KPIs
# ═══════════════════════════════════════════════════════════════════════

def calculate_kpis(df):
    """Calcular todos los KPIs del dashboard"""
    
    kpis = {}
    
    # ───────────────────────────────────────────────────────────────────
    # KPI 1: DEUDA BRUTA (Solo positivos)
    # ───────────────────────────────────────────────────────────────────
    kpis['gross_debt'] = df[df['Open Amount'] > 0]['Open Amount'].sum()
    
    # ───────────────────────────────────────────────────────────────────
    # KPI 2: SALDOS A FAVOR (Solo negativos - valor absoluto)
    # ───────────────────────────────────────────────────────────────────
    kpis['credits'] = abs(df[df['Open Amount'] < 0]['Open Amount'].sum())
    
    # ───────────────────────────────────────────────────────────────────
    # KPI 3: % VENCIDO VS AL DÍA
    # ───────────────────────────────────────────────────────────────────
    current_amount = df[df['Open Amount'] > 0]['Current Amount'].sum()
    kpis['pct_current'] = (current_amount / kpis['gross_debt'] * 100) if kpis['gross_debt'] > 0 else 0
    kpis['pct_overdue'] = 100 - kpis['pct_current']
    kpis['current_amount'] = current_amount
    kpis['overdue_amount'] = kpis['gross_debt'] - current_amount
    
    # ───────────────────────────────────────────────────────────────────
    # KPI 4: RIESGO DE CRÉDITO
    # ───────────────────────────────────────────────────────────────────
    # Agrupar por cliente y calcular total por cliente
    client_totals = df.groupby('Counterparty Name').agg({
        'Open Amount': 'sum',
        'Credit Limit': 'first'  # Asumir que el límite es el mismo por cliente
    }).reset_index()
    
    # Contar clientes que exceden su límite
    kpis['credit_risk_count'] = len(
        client_totals[(client_totals['Open Amount'] > client_totals['Credit Limit']) & 
                     (client_totals['Credit Limit'] > 0)]
    )
    
    # ───────────────────────────────────────────────────────────────────
    # MÉTRICAS ADICIONALES
    # ───────────────────────────────────────────────────────────────────
    kpis['total_invoices'] = len(df)
    kpis['unique_customers'] = df['Counterparty Name'].nunique()
    kpis['avg_invoice'] = kpis['gross_debt'] / kpis['total_invoices'] if kpis['total_invoices'] > 0 else 0
    
    # DSO (Days Sales Outstanding) - Aproximado
    kpis['avg_days_overdue'] = df[df['Days_Overdue'] > 0]['Days_Overdue'].mean()
    if pd.isna(kpis['avg_days_overdue']):
        kpis['avg_days_overdue'] = 0
    
    return kpis


# ═══════════════════════════════════════════════════════════════════════
# VISUALIZACIONES
# ═══════════════════════════════════════════════════════════════════════

def create_aging_chart(df, theme='light'):
    """Gráfico de antigüedad (Aging Buckets)"""
    
    # Columnas de aging
    aging_cols = [
        'Current Amount',
        '1 - 30\ndays',
        '31 - 60\ndays',
        '61 - 90\ndays',
        '91 - 120\ndays',
        '121 - 180\ndays',
        '181 - 365\ndays',
        '> 365\ndays'
    ]
    
    # Sumar cada bucket (incluye negativos naturalmente)
    aging_data = []
    for col in aging_cols:
        if col in df.columns:
            total = df[col].sum()
            # Usar valor absoluto para visualización si es negativo
            aging_data.append({
                'Bucket': col.replace('\n', ' '),
                'Amount': abs(total),
                'Original_Amount': total
            })
    
    df_aging = pd.DataFrame(aging_data)
    
    # Colores degradados
    colors = [S_GREEN, AMZ_SKY, AMZ_ROYAL, S_AMBER, S_YELLOW, '#FFA500', '#FF6B35', S_RED]
    
    # Crear gráfico
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_aging['Bucket'],
        y=df_aging['Amount'],
        marker=dict(
            color=colors[:len(df_aging)],
            line=dict(color='white', width=2)
        ),
        text=[human_format(v) for v in df_aging['Amount']],
        textposition='outside',
        textfont=dict(size=11, weight='bold'),
        hovertemplate='<b>%{x}</b><br>Monto: $%{y:,.2f}<extra></extra>'
    ))
    
    bg_color = '#0F172A' if theme == 'dark' else 'white'
    text_color = '#F1F5F9' if theme == 'dark' else '#0F172A'
    grid_color = '#475569' if theme == 'dark' else '#E2E8F0'
    
    fig.update_layout(
        title={
            'text': '📊 Distribución por Antigüedad (Aging)',
            'font': {'size': 18, 'weight': 'bold', 'color': text_color}
        },
        xaxis_title='Período',
        yaxis_title='Monto (USD)',
        height=450,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, family='Arial', size=11),
        margin=dict(l=50, r=50, t=80, b=80),
        xaxis=dict(
            showgrid=False,
            tickangle=-45,
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            gridwidth=1
        ),
        hovermode='x unified'
    )
    
    return fig


def create_top_debtors_chart(df, top_n=10, theme='light'):
    """Gráfico de Top N deudores"""
    
    # Agrupar por cliente y sumar deuda (solo positivos)
    debtors = df[df['Open Amount'] > 0].groupby('Counterparty Name').agg({
        'Open Amount': 'sum'
    }).reset_index()
    
    # Ordenar y tomar top N
    debtors = debtors.sort_values('Open Amount', ascending=True).tail(top_n)
    
    # Asignar colores por ranking
    colors = []
    for i in range(len(debtors)):
        if i >= len(debtors) - 3:  # Top 3
            colors.append(S_RED)
        elif i >= len(debtors) - 5:  # 4-5
            colors.append(S_AMBER)
        else:
            colors.append(AMZ_SKY)
    
    # Crear gráfico
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=debtors['Counterparty Name'],
        x=debtors['Open Amount'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='white', width=1)
        ),
        text=[human_format(v) for v in debtors['Open Amount']],
        textposition='outside',
        textfont=dict(size=11, weight='bold'),
        hovertemplate='<b>%{y}</b><br>Deuda: $%{x:,.2f}<extra></extra>'
    ))
    
    bg_color = '#0F172A' if theme == 'dark' else 'white'
    text_color = '#F1F5F9' if theme == 'dark' else '#0F172A'
    grid_color = '#475569' if theme == 'dark' else '#E2E8F0'
    
    fig.update_layout(
        title={
            'text': f'🏆 Top {top_n} Deudores',
            'font': {'size': 18, 'weight': 'bold', 'color': text_color}
        },
        xaxis_title='Monto Adeudado (USD)',
        yaxis_title='',
        height=450,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, family='Arial', size=11),
        margin=dict(l=200, r=80, t=80, b=50),
        xaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            gridwidth=1
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=10)
        ),
        hovermode='y unified'
    )
    
    return fig


def create_status_pie_chart(df, theme='light'):
    """Gráfico circular de estado de cuentas"""
    
    # Contar por estado (solo deuda positiva)
    df_debt = df[df['Open Amount'] > 0].copy()
    status_counts = df_debt.groupby('Status').agg({
        'Open Amount': 'sum'
    }).reset_index()
    
    # Colores
    color_map = {
        'Al Día': S_GREEN,
        'Vencida': S_RED,
        'Saldo a Favor': AMZ_SKY
    }
    
    colors = [color_map.get(status, S_GRAY) for status in status_counts['Status']]
    
    fig = go.Figure(data=[go.Pie(
        labels=status_counts['Status'],
        values=status_counts['Open Amount'],
        hole=0.4,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='label+percent',
        textfont=dict(size=12, weight='bold'),
        hovertemplate='<b>%{label}</b><br>Monto: $%{value:,.2f}<br>%{percent}<extra></extra>'
    )])
    
    bg_color = '#0F172A' if theme == 'dark' else 'white'
    text_color = '#F1F5F9' if theme == 'dark' else '#0F172A'
    
    fig.update_layout(
        title={
            'text': '📈 Estado de Cuentas',
            'font': {'size': 18, 'weight': 'bold', 'color': text_color}
        },
        height=450,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, family='Arial', size=11),
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.05
        )
    )
    
    return fig


# ═══════════════════════════════════════════════════════════════════════
# APLICACIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Función principal del dashboard"""
    
    # ═══════════════════════════════════════════════════════════════════
    # AUTENTICACIÓN
    # ═══════════════════════════════════════════════════════════════════
    if not check_authentication():
        return
    
    # ═══════════════════════════════════════════════════════════════════
    # INICIALIZAR ESTADO
    # ═══════════════════════════════════════════════════════════════════
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # ═══════════════════════════════════════════════════════════════════
    # INYECTAR CSS
    # ═══════════════════════════════════════════════════════════════════
    inject_css(st.session_state.theme)
    
    # ═══════════════════════════════════════════════════════════════════
    # HEADER PRINCIPAL
    # ═══════════════════════════════════════════════════════════════════
    col_header1, col_header2 = st.columns([4, 1])
    
    with col_header1:
        st.markdown(f"""
        <div class="header-gradient">
            <h1 class="header-title">💰 AMRIZE AR DASHBOARD</h1>
            <p class="header-subtitle">Accounts Receivable Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_header2:
        st.markdown("<br>", unsafe_allow_html=True)
        # Toggle de tema
        theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        if st.button(f"{theme_icon} Cambiar Tema", use_container_width=True):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()
    
    # ═══════════════════════════════════════════════════════════════════
    # SIDEBAR
    # ═══════════════════════════════════════════════════════════════════
    with st.sidebar:
        st.markdown("### 📁 Carga de Datos")
        
        uploaded_file = st.file_uploader(
            "Seleccione archivo AR Report",
            type=['csv', 'xlsx', 'xls'],
            help="Archivo de Cuentas por Cobrar de SAP"
        )
        
        st.markdown("---")
        
        if uploaded_file is not None:
            # Procesar datos
            with st.spinner("🔄 Procesando datos..."):
                df, error = load_and_process_data(uploaded_file)
            
            if error:
                st.error(f"❌ {error}")
                return
            
            if df is None or len(df) == 0:
                st.warning("⚠️ No se encontraron datos válidos")
                return
            
            # Guardar en session_state
            st.session_state.df = df
            
            st.success(f"✅ {len(df)} registros cargados")
            
            # ═══════════════════════════════════════════════════════════
            # FILTROS
            # ═══════════════════════════════════════════════════════════
            st.markdown("### 🔍 Filtros")
            
            # Filtro 1: Tipo de Cliente
            all_types = ['Todos'] + sorted(df['Counterparty Type'].dropna().unique().tolist())
            selected_types = st.multiselect(
                "Tipo de Cliente",
                options=all_types,
                default=['Todos']
            )
            
            # Filtro 2: Cliente específico
            if 'Todos' in selected_types or not selected_types:
                available_clients = sorted(df['Counterparty Name'].dropna().unique().tolist())
            else:
                available_clients = sorted(
                    df[df['Counterparty Type'].isin([t for t in selected_types if t != 'Todos'])]['Counterparty Name'].dropna().unique().tolist()
                )
            
            all_clients = ['Todos'] + available_clients
            selected_clients = st.multiselect(
                "Cliente",
                options=all_clients,
                default=['Todos']
            )
            
            # Aplicar filtros
            df_filtered = df.copy()
            
            if 'Todos' not in selected_types and selected_types:
                df_filtered = df_filtered[df_filtered['Counterparty Type'].isin(selected_types)]
            
            if 'Todos' not in selected_clients and selected_clients:
                df_filtered = df_filtered[df_filtered['Counterparty Name'].isin(selected_clients)]
            
            # Guardar filtrado
            st.session_state.df_filtered = df_filtered
            
            st.markdown("---")
            st.info(f"📊 **{len(df_filtered)}** registros filtrados")
            
            # Botón de logout
            st.markdown("---")
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
        
        else:
            st.info("👆 Suba un archivo para comenzar")
    
    # ═══════════════════════════════════════════════════════════════════
    # CONTENIDO PRINCIPAL
    # ═══════════════════════════════════════════════════════════════════
    
    if 'df_filtered' not in st.session_state:
        # Mostrar mensaje de bienvenida
        st.markdown("""
        ## 👋 Bienvenido al Dashboard de AR
        
        ### 📋 Instrucciones:
        
        1. **Cargue un archivo** de Cuentas por Cobrar usando el panel lateral
        2. **Aplique filtros** según necesite (Tipo de Cliente, Cliente específico)
        3. **Analice los KPIs** en la sección superior
        4. **Explore visualizaciones** interactivas
        5. **Revise la tabla detallada** al final
        
        ### ✨ Características:
        
        - 🎨 Modo Claro/Oscuro
        - 📊 KPIs ejecutivos en tiempo real
        - 📈 Gráficos interactivos (Aging, Top Deudores)
        - 🔍 Filtros dinámicos
        - 📥 Exportación de datos
        - 🔐 Acceso seguro con contraseña
        
        ---
        
        💡 **Nota:** El sistema detecta y elimina automáticamente subtotales de SAP (filas "Result")
        """)
        
        return
    
    # Obtener datos filtrados
    df_filtered = st.session_state.df_filtered
    
    # Calcular KPIs
    kpis = calculate_kpis(df_filtered)
    
    # ═══════════════════════════════════════════════════════════════════
    # SECCIÓN 1: KPIs PRINCIPALES
    # ═══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">📊 Indicadores Clave (KPIs)</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        kpi_card(
            label="Deuda Bruta",
            value=human_format(kpis['gross_debt']),
            delta=f"{kpis['total_invoices']} facturas",
            delta_type='neutral',
            icon='💵'
        )
    
    with col2:
        kpi_card(
            label="Saldos a Favor",
            value=human_format(kpis['credits']),
            delta="Créditos del cliente",
            delta_type='positive',
            icon='💚'
        )
    
    with col3:
        delta_text = f"Vencido: {fmt_pct(kpis['pct_overdue'])}"
        delta_type = 'negative' if kpis['pct_overdue'] > 50 else 'neutral'
        kpi_card(
            label="% Al Día",
            value=fmt_pct(kpis['pct_current']),
            delta=delta_text,
            delta_type=delta_type,
            icon='📈'
        )
    
    with col4:
        delta_text = f"De {kpis['unique_customers']} clientes"
        delta_type = 'negative' if kpis['credit_risk_count'] > 0 else 'positive'
        kpi_card(
            label="Riesgo de Crédito",
            value=str(kpis['credit_risk_count']),
            delta=delta_text,
            delta_type=delta_type,
            icon='⚠️'
        )
    
    # KPIs secundarios
    st.markdown("<br>", unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            "💼 Total Clientes",
            f"{kpis['unique_customers']:,}",
            delta=None
        )
    
    with col6:
        st.metric(
            "📄 Promedio por Factura",
            human_format(kpis['avg_invoice']),
            delta=None
        )
    
    with col7:
        st.metric(
            "🔴 Monto Vencido",
            human_format(kpis['overdue_amount']),
            delta=f"{fmt_pct(kpis['pct_overdue'])} del total",
            delta_color='inverse'
        )
    
    with col8:
        st.metric(
            "⏱️ Días Prom. Vencido",
            f"{int(kpis['avg_days_overdue'])}",
            delta="DSO Aproximado"
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # SECCIÓN 2: VISUALIZACIONES
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown('<div class="section-header">📈 Análisis Visual</div>', unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig_aging = create_aging_chart(df_filtered, st.session_state.theme)
        st.plotly_chart(fig_aging, use_container_width=True)
    
    with col_chart2:
        fig_top = create_top_debtors_chart(df_filtered, top_n=10, theme=st.session_state.theme)
        st.plotly_chart(fig_top, use_container_width=True)
    
    # Gráfico de estado (full width)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_pie1, col_pie2, col_pie3 = st.columns([1, 2, 1])
    with col_pie2:
        fig_status = create_status_pie_chart(df_filtered, st.session_state.theme)
        st.plotly_chart(fig_status, use_container_width=True)
    
    # ═══════════════════════════════════════════════════════════════════
    # SECCIÓN 3: TABLA OPERATIVA
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown('<div class="section-header">📋 Tabla Detallada de Facturas</div>', unsafe_allow_html=True)
    
    # Seleccionar columnas para mostrar
    display_columns = [
        'Counterparty Name',
        'Counterparty Type',
        'INV # - Salesforce',
        'SP #',
        'Document date',
        'Net due date',
        'Open Amount',
        'Credit Limit',
        'Status',
        'Days_Overdue'
    ]
    
    # Crear DataFrame para display
    df_display = df_filtered[display_columns].copy()
    
    # Renombrar columnas
    df_display.columns = [
        'Cliente',
        'Tipo',
        'INV #',
        'SP #',
        'Fecha Documento',
        'Fecha Vencimiento',
        'Monto Abierto',
        'Límite Crédito',
        'Estado',
        'Días Vencido'
    ]
    
    # Ordenar por Monto Abierto descendente
    df_display = df_display.sort_values('Monto Abierto', ascending=False)
    
    # Configurar formato de columnas
    column_config = {
        'Monto Abierto': st.column_config.NumberColumn(
            'Monto Abierto',
            format='$%.2f',
            help='Saldo pendiente en USD'
        ),
        'Límite Crédito': st.column_config.NumberColumn(
            'Límite Crédito',
            format='$%.2f',
            help='Límite de crédito aprobado'
        ),
        'Fecha Documento': st.column_config.DateColumn(
            'Fecha Documento',
            format='YYYY-MM-DD'
        ),
        'Fecha Vencimiento': st.column_config.DateColumn(
            'Fecha Vencimiento',
            format='YYYY-MM-DD'
        ),
        'Estado': st.column_config.TextColumn(
            'Estado',
            help='Estado de la factura'
        ),
        'Días Vencido': st.column_config.NumberColumn(
            'Días Vencido',
            format='%d días',
            help='Días desde vencimiento'
        )
    }
    
    # Mostrar tabla
    st.dataframe(
        df_display,
        use_container_width=True,
        height=500,
        column_config=column_config,
        hide_index=True
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # SECCIÓN 4: EXPORTAR DATOS
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown('<div class="section-header">📥 Exportar Datos</div>', unsafe_allow_html=True)
    
    col_export1, col_export2, col_export3 = st.columns([2, 2, 3])
    
    with col_export1:
        # Exportar a Excel
        if st.button("📊 Exportar a Excel", use_container_width=True, type="primary"):
            try:
                # Crear archivo Excel
                output = BytesIO()
                
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    # Sheet 1: Datos completos
                    df_display.to_excel(writer, sheet_name='Datos Completos', index=False)
                    
                    # Sheet 2: Resumen KPIs
                    kpi_summary = pd.DataFrame({
                        'KPI': [
                            'Deuda Bruta',
                            'Saldos a Favor',
                            'Monto Al Día',
                            'Monto Vencido',
                            '% Al Día',
                            '% Vencido',
                            'Clientes en Riesgo',
                            'Total Clientes',
                            'Total Facturas',
                            'Promedio por Factura',
                            'Días Prom. Vencido'
                        ],
                        'Valor': [
                            fmt_currency(kpis['gross_debt']),
                            fmt_currency(kpis['credits']),
                            fmt_currency(kpis['current_amount']),
                            fmt_currency(kpis['overdue_amount']),
                            fmt_pct(kpis['pct_current']),
                            fmt_pct(kpis['pct_overdue']),
                            kpis['credit_risk_count'],
                            kpis['unique_customers'],
                            kpis['total_invoices'],
                            fmt_currency(kpis['avg_invoice']),
                            f"{int(kpis['avg_days_overdue'])} días"
                        ]
                    })
                    kpi_summary.to_excel(writer, sheet_name='Resumen KPIs', index=False)
                
                output.seek(0)
                
                # Botón de descarga
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                st.download_button(
                    label="⬇️ Descargar Excel",
                    data=output,
                    file_name=f"AR_Report_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                st.success("✅ Archivo generado correctamente")
                
            except Exception as e:
                st.error(f"❌ Error al exportar: {str(e)}")
    
    with col_export2:
        # Exportar a CSV
        if st.button("📄 Exportar a CSV", use_container_width=True):
            try:
                csv = df_display.to_csv(index=False)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                st.download_button(
                    label="⬇️ Descargar CSV",
                    data=csv,
                    file_name=f"AR_Report_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                st.success("✅ Archivo CSV generado")
                
            except Exception as e:
                st.error(f"❌ Error al exportar: {str(e)}")
    
    with col_export3:
        st.info("""
        **💡 Opciones de exportación:**
        - **Excel**: Incluye datos + resumen KPIs
        - **CSV**: Solo datos tabulares
        """)
    
    # ═══════════════════════════════════════════════════════════════════
    # FOOTER
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center;padding:1.5rem;color:{S_GRAY}'>
        <p style='margin:0;font-size:0.9rem'>
            💼 <strong>AMRIZE AR Dashboard v1.0</strong> | 
            Desarrollado con Streamlit | 
            © {datetime.now().year}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# EJECUTAR APLICACIÓN
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
