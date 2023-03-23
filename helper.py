from urlextract import URLExtract
extract=URLExtract()
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emojis




def fetch_stats(selected_user,df):
    #fetch number of messages
    if selected_user!='Overall':
        df=df[df['users']==selected_user]
    num_msg= df.shape[0]
        #fetch number of words
    words = []
    for message in df['messages']:
        words.extend(message.split())
    num_media=df[df['messages']=='<Media omitted>\n'].shape[0]
    links=[]
    for message in df['messages']:
        links.extend(extract.find_urls(message))
    return num_msg, len(words),num_media,len(links)
def most_busy_users(df):
    x = df['users'].value_counts().head()
    name = x.index
    count = x.values
    df=round((df['users'].value_counts() / df['users'].shape[0] * 100), 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percent'})
    return x,df


def create_wordcloud(selected_user,df):
    f = open('stop_words.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=18,background_color='white')
    temp['messages']=temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user,df):
    f=open('stop_words.txt','r')
    stop_words=f.read()
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    emojis_list = []

    for message in df['messages']:
        emojis_in_message = emojis.get(message)
        emojis_list.extend(emojis_in_message)
    emoji_df=pd.DataFrame(Counter(emojis_list).most_common(len(Counter(emojis_list))))
    return emoji_df
def monthly_user(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    user_heatmap=df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)
    return user_heatmap