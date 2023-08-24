import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.ensemble import HistGradientBoostingClassifier, ExtraTreesClassifier, BaggingClassifier, AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
import joblib
import os
from preprocess import preprocess
from create_model import create_model

## \brief Кортеж с признаками и целевым переменными
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
response_tuple = preprocess("data/train.csv", "train")

## \brief Признаки данных
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
X = response_tuple[0]

## \brief Целевые переменные данных
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
Y = response_tuple[1]

## \brief Функция-оценщик моделей
## \authors ivan-dev-lab
## \version 1.1.0
## \date 05.08.2023
## \param[in] X Признаки входных данных 
## \param[in] Y Целевые переменные входных данных 
## \param[in] verbose Аргумент определяет вывод на экран результаты обучения моделей. По умолчанию = True
## \details В приведенной ниже конструкции выполняется сохранение моделей. Это нужно для того, чтобы при итоговой работе в файле main.py моделям не нужно было заново обучаться - достаточно просто загрузить их из файла
## \code
# joblib.dump(model, f"models/{name}.pkl")
## \endcode
## \code
# joblib.dump(model, f"models/MyModelRegression.pkl")
## \endcode
## \return Кортеж tuple(), содержащий названия моделей и результаты их обучения ( mse, mae, r2_score )
def rate_models (X: pd.DataFrame, Y: pd.DataFrame, verbose=True) -> tuple:
    model = create_model(input_shape=len(X.columns))

    models = {
        'HistGradientBoostingClassifier': HistGradientBoostingClassifier,
        'ExtraTreesClassifier': ExtraTreesClassifier,
        'BaggingClassifier': BaggingClassifier,
        'AdaBoostClassifier': AdaBoostClassifier,
        'RandomForestClassifier': RandomForestClassifier,
        'GradientBoostingClassifier': GradientBoostingClassifier,
        'DecisionTreeClassifier': DecisionTreeClassifier
    }
    
    names, mse_scores, mae_scores, r2_scores = [], [], [], []

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    for name, Model in models.items():

        model = Model().fit(x_train, y_train)
        joblib.dump(model, f"models/{name}.pkl")

        y_pred = model.predict(x_test)

        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        names.append(name)
        mse_scores.append(mse)
        mae_scores.append(mae)
        r2_scores.append(r2)

        if verbose:
            print(f"\n{name}:\nmean_squared_error: {mse}\nmean_absolute_error: {mae}\nr2_score: {r2}")

    model = create_model(input_shape=X.shape[1])
    model.fit(x_train, y_train, batch_size=64, epochs=30, verbose=0)
    joblib.dump(model, f"models/MyModelRegression.pkl")

    y_pred = model.predict(x_test)
    
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    names.append("MyModelRegression")
    mse_scores.append(mse)
    mae_scores.append(mae)
    r2_scores.append(r2)

    if verbose:
        print(f"\nMyModelRegression:\nmean_squared_error: {mse}\nmean_absolute_error: {mae}\nr2_score: {r2}")
            
    return (names, mse_scores, mae_scores, r2_scores)
     
## \brief Функция построения графиков рейтинга моделей
## \authors ivan-dev-lab
## \version 1.1.0
## \date 24.08.2023
## \param[in] models_rating Кортеж с рейтингом моделей из rate_models
## \param[in] fcharts Путь до каталога с графиками 
## \return None
def create_models_charts (models_rating: tuple, fcharts: str) -> None:
    names, mse_scores, mae_scores, r2_scores = models_rating

    print(names, mse_scores, mae_scores, r2_scores, sep="\n\n")

    sns.set_style("darkgrid")
    plt.figure(figsize=(20,10))

    sns.barplot(x=r2_scores, y=names)
    plt.xlabel("r2_score")
    plt.ylabel("Названия моделей")
    plt.savefig(f"{fcharts}/r2_scores")
    
    sns.barplot(x=mse_scores, y=names)
    plt.xlabel("Mean-Squared-Error")
    plt.ylabel("Названия моделей")
    plt.savefig(f"{fcharts}/MSE")

    sns.barplot(x=mae_scores, y=names)
    plt.xlabel("Mean-Absolute-Error")
    plt.ylabel("Названия моделей")
    plt.savefig(f"{fcharts}/MAE")

