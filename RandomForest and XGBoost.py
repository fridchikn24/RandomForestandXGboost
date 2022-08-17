# -*- coding: utf-8 -*-
"""Sameeullah_File1_HW6

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cmiWcIP0YPa9hae1K8JnmoxNjPkHVlN1

# **HW6: Required Submissions:**
1.  Submit  colab/jupyter notebooks and pdf files.
2. For this HW, you will use XGBoost Regressiona and Random Forest regreesion on Bike Sharing Dataset.
3. You do not need to do EDA again. You can use the EDA from last HW. We are using the same datasets as in the last HW.
4. While choosing the pre-processing step, keep in mind the algorithm that you are using. .
2. Pdf version of the notebooks (HWs will not be graded if pdf version is not provided).
3. **The notebooks and pdf files should have the output.**
4. **Name files as follows : FirstName_file1_hw6, FirstName_file2_h6 **

# Question (10 Points) : XGBoost Regression and Random Forest regression on Bike Sharing Dataset

- Download the data from following link: https://archive.ics.uci.edu/ml/datasets/Seoul+Bike+Sharing+Demand'.

- Your goal is to predict the rented bike count.

-  Craete a separate pipeline for each algorithm. 

- Compare KNN (last HW), DecisonTree and Linear Regression, XgBoost, and Random Forest Regression. Basd on your anaysis which algorithm you will recommend.

- For XGBoost Notebook also provide a list and explanation of different hyperparameters availaible.
"""

import warnings
warnings.filterwarnings(action='once')

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install feature_engine

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install -U scikit-learn

import sklearn
import feature_engine

# Commented out IPython magic to ensure Python compatibility.
# For DataFrames and manipulations
import pandas as pd
import numpy as np
import scipy.stats as stats

# For data Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as po
import plotly.graph_objects as go

# %matplotlib inline
import plotly.io as pio
pio.renderers.default = 'colab'

# For splitting the dataset
from sklearn.model_selection import train_test_split

# drop arbitrary features
from sklearn.datasets import fetch_openml

# For categorical variables
from feature_engine.encoding import OneHotEncoder
from feature_engine.encoding import RareLabelEncoder
from feature_engine.encoding import DecisionTreeEncoder
from feature_engine.encoding import MeanEncoder

# For scaling the data
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

from feature_engine.transformation import YeoJohnsonTransformer
from feature_engine.transformation import LogTransformer

# DIscretization
from sklearn.preprocessing import KBinsDiscretizer

# Handling Outliers
from feature_engine.outliers import Winsorizer

# feature engine wrapper 
from feature_engine.wrappers import SklearnTransformerWrapper

# Using KNN classification for our data
from sklearn.neighbors import KNeighborsClassifier

# creating pipelines 
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Hyper parameter tuning
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold

# learning Curves
from sklearn.model_selection import learning_curve

# draws a confusion matrix
from sklearn.metrics import plot_confusion_matrix 
from scipy.stats import uniform, truncnorm, randint, loguniform


# save and load models
import joblib

# Pathlib to navigate file system
from pathlib import Path

from sklearn.neighbors import KNeighborsRegressor



#import os
#os.makedirs("/content/drive/MyDrive/teaching_fall_2021/ml_fall_2021/HW_Assignments/HW6/saved_models")
#!ls



from google.colab import drive
drive.mount('/content/drive')

save_model_folder  = Path('/content/drive/MyDrive/teaching_fall_2021/ml_fall_2021/HW_Assignments/HW6/saved_models')

# Load data from  https://archive.ics.uci.edu/ml/datasets/Seoul+Bike+Sharing+Demand'
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00560/SeoulBikeData.csv'
!wget {url} -P {'/content/drive/MyDrive/teaching_fall_2021/ml_fall_2021/HW_Assignments/HW6/'}

datafolder = Path('/content/drive/MyDrive/teaching_fall_2021/ml_fall_2021/HW_Assignments/HW6/')

bike_data = datafolder /'SeoulBikeData.csv'
#X, y = fetch_openml("credit-g", version=1, as_frame=True, return_X_y=True)

with open(bike_data, encoding="utf8",errors='ignore') as csv_file:
    df = pd.read_csv(csv_file)
df.head()

y = df.iloc[:,1]
print(y.head())
x=df.iloc[:,2:]
x.head()

