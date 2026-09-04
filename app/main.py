import logging
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.category import router as category_router
from app.api.routers.task import router as task_router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()

settings = get_settings()
app = FastAPI()
logger = logging.getLogger("app.middleware")

request_count = 0

app.add_middleware(
    CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["*"]
)


@app.middleware("http")
async def log_request(request: Request, call_next) -> Response:
    global request_count
    request_count += 1
    current_request_number = request_count
    started_at = perf_counter()
    try:
        response = await call_next(request)
    except:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise
    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    response.headers["X-Request-Number"] = str(current_request_number)
    return response


app.include_router(task_router)
app.include_router(category_router)
