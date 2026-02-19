import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

def train():
    df = pd.read_csv("dataset.csv")

    X = df[["mass", "speed", "distance", "altitude"]]
    y = df["energy_kwh"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)

    print("MSE:", mse)

    joblib.dump(model, "energy_model.pkl")

if __name__ == "__main__":
    train()
