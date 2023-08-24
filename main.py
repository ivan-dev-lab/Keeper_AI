import argparse
import os
import re
import joblib
from sklearn.model_selection import train_test_split
from preprocess import preprocess
from create_model import create_model

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
## \version 1.1.2
## \date 22.08.2023
## \details Функция обеспечивает коммуникацию между моделью и пользователем путем создания флагов для комадной строки
## \brief Подумать над сохранением исходного models_rating
## \returns Пространство имен argparse.Namespace
def make_communication () -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Keeper_AI - Cистема классификации клиентов.")

    data_arg_group = parser.add_argument_group(title="Сохранение и загрузка данных", description="Если не указывать флаг --pred, то данные с предсказаниями будут загружаться в C:/Users/User/Keeper_AI-work/predictions/clients.csv")
    data_arg_group.add_argument("--clients", type=str, help="Путь до исходных данных в формате [.CSV|.XLSX]") # В КОНЦЕ ОБЯЗАТЕЛЬНО СДЕЛАТЬ required=True
    data_arg_group.add_argument("--pred", type=str, help="Путь до предполагаемого файла в формате [.CSV|.XLSX] с конечными данными", default="C:/Users/User/Keeper_AI-work/predictions/clients.csv")
    data_arg_group.add_argument("--save_models", type=str, help="Путь до предполагаемого каталога с сохраненными моделями из составленного топа")
    
    rate_arg_group = parser.add_argument_group(title="Оценка различных моделей", description="Если не проводить оценку моделей, то для работы с данными будет использоваться модель по умолчанию. При использовании только флага --rate из данной группы все будет сохранено в каталог по умолчанию в C:/Users/User/Keeper_AI-work/rating/ . Если не использовать свое значение при флаге --num_top, то топ будет включать в себя 3 позиции")
    rate_arg_group.add_argument("--rate", action="store_true", help="флаг определяет выполнение задачи оценки по умолчанию")
    rate_arg_group.add_argument("--charts", type=str, help="Путь до предполагаемого каталога с графиками", default="C:/Users/User/Keeper_AI-work/rating/charts/")
    rate_arg_group.add_argument("--best", type=str, help="Путь до предполагаемого файла в формате [.CSV|.XLSX] с оценкой моделей", default="C:/Users/User/Keeper_AI-work/rating/best.csv")

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
## \version 1.1.0
## \date 23.08.2023
## \returns None
def main ():
    # request временно заполнен на время разработки, в конце должно быть request = create_request ()
    request = {
        'clients': 'C:/Users/User/Desktop/clients.csv',
        'pred': 'C:/Users/User/Desktop/Keeper_AI-work/clients_preprocessed.xlsx',
        'save_models': 'C:/Users/User/Desktop/Keeper_AI-work/models/',
        'rate': True,
        'charts': 'C:/Users/User/Desktop/Keeper_AI-work/charts',
        'best': 'C:/Users/User/Desktop/Keeper_AI-work/rating/best.csv',
        'top': 'C:/Users/User/Desktop/Keeper_AI-work/rating/top.csv',
        'top_by': 'r2_score',
        'num_top': 4,
        'train': True
    }
    # СДЕЛАТЬ ПРОВЕРКУ НА СУЩЕТВОВАНИЕ У КАТАЛОГОВ ВЕЗДЕ
        
    clients_data = preprocess(request["clients"], data_type="test")
    X,Y = preprocess("data/train.csv", data_type="train")
    X = X.iloc[0:100000]
    Y = Y.iloc[0:100000]
    
    model = create_model(input_shape=X.shape[1])

    if request['train'] and request['rate'] == False:
        x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size=0.2, random_state=42)
        model.fit(x_train, y_train, batch_size=64, epochs=10, verbose=0)

        joblib.dump(model, "models/ModelRegression.pkl")
    elif request['train'] == False:
        model = joblib.load("models/ModelRegression.pkl")

    if request['rate']:
        from rate import rate_models, create_models_charts, get_best_models, get_models_top
        models_rating = rate_models(X,Y, verbose=False)

        os.makedirs(request['charts'])
        create_models_charts(models_rating, request['charts'])

        get_best_models(models_rating, fpath=request['best'])

        models_top = get_models_top(models_rating, top_by=request['top_by'], num_top=request["num_top"])

        model = joblib.load(f'models/{models_top[0]}.pkl')

    clients_data["Исход"] = model.predict(clients_data)

    if request['pred'].find(".csv") != -1:
        clients_data.to_csv(request['pred'])
    elif request['pred'].find(".xlsx") != -1:
        clients_data.to_excel(request['pred'])





if __name__ == "__main__":
    main()