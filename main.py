from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os
import math
from database import init_db, save_search, get_recent_searches

load_dotenv()

app = FastAPI(title="Creator Trend Radar")

init_db()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

class TopicRequest(BaseModel):
    topic: str
    platform: str = "youtube"

def fetch_youtube_data(topic: str):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": topic,
        "type": "video",
        "order": "viewCount",
        "publishedAfter": "2024-01-01T00:00:00Z",
        "maxResults": 10,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def calculate_score(data: dict, topic: str):
    items = data.get("items", [])
    
    if not items:
        return 10, "cold"
    
    result_count = len(items)
    title_matches = sum(
        1 for item in items
        if topic.lower() in item["snippet"]["title"].lower()
    )
    
    base_score = (result_count / 10) * 50
    match_bonus = (title_matches / max(result_count, 1)) * 50
    raw_score = base_score + match_bonus
    score = max(1, min(100, math.ceil(raw_score)))

    if score >= 70:
        trend = "rising"
    elif score >= 40:
        trend = "stable"
    else:
        trend = "cold"

    return score, trend

@app.get("/")
def root():
    return {"message": "Creator Trend Radar is running!"}

@app.post("/score")
def get_score(request: TopicRequest):
    data = fetch_youtube_data(request.topic)
    score, trend = calculate_score(data, request.topic)
    save_search(request.topic, request.platform, score, trend)

    if trend == "rising":
        recommendation = "Post within 48 hours, this topic is hot!"
    elif trend == "stable":
        recommendation = "Good topic, post within the week."
    else:
        recommendation = "Topic is cold, consider a different angle."

    return {
        "topic": request.topic,
        "platform": request.platform,
        "score": score,
        "trend": trend,
        "recommendation": recommendation
    }

@app.get("/history")
def get_history():
    rows = get_recent_searches()
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "topic": row[1],
            "platform": row[2],
            "score": row[3],
            "trend": row[4],
            "searched_at": row[5]
        })
    return {"recent_searches": results}