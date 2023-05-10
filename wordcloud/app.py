import streamlit as st
from maple_inven_crawl import inven
from maple_homepage_crawl import maple
from preprocess import preprocess
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title('MAPLE WORD CLOUD')
st.info('it shows wordcloud of maple inven site and maple homepage')

# button cache setting
if 'start' not in st.session_state:
    st.session_state.start = False
if 'inven' not in st.session_state:
    st.session_state.inven = False
if 'maple' not in st.session_state:
    st.session_state.maple = False

choice_site = st.selectbox('choice what you want!', ('inven', 'maple_homepage'))
if st.button('start') or st.session_state.start:
    st.session_state.start = True

    if choice_site == 'inven':
        choice_recommend = st.selectbox('choice recommend!', ('all', 'chu', 'chuchu'))
        choice_dates = st.selectbox('choice dates!', ('day', '7day'))

        st.info('all : all post title \n \n \n chu : post that gain over 10 recommends \n \n \n chuchu : post that gain over 30 recommends')
        st.info('day : posts collected in one day \n \n \n 7day : posts collected in seven day')

        if st.button('inven') or st.session_state.inven:
            with st.spinner('Wait for it...'):

                # make word cloud 
                crawl_class = inven()
                results = crawl_class.inven_title(choice_recommend, choice_dates)
                final_dict = preprocess(results)
                font_path = 'SeoulNamsanvert.ttf'
                wc = WordCloud(font_path=font_path, width=1500, height=1200, background_color='black', colormap='Paired_r', prefer_horizontal=True).fit_words(final_dict)
                plt.imshow(wc)
                plt.axis('off')
                plt.savefig('result.png')
                st.image('result.png')
            st.session_state.inven = True
            

    elif choice_site == 'maple_homepage':
        choice_dates = st.selectbox('choice dates!', ('day', '7day'))

        st.info('day : posts collected in one day \n \n \n 7day : posts collected in seven day')

        if st.button('maple') or st.session_state.maple:

            with st.spinner('Wait for it...'):

                # make word cloud 
                crawl_class = maple()
                results = crawl_class.maple_title(choice_dates)
                final_dict = preprocess(results)
                font_path = 'SeoulNamsanvert.ttf'
                wc = WordCloud(font_path=font_path, width=1500, height=1200, background_color='black', colormap='Paired_r', prefer_horizontal=True).fit_words(final_dict)
                plt.imshow(wc)
                plt.axis('off')
                plt.savefig('result.png')
                st.image('result.png')
            st.session_state.maple = True