import random

def print_matrix(matrix):
    users = list(matrix.keys())
    objects = list(matrix[users[0]].keys()) # получаем объекты, по первому пользователю, тк объекты повторяются у всех пользователей

    
    header = f"{'':<12} | " + " | ".join(f"{obj:<15}" for obj in objects)
    separator = "-" * len(header)
    
    print("МАТРИЦА ДОСТУПА")
    print(separator)
    print(header)
    print(separator)
    
    for user in users:
        row = f"{user:<12} | "
        for obj in objects:
            rights = matrix[user][obj]
            if rights:
                rights_str = ', '.join(sorted(rights))
            else:
                rights_str = 'Запрет'
            row += f"{rights_str:<15} | "
        print(row)
    
    print(separator)

USERS = ['DmitriyS', 'IvanB', 'SergeyA', 'PetrV'] #идентификаторы
OBJECTS = ["Object1", "Object2", "Object3", "Object4"]
S = {
    1: "read",
    2: "write",
    3: "Полные права"
}
USER_ADMIN = "DmitriyS" #администратор системы


def create_access_matrix(seed=None):
    if seed is not None:
        random.seed(seed)
    
    mat = {}
    for u in USERS:
        mat[u] = {}
        for o in OBJECTS:
            mat[u][o] = set()

    for o in OBJECTS:
        mat[USER_ADMIN][o] = {S[3]}

    base_rights = list(S.values())[:-1]  #СРЕЗАЕМ ПОСЛЕДНИЙ ЭЛЕМЕНТ, ТК АДМИН УЖЕ ПОЛУЧИЛ СВОИ ПРАВА
    

    for u in USERS:
        if u == USER_ADMIN:
            continue
        for o in OBJECTS:
            r = random.random()
            if r < 0.30:
                mat[u][o] = set()
            elif r < 0.65:
                mat[u][o] = {random.choice(base_rights)}  
            else:
                mat[u][o] = set(base_rights)
    print(mat)               
    return mat


def show_user_rights(user, matrix):
    print(f"\nUser: {user}")
    print("Идентификация прошла успешно, добро пожаловать в систему")
    print("Перечень Ваших прав:")
    for obj in OBJECTS:
        rights = matrix[user][obj]
        if not rights:
            print(f"{obj}: Запрет")
        else:
            print(f"{obj}: {', '.join(rights)}")

def main():
    matrix = create_access_matrix(seed=42)
    print_matrix(matrix)
    while True:
        user = input("\nUser: ")
        if user not in USERS:
            print("Ошибка: пользователь не найден. Повторите ввод.")
            continue
        show_user_rights(user, matrix)

        
        while True:
            command = input("\nЖду ваших указаний > ").strip().lower()

            if command == "quit":
                print(f"Работа пользователя {user} завершена. До свидания.")
                break

            elif command in ["read", "write"]:
                obj_num = input("Над каким объектом производится операция? ")
                if not obj_num.isdigit() or not (1 <= int(obj_num) <= len(OBJECTS)):
                    print("Ошибка: неверный номер объекта.")
                    continue

                obj = OBJECTS[int(obj_num) - 1]
                rights = matrix[user][obj]

                if "Полные права" in rights or S[1] in rights and command == "read" or S[2] in rights and command == "write":
                    print("Операция прошла успешно")
                else:
                    print("Отказ в выполнении операции. У Вас нет прав для ее осуществления.")

            elif command == "grant":
                obj_num = input("Право на какой объект передается? ")
                if not obj_num.isdigit() or not (1 <= int(obj_num) <= len(OBJECTS)):
                    print("Ошибка: неверный номер объекта.")
                    continue

                obj = OBJECTS[int(obj_num) - 1]
                rights = matrix[user][obj]

                if "Полные права" not in rights:
                    print("Отказ в выполнении операции. У Вас нет прав для ее осуществления.")
                    continue

                right_to_give = input("Какое право передается? (read/write) ").strip()
                if right_to_give not in ["read", "write"]:
                    print("Ошибка: недопустимое право.")
                    continue

                target_user = input("Какому пользователю передается право? ").strip()
                if target_user not in USERS:
                    print("Ошибка: пользователь не найден.")
                    continue

                matrix[target_user][obj].add(right_to_give)
                print("Операция прошла успешно")
                print_matrix(matrix)
            elif command == "pickup":
                obj_num = input("Право на какой объект нужно забрать? ")
                if not obj_num.isdigit() or not (1 <= int(obj_num) <= len(OBJECTS)):
                    print("Ошибка: неверный номер объекта.")
                    continue

                obj = OBJECTS[int(obj_num) - 1]
                rights = matrix[user][obj]

                if "Полные права" not in rights:
                    print("Отказ в выполнении операции. У Вас нет прав для ее осуществления.")
                    continue

                right_to_give = input("Какое право забирается? (read/write) ").strip()
                if right_to_give not in ["read", "write"]:
                    print("Ошибка: недопустимое право.")
                    continue

                target_user = input("У какого пользователя забирается право? ").strip()
                if target_user not in USERS:
                    print("Ошибка: пользователь не найден.")
                    continue
                if right_to_give not in matrix[target_user][obj]:
                    print(f"Ошибка: у пользователя {target_user} нет права {right_to_give} на объект {obj}")
                    continue
                
                matrix[target_user][obj].remove(right_to_give)
                print("Операция прошла успешно")
                print_matrix(matrix)
            else:
                print("Неизвестная команда. Доступные: read, write, grant, pickup, quit")
                
main()