import ast
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Churned - Demo Data",
    layout="wide"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.image('logo-churned.png', width=200)
st.sidebar.title("Demo data")

datafiles = [
    '',
    'Categories',
    'Marketing',
    'Crm',
    'Data Viewer',
    'Modify Data'
]

file = st.sidebar.selectbox("Select Demo Data", datafiles)

if file == 'Categories':
    df = pd.read_csv('amazon_co-ecommerce_sample.csv')

    columnnames = [
        'uniq_id',
        'number_of_reviews',
        'number_of_answered_questions',
        'average_review_rating',
        'customers_who_bought_this_item_also_bought',
        'items_customers_buy_after_viewing_this_item',
        'customer_questions_and_answers',
        'customer_reviews',
        'sellers',
        'number_available_in_stock'
    ]

    df = df.drop(columnnames, 1)

    cats = st.text_area("Add categories with a ; seperator")
    cats = cats.split(";")
    cats = list(filter(None, cats))

    st.header("Categories")
    st.write(cats)

    seizoenen = [
        'Zomer',
        'Lente',
        'Winter',
        'Herfst'
    ]

    df['seizoen'] = np.random.choice(seizoenen, len(df))

    df['jaar'] = np.random.randint(2014, 2022, len(df))
    df['ontvangen'] = np.random.randint(304, 2195, len(df))
    df['beschikbare_voorraad'] = np.random.randint(182, 1471, len(df))
    df['aantal_verkocht'] = np.random.randint(4, 1792, len(df))
    df['aantal_retour'] = np.random.randint(4, 92, len(df))
    df['retour_percent'] = df['aantal_retour'] / df['aantal_verkocht']
    df['in_bestelling'] = np.random.randint(4, 92, len(df))
    df['dvk'] = np.random.randint(12, 114, len(df))
    df['price'] = np.random.randint(8, 180, len(df))

    min_date = pd.to_datetime('2019-01-01')
    max_date = pd.to_datetime('2022-02-18')
    d = (max_date - min_date).days + 1

    df['laatst_ontvangen'] = min_date + \
        pd.to_timedelta(pd.np.random.randint(d, size=len(df)), unit='d')

    df['Productcategorie'] = np.random.choice(cats, len(df))

    df['Productcode'] = df.index

    st.header("DataFrames")

    df = df.sample(128)
    st.write("DF1")
    st.dataframe(df.sample(8))

    df2 = pd.read_csv('data.csv')
    df2['Saletype'] = np.random.choice(cats, len(df2))

    st.write("DF2")
    st.dataframe(df2.sample(8))

    if st.button("Make csv"):
        df.to_csv('test.csv')
        df2.to_csv('streamlit2.csv')

if file == 'Crm':
    st.header("Select and Preview Data")
    df = pd.read_csv('CRM-compleet.csv')
    df = df.drop_duplicates(subset='Company', keep="last")

    available_columns = [
        'WARNING FLAG',
        'CHURN RISK',
        'CHURN DRIVER - B2B SaaS',
        'CHURN DRIVER - B2C Subs',
        'CHURN DRIVER - B2C Ecom',
        'NEXT BEST ACTION - B2B SaaS',
        'NEXT BEST ACTION - B2C Subs',
        'NEXT BEST ACTION - B2C Ecom',
        'NEXT BEST CHANNEL - B2B SaaS',
        'NEXT BEST CHANNEL - B2C Subs',
        'NEXT BEST CHANNEL - B2C Ecom',
        'MRR',
        'First Name',
        'Last Name',
        'Title',
        'Account Name',
        'Phone',
        'Email',
        'CLV',
        'Company',
        'Customer Success Manager'
    ]

    col1, col2 = st.columns([1, 3])

    with col1:
        cols = st.multiselect('Select columns', available_columns)

    with col2:
        st.write("")
        st.write("")
        st.dataframe(df[cols].head(10))
        df = df[cols]

    coll1, coll2, coll3 = st.columns([1,1,1])

    with coll1:
        if st.button("To Google Query"):
            # df.to_csv('crm-file.csv')
            st.warning("Unavailable")
    
    with coll2:
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
        
        csv = convert_df(df)
        
        if (st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='CRM-contacts-data.csv',
        mime='text/csv',
        )):
            df.to_csv('crm-file.csv')
            st.success("CSV data downloaded")
        
    with coll3:
        with open("cheatsheet.pdf", "rb") as file:
            
            if (st.download_button(
            label="Download Cheatsheet",
            data=file,
            file_name="Cheatsheet.pdf",
            mime="application/octet-stream"
        )): st.success("Cheatsheet downloaded")     

if file == 'Data Viewer':
    st.header("Data Viewer")

    choise = st.selectbox("Select File", ['', 'Categories', 'Crm'])

    try:

        if choise == 'Crm':
            temp = pd.read_csv('crm-file.csv', index_col=[0])
            st.subheader("Dataframe information")
            st.write("Size: " + str(temp.shape[0]) + " rows")
            st.dataframe(temp)
        if choise == 'Categories':
            temp = pd.read_csv('test.csv', index_col=[0])
            st.subheader("Dataframe information")
            st.write("Size: " + str(temp.shape[0]) + " rows")
            st.dataframe(temp)
            temp = pd.read_csv('streamlit2.csv', index_col=[0])
            st.subheader("Dataframe information")
            st.write("Size: " + str(temp.shape[0]) + " rows")
            st.dataframe(temp)
    except Exception as e:
        st.error(e)

if file == 'Modify Data':
    st.header("Modify Data")

    choise = st.selectbox("Select datafile", ['', 'Crm'])

    if choise == 'Crm':
        df = pd.read_csv('CRM-compleet.csv', index_col=[0])
        change_col = st.selectbox("Select column to change", df.columns)

        uniquevals = df[change_col].unique()
        uniquevals = uniquevals.tolist()

        st.write(uniquevals)

        jsontext = st.text_area("Change values", uniquevals)
        new_values = ast.literal_eval(jsontext)

        if st.button("Change values"):
            st.write(new_values)
            df[change_col] = np.random.choice(new_values, len(df))
            df.to_csv('CRM-compleet.csv')
            st.write("Changed " + change_col + " with new values!")