## \brief Функция расчета лучшей модели по трем метрикам
## \authors ivan-dev-lab-home
## \version 1.0.0
## \date 13.08.2023
## \param[in] models_rating Рейтинг моделей, полученный из функции rate_models 
## \details Программа ищет минимальную метрику из каждого массива ( mse_scores, mae_scores, r2_scores)
## \details Далее в массиве names происходит поиск имени модели по индексу минимальной ( в случае r2_scores - максимальной) метрики в массиве ( mse_scores, mae_scores, r2_scores)
## \code
# best_models["mse"] = [names[mse_scores.index(min(mse_scores))], min(mse_scores)]
## \endcode
## \code
# best_models["mae"] = [names[mae_scores.index(min(mae_scores))], min(mae_scores)]
## \endcode
## \code
# best_models["r2_score"] = [names[r2_scores.index(max(r2_scores))], max(r2_scores)]
## \endcode
## \brief Пример использования:
## \code
# models_rating = rate_models(X, Y, verbose=False)
# best_models = get_best_models(models_rating)
# for metric, result in best_models.items():
#     print(f"Метрика {metric} - лучший результат у {result[0]} = {result[1]}")
## \endcode
## \return Словарь dict() с тремя лучшими моделями по метрикам mse, mae, r2_score
def get_best_models (models_rating: tuple) -> dict:
    best_models = {
        "mse": list,
        "mae": list,
        "r2_score": list
    }
    names, mse_scores, mae_scores, r2_scores = models_rating
    
    best_models["mse"] = [names[mse_scores.index(min(mse_scores))], min(mse_scores)]
    best_models["mae"] = [names[mae_scores.index(min(mae_scores))], min(mae_scores)]
    best_models["r2_score"] = [names[r2_scores.index(max(r2_scores))], max(r2_scores)]

    return best_models

## \brief Пользовательское исключение
## \authors ivan-dev-lab-home
## \version 1.0.0
## \date 22.08.2023
## \details Исключение создано для создания ошибки при передаче некорректного параметра в функцию get_models_top. Ниже примеры кода с использованием исключения
## \code
# else:
#     raise IncorrectParameterError(f'Введенный параметр [top_by={top_by}] является некорректным т.к не принадлежит последовательности ["mse", "mae", "r2_score"])')
## \endcode
## \code
# else:
#     raise IncorrectParameterError(f'Введенный параметр [top_models_num={top_models_num}] является некорректным т.к является больше, чем количество нейросетей, участвующих в рейтинге')
## \endcode
class IncorrectParameterError (Exception): pass

## \brief Функция возврата n-лучших моделей по метрике
## \authors ivan-dev-lab-home
## \version 1.0.0
## \date 16.08.2023
## \param[in] models_rating Рейтинг моделей, полученный из функции rate_models
## \param[in] top_by Метрика, на основании которой будет составлять топ n лучших моделей 
## \param[in] top_models_num Количество моделей, которые зайдут в топ
## \brief Объяснение кода
## \details В приведенных ниже конструкциях выполняется добавления названия модели с наилучшим результатом. В конструкции выполняется поиск названия модели в массиве names по индексу наилучшего результата в массиве с соотвествующими метрииками
## \code
# models_top.append(names[mse_scores.index(min(mse_scores))])
## \endcode
## \code
# models_top.append(names[mae_scores.index(min(mae_scores))])
## \endcode
## \code
# models_top.append(names[r2_scores.index(max(r2_scores))])
## \endcode
## \details В приведенных ниже конструкциях выполняется удаление наилучшего результата из массива с метриками ( в конце - из массива с названиями моделей ) для того, чтобы название модели в итоговом массиве models_top не повторялось
## \code
# mse_scores.pop(mse_scores.index(min(mse_scores)))
## \endcode
## \code
# mae_scores.pop(mae_scores.index(min(mae_scores)))
## \endcode
## \code
# r2_scores.pop(r2_scores.index(max(r2_scores)))
## \endcode
## \code
# names.remove(models_top[len(models_top)-1])
## \endcode
## \details В приведенной ниже конструкции выполняется удаление файлов с моделями, кроме тех, которые были лучшими ( названия которых есть в массиве models_top )
## \code
# for model_file in os.listdir("models"):
#     if model_file.split(".")[0] not in models_top:
#         os.remove(f"models/{model_file}")
## \endcode
## \return Список list() с n-лучшими моделями по определенному признаку
def get_models_top (models_rating: tuple, top_by: str, top_models_num: int=3) -> list:
    models_top = []
    names, mse_scores, mae_scores, r2_scores = models_rating
    
    if top_models_num <= len(names):
        if top_by in ["mse", "mae", "r2_score"]:
            for _ in range(top_models_num):
                if top_by == "mse":
                    models_top.append(names[mse_scores.index(min(mse_scores))])
                    mse_scores.pop(mse_scores.index(min(mse_scores)))
                if top_by == "mae":
                    models_top.append(names[mae_scores.index(min(mae_scores))])
                    mae_scores.pop(mae_scores.index(min(mae_scores)))
                if top_by == "r2_score":
                    models_top.append(names[r2_scores.index(max(r2_scores))])
                    r2_scores.pop(r2_scores.index(max(r2_scores)))

                names.remove(models_top[len(models_top)-1])
            
            for model_file in os.listdir("models"):
                if model_file.split(".")[0] not in models_top:
                    os.remove(f"models/{model_file}")
        else:
            raise IncorrectParameterError(f'Введенный параметр [top_by={top_by}] является некорректным т.к не принадлежит последовательности ["mse", "mae", "r2_score"])')
    else:
        raise IncorrectParameterError(f'Введенный параметр [top_models_num={top_models_num}] является некорректным т.к является больше, чем количество нейросетей, участвующих в рейтинге')

    return models_top