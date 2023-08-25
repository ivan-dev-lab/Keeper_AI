import argparse
import os
import re
import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from preprocess import preprocess

## \brief Пользовательское исключение
## \authors ivan-dev-lab
## \version 1.0.0
## \date 22.08.2023
## \details Исключение создано для создания ошибки при передаче НЕ двух кортежей в функцию check_both_args. Ниже примеры кода с использованием исключения
## \code
# if len(types) != 2:
#     raise IncorrectNumberOfArgumentsError(f"Количество переданных объектов [{len(types)}] не соотвествует ожидаемой длине [2]")
## \endcode
class IncorrectNumberOfArgumentsError (Exception): pass

## \brief Функция-коммуникатор между пользователем и моделью
## \authors ivan-dev-lab
## \version 1.2.2
## \date 24.08.2023
## \details Функция обеспечивает коммуникацию между моделью и пользователем путем создания флагов для комадной строки
## \returns Пространство имен argparse.Namespace
def make_communication () -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Keeper_AI - Cистема классификации клиентов.")

    data_arg_group = parser.add_argument_group(title="Сохранение и загрузка данных", description="Если не указывать флаг --pred, то данные с предсказаниями будут загружаться в C:/Users/User/Keeper_AI-work/clients_preprocessed.csv")
    data_arg_group.add_argument("--clients", type=str, help="Путь до исходных данных в формате [.CSV|.XLSX]", required=True) 
    data_arg_group.add_argument("--pred", type=str, help="Путь до предполагаемого файла в формате [.CSV|.XLSX] с конечными данными", default="C:/Users/User/Keeper_AI-work/clients_preprocessed.csv")

    train_arg_group = parser.add_argument_group(title="Тренировка моделей", description="При тренировки модели для предсказаний и моделей для оценки, будут использоваться данные по-умолчанию из каталога Keeper_AI/data/train.csv")
    train_arg_group.add_argument("--train", action="store_true", help="Флаг определяет необходимость обучения моделей")
    
    return parser.parse_args()

## \brief Функция проверки введенных аргументов 
## \authors ivan-dev-lab
## \version 1.0.0
## \date 23.08.2023
## \details Функция проверят корректность введенных аргументов при запуске программы из командной строки.
## \details Проверятся существование файла только для флага --clients, во всех остальных случаях используются регулярные выражения
## \returns Словарь dict() с именами и значениями полученных аргументов
def create_request () -> dict:
    args = make_communication ()
    request = {}

    for arg in args._get_kwargs():
        if arg[0] == "clients" and os.path.exists(arg[1]):
            request["clients"] = arg[1]
        elif arg[0] == "train":
            request["train"] = arg[1]
        if arg[0] == "pred" and re.match(r"\S*/*\.(csv|xlsx)", arg[1]) != None:
            request["pred"] = arg[1]
        elif arg[0] == "rate":
            request["rate"] = arg[1]
        elif arg[0] == "charts" and re.match(r"\S*/*$", arg[1]) != None:
            request["charts"] = arg[1]
        elif arg[0] == "save_models" and re.match(r"\S*/*$", arg[1]) != None:
            request["save_models"] = arg[1]
        elif arg[0] == "best" and re.match(r"\S*/*\.(csv|xlsx)", arg[1]) != None:
            request["best"]  = arg[1]
        elif arg[0] == "top" and re.match(r"\S*/*\.(csv|xlsx)", arg[1]) != None:
            request["top"] = arg[1]
        elif arg[0] == "num_top":
            request["num_top"] = arg[1]

    return request

## \brief Главная функция в которой собраны все остальные функци проекта
## \authors ivan-dev-lab
## \version 2.1.0
## \date 24.08.2023
## \returns None
def main ():
    request = create_request ()

    DEST_DIR = request["pred"].split("/")
    DEST_DIR.pop()
    DEST_DIR = "/".join(DEST_DIR)
    
    if os.path.exists(DEST_DIR) == False:
        os.makedirs(DEST_DIR)

    clients_data, clients_data_prep = None, None

    if request['clients'].find(".csv") != -1:
        clients_data = pd.read_csv(request["clients"], index_col=[0])
        clients_data_prep = preprocess(clients_data.copy(), data_type="test")

    elif request['clients'].find(".xlsx") != -1:
        clients_data = pd.read_excel(request["clients"], index_col=[0])
        clients_data_prep = preprocess(clients_data.copy(), data_type="test")
    
    clients_data = clients_data[["CustomerID"]]
 
    train_data = pd.read_csv("data/train.csv")
    X,Y = preprocess(train_data, data_type="train")
    
    model = HistGradientBoostingClassifier()

    if os.path.exists(DEST_DIR+"/model/") == False:
        os.makedirs(DEST_DIR+"/model/")

    if request['train']:
        model.fit(X, Y)
        joblib.dump(model, f"{DEST_DIR}/model/HistGradientBoostingClassifier.pkl")
    else:
        if os.path.exists(f"{DEST_DIR}/model/HistGradientBoostingClassifier.pkl"):
            model = joblib.load(f"{DEST_DIR}/model/HistGradientBoostingClassifier.pkl")
        else:
            model.fit(X, Y)
            joblib.dump(model, f"{DEST_DIR}/model/HistGradientBoostingClassifier.pkl")

    churn_df = pd.DataFrame(data=model.predict(clients_data_prep), columns=["Исход"])
    churn_df.replace({1: "Ушел", 0: "Остался"}, inplace=True)

    clients_data["Исход"] = churn_df

    if request['pred'].find(".csv") != -1:
        clients_data.to_csv(request['pred'])
    elif request['pred'].find(".xlsx") != -1:
        clients_data.to_excel(request['pred'])
    
    print(f"Анализ данных закончен.\nФайл с предсказаниями системы находится по адресу {request['pred']}")

if __name__ == "__main__":
    main()