# 🛡️ Network Security – Phishing URL Detection

A machine learning–powered phishing website detection system with a full end-to-end pipeline:

- Automated data ingestion, validation, transformation, training  
- Artifact tracking (every training run is saved with timestamps)  
- Model deployment using Docker + AWS + GitHub Actions (CI/CD)  
- Simple web app to check if a URL is phishing or legitimate  

---

## 🚀 Features
- 🔄 Modular ML pipeline (ingestion → validation → transformation → training)  
- 📦 Artifacts saved for every run (datasets, reports, models, transformers)  
- ✅ Data validation with schema checks & drift detection  
- 📊 MLflow tracking for experiments  
- 🐳 Dockerized deployment (AWS ECR + ECS/self-hosted runner)  
- 🌐 Flask/FastAPI app with web UI + API endpoints  
- ☁️ AWS S3 sync support for data & models  
- 🗄️ MongoDB integration for storing predictions/data  

---
<img width="1602" height="757" alt="image" src="https://github.com/user-attachments/assets/7c3c3e15-3df6-4442-a7c0-ccede3fd273d" />

<img width="1606" height="756" alt="image" src="https://github.com/user-attachments/assets/274a9f19-98c8-4a6f-a677-4768cf82167f" />


## 🏗️ Project Structure
```bash
networksecurity/
│── components/             # Core ML pipeline components
│   │── data_ingestion.py
│   │── data_validation.py
│   │── data_transformation.py
│   │── model_trainer.py
│   │── model_evaluation.py
│
│── pipeline/               # Orchestration of training & prediction pipelines
│   │── training_pipeline.py
│   │── prediction_pipeline.py
│
│── entity/                 # Config and artifact entity definitions
│   │── config_entity.py
│   │── artifact_entity.py
│
│── utils/                  # Helper utilities (ML + general)
│   │── __init__.py
│   │── common.py
│
│── cloud/                  # AWS / cloud syncer
│   │── s3_syncer.py
│
│── exception/              # Custom exceptions
│   │── exception.py
│
│── logging/                # Central logging module
│   │── logger.py
│
│── tests/                  # Unit & integration tests
│   │── test_ingestion.py
│   │── test_transformation.py
│   │── test_training.py
│
│── notebooks/              # Jupyter notebooks for EDA & experiments
│   │── 01_data_exploration.ipynb
│   │── 02_model_baseline.ipynb
│   │── 03_feature_engineering.ipynb
│
│── configs/                # YAML/JSON config files
│   │── schema.yaml
│   │── model_config.yaml
│
│── scripts/                # Handy shell/python scripts
│   │── run_pipeline.sh
│   │── deploy.sh
│
│── .github/workflows/      # CI/CD workflows (GitHub Actions)
│   │── ci-cd.yml
│
│── templates/              # Web UI (HTML templates)
│   │── home.html
│   │── result.html
│
│── Artifacts/              # Timestamped training outputs
│── final_model/            # Production-ready model + preprocessor
│── prediction_output/      # Predictions on new data
│
│── requirements.txt        # Project dependencies
│── Dockerfile              # Container definition
│── docker-compose.yml      # Multi-container setup (optional)
│── setup.py                # Installable package setup
│── app.py                  # Web app entry point (Flask/FastAPI)
│── main.py                 # Training entry point
│── README.md               # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ShubhamJadhav03/networksecurity.git
cd networksecurity
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Training Pipeline
```bash
python main.py
```
This will:
- Ingest and validate dataset (`Network_Data/phisingData.csv`)  
- Transform data and save preprocessing pipeline  
- Train ML model and save it into `final_model/`  

### 4. Run Web Application
```bash
python app.py
```
Then open your browser at [http://localhost:8080](http://localhost:8080) to test URLs.

---

## 🐳 Docker Deployment
```bash
docker build -t networksecurity .
docker run -p 8080:8080 networksecurity
```

---

## 🔄 CI/CD (GitHub Actions + AWS)
On push to `main` branch:
- Runs integration checks  
- Builds Docker image & pushes to AWS ECR  
- Deploys updated container on server (self-hosted runner / ECS)  

---

## 📊 Artifacts & Logs
- `Artifacts/` → Saved datasets, transformed data, preprocessing objects, trained models  
- `logs/` → Timestamped training logs  
- `mlflow.db` → MLflow experiment tracking database  

---

## 🛠️ Tech Stack
- **Python 3.10+**  
- Pandas, NumPy, Scikit-learn (ML pipeline)  
- FastAPI (web app & API)  
- MongoDB (storage)  
- Docker (containerization)  
- AWS (ECR, S3, ECS) (deployment & storage)  
- GitHub Actions (CI/CD)  

---

## 📌 To-Do / Future Improvements
- [ ] Add unit tests for components  
- [ ] Improve web UI for predictions  
- [ ] Add explainability (SHAP/LIME)  
- [ ] Automate dataset updates from phishing feeds  
- [ ] Add monitoring for false positives/negatives  
