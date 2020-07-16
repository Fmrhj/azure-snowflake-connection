from fastapi import FastAPI
import uvicorn

from db.snowflakeconnector import SnowflakeConnector

def main(configfile="./config.yml"):
    app = FastAPI()
    @app.get("/")
    
    async def root():
        return {"message": "Pexon to the World"}

    # implement an asgi async server (socket io). For the time keep it simple

    uvicorn.run(app, host="0.0.0.0", port=8080, workers=1)

if __name__=="__main__":
    main()
