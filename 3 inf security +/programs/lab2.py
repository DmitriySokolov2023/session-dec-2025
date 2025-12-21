import secrets

A = []

for code in range(65, 91): 
    A.append(chr(code))

for code in range(97, 123):   
    A.append(chr(code))

for code in range(48, 58):
    A.append(chr(code))

print("Мощность алфавита A =", len(A))

def generate_password(L, A_list):
    pw_chars = []
    for _ in range(L):
        pw_chars.append(secrets.choice(A_list))
    return ''.join(pw_chars)

L = 8

def main():
    for i in range(10):
        p = generate_password(L, A)
        print(f"Пароль №{i+1}: {p}")

main()