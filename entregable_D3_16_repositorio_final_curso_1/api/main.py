from io import StringIO

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from api.dependencies import get_model, get_prediction_threshold
from api.schemas import CustomerInput, PredictionResponse
from src.models.prediction import predict_customers


app = FastAPI(
    title="NovaTel Customer Churn API",
    description="API REST para prediccion de churn de clientes de NovaTel.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "customer-churn-api",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    get_model()
    return {
        "status": "healthy",
        "service": "customer-churn-api",
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerInput):
    try:
        dataframe = pd.DataFrame([customer.model_dump()])
        result = predict_customers(
            model=get_model(),
            dataframe=dataframe,
            threshold=get_prediction_threshold(),
        )
        row = result.iloc[0]

        return PredictionResponse(
            customer_id=(
                str(row["customer_id"])
                if "customer_id" in result.columns
                else None
            ),
            churn_probability=float(row["churn_probability"]),
            churn_prediction=int(row["churn_prediction"]),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/predict/batch")
async def predict_batch(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="The CSV file is empty.")

    try:
        dataframe = pd.read_csv(StringIO(content.decode("utf-8")))
        if dataframe.empty:
            raise HTTPException(status_code=400, detail="The CSV file is empty.")

        result = predict_customers(
            model=get_model(),
            dataframe=dataframe,
            threshold=get_prediction_threshold(),
        )

        output = StringIO()
        result.to_csv(output, index=False)
        output.seek(0)

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="predictions.csv"',
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc