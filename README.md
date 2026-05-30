# Satellite Imagery–Based Property Valuation

A multimodal real estate valuation system that predicts property prices by combining structured housing attributes with visual features derived from satellite imagery.

This project investigates whether environmental context, such as **green cover, road density, and waterfront proximity**—extracted from satellite images can improve traditional property valuation models beyond standard tabular data (e.g., square footage, number of rooms).

---

## 📌 Project Overview

Real estate valuation is traditionally treated as a structured data problem. However, property prices are heavily influenced by qualitative environmental factors that are often missing from spreadsheets.

This project implements a complete multimodal pipeline that:
* **Programmatically fetches** satellite images using geographic coordinates (Latitude/Longitude).
* **Extracts visual features** using a pretrained Convolutional Neural Network (CNN) as a feature extractor.
* **Fuses visual embeddings** with tabular housing data into a unified feature vector.
* **Predicts property values** and evaluates the performance gain provided by the inclusion of visual context.

---

## 📂 Directory Structure

```text
SatelliteImagery/
├── data/
│   ├── raw/                       # Original datasets (train.csv, test.csv)
│   ├── processed/                 # Cleaned tabular data & generated embeddings
│   │   ├── train_tabular.csv
│   │   ├── train_image_embeddings.npy
│   │   └── train_image_ids.npy
│   └── images/                    # Downloaded satellite tiles
│       ├── train/
│       └── test/
├── results/                       # Predictions and final documentation
│   ├── 24115144_final.csv
│   └── 24115144_report.pdf
├── data_fetcher.py                # Script to download images via API
├── preprocessing.ipynb            # Data cleaning and image augmentation
├── model_training.ipynb           # Model architecture, fusion, and training
├── run_fetch_train.py             # Main execution script for the pipeline
├── test_fetch.py                  # Unit test for API connectivity
├── requirements.txt               # Project dependencies
├── .gitignore                     # Files to exclude (images, .env, etc.)
├── .env                           # API keys and environment variables
└── README.md                      # Project documentation
```
---
## 📊 Dataset Description
 
### Tabular Data
* **Source:** King County House Sales Dataset
* **Target Variable:** `price` (Log-transformed during training to stabilize variance)
* **Key Features:**
    * **Internal:** Bedrooms, bathrooms, living area (`sqft_living`).
    * **External:** Lot size (`sqft_lot`), construction grade, and condition.
    * **Spatial:** Geographic coordinates (latitude, longitude).
    * **Contextual:** Neighborhood context (`sqft_living15`, `sqft_lot15`).

### Image Data
* **Retrieval:** One satellite image per property fetched via **Mapbox Static Images API**.
* **Mapping:** Linked to tabular data using geographic coordinates.
* **Resolution:** Specifically tuned to capture both property-level detail and immediate neighborhood context.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/soham-uni/SatelliteImagery.git](https://github.com/soham-uni/SatelliteImagery.git
cd SatelliteImagery
```
### 2. Create Environment and Install Dependencies
```bash
conda create -n satval python=3.10
conda activate satval
pip install -r requirements.txt
```
### 3. Configure API Key
> Create a .env file in the project root:
```bash
MAPBOX_TOKEN=your_mapbox_api_key_here
```
## 🛠️ Pipeline Execution
Satellite Image Acquisition
To fetch satellite images for properties or test connectivity:

```bash
# Fetch training property images
python run_fetch_train.py

# Test API connectivity and single image retrieval
python test_fetch.py
```
> Downloaded images are stored in data/images/train/ and data/images/test/.

---

## ⚙️ Data Preprocessing

Execute `preprocessing.ipynb` to perform the following pipeline steps:

* **Data Cleaning & Validation:** Handling missing values and ensuring geographic coordinate bounds are accurate for API calls.
* **Target Scaling:** Log transformation of the price variable to normalize the distribution.
* **Feature Engineering:** Selection of key predictors and creation of derived housing metrics.
* **Data Alignment:** Generating mapping files to ensure a 1:1 correspondence between Image IDs and tabular data rows.

---

## 🤖 Model Training and Evaluation

The project experiments are contained within `model_training.ipynb`:

1.  **Tabular Baseline:** Training a Random Forest Regressor using only structured housing data.
2.  **Vision Feature Extraction:** Utilizing a pretrained **ResNet-18** (ImageNet weights) to generate visual embeddings from satellite tiles.
3.  **Multimodal Fusion:** Concatenating visual embeddings with tabular features for a unified prediction model.

### 📈 Results

| Model | RMSE (log-price) | R² Score |
| :--- | :--- | :--- |
| **Tabular Random Forest** | **0.1787** | **0.8843** |
| Multimodal Random Forest | 0.1822 | 0.8727 |

> **Final Submission Choice:** The **Tabular Random Forest** was selected as the final model. Although the multimodal approach was successfully implemented, it did not outperform the tabular baseline on this specific dataset.

---

## 📤 Submission Files

* **Prediction CSV:** `results/24115144_final.csv`
    * *Format:* `id, predicted_price`
* **Final Report:** `results/24115144_report.pdf` (Comprehensive project documentation and analysis).

---

## 🔍 Key Observations & Future Work

### Why didn't the images improve the score?
* **Strong Proxies:** Features like `zipcode` and `sqft_living15` already encode high-quality information about neighborhood affluence and density.
* **Marginal Gains:** While satellite imagery captures greenery and road access, these are often already reflected in the "Grade" and "Condition" columns of the King County dataset.
* **Context vs. Detail:** Standard satellite tiles may lack the resolution to distinguish specific property upgrades (e.g., interior renovations) that significantly impact the price.  

### Future Opportunities
* **Data Sparsity:** Multimodal pipelines will likely show higher utility in regions where structured real estate data is unreliable or unavailable.
* **Fine-tuning:** Unfreezing CNN layers to train specifically on urban morphology rather than general ImageNet features.
* **Multi-scale Inputs:** Feeding the model both a "close-up" property view and a "wide-angle" neighborhood view.

---

**Author:** Soham Adak