def plot_learning_curve(estimator, title, X, y, axes=None, ylim=None, cv=None,
                        n_jobs=None, train_sizes=np.linspace(.2, 1.0, 5)):
    """
    Generate 2 plots: the test and training learning curve, the training
    samples vs fit times curve.

    Parameters
    ----------
    estimator : estimator instance
        An estimator instance implementing `fit` and `predict` methods which
        will be cloned for each validation.

    title : str
        Title for the chart.

    X : array-like of shape (n_samples, n_features)
        Training vector, where ``n_samples`` is the number of samples and
        ``n_features`` is the number of features.

    y : array-like of shape (n_samples) or (n_samples, n_features)
        Target relative to ``X`` for classification or regression;
        None for unsupervised learning.

    axes : array-like of shape (3,), default=None
        Axes to use for plotting the curves.

    ylim : tuple of shape (2,), default=None
        Defines minimum and maximum y-values plotted, e.g. (ymin, ymax).

    cv : int, cross-validation generator or an iterable, default=None
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:

          - None, to use the default 5-fold cross-validation,
          - integer, to specify the number of folds.
          - :term:`CV splitter`,
          - An iterable yielding (train, test) splits as arrays of indices.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : int or None, default=None
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.

    train_sizes : array-like of shape (n_ticks,)
        Relative or absolute numbers of training examples that will be used to
        generate the learning curve. If the ``dtype`` is float, it is regarded
        as a fraction of the maximum size of the training set (that is
        determined by the selected validation method), i.e. it has to be within
        (0, 1]. Otherwise it is interpreted as absolute sizes of the training
        sets. Note that for classification the number of samples usually have
        to be big enough to contain at least one sample from each class.
        (default: np.linspace(0.1, 1.0, 5))
    """
    if axes is None:
        _, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].set_title(title)
    if ylim is not None:
        axes[0].set_ylim(*ylim)
    axes[0].set_xlabel("Training examples")
    axes[0].set_ylabel("Score")

    train_sizes, train_scores, test_scores, fit_times, _ = \
        learning_curve(estimator, X, y, cv=cv, n_jobs=n_jobs,
                       train_sizes=train_sizes,
                       return_times=True,
                       random_state=123)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    fit_times_mean = np.mean(fit_times, axis=1)
    fit_times_std = np.std(fit_times, axis=1)

    # Plot learning curve
    axes[0].grid()
    axes[0].fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
    axes[0].fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1,
                         color="g")
    axes[0].plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
    axes[0].plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")
    axes[0].legend(loc="best")

    # Plot n_samples vs fit_times
    axes[1].grid()
    axes[1].plot(train_sizes, fit_times_mean, 'o-')
    axes[1].fill_between(train_sizes, fit_times_mean - fit_times_std,
                         fit_times_mean + fit_times_std, alpha=0.1)
    axes[1].set_xlabel("Training examples")
    axes[1].set_ylabel("fit_times")
    axes[1].set_title("Scalability of the model")

    return plt

print(x.dtypes)

# Create a list of categorical variables
# Since the dtype of categorical variable is Object we can compare the values with 'O' 
categorical = [var for var in x.columns if x[var].dtype.name == 'object']

# Create a list of discrete variables
# we do not want to consider Exited as this is target variable
discrete = [
    var for var in x.columns if x[var].dtype.name != 'object'
    and len(x[var].unique()) < 20
]

# Create a list of continuous Variables
continuous = [
    var for var in x.columns if x[var].dtype.name != 'object'
    if var not in discrete
]

print(categorical)
print(discrete)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=123,stratify =x[['Functioning Day','Holiday']])
x_train.head()

#ohe = OneHotEncoder(variables=categorical,drop_last = True,ignore_format= True)
#x_train = ohe.fit_transform(x_train)
print(x_train)

bikepipeline = Pipeline([
            #('rare labels', RareLabelEncoder(tol=.05,n_categories =2,variables = ['Holiday','Functioning Day'])),
            #('log_transform',LogTransformer(variables=continuous)), 
            ('one_hot_encoder', OneHotEncoder(variables=categorical
                   ,drop_last= True, ignore_format=True)),
            ('scalar', SklearnTransformerWrapper(StandardScaler(), variables = continuous)),
            ('knn_reg',KNeighborsRegressor())       
])

param_grid_1 = {
    'scalar__transformer': [StandardScaler()],
    'knn_reg__n_neighbors': range(2,20,2),
    'knn_reg__weights': ['uniform', 'distance'],
    'knn_reg__p': [1, 2],
    'knn_reg__n_jobs':[-1]
}

