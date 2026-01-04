# Satellite Imagery–Based Property Valuation

This project develops a **multimodal regression pipeline** to predict residential property prices by combining traditional tabular housing attributes with **satellite imagery–derived visual features**. The goal is to enhance property valuation by incorporating environmental and neighborhood context such as greenery, density, and surrounding infrastructure.

---

## Project Overview

- **Objective:** Predict property prices using both numerical housing data and satellite images.
- **Approach:**  
  - Clean and preprocess tabular housing data  
  - Engineer meaningful ratio-based features  
  - Programmatically fetch satellite images using geographic coordinates  
  - Extract visual embeddings from images using a pretrained CNN  
  - Train and evaluate regression models  
- **Baseline:** Tabular-only Random Forest regression  
- **Extension:** Multimodal learning using tabular + image features

---

## Dataset

### Tabular Data
- Source: King County House Sales dataset
- Key features include:
  - `bedrooms`, `bathrooms`
  - `sqft_living`, `sqft_lot`
  - `sqft_living15`, `sqft_lot15`
  - `lat`, `long`
  - `condition`, `grade`, `view`, `waterfront`
- Target variable: `price`

### Visual Data
- Satellite images fetched using latitude and longitude
- Data source: **Copernicus Sentinel-2 (via Sentinel Hub)**
- Images stored separately for train and test splits

> Note: Images are downloaded dynamically and are **not included** in the repository.

---

## Feature Engineering

- Median imputation for missing numeric values
- Log transformation of the target variable (training only)
- Ratio-based engineered features:
  - **House Density Ratio:** `sqft_living / sqft_living15`
  - **Lot Density Ratio:** `sqft_lot / sqft_lot15`
  - **Basement Ratio:** `sqft_basement / sqft_living`

---

## Image Processing

- Satellite images are resized and normalized
- Pretrained **ResNet-18** is used as a feature extractor
- High-dimensional image embeddings are saved and later fused with tabular features

---

## Model Training

### Tabular Model (Baseline)
- Algorithm: Random Forest Regressor
- Validation metrics:
  - **RMSE**
  - **R² Score**

### Multimodal Model
- Combines tabular features with CNN-extracted image features
- Designed to capture both structural and visual context

---

## Results (Summary)

| Model Type | RMSE ↓ | R² ↑ |
|----------|-------|------|
| Tabular Only | ~130K | ~0.86 |
| Tabular + Images | Improved | Improved |

Satellite imagery provides additional contextual information, leading to improved predictive performance.

---

