import streamlit as st
from PIL import Image
import pickle
import numpy as np
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import altair_ally as aly
import altair as alt

## Set page icon
icon = Image.open("./resources/favicon.ico")

## Set page title and layout
st.set_page_config(
    page_title="Poverty Prediction by NTL - Povtrait",
    page_icon=icon,
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.sidebar.title("About")
st.sidebar.info(
    """
    Web App URL: <https://povtrait.streamlit.app/>

    GitHub Repository: <https://github.com/fitriandriastuti/povtrait>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Abd. Hadi Asfarangga: 
    [GitHub](https://github.com/hadi-asfarangga) | | [LinkedIn](https://www.linkedin.com/in/abdul-hadi-asfarangga-76b698130/)

    Baiq Nurul Haqiqi:
    [GitHub](https://github.com/bnhaqiqi) | [Twitter](https://twitter.com/fitriandriast) | [LinkedIn](https://www.linkedin.com/in/baiq-nurul-haqiqi/)

    Ferdian Fadly:
    [GitHub](https://github.com/ferdi-fadly) | [Twitter](https://twitter.com/ferdianfadly) | [LinkedIn](https://www.linkedin.com/in/ferdian-fadly-81826466/)

    Fitri Andri Astuti:
    [GitHub](https://github.com/fitriandriastuti) | [Twitter](https://twitter.com/fitriandriast) | [YouTube](https://www.youtube.com/channel/UC1CC_1KKL32tTAFsNNBBlag) | [LinkedIn](https://www.linkedin.com/in/fitriandriastuti)

    Muhammad Syahrul: 
    [GitHub](https://github.com/muhammad92syahrul) | [Twitter](https://twitter.com/pegawaiumbi) | [YouTube](https://www.youtube.com/channel/UCON57Bvk-qsED80SI8jlqkw) | [LinkedIn](https://www.linkedin.com/in/muhammad-syahrul-aa8892218/)

    """
)

## Functions to predict the result based on the trained model
df_country = pd.read_excel("data/country models and score.xlsx")

# Poverty Prediction by NTL
def predict_poverty(data, country_option):
    # Load the model
    model_path = df_country.loc[df_country["country name"]==country_option,'model name'].to_list()[0]
    with open('models/'+model_path, 'rb') as f:
        model = pickle.load(f)
    result = model.predict(data)
    return result

# Display team's logo
image = Image.open('resources/logo-povtrait small.png')
st.image(image)

# Set title
st.title('Poverty Potrait with NTL')

# Load the data
df = pd.read_excel("data/NTL and Poverty.xlsx")
df['Year'] = df['Year'].astype(str)

df_quarter = pd.read_excel("data/prediction all countries quarterly.xlsx")

# Create multiple tabs
vis_tab, pred_single_tab, pred_batch_tab  = st.tabs(["Visualisation", "Single Poverty Prediction", "Batch Poverty Prediction"])

###### Tab 1: Visualisation ######
with vis_tab:
    st.subheader("Visualisation")
    col1 = st.columns(2)

    with col1[0]:
        option = st.selectbox("Select Data", ("NTL", "Poverty"))

    st.markdown('#### Poverty and NTL Over the Year')
    st.altair_chart(
            alt.Chart(df).mark_line(color='orange').encode(
                x='Year',
                y=option,
                # y=alt.Y('Value', scale=alt.Scale(domain=[350, 550])),
                tooltip=['Year', alt.Tooltip(option, format=",.2f")],
            ).interactive()
            , use_container_width=True, )

    st.markdown('#### Scatter Plot')
    st.altair_chart(
            alt.Chart(df).mark_circle(size=90,color='steelblue').encode(
                x='NTL',
                y='Poverty',
                tooltip=['Year', 'NTL', 'Poverty']
            ).interactive(),
            use_container_width=True, )

    st.markdown('#### Poverty Quarterly Prediction by Country')

    col_viz = st.columns(3)
    with col_viz[0]:
        country_option = st.multiselect("Select Country",sorted(df_country["country name"].unique()), ['Albania'], key="Country Vis")

    country_codes = []

    for country in country_option:
        country_code = df_country.loc[df_country["country name"] == country, 'country code'].to_list()[0]
        country_codes.append(country_code)

    selected_data = df_quarter[df_quarter["country_code_2"].isin(country_codes)]

    st.altair_chart(
            alt.Chart(selected_data).mark_line(color='MediumAquaMarine').encode(
                x='Year-Quarter',
                y='Poverty',
                color=alt.Color('country_code_2', title='Country Code'),
                # y=alt.Y('Value', scale=alt.Scale(domain=[350, 550])),
                tooltip=['Year-Quarter', alt.Tooltip('Poverty', format=",.2f")],
            ).interactive()
            , use_container_width=True, )

###### Tab 2: Single Prediction ######
with pred_single_tab:
    st.subheader("Predicting Poverty with NTL")
    col2 = st.columns(2)

    # Sliders for the variables
    with col2[0]:
        country_option = st.selectbox("Select Country",sorted(df_country["country name"].unique()))
        ntl = st.slider(
            'NTL',
            0.0, 1.0, 0.5)


    # Create dataframe for the features
    features = {
                'NTL': ntl,
                }
    features_df = pd.DataFrame([features])

    prediction = predict_poverty(features_df, country_option)
    # Display the prediction
    st.markdown('#### Predicted Poverty: ' + str(round(prediction[0], 2)))
    #st.markdown('#### Predicted Poverty: ' + str(30))


###### Tab 3: Batch Prediction ######
with pred_batch_tab:
    #@st.cache
    # Function to create an Excel file
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('A:A', None, format1)
        writer.save()
        processed_data = output.getvalue()
        return processed_data

    # Upload the excel file
    st.markdown('#### Upload the NTL data')

    st.write("Please make sure the uploaded file follows the right template.")
    # Create the template file
    template_file = to_excel(df.iloc[:,-1:])

    # Button to download the template file
    st.download_button(
        label='???? Download template file',
        data=template_file,
        file_name='template_NTL.xlsx',
    )
    # Input file uploader
    uploaded_file = st.file_uploader("Choose an Excel file")
    # Read the input file
    if uploaded_file is not None:
        df_input = pd.read_excel(uploaded_file)
        st.dataframe(df_input)

    col3 = st.columns(3)

    with col3[0]:
        country_option_batch = st.selectbox("Select Country", sorted(df_country["country name"].unique()), key="Country Option Batch")

    # Predict poverty based on the input dataframe
    if st.button('Predict', key="Button Predict Batch"):
        st.markdown('#### Predicted Poverty')
        prediction_batch = predict_poverty(df_input,country_option_batch)

        # Add prediction as a new column
        df_predicted = df_input.assign(Poverty=prediction_batch)

        # Display prediction dataframe
        st.dataframe(df_predicted)

        # Create Excel file to download
        excel_file = to_excel(df_predicted)

        # Button to download the prediction data
        st.download_button(
            label='???? Download data as Excel',
            data=excel_file,
            file_name='predicted Poverty by NTL.xlsx',
        )
