import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import base64
# Create the Streamlit app
st.set_page_config(layout="wide")
st.title('Data Visualization')

# Add a file uploader in the sidebar
with st.sidebar:
    # Load and encode the logo image
    try:
        with open("logo.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        img = f"<img src='data:image/png;base64,{encoded_string}' alt='App Logo' style='width:200px;height:auto;'>"
        st.markdown(img, unsafe_allow_html=True)
    except FileNotFoundError:
        print("Logo image not found. Please ensure the path is correct.")
    uploaded_file = st.file_uploader("Choose a data file (CSV or XLSX)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Load the data based on file extension
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Data preview in the main app area
    st.subheader('Data Preview')
    with st.expander ('Data Preview'):
     st.dataframe(df)  # Display the first 10 rows

    # Get the unique Short Label Questions
    short_label_questions = df['Short Label Question'].unique()

    # Select the Short Label Question to plot (optional)
    if len(short_label_questions) > 1:  # Only show dropdown if multiple options
        selected_question = st.selectbox('Select a Short Label Question', short_label_questions)
    else:
        selected_question = short_label_questions[0]  # Use the only available question

    # Visualization controls in a collapsible section
    visualization_controls = st.expander('Visualization Controls (Optional)')  # Collapsible section
    with visualization_controls:
        visualization_type = st.selectbox('Select the visualization type', ['Bar Chart', 'Line Chart', 'Pie Chart'])

    # Create the plot based on the selected options (optional)
    # Create the plot based on the selected options (optional)
    if visualization_type is not None:


        if visualization_type == 'Bar Chart':
            question_data = df[df['Short Label Question'] == selected_question]
            fig = px.bar(question_data, x='Attributes', y='Audience %', title=selected_question)
            fig.update_layout(xaxis_title='Attributes', yaxis_title='Audience %')
            fig.update_xaxes(tickangle=90)  # Rotate x-axis labels for readability

        elif visualization_type == 'Line Chart':
            question_data = df[df['Short Label Question'] == selected_question]
            fig = px.line(question_data, x='Attributes', y='Audience %', title=selected_question)
            fig.update_layout(xaxis_title='Attributes', yaxis_title='Audience %')
            fig.update_xaxes(tickangle=90)  # Rotate x-axis labels for readability

        elif visualization_type == 'Pie Chart':
            question_data = df[df['Short Label Question'] == selected_question]
            fig = px.pie(question_data, values='Audience %', names='Attributes', title=selected_question)

        # Display the plot in Streamlit
        st.plotly_chart(fig)
