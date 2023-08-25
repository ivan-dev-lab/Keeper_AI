import pandas as pd
from sklearn.preprocessing import StandardScaler

## \brief Функция предобработки данных
## \authors ivan-dev-lab
## \version 2.0.2
## \date 25.08.2023
## \param[out] filepath путь до необработанных данных 
## \param[in] data_type Определение типа данных для функции. От параметра зависит - будет ли функция возвращать целевую переменную ( data_type="train" ) или только признаки ( data_type="test" )
## \details Т.к столбцы Gender, Subscription Type и Contract Length содержат категориальные значение, то было принято решение использовать pd.get_dummies для этиъ столбцов
## \code
# data_df = pd.get_dummies(data_df, prefix=["gender"], columns=["Gender"], dtype=int)
# data_df = pd.get_dummies(data_df, prefix=["sub_type"], columns=["Subscription Type"], dtype=int)
# data_df = pd.get_dummies(data_df, prefix=["contract_len"], columns=["Contract Length"], dtype=int)
## \endcode
## \return Кортеж tuple(), содержащий признаки и целевые переменные
def preprocess (data_df: pd.DataFrame, data_type: str) -> tuple:
    data_df.drop(columns=["CustomerID", "Tenure", "Last Interaction"], inplace=True)
    data_df.dropna(inplace=True)

    data_df = pd.get_dummies(data_df, prefix=["gender"], columns=["Gender"], dtype=int)
    data_df = pd.get_dummies(data_df, prefix=["sub_type"], columns=["Subscription Type"], dtype=int)
    data_df = pd.get_dummies(data_df, prefix=["contract_len"], columns=["Contract Length"], dtype=int)

    if data_type == "train":
        X = data_df.drop(columns=["Churn"])
        Y = data_df["Churn"]
        X_columns = X.columns

        scaler = StandardScaler().fit(X)
        X = pd.DataFrame(data=scaler.transform(X), columns=X_columns)

        return (X, Y)
    else:
        X = data_df.copy()
        X_columns = X.columns

        scaler = StandardScaler().fit(X)
        X = pd.DataFrame(data=scaler.transform(X), columns=X_columns)
        
        return X