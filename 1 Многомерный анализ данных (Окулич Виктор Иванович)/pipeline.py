import pandas as pd

df = pd.read_csv("text.txt", sep=None)
df.to_csv("test.csv", index=False)

df_read = pd.read_csv("test.csv")
df_read.to_excel("test.xlsx", index=False)

print("Успешное преобразование файлов!")