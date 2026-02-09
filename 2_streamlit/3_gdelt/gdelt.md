# Introduction to Streamlit

In this activity, we will create a simple web application using Streamlit. Streamlit is a python library that allows you to create interactive web applications with data and AI with a small amount of code.

We will develop a web app that allows users to search for news
articles by keyword, and optionally view the sentiment of the article titles.

## Purpose of the notes
These notes are intented to be a summary in order to reproduce the steps after class and recap the concepts, but it does not replace the lecture.

## Preliminary understanding

We will use GDELT API to fetch news articles based on a search query.

The Global Database of Events, Language, and Tone (GDELT) is a project that
monitors and analyzes news media from around the world. It provides a free API
to access news articles, events, and other data.

An example query could be (try this in your browser):

https://api.gdeltproject.org/api/v2/doc/doc?query=Microsoft%20sourcelang:eng&startdatetime=20190920133005&enddatetime=20190920143005&format=html

If you look at the query parameters, you can see that it includes:
- `query`: The search term (e.g., "Microsoft")
- `sourcelang`: The language of the source (e.g., "eng" for English, "spa" for
    Spanish)
- `startdatetime`: The start date and time for the search (in YYYYMMDDHHMMSS
    format)
- `enddatetime`: The end date and time for the search (in YYYYMMDDHHMMSS
    format)
- `format`: The format of the response (e.g., "json" or "html")

We will also use a sentiment analysis API  that has the following endpoint
(also try this in your browser):

https://zkx093ybh8.execute-api.us-east-1.amazonaws.com/detect_sentiment?text=This company performed really bad on the market&lang=en

(The sentiment analysis API is 
a custom API set up for this activity, that connects to a 
pre-trained sentiment analysis model in the AWS cloud)

## Step 1

Open a new folder in Visual Studio Code and create a new file called `app1.py`. Copy the following code into the file:

```python

import streamlit as st
import requests


st.title("News Search with GDELT")

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

```
The lecture anticipates a discussion 
of the different components of the code. 

In a nutshell, the value that the user enters in the text input field is stored in the variable `query`. Then the `API_NEWS` variable is constructed containing the GDELT API endpoint with the search query. When the user clicks the "Search" button, a request is sent to the GDELT API, and the results are displayed in the Streamlit app through the `st.subheader` command. Also, we use a `st.link_button` to create a clickable link that opens the article in a new tab.

You can also copy paste the code into a generative AI tool like ChatGPT and ask to explain it in blocks. 

Select Terminal > New Terminal in Visual Studio Code, and run the following command to install Streamlit:

```bash
streamlit run app1.py
```

A new browser window should open, displaying the Streamlit app. You can enter a search query and click the "Search" button to fetch news articles from GDELT.

Press `Ctrl+C` in the terminal to stop the Streamlit app when you are done testing it.

## Step 2

Let's add a widget to select the language. 

Add the following code after the line `query = st...`:

```python
lang = st.selectbox("Select language", ["eng", "spa"])
```

This will create a dropdown menu to select the language of the news articles with the options "eng" (English) and "spa" (Spanish).

Next, update the `API_NEWS` line that contains the API code to take  the selected language into account:

```python
API_NEWS = f'https://api.gdeltproject.org/api/v2/doc/doc?query=%22{query}%22%20sourcelang:{lang}&startdatetime=20190920133005&enddatetime=20190920143005&format=json'
```

Save the changes and run the Streamlit app again.

## Step 3

Now let's add a sentiment analysis feature to the app. We will use the sentiment analysis API to analyze the sentiment of the article titles.

Copy-paste this code after the `st.subheader...` line:

```python
            API_sentiment = f"https://zkx093ybh8.execute-api.us-east-1.amazonaws.com/detect_sentiment?text={results['title']}&lang=en"
            sentiment_response = requests.get(API_sentiment)

            if sentiment_response.status_code == 200:
                sentiment_data = sentiment_response.json()
                print(sentiment_data)
                sentiment = sentiment_data['Sentiment']
                if sentiment == "POSITIVE":
                    st.badge(f"{sentiment}", color="blue", icon="✔️")
                elif sentiment == "NEGATIVE":
                    st.badge(f"{sentiment}", color="red", icon="❌")
                else:
                    st.badge(f"{sentiment}", color="gray")
            else:
                sentiment = "UNKNOWN"
```

(Keep the indentation of the code, as it is important for Python).

Save the changes and run the Streamlit app again. 

This code constructs the API endpoint for the sentiment analysis API using the article title and sends a request to it. If the response is successful (status code 200), it retrieves the sentiment from the response and displays it as a badge in the Streamlit app. The badge color and icon change based on whether the sentiment is positive, negative, or neutral.
