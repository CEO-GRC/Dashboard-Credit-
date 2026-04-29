"""
AMRIZE AR DASHBOARD v2.0
Professional Accounts Receivable Analytics Platform
Bilingual | Dark/Light Mode | Tabbed Interface
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
import base64

# ═══════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Amrize Trading Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════
# BRAND COLORS
# ═══════════════════════════════════════════════════════════════════════

AMZ_MIDNIGHT = "#011E6A"
AMZ_SKY = "#00A7E1"
AMZ_ROYAL = "#0047AB"
S_GREEN = "#059669"
S_RED = "#DC2626"
S_AMBER = "#D97706"
S_GRAY = "#6B7280"

# ═══════════════════════════════════════════════════════════════════════
# TRANSLATIONS
# ═══════════════════════════════════════════════════════════════════════

TRANSLATIONS = {
    'en': {
        'title': 'TRADING DASHBOARD',
        'subtitle': 'Accounts Receivable Analytics',
        'login_title': 'Access Control',
        'password': 'Password',
        'sign_in': 'Sign In',
        'sign_out': 'Sign Out',
        'invalid_credentials': 'Invalid credentials',
        'data_source': 'DATA SOURCE',
        'upload': 'Upload AR Report',
        'upload_help': 'SAP Accounts Receivable export file',
        'processing': 'Processing...',
        'records_loaded': 'records loaded',
        'subtotals_removed': 'SAP subtotals removed',
        'no_data': 'No valid data found',
        'filters': 'FILTERS',
        'counterparty_type': 'Counterparty Type',
        'counterparty': 'Counterparty',
        'all': 'All',
        'filtered_records': 'Filtered Records',
        'upload_to_begin': 'Upload a file to begin',
        'upload_message': 'Upload an AR report file to begin analysis',
        'kpi_header': 'KEY PERFORMANCE INDICATORS',
        'gross_receivables': 'Gross Receivables',
        'customer_credits': 'Customer Credits',
        'current_pct': 'Current %',
        'credit_risk': 'Credit Risk',
        'invoices': 'invoices',
        'advance_payments': 'Advance payments',
        'overdue': 'Overdue',
        'of': 'of',
        'customers': 'customers',
        'total_customers': 'Total Customers',
        'avg_invoice': 'Avg Invoice',
        'overdue_amount': 'Overdue Amount',
        'avg_days_overdue': 'Avg Days Overdue',
        'analytics': 'ANALYTICS',
        'aging_analysis': 'Aging Analysis',
        'top_debtors': 'Top Debtors',
        'portfolio_status': 'Portfolio Status',
        'amount_usd': 'Amount (USD)',
        'outstanding_usd': 'Outstanding Amount (USD)',
        'detailed_records': 'DETAILED RECORDS',
        'customer': 'Customer',
        'type': 'Type',
        'invoice': 'Invoice #',
        'doc_date': 'Doc Date',
        'due_date': 'Due Date',
        'open_amount': 'Open Amount',
        'credit_limit': 'Credit Limit',
        'status': 'Status',
        'days_overdue_col': 'Days Overdue',
        'export_excel': 'Export Excel',
        'export_csv': 'Export CSV',
        'download': 'Download',
        'export_error': 'Export error',
        'overview': 'Overview',
        'aging': 'Aging',
        'customers_tab': 'Customers',
        'exports': 'Export',
        'current': 'Current',
        'overdue_status': 'Overdue',
        'credit': 'Credit'
    },
    'es': {
        'title': 'DASHBOARD AR',
        'subtitle': 'Análisis de Cuentas por Cobrar',
        'login_title': 'Control de Acceso',
        'password': 'Contraseña',
        'sign_in': 'Ingresar',
        'sign_out': 'Cerrar Sesión',
        'invalid_credentials': 'Credenciales inválidas',
        'data_source': 'FUENTE DE DATOS',
        'upload': 'Cargar Reporte AR',
        'upload_help': 'Archivo de exportación de SAP',
        'processing': 'Procesando...',
        'records_loaded': 'registros cargados',
        'subtotals_removed': 'subtotales SAP eliminados',
        'no_data': 'No se encontraron datos válidos',
        'filters': 'FILTROS',
        'counterparty_type': 'Tipo de Contraparte',
        'counterparty': 'Contraparte',
        'all': 'Todos',
        'filtered_records': 'Registros Filtrados',
        'upload_to_begin': 'Cargue un archivo para comenzar',
        'upload_message': 'Cargue un archivo de reporte AR para comenzar el análisis',
        'kpi_header': 'INDICADORES CLAVE DE DESEMPEÑO',
        'gross_receivables': 'Cuentas por Cobrar',
        'customer_credits': 'Créditos de Clientes',
        'current_pct': '% Al Día',
        'credit_risk': 'Riesgo de Crédito',
        'invoices': 'facturas',
        'advance_payments': 'Pagos anticipados',
        'overdue': 'Vencido',
        'of': 'de',
        'customers': 'clientes',
        'total_customers': 'Total Clientes',
        'avg_invoice': 'Promedio Factura',
        'overdue_amount': 'Monto Vencido',
        'avg_days_overdue': 'Días Prom. Vencido',
        'analytics': 'ANÁLISIS',
        'aging_analysis': 'Análisis de Antigüedad',
        'top_debtors': 'Principales Deudores',
        'portfolio_status': 'Estado del Portafolio',
        'amount_usd': 'Monto (USD)',
        'outstanding_usd': 'Monto Pendiente (USD)',
        'detailed_records': 'REGISTROS DETALLADOS',
        'customer': 'Cliente',
        'type': 'Tipo',
        'invoice': 'Factura #',
        'doc_date': 'Fecha Doc',
        'due_date': 'Fecha Venc',
        'open_amount': 'Monto Abierto',
        'credit_limit': 'Límite Crédito',
        'status': 'Estado',
        'days_overdue_col': 'Días Vencido',
        'export_excel': 'Exportar Excel',
        'export_csv': 'Exportar CSV',
        'download': 'Descargar',
        'export_error': 'Error de exportación',
        'overview': 'Resumen',
        'aging': 'Antigüedad',
        'customers_tab': 'Clientes',
        'exports': 'Exportar',
        'current': 'Al Día',
        'overdue_status': 'Vencido',
        'credit': 'Crédito'
    }
}

def t(key):
    """Get translation for current language"""
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS[lang].get(key, key)

# ═══════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def human_format(num):
    """Format large numbers"""
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
    """Format as USD"""
    try:
        num = float(value)
        if pd.isna(num):
            return "$0.00"
        return f"${num:,.2f}"
    except:
        return "$0.00"

def fmt_pct(value):
    """Format as percentage"""
    try:
        num = float(value)
        if pd.isna(num):
            return "0.0%"
        return f"{num:.1f}%"
    except:
        return "0.0%"

def get_color_scheme(theme='light'):
    """Return color scheme"""
    if theme == 'dark':
        return {
            'bg_primary': '#0F172A',
            'bg_secondary': '#1E293B',
            'bg_card': '#1E293B',
            'text_primary': '#F1F5F9',
            'text_secondary': '#94A3B8',
            'border': '#334155',
        }
    else:
        return {
            'bg_primary': '#FFFFFF',
            'bg_secondary': '#F8FAFC',
            'bg_card': '#FFFFFF',
            'text_primary': '#1E293B',
            'text_secondary': '#64748B',
            'border': '#E2E8F0',
        }

# ═══════════════════════════════════════════════════════════════════════
# PROFESSIONAL CSS
# ═══════════════════════════════════════════════════════════════════════

def inject_css(theme='light'):
    """Inject CSS"""
    colors = get_color_scheme(theme)
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    .main {{
        background-color: {colors['bg_secondary']};
        color: {colors['text_primary']};
    }}
    
    .block-container {{
        padding: 4rem 2rem 1.5rem 2rem !important;
        max-width: 100% !important;
    }}
    
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {AMZ_MIDNIGHT} 0%, {AMZ_ROYAL} 100%);
        padding-top: 1rem;
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] label {{
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }}
    
    [data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.05);
        border: 1px dashed rgba(255,255,255,0.3);
        border-radius: 6px;
        padding: 1rem;
    }}
    
    .logo-container {{
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }}
    
    .logo-container img {{
        max-width: 180px;
        height: auto;
    }}
    
    .main-header {{
        background: linear-gradient(135deg, {AMZ_MIDNIGHT} 0%, {AMZ_ROYAL} 100%);
        padding: 1.2rem 2rem;
        margin: -4rem 2rem 1.5rem -2rem;
        border-bottom: 3px solid {AMZ_SKY};
    }}
    
    .main-title {{
        color: white;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.3px;
    }}
    
    .main-subtitle {{
        color: {AMZ_SKY};
        font-size: 0.9rem;
        margin: 0.2rem 0 0;
    }}
    
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }}
    
    .kpi-card {{
        background: {colors['bg_card']};
        border: 1px solid {colors['border']};
        border-radius: 6px;
        padding: 1rem;
        transition: all 0.2s;
    }}
    
    .kpi-card:hover {{
        border-color: {AMZ_SKY};
        box-shadow: 0 2px 8px rgba(0,167,225,0.15);
    }}
    
    .kpi-label {{
        font-size: 0.7rem;
        font-weight: 600;
        color: {colors['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }}
    
    .kpi-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {colors['text_primary']};
        margin-bottom: 0.3rem;
    }}
    
    .kpi-delta {{
        font-size: 0.75rem;
        color: {colors['text_secondary']};
        font-weight: 500;
    }}
    
    .kpi-delta.positive {{ color: {S_GREEN}; }}
    .kpi-delta.negative {{ color: {S_RED}; }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: {colors['bg_card']};
        border-radius: 6px;
        padding: 0.3rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 40px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {AMZ_ROYAL}, {AMZ_SKY});
        color: white !important;
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {AMZ_ROYAL}, {AMZ_SKY});
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.4rem 1rem;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.2s;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 4px 12px rgba(0,71,171,0.25);
        transform: translateY(-1px);
    }}
    
    [data-testid="stMetric"] {{
        background: {colors['bg_card']};
        padding: 0.7rem;
        border-radius: 4px;
        border: 1px solid {colors['border']};
    }}
    
    [data-testid="stMetric"] label {{
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        color: {colors['text_secondary']} !important;
    }}
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }}
    
    .dataframe {{
        font-size: 0.8rem !important;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 3rem !important;
   }}     
        
    .element-container {{
        margin-bottom: 0.5rem !important;
    }}
    
    h3 {{
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: {colors['text_primary']} !important;
        margin: 1rem 0 0.7rem 0 !important;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid {colors['border']};
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def kpi_card(label, value, delta=None, delta_type='neutral'):
    """Render KPI card"""
    delta_class = f'kpi-delta {delta_type}'
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ''
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """

