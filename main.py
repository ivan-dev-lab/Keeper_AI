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
## \version 1.1.1
## \date 22.08.2023
## \details Функция обеспечивает коммуникацию между моделью и пользователем путем создания флагов для комадной строки
## \returns Пространство имен argparse.Namespace
def make_communication () -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Keeper_AI - Cистема классификации клиентов.")

    parser.add_argument("--clients", type=str, help="путь до исходных данных в формате [.CSV|.XLSX]")
    parser.add_argument("--pred", type=str, help="предолагаемый путь до конечных данных в формате [.CSV|.XLSX]")
    
    rate_arg_group = parser.add_argument_group(title="Оценка различных моделей", description="При использовании только флага --rate из данной группы будут построены ТОЛЬКО графики, которые будут сохранены по умолчанию в C:/Users/User/Keeper_AI-work/rating/")
    rate_arg_group.add_argument("--rate", action="store_true", help="флаг определяет выполнение задачи оценки по умолчанию")
    rate_arg_group.add_argument("--charts", type=str, help="Путь до предполагаемой папки с графиками")
    rate_arg_group.add_argument("--best", type=str, help="Путь до предполагаемого файла .CSV с оценкой моделей")
    rate_arg_group.add_argument("--num_top", type=int, help="Длина составляемого топа", default=3)
    rate_arg_group.add_argument("--top", type=str, help="Путь до предполагаемого файла .CSV с топ 3 моделей")

    parser.add_argument("--train", action="store_true", help="флаг определяет необходимость обучения моделей")
    
    return parser.parse_args()


## \brief Главная функция в которой собраны все остальные функци проекта
## \authors ivan-dev-lab-home
## \version 1.1.0
## \returns None
def main ():
    args = make_communication ()

    request = {}

    for arg in args._get_kwargs():
        #print(index,arg)
        if arg[0] == "clients":
            request["path_clients"] = arg[1]
        elif arg[0] == "train":
            request["need_train"] = arg[1]
        if arg[0] == "pred":
            request["path_pred"] = arg[1]
        elif arg[0] == "rate":
            request["need_rate"] = arg[1]
        elif arg[0] == "charts":
            request["path_charts"] = arg[1]
        elif arg[0] == "best":
            request["path_best"] = arg[1]
        elif arg[0] == "num_top":
            request["num_top"] = arg[1]
        elif arg[0] == "top":
            request["path_top"] = arg[1]
            
    for name,value in request.items():
        print(f"{name}: {value}")



if __name__ == "__main__":
    main()