"""
AMRIZE AR DASHBOARD v2.1
Professional Accounts Receivable Analytics Platform
Bilingual | Dark/Light Mode | Tabbed Interface | Advanced Filters
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
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
        'document_type': 'Document Type',
        'payment_terms': 'Payment Terms',
        'amount_range': 'Amount Range',
        'date_range': 'Document Date Range',
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
        'credit': 'Credit',
        'min_amount': 'Min Amount',
        'max_amount': 'Max Amount',
        'from_date': 'From Date',
        'to_date': 'To Date',
        'toggle_filters': '☰ Filters',
        'hide_filters': '✕ Hide'
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
        'document_type': 'Tipo de Documento',
        'payment_terms': 'Términos de Pago',
        'amount_range': 'Rango de Monto',
        'date_range': 'Rango de Fecha Documento',
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
        'credit': 'Crédito',
        'min_amount': 'Monto Mínimo',
        'max_amount': 'Monto Máximo',
        'from_date': 'Desde Fecha',
        'to_date': 'Hasta Fecha',
        'toggle_filters': '☰ Filtros',
        'hide_filters': '✕ Ocultar'
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
        return f"${float(value):,.2f}"
    except:
        return "$0.00"

def fmt_pct(value):
    """Format as percentage"""
    try:
        return f"{float(value):.1f}%"
    except:
        return "0.0%"

# ═══════════════════════════════════════════════════════════════════════
# DATA PROCESSING
# ═══════════════════════════════════════════════════════════════════════

def clean_sap_data(df):
    """Remove SAP subtotals and clean data"""
    removed = 0
    
    # Remove rows where Counterparty Name is NaN or looks like a subtotal
    mask = df['Counterparty Name'].notna()
    df_clean = df[mask].copy()
    removed = len(df) - len(df_clean)
    
    # Convert date columns
    date_cols = ['Document date', 'Net due date']
    for col in date_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
    
    # Calculate Days Overdue
    today = pd.Timestamp.now()
    df_clean['Days_Overdue'] = (today - df_clean['Net due date']).dt.days
    df_clean['Days_Overdue'] = df_clean['Days_Overdue'].fillna(0).astype(int)
    
    # Determine Status
    def get_status(row):
        if pd.isna(row['Open Amount']):
            return 'Unknown'
        if row['Open Amount'] < 0:
            return t('credit')
        if row['Days_Overdue'] <= 0:
            return t('current')
        return t('overdue_status')
    
    df_clean['Status'] = df_clean.apply(get_status, axis=1)
    
    return df_clean, removed

def load_data(file):
    """Load and process AR data"""
    try:
        df = pd.read_excel(file)
        df_clean, removed = clean_sap_data(df)
        return df_clean, removed
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None, 0

def calculate_kpis(df):
    """Calculate KPIs from filtered data"""
    kpis = {}
    
    # Gross Debt & Credits
    kpis['gross_debt'] = df[df['Open Amount'] > 0]['Open Amount'].sum()
    kpis['credits'] = abs(df[df['Open Amount'] < 0]['Open Amount'].sum())
    
    # Current vs Overdue
    current = df[df['Status'] == t('current')]['Open Amount'].sum()
    overdue = df[df['Status'] == t('overdue_status')]['Open Amount'].sum()
    total_positive = kpis['gross_debt']
    
    kpis['pct_current'] = (current / total_positive * 100) if total_positive > 0 else 0
    kpis['pct_overdue'] = (overdue / total_positive * 100) if total_positive > 0 else 0
    
    # Credit Risk (over limit)
    credit_risk = df[(df['Credit Limit'].notna()) & (df['Open Amount'] > df['Credit Limit'])]
    kpis['credit_risk_count'] = credit_risk['Counterparty Name'].nunique()
    
    # Other metrics
    kpis['unique_customers'] = df['Counterparty Name'].nunique()
    kpis['total_invoices'] = len(df[df['Open Amount'] > 0])
    kpis['avg_invoice'] = df[df['Open Amount'] > 0]['Open Amount'].mean() if kpis['total_invoices'] > 0 else 0
    kpis['overdue_amount'] = overdue
    
    overdue_df = df[df['Status'] == t('overdue_status')]
    kpis['avg_days_overdue'] = overdue_df['Days_Overdue'].mean() if len(overdue_df) > 0 else 0
    
    return kpis

# ═══════════════════════════════════════════════════════════════════════
# VISUALIZATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def create_aging_chart(df, theme='dark'):
    """Create aging analysis bar chart"""
    aging_cols = ['Current Amount', '1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays',
                 '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays']
    
    values = []
    labels = []
    for col in aging_cols:
        if col in df.columns:
            val = df[col].sum()
            values.append(val)
            labels.append(col.replace('\n', ' '))
    
    bg_color = '#1E1E1E' if theme == 'dark' else '#FFFFFF'
    text_color = '#FFFFFF' if theme == 'dark' else '#000000'
    grid_color = '#333333' if theme == 'dark' else '#E5E5E5'
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels,
        y=values,
        marker_color=AMZ_SKY,
        text=[human_format(v) for v in values],
        textposition='outside',
        textfont=dict(color=text_color, size=11),
        hovertemplate='%{x}<br>%{y:$,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=t('aging_analysis'), font=dict(size=16, color=text_color)),
        xaxis=dict(title='', tickfont=dict(size=10, color=text_color), gridcolor=grid_color),
        yaxis=dict(title=t('amount_usd'), tickfont=dict(color=text_color), gridcolor=grid_color),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color),
        height=350,
        margin=dict(t=40, b=60, l=60, r=20)
    )
    
    return fig

def create_top_debtors_chart(df, top_n=10, theme='dark'):
    """Create top debtors horizontal bar chart"""
    top_debtors = df[df['Open Amount'] > 0].groupby('Counterparty Name')['Open Amount'].sum().sort_values(ascending=True).tail(top_n)
    
    bg_color = '#1E1E1E' if theme == 'dark' else '#FFFFFF'
    text_color = '#FFFFFF' if theme == 'dark' else '#000000'
    grid_color = '#333333' if theme == 'dark' else '#E5E5E5'
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_debtors.index,
        x=top_debtors.values,
        orientation='h',
        marker_color=AMZ_ROYAL,
        text=[human_format(v) for v in top_debtors.values],
        textposition='outside',
        textfont=dict(color=text_color, size=10),
        hovertemplate='%{y}<br>%{x:$,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=f"{t('top_debtors')} (Top {top_n})", font=dict(size=16, color=text_color)),
        xaxis=dict(title=t('outstanding_usd'), tickfont=dict(color=text_color), gridcolor=grid_color),
        yaxis=dict(title='', tickfont=dict(size=9, color=text_color)),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color),
        height=350,
        margin=dict(t=40, b=40, l=120, r=80)
    )
    
    return fig

def create_status_donut(df, theme='dark'):
    """Create portfolio status donut chart"""
    status_summary = df.groupby('Status')['Open Amount'].sum()
    
    colors = {
        t('current'): S_GREEN,
        t('overdue_status'): S_RED,
        t('credit'): S_AMBER
    }
    
    bg_color = '#1E1E1E' if theme == 'dark' else '#FFFFFF'
    text_color = '#FFFFFF' if theme == 'dark' else '#000000'
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=status_summary.index,
        values=status_summary.values.abs(),
        hole=0.5,
        marker=dict(colors=[colors.get(s, S_GRAY) for s in status_summary.index]),
        textinfo='label+percent',
        textfont=dict(size=11, color=text_color),
        hovertemplate='%{label}<br>%{value:$,.2f}<br>%{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=t('portfolio_status'), font=dict(size=16, color=text_color)),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color),
        height=350,
        margin=dict(t=40, b=20, l=20, r=20),
        showlegend=True,
        legend=dict(font=dict(color=text_color))
    )
    
    return fig

# ═══════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════

def kpi_card(title, value, subtitle, status='neutral'):
    """Generate KPI card HTML"""
    status_colors = {
        'positive': S_GREEN,
        'negative': S_RED,
        'neutral': AMZ_SKY
    }
    color = status_colors.get(status, AMZ_SKY)
    
    return f"""
    <div style="background: linear-gradient(135deg, {color}15 0%, {color}05 100%);
                border-left: 4px solid {color};
                padding: 1.2rem;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div style="font-size: 0.85rem; font-weight: 600; color: {color}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">
            {title}
        </div>
        <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem;">
            {value}
        </div>
        <div style="font-size: 0.75rem; opacity: 0.7;">
            {subtitle}
        </div>
    </div>
    """

def inject_custom_css():
    """Inject custom CSS for enhanced styling"""
    st.markdown("""
    <style>
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Floating toggle button */
    .filter-toggle {
        position: fixed;
        left: 10px;
        top: 80px;
        z-index: 999;
        background: linear-gradient(135deg, #011E6A 0%, #0047AB 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .filter-toggle:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

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
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Main application logic"""
    
    # Initialize session state
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    if 'sidebar_visible' not in st.session_state:
        st.session_state.sidebar_visible = True
    
    # Authentication
    if not check_password():
        return
    
    # Inject CSS
    inject_custom_css()
    
    # Header
    col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
    
    with col_h1:
        st.markdown(f"# {t('title')}")
        st.caption(t('subtitle'))
    
    with col_h2:
        lang_option = st.selectbox("Language", ["English", "Español"], 
                                   index=0 if st.session_state.language == 'en' else 1,
                                   label_visibility="collapsed")
        st.session_state.language = 'en' if lang_option == "English" else 'es'
    
    with col_h3:
        theme_option = st.selectbox("Theme", ["🌙 Dark", "☀️ Light"],
                                   index=0 if st.session_state.theme == 'dark' else 1,
                                   label_visibility="collapsed")
        st.session_state.theme = 'dark' if "Dark" in theme_option else 'light'
        
        if st.button(t('sign_out'), use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    st.markdown("---")
    
    # Floating toggle button (always visible)
    if not st.session_state.sidebar_visible:
        toggle_html = f"""
        <div class="filter-toggle" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'toggle_sidebar'}}, '*')">
            {t('toggle_filters')}
        </div>
        """
        st.markdown(toggle_html, unsafe_allow_html=True)
    
    # Toggle sidebar button
    if st.button(t('hide_filters') if st.session_state.sidebar_visible else t('toggle_filters'), 
                 key='sidebar_toggle'):
        st.session_state.sidebar_visible = not st.session_state.sidebar_visible
        st.rerun()
    
    # Sidebar (conditional)
    if st.session_state.sidebar_visible:
        with st.sidebar:
            st.markdown(f"### {t('data_source')}")
            
            uploaded_file = st.file_uploader(t('upload'), type=['xlsx', 'xls'], 
                                           help=t('upload_help'))
            
            if uploaded_file is not None:
                with st.spinner(t('processing')):
                    df, removed = load_data(uploaded_file)
                
                if df is None or len(df) == 0:
                    st.warning(t('no_data'))
                    return
                
                st.session_state.df = df
                st.success(f"{len(df):,} {t('records_loaded')}")
                
                if removed > 0:
                    st.info(f"{removed} {t('subtotals_removed')}")
                
                st.markdown("---")
                st.markdown(f"### {t('filters')}")
                
                # Counterparty Type filter
                all_types = [t('all')] + sorted(df['Counterparty Type'].dropna().unique().tolist())
                selected_types = st.multiselect(t('counterparty_type'), options=all_types, default=[t('all')])
                
                # Counterparty filter
                if t('all') in selected_types or not selected_types:
                    available_clients = sorted(df['Counterparty Name'].dropna().unique().tolist())
                else:
                    available_clients = sorted(
                        df[df['Counterparty Type'].isin([t for t in selected_types if t != t('all')])]['Counterparty Name'].dropna().unique().tolist()
                    )
                
                all_clients = [t('all')] + available_clients
                selected_clients = st.multiselect(t('counterparty'), options=all_clients, default=[t('all')])
                
                # Document Type filter
                if 'Document type' in df.columns:
                    all_doc_types = [t('all')] + sorted(df['Document type'].dropna().unique().tolist())
                    selected_doc_types = st.multiselect(t('document_type'), options=all_doc_types, default=[t('all')])
                else:
                    selected_doc_types = [t('all')]
                
                # Payment Terms filter
                if 'Payment terms' in df.columns:
                    all_payment_terms = [t('all')] + sorted(df['Payment terms'].dropna().unique().tolist())
                    selected_payment_terms = st.multiselect(t('payment_terms'), options=all_payment_terms, default=[t('all')])
                else:
                    selected_payment_terms = [t('all')]
                
                # Amount Range filter
                st.markdown(f"#### {t('amount_range')}")
                min_amount = float(df['Open Amount'].min())
                max_amount = float(df['Open Amount'].max())
                
                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    amount_min = st.number_input(t('min_amount'), 
                                                value=min_amount, 
                                                min_value=min_amount,
                                                max_value=max_amount,
                                                step=1000.0,
                                                format="%.2f")
                with col_a2:
                    amount_max = st.number_input(t('max_amount'), 
                                                value=max_amount,
                                                min_value=min_amount,
                                                max_value=max_amount,
                                                step=1000.0,
                                                format="%.2f")
                
                # Date Range filter
                st.markdown(f"#### {t('date_range')}")
                df['Document date'] = pd.to_datetime(df['Document date'], errors='coerce')
                date_min = df['Document date'].min()
                date_max = df['Document date'].max()
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    date_from = st.date_input(t('from_date'), 
                                             value=date_min,
                                             min_value=date_min,
                                             max_value=date_max)
                with col_d2:
                    date_to = st.date_input(t('to_date'), 
                                           value=date_max,
                                           min_value=date_min,
                                           max_value=date_max)
                
                # Apply all filters
                df_filtered = df.copy()
                
                # Counterparty Type filter
                if t('all') not in selected_types and selected_types:
                    df_filtered = df_filtered[df_filtered['Counterparty Type'].isin(selected_types)]
                
                # Counterparty filter
                if t('all') not in selected_clients and selected_clients:
                    df_filtered = df_filtered[df_filtered['Counterparty Name'].isin(selected_clients)]
                
                # Document Type filter
                if t('all') not in selected_doc_types and selected_doc_types and 'Document type' in df_filtered.columns:
                    df_filtered = df_filtered[df_filtered['Document type'].isin(selected_doc_types)]
                
                # Payment Terms filter
                if t('all') not in selected_payment_terms and selected_payment_terms and 'Payment terms' in df_filtered.columns:
                    df_filtered = df_filtered[df_filtered['Payment terms'].isin(selected_payment_terms)]
                
                # Amount range filter
                df_filtered = df_filtered[(df_filtered['Open Amount'] >= amount_min) & 
                                         (df_filtered['Open Amount'] <= amount_max)]
                
                # Date range filter
                df_filtered = df_filtered[(df_filtered['Document date'] >= pd.Timestamp(date_from)) & 
                                         (df_filtered['Document date'] <= pd.Timestamp(date_to))]
                
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
