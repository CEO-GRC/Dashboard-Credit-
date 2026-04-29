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
    page_title="Amrize AR Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════
# CSS PARA HACER LA BARRA LATERAL SIEMPRE VISIBLE
# ═══════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Asegurar que el botón de la barra lateral sea siempre visible */
    [data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 0.5rem !important;
        left: 0.5rem !important;
        z-index: 999999 !important;
        background-color: #011E6A !important;
        color: white !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
    }
    
    /* Mejorar visibilidad del ícono */
    [data-testid="collapsedControl"] svg {
        color: white !important;
        fill: white !important;
    }
    
    /* Hover effect para el botón */
    [data-testid="collapsedControl"]:hover {
        background-color: #00A7E1 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

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
        'title': 'AR DASHBOARD',
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
        if pd.isna(value):
            return "$0.00"
        return f"${float(value):,.2f}"
    except:
        return "$0.00"

def fmt_pct(value):
    """Format percentage"""
    try:
        return f"{float(value):.1f}%"
    except:
        return "0.0%"

def kpi_card(title, value, subtitle, color_type='neutral'):
    """Generate KPI card HTML"""
    colors = {
        'positive': S_GREEN,
        'negative': S_RED,
        'neutral': AMZ_ROYAL,
        'warning': S_AMBER
    }
    color = colors.get(color_type, AMZ_ROYAL)
    
    return f"""
    <div style="
        background: linear-gradient(135deg, {color}15 0%, {color}05 100%);
        border-left: 4px solid {color};
        padding: 1.25rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="color: {S_GRAY}; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">
            {title}
        </div>
        <div style="color: {color}; font-size: 1.875rem; font-weight: 700; margin-bottom: 0.25rem;">
            {value}
        </div>
        <div style="color: {S_GRAY}; font-size: 0.875rem;">
            {subtitle}
        </div>
    </div>
    """

# ═══════════════════════════════════════════════════════════════════════
# DATA PROCESSING
# ═══════════════════════════════════════════════════════════════════════

def load_ar_data(uploaded_file):
    """Load and clean AR data from SAP export"""
    try:
        with st.spinner(t('processing')):
            df = pd.read_excel(uploaded_file, sheet_name=0)
            
            original_count = len(df)
            df = df[df['Counterparty Name'].notna()]
            df = df[~df['Counterparty Name'].astype(str).str.contains('Total', case=False, na=False)]
            removed = original_count - len(df)
            
            date_cols = ['Document date', 'Net due date']
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            numeric_cols = ['Open Amount', 'Credit Limit', 'Current Amount',
                          '1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays',
                          '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays']
            
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            today = pd.Timestamp.now().normalize()
            df['Days_Overdue'] = (today - df['Net due date']).dt.days
            df['Days_Overdue'] = df['Days_Overdue'].clip(lower=0)
            
            def get_status(row):
                if pd.notna(row.get('Open Amount')) and row.get('Open Amount', 0) < 0:
                    return t('credit')
                elif row.get('Days_Overdue', 0) > 0:
                    return t('overdue_status')
                else:
                    return t('current')
            
            df['Status'] = df.apply(get_status, axis=1)
            
            return df, removed
            
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None, 0

def calculate_kpis(df):
    """Calculate key performance indicators"""
    kpis = {}
    
    kpis['gross_debt'] = df[df['Open Amount'] > 0]['Open Amount'].sum()
    kpis['credits'] = abs(df[df['Open Amount'] < 0]['Open Amount'].sum())
    kpis['total_invoices'] = len(df[df['Open Amount'] > 0])
    kpis['unique_customers'] = df['Counterparty Name'].nunique()
    
    current = df[df['Status'] == t('current')]['Open Amount'].sum()
    kpis['pct_current'] = (current / kpis['gross_debt'] * 100) if kpis['gross_debt'] > 0 else 0
    
    overdue = df[df['Status'] == t('overdue_status')]['Open Amount'].sum()
    kpis['pct_overdue'] = (overdue / kpis['gross_debt'] * 100) if kpis['gross_debt'] > 0 else 0
    
    kpis['avg_invoice'] = kpis['gross_debt'] / kpis['total_invoices'] if kpis['total_invoices'] > 0 else 0
    
    overdue_df = df[df['Days_Overdue'] > 0]
    kpis['avg_days_overdue'] = overdue_df['Days_Overdue'].mean() if len(overdue_df) > 0 else 0
    kpis['overdue_amount'] = overdue
    
    credit_risk = df.groupby('Counterparty Name').agg({
        'Open Amount': 'sum',
        'Credit Limit': 'first'
    }).reset_index()
    credit_risk = credit_risk[credit_risk['Open Amount'] > credit_risk['Credit Limit']]
    kpis['credit_risk_count'] = len(credit_risk)
    
    return kpis

# ═══════════════════════════════════════════════════════════════════════
# VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════

def create_aging_chart(df, theme='dark'):
    """Create aging buckets bar chart"""
    aging_cols = ['Current Amount', '1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays',
                 '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays']
    
    amounts = [df[col].sum() for col in aging_cols if col in df.columns]
    labels = [col.replace('\n', ' ') for col in aging_cols if col in df.columns]
    
    colors = [S_GREEN, AMZ_SKY, AMZ_ROYAL, S_AMBER, S_AMBER, S_RED, S_RED, '#8B0000']
    
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=amounts,
            marker=dict(
                color=colors[:len(amounts)],
                line=dict(color='rgba(0,0,0,0.2)', width=1)
            ),
            text=[human_format(x) for x in amounts],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Amount: %{text}<extra></extra>'
        )
    ])
    
    bg_color = '#0E1117' if theme == 'dark' else 'white'
    text_color = 'white' if theme == 'dark' else 'black'
    
    fig.update_layout(
        title=dict(text=t('aging_analysis'), font=dict(size=16, color=text_color)),
        xaxis=dict(title='', tickangle=-45, color=text_color),
        yaxis=dict(title=t('amount_usd'), color=text_color),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor=bg_color,
        font=dict(color=text_color),
        height=350,
        margin=dict(t=50, b=100, l=50, r=20),
        showlegend=False
    )
    
    return fig

