from fastapi import FastAPI

import os
import time
from datetime import date as d
from typing import Union

from api.db.wage import Wage

os.environ["TZ"] = "Asia/Tokyo"
time.tzset()

app = FastAPI()


@app.get("/")
async def root(prefecture: str = "all", date: Union[str, None] = None):
    try:
        date = d.today() if date is None else d.fromisoformat(date)
    except ValueError:
        return {"error": f"Invalid date format: {date}. Required format: YYYY-MM-DD"}

    return Wage.search(prefecture, date).to_response()


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(app, host="0.0.0.0", port=port)
