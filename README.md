<div align="center">

# 🔗 SafeLink — Phishing URL Detection (MLOps)

**An end-to-end Machine Learning system that detects phishing websites from URL features — served through a FastAPI web app and deployed to AWS with a full CI/CD pipeline.**

[![Python](img.shields.io/badge/…/www.python.org)
[![FastAPI](img.shields.io/badge/FastAPI-Serving-009688.svg)](https:/fastapi.tiangolo.com)
[![MLflow](img.shields.io/badge/…/mlflow.org)
[![AWS](img.shields.io/badge/…/aws.amazon.com)
[![Docker](img.shields.io/badge/…/www.docker.com)

</div>

---

## 📖 Overview

**SafeLink** is a production-style **MLOps** project that trains a machine-learning model to identify **phishing websites** from a set of URL and website features. It goes far beyond a notebook model — it implements a fully modular, reproducible ML pipeline and ships the trained model as a live prediction service.

Given a CSV of website features, SafeLink predicts whether each entry is **safe (legitimate)** or a **phishing attempt**, and returns the results as a clean HTML table.

---

## ✨ Key Features

- 🧩 **Modular training pipeline** — clearly separated components for ingestion, validation, transformation, and training.
- 🗄️ **Data ingestion from MongoDB** into a local feature store, with automatic train/test split.
- ✅ **Data validation** — schema checks, numerical-column checks, and **dataset drift detection** using the Kolmogorov–Smirnov test, with a YAML drift report.
- 🔧 **Data transformation** — KNN-based imputation pipeline persisted as a reusable preprocessor.
- 🤖 **Multi-model training** — Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, and AdaBoost with hyperparameter search and automatic best-model selection.
- 📊 **Experiment tracking** with **MLflow on DagsHub** (F1, precision, recall + model logging).
- ☁️ **Cloud artifact sync** — training artifacts and the final model pushed to **AWS S3**.
- 🚀 **FastAPI serving** with `/train` and `/predict` endpoints, HTML result rendering, and Swagger docs.
- 🐳 **Containerized** with Docker and deployed via **GitHub Actions → AWS ECR → EC2**.
- 🧾 **Custom logging** and a **custom exception** class used consistently across the codebase.

---

## 🛠️ Tech Stack

| Category | Tools |
| --- | --- |
| **Language** | Python 3.10+ |
| **ML / Data** | scikit-learn, pandas, numpy, scipy |
| **Database** | MongoDB |
| **Serving** | FastAPI, Uvicorn, Jinja2 |
| **Experiment Tracking** | MLflow, DagsHub |
| **Cloud** | AWS S3, ECR, EC2 |
| **DevOps** | Docker, GitHub Actions |

---

## 🧭 How It Works

```
MongoDB
   │
   ▼
Data Ingestion ──► Data Validation ──► Data Transformation ──► Model Trainer ──► (S3 Sync)
   │                     │                      │                     │
DataIngestion       DataValidation      DataTransformation      ModelTrainer
   Artifact            Artifact              Artifact              Artifact
                                                                     │
                                                                     ▼
                                                       final_model/{model,preprocessor}.pkl
                                                                     │
                                                                     ▼
                                          FastAPI Serving  ──►  Docker  ──►  ECR  ──►  EC2

Serving (app.py)
   • GET  /train    → runs the full training pipeline
   • POST /predict  → CSV upload → preprocessor + model → HTML table + output.csv
```

1. **Data Ingestion** — reads the phishing dataset from a MongoDB collection, saves it to a feature store, and splits it into `train.csv` / `test.csv`.
2. **Data Validation** — validates the column count and numerical columns against `schema.yaml`, and runs a **KS-test drift check** between train and test, writing `report.yaml`.
3. **Data Transformation** — builds a **KNNImputer** pipeline, transforms data into numpy arrays, and persists `preprocessor.pkl`.
4. **Model Training** — trains 5 classifiers with hyperparameter search, selects the best model by score, logs metrics/models to **MLflow (DagsHub)**, and saves `final_model/model.pkl`.
5. **Cloud Sync** — pushes timestamped `Artifacts/` and the final model to **AWS S3**.
6. **Serving** — FastAPI exposes `/train` and `/predict`; predictions are rendered as an HTML table and saved to `prediction_output/output.csv`.

---

## 📁 Project Structure

```
safelink_mlops/
├── app.py                          # FastAPI app: / , /train and /predict endpoints
├── main.py                         # Run the full training pipeline directly
├── push_data.py                    # Push CSV data into MongoDB
├── requirements.txt                # Python dependencies
├── setup.py                        # Package definition (SafeLink)
├── Dockerfile                      # Container build (python:3.11-slim)
├── pytest.ini                      # Test configuration
├── .github/workflows/
│   ├── main.yml                    # CI: build & push image to AWS ECR
│   └── cd.yml                      # CD: deploy container on self-hosted EC2 runner
├── data_schema/
│   └── schema.yaml                 # Expected columns / schema for validation
├── templates/
│   ├── index.html                  # Upload page
│   └── table.html                  # HTML template for prediction output
├── final_model/
│   ├── model.pkl                   # Trained model
│   └── preprocessor.pkl            # Fitted preprocessing pipeline
├── Network_Data/
│   └── phisingData.csv             # Source dataset
├── prediction_output/output.csv    # Batch prediction results
├── tests/                          # Unit tests (pytest)
└── safelink/                       # Main package
    ├── components/                 # data_ingestion, data_validation,
    │                               # data_transformation, model_trainer
    ├── pipeline/                   # training_pipeline, batch_prediction
    ├── entity/                     # config_entity, artifact_entity
    ├── constant/training_pipeline/ # paths, DB names, bucket, params
    ├── utils/                      # I/O helpers, metrics, model estimator
    ├── cloud/s3_syncer.py          # Sync folders to/from AWS S3
    ├── exception/exception.py      # Custom SafeLinkException
    └── logging/logger.py           # Logging configuration
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- A MongoDB instance (Atlas or local) with the phishing dataset loaded
- *(Optional)* AWS account for S3/ECR/EC2, and a DagsHub account for MLflow

### Steps

```bash
# 1. Clone the repository
git clone github.com/Ankit-Singh-12/safelink_mlops.git
cd safelink_mlops

# 2. Create & activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .

# 4. Create a .env file with your MongoDB connection string
#    MONGODB_URL_KEY=<your_mongo_connection_string>
#    MONGO_DB_URL=<your_mongo_connection_string>

# 5. (Optional) Load data into MongoDB
python push_data.py

# 6. Run the training pipeline
python main.py

# 7. Start the API server
python app.py
```

The API will be available at **`localhost`** (Swagger docs at **`/docs`**).

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Upload page for prediction |
| `GET` | `/train` | Runs the full training pipeline |
| `POST` | `/predict` | Upload a CSV → returns predictions as an HTML table |
| `GET` | `/docs` | Interactive Swagger documentation |

---

## 🐳 Docker

```bash
# Build the image
docker build -t safelink .

# Run the container
docker run -d -p 8080:8000 \
  -e AWS_ACCESS_KEY_ID=... \
  -e AWS_SECRET_ACCESS_KEY=... \
  -e AWS_REGION=us-east-1 \
  --name safelink safelink
```

App will be reachable at **`localhost`**.

---

## ⚙️ CI/CD (GitHub Actions → AWS)

- **`main.yml` — Continuous Integration & Delivery:** checkout → install deps → run `pytest` → configure AWS credentials → log in to **ECR** → build & push the Docker image.
- **`cd.yml` — Continuous Deployment:** on a **self-hosted EC2 runner**, pulls the latest image from ECR and runs the container, exposing it on port `8080`.

---

## 🧪 Testing

```bash
pytest
```

Unit tests live in the `tests/` directory and cover the exception class, classification metrics, the model estimator, batch prediction, and utility helpers.

---