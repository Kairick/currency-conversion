from fastapi import APIRouter, FastAPI
from starlette.responses import RedirectResponse

from routes import currency_api
from settings import server_settings

router = APIRouter(prefix='/api')
router.include_router(currency_api, prefix='/currency', tags=['Currency'])

tags_metadata = [{'name': 'Currency', 'description': 'Currency API'}]

app = FastAPI(
    title='Currency conversion API',
    version='0.0.1',
    description='API for currency conversion',
    docs_url='/api/docs',
    openapi_url='/api/docs/openapi.json',
    redoc_url=None,
    openapi_tags=tags_metadata,
    debug=server_settings.debug
)
app.include_router(router)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/api/docs')