# ═══════════════════════════════════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════

def check_authentication():
    """Authentication"""
    try:
        correct_password = st.secrets.get("AR_PASSWORD", "AMRIZE2024")
    except:
        correct_password = "AMRIZE2024"
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    st.markdown(f"""
    <div style='max-width: 400px; margin: 5rem auto; padding: 2.5rem;
                background: linear-gradient(135deg, {AMZ_MIDNIGHT}, {AMZ_ROYAL});
                border-radius: 8px; box-shadow: 0 10px 40px rgba(0,0,0,0.2);'>
        <h1 style='color: white; margin: 0 0 0.5rem; font-size: 1.8rem; font-weight: 700;'>
            AMRIZE
        </h1>
        <p style='color: {AMZ_SKY}; margin: 0 0 2rem; font-size: 0.95rem;'>
            {t('subtitle')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        st.markdown(f"#### {t('login_title')}")
        password = st.text_input(t('password'), type="password", placeholder="")
        submitted = st.form_submit_button(t('sign_in'), use_container_width=True, type="primary")
        
        if submitted:
            if password == correct_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(t('invalid_credentials'))
    
    return False

# ═══════════════════════════════════════════════════════════════════════
# DATA PROCESSING
# ═══════════════════════════════════════════════════════════════════════

def load_and_process_data(uploaded_file):
    """Load and process data"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        initial_rows = len(df)
        df = df[df['Document date'] != 'Result'].copy()
        removed_rows = initial_rows - len(df)
        
        df['Document date'] = pd.to_datetime(df['Document date'], errors='coerce')
        df['Net due date'] = pd.to_datetime(df['Net due date'], errors='coerce')
        
        numeric_columns = [
            'Open Amount', 'Credit Limit', 'Current Amount',
            '1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays',
            '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '').replace('nan', '0')
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        if 'SP #' in df.columns:
            df['SP #'] = df['SP #'].astype(str).replace('nan', '').replace('None', '')
        
        df['Debt_Type'] = df['Open Amount'].apply(
            lambda x: 'Debt' if x > 0 else ('Credit' if x < 0 else 'Zero')
        )
        
        today = pd.Timestamp.now()
        df['Days_Overdue'] = (today - df['Net due date']).dt.days
        df['Days_Overdue'] = df['Days_Overdue'].fillna(0).astype(int)
        
        df['Status'] = df.apply(lambda row: 
            t('overdue_status') if row['Days_Overdue'] > 0 and row['Open Amount'] > 0
            else t('current') if row['Open Amount'] > 0
            else t('credit'),
            axis=1
        )
        
        df['Over_Credit_Limit'] = (df['Open Amount'] > df['Credit Limit']) & (df['Credit Limit'] > 0)
        
        return df, None, removed_rows
        
    except Exception as e:
        return None, f"Error: {str(e)}", 0

# ═══════════════════════════════════════════════════════════════════════
# KPI CALCULATIONS
# ═══════════════════════════════════════════════════════════════════════

def calculate_kpis(df):
    """Calculate KPIs"""
    kpis = {}
    
    kpis['gross_debt'] = df[df['Open Amount'] > 0]['Open Amount'].sum()
    kpis['credits'] = abs(df[df['Open Amount'] < 0]['Open Amount'].sum())
    
    current_amount = df[df['Open Amount'] > 0]['Current Amount'].sum()
    kpis['pct_current'] = (current_amount / kpis['gross_debt'] * 100) if kpis['gross_debt'] > 0 else 0
    kpis['pct_overdue'] = 100 - kpis['pct_current']
    kpis['current_amount'] = current_amount
    kpis['overdue_amount'] = kpis['gross_debt'] - current_amount
    
    client_totals = df.groupby('Counterparty Name').agg({
        'Open Amount': 'sum',
        'Credit Limit': 'first'
    }).reset_index()
    
    kpis['credit_risk_count'] = len(
        client_totals[(client_totals['Open Amount'] > client_totals['Credit Limit']) & 
                     (client_totals['Credit Limit'] > 0)]
    )
    
    kpis['total_invoices'] = len(df)
    kpis['unique_customers'] = df['Counterparty Name'].nunique()
    kpis['avg_invoice'] = kpis['gross_debt'] / kpis['total_invoices'] if kpis['total_invoices'] > 0 else 0
    
    kpis['avg_days_overdue'] = df[df['Days_Overdue'] > 0]['Days_Overdue'].mean()
    if pd.isna(kpis['avg_days_overdue']):
        kpis['avg_days_overdue'] = 0
    
    return kpis

# ═══════════════════════════════════════════════════════════════════════
# VISUALIZATIONS
# ═══════════════════════════════════════════════════════════════════════

def create_aging_chart(df, theme='light'):
    """Aging chart"""
    aging_cols = [
        'Current Amount', '1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays',
        '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays'
    ]
    
    aging_data = []
    for col in aging_cols:
        if col in df.columns:
            total = df[col].sum()
            aging_data.append({'Bucket': col.replace('\n', ' '), 'Amount': abs(total)})
    
    df_aging = pd.DataFrame(aging_data)
    colors = [S_GREEN, AMZ_SKY, AMZ_ROYAL, S_AMBER, '#F59E0B', '#FFA500', '#FF6B35', S_RED]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_aging['Bucket'],
        y=df_aging['Amount'],
        marker=dict(color=colors[:len(df_aging)], line=dict(color='rgba(255,255,255,0.5)', width=1)),
        text=[human_format(v) for v in df_aging['Amount']],
        textposition='outside',
        textfont=dict(size=10),
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
    ))
    
    bg_color = '#1E293B' if theme == 'dark' else 'white'
    text_color = '#F1F5F9' if theme == 'dark' else '#1E293B'
    grid_color = '#334155' if theme == 'dark' else '#E2E8F0'
    
    fig.update_layout(
        title={'text': t('aging_analysis'), 'font': {'size': 13, 'weight': 'bold', 'color': text_color}},
        xaxis_title=None,
        yaxis_title=t('amount_usd'),
        height=280,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, family='Inter', size=9),
        margin=dict(l=50, r=20, t=40, b=30),
        xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=8)),
        yaxis=dict(showgrid=True, gridcolor=grid_color, gridwidth=0.5),
        hovermode='x unified'
    )
    
    return fig

