# Credit Card Fraud Detection 

This project was developed as part of the AI Model Building and Development Bootcamp at Tuwaiq Academy.
The objective is to experiment with multiple machine learning models, evaluate their performance, and select the most effective model for deployment in a real-world fraud detection scenario.

## Dataset

**Title:** Credit Card Fraud Detection Dataset 2023  
**Source:** Kaggle dataset by nelgiriyewithana  
**Link:** ([https://www.kaggle.com/datasets/nelgiriyewithanacredit-card-fraud-detection-dataset-2023](https://www.kaggle.com/datasets/nelgiriyewithana/credit-card-fraud-detection-dataset-2023))  

**Main columns:**

- `id`: Transaction identifier.  
- `V1-V28`: Anonymized numerical features for privacy.  
- `Amount`: Transaction amount. 
- `Class`: Target label (0=legitimate, 1=fraudulent) – perfectly balanced at 284,315 each.

## Project Goals

This project aims to:

- Analyze feature distributions and correlations in anonymized transaction data.  
- Identify top predictive features using Random Forest importance scores.  
- Train and compare multiple classifiers (Logistic Regression, KNN, SVM, Random Forest, XGBoost).  
- Evaluate model performance with metrics like precision, recall, F1-score, and ROC-AUC.

## Key Insights

The dataset is perfectly balanced with 50% fraud (284,315 each), enabling robust model training without SMOTE.  
Top features by Random Forest importance include V14 (17.3%), V10 (15.2%), V12 (12.1%), and V4 (12.1%), capturing ~95% predictive power with 20 features.
XGBoost and Random Forest achieve near-perfect performance (F1 >0.999, ROC-AUC >0.999).

## Features

- EDA: Descriptive stats, class balance, null checks, correlation heatmap.  
- Feature selection: Top 20 features covering 95% importance.  
- Model comparison: 5 algorithms with timing and comprehensive metrics.  
- Visualizations: Distributions, heatmaps, feature importances.
- Streamlit: Interactive UI with predictions.
- FastAPI: Deployed the selected model as a production-ready inference endpoint for real-world fraud detection.
- Model Export: Best Random forest model pickled for deployment.

## Technology Stack

- Python  
- Pandas, NumPy for data manipulation  
- Matplotlib, Seaborn for visualization  
- Scikit-learn for preprocessing and models (Logistic Regression, KNN, SVM, Random Forest)  
- XGBoost for gradient boosting  
- Jupyter Notebook for analysis
- Streamlit for interactive user interface 
- FastAPI for model deployment

## Getting Started (Local)

### 1. Install Kaggle API (optional, for dataset download)

```bash
pip install kagglehub
```

### 2. Download dataset

Run the first cell in the notebook to download via KaggleHub:
```python
import kagglehub
path = kagglehub.dataset_download("nelgiriyewithanacredit-card-fraud-detection-dataset-2023")
```

### 3. Run the notebook

- Open `ml_project.ipynb` in Jupyter Notebook, JupyterLab, or VS Code.  
- Execute cells sequentially for full analysis, model training, and results.

## Using the Notebook

1. Load and inspect dataset (shape: 568,630 × 31).  
2. EDA: Stats, balance check (50/50), nulls/duplicates (0).  
3. Feature engineering: Scale Amount, select top 20 features.  
4. Train/test split (80/20), model training/comparison.  
5. View results table and visualizations.

