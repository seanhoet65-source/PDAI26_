import streamlit as st
import requests


st.title("News Search with GDELT")

st.write("This demo shows how to search for news articles using the **GDELT API**. ")


query = st.text_input("Enter your search query")

API_NEWS = f'https://api.gdeltproject.org/api/v2/doc/doc?query=%22{query}%22%20sourcelang:eng&startdatetime=20190920133005&enddatetime=20190920143005&format=json'

if st.button("Search"):
    data = requests.get(API_NEWS, headers={'User-Agent': 'request'})

    results = data.json()
    if 'articles' in results:
        for result in results['articles']:

            st.subheader(result['title'])

            st.link_button("Read more", url=result['url'])
            st.write("---")
