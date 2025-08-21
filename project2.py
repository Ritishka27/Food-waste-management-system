import streamlit as st
import pandas as pd
import numpy as np
import pymysql

#st.title("Welcome to  food waste management system")
#st.header("Welcome to  food waste management system")

r=st.sidebar.radio('Navigation',['Home','View available food','Database','Update','SQL Queries','Contact'])

if r == 'Home' :
    st.title("Welcome to  food waste management system")
    st.image("C:/Users/ritis/Downloads/waste diag.jpg")

    st.text("Food wastage is a significant issue, with many households and ")
    st.text("restaurants discarding surplus food while numerous people struggle")
    st.text("with food insecurity. This project aims to develop a Local Food ")
    st.text("Wastage Management System,where:")
    st.write("Restaurants and individuals can list surplus food.")
    st.write("NGOs or individuals in need can claim the food.")
    st.write("SQL stores available food details and locations.")
    st.write("A Streamlit app enables interaction, filtering, CRUD operation and visualization.")

if r == 'View available food':
    st.subheader("You can view the food listing records here")
    df1= pd.read_csv("C:/Users/ritis/Downloads/food_listings_data.csv")
    st.write(df1)

if r=='Database':
    st.subheader("You can view the providers records here")
    df2= pd.read_csv("C:/Users/ritis/Downloads/providers_data.csv")
    st.write(df2)
    st.subheader("You can view the receivers records here")
    df3= pd.read_csv("C:/Users/ritis/Downloads/receivers_data.csv")
    st.write(df3)
    st.subheader("You can view the claims records here")
    df2= pd.read_csv("C:/Users/ritis/Downloads/claims_data.csv")
    st.write(df2)

if r== 'SQL Queries':
    st.subheader("You can View SQL queries here")
    conn = pymysql.connect(
    host="localhost",        # or your DB host/IP
    user="root",             # your MySQL username
    password="1234",# your MySQL password
    database="waste",# your DB name
    port=3306,
    ssl_disabled=True                
)
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()
    #print("✅ Connected to MySQL:", cursor.fetchone()[0])
    if version:
        st.success(f"✅ Connected to MySQL: {version[0]}")
    else:
        st.warning("⚠️ Connected, but could not fetch MySQL version.")

    q1="SELECT city, count(prov_id) FROM provider GROUP BY city ORDER BY city;"
    cursor.execute(q1)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d1 = pd.DataFrame(rows, columns=cols)

    st.write("Query1: How many food providers are there in each city")
    st.dataframe(d1)

    q1_2="SELECT city, count(Receiver_id) FROM receivers_data GROUP BY city ORDER BY city;"
    cursor.execute(q1_2)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d1_2 = pd.DataFrame(rows, columns=cols)

    st.write("Query1: How many food receivers are there in each city")
    st.dataframe(d1_2)

    q2="SELECT Provider_Type, sum(Quantity) FROM food GROUP BY Provider_Type ORDER BY sum(Quantity) DESC LIMIT 1;"
    cursor.execute(q2)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d2 = pd.DataFrame(rows, columns=cols)

    st.write("Query2: Which type of food provider (restaurant, grocery store, etc.) contributes the most food")
    st.dataframe(d2)

    #q3="SELECT city, contact FROM PROVIDER GROUP BY City ;"
    #cursor.execute(q3)
    #rows = cursor.fetchall()

    #cols = [desc[0] for desc in cursor.description]
    #d3 = pd.DataFrame(rows, columns=cols)

    #st.write("Query3: What is the contact information of food providers in a specific city")
    #st.dataframe(d3)

    q4="SELECT RECEIVER_ID, COUNT(CLAIM_ID) FROM CLAIM GROUP BY RECEIVER_ID ORDER BY COUNT(CLAIM_ID) DESC LIMIT 5 ;"
    cursor.execute(q4)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d4 = pd.DataFrame(rows, columns=cols)

    st.write("Query4: Which receivers have claimed the most food?")
    st.dataframe(d4)

    q5="SELECT SUM(QUANTITY) FROM FOOD;"
    cursor.execute(q5)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d5 = pd.DataFrame(rows, columns=cols)

    st.write("Query5: What is the total quantity of food available from all providers")
    st.dataframe(d5)

    q6="SELECT LOCATION, SUM(QUANTITY) FROM food GROUP BY LOCATION ORDER BY sum(Quantity) DESC LIMIT 1;"
    cursor.execute(q6)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d6 = pd.DataFrame(rows, columns=cols)

    st.write("Query6: Which city has the highest number of food listings")
    st.dataframe(d6)

    q7="SELECT FOOD_TYPE, SUM(QUANTITY) FROM FOOD GROUP BY FOOD_TYPE ORDER BY sum(Quantity) DESC;"
    cursor.execute(q7)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d7 = pd.DataFrame(rows, columns=cols)

    st.write("Query7: What are the most commonly available food types")
    st.dataframe(d7)

    q10="SELECT status,COUNT(*) AS total, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claim), 2) AS percentage FROM claim GROUP BY status;"
    cursor.execute(q10)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d10 = pd.DataFrame(rows, columns=cols)

    st.write("Query10: What percentage of food claims are completed vs. pending vs. canceled")
    st.dataframe(d10)

    q13="select provider_id, sum(quantity) from food group by provider_id order by sum(quantity) DESC;"
    cursor.execute(q13)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d13 = pd.DataFrame(rows, columns=cols)

    st.write("Query13: What is the total quantity of food donated by each provider")
    st.dataframe(d13)

    
