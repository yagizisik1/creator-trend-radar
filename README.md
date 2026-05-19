# Creator Trend Radar 🎯

A REST API that scores YouTube topics by trend potential. Built with FastAPI and SQLite.

## What it does

Send a topic → get a trend score (0-100), trend status, and posting recommendation.

```json
POST /score
{
  "topic": "minimalist apartment tour",
  "platform": "youtube"
}

→ {
  "score": 78,
  "trend": "rising",
  "recommendation": "Post within 48 hours, this topic is hot!"
}
```

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/score` | Score a topic |
| GET | `/history` | Last 10 searches |

## How it works

1. Fetches top 10 YouTube videos for the given topic
2. Calculates a score based on result count and title match rate
3. Returns trend status: `rising` (70+), `stable` (40-70), `cold` (<40)
4. Saves every search to SQLite database

## Setup

```bash
git clone https://github.com/yagizisik1/creator-trend-radar.git
cd creator-trend-radar

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
Get your free API key at: https://console.cloud.google.com

## Run

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Tech Stack

- **FastAPI** — API framework
- **SQLite** — Local database
- **YouTube Data API v3** — Trend data source
- **Uvicorn** — ASGI server
