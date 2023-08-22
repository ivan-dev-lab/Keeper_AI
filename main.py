import argparse

## \brief Функция-коммуникатор между пользователем и моделью
## \authors ivan-dev-lab-home
## \version 1.0.0
## \date 22.08.2023
## \details Функция обеспечивает коммуникацию между моделью и пользователем путем создания флагов для комадной строки
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
    rate_arg_group.add_argument("--save_charts", type=str, help="Путь до предполагаемой папки с графиками", default="C:/Users/User/Keeper_AI-work/rating/charts/")
    rate_arg_group.add_argument("--save_best", type=str, help="Путь до предполагаемого файла .CSV с оценкой моделей", default="C:/Users/User/Keeper_AI-work/rating/best.csv")
    rate_arg_group.add_argument("--save_best_x", type=str, help="Путь до предполагаемого файла .XLSX с оценкой моделей", default="C:/Users/User/Keeper_AI-work/rating/best.xlsx")
    rate_arg_group.add_argument("--top", action="store_true", help="флаг определяет выполнение задачи составление топ 3 моделей с сохранением по умолчанию")
    rate_arg_group.add_argument("--num_in_top", type=int, help="Длина составляемого топа", default=3)
    rate_arg_group.add_argument("--save_top", type=str, help="Путь до предполагаемого файла .CSV с топ 3 моделей", default="C:/Users/User/Keeper_AI-work/rating/top.csv")
    rate_arg_group.add_argument("--save_top_x", type=str, help="Путь до предполагаемого файла .XLSX с топ 3 моделей", default="C:/Users/User/Keeper_AI-work/rating/top.xlsx")

    parser.add_argument("--train", action="store_true", help="флаг определяет необходимость обучения моделей")
    
    return parser.parse_args()

## \brief Главная функция в которой собраны все остальные функци проекта
## \authors ivan-dev-lab-home
## \version 1.0.0
## \returns None
def main ():
    make_communication ()



if __name__ == "__main__":
    main()