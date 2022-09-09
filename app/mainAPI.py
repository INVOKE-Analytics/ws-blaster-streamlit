from fastapi import FastAPI
import app.routers.blastingAPI as blastingAPI
import app.routers.manageAPI as manageAPI
from mangum import Mangum

from app.config import get_settings

settings = get_settings()
root_path = "/" if settings.STAGE == 'local' else f"/{settings.STAGE}/"
app = FastAPI(title=f"{settings.PROJECT_NAME} ({settings.STAGE.upper()})",
              root_path=root_path,
              description="""An API Service created to blast promotional 
                            messages to prospective clients using Whats App.""")
handler = Mangum(app)



app.include_router(blastingAPI.router)
app.include_router(manageAPI.router)

#### DUMMY DATABASE ################

@app.get('/')
def testing():
    return {'testing':'succeed'}
