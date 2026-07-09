import pandas as pd

df = pd.read_csv("Speed Dating Data.csv", encoding="latin-1")

print("Shape:", df.shape)
print("\nColumns:\n", df.columns.tolist())
print("\nFirst row:\n", df.head(1))
print("\nMissing values:\n", df.isnull().sum().sort_values(ascending=False).head(20))
relevant_columns = ["match","attr","fun","like","prob","shar","int_corr","sinc","amb","intel"]
df_clean = df[relevant_columns].copy()
print(df_clean.describe())
print("\n Match Distribution",df_clean["match"].value_counts())
df_clean = df_clean.dropna()
print("Clean shape",df_clean.shape)
print("Match rate",df_clean["match"].mean()*100,"%")
print(df["int_corr"].describe())
print(df["match"].value_counts(normalize=True))