def create_top_debtors_chart(df, top_n=10, theme='light'):
    """Top debtors chart"""
    debtors = df[df['Open Amount'] > 0].groupby('Counterparty Name').agg({'Open Amount': 'sum'}).reset_index()
    debtors = debtors.sort_values('Open Amount', ascending=True).tail(top_n)
    
    colors = [S_RED if i >= len(debtors) - 3 else S_AMBER if i >= len(debtors) - 5 else AMZ_SKY 
              for i in range(len(debtors))]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=debtors['Counterparty Name'],
        x=debtors['Open Amount'],
        orientation='h',
        marker=dict(color=colors, line=dict(color='rgba(255,255,255,0.5)', width=1)),
        text=[human_format(v) for v in debtors['Open Amount']],
        textposition='outside',
        textfont=dict(size=10),
        hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>'
    ))
    
    bg_color = '#1E293B' if theme == 'dark' else 'white'
    text_color = '#F1F5F9' if theme == 'dark' else '#1E293B'
    grid_color = '#334155' if theme == 'dark' else '#E2E8F0'
    
    fig.update_layout(
        title={'text': f"{t('top_debtors')} {top_n}", 'font': {'size': 13, 'weight': 'bold', 'color': text_color}},
        xaxis_title=t('outstanding_usd'),
        yaxis_title=None,
        height=280,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, family='Inter', size=9),
        margin=dict(l=160, r=40, t=40, b=30),
        xaxis=dict(showgrid=True, gridcolor=grid_color, gridwidth=0.5),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        hovermode='y unified'
    )
    
    return fig

