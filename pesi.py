import csv
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

goods = load_prices(os.path.join(BASE_DIR, "DATA", "manila_prices.csv"))
print("Loaded goods:")
for g in goods:
    print(" -", g["name"])

def percent_change(prices):
    start = prices[0]
    end = prices[-1]
    change = end - start
    percent = (change / start) * 100
    return percent

pesi_score = 0

print("\nBreakdown:")
for g in goods:
    pct = percent_change(g["prices"])
    weighted = pct * g["weight"]
    pesi_score += weighted
    print(f" - {g['name']}: {pct:.2f}% change (weighted: {weighted:.2f})")

print("\n===========================")
print(f" PESI SCORE: {pesi_score:.2f}")
print("===========================")

if pesi_score < 2:
    label = "LOW STRESS"

elif pesi_score < 5:
 label = "MODERATE STRESS"

else:
 label = "HIGH STRESS"

print(f" STATUS: {label}")
print("==========================")

import matplotlib.pyplot as plt

names = [g["name"] for g in goods]
changes = [percent_change(g["prices"]) for g in goods]

plt.figure(figsize=(10, 6))
plt.bar(names, changes, color="tomato")
plt.title(f"PESI - Manila | Score: {pesi_score:.2f} | {label}")
plt.ylabel("Percent Change (%)")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()