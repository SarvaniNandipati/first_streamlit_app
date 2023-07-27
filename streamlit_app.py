# Adding all import statements on top
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
 
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)

# Display fruit name while selecting instead of number
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include # choosing a few fruits to set as an example
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# Filtering selected fruits and displaying it
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# Giving user an option to select which fruit info he wants and showcasing its nutrition values by hitting a api call

# creating a function for repeatable code block
def get_fruityvice_data(this_fruit_choice):
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 return fruityvice_normalized

#Let's Call the Fruityvice API from Our Streamlit App!
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
   back_from_function = get_fruityvice_data(fruit_choice)
   streamlit.dataframe(back_from_function)

except URLError as e:
 streamlit.error()

# don't run beneath this
#streamlit.stop()

# Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call

## changing the query to show Some Data, Instead

streamlit.header("The fruit load list contains")
# snowflake related functions
def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
  my_cur.execute("SELECT * from fruit_load_list")
  return my_cur.fetchall()

#adding a button to load the fruit:
if streamlit.button('Get Fruit Load List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_load_list()
 streamlit.dataframe(my_data_rows)

#allowing user to add fruit he likes

def insert_row_snowflake(new_fruit):
 with my_cnx.cursor() as my_cur:
 my_cur.execute("insert into fruit_load_list values ('from streamlit')")
 return 'Thanks for adding'+ new_fruit
 
add_my_fruit = streamlit.text_input('What fruit would you like to add?')

if streamlit.button('Add fruit to the List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 back_from_function = insert_row_snowflake(add_my_fruit)
 streamlit.text(back_from_function)
