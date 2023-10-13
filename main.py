from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
from api.controllers import health_controller, comparison_controller
from domain.exceptions.application_error import ApplicationError


from containers import Services
import uvicorn


def create_app() -> FastAPI:
    app = FastAPI(version='1.0', title='VSM Text Base Similarity API: IDPA Project')
    services = Services()

    services.wire(modules=[comparison_controller])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        health_controller.router,
        prefix="/health",
        tags=["Health"]
    )

    app.include_router(
        comparison_controller.router,
        prefix="/compare",
        tags=["Comparison"]
    )

    app.services = services

    @app.exception_handler(ApplicationError)
    async def api_exception_handler(request: Request, exception: ApplicationError):
        return JSONResponse(status_code=exception.status_code, content={"message": exception.message})

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(request: Request, exception: Exception):
        return JSONResponse(status_code=500, content={"message": exception.__str__()})

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=2000
    )

