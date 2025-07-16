import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
API_KEY = os.getenv("TWITTER_API_KEY")
headers = {"X-API-Key": API_KEY}


def get_all_tweets(username, max_tweets=5):
    all_tweets = []
    cursor = ""
    page = 1
    while len(all_tweets) < max_tweets:
        base_url = "https://api.twitterapi.io/twitter/user/last_tweets"
        params = {
            "userName": username, 
            "count": 50,  # Maximum par page
            "cursor": cursor
        }
        
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Erreur API: {response.text}")
            break
            
        data = response.json()
        tweets = data.get("data", {}).get("tweets", [])
        if not tweets:
            print(f"📄 Page {page}: Aucun tweet trouvé")
            break
        page_original_tweets = []
        for tweet in tweets:
            if tweet.get("isReply", False):
                continue
            if tweet.get("retweeted_tweet") is not None and tweet.get("retweeted_tweet"):
                continue
            page_original_tweets.append(tweet)
            if len(all_tweets) + len(page_original_tweets) >= max_tweets:
                break
        
        all_tweets.extend(page_original_tweets)
        if not data.get("has_next_page", False):
            break
        cursor = data.get("next_cursor", "")
        if not cursor:
            break
        page += 1
    
    return all_tweets[:max_tweets]


def save_to_csv(tweets, username):
    data_dir = "./data"
    os.makedirs(data_dir, exist_ok=True)
    filename = f"{username}_tweets.csv"
    filepath = os.path.join(data_dir, filename)

    df = pd.DataFrame([{
        "id": tweet.get("id", ""),
        "date": tweet.get("createdAt", ""),
        "text": tweet.get("text", ""),
        "retweet_count": tweet.get("retweetCount", 0),
        "reply_count": tweet.get("replyCount", 0),
        "like_count": tweet.get("likeCount", 0),
        "quote_count": tweet.get("quoteCount", 0),
        "view_count": tweet.get("viewCount", 0),
        "bookmark_count": tweet.get("bookmarkCount", 0),
        "lang": tweet.get("lang", ""),
        "source": tweet.get("source", ""),
        "url": tweet.get("url", ""),
        "author_username": tweet.get("author", {}).get("userName", ""),
        "author_name": tweet.get("author", {}).get("name", ""),
        "author_followers": tweet.get("author", {}).get("followers", 0)
    } for tweet in tweets])
    
    df.to_csv(filepath, index=False, encoding="utf-8")
    print(f"{len(tweets)} tweets sauvegardés dans {filepath}")
    return filepath


def main(username = "elonmusk" , max_tweets = 5):   
    tweets = get_all_tweets(username, max_tweets) 
    if tweets:
        print(f"\n Résultat : {len(tweets)} tweets originaux récupérés pour @{username}")
        filepath = save_to_csv(tweets, username)
        
    else:
        print("Aucun tweet original trouvé")
