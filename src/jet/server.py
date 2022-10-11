from fastapi import FastAPI
import structlog
logger = structlog.getLogger(__name__)
app = FastAPI()


@app.get("/execute/{pull_request_name}")
async def read_item(pull_request_name):
    logger.info(
        "Received command for merging pull request", pull_request=pull_request_name
    )
    return {"pull_request_name": pull_request_name}