def create_top_debtors_chart(df, top_n=10, theme='dark'):
    """Create top debtors horizontal bar chart"""
    top_debtors = df.groupby('Counterparty Name')['Open Amount'].sum().nlargest(top_n).sort_values()
    
    fig = go.Figure(data=[
        go.Bar(
            y=top_debtors.index,
            x=top_debtors.values,
            orientation='h',
            marker=dict(
                color=AMZ_ROYAL,
                line=dict(color='rgba(0,0,0,0.2)', width=1)
            ),
            text=[human_format(x) for x in top_debtors.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Outstanding: %{text}<extra></extra>'
        )
    ])
    
    bg_color = '#0E1117' if theme == 'dark' else 'white'
    text_color = 'white' if theme == 'dark' else 'black'
    
    fig.update_layout(
        title=dict(text=f"{t('top_debtors')} (Top {top_n})", font=dict(size=16, color=text_color)),
        xaxis=dict(title=t('outstanding_usd'), color=text_color),
        yaxis=dict(title='', color=text_color),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor=bg_color,
        font=dict(color=text_color),
        height=350,
        margin=dict(t=50, b=50, l=150, r=50),
        showlegend=False
    )
    
    return fig

def create_status_donut(df, theme='dark'):
    """Create portfolio status donut chart"""
    status_data = df.groupby('Status')['Open Amount'].sum()
    
    colors_map = {
        t('current'): S_GREEN,
        t('overdue_status'): S_RED,
        t('credit'): AMZ_SKY
    }
    
    colors = [colors_map.get(status, S_GRAY) for status in status_data.index]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=status_data.index,
            values=status_data.values,
            hole=0.5,
            marker=dict(colors=colors, line=dict(color='rgba(0,0,0,0.2)', width=2)),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Amount: %{value:$,.2f}<br>Percentage: %{percent}<extra></extra>'
        )
    ])
    
    bg_color = '#0E1117' if theme == 'dark' else 'white'
    text_color = 'white' if theme == 'dark' else 'black'
    
    fig.update_layout(
        title=dict(text=t('portfolio_status'), font=dict(size=16, color=text_color)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor=bg_color,
        font=dict(color=text_color),
        height=350,
        margin=dict(t=50, b=50, l=20, r=20),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5)
    )
    
    return fig

