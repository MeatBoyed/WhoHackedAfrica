from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import attacks_router
# from .errors import register_all_errors
# from .middleware import register_middleware


version = "v1"

description = """
A REST API for a book review web service.

This REST API is able to;
- Create Read Update And delete books
- Add reviews to books
- Add tags to Books e.t.c.
    """

version_prefix =f"/api/{version}"

app = FastAPI(
    title="Charles' Api Integration Platform",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Charles Rossouw",
        "url": "https://github.com/meatboyed",
        "email": "charles@mbvit.co.za",
    },
    terms_of_service="httpS://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc"
)

# register_all_errors(app)

# register_middleware(app)


app.include_router(attacks_router, prefix=f"{version_prefix}/attacks", tags=["attacks"])


# Custom exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return RedirectResponse(url=f"{version_prefix}/docs")