"""
08_predictive_machine_learning.py - Predictive Analysis using Machine Learning
Trains and evaluates Logistic Regression, SVM, Decision Tree, and KNN using 10-fold GridSearchCV.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report

os.makedirs('figures', exist_ok=True)

df2 = pd.read_csv('data/dataset_part_2.csv')
df3 = pd.read_csv('data/dataset_part_3.csv')

X = df3.copy()
Y = df2['Class'].to_numpy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)

models = {
    'Logistic Regression': (LogisticRegression(random_state=2), {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}),
    'SVM': (SVC(random_state=2), {'C': [0.5, 1.0, 1.5], 'kernel': ['linear', 'rbf', 'sigmoid']}),
    'Decision Tree': (DecisionTreeClassifier(random_state=2), {'criterion': ['gini', 'entropy'], 'max_depth': [2, 4, 6, 8], 'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 5, 10]}),
    'KNN': (KNeighborsClassifier(), {'n_neighbors': [3, 5, 7, 9, 10], 'p': [1, 2], 'algorithm': ['auto', 'ball_tree', 'kd_tree']})
}

for name, (mdl, params) in models.items():
    clf = GridSearchCV(mdl, params, cv=10)
    clf.fit(X_train, Y_train)
    train_acc = clf.best_score_
    test_acc = clf.score(X_test, Y_test)
    print(f"\n{name}:")
    print(f"  Best CV Train Accuracy: {train_acc:.4f}")
    print(f"  Holdout Test Accuracy:  {test_acc:.4f}")
    print(f"  Best Parameters:        {clf.best_params_}")
    
    if name == 'Logistic Regression':
        y_pred = clf.predict(X_test)
        cm = confusion_matrix(Y_test, y_pred)
        print("  Confusion Matrix:")
        print(cm)
        print("  Classification Report:")
        print(classification_report(Y_test, y_pred))

print("\nPredictive machine learning pipeline executed successfully.")
