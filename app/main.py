import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException, Query

from app import broker, data, image_analysis, results

app = FastAPI(title="Movies API")


def _paginate(items: list, limit: int, offset: int) -> list:
    """limit=0 oznacza wszystkie rekordy."""
    end = None if limit == 0 else offset + limit
    return [item.__dict__ for item in items[offset:end]]


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/movies")
def get_movies(limit: int = Query(100, ge=0), offset: int = Query(0, ge=0)):
    return _paginate(data.load_movies(), limit, offset)


@app.get("/links")
def get_links(limit: int = Query(100, ge=0), offset: int = Query(0, ge=0)):
    return _paginate(data.load_links(), limit, offset)


@app.get("/ratings")
def get_ratings(limit: int = Query(100, ge=0), offset: int = Query(0, ge=0)):
    return _paginate(data.load_ratings(), limit, offset)


@app.get("/tags")
def get_tags(limit: int = Query(100, ge=0), offset: int = Query(0, ge=0)):
    return _paginate(data.load_tags(), limit, offset)


@app.get("/analyze_img_sync")
def analyze_img_sync(url: str):
    """Wersja bez kolejki: analiza zdjęcia wprost w endpoincie."""
    try:
        return {"url": url, "people": image_analysis.count_people(url)}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/analyze_img")
def analyze_img(url: str):
    """Producer: nie analizuje zdjęcia, tylko wrzuca pracę na kolejkę."""
    job_id = uuid.uuid4().hex
    results.create_job(job_id, url)
    try:
        broker.publish_job(job_id, url)
    except Exception as error:
        results.save_result(job_id, None, f"Brak kolejki: {error}")
        raise HTTPException(status_code=503, detail="Kolejka niedostępna")
    return {"job_id": job_id, "status": "queued"}


@app.get("/analyze_img/{job_id}")
def get_analysis(job_id: str) -> Optional[dict]:
    result = results.get_result(job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Nie ma takiej pracy")
    return result
