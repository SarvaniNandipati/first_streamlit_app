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

#Let's Call the Fruityvice API from Our Streamlit App!
streamlit.header("Fruityvice Fruit Advice!")

# Giving user an option to select which fruit info he wants and showcasing its nutrition values by hitting a api call
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   streamlit.dataframe(fruityvice_normalized)

except URLError as e:
 streamlit.error()

# don't run beneath this
streamlit.stop()

# Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call

#Query about Our Snowflake Trial Account Metadata 
## changing the query to show Some Data, Instead
#Let's Change the Streamlit Components to Make Things Look a Little Nicer and Get All the Rows, Not Just One
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_rows)

#allowing user to add fruit he likes
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding', add_my_fruit)

# this will not work correctly but proceeding with it now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
