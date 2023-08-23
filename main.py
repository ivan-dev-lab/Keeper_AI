import argparse

## \brief Пользовательское исключение
## \authors ivan-dev-lab-home
## \version 1.0.0
## \date 22.08.2023
## \details Исключение создано для создания ошибки при передаче НЕ двух кортежей в функцию check_both_args. Ниже примеры кода с использованием исключения
## \code
# if len(types) != 2:
#     raise IncorrectNumberOfArgumentsError(f"Количество переданных объектов [{len(types)}] не соотвествует ожидаемой длине [2]")
## \endcode
class IncorrectNumberOfArgumentsError (Exception): pass

## \brief Функция-коммуникатор между пользователем и моделью
## \authors ivan-dev-lab-home
## \version 1.0.1
## \date 22.08.2023
## \details Функция обеспечивает коммуникацию между моделью и пользователем путем создания флагов для комадной строки
## \warning Необходимо что-то сделать с аргументами передачи путей хранения. При передаче определенного из пары ( например, clients_x вместо clients ), вписывается значение по умолчанию у clients
## \returns Пространство имен argparse.Namespace
def make_communication () -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Keeper_AI - Cистема классификации клиентов.")

    clients_arg_group = parser.add_argument_group(title="Загрузка данных о клиентах")
    clients_arg_group.add_argument("--clients", type=str, help="путь до исходных данных в формате .CSV")
    clients_arg_group.add_argument("--clients_x", type=str, help="путь до исходных данных в формате .XLSX")
    
    pred_arg_group = parser.add_argument_group(title="Выгрузка данных с предсказаниями модели", description="По умолчанию данные будут сохраняться в C:/Users/User/Keeper_AI-work/predictions/pred.[csv|xlsx]")
    pred_arg_group.add_argument("--pred", type=str, help="путь до данных в формате .CSV", default="C:/Users/User/Keeper_AI-predictions/pred.csv")
    pred_arg_group.add_argument("--pred_x", type=str, help="путь до данных в формате .XLSX", default="C:/Users/User/Keeper_AI-predictions/pred.xlsx")
    
    rate_arg_group = parser.add_argument_group(title="Оценка различных моделей", description="При использовании только флага --rate из данной группы будут построены ТОЛЬКО графики, которые будут сохранены по умолчанию в C:/Users/User/Keeper_AI-work/rating/")
    rate_arg_group.add_argument("--rate", action="store_true", help="флаг определяет выполнение задачи оценки по умолчанию")
    rate_arg_group.add_argument("--charts", type=str, help="Путь до предполагаемой папки с графиками", default="C:/Users/User/Keeper_AI-work/rating/charts/")
    rate_arg_group.add_argument("--best", type=str, help="Путь до предполагаемого файла .CSV с оценкой моделей", default="C:/Users/User/Keeper_AI-work/rating/best.csv")
    rate_arg_group.add_argument("--best_x", type=str, help="Путь до предполагаемого файла .XLSX с оценкой моделей", default="C:/Users/User/Keeper_AI-work/rating/best.xlsx")
    rate_arg_group.add_argument("--num_top", type=int, help="Длина составляемого топа", default=3)
    rate_arg_group.add_argument("--top", type=str, help="Путь до предполагаемого файла .CSV с топ 3 моделей", default="C:/Users/User/Keeper_AI-work/rating/top.csv")
    rate_arg_group.add_argument("--top_x", type=str, help="Путь до предполагаемого файла .XLSX с топ 3 моделей", default="C:/Users/User/Keeper_AI-work/rating/top.xlsx")

    parser.add_argument("--train", action="store_true", help="флаг определяет необходимость обучения моделей")
    
    return parser.parse_args()

## \brief Функция проверки пары аргументов
## \authors ivan-dev-lab-home
## \version 1.0.0
## \date 22.08.2023
## \details Т.к в функции make_communication для передачи путей к данным имеются два парных флага ( например, --clients и --clients_x - стандартный .csv и .xlsx соотсвественно ), то необходимо проверять их обоих для выявления подходящего, после чего возвращать первый соотвествующий
## \details Передаются эти флаги в код в виде массива с кортежами. Каждый кортеж выглядит как ( название_флага, значение_переданное_из_командной_строки )
## \details ВАЖНО! Функция не проверяет правильность значения, она лишь возвращает тот кортеж, значение в котором НЕ None
## \returns Значение переданного аргумента, либо None, если оба флага не были использованы
def check_both_args (*types: tuple):
    if len(types) != 2:
        raise IncorrectNumberOfArgumentsError(f"Количество переданных объектов [{len(types)}] не соотвествует ожидаемой длине [2]")
    else:
        for arg in types:
            if arg[1] != None and str(arg[1]).isdigit() == False:
                return arg[1]
            

## \brief Главная функция в которой собраны все остальные функци проекта
## \authors ivan-dev-lab-home
## \version 1.1.0
## \returns None
def main ():
    args = make_communication ()

    request = {}

    for i, arg in enumerate(args._get_kwargs()):
        #print(index,arg)
        if arg[0] == "clients" and args._get_kwargs()[i+1][0] == "clients_x":
            request["path_clients"] = check_both_args(arg, args._get_kwargs()[i+1])
        elif arg[0] == "train":
            request["need_train"] = arg[1]
        if arg[0] == "pred" and args._get_kwargs()[i+1][0] == "pred_x":
            request["path_pred"] = check_both_args(arg, args._get_kwargs()[i+1])
        elif arg[0] == "rate":
            request["need_rate"] = arg[1]
        elif arg[0] == "charts":
            request["path_charts"] = arg[1]
        elif arg[0] == "best" and args._get_kwargs()[i+1][0] == "best_x":
            request["path_best"] = check_both_args(arg, args._get_kwargs()[i+1])
        elif arg[0] == "num_top":
            request["num_top"] = arg[1]
        elif arg[0] == "top" and args._get_kwargs()[i+1][0] == "top_x":
            request["path_top"] = check_both_args(arg, args._get_kwargs()[i+1])
            
    for name,value in request.items():
        print(f"{name}: {value}")



if __name__ == "__main__":
    main()