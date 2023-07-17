import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

###### Title and Markdown
st.title("My first EDA app")
st.markdown("""
            This app perform EDA
             
            - **Python libraries:** streamlit, pandas, numpy, ...
             
            - **Need to contact:** [mon portfolio](https://github.com/paulmaitre/)""")


###### File upload
# Check if file has been uploaded, if yes read the file
file_bytes = st.file_uploader("Upload a file:", type='csv')

if file_bytes is not None:
    print(type(file_bytes))
    data = pd.read_csv(file_bytes)
    obj=[]
    int_float=[]
    for c in data.columns:
        typ = data[c].dtypes
        if typ =='object':
            obj.append(c)
        else:
            int_float.append(c)
    
    st.write(data.head())
    # Randomly select at least one entry as null in each feature
    for column in data.columns:
        # Get a random index for null assignment
        random_index = np.random.choice(data.index)
        # Assign null value to the randomly selected entry
        data.loc[random_index, column] = np.nan
        
        
###### Remove null values : button to remove values and replace with mean & median
# Adding submit button sidebar
    with st.form(key='my_form'):
        with st.sidebar:
            st.sidebar.header("To remove null values press button")
            submit_button = st.form_submit_button(label='Remove Null')
            
# If we click remove null button, null values will be replaced with mean and mode
    if submit_button:
        # st.write("Before cleaning:")
        # st.write(data.isnull().sum())
        for c in data.columns:
            typ = data[c].dtypes
            if typ =='object':
                data[c].fillna(data[c].mode()[0], inplace=True)
            else:
                data[c].fillna(data[c].mean(), inplace=True)
        # st.write("After cleaning:")
        # st.write(data.isnull().sum())

##### Null values : if 0 message else, create & show a graph
    # Finding number of null values in each colum
    lis = []
    for c in data.columns:
        dd = sum(pd.isnull(data[c]))
        lis.append(dd)

    # if no if null values are zero it will display some text, else it will display bar plot by each col
    if max(lis)==0:
        st.write("No null values detected.")
    else:
        st.write("Bar plot to know no.of null values in each col")
        st.write("Total no.of null values= "+str(sum(lis)))
        fig2 = px.bar(x=data.columns, 
                      y=lis, 
                      labels={'x':"Column Names", 'y':"No. of Null values"})
        st.plotly_chart(fig2)
        
    ##### Box or bar chart - Frequency for each column
    # Frequency plot 
    st.sidebar.header("Select variable for frequency plot")
    selected_pos = st.sidebar.selectbox('Object variables', obj)
    st.write("Bar plot to know frequency of each category")
    frequency_data = data[selected_pos].value_counts()
    #st.write(frequency_data.index)
    fig = px.bar(frequency_data, 
                x=frequency_data.index, 
                y='count', 
                labels={'x':selected_pos, 'y':'count'})
    st.plotly_chart(fig)

    ##### Histogram - Distribution for each column
    # Histogram
    st.sidebar.header("Select variable for histogram")
    selected_pos_1 = st.sidebar.selectbox('Int of Float variables', int_float)
    st.write("Bar plot to know count of values based on range")
    counts, bins = np.histogram(data[selected_pos_1],
                                bins=range(int(min(data[selected_pos_1])), 
                                           int(max(data[selected_pos_1])), 
                                           int(max(data[selected_pos_1])/10)))
    bins = 0.5*(bins[:-1]+bins[1:])
    fig1 = px.bar(x=bins,
                  y=counts,
                  labels={'x':selected_pos_1, 'y':'count'})
    st.plotly_chart(fig1)

    ##### Correlation chart
    st.sidebar.header("Select variables for correlation")
    selected_pos_2 = st.sidebar.multiselect('Int or Float variables', int_float)
    st.write("Scatter plot for correlation")
    if len(selected_pos_2)==2:
        fig3 = px.scatter(data, x=selected_pos_2[0], y=selected_pos_2[1])
        st.plotly_chart(fig3)
    else: 
        st.write("Select two variables")