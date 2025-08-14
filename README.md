# Convolutional Neural Network for Image Classification

A deep learning project implementing a Convolutional Neural Network (CNN) for multi-class image classification. The model is designed with optimised architecture, data augmentation, and training callbacks to achieve high accuracy and generalisation.

---

## Overview
This project forms **Part A of the DELE CA1 assignment** and focuses on building a robust CNN for image classification tasks. It leverages convolutional layers for feature extraction, pooling layers for dimensionality reduction, and fully connected layers for classification.

---

## Tech Stack
- **Python**
- **TensorFlow / Keras** – Deep learning model creation and training
- **NumPy**, **pandas** – Data handling
- **Matplotlib**, **Seaborn** – Visualisation

---

## Features
- Data preprocessing and normalisation
- Data augmentation to improve generalisation
- CNN architecture with convolutional, pooling, and dense layers
- Use of callbacks including:
  - **ReduceLROnPlateau** for dynamic learning rate adjustment
  - **EarlyStopping** for preventing overfitting
- Evaluation of training/validation accuracy and loss

---

## Model Performance
- **Validation Accuracy:** ~88.0%
- **Validation Loss:** ~0.58
- Trained over **100 epochs** with learning rate scheduling
