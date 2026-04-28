"""
AMRIZE AR DASHBOARD v1.0
Professional Accounts Receivable Analytics Platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO

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
AMZ_GOLD = "#FFB800"
S_GREEN = "#059669"
S_RED = "#DC2626"
S_AMBER = "#D97706"
S_YELLOW = "#F59E0B"
S_GRAY = "#6B7280"

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
    """Format as USD currency"""
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
    """Return color scheme based on theme"""
    if theme == 'dark':
        return {
            'bg_primary': '#0F172A',
            'bg_secondary': '#1E293B',
            'bg_card': '#1E293B',
            'text_primary': '#F1F5F9',
            'text_secondary': '#94A3B8',
            'border': '#334155',
            'accent': AMZ_SKY
        }
    else:
        return {
            'bg_primary': '#FFFFFF',
            'bg_secondary': '#F8FAFC',
            'bg_card': '#FFFFFF',
            'text_primary': '#1E293B',
            'text_secondary': '#64748B',
            'border': '#E2E8F0',
            'accent': AMZ_ROYAL
        }


# ═══════════════════════════════════════════════════════════════════════
# PROFESSIONAL CSS
# ═══════════════════════════════════════════════════════════════════════

def inject_css(theme='light'):
    """Inject professional CSS"""
    colors = get_color_scheme(theme)
    
    css = f"""
    <style>
    /* Global Reset */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    /* Main Container */
    .main {{
        background-color: {colors['bg_secondary']};
        color: {colors['text_primary']};
        padding: 0 !important;
    }}
    
    .block-container {{
        padding: 1.5rem 2rem !important;
        max-width: 100% !important;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {AMZ_MIDNIGHT} 0%, {AMZ_ROYAL} 100%);
        padding-top: 2rem;
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] label {{
        color: white !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.1);
        border: 1px dashed rgba(255,255,255,0.3);
        border-radius: 6px;
        padding: 1.5rem;
    }}
    
    [data-testid="stFileUploader"] label {{
        color: white !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stFileUploader"] section {{
        border: none !important;
    }}
    
    [data-testid="stFileUploader"] small {{
        color: rgba(255,255,255,0.7) !important;
    }}
    
    /* Header */
    .main-header {{
        background: linear-gradient(135deg, {AMZ_MIDNIGHT} 0%, {AMZ_ROYAL} 100%);
        padding: 1.5rem 2rem;
        margin: -1.5rem -2rem 1.5rem -2rem;
        border-bottom: 3px solid {AMZ_SKY};
    }}
    
    .main-title {{
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }}
    
    .main-subtitle {{
        color: {AMZ_SKY};
        font-size: 0.95rem;
        margin: 0.3rem 0 0;
        font-weight: 400;
    }}
    
    /* KPI Cards */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .kpi-card {{
        background: {colors['bg_card']};
        border: 1px solid {colors['border']};
        border-radius: 6px;
        padding: 1.2rem;
        transition: all 0.2s ease;
    }}
    
    .kpi-card:hover {{
        border-color: {AMZ_SKY};
        box-shadow: 0 2px 8px rgba(0,167,225,0.15);
    }}
    
    .kpi-label {{
        font-size: 0.75rem;
        font-weight: 600;
        color: {colors['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }}
    
    .kpi-value {{
        font-size: 1.6rem;
        font-weight: 700;
        color: {colors['text_primary']};
        line-height: 1.2;
        margin-bottom: 0.3rem;
    }}
    
    .kpi-delta {{
        font-size: 0.8rem;
        color: {colors['text_secondary']};
        font-weight: 500;
    }}
    
    .kpi-delta.positive {{ color: {S_GREEN}; }}
    .kpi-delta.negative {{ color: {S_RED}; }}
    
    /* Section Headers */
    .section-header {{
        font-size: 1rem;
        font-weight: 700;
        color: {colors['text_primary']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {colors['border']};
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {AMZ_ROYAL}, {AMZ_SKY});
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 4px 12px rgba(0,71,171,0.25);
        transform: translateY(-1px);
    }}
    
    /* Metrics */
    [data-testid="stMetric"] {{
        background: {colors['bg_card']};
        padding: 0.8rem;
        border-radius: 4px;
        border: 1px solid {colors['border']};
    }}
    
    [data-testid="stMetric"] label {{
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: {colors['text_secondary']} !important;
    }}
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }}
    
    /* Dataframe */
    .dataframe {{
        font-size: 0.85rem !important;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Compact spacing */
    .element-container {{
        margin-bottom: 0.5rem !important;
    }}
    
    /* Chart containers */
    .chart-container {{
        background: {colors['bg_card']};
        border: 1px solid {colors['border']};
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 1rem;
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def kpi_card(label, value, delta=None, delta_type='neutral'):
    """Render professional KPI card"""
    delta_class = f'kpi-delta {delta_type}'
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ''
    
    html = f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """
    return html


# ═══════════════════════════════════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════

def check_authentication():
    """Secure authentication system"""
    
    try:
        correct_password = st.secrets.get("AR_PASSWORD", "AMRIZE2024")
    except:
        correct_password = "AMRIZE2024"
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    # Professional login screen
    st.markdown(f"""
    <div style='max-width: 400px; margin: 5rem auto; padding: 2.5rem;
                background: linear-gradient(135deg, {AMZ_MIDNIGHT}, {AMZ_ROYAL});
                border-radius: 8px; box-shadow: 0 10px 40px rgba(0,0,0,0.2);'>
        <h1 style='color: white; margin: 0 0 0.5rem; font-size: 1.8rem; font-weight: 700;'>
            AMRIZE
        </h1>
        <p style='color: {AMZ_SKY}; margin: 0 0 2rem; font-size: 0.95rem;'>
            Accounts Receivable Dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        st.markdown("#### Access Control")
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )
        
        submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
        
        if submitted:
            if password == correct_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    return False


# ═══════════════════════════════════════════════════════════════════════
# DATA PROCESSING
# ═══════════════════════════════════════════════════════════════════════

def load_and_process_data(uploaded_file):
    """Load and process SAP AR file"""
    
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Remove SAP subtotals
        initial_rows = len(df)
        df = df[df['Document date'] != 'Result'].copy()
        removed_rows = initial_rows - len(df)
        
        # Convert dates
        df['Document date'] = pd.to_datetime(df['Document date'], errors='coerce')
        df['Net due date'] = pd.to_datetime(df['Net due date'], errors='coerce')
        
        # Clean numeric columns
        numeric_columns = [
            'Open Amount', 'Credit Limit', 'Current Amount',
            '1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays',
            '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '').replace('nan', '0')
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Preserve SP #
        if 'SP #' in df.columns:
            df['SP #'] = df['SP #'].astype(str).replace('nan', '').replace('None', '')
        
        # Calculated columns
        df['Debt_Type'] = df['Open Amount'].apply(
            lambda x: 'Debt' if x > 0 else ('Credit' if x < 0 else 'Zero')
        )
        
        today = pd.Timestamp.now()
        df['Days_Overdue'] = (today - df['Net due date']).dt.days
        df['Days_Overdue'] = df['Days_Overdue'].fillna(0).astype(int)
        
        df['Status'] = df.apply(lambda row: 
            'Overdue' if row['Days_Overdue'] > 0 and row['Open Amount'] > 0
            else 'Current' if row['Open Amount'] > 0
            else 'Credit',
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
    """Calculate dashboard KPIs"""
    
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
    """Professional aging chart"""
    
    aging_cols = [
        'Current Amount', '1 - 30\ndays', '31 - 60\ndays', '61 - 90\ndays',
        '91 - 120\ndays', '121 - 180\ndays', '181 - 365\ndays', '> 365\ndays'
    ]
    
    aging_data = []
    for col in aging_cols:
        if col in df.columns:
            total = df[col].sum()
            aging_data.append({
                'Bucket': col.replace('\n', ' '),
                'Amount': abs(total)
            })
    
    df_aging = pd.DataFrame(aging_data)
    
    colors = [S_GREEN, AMZ_SKY, AMZ_ROYAL, S_AMBER, S_YELLOW, '#FFA500', '#FF6B35', S_RED]
    
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
        title={'text': 'Aging Analysis', 'font': {'size': 14, 'weight': 'bold', 'color': text_color}},
        xaxis_title=None,
        yaxis_title='Amount (USD)',
        height=320,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, family='Inter, sans-serif', size=10),
        margin=dict(l=50, r=30, t=50, b=40),
        xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor=grid_color, gridwidth=0.5),
        hovermode='x unified'
    )
    
    return fig


def create_top_debtors_chart(df, top_n=10, theme='light'):
    """Professional top debtors chart"""
    
    debtors = df[df['Open Amount'] > 0].groupby('Counterparty Name').agg({
        'Open Amount': 'sum'
    }).reset_index()
    
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
        title={'text': f'Top {top_n} Debtors', 'font': {'size': 14, 'weight': 'bold', 'color': text_color}},
        xaxis_title='Outstanding Amount (USD)',
        yaxis_title=None,
        height=320,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, family='Inter, sans-serif', size=10),
        margin=dict(l=180, r=50, t=50, b=40),
        xaxis=dict(showgrid=True, gridcolor=grid_color, gridwidth=0.5),
        yaxis=dict(showgrid=False, tickfont=dict(size=9)),
        hovermode='y unified'
    )
    
    return fig


def create_status_donut(df, theme='light'):
    """Professional status donut chart"""
    
    df_debt = df[df['Open Amount'] > 0].copy()
    status_counts = df_debt.groupby('Status').agg({'Open Amount': 'sum'}).reset_index()
    
    color_map = {'Current': S_GREEN, 'Overdue': S_RED, 'Credit': AMZ_SKY}
    colors = [color_map.get(status, S_GRAY) for status in status_counts['Status']]
    
    fig = go.Figure(data=[go.Pie(
        labels=status_counts['Status'],
        values=status_counts['Open Amount'],
        hole=0.5,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='label+percent',
        textfont=dict(size=11),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<extra></extra>'
    )])
    
    bg_color = '#1E293B' if theme == 'dark' else 'white'
    text_color = '#F1F5F9' if theme == 'dark' else '#1E293B'
    
    fig.update_layout(
        title={'text': 'Portfolio Status', 'font': {'size': 14, 'weight': 'bold', 'color': text_color}},
        height=320,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, family='Inter, sans-serif', size=10),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=20, r=20, t=50, b=60)
    )
    
    return fig


