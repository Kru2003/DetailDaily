import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
from textblob import TextBlob
nltk.download('punkt')

def fetch_news_search_topic(topic):
    site = 'https://news.google.com/rss/search?q={}'.format(topic)
    op = urlopen(site)
    rd = op.read()
    op.close()
    sp_page = soup(rd, 'xml')
    news_list = sp_page.find_all('item')
    return news_list

def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)
    rd = op.read()
    op.close()
    sp_page = soup(rd, 'xml')
    news_list = sp_page.find_all('item')
    return news_list

def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site)
    rd = op.read()
    op.close()
    sp_page = soup(rd, 'xml')
    news_list = sp_page.find_all('item')
    return news_list

def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        st.image(image, use_column_width=True)
    except Exception as e:
        st.error("Error loading image: " + str(e))
        image = Image.open('noimage.jpg')
        st.image(image, use_column_width=True)

def display_news(list_of_articles, news_quantity):
    c = 0
    for article in list_of_articles:
        c += 1
        st.write('**({}) {}**'.format(c, article.title.text))
        news_data = Article(article.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            st.error("Error processing article: " + str(e))
            continue

        fetch_news_poster(news_data.top_image)
        with st.expander(article.title.text):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}"</h6>'''.format(news_data.summary),
                unsafe_allow_html=True)
            st.markdown("[Read more at {}...]({})".format(article.source.text, article.link.text))
        st.success("Published Date: " + article.pubDate.text)
        
        # Sentiment Analysis
        analysis = TextBlob(news_data.text)
        sentiment = "positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"
        st.success("Sentiment: {}".format(sentiment))
        
        if c >= news_quantity:
            break

# Main Streamlit UI
def main():
    st.title("DETAIL DAILY")

    if "is_logged_in" not in st.session_state or not st.session_state.is_logged_in:
        st.error("You need to login to access this page.")
        return
    
    option = st.selectbox(
        'Select a category:',
        ('Top News', 'Category', 'Search')
    )

    if option == 'Top News':
        news_list = fetch_top_news()
        display_news(news_list, 5)
        pass

    elif option == 'Category':
        categories = ['WORLD','POLITICS', 'TECHNOLOGY', 'SPORTS', 'ENTERTAINMENT','BUSINESS','SCIENCE','HEALTH']
        topic = st.selectbox('Select a category:', categories)
        if topic:
            news_list = fetch_category_news(topic)
            display_news(news_list, 5)
        else:
            st.warning("Please select a category.")
        pass
            
    elif option == 'Search':
        topic = st.text_input('Enter a topic to search:')
        if topic:
            news_list = fetch_news_search_topic(topic)
            display_news(news_list, 5)
        else:
            st.warning("Please enter a topic to search.")
        pass

if __name__ == "__main__":
    main()