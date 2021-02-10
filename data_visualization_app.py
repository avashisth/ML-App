import streamlit as st
import plotly_express as px
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import KNNImputer
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from numpy import percentile
from scipy import stats

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# title of the app
st.title("ML Process Guide")


# Setup file upload
uploaded_file = st.sidebar.file_uploader(
                        label="Upload your CSV or Excel file. (200MB max)",
                         type=['csv', 'xlsx'])

global df
if uploaded_file is not None:
    print(uploaded_file)
    print("hello")

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        print(e)
        df = pd.read_excel(uploaded_file)

global numeric_columns
global non_numeric_columns
try:
    
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    non_numeric_columns = list(df.select_dtypes(['object']).columns)
    non_numeric_columns.append(None)
    #print(non_numeric_columns)
except Exception as e:
    print(e)
    st.write("Please upload file to the application.")


def showPlots(chart_select):
    if chart_select == 'Scatterplots':
        st.sidebar.subheader("Scatterplot Settings")
        try:
            x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.scatter(data_frame=df, x=x_values, y=y_values, color=color_value)
            # display the chart
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Lineplots':
        st.sidebar.subheader("Line Plot Settings")
        try:
            x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.line(data_frame=df, x=x_values, y=y_values, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Histogram':
        st.sidebar.subheader("Histogram Settings")
        try:
            x = st.sidebar.selectbox('Feature', options=numeric_columns)
            bin_size = st.sidebar.slider("Number of Bins", min_value=10,
                                        max_value=100, value=40)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.histogram(x=x, data_frame=df, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Boxplot':
        st.sidebar.subheader("Boxplot Settings")
        try:
            y = st.sidebar.selectbox("Y axis", options=numeric_columns)
            x = st.sidebar.selectbox("X axis", options=non_numeric_columns)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.box(data_frame=df, y=y, x=x, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

def identifyData():
    descVal = st.sidebar.selectbox(label="select the property", 
    options=['Describe Data','Data Types','Data Shape']
    )

    if descVal == 'Describe Data':
        st.write(df.describe())
    elif descVal == 'Data Types':
        st.write(df.dtypes)
    elif descVal == 'Data Shape':
        st.write(df.shape)

    check_box = st.sidebar.checkbox(label="Display charts")

    if check_box:       
        chart_select = st.sidebar.selectbox(
        label="Select the chart type",
        options=['Scatterplots', 'Lineplots', 'Histogram', 'Boxplot']
        )
  
        showPlots(chart_select)

def corrAnalysis():
    st.write("Correlation Analysis")
    st.write(df.corr())
    fig = px.density_heatmap(df.corr())
    st.plotly_chart(fig)

def anamolyHandle():
     st.write("Anamolous data depiction")



def handleNull(df):
    
    col1, col2 = st.beta_columns(2)
    cat_data = df.select_dtypes(include=['object']).copy()
    col1.header("Categorical data: ")
    col1.write(cat_data.head())
    col1.write('Null values: ') 
    col1.write(cat_data.isna().sum())
    num_data = df.select_dtypes(include=['int64','float64']).copy()
    col2.header("Numerical data: ")
    col2.write(num_data.head())
    action = st.sidebar.selectbox( label="Select the action",
        options=['Handle null values', 'Handle outliers'])     
    
    if action == 'Handle null values':
        col2.write('Null values: ') 
        col2.write(num_data.isna().sum())
        imputer = KNNImputer(n_neighbors=4)
        imputer.fit(num_data)
        Xtrans=imputer.transform(num_data)
        st.write("Imputed values: ")
        st.dataframe(Xtrans)
    elif action == 'Handle outliers':
        st.sidebar.write("Outlier plot settings: ")
        x_val = st.sidebar.selectbox(label="Select x-axis value", options=non_numeric_columns)
        y_val = st.sidebar.selectbox(label="Select y-axis value", options=numeric_columns)
        colour = st.sidebar.selectbox(label="Select color value", options=non_numeric_columns)
        plot=px.box(df, x = x_val, y = y_val, color=colour)
        st.plotly_chart(plot)
        if st.button('Remove Outliers'):
            st.write(df.shape)
            rowNums = []
            for column in num_data:
                med = num_data[column].median()
                List=abs(num_data-med)
                cond=List.median()*4.5
                num_data[column] = List[~(List>cond)]

            st.write("Modified dataset")
            st.dataframe(num_data)
            st.write(num_data.shape)
        
        
        
            
          


    
    
    
    
    

    





#main method front page:
usr_model = st.selectbox ('Chose your process: ',('Select a process','Missing values and outlier handling','Identification of variables and data types', 'Correlation Analysis','Outlier and anamoly handling'))
if usr_model == 'Missing values and outlier handling' :
    handleNull(df)
elif usr_model == 'Identification of variables and data types' :
    identifyData()
elif usr_model == 'Correlation Analysis' :
    corrAnalysis()
elif usr_model == '' :
    handleAnamoly()
    



