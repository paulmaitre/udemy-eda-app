import streamlit as st
import pandas as pd 
import plotly.express as px

st.header("Header")
st.subheader('Sub HEader')
st.title('Title')
st.markdown('Markdown')

st.success('Success')
df = pd.read_csv("data/Insurance_multiple_regression.csv")
st.write(df)

files_bytes = st.file_uploader("Upload a csv file", type="csv")
st.warning('Warning')
st.error("Error")

