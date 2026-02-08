from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__, static_folder=".", static_url_path="")

df = pd.read_csv("10_Property_stolen_and_recovered.csv")
df.columns = df.columns.str.strip()

area_col = df.select_dtypes(include="object").columns[0]
year_col = df.select_dtypes(include="number").columns[0]
count_col = df.select_dtypes(include="number").columns[-1]
recovered_col = df.select_dtypes(include="number").columns[-2]

le = LabelEncoder()
df["area_encoded"] = le.fit_transform(df[area_col])

X = df[[year_col, "area_encoded"]]
y = df[count_col]

model = LinearRegression()
model.fit(X, y)


# fake but spread coordinates
areas = df[area_col].unique()
coords = {
    a: (8 + (i % 8)*3, 68 + (i // 8)*4)
    for i, a in enumerate(areas)
}


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/summary")
def summary():
    latest = df[df[year_col] == df[year_col].max()]

    return jsonify({
        "stolen": int(latest[count_col].sum()),
        "recovered": int(latest[recovered_col].sum()),
        "area": latest.sort_values(count_col, ascending=False).iloc[0][area_col]
    })


@app.route("/api/heatmap")
def heatmap():

    latest = df[df[year_col] == df[year_col].max()]

    points = []
    for _, r in latest.iterrows():
        lat, lon = coords[r[area_col]]
        points.append({"lat": lat, "lng": lon, "weight": int(r[count_col])})

    return jsonify(points)


@app.route("/api/trends")
def trends():

    yearly = df.groupby(year_col)[count_col].sum()

    return jsonify({
        "labels": yearly.index.astype(str).tolist(),
        "values": yearly.tolist()
    })


@app.route("/api/predict", methods=["POST"])
def predict():

    data = request.json
    year = int(data["year"])
    area = data["area"]

    enc = le.transform([area])[0]

    pred = model.predict(np.array([[year, enc]]))[0]

    return jsonify({"prediction": int(pred)})


if __name__ == "__main__":
    app.run(debug=True)