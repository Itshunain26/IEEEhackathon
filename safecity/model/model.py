import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df = pd.read_csv("data/crdata.csv")

le = LabelEncoder()
df["crime_type"] = le.fit_transform(df["crime_type"])
df["area_type"] = le.fit_transform(df["area_type"])
df["risk_level"] = le.fit_transform(df["risk_level"])

X = df.drop("risk_level", axis = 1)
y = df["risk_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.2, random_state = 42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

importance = pd.Series(model.feature_importances_, index = X.columns)
print("\nFeature Importance : \n", importance.sort_values(ascending=False))

