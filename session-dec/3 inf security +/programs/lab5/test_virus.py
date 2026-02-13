import os
import glob


MARKER = b'$' #маркер вируса
JMP_CODE = b'JMP TO VIRUS'  # JMP 

def infect_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        # Проверка на заражение
        if MARKER in data[-50:]:
            print(f"{os.path.basename(filepath)} уже заражён")
            return
        # Сохраняю первые 3 байта
        first3 = data[:3] if len(data) >= 3 else data.ljust(3, b'\x00')
        # body вируса
        virus_payload = (
            b'\n--- VIRUS999 PAYLOAD ---\n' +
            b'ORIGINAL_FIRST3: ' + first3 + b'\n' +
            MARKER + b'\n'
        )
        #заменя первых 3х байт на JMP код
        jmp3 = JMP_CODE[:3] 
        infected_data = jmp3 + data[3:] + virus_payload
        
        # Перезапись данных
        with open(filepath, 'wb') as f:
            f.write(infected_data)
        print(f"Заражён: {filepath}")
        print("Hello! You have been infected by VIRUS999!")
    except Exception as e:
        print(f"Ошибка при заражении {filepath}: {e}")

def main():
    # Ищем все файлы с расширением .comtest в текущей папке
    victims = glob.glob("lab5/dir/*.comtest")
    if not victims:
        print("Нет файлов *.comtest для заражения.")
        return
    for filepath in victims:
        infect_file(filepath)

if __name__ == "__main__":
    print("Запуск учебного вируса VIRUS999")
    main()
