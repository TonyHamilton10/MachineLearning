import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title='Super Store Analytics Dashboard',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state="expanded"
)

# ===== WORLD-CLASS CSS STYLING & ANIMATIONS =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* ===== HEADER SECTION ===== */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 50px 40px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
        animation: slideInDown 0.8s ease;
    }
    
    .header-title {
        font-size: 3.2em;
        font-weight: 800;
        color: white;
        margin-bottom: 10px;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
        letter-spacing: 1px;
    }
    
    .header-subtitle {
        font-size: 1.3em;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* ===== METRICS/KPI CARDS ===== */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-top: 4px solid #667eea;
        transition: all 0.3s ease;
        animation: slideUp 0.6s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.3);
    }
    
    .metric-icon {
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    
    .metric-label {
        font-size: 0.95em;
        color: #777;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 2.2em;
        font-weight: 700;
        color: #333;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        font-size: 1.6em;
        font-weight: 700;
        color: white;
        margin-top: 30px;
        margin-bottom: 20px;
        padding: 15px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.8s ease;
    }
    
    .subsection-header {
        font-size: 1.3em;
        font-weight: 700;
        color: #333;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
        letter-spacing: 0.5px;
    }
    
    /* ===== CHART CONTAINER ===== */
    .chart-container {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        animation: fadeIn 0.8s ease;
    }
    
    .chart-annotation {
        font-size: 0.95em;
        color: #666;
        margin-top: 15px;
        padding: 15px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-left: 4px solid #667eea;
        border-radius: 5px;
        font-style: italic;
        line-height: 1.6;
    }
    
    /* ===== FILTER SIDEBAR ===== */
    .sidebar-header {
        font-size: 1.3em;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    div.block-container {
        padding-top: 1rem;
        background: white;
        border-radius: 12px;
    }
    
    /* ===== NAVIGATION CARDS ===== */
    .nav-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
        animation: slideUp 0.6s ease;
        cursor: pointer;
    }
    
    .nav-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        border-left-color: #764ba2;
    }
    
    .nav-title {
        font-size: 1.2em;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .nav-description {
        font-size: 0.95em;
        color: #555;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
@st.cache_data
def load_data(file_path=None):
    """Load and validate data from file or default source"""
    try:
        if file_path is not None:
            # Determine file type and read accordingly
            file_extension = file_path.name.split('.')[-1].lower()
            if file_extension == 'csv':
                df = pd.read_csv(file_path)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file_path)
            else:
                st.error(f"❌ Unsupported file format: .{file_extension}")
                return None
        else:
            os.chdir(r'C:\Users\user\Desktop\MyMasterPiece')
            if not os.path.exists('SuperStore Sales DataSet.xlsx'):
                st.error("❌ Default dataset not found. Please upload a file.")
                return None
            df = pd.read_excel('SuperStore Sales DataSet.xlsx')
        
        # Validate data
        if df.empty:
            st.error("❌ Uploaded file is empty. Please provide a valid dataset.")
            return None
            
        # Convert date columns
        date_columns = df.select_dtypes(include=['object']).columns
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')
            except:
                pass
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

# ===== HEADER =====
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📊 Super Store Analytics Dashboard</h1>
    <p class="header-subtitle">Advanced Business Intelligence & Sales Performance Platform</p>
</div>
""", unsafe_allow_html=True)

# ===== FILE UPLOADER & DATA LOADING =====
st.markdown('<div class="section-header">📁 Data Source Selection</div>', unsafe_allow_html=True)

col_upload, col_info = st.columns([2, 1])

with col_upload:
    f1 = st.file_uploader('Upload Excel/CSV File', type=['csv', 'txt', 'xlsx', 'xls'])

# Load data with error handling
if f1 is not None:
    df = load_data(f1)
    if df is not None:
        with col_info:
            st.success(f'✅ File: **{f1.name}** ({len(df)} rows)')
    else:
        st.stop()  # Stop execution if data loading fails
else:
    df = load_data()
    if df is not None:
        with col_info:
            st.success(f'✅ Default Dataset ({len(df)} rows)')
    else:
        st.error("❌ Unable to load default dataset. Please upload a file.")
        st.stop()

# Validate required columns
if 'Order Date' not in df.columns:
    st.error("❌ Missing 'Order Date' column. Please ensure your dataset contains this column.")
    st.stop()

# ===== DATE RANGE FILTERS =====
st.markdown('<div class="section-header">📅 Date Range Filter</div>', unsafe_allow_html=True)

try:
    startDate = pd.to_datetime(df['Order Date']).min()
    endDate = pd.to_datetime(df['Order Date']).max()
except Exception as e:
    st.error(f"❌ Error processing dates: {str(e)}")
    st.stop()

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown('<p style="color: #333; font-weight: 600;">📅 Start Date</p>', unsafe_allow_html=True)
    date1 = pd.to_datetime(st.date_input('Start Date', startDate, label_visibility="collapsed"))
    
with col2:
    st.markdown('<p style="color: #333; font-weight: 600;">📅 End Date</p>', unsafe_allow_html=True)
    date2 = pd.to_datetime(st.date_input('End Date', endDate, label_visibility="collapsed"))

with col3:
    st.markdown('<p style="color: #333; font-weight: 600;">📊 Date Range</p>', unsafe_allow_html=True)
    date_range = (date2 - date1).days
    st.markdown(f"<p style='color: #667eea; font-weight: 600; margin-top: 5px;'>{date_range} days</p>", unsafe_allow_html=True)

# Validate date range
if date1 > date2:
    st.error("❌ Start Date must be before End Date")
    st.stop()
    
df = df[(df['Order Date'] >= date1) & (df['Order Date'] <= date2)].copy()

# Warn if no data in selected range
if len(df) == 0:
    st.warning("⚠️ No data found in the selected date range. Please adjust your filters.")
    st.stop()

# ===== ADVANCED SIDEBAR FILTERS =====
st.sidebar.markdown("""
<style>
    .sidebar-header {
        font-size: 1.3em;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }
</style>
<div class="sidebar-header">⚙️ Advanced Filters</div>
""", unsafe_allow_html=True)

region = st.sidebar.multiselect('🌍 Pick Your Region', df['Region'].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]
    
state = st.sidebar.multiselect('🏛️ Pick The State', df2['State'].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(state)]
    
city = st.sidebar.multiselect('🏙️ Pick The City', df3['City'].unique())

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df['Region'].isin(region)]
elif not region and not city:
    filtered_df = df[df['State'].isin(state)]
elif state and city:
    filtered_df = df3[df['State'].isin(state) & df3['City'].isin(city)]
elif region and city:
    filtered_df = df3[df['Region'].isin(region) & df3['City'].isin(city)]
elif region and state:
    filtered_df = df3[df['Region'].isin(region) & df3['State'].isin(state)]
elif city:
    filtered_df = df3[df3['City'].isin(city)]
else:
    filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3['City'].isin(city)]

# ===== KPI METRICS SECTION =====
st.markdown('<div class="section-header">📈 Key Performance Indicators (KPIs)</div>', unsafe_allow_html=True)

try:
    # Ensure required columns exist
    if 'Quantity' not in filtered_df.columns or 'Sales' not in filtered_df.columns:
        st.warning("⚠️ Required columns (Quantity/Sales) not found in dataset")
    else:
        filtered_df['Total_Sales'] = filtered_df['Sales'] * filtered_df['Quantity']
        
        total_qty = filtered_df['Quantity'].sum()
        total_sales = filtered_df['Total_Sales'].sum()
        total_categories = filtered_df['Category'].nunique()
        total_regions = filtered_df['Region'].nunique()
        avg_order_value = total_sales / max(len(filtered_df), 1)
        
        k1, k2, k3, k4 = st.columns(4)
        
        with k1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📦</div>
                <div class="metric-label">Total Transactions</div>
                <div class="metric-value">{int(total_qty):,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with k2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">💰</div>
                <div class="metric-label">Total Sales Amount</div>
                <div class="metric-value">${total_sales:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with k3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🏪</div>
                <div class="metric-label">Store Categories</div>
                <div class="metric-value">{int(total_categories):,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with k4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-label">Avg Order Value</div>
                <div class="metric-value">${avg_order_value:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"❌ Error calculating KPIs: {str(e)}")

# ===== CHARTS SECTION =====
st.markdown('<div class="section-header">📊 Sales Analysis & Visualization</div>', unsafe_allow_html=True)

category_df = filtered_df.groupby(by=['Category'], as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)

col1, col2 = st.columns(2)

# ===== CATEGORY WISE SALES - BAR CHART =====
with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-header">📊 Category-wise Sales Performance</div>', unsafe_allow_html=True)
    
    fig = px.bar(
        category_df,
        x='Category',
        y='Sales',
        text=[f'${x:,.2f}' for x in category_df['Sales']],
        color='Sales',
        color_continuous_scale='Viridis',
        template='plotly_white',
        labels={'Sales': 'Sales Amount ($)', 'Category': 'Product Category'},
        hover_data={'Sales': ':.2f'}
    )
    
    fig.update_traces(
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>',
        marker=dict(line=dict(width=2, color='white'))
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        hovermode='x unified',
        xaxis=dict(title='Product Category', title_font=dict(size=12, color='#333')),
        yaxis=dict(title='Sales ($)', title_font=dict(size=12, color='#333')),
        font=dict(family='Poppins', color='#333', size=11),
        plot_bgcolor='rgba(240, 244, 255, 0.5)',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="chart-annotation">
    💡 <b>Key Insight:</b> This bar chart displays total sales revenue by product category, automatically sorted from highest to lowest sales. Each bar represents a different category with the exact sales amount displayed on top. Wider bars indicate stronger market performance. This metric helps identify which product lines are driving the most revenue and where to focus marketing efforts.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== REGION WISE SALES - DONUT CHART =====
with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-header">🌍 Regional Sales Distribution</div>', unsafe_allow_html=True)
    
    region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
    
    colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
    fig = px.pie(
        region_sales,
        values='Sales',
        names='Region',
        hole=0.4,
        color_discrete_sequence=colors,
        labels={'Sales': 'Sales Amount ($)', 'Region': 'Region'},
        hover_data={'Sales': ':.2f'}
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>',
        marker=dict(line=dict(width=3, color='white'))
    )
    
    fig.update_layout(
        height=500,
        font=dict(family='Poppins', color='#333', size=11),
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(x=0.85, y=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="chart-annotation">
    💡 <b>Key Insight:</b> This donut chart visualizes how sales revenue is distributed across different geographic regions. The percentage labels show each region's contribution to total sales. A balanced distribution indicates healthy market penetration, while concentrated sales in one region suggests opportunity for geographic expansion and market development.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== DATA ANALYSIS SECTION =====
st.markdown('<div class="section-header">📑 Detailed Data Analysis & Export</div>', unsafe_allow_html=True)

cl1, cl2 = st.columns(2)

with cl1:
    with st.expander('📋 Category Performance Data', expanded=False):
        st.markdown('<p style="color: #667eea; font-weight: 600; margin-bottom: 15px;">Category Sales Summary</p>', unsafe_allow_html=True)
        
        st.dataframe(category_df, use_container_width=True, hide_index=True)
        
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='⬇️ Download Category Data (CSV)',
            data=csv,
            file_name='Category_Sales.csv',
            mime='text/csv',
            use_container_width=True,
            help='Export category sales data for further analysis'
        )

with cl2:
    with st.expander('🌍 Regional Performance Data', expanded=False):
        st.markdown('<p style="color: #667eea; font-weight: 600; margin-bottom: 15px;">Regional Sales Summary</p>', unsafe_allow_html=True)
        
        Region_df = filtered_df.groupby(by='Region', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)
        st.dataframe(Region_df, use_container_width=True, hide_index=True)
        
        csv = Region_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='⬇️ Download Regional Data (CSV)',
            data=csv,
            file_name='Regional_Sales.csv',
            mime='text/csv',
            use_container_width=True,
            help='Export regional sales data for further analysis'
        )

# ===== FUNNEL CHART SECTION =====
st.markdown('<div class="section-header">🔻 Sales Funnel Analysis by Region</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="subsection-header">🌐 Regional Sales Funnel</div>', unsafe_allow_html=True)

funnel_stages = ['East', 'West', 'Central', 'South']
funnel_values = [
    filtered_df.loc[filtered_df['Region'] == 'East', ['Total_Sales']]['Total_Sales'].sum(),
    filtered_df.loc[filtered_df['Region'] == 'West', ['Total_Sales']]['Total_Sales'].sum(),
    filtered_df.loc[filtered_df['Region'] == 'Central', ['Total_Sales']]['Total_Sales'].sum(),
    filtered_df.loc[filtered_df['Region'] == 'South', ['Total_Sales']]['Total_Sales'].sum()
]

sorted_pairs = sorted(zip(funnel_stages, funnel_values), key=lambda x: x[1], reverse=True)
funnel_stages_sorted, funnel_values_sorted = zip(*sorted_pairs)

fig_funnel = go.Figure(go.Funnel(
    y=list(funnel_stages_sorted),
    x=list(funnel_values_sorted),
    text=[f'${x:,.0f}' for x in funnel_values_sorted],
    textposition='inside',
    textfont=dict(size=12, color='white', family='Poppins'),
    marker=dict(
        color=['#667eea', '#764ba2', '#f093fb', '#4facfe'],
        line=dict(width=2, color='white')
    ),
    hovertemplate='<b>%{y}</b><br>Total Sales: $%{x:,.2f}<extra></extra>'
))

fig_funnel.update_layout(
    height=450,
    margin=dict(t=30, b=10, l=20, r=20),
    font=dict(family='Poppins', color='#333', size=12),
    paper_bgcolor='white',
    plot_bgcolor='rgba(240, 244, 255, 0.5)',
    hovermode='closest'
)

st.plotly_chart(fig_funnel, use_container_width=True)

st.markdown("""
<div class="chart-annotation">
💡 <b>Key Insight:</b> The funnel chart displays total sales revenue across regions, automatically arranged in descending order from top to bottom. Wider funnel sections represent higher revenue contributions. This visualization helps identify regional performance hierarchy, showing which regions generate the most sales and which require development strategies or resource allocation adjustments.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===== SIDEBAR NAVIGATION INFO =====
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; color: white;">
    <h2 style="margin: 0; font-size: 1.3em;">📊 Multi-Page Dashboard</h2>
    <p style="margin: 10px 0 0 0; font-size: 0.9em; opacity: 0.9;">Navigate using the pages menu above</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="background: #f0f4ff; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea;">
    <p style="margin: 0; font-weight: 600; color: #667eea;">🗺️ Available Pages:</p>
    <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9em;">
        • <b>Dashboard</b> - Main overview & KPIs<br>
        • <b>Advanced Analysis</b> - Deep category insights<br>
        • <b>Regional Intelligence</b> - Geographic analytics
    </p>
</div>
""", unsafe_allow_html=True)

# ===== EXPLORE OTHER PAGES SECTION =====
st.markdown('<div class="section-header">🔍 Explore More Insights</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-title">🔬 Advanced Analysis</div>
        <div class="nav-description">
        Deep dive into subcategory performance, profit vs sales correlation, and detailed market analysis. Use advanced filters to explore specific categories and understand profitability metrics.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-title">🌍 Regional Intelligence</div>
        <div class="nav-description">
        Geographic performance analysis including regional KPIs, state-wise performance, and customer segment breakdowns. Identify market opportunities and expansion possibilities.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="background: #f0f4ff; padding: 20px; border-radius: 10px; text-align: center; margin-top: 30px; border: 2px solid #667eea;">
    <p style="margin: 0; color: #667eea; font-weight: 600;">👉 Use the navigation menu above to explore other dashboard pages!</p>
</div>
""", unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <p style="margin: 0; font-size: 1.1em; font-weight: 600;">© 2026 Super Store Analytics Dashboard</p>
    <p style="margin: 8px 0 0 0; font-size: 0.95em; opacity: 0.9;">Multi-Page Business Intelligence Platform | Powered by Advanced Analytics</p>
</div>
""", unsafe_allow_html=True)
#               height =500 , width = 1000 , template='gridon')
#st.plotly_chart(fig2 , use_container_width=True)


# ===== ADVANCED INSIGHTS SECTION =====
st.markdown('<div class="section-header">🔗 Advanced Correlations & Relationships</div>', unsafe_allow_html=True)

# Quantity vs Sales Scatter Plot
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="subsection-header">📊 Sales vs Quantity Relationship</div>', unsafe_allow_html=True)

fig3 = px.scatter(
    data_frame=filtered_df,
    x='Quantity',
    y='Sales',
    template='plotly_white',
    height=500,
    trendline='ols',
    labels={'Quantity': 'Order Quantity (Units)', 'Sales': 'Sales Amount ($)'},
    hover_data={'Quantity': ':.0f', 'Sales': ':.2f'},
    color_discrete_sequence=['#667eea']
)

fig3.update_traces(
    hovertemplate='<b>Quantity:</b> %{x} units<br><b>Sales:</b> $%{y:,.2f}<extra></extra>',
    marker=dict(size=8, opacity=0.7, line=dict(width=1, color='white'))
)

fig3.update_layout(
    font=dict(family='Poppins', color='#333', size=11),
    plot_bgcolor='rgba(240, 244, 255, 0.5)',
    paper_bgcolor='white',
    xaxis=dict(title_font=dict(size=12, color='#333')),
    yaxis=dict(title_font=dict(size=12, color='#333')),
    hovermode='closest'
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
<div class="chart-annotation">
💡 <b>Key Insight:</b> This scatter plot with trend line reveals the relationship between order quantity and sales amount. The upward trend indicates a positive correlation between quantity ordered and total sales revenue. The trend line (OLS regression) helps identify the average sales contribution per unit sold, useful for forecasting and pricing strategies.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Correlation Heatmap
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="subsection-header">🔥 Correlation Matrix - Numerical Features</div>', unsafe_allow_html=True)

# Create correlation matrix
numeric_df = filtered_df.select_dtypes(include=['number']).copy()
if numeric_df.shape[1] > 0:
    correlation_matrix = numeric_df.corr(method='pearson')
    
    fig4 = px.imshow(
        correlation_matrix,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu_r',
        zmin=-1,
        zmax=1,
        labels={'color': 'Correlation'},
        height=450
    )
    
    fig4.update_layout(
        font=dict(family='Poppins', color='#333', size=11),
        paper_bgcolor='white',
        title_x=0.5,
        xaxis_title='',
        yaxis_title='',
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("""
    <div class="chart-annotation">
    💡 <b>Key Insight:</b> The correlation matrix (heatmap) shows relationships between numerical variables:
    <br>• <b>Red colors</b> = Strong negative correlation (inverse relationship)
    <br>• <b>Blue colors</b> = Strong positive correlation (direct relationship)
    <br>• <b>White colors</b> = No correlation
    <br>Understanding these relationships helps identify dependencies for forecasting and strategic planning.
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ No numerical data available for correlation analysis")

st.markdown('</div>', unsafe_allow_html=True)

# ===== SUMMARY STATISTICS SECTION =====
st.markdown('<div class="section-header">📊 Summary Statistics & Data Profile</div>', unsafe_allow_html=True)

with st.expander('📈 Statistical Summary of Filtered Data', expanded=False):
    st.markdown('<p style="color: #667eea; font-weight: 600; margin-bottom: 15px;">Descriptive Statistics</p>', unsafe_allow_html=True)
    
    numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        summary_stats = filtered_df[numeric_cols].describe().round(2)
        st.dataframe(summary_stats, use_container_width=True)
        
        # Download statistics
        csv_stats = summary_stats.to_csv().encode('utf-8')
        st.download_button(
            label='⬇️ Download Summary Statistics (CSV)',
            data=csv_stats,
            file_name='Summary_Statistics.csv',
            mime='text/csv',
            use_container_width=True,
            help='Export statistical summary for further analysis'
        )
    else:
        st.info("ℹ️ No numerical columns available for statistical analysis")

# ===== DATASET OVERVIEW =====
st.markdown('<div class="section-header">📋 Dataset Overview & Raw Data</div>', unsafe_allow_html=True)

col_overview1, col_overview2, col_overview3 = st.columns(3)

with col_overview1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-label">Total Records</div>
        <div class="metric-value">{len(filtered_df):,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col_overview2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-label">Total Columns</div>
        <div class="metric-value">{len(filtered_df.columns)}</div>
    </div>
    """, unsafe_allow_html=True)

with col_overview3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">⚠️</div>
        <div class="metric-label">Missing Values</div>
        <div class="metric-value">{filtered_df.isna().sum().sum():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with st.expander('🗂️ View Raw Data Table', expanded=False):
    st.markdown('<p style="color: #667eea; font-weight: 600; margin-bottom: 15px;">Complete Filtered Dataset</p>', unsafe_allow_html=True)
    
    # Add column selection for better visibility
    columns_to_display = st.multiselect(
        '📋 Select columns to display (leave empty for all):',
        options=filtered_df.columns.tolist(),
        default=filtered_df.columns.tolist()
    )
    
    display_df = filtered_df[columns_to_display] if columns_to_display else filtered_df
    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Download complete dataset
    csv_full = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label='⬇️ Download Complete Dataset (CSV)',
        data=csv_full,
        file_name='Complete_Dataset.csv',
        mime='text/csv',
        use_container_width=True,
        help='Export entire filtered dataset for external analysis'
    )

# ===== PROFESSIONAL FOOTER =====
st.markdown("""
<div style="border-top: 2px solid #667eea; margin-top: 50px; padding-top: 30px;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
        <div>
            <p style="margin: 0; color: #667eea; font-weight: 600; font-size: 1.1em;">© 2026 Super Store Analytics Dashboard</p>
            <p style="margin: 5px 0 0 0; color: #999; font-size: 0.85em;">Multi-Page Business Intelligence Platform | Enterprise-Grade Analytics</p>
        </div>
        <div style="text-align: right; color: #999; font-size: 0.85em;">
            <p style="margin: 0;">📊 Data-Driven Insights</p>
            <p style="margin: 5px 0 0 0;">🚀 Powered by Streamlit & Plotly</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)