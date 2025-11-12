# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

# Write directly to the app
st.title(f":cup_with_straw: Custom Smoothie Order Form :cup_with_straw:")
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be ", name_on_order)
st.write(
  """Choose the fruit you want in Custom smoothie.
  """
)
cnx=st.connection("snowflake")
session = cnx.session();
mydataframe=session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col("FRUIT_NAME"),col("SEARCH_ON"))
pd_df=mydataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
#st.dataframe(data=mydataframe,use_container_width=True)
#st.stop()
ingredients_list=st.multiselect('Choose Upto 5 Fruit:',mydataframe,max_selections=5)
if ingredients_list:
    st.write(ingredients_list);
    st.text(ingredients_list);
    ingredients_string =''

    for fruits_chosen in ingredients_list:
        ingredients_string+=fruits_chosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruits_chosen,' is ', search_on, '.')
        st.subheader(fruits_chosen +' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_dt= st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    time_to_insert=st.button("Confirm Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
