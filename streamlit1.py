import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

#title
st.set_page_config(page_title = 'Super Store Analysis' , page_icon = ':bar_chart:' , layout = 'wide')

st.title(':bar_chart: Super Store EDA')
st.markdown('<style>div.block-container{padding-top:1rem;}<style>' , unsafe_allow_html = True)

# Using a File Uploader

f1 = st.file_uploader(':file_folder:' ,  type  =(['csv' , 'txt' , 'xlsx' , 'xls']))
if f1 is not None:
    filename  = f1.name
    st.write(filename)
    df = pd.read_excel(filename)
else:
    os.chdir(r'C:\Users\user\Desktop\MyMasterPiece')
    df = pd.read_excel('SuperStore Sales DataSet.xlsx' )
    

col1 , col2 = st.columns((2))

df['Order Date'] = pd.to_datetime(df['Order Date'])

startDate = pd.to_datetime(df['Order Date']).min()
endDate = pd.to_datetime(df['Order Date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input('Start Date' , startDate))
    
with col2:
    date2 =  pd.to_datetime(st.date_input('End Date' , endDate))
    
df = df[(df['Order Date'] >= date1) & (df['Order Date']<= date2)].copy()

st.sidebar.header('Choose Your Filter: ')
region  = st.sidebar.multiselect('Pick Your Region' , df['Region'].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]
    
# Create for State
state = st.sidebar.multiselect('Pick The State' , df2['State'].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(state)]
    
# Create a filter for City

city = st.sidebar.multiselect('Pick The City' , df3['City'].unique())



if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df  = df[df['Region'].isin(region)]
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

# Metrics KPI
st.divider()
filtered_df['Total_Sales'] = filtered_df['Sales']*filtered_df['Quantity']
k1 , k2 , k3 , k4 = st.columns(4)

k1.metric('Total Transactions', f'{filtered_df.Quantity.sum(): ,}')
k2.metric('Total Sales Amount' , f'{filtered_df.Total_Sales.sum(): ,.2f}')
k3.metric('Store Category' , f'{filtered_df.Category.nunique(): ,}')
k4.metric('Operations Regions' , f'{filtered_df.Region.nunique(): ,}')

st.divider()







# Charts

category_df = filtered_df.groupby(by = ['Category'] ,as_index = False )['Sales'].sum()

with col1:
    st.subheader('Category Wise Sales')
    fig = px.bar(category_df , x = 'Category' , y = 'Sales' , text = ['${: ,.2f}'.format(x) for x in category_df['Sales']],
                 template  ='seaborn')
    st.plotly_chart(fig , use_container_width = True , height = 200)
    
with col2:
    st.subheader('Region Wise Sales')
    fig = px.pie(filtered_df , values = 'Sales' , names = 'Region' , hole = .5)
    fig.update_traces(text = filtered_df['Region'] , textposition = 'outside')
    st.plotly_chart(fig , use_container_width = True)
    
 # Present Data    
cl1  ,cl2 = st.columns(2)   

with cl1:
    with st.expander('View Category Data'):
        st.write(category_df)
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button('Download Data', data = csv , file_name = 'Category.csv' , mime = 'text/csv' ,
                           help = 'Click Here to Download Data')
        
    

with cl2:
    with st.expander('View Region Data'):
        Region_df = filtered_df.groupby(by = 'Region' , as_index = False)['Sales'].sum()
        st.write(Region_df)
        csv = Region_df.to_csv(index = False).encode('utf-8')
        st.download_button('Download Data', data = csv , file_name = 'Region.csv' , mime = 'text/csv' ,
                           help = 'Click Here to Download Data')
        

st.divider()

# Funnel Plot

st.subheader('Sales Per Region')

funnel_stages = ['East', 'West','Central','South']
funnel_values = [ filtered_df.loc[filtered_df['Region']=='East' , ['Total_Sales']]['Total_Sales'].sum() ,
                 filtered_df.loc[filtered_df['Region']=='West' , ['Total_Sales']]['Total_Sales'].sum(), 
                 filtered_df.loc[filtered_df['Region']=='Central' , ['Total_Sales']]['Total_Sales'].sum(),
                 filtered_df.loc[filtered_df['Region']=='South' , ['Total_Sales']]['Total_Sales'].sum()]
#funnel_values = [10000 , 6000 , 4000 , 800]
fig_funnel = go.Figure(go.Funnel(y = funnel_stages ,  x= funnel_values, 
                                 marker= dict(color = ['green' , 'skyblue' , 'black' , 'grey'])))
fig_funnel.update_layout(height = 420 , margin = dict(t=10 , b=10))
st.plotly_chart(fig_funnel , use_container_width=True)


# Time Series Analysis
#filtered_df['Order Date'] = pd.to_datetime(filtered_df['Order Date'])
filtered_df['Year'] = filtered_df['Order Date'].dt.year
filtered_df['Month'] = filtered_df['Order Date'].dt.month
filtered_df.sort_values(by = ['Year' ] , ascending=False , inplace=True)
filtered_df['Month_year'] = filtered_df['Order Date'].dt.to_period('M')

st.subheader('Time Series Analysis')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df['Month_year'].dt.strftime('%Y : %b'))['Total_Sales'].sum()).reset_index()

fig2 = px.line(linechart , x = 'Month_year' , y = 'Total_Sales' , labels = {'Total_Sales': 'Amount'} , 
               height =500 , width = 1000 , template='gridon')
st.plotly_chart(fig2 , use_container_width=True)


st.subheader('Relationship Between Sales And Quantity')

fig3 = px.scatter(data_frame=  filtered_df , x = 'Quantity' , y  = 'Sales' , template='gridon' ,
                  height = 500 , width=1000 , trendline = 'ols')
st.plotly_chart(fig3 , use_container_width=True)

st.subheader('Relationships')

df = filtered_df.select_dtypes(include = ['number']).corr(method = 'pearson')
fig4 = px.imshow(df , text_auto=True , aspect='auto')
st.plotly_chart(fig4 , use_container_width=True)