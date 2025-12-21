
import subprocess
import re
import hashlib
import secrets
import os
import sys

LICENSE_FILE = "license.dat"


def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True, shell=False)
        return out
    except Exception:
        return None


def get_mac_wmic():
    out = run_cmd(["wmic", "nic", "where", "NetEnabled=true", "get", "MACAddress"])
    
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return lines[1]


def get_cpu_max_mhz_wmic():
    out = run_cmd(["wmic", "cpu", "get", "MaxClockSpeed"])
    if not out:
        return None
    
    nums = re.findall(r"\d+", out)
    if nums:
        try:
            return int(nums[0])
        except:
            return None
    return None


def build_machine_id():
    mac = get_mac_wmic() or ""
    freq = get_cpu_max_mhz_wmic() or 0
    return f"MAC={mac}|FREQ={freq}"


def create_license_file(path=f'{LICENSE_FILE}'):
    machine_id = build_machine_id()
    if not machine_id or machine_id == "MAC=|FREQ=0":
        print("Нет MAC или частоты")
        return False
    
    salt = secrets.token_hex(16)

    digest = hashlib.sha256((salt + machine_id).encode("utf-8")).hexdigest()

    with open(path, "w", encoding="utf-8") as f:
        f.write(salt + ":" + digest + "\n")
    print(f"license создан: {path}")
    print("machine_id (для демонстрации):", machine_id)
    return True


def check_license_file(path=LICENSE_FILE):
    if not os.path.exists(path):
        print("license.dat не найден.")
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            first = f.readline().strip()
            if ":" not in first:
                print("Неверный формат license.dat")
                return False
            salt, stored = first.split(":", 1)
    except Exception as e:
        print("Ошибка чтения license:", e)
        return False
    machine_id = build_machine_id()
    digest = hashlib.sha256((salt + machine_id).encode("utf-8")).hexdigest()
    ok = (digest == stored)
    if ok:
        print("Лицензия валидна. Машина совпадает.")
    else:
        print("Лицензия не соответствует текущей машине.")
        print("Текущий machine_id:", machine_id)
    return ok


def usage():
    print("Использование:")
    print("python lab4.py bind - создать license.dat")
    print("python lab4.py check - проверить соответствие")
    print("python lab4.py run - попытаться запустить (проверка)")

def demo_run():
    if check_license_file():
        print("Запуск приложения...")
    else:
        print("Запуск запрещён - лицензия не подходит.")

def main():
    if len(sys.argv) < 2:
        usage()
        return
    cmd = sys.argv[1].lower()
    if cmd == "bind":
        create_license_file()
    elif cmd == "check":
        check_license_file()
    elif cmd == "run":
        demo_run()
    else:
        usage()


main()
