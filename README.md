# Logos Quotes API

A tiny FastAPI service that returns a random (or daily) quote for dashboards like [Homepage](https://github.com/gethomepage/homepage).
---
## What this does

- Serves a quote JSON response at `GET /quote`
- Optional `daily=true` makes the quote stable for the day
- Quotes are stored in a **live** `quotes.json` file mounted into the container
- On first run, the container will seed `/config/quotes.json` from the repo seed file `config/quotes.json`
---
## API

### Health
- `GET /health`

### Quote
- `GET /quote`
- `GET /quote?daily=true`
- `GET /quote?tag=motivation`
- `GET /quote?tag=motivation&daily=true`
---
## Repo layout

- `app.py` – FastAPI server
- `requirements.txt` – Python dependencies
- `Dockerfile` – image build
- `config/quotes.json` – **seed** quotes (tracked in git)
- `/config/quotes.json` – **live** quotes inside container (bind-mounted on Unraid)
---
## Docker Compose

```yaml
services:
  inspire:
    build: .
    container_name: logos
    restart: unless-stopped
    ports:
      - "8765:8000"
    volumes:
      - /mnt/user/appdata/logos:/config
    environment:
      - QUOTES_PATH=/config/quotes.json

