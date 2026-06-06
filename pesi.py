import csv
import os
import matplotlib.pyplot as plt

BASE_DIR = r"C:\Users\noces\PycharmProjects\PythonProject"

def load_prices(filepath):
    goods = []
    with open(filepath, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            goods.append({
                "name": row["good"],
                "weight": float(row["weight"]),
                "prices": [
                    float(row["month1"]),
                    float(row["month2"]),
                    float(row["month3"])
                ]
            })
    return goods

def percent_change(prices):
    start = prices[0]
    end = prices[-1]
    change = end - start
    percent=(change/start)*100
    return percent

def calculate_pesi(goods):
    pesi_score=0
    for g in goods:
        pct = percent_change(g["prices"])
        weighted = pct* g["weight"]
        pesi_score += weighted
    return pesi_score

def get_label(score):
    if score < 2:
        return "LOW STRESS"
    elif score < 5:
        return "MEDIUM STRESS"
    else:
        return "HIGH STRESS"

regions = {
    "Manila": os.path.join(BASE_DIR, "DATA", "manila_prices.csv"),
    "Cebu": os.path.join(BASE_DIR, "DATA", "cebu_prices.csv"),
    "Davao": os.path.join(BASE_DIR, "DATA", "davao_prices.csv")
}

scores = {}

for region,filepath in regions.items():
    print("Looking for:", filepath)
    print("Exists?", os.path.exists(filepath))
    full_path = filepath
    goods = load_prices(full_path)
    score = calculate_pesi(goods)
    label = get_label(score)
    scores[region] = score
    print(f"{region}: PESI = {score:.2F} | {label}")

# ================================
# STEP 6: Multi-region bar chart
# ================================

region_names = list(scores.keys())
region_scores = list(scores.values())

colors = ["tomato", "steelblue", "seagreen"]

plt.figure(figsize=(10, 6))
plt.bar(region_names, region_scores, color=colors)
plt.title("PESI - Regional Comparison")
plt.ylabel("PESI Score")
plt.axhline(y=5, color="orange", linestyle="--", label="Moderate threshold")
plt.axhline(y=2, color="green", linestyle="--", label="Low threshold")
plt.legend()
plt.tight_layout()
plt.show()