def create_status_donut(df, theme='light'):
    """Status donut"""
    df_debt = df[df['Open Amount'] > 0].copy()
    status_counts = df_debt.groupby('Status').agg({'Open Amount': 'sum'}).reset_index()
    
    color_map = {t('current'): S_GREEN, t('overdue_status'): S_RED, t('credit'): AMZ_SKY}
    colors = [color_map.get(status, S_GRAY) for status in status_counts['Status']]
    
    fig = go.Figure(data=[go.Pie(
        labels=status_counts['Status'],
        values=status_counts['Open Amount'],
        hole=0.5,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='label+percent',
        textfont=dict(size=10),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<extra></extra>'
    )])
    
    bg_color = '#1E293B' if theme == 'dark' else 'white'
    text_color = '#F1F5F9' if theme == 'dark' else '#1E293B'
    
    fig.update_layout(
        title={'text': t('portfolio_status'), 'font': {'size': 13, 'weight': 'bold', 'color': text_color}},
        height=280,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, family='Inter', size=9),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
        margin=dict(l=10, r=10, t=40, b=50)
    )
    
    return fig

# ═══════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Main application"""
    
    # Initialize session state
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # Authentication
    if not check_authentication():
        return
    
    # Inject CSS
    inject_css(st.session_state.theme)
    
    # Header
    col_h1, col_h2, col_h3, col_h4 = st.columns([4, 1, 1, 1])
    
    with col_h1:
        st.markdown(f"""
        <div class="main-header">
            <div class="main-title">AMRIZE {t('title')}</div>
            <div class="main-subtitle">{t('subtitle')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h2:
        if st.button("EN" if st.session_state.language == 'es' else "ES", use_container_width=True):
            st.session_state.language = 'en' if st.session_state.language == 'es' else 'es'
            st.rerun()
    
    with col_h3:
        theme_label = "Dark" if st.session_state.theme == 'light' else "Light"
        if st.button(f"◐ {theme_label}", use_container_width=True):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()
    
    with col_h4:
        if st.button(t('sign_out'), use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Sidebar
    with st.sidebar:
        # Logo
        try:
            from PIL import Image
            logo = Image.open('logo.jpg')
            st.image(logo, use_container_width=True)
        except:
            st.markdown(f"""
            <div class="logo-container">
                <h2 style='color: white; margin: 0;'>AMRIZE</h2>
                <p style='color: {AMZ_SKY}; font-size: 0.8rem; margin: 0.3rem 0 0;'>BUILD YOUR AMBITION</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"### {t('data_source')}")
        
        uploaded_file = st.file_uploader(
            t('upload'),
            type=['csv', 'xlsx', 'xls'],
            help=t('upload_help')
        )
        
        if uploaded_file is not None:
            with st.spinner(t('processing')):
                df, error, removed = load_and_process_data(uploaded_file)
            
            if error:
                st.error(error)
                return
            
            if df is None or len(df) == 0:
                st.warning(t('no_data'))
                return
            
            st.session_state.df = df
            st.success(f"{len(df):,} {t('records_loaded')}")
            
            if removed > 0:
                st.info(f"{removed} {t('subtotals_removed')}")
            
            st.markdown("---")
            st.markdown(f"### {t('filters')}")
            
            all_types = sorted(df['Counterparty Type'].dropna().unique().tolist())
            selected_types = st.multiselect(
                t('counterparty_type'),
                options=all_types,
                default=all_types,
                key='filter_types'
            )
            
            # Filtro por Company Name (Columna A: Counterparty Name)
            if selected_types:
                available_clients = sorted(
                    df[df['Counterparty Type'].isin(selected_types)]['Counterparty Name'].dropna().unique().tolist()
                )
            else:
                available_clients = sorted(df['Counterparty Name'].dropna().unique().tolist())
            
            selected_clients = st.multiselect(
                t('counterparty'),
                options=available_clients,
                default=available_clients,
                key='filter_clients'
            )
            
            df_filtered = df.copy()
            
            if selected_types:
                df_filtered = df_filtered[df_filtered['Counterparty Type'].isin(selected_types)]
            
            if selected_clients:
                df_filtered = df_filtered[df_filtered['Counterparty Name'].isin(selected_clients)]
            
            st.session_state.df_filtered = df_filtered
            
            st.markdown("---")
            st.metric(t('filtered_records'), f"{len(df_filtered):,}")
        
        else:
            st.info(t('upload_to_begin'))
    
    # Main content
    if 'df_filtered' not in st.session_state:
        st.info(f"**{t('upload_message')}**")
        return
    
    df_filtered = st.session_state.df_filtered
    kpis = calculate_kpis(df_filtered)
    
    # KPIs
    st.markdown(f"### {t('kpi_header')}")
    
    kpi_html = f"""
    <div class="kpi-grid">
        {kpi_card(t('gross_receivables'), human_format(kpis['gross_debt']), f"{kpis['total_invoices']:,} {t('invoices')}", 'neutral')}
        {kpi_card(t('customer_credits'), human_format(kpis['credits']), t('advance_payments'), 'positive')}
        {kpi_card(t('current_pct'), fmt_pct(kpis['pct_current']), f"{t('overdue')}: {fmt_pct(kpis['pct_overdue'])}", 'negative' if kpis['pct_overdue'] > 50 else 'neutral')}
        {kpi_card(t('credit_risk'), str(kpis['credit_risk_count']), f"{t('of')} {kpis['unique_customers']} {t('customers')}", 'negative' if kpis['credit_risk_count'] > 0 else 'positive')}
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t('total_customers'), f"{kpis['unique_customers']:,}")
    with col2:
        st.metric(t('avg_invoice'), human_format(kpis['avg_invoice']))
    with col3:
        st.metric(t('overdue_amount'), human_format(kpis['overdue_amount']))
    with col4:
        st.metric(t('avg_days_overdue'), f"{int(kpis['avg_days_overdue'])}")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([t('overview'), t('aging'), t('customers_tab'), t('exports')])
    
    with tab1:
        st.markdown(f"### {t('analytics')}")
        
        col_c1, col_c2, col_c3 = st.columns([2, 2, 1.5])
        
        with col_c1:
            fig_aging = create_aging_chart(df_filtered, st.session_state.theme)
            st.plotly_chart(fig_aging, use_container_width=True)
        
        with col_c2:
            fig_top = create_top_debtors_chart(df_filtered, top_n=10, theme=st.session_state.theme)
            st.plotly_chart(fig_top, use_container_width=True)
        
        with col_c3:
            fig_status = create_status_donut(df_filtered, st.session_state.theme)
            st.plotly_chart(fig_status, use_container_width=True)
    
    with tab2:
        st.markdown(f"### {t('aging_analysis')}")
        
        col_a1, col_a2 = st.columns([3, 2])
        
        with col_a1:
            fig_aging_full = create_aging_chart(df_filtered, st.session_state.theme)
            fig_aging_full.update_layout(height=400)
            st.plotly_chart(fig_aging_full, use_container_width=True)
        
        with col_a2:
            aging_cols = ['Current Amount', '1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays',
                         '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays']
            
            aging_summary = []
            for col in aging_cols:
                if col in df_filtered.columns:
                    total = df_filtered[col].sum()
                    pct = (total / kpis['gross_debt'] * 100) if kpis['gross_debt'] > 0 else 0
                    aging_summary.append({
                        'Period': col.replace('\n', ' '),
                        'Amount': fmt_currency(total),
                        '%': fmt_pct(pct)
                    })
            
            st.dataframe(
                pd.DataFrame(aging_summary),
                use_container_width=True,
                hide_index=True,
                height=400
            )
    
    with tab3:
        st.markdown(f"### {t('detailed_records')}")
        
        display_columns = [
            'Counterparty Name', 'Counterparty Type', 'INV # - Salesforce', 'SP #',
            'Document date', 'Net due date', 'Open Amount', 'Credit Limit', 'Status', 'Days_Overdue'
        ]
        
        df_display = df_filtered[display_columns].copy()
        df_display.columns = [
            t('customer'), t('type'), t('invoice'), 'SP #', t('doc_date'), t('due_date'),
            t('open_amount'), t('credit_limit'), t('status'), t('days_overdue_col')
        ]
        
        df_display = df_display.sort_values(t('open_amount'), ascending=False)
        
        column_config = {
            t('open_amount'): st.column_config.NumberColumn(t('open_amount'), format='$%.2f'),
            t('credit_limit'): st.column_config.NumberColumn(t('credit_limit'), format='$%.2f'),
            t('doc_date'): st.column_config.DateColumn(t('doc_date'), format='YYYY-MM-DD'),
            t('due_date'): st.column_config.DateColumn(t('due_date'), format='YYYY-MM-DD'),
            t('days_overdue_col'): st.column_config.NumberColumn(t('days_overdue_col'), format='%d')
        }
        
        st.dataframe(df_display, use_container_width=True, height=450, column_config=column_config, hide_index=True)
    
    with tab4:
        st.markdown(f"### {t('exports')}")
        
        col_e1, col_e2, col_e3 = st.columns([1, 1, 2])
        
        with col_e1:
            if st.button(t('export_excel'), use_container_width=True, type="primary"):
                try:
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_display.to_excel(writer, sheet_name='Data', index=False)
                        
                        kpi_summary = pd.DataFrame({
                            'KPI': [t('gross_receivables'), t('customer_credits'), t('current_pct'), t('overdue'),
                                   t('credit_risk'), t('total_customers'), t('invoices'), t('avg_invoice'), t('avg_days_overdue')],
                            'Value': [fmt_currency(kpis['gross_debt']), fmt_currency(kpis['credits']),
                                     fmt_pct(kpis['pct_current']), fmt_pct(kpis['pct_overdue']),
                                     kpis['credit_risk_count'], kpis['unique_customers'], kpis['total_invoices'],
                                     fmt_currency(kpis['avg_invoice']), f"{int(kpis['avg_days_overdue'])} days"]
                        })
                        kpi_summary.to_excel(writer, sheet_name='KPIs', index=False)
                    
                    output.seek(0)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    
                    st.download_button(
                        label=t('download'),
                        data=output,
                        file_name=f"AR_Report_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"{t('export_error')}: {e}")
        
        with col_e2:
            if st.button(t('export_csv'), use_container_width=True):
                csv = df_display.to_csv(index=False)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                st.download_button(t('download'), data=csv, file_name=f"AR_Report_{timestamp}.csv",
                                 mime="text/csv", use_container_width=True)


if __name__ == "__main__":
    main()
