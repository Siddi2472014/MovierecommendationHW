import time
import pandas as pd
from textblob import TextBlob
from colorama import init, Fore
init(autoreset=True)
try:
    df=pd.read_csv('imdb_top_1000.csv')
except FileNotFoundError:
    print(Fore.RED+"Error: File not found")
    exit()
genres=sorted({g.strip() for xs in df['Genre'].dropna().str.split(',') for g in xs})
def dots():
    for i in range(3):
        print('.',end='',flush=True)
        time.sleep(0.5)
def senti(p):
    if p==0:
        return 'Neutral'
    elif p>0:
        return 'Positive'
    else:
        return 'Negative'
def recommend(genre=None,mood=None,rating=None,n=5):
    d=df
    if genre:
        d=d[d['Genre'].str.contains(genre,case=False,na=False)]
    if rating is not None:
        d=d[d['IMDB_Rating']>=rating]
    if d.empty:
        return "No movies found matching the criteria"
    d=d.sample(frac=1).reset_index(drop=True)
    need_nonneg=bool(mood)
    out=[]
    for _,r in d.iterrows():
        ov=r.get('Overview')
        if pd.isna(ov):
            continue
        pol=TextBlob(ov).sentiment.polarity
        if (not need_nonneg) or (need_nonneg and pol>=0):
            out.append((r,pol))
            if len(out)==n:
                break
    return out if out else "No movies found matching the criteria"
def show(recs,name):
    print(Fore.GREEN+f"\n{name}'s Movie Recommendations:")
    for i,(r,pol) in enumerate(recs,1):
        print(Fore.CYAN+"\n"+"="*60)
        print(Fore.YELLOW+f"{i}. {r['Series_Title'].upper()}")
        print(Fore.CYAN+"="*60)
        print(Fore.WHITE+f"Release Year:{r['Released_Year']}")
        print(Fore.WHITE+f"Genre:{r['Genre']}")
        print(Fore.WHITE+f"IMDb Rating:{r['IMDB_Rating']}/10")
        print(Fore.WHITE+f"Runtime:{r['Runtime']}")
        print(Fore.WHITE+f"Certificate:{r['Certificate']}")
        print(Fore.WHITE+f"Director:{r['Director']}")
        cast=", ".join([str(r['Star1']),str(r['Star2']),str(r['Star3']),str(r['Star4'])])
        print(Fore.WHITE+f"Cast:{cast}")
        print(Fore.YELLOW+"\nOverview:")
        print(Fore.WHITE+str(r['Overview']))
        print(Fore.WHITE+f"\nMeta Score:{r['Meta_score']}")
        print(Fore.WHITE+f"IMDb Votes:{r['No_of_Votes']:,}")
        print(Fore.WHITE+f"Gross:{r['Gross']}")
        print(Fore.GREEN+f"Sentiment:{senti(pol)}")
        print(Fore.CYAN+"="*60)
def get_genre():
    print(Fore.YELLOW+"Available Genres:")
    for i,g in enumerate(genres,1):
        print(Fore.CYAN+f"{i}. {g}")
    while True:
        choice=input(Fore.YELLOW+"Enter the genre number (or press Enter to skip): ")
        if not choice:
            return None
        if choice.isdigit() and 1<=int(choice)<=len(genres):
            return genres[int(choice)-1]
        else:
            print(Fore.RED+"Invalid choice. Please try again.")
def get_rating():
    while True:
        choice=input(Fore.YELLOW+"Enter minimum IMDB rating (7.6-9.6) (or press Enter to skip): ")
        if not choice:
            return None
        try:
            rating=float(choice)
            if 7.6<=rating<=9.6:
                return rating
            else:
                print(Fore.RED+"Rating must be between 7.6 and 9.6.")
        except ValueError:
            print(Fore.RED+"Invalid input. Please enter a number.")
print("Welcome to the Movie Recommendation System!")
name=input(Fore.YELLOW+"Enter your name: ")
print(Fore.GREEN+f"Hello, {name}! Let's find the perfect movie for you.")
mood=input(Fore.YELLOW+"What is your mood today? (happy, sad, neutral) or press Enter to skip: ").strip().lower()
mp=TextBlob(mood).sentiment.polarity
rating=get_rating()
genre=get_genre()
print(Fore.YELLOW+f"Finding recommendations for {name}",end='')
dots()
recs=recommend(genre=genre,mood=mood,rating=rating,n=5)
if isinstance(recs,str):
    print(Fore.RED+"\n"+recs+"\n")
else:
    show(recs,name)
while True:
    answer=input(Fore.YELLOW+"\nWould you like more recommendations? (yes/no): ").strip().lower()
    if answer=='yes':
        mood_2=input(Fore.YELLOW+"Enter your mood: ").strip().lower()
        sentiment_2=TextBlob(mood_2).sentiment.polarity
        rating_2=get_rating()
        genre_2=get_genre()
        print(Fore.YELLOW+f"Finding recommendations for {name}",end='')
        dots()
        recs_2=recommend(genre=genre_2,mood=sentiment_2,rating=rating_2,n=5)
        if isinstance(recs_2,str):
            print(Fore.RED+"\n"+recs_2+"\n")
        else:
            show(recs_2,name)
    elif answer=='no':
        print(Fore.GREEN+"Thank you for using the Movie Recommendation System. Enjoy your movie!")
        break
    else:
        print(Fore.RED+"Invalid choice. Please enter yes or no.")
#Note
#All changes made in this code compared to prev code that was made in class:
#Code made in class: Once recommendations were found, only the sentiment and the name of the movie was displayed
#Code made by me: Once recommendations are displayed, these 13 datas are displayed:-
#-name of the movie
#-release year
#-genre
#-imdb Rating
#-time
#-certificate
#-director
#-cast
#-overview
#-meta Score
#-imdb Votes
#-gross
#-sentiment