grid_knn_1 = GridSearchCV(bikepipeline, param_grid_1,cv=5,return_train_score= True)

grid_knn_1.fit(x_train,y_train)

grid_knn_1.best_params_

# Here  save_model_folder is folder where I have saved models. Change that to appropriate location. 
# This variable is defined in section Mount Google Drive, Import Data

# specify the file to save the best estimator
file_best_estimator_round1 = save_model_folder / 'knn_reg_round1_best_estimator.pkl'

# specify the file to save complete grid results
file_complete_grid_round1 = save_model_folder / 'knn_reg_round1_complete_grid.pkl'

# save the best estimator
joblib.dump(grid_knn_1.best_estimator_, file_best_estimator_round1)

# save complete grid results
joblib.dump(grid_knn_1, file_complete_grid_round1)

# load  the best estimator
loaded_best_estimator_round1 = joblib.load(file_best_estimator_round1)

# load complete grid results
loaded_complete_grid_round1 = joblib.load(file_complete_grid_round1)

# plot learning curves
# Notice that we are using the best estimator
plot_learning_curve(loaded_best_estimator_round1, 'Learning Curves KNN', x_train, y_train, n_jobs=-1)

print(loaded_best_estimator_round1.score(x_train,y_train))

print(loaded_complete_grid_round1.best_score_)

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from feature_engine.encoding import DecisionTreeEncoder
from sklearn.tree import DecisionTreeClassifier

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=123, stratify =x[['Functioning Day','Holiday']])
print(X_train)

churn_pipeline_dtree = Pipeline([
    ('one_hot_encoder',
      OneHotEncoder(variables=categorical,drop_last=True)),

    ('dtree',
     DecisionTreeClassifier(random_state=0))
])

param_grid__tree_1 = {
    'dtree__max_depth': np.arange(4,20),
    'dtree__min_samples_leaf': np.arange(2,20,4)
    #'dtree__max_leaf_nodes': np.arange(4, 20)
     }

grid_dtree1 = GridSearchCV(churn_pipeline_dtree, param_grid__tree_1,
                           cv=5, return_train_score= True, n_jobs=-1)
grid_dtree1.fit(X_train,y_train)

print(grid_dtree1.best_params_)

file_params_tree1 = save_model_folder / 'dtree_round1_params.pkl'
file_model_tree1 = save_model_folder / 'dtree_round1_model.pkl'

joblib.dump(grid_dtree1.best_estimator_, file_params_tree1)
joblib.dump(grid_dtree1, file_model_tree1)

loaded_dtree_params_round1 = joblib.load(file_params_tree1)
loaded_dtree_model_round1 = joblib.load(file_model_tree1)

plot_learning_curve(loaded_dtree_params_round1, 'Learning Curves dtree', X_train, y_train, n_jobs=-1)

#let's check the train scores
print(loaded_dtree_model_round1.score(X_train,y_train))

#let's check the cross validation score
print(loaded_dtree_model_round1.best_score_)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=123)#, stratify =x[['Functioning Day','Holiday']])
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing  import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet

#cd = categorical + continuous
#print(cd)
pipeline_lin = Pipeline([
    
    ('one_hot_encoder',
      OneHotEncoder(variables=categorical,drop_last=True)),

    ('scalar',
      SklearnTransformerWrapper(StandardScaler(), variables = continuous)),

    ('linreg',
     LinearRegression())
])
#np.logspace(-4, -1, 10)

np.linspace(0,1, 5)
param_grid_lin1 = {
    'scalar__transformer': [StandardScaler(), MinMaxScaler()],
    #'logreg__l1_ratio': np.linspace(0, 1, 5)
    }
grid_linreg_1 = GridSearchCV(pipeline_lin, param_grid_lin1,
                           cv=5, return_train_score= True, n_jobs=-1 )
grid_linreg_1.fit(X_train,y_train)

grid_linreg_1.best_params_

file_params_lin1 = save_model_folder / 'linreg_round1_params.pkl'
file_model_lin1 = save_model_folder / 'linreg_round1_model.pkl'

joblib.dump(grid_linreg_1.best_estimator_, file_params_lin1)
joblib.dump(grid_linreg_1, file_model_lin1)

loaded_linreg_params_lin1 = joblib.load(file_params_lin1)
loaded_linreg_model_lin1 = joblib.load(file_model_lin1)