# ═══════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Main dashboard application"""
    
    # Authentication
    if not check_authentication():
        return
    
    # Initialize theme
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # Inject CSS
    inject_css(st.session_state.theme)
    
    # Header
    col_h1, col_h2 = st.columns([5, 1])
    with col_h1:
        st.markdown("""
        <div class="main-header">
            <div class="main-title">AMRIZE AR DASHBOARD</div>
            <div class="main-subtitle">Accounts Receivable Analytics</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h2:
        theme_label = "Dark" if st.session_state.theme == 'light' else "Light"
        if st.button(f"◐ {theme_label}", use_container_width=True):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### DATA SOURCE")
        
        uploaded_file = st.file_uploader(
            "Upload AR Report",
            type=['csv', 'xlsx', 'xls'],
            help="SAP Accounts Receivable export file"
        )
        
        if uploaded_file is not None:
            with st.spinner("Processing..."):
                df, error, removed = load_and_process_data(uploaded_file)
            
            if error:
                st.error(error)
                return
            
            if df is None or len(df) == 0:
                st.warning("No valid data found")
                return
            
            st.session_state.df = df
            st.success(f"{len(df):,} records loaded")
            
            if removed > 0:
                st.info(f"{removed} SAP subtotals removed")
            
            st.markdown("---")
            st.markdown("### FILTERS")
            
            # Type filter
            all_types = ['All'] + sorted(df['Counterparty Type'].dropna().unique().tolist())
            selected_types = st.multiselect("Counterparty Type", options=all_types, default=['All'])
            
            # Client filter
            if 'All' in selected_types or not selected_types:
                available_clients = sorted(df['Counterparty Name'].dropna().unique().tolist())
            else:
                available_clients = sorted(
                    df[df['Counterparty Type'].isin([t for t in selected_types if t != 'All'])]['Counterparty Name'].dropna().unique().tolist()
                )
            
            all_clients = ['All'] + available_clients
            selected_clients = st.multiselect("Counterparty", options=all_clients, default=['All'])
            
            # Apply filters
            df_filtered = df.copy()
            
            if 'All' not in selected_types and selected_types:
                df_filtered = df_filtered[df_filtered['Counterparty Type'].isin(selected_types)]
            
            if 'All' not in selected_clients and selected_clients:
                df_filtered = df_filtered[df_filtered['Counterparty Name'].isin(selected_clients)]
            
            st.session_state.df_filtered = df_filtered
            
            st.markdown("---")
            st.metric("Filtered Records", f"{len(df_filtered):,}")
            
            st.markdown("---")
            if st.button("Sign Out", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
        
        else:
            st.info("Upload a file to begin")
    
    # Main content
    if 'df_filtered' not in st.session_state:
        st.info("**Upload an AR report file to begin analysis**")
        return
    
    df_filtered = st.session_state.df_filtered
    kpis = calculate_kpis(df_filtered)
    
    # KPIs
    st.markdown("### KEY PERFORMANCE INDICATORS")
    
    kpi_html = f"""
    <div class="kpi-grid">
        {kpi_card("Gross Receivables", human_format(kpis['gross_debt']), f"{kpis['total_invoices']:,} invoices", 'neutral')}
        {kpi_card("Customer Credits", human_format(kpis['credits']), "Advance payments", 'positive')}
        {kpi_card("Current %", fmt_pct(kpis['pct_current']), f"Overdue: {fmt_pct(kpis['pct_overdue'])}", 'negative' if kpis['pct_overdue'] > 50 else 'neutral')}
        {kpi_card("Credit Risk", str(kpis['credit_risk_count']), f"of {kpis['unique_customers']} customers", 'negative' if kpis['credit_risk_count'] > 0 else 'positive')}
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)
    
    # Secondary KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", f"{kpis['unique_customers']:,}")
    with col2:
        st.metric("Avg Invoice", human_format(kpis['avg_invoice']))
    with col3:
        st.metric("Overdue Amount", human_format(kpis['overdue_amount']))
    with col4:
        st.metric("Avg Days Overdue", f"{int(kpis['avg_days_overdue'])}")
    
    st.markdown("---")
    
    # Charts
    st.markdown("### ANALYTICS")
    
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
    
    st.markdown("---")
    
    # Data Table
    st.markdown("### DETAILED RECORDS")
    
    display_columns = [
        'Counterparty Name', 'Counterparty Type', 'INV # - Salesforce', 'SP #',
        'Document date', 'Net due date', 'Open Amount', 'Credit Limit', 'Status', 'Days_Overdue'
    ]
    
    df_display = df_filtered[display_columns].copy()
    df_display.columns = [
        'Customer', 'Type', 'Invoice #', 'SP #', 'Doc Date', 'Due Date',
        'Open Amount', 'Credit Limit', 'Status', 'Days Overdue'
    ]
    
    df_display = df_display.sort_values('Open Amount', ascending=False)
    
    column_config = {
        'Open Amount': st.column_config.NumberColumn('Open Amount', format='$%.2f'),
        'Credit Limit': st.column_config.NumberColumn('Credit Limit', format='$%.2f'),
        'Doc Date': st.column_config.DateColumn('Doc Date', format='YYYY-MM-DD'),
        'Due Date': st.column_config.DateColumn('Due Date', format='YYYY-MM-DD'),
        'Days Overdue': st.column_config.NumberColumn('Days Overdue', format='%d')
    }
    
    st.dataframe(df_display, use_container_width=True, height=350, column_config=column_config, hide_index=True)
    
    # Export
    col_e1, col_e2, col_e3 = st.columns([1, 1, 3])
    
    with col_e1:
        if st.button("Export Excel", use_container_width=True, type="primary"):
            try:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_display.to_excel(writer, sheet_name='Data', index=False)
                    
                    kpi_summary = pd.DataFrame({
                        'KPI': ['Gross Receivables', 'Customer Credits', 'Current %', 'Overdue %',
                               'Credit Risk', 'Total Customers', 'Total Invoices', 'Avg Invoice', 'Avg Days Overdue'],
                        'Value': [fmt_currency(kpis['gross_debt']), fmt_currency(kpis['credits']),
                                 fmt_pct(kpis['pct_current']), fmt_pct(kpis['pct_overdue']),
                                 kpis['credit_risk_count'], kpis['unique_customers'], kpis['total_invoices'],
                                 fmt_currency(kpis['avg_invoice']), f"{int(kpis['avg_days_overdue'])} days"]
                    })
                    kpi_summary.to_excel(writer, sheet_name='KPIs', index=False)
                
                output.seek(0)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                st.download_button(
                    label="Download",
                    data=output,
                    file_name=f"AR_Report_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Export error: {e}")
    
    with col_e2:
        if st.button("Export CSV", use_container_width=True):
            csv = df_display.to_csv(index=False)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            st.download_button("Download", data=csv, file_name=f"AR_Report_{timestamp}.csv",
                             mime="text/csv", use_container_width=True)


if __name__ == "__main__":
    main()