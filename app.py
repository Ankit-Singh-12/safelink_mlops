import sys
import os
from urllib import request
import certifi
import pymongo
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from safelink.exception.exception import SafeLinkException
from safelink.logging.logger import logging
from safelink.pipeline.training_pipeline import TrainingPipeline
from safelink.utils.main_utils.utils import load_object
from safelink.utils.ml_utils.model.estimator import NetworkModel

ca = certifi.where()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from safelink.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from safelink.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train", tags=["Train Dataset"])
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise SafeLinkException(e,sys)

@app.post("/predict", tags=["Predict"])
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes="table table-striped", index=False, escape=True)

        return templates.TemplateResponse(
        request=request,
        name="table.html",
        context={"table": table_html},
        status_code=200
        )
        
    except Exception as e:
            raise SafeLinkException(e,sys)

    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
