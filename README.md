# AI Brochure Generator

The AI Brochure Generator is a full-stack web application that scrapes a company's website, pulls useful content, and uses OpenAI's GPT-4o to create a clean, professional brochure in seconds.

Perfect for startups, marketing agencies, or anyone who needs to generate branded material fast.

---

## Live Demo

> **Note:** The currently deployed version runs on Render's free tier (512 MB RAM), which severely limits resources. Because of this, Chrome/Selenium runs in a minimal configuration - sequential scraping, no parallel processing, and basic headless mode. On a local machine or a more powerful server, the app runs with its full capabilities including undetected Chrome mode and parallel page scraping via multiprocessing.

---

## What It Does

- Crawls the important pages of a company's website
- Uses AI to extract and summarize what the company does
- Generates an elegant brochure in Markdown format
- Displays the result in a beautiful dark-themed frontend
- User authentication (register/login) with JWT tokens
- Personal dashboard to save, view, and delete generated brochures
- Designed to be fast, secure, and production-ready

---

## Tech Stack

| Layer          | Technology                        |
|----------------|-----------------------------------|
| Frontend       | React 18 (with Vite)              |
| Backend        | FastAPI (Python 3.11)             |
| AI Engine      | OpenAI GPT-4o / 4o-mini          |
| Scraper        | SeleniumBase + BeautifulSoup4     |
| Auth           | OAuth2 + JWT (python-jose)        |
| Database       | SQLite + SQLAlchemy               |
| Password Hash  | passlib + bcrypt                  |
| Styling        | CSS3 (Custom Dark Mode UI)        |
| Deployment     | Docker (Render) + Static (Vercel) |

---

## Authentication & Authorization

- **Register** a new account with username and password
- **Login** via OAuth2 password flow — returns a JWT access token
- All brochure generation and dashboard endpoints are **protected** — requires a valid token
- Passwords are hashed with **bcrypt** via passlib
- Tokens expire after **60 minutes**

---

## Dashboard

- View all previously generated brochures
- Click any brochure to see the full Markdown content
- Delete brochures you no longer need
- Each user only sees their own saved brochures

---

## Scraping Modes

The app automatically detects the environment and adapts:

| Environment        | Chrome Mode                          | Scraping        | Timeouts |
|--------------------|--------------------------------------|-----------------|----------|
| **Local**          | Undetected Chrome (`uc=True`)        | Parallel (Pool) | 2s       |
| **Docker / Render**| Standard headless + sandbox disabled | Sequential      | 10-15s   |

On resource-constrained servers (like Render free tier), the app:
- Uses regular headless Chrome instead of undetected mode
- Scrapes pages one at a time to avoid OOM crashes
- Falls back to BeautifulSoup if Chrome fails on a page

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key
- Google Chrome installed (for local development)

### Backend Setup

```bash
cd backend
pip install -r app/requirements.txt
# Set environment variable
export OPENAI_API_KEY=your_key_here
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Docker (Production)

```bash
cd backend
docker build -t ai-brochure .
docker run -p 8080:8080 -e OPENAI_API_KEY=your_key_here ai-brochure
```
