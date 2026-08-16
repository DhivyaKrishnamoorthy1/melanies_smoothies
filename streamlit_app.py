import streamlit as st
from snowflake.snowpark.functions import col
import os
import requests  
import pandas as pd
#session =get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()

st.title(f" :cup_with_straw: Customise Your Smoothie! :cup_with_straw: ")

st.write(
  """Choose the fruits you want in your custom smoothie
  """
)

name_on_order=st.text_input('Name on Smoothies: ')
st.write('The name on the smoothie will be :',name_on_order)

#
#option=st.selectbox(
#        ('How would you like to be contacted?'),
#        ('Email','Mobile Phone','Home Phone'))
#st.write ('Your selected: ',option)


#option1=st.selectbox(
#        ('What is your favourite fruit?'),
#        ('Banana','Strawberries','Peaches'))
#st.write ('Your favourite fruit is: ',option1)
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# Convert to a Snowpark datafram from pandas dataframe so we can use LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list =st.multiselect('Choose up to 5 ingredients :',my_dataframe)
if ingredients_list:
    st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen +' Nutrition Information ')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")  
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width =True)
    #st.write(ingredients_string)    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert =st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
      
# New section to display Smoothiefroot nutrition information

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width =True)
