import pandas as pd
from sklearn.preprocessing import StandardScaler
from progress.bar import IncrementalBar

## \brief Переменная с полосой загрузки
## \authors ivan-dev-lab
## \version 1.0.0
## \date 23.08.2023
## \details При наличии полосы загрузке в консоли будет легче отследить ошибку, возникающую при работе функции preprocess
bar = IncrementalBar('Предобработка данных...', max=6)

## \brief Функция предобработки данных
## \authors ivan-dev-lab
## \version 1.0.1
## \date 23.08.2023
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
    bar.next()

    data = pd.get_dummies(data, prefix=["gender"], columns=["Gender"], dtype=int)
    bar.next()
    data = pd.get_dummies(data, prefix=["sub_type"], columns=["Subscription Type"], dtype=int)
    bar.next()
    data = pd.get_dummies(data, prefix=["contract_len"], columns=["Contract Length"], dtype=int)
    bar.next()

    if data_type == "train":
        X = data.drop(columns=["Churn"])
        Y = data["Churn"]
        X_columns = X.columns
        bar.next()

        scaler = StandardScaler().fit(X)
        X = pd.DataFrame(data=scaler.transform(X), columns=X_columns)
        bar.next()
        return (X, Y)
    else:
        X = data.copy()
        X_columns = X.columns
        bar.next()

        scaler = StandardScaler().fit(X)
        X = pd.DataFrame(data=scaler.transform(X), columns=X_columns)
        bar.next()
        return X