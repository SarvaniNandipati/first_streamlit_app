import streamlit
streamlit.title('My Parents New Healthy Diner')
 
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
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
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit"+ fruit_choice)

# Remove hashtag from this code incase you want to see watermelon data in json format and '#' below code
# streamlit.text(fruityvice_response.json());

# Show casing watermelon data in Dataframe format
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

# Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
