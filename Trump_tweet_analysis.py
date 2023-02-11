import pandas as pd
df = pd.read_csv('downloads/trumptweets.csv')
df.head()

df.isnull().sum()

dup = df.duplicated(['id'], keep = False)

df1 = df.drop_duplicates(['id'], keep= 'first')

word = []
for sen in df['content']:
    sen = sen.replace('.', ' ').replace(',',' ').replace(':', ' ').replace('!', " ").replace("?", " ")
    w = sen.split(' ')
    for i in w:
        if i != '':
            word.append(i)   
from collections import Counter
word_count = Counter(word)

from wordcloud import WordCloud, STOPWORDS 
wordcloud = WordCloud(width = 400, height = 400, 
                      background_color ='black', 
                      stopwords = set(STOPWORDS), 
                      max_words=100,
                      max_font_size = 100,
                     ).generate_from_frequencies(word_count) 
                    
plt.figure(figsize = (4, 4), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout() 
plt.show()

df['day'] = df.date.str.split(' ').str[0]
df['response'] = df['retweets']+df['favorites'] 
df['dup'] = df.loc[dup, 'response']
df['Nodup'] = df.loc[dup == False, 'response']
df[['dup', 'Nodup']].plot()

df['time'] = df['date'].str[-8:-6]
df1 = df.sort_values(by = 'time', ascending = True)
df1.plot(x = 'time', y = 'response')

grouped = df['response'].groupby(df['time'])
grouped.mean().plot()

grouped2 = df['favorites'].groupby(df['time'])
grouped2.mean().plot()

grouped3 = df['retweets'].groupby(df['time'])
grouped3.mean().plot()

condition = df['mentions'].isnull() & df['hashtags'].isnull()
df.loc[condition, 'response'].plot()
df.loc[condition == False, 'response'].plot()

df.loc[condition, 'response'].mean()
df.loc[condition == False, 'response'].mean()

hash_condition = df['hashtags'].notnull()
men_condition = df['mentions'].notnull()
df.loc[men_condition, 'response'].describe()
df.loc[hash_condition, 'response'].describe()

df['condition'] = df['content'].str.isupper()
sns.catplot(data = df, x = 'condition', y = 'response', kind = 'box')

df['I_contain'] = df['content'].str.contains('I ')
sns.catplot(data = df, x = 'I_contain', y = 'response', kind = 'box')

