from fastapi import FastAPI
import app.routers.blastingAPI as blastingAPI
import app.routers.manageAPI as manageAPI

app = FastAPI(title="Whatsapp Blaster API", 
            description="An API to blast message using Whatsapp.", 
            version="0.1.0")
app.include_router(blastingAPI.router)
app.include_router(manageAPI.router)

#### DUMMY DATABASE ################

@app.get('/')
def testing():
    return {'testing':'succeed'}
