import json
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import dotenv_values
from fastapi.encoders import jsonable_encoder
from sklearn.ensemble import AdaBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor

config = dotenv_values(".env")

with open("src/ml_models/trained_adaboost.pkl", "rb") as file:
    shark_probability_model = pickle.load(file)


def _check_and_add(name, values, data):
    for val in sorted(values):
        if name.lower() == val.lower():
            data.append(True)
        else:
            data.append(False)


def predict_shark_attack_probability_value(new_data_standard_format):
    """
    Predict shark attack probability for new data
    """
    data_transformed = _preprocess_new_data(new_data_standard_format)
    data_transformed_array = np.array(data_transformed).reshape(1, -1)
    return str(shark_probability_model.predict(data_transformed_array)[0])


def _preprocess_new_data(new_data_standard_format):
    """
    Preprocess new data for prediction
    """
    data_for_prediction = []
    for key in json.loads(config["schema_order"]):
        _check_and_add(
            new_data_standard_format[key],
            sorted(json.loads(config[key])),
            data_for_prediction,
        )

    return data_for_prediction


class SharkAttackRatePredictor:
    def __init__(
        self, model_type="adaboost", estimators=100, learning_rate=0.1, max_depth=3
    ):
        if model_type == "adaboost":
            self.model = AdaBoostRegressor(
                n_estimators=estimators,
                learning_rate=learning_rate,
                random_state=42,
                estimator=DecisionTreeRegressor(max_depth=max_depth),
            )
        elif model_type == "linear":
            self.model = LinearRegression()
        else:
            raise ValueError("model_type must be 'adaboost' or 'linear'")

        self.feature_names = None

    def fit(self, X, y):
        """
        Fit model on prepared data
        """
        self.model.fit(X, y)
        self.feature_names = X.columns
        return self

    def predict(self, new_data):
        """
        Make predictions for new data
        """
        return self.model.predict(new_data)

    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        """
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        return {"mse": mse, "rmse": np.sqrt(mse), "r2": r2, "mae": mae}

    def plot_feature_importance(self):
        """
        Plot feature importance (for AdaBoost)
        """
        if isinstance(self.model, AdaBoostRegressor):
            importance = pd.DataFrame(
                {
                    "feature": self.feature_names,
                    "importance": self.model.feature_importances_,
                }
            )
            importance = importance.sort_values("importance", ascending=False)

            plt.figure(figsize=(10, 6))
            plt.bar(importance["feature"][:15], importance["importance"][:15])
            plt.xticks(rotation=45, ha="right")
            plt.title("Feature Importance")
            plt.tight_layout()
            plt.show()
