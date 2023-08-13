import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess (filepath: str) -> tuple:
    data = pd.read_csv(filepath)

    data.drop(columns=["CustomerID", "Tenure", "Last Interaction"], inplace=True)
    data.dropna(inplace=True)

    data = pd.get_dummies(data, prefix=["gender"], columns=["Gender"], dtype=int)
    data = pd.get_dummies(data, prefix=["sub_type"], columns=["Subscription Type"], dtype=int)
    data = pd.get_dummies(data, prefix=["contract_len"], columns=["Contract Length"], dtype=int)

    X = data.drop(columns=["Churn"])
    Y = data["Churn"]

    X_columns = X.columns

    scaler = StandardScaler().fit(X)
    X = pd.DataFrame(data=scaler.transform(X), columns=X_columns)

    return (X,Y)