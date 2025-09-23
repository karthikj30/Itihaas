import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from website import create_app, db
from website.merchandise_data import add_clothing_items
from website.automated_messaging import start_scheduler
import requests
import threading

# --------------------------
# Environment Configuration
# --------------------------

# Email credentials (use environment variables in production)
os.environ['EMAIL_USER'] = os.environ.get('EMAIL_USER', 'itihaasdairy@gmail.com')
os.environ['EMAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD', 'opuo ywpj izjy qnxf')  

# Google Maps API key
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', "AIzaSyBygM66vagm5UY7vMN_mHOiUdNNZmidvZQ")
os.environ['GOOGLE_MAPS_API_KEY'] = GOOGLE_MAPS_API_KEY

# Gnews API configuration
GNEWS_API_KEY = os.environ.get('GNEWS_API_KEY', "4036a646f52401f9c151f4850ad306aa")
GNEWS_API_URL = "https://gnews.io/api/v4/search"

# --------------------------
# Create Flask App
# --------------------------
app = create_app()

# --------------------------
# News Routes
# --------------------------

@app.route("/news")
def news():
    query = "(Taj Mahal OR Red Fort OR Qutub Minar OR India Gate OR heritage sites OR Indian tourism OR Indian transport) AND (India OR Indian)"
    news_data = fetch_news(query)
    return render_template("news.html", news=news_data)

@app.route("/api/news")
def api_news():
    query = request.args.get("q", "(Taj Mahal OR Red Fort OR Qutub Minar OR India Gate OR heritage sites OR Indian tourism OR Indian transport) AND (India OR Indian)")
    news_data = fetch_news(query)
    return jsonify({"articles": news_data})

def fetch_news(query):
    """
    Fetch news from Gnews API with fallback for broader search if no results.
    """
    try:
        params = {
            "q": query,
            "lang": "en",
            "country": "in",
            "max": 12,
            "apikey": GNEWS_API_KEY,
            "sortby": "publishedAt",
            "in": "title,description"
        }
        response = requests.get(GNEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])

        # Filter and transform
        keywords = ["monument", "heritage", "tourism", "transport", "taj mahal", 
                    "red fort", "qutub minar", "india gate", "temple", "palace", 
                    "fort", "museum", "tourist", "travel", "india", "indian"]
        transformed_articles = [
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "url": a.get("url", ""),
                "urlToImage": a.get("image", ""),
                "source": {"name": a.get("source", {}).get("name", "Unknown Source")},
                "publishedAt": a.get("publishedAt", "")
            }
            for a in articles
            if any(k in (a.get("title", "") + a.get("description", "")).lower() for k in keywords)
        ]

        # Fallback if no articles
        if not transformed_articles:
            params["q"] = "Indian tourism OR Indian monuments"
            response = requests.get(GNEWS_API_URL, params=params)
            response.raise_for_status()
            articles = response.json().get("articles", [])
            transformed_articles = [
                {
                    "title": a.get("title", ""),
                    "description": a.get("description", ""),
                    "url": a.get("url", ""),
                    "urlToImage": a.get("image", ""),
                    "source": {"name": a.get("source", {}).get("name", "Unknown Source")},
                    "publishedAt": a.get("publishedAt", "")
                }
                for a in articles
            ]

        return transformed_articles

    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []

# --------------------------
# Background Tasks
# --------------------------

def start_background_tasks():
    """
    Start all background tasks, e.g., WhatsApp scheduler.
    """
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    print("Background tasks started successfully")

# --------------------------
# Main Entry Point
# --------------------------
if __name__ == '__main__':
    print("\nStarting ITIHASA server...")
    print("=" * 50)

    # Database setup
    with app.app_context():
        db.create_all()
        add_clothing_items()

    # Start background tasks
    start_background_tasks()

    # Use Render's PORT or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
