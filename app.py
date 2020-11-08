import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from config import DBConfig
import datetime


@st.cache(allow_output_mutation=True, show_spinner=False)
def get_con():
    return create_engine('mysql+pymysql://{}:{}@{}/twitter_sqlalc'.format(DBConfig.USER, DBConfig.PWORD, DBConfig.HOST),
                         convert_unicode=True)


@st.cache(allow_output_mutation=True, show_spinner=False, ttl=5*60)
def get_data():
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    df = pd.read_sql_table('tweets', get_con())
    df = df.rename(columns={'body': 'Tweet', 'tweet_date': 'Timestamp',
                            'followers': 'Followers', 'sentiment': 'Sentiment',
                            'keyword': 'Subject'})
    return df, timestamp


@st.cache(show_spinner=False)
def filter_by_date(df, start_date, end_date):
    df_filtered = df.loc[(df.Timestamp.dt.date >= start_date) & (df.Timestamp.dt.date <= end_date)]
    return df_filtered


@st.cache(show_spinner=False)
def filter_by_subject(df, subjects):
    return df[df.Subject.isin(subjects)]


@st.cache(show_spinner=False)
def count_plot_data(df, freq):
    plot_df = df.set_index('Timestamp').groupby('Subject').resample(freq).id.count().unstack(level=0, fill_value=0)
    plot_df.index.rename('Date', inplace=True)
    plot_df = plot_df.rename_axis(None, axis='columns')
    return plot_df


@st.cache(show_spinner=False)
def sentiment_plot_data(df, freq):
    plot_df = df.set_index('Timestamp').groupby('Subject').resample(freq).Sentiment.mean().unstack(level=0, fill_value=0)
    plot_df.index.rename('Date', inplace=True)
    plot_df = plot_df.rename_axis(None, axis='columns')
    return plot_df


st.set_page_config(layout="wide", page_title='UK Leader Tweets')

data, timestamp = get_data()

st.header('Boris Johnson vs Keir Starmer')
st.write('Daily tweet count: {}'.format(len(filter_by_date(data, datetime.date.today(), datetime.date.today()))))
st.write('Data last loaded {}'.format(timestamp))

col1, col2 = st.beta_columns(2)

date_options = data.Timestamp.dt.date.unique()
start_date_option = st.sidebar.selectbox('Select Start Date', date_options, index=0)
end_date_option = st.sidebar.selectbox('Select End Date', date_options, index=len(date_options)-1)

keywords = data.Subject.unique()
keyword_options = st.sidebar.multiselect(label='Subjects to Include:', options=keywords.tolist(), default=keywords.tolist())

data_subjects = data[data.Subject.isin(keyword_options)]
data_daily = filter_by_date(data_subjects, start_date_option, end_date_option)

top_daily_tweets = data_daily.sort_values(['Followers'], ascending=False).head(10)

col1.subheader('Influential Tweets')
col1.dataframe(top_daily_tweets[['Tweet', 'Timestamp', 'Followers', 'Subject']].reset_index(drop=True), 1000, 400)

col2.subheader('Recent Tweets')
col2.dataframe(data_daily[['Tweet', 'Timestamp', 'Followers', 'Subject']].sort_values(['Timestamp'], ascending=False).
               reset_index(drop=True).head(10))

plot_freq_options = {
    'Hourly': 'H',
    'Daily': 'D'
}
plot_freq_box = st.sidebar.selectbox(label='Plot Frequency:', options=list(plot_freq_options.keys()), index=0)
plot_freq = plot_freq_options[plot_freq_box]

col1.subheader('Tweet Volumes')
plotdata = count_plot_data(data_daily, plot_freq)
col1.line_chart(plotdata)

col2.subheader('Sentiment')
plotdata2 = sentiment_plot_data(data_daily, plot_freq)
col2.line_chart(plotdata2)


locations = pd.DataFrame(pd.eval(data_daily[data_daily['location'].notnull()].location), columns=['lon', 'lat'])
st.map(locations)



