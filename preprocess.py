import pandas as pd
from sklearn.preprocessing import StandardScaler

## \brief Функция предобработки данных
## \authors ivan-dev-lab
## \version 1.0.2
## \date 24.08.2023
## \param[in] filepath путь до необработанных данных 
## \param[in] data_type Определение типа данных для функции. От параметра зависит - будет ли функция возвращать целевую переменную ( data_type="train" ) или только признаки ( data_type="test" )
## \details Т.к столбцы Gender, Subscription Type и Contract Length содержат категориальные значение, то было принято решение использовать pd.get_dummies для этиъ столбцов
## \code
# data = pd.get_dummies(data, prefix=["gender"], columns=["Gender"], dtype=int)
# data = pd.get_dummies(data, prefix=["sub_type"], columns=["Subscription Type"], dtype=int)
# data = pd.get_dummies(data, prefix=["contract_len"], columns=["Contract Length"], dtype=int)
## \endcode
## \return Кортеж tuple(), содержащий признаки и целевые переменные
def preprocess (filepath: str, data_type: str) -> tuple:
    if data_type == "train":
        data = pd.read_csv(filepath)
    else:
        data = pd.read_csv(filepath, index_col=[0])

    data.drop(columns=["CustomerID", "Tenure", "Last Interaction"], inplace=True)
    data.dropna(inplace=True)

    data = pd.get_dummies(data, prefix=["gender"], columns=["Gender"], dtype=int)
    data = pd.get_dummies(data, prefix=["sub_type"], columns=["Subscription Type"], dtype=int)
    data = pd.get_dummies(data, prefix=["contract_len"], columns=["Contract Length"], dtype=int)

    if data_type == "train":
        X = data.drop(columns=["Churn"])
        Y = data["Churn"]
        X_columns = X.columns

        scaler = StandardScaler().fit(X)
        X = pd.DataFrame(data=scaler.transform(X), columns=X_columns)

        return (X, Y)
    else:
        X = data.copy()
        X_columns = X.columns

        scaler = StandardScaler().fit(X)
        X = pd.DataFrame(data=scaler.transform(X), columns=X_columns)
        
        return X