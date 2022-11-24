from fastapi import FastAPI, Request
from common import get_data
from generate_schema import get_schema
from get_data import format_keys, get_filtered_data
import logging
from logging.config import dictConfig

from config import LogConfig

from fastapi_pagination import Page, add_pagination, paginate
from models import ResponseModel, Item, Station

dictConfig(LogConfig().dict())
logger = logging.getLogger("swancoolapplogger")

app = FastAPI()


@app.get("/schema")
async def get():
    """Get json schema from json response."""
    return get_schema()


@app.post("/data/", response_model=Page[ResponseModel])
async def post(request: Request, item: Item):
    """Return data for a given query."""
    appended_data = []
    rows = format_keys(get_data())

    if not item.where:
        appended_data.extend(rows)
    else:
        for row in rows:
            appended_data.extend(get_filtered_data(row, item.where))

    if order_by := request.query_params.get("orderBy"):
        order = request.query_params.get("order")
        appended_data = sorted(
            appended_data,
            key=lambda d: d[order_by],
            reverse=True if order == "desc" else False,
        )

    return paginate(appended_data)


@app.get("/data/{stationId}")
async def get(stationId: int):
    """Return single station by id."""
    rows = format_keys(get_data())
    return [item for item in rows if item["stationId"] == stationId]


@app.put("/data/{stationId}")
async def put(stationId: int, body: Station):
    """Update station by id."""
    rows = format_keys(get_data())
    logger.info(f"put request logged {stationId=}")

    record = [item for item in rows if item["stationId"] == stationId]
    record[0]["stationId"] = body.stationId
    return record


add_pagination(app)