if r=='Update':
    st.subheader("You can update the receivers records here")
    form = st.form(key='Update recievers database')
    Receiver_ID= form.text_input("Unique id")
    name = form.text_input("Name")
    type=form.radio("type",("Charity","Individual","NGO","Shelter"))
    city=form.text_input("City")
    contact=form.text_input("contact number")
    submit_button = form.form_submit_button(label='Submit Records')
    if submit_button:
        form_data= {'Receiver_ID':Receiver_ID,'Name':name,'Type':type,'City':city,'Contact':contact}
        df4 = pd.DataFrame([form_data])
        st.success("Registration Successful!")
        st.write("Here are your details:")
        st.table(df4)
        insert_query = """
        INSERT INTO receivers_data (Receiver_ID,name,type,city,contact)
        VALUES (%s, %s, %s, %s, %s)"""

        data = (Receiver_ID,name,type,city,contact)
        conn = pymysql.connect(
            host="localhost",        # or your DB host/IP
            user="root",             # your MySQL username
            password="1234",# your MySQL password
            database="waste",# your DB name
            port=3306,
            ssl_disabled=True                )
        cursor = conn.cursor()
        cursor.execute(insert_query,data)
        st.success('Data inserted to sql')

if r=='Contact':
    conn = pymysql.connect(
        host="localhost",        # or your DB host/IP
        user="root",             # your MySQL username
        password="1234",# your MySQL password
        database="waste",# your DB name
        port=3306,
        ssl_disabled=True                )
    st.subheader("You can view the contacts of the providers here")
    prov=st.slider("Select provider_id of the provider",1,1000)
    cursor = conn.cursor()
    p= ("select prov_id,name,address,city,contact from provider where prov_id= %d ;" % prov )
    cursor.execute(p)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d15 = pd.DataFrame(rows, columns=cols)

    st.dataframe(d15)

    st.subheader("You can view the contacts of the receivers here")
    rec=st.slider("Select receiver_id of the receiver on the slider below",1,1000)
    cursor = conn.cursor()
    p1= ("select * from receivers_data where receiver_id= %d ;" % rec )
    cursor.execute(p1)
    rows = cursor.fetchall()

    cols = [desc[0] for desc in cursor.description]
    d16 = pd.DataFrame(rows, columns=cols)

    st.dataframe(d16)
