import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from website import create_app, db
from website.merchandise_data import add_clothing_items
from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta
import threading
from website.automated_messaging import start_scheduler

# Set email credentials for testing (remove in production)
os.environ['EMAIL_USER'] = 'itihaasdairy@gmail.com'
os.environ['EMAIL_PASSWORD'] = 'opuo ywpj izjy qnxf'  # Replace with the 16-character App Password you generated

# Add Google Maps configuration
GOOGLE_MAPS_API_KEY = "AIzaSyBygM66vagm5UY7vMN_mHOiUdNNZmidvZQ"
GOOGLE_MAPS_API_KEY = "AIzaSyBygM66vagm5UY7vMN_mHOiUdNNZmidvZQ"
os.environ['GOOGLE_MAPS_API_KEY'] = GOOGLE_MAPS_API_KEY

app = create_app()

# Gnews API configuration
GNEWS_API_KEY = "4036a646f52401f9c151f4850ad306aa"  # Get your free API key from https://gnews.io/
GNEWS_API_URL = "https://gnews.io/api/v4/search"

@app.route("/news")
def news():
    # Default search query for monument-related news
    query = "(Taj Mahal OR Red Fort OR Qutub Minar OR India Gate OR heritage sites OR Indian tourism OR Indian transport) AND (India OR Indian)"
    news_data = fetch_news(query)
    return render_template("news.html", news=news_data)

@app.route("/api/news")
def api_news():
    query = request.args.get("q", "(Taj Mahal OR Red Fort OR Qutub Minar OR India Gate OR heritage sites OR Indian tourism OR Indian transport) AND (India OR Indian)")
    news_data = fetch_news(query)
    return jsonify({"articles": news_data})

def fetch_news(query):
    try:
        params = {
            "q": query,
            "lang": "en",
            "country": "in",
            "max": 12,  # Number of articles to fetch
            "apikey": GNEWS_API_KEY,
            "sortby": "publishedAt",  # Get the most recent news first
            "in": "title,description"  # Search in title and description
        }
        
        response = requests.get(GNEWS_API_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get("articles", [])
        
        # Transform the articles to match our template format
        transformed_articles = []
        for article in articles:
            # Only include articles that are relevant to our topics
            if any(keyword in article.get("title", "").lower() or 
                  keyword in article.get("description", "").lower() 
                  for keyword in ["monument", "heritage", "tourism", "transport", "taj mahal", 
                                "red fort", "qutub minar", "india gate", "temple", "palace", 
                                "fort", "museum", "tourist", "travel", "india", "indian"]):
                transformed_article = {
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "url": article.get("url", ""),
                    "urlToImage": article.get("image", ""),
                    "source": {
                        "name": article.get("source", {}).get("name", "Unknown Source")
                    },
                    "publishedAt": article.get("publishedAt", "")
                }
                transformed_articles.append(transformed_article)
        
        # If no articles found, try a broader search
        if not transformed_articles:
            params["q"] = "Indian tourism OR Indian monuments"
            response = requests.get(GNEWS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            
            for article in articles:
                transformed_article = {
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "url": article.get("url", ""),
                    "urlToImage": article.get("image", ""),
                    "source": {
                        "name": article.get("source", {}).get("name", "Unknown Source")
                    },
                    "publishedAt": article.get("publishedAt", "")
                }
                transformed_articles.append(transformed_article)
        
        return transformed_articles
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []

def start_background_tasks():
    """
    Start all background tasks
    """
    # Start the WhatsApp message scheduler
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    print("Background tasks started successfully")

if __name__ == '__main__':
    print("\nStarting ITIHASA server...")
    print("=" * 50)
    print("Access the website at: http://127.0.0.1:5000")
    print("=" * 50)
    print("\n")
    
    with app.app_context():
        # Drop all tables and recreate them
        #db.drop_all()
        db.create_all()
        
        # Add initial data
        add_clothing_items()
    
    # Start background tasks
    start_background_tasks()
    
    app.run(debug=True) 