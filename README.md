# Izba AI

An AI-powered real estate assistant for the UK housing market, focused on the Royal Borough of Kensington and Chelsea. Izba AI combines historical Land Registry property price data (since 1995) with current Rightmove listings to answer natural language questions about properties, prices, and local amenities.

The assistant — named **Domovenok** (a friendly house spirit from Slavic folklore) — can query historical price trends, search current listings, calculate commute times, and find nearby cafes, all through a conversational chat interface.

## Architecture

```
izba-ai/
├── backend/              # FastAPI server with LLM-powered agent
│   ├── main.py           # REST API (4 endpoints)
│   ├── agent_implementation.py  # ReAct agent with 5 tools
│   ├── tools/            # Orchestrator, SQL generators, search, maps
│   ├── prompts/          # Jinja2 templates for LLM prompts
│   ├── data_processing/  # CSV-to-SQLite pipeline
│   └── databases/        # SQLite databases
├── scraper/              # Rightmove property listing scraper
│   └── main.py
├── ui/                   # Streamlit chat interface
│   └── main.py
├── data/                 # Raw CSV data (Land Registry)
└── notebooks/            # Jupyter notebooks for exploration
```

## How It Works

1. **User asks a question** via the Streamlit chat UI
2. **Orchestrator** classifies the query and routes it to the right handler:
   - Historical price queries -> natural language to SQL against Land Registry data
   - Current listing queries -> natural language to SQL against scraped Rightmove data
   - General questions -> ReAct agent with full tool access
3. **LLM generates SQL** from the user's question using Jinja2 prompt templates
4. **Results are formatted** into human-readable responses with currency formatting and property cards

### Agent Tools

The ReAct agent (built with LlamaIndex) has access to five tools:

| Tool | Description |
|------|-------------|
| **Historical Data** | Query Land Registry price paid data since 1995 via natural language to SQL |
| **Current Market Data** | Search current Rightmove listings via natural language to SQL |
| **Search Engine** | General internet search via Tavily API |
| **Nearby Cafes** | Find top-rated cafes near an address via Google Maps |
| **Journey Planner** | Calculate public transit commute times via Google Maps Directions |

## Tech Stack

- **Backend**: FastAPI, LlamaIndex (ReAct agent), Jinja2
- **LLM**: Meta Llama 3.1 405B Instruct (via Nebius AI Studio)
- **Frontend**: Streamlit
- **Scraper**: Firecrawl
- **Database**: SQLite
- **Data**: Pandas
- **APIs**: Nebius, Tavily, Google Maps, Firecrawl

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) package manager
- API keys for: Nebius AI Studio, Firecrawl, Tavily, Google Maps

## Setup

### 1. Install dependencies

```bash
poetry install
```

### 2. Configure environment variables

Create a `.env` file in the project root (and/or `backend/` directory) with:

```
NEBIUS_API_KEY=your_nebius_api_key
NEBIUS_BASE_URL=https://api.studio.nebius.ai/v1/
FIRECRAWL_API_KEY=your_firecrawl_api_key
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

### 3. Initialize the historical price database

```bash
python backend/data_processing/pandas_to_sqlite.py
```

This loads `data/kensington_chelsea_price_paid_data.csv` into `backend/databases/price_paid_data.db`.

### 4. Scrape current listings (optional)

```bash
python scraper/main.py
```

Scrapes up to 20 pages of Kensington & Chelsea property listings from Rightmove into `backend/databases/scraped_listings.db`.

## Running

### Start the backend

```bash
cd backend
poetry run uvicorn main:app --host 127.0.0.1 --port 8080
```

### Start the UI

```bash
cd ui
poetry run streamlit run main.py
```

Then open http://localhost:8501 in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/llama_index_agent/{user_query}` | Full ReAct agent with all tools |
| GET | `/orchestrator/{user_query}` | Query router — classifies and routes to the right handler |
| GET | `/historical_prices/{user_query}` | Historical Land Registry price queries |
| GET | `/current_listings/{user_query}` | Current Rightmove listing queries |

## Example Queries

- "What was the average price of a flat in 2020?"
- "Show me 3-bedroom properties under 1.5 million"
- "What's the difference in price between detached and terraced houses in January 2024?"
- "Find me cafes near Kensington High Street"
- "How long is the commute from Chelsea to Canary Wharf?"

## Data Sources

- **Historical prices**: [UK Land Registry Price Paid Data](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads) — property transactions in Kensington & Chelsea since 1995
- **Current listings**: Scraped from [Rightmove](https://www.rightmove.co.uk/) for properties for sale in Kensington & Chelsea