# ═══════════════════════════════════════════════════════════════════════
# THEME MANAGER
# ═══════════════════════════════════════════════════════════════════════

def apply_theme():
    """Apply custom CSS based on theme"""
    theme = st.session_state.get('theme', 'dark')
    
    if theme == 'dark':
        bg = '#0E1117'
        text = 'white'
        card_bg = '#262730'
    else:
        bg = '#FFFFFF'
        text = '#262730'
        card_bg = '#F0F2F6'
    
    st.markdown(f"""
    <style>
        .main {{
            background-color: {bg};
            color: {text};
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: {card_bg};
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            color: {text};
            font-weight: 600;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {AMZ_ROYAL};
            color: white;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .metric-container {{
            background-color: {card_bg};
            border-radius: 8px;
            padding: 1rem;
        }}
        
        div[data-testid="stMetricValue"] {{
            font-size: 1.5rem;
            color: {AMZ_ROYAL};
            font-weight: 700;
        }}
        
        h1, h2, h3 {{
            color: {text} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════

def check_password():
    """Simple password protection"""
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    st.markdown(f"### 🔐 {t('login_title')}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        password = st.text_input(t('password'), type="password", key="password_input")
        
        if st.button(t('sign_in'), use_container_width=True, type="primary"):
            if password == "amrize2025":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(t('invalid_credentials'))
    
    return False

# ═══════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Main application"""
    
    if not check_password():
        return
    
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    apply_theme()
    
    st.markdown(f"""
    <h1 style='text-align: center; color: {AMZ_MIDNIGHT}; margin-bottom: 0;'>
        📊 {t('title')}
    </h1>
    <p style='text-align: center; color: {AMZ_SKY}; font-size: 1.2rem; margin-top: 0;'>
        {t('subtitle')}
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### ⚙️ Settings")
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            if st.button("🌙 Dark" if st.session_state.theme == 'dark' else "☀️ Light",
                        use_container_width=True):
                st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
                st.rerun()
        
        with col_s2:
            if st.button("🇺🇸 EN" if st.session_state.language == 'en' else "🇪🇸 ES",
                        use_container_width=True):
                st.session_state.language = 'es' if st.session_state.language == 'en' else 'en'
                st.rerun()
        
        if st.button(f"🚪 {t('sign_out')}", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.rerun()
        
        st.markdown("---")
        st.markdown(f"### 📁 {t('data_source')}")
        
        uploaded_file = st.file_uploader(
            t('upload'),
            type=['xlsx', 'xls'],
            help=t('upload_help')
        )
        
        if uploaded_file is not None:
            df, removed = load_ar_data(uploaded_file)
            
            if df is None or len(df) == 0:
                st.warning(t('no_data'))
                return
            
            st.session_state.df = df
            st.success(f"{len(df):,} {t('records_loaded')}")
            
            if removed > 0:
                st.info(f"{removed} {t('subtotals_removed')}")
            
            # ═══════════════════════════════════════════════════════════════
            # FILTROS MEJORADOS - NUEVA SECCIÓN
            # ═══════════════════════════════════════════════════════════════
            
            st.markdown("---")
            st.markdown(f"### 🔍 {t('filters')}")
            
            # Filtro por Counterparty Type (Group)
            st.markdown("**Counterparty Type (Group)**")
            all_types = sorted(df['Counterparty Type'].dropna().unique().tolist())
            selected_types = st.multiselect(
                t('counterparty_type'),
                options=all_types,
                default=all_types,
                key='filter_types',
                label_visibility='collapsed'
            )
            
            # Filtro por Counterparty Name (Company Name)
            st.markdown("**Counterparty Name (Company)**")
            
            # Filtrar opciones disponibles basadas en el tipo seleccionado
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
                key='filter_clients',
                label_visibility='collapsed'
            )
            
            # Aplicar filtros
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
