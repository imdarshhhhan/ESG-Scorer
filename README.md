# ESG Trust Score (FastAPI)

The ESG Scorer app, moved from Streamlit to FastAPI. Same data, same Random Forest model,
same trust score maths and the same look.

## Run it

```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python main.py                 # or: uvicorn main:app --reload
```

Open http://127.0.0.1:8000

## Folder structure

```
esg-scorer-fastapi/
├── main.py                      # creates the app, mounts static files, adds routers
├── requirements.txt
├── data/                        # display_data.csv, Global_data_preprocessed.csv, model.pkl
└── app/
    ├── config.py                # paths + all the fixed numbers in one place
    ├── templating.py            # Jinja2 setup + small alert helper
    ├── routers/                 # URL layer (thin, no logic)
    │   ├── pages.py             # GET /          -> full page
    │   ├── compare.py           # GET /compare   -> comparison results (HTML piece)
    │   ├── sector.py            # GET /sector    -> sector results (HTML piece)
    │   └── assets.py            # GET /vendor/plotly.min.js
    ├── services/                # all the real logic
    │   ├── data_loader.py       # load csv + load/train model (cached)
    │   ├── trust_score.py       # model prediction -> 0-100 trust score
    │   ├── card_builder.py      # one company -> data for its card
    │   ├── company_service.py   # find companies, build the comparison
    │   ├── sector_service.py    # sector stats + ranked list
    │   └── chart_service.py     # plotly figures
    ├── templates/               # html only (index, partials/, macros/)
    └── static/
        ├── css/                 # one css file per section of the page
        └── js/                  # dropdown, tabs, history, compare, sector, charts
```

## How a request flows

1. Browser opens `/` -> `pages.py` renders the full page (header, hero, tabs, footer).
2. User clicks **Compare** -> `compare.js` calls `/compare?company1=..&company2=..`
   -> `compare.py` -> `company_service` -> returns the cards, winner banner and chart as an HTML piece.
3. User picks a sector -> `sector.js` calls `/sector?name=..` -> same idea.
4. Charts are built in Python (plotly), sent as JSON, and drawn in the browser by `charts.js`.

Interactive API docs are available at http://127.0.0.1:8000/docs
