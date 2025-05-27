# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order=st.text_input('Name on Smoothie:')
st.write('Name on your smoothie will be :',name_on_order)

#option= st.selectbox('How would you like to be contacted?',('Email','Home_phone','Mobile_phone'));

#st.write('You selected:',option)

#option1=st.selectbox('What is your favourite fruit',('Strawberries','Banana','Peaches'))
#st.write('You have selected the fruit:',option1)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
ingredients_list=st.multiselect('choose fruits',my_dataframe,max_selections=3)

if ingredients_list:
    ##st.write(ingredients_list)
    ##st.text(ingredients_list)
    
    ingredients_string=''
    for fruits_chosen in ingredients_list:
        ingredients_string +=fruits_chosen +' '
        st.subheader(fruits_chosen+'Nutrition_information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruits_chosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json())
        
    st.write(ingredients_string)
    my_insert_stmt="""insert into smoothies.public.orders(INGREDIENTS,NAME_ON_ORDER) values('""" +ingredients_string+"""','""" +name_on_order+"""')"""
    st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'""+name_on_order+""'!', icon="✅")



