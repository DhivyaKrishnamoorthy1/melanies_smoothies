import streamlit as st
from snowflake.snowpark.functions import col
import os
#session =get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()

st.title(f" My Parents New Healthy Diner ")

st.write(
  """Breakfast Menu
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
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list =st.multiselect('Choose up to 5 ingredients :',my_dataframe)
if ingredients_list:
    st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert =st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