plot_learning_curve(loaded_linreg_params_lin1 , 'Learning Curves linreg', X_train, y_train, n_jobs=-1)

#let's check the train scores
print(loaded_linreg_model_lin1.score(X_train,y_train))

#let's check the cross validation score
print(loaded_linreg_model_lin1.best_score_)

print(f'Test data accauracy for lin reg : {loaded_linreg_params_lin1.score(X_test,y_test)}')

print(f'Test data accauracy for decision tree : {loaded_dtree_params_round1.score(X_test,y_test)}')

pip install xgboost

churn_pipeline = Pipeline([
                   
('one_hot_encoder',
      OneHotEncoder(variables=categorical,drop_last=True))])

X_train=OneHotEncoder(variables=categorical, drop_last=True).fit_transform(X_train) 
X_test = OneHotEncoder(variables=categorical, drop_last=True).fit_transform(X_test)

from  xgboost import XGBRegressor

xgbc= XGBRegressor(random_state=123,early_stopping_rounds=2)
xgbc_param = {
              'max_depth' : [6],
              'n_estimators' : [100],
              'learning_rate' : [0.6],
               'min_child_weight' : [1],
                'subsample':[1]
             }
xgbc_grid = GridSearchCV(xgbc, xgbc_param,cv=5, return_train_score=True, )
xgbc_grid.fit(X_train,y_train)

print(f'Best Mean Cross Validation Score is {xgbc_grid.best_score_}')
print(f'Best Mean Cross Validation Score is {xgbc_grid.best_params_}')
print(f'Train score is {xgbc_grid.score(X_train,y_train)}')
#print(f'Test score is {xgbc_grid.score(X_test,y_test)}')
#print(f'Val score is {xgbc_grid.score(X_val,y_val)}')

file_params_roundxg = save_model_folder / 'xg_params.pkl'
file_model_roundxg = save_model_folder / 'xg_model.pkl'

joblib.dump(xgbc_grid.best_estimator_, file_params_roundxg)
joblib.dump(xgbc_grid, file_model_roundxg)

loaded_xg_params = joblib.load(file_params_roundxg)
loaded_xg_model = joblib.load(file_model_roundxg)

plot_learning_curve(loaded_xg_params, 'Learning Curves dtree', X_train, y_train)

#let's check the train scores
print(loaded_xg_model.score(X_train,y_train))

#let's check the cross validation score
print(loaded_xg_model.best_score_)

#let's check the test scores for final model
print(f'Test data accauracy for xg: {loaded_xg_model.score(X_test,y_test)}')

# define model
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestRegressor



model= Pipeline([
  
 
     ('rf',
       RandomForestRegressor(warm_start=True, random_state=0, oob_score=True))])
param_grid = {
    
    'rf__n_estimators': [200],
    'rf__max_features': ['sqrt', 'log2'],
    'rf__max_depth': np.arange(2,10),
    'rf__criterion' :['squared_error'],
    #'rf__min_samples_leaf': np.arange(2,10),
    #'rf__max_leaf_nodes': np.arange(2, 10),
}

# define evaluation procedure
#cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)


grid_randomforest= GridSearchCV(model, param_grid, cv=5, n_jobs=-1)
grid_randomforest.fit(X_train, y_train)

grid_randomforest.best_params_

file_params_roundrf = save_model_folder / 'rf_round1_params.pkl'
file_model_roundrf = save_model_folder / 'rf_round1_model.pkl'

joblib.dump(grid_randomforest.best_estimator_, file_params_roundrf)
joblib.dump(grid_randomforest, file_model_roundrf)

loaded_rf_params = joblib.load(file_params_roundrf)
loaded_rf_model = joblib.load(file_model_roundrf)

plot_learning_curve(loaded_rf_params, 'Learning Curves dtree', X_train, y_train)

#let's check the train scores
print(loaded_rf_model.score(X_train,y_train))

#let's check the cross validation score
print(loaded_rf_model.best_score_)

#let's check the test scores for final model
print(f'Test data accauracy for rf: {loaded_rf_model.score(X_test,y_test)}')

"""Based on analysis, the learning and scaling curves, I conclude that Random Forest is the most accurate model. However, there is an overfitting issue and it does not scale well. For slightly less overfitting but a more scalable model, xgboost might be more effective."""

!wget -nc https://raw.githubusercontent.com/brpy/colab-pdf/master/colab_pdf.py
from colab_pdf import colab_pdf
colab_pdf('Sameeullah_File1_HW6.ipynb')