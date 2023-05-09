import json
import pandas as pd
import matplotlib.pyplot as plt



def visual_analysis(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    if df.empty == 0:
        # Removing rows with empty comments
        df = df[df['comment'] != '']

        # Adding a column with a rating on a scale of 1-10
        df['sentiment_rating'] = round((df['sentiment_score'] + 1) * 5, 1)

        # Grouping comments by sentiment rating and calculating the number of occurrences in each group
        #rating_counts = df.groupby('sentiment_rating')['comment'].count()
        df['category'] = df['sentiment_score'].apply(
            lambda x: 'negatywny' if x < -0.05 else ('neutralny' if x <= 0.05 else 'pozytywny'))
        categories = df.groupby('category').count()

        # Displaying a sentiment bar chart
        sentiment_bar_char(categories)

        # Displaying a sentiment box plot
        sentiment_box_plot(df['sentiment_rating'])

        # Displaying a subjectivity bar chart
        subjectivity_rating(df)

def sentiment_bar_char(categories):
    plt.bar(categories.index, categories['comment'])
    plt.xlabel('Kategorie')
    plt.ylabel('Liczba komentarzy')
    plt.show()


def sentiment_box_plot(sentiment_rating):
    plt.boxplot(sentiment_rating)
    plt.xlabel('Sentyment')
    plt.title('Boxplot sentymentu w komentarzach')
    plt.show()

def subjectivity_rating(df):
    sub = df[df['subjectivity_score'] > 0.5]
    obj = df[df['subjectivity_score'] <= 0.5]
    sub_count = len(sub)
    obj_count = len(obj)

    plt.bar(['Subiektywne', 'Obiektywne'], [sub_count, obj_count])
    plt.xticks(rotation='horizontal')
    plt.show()