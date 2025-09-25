from pathlib import Path
import pandas as pd
import numpy as np
rng = np.random.default_rng(7)

root = Path(__file__).resolve().parents[2] / "data"
root.mkdir(parents=True, exist_ok=True)

# Dimensions
hcp = pd.DataFrame({
    "hcp_id": [f"H{i:03d}" for i in range(1, 41)],
    "segment": rng.choice(["A", "B", "C"], size=40),
    "specialty": rng.choice(["Cardio","Endo","GP"], size=40),
})
geo = pd.DataFrame({
    "geo_id": [f"G{i:02d}" for i in range(1, 11)],
    "province": rng.choice(["ON","QC","BC"], size=10),
    "district": [f"D{i:02d}" for i in range(1, 11)],
})
payer = pd.DataFrame({
    "payer_id": [f"P{i:02d}" for i in range(1, 6)],
    "payer_name": rng.choice(["OHIP","RAMQ","PrivateA","PrivateB","BC MSP"], size=5, replace=False),
    "tier": rng.choice(["Preferred","Non-Preferred"], size=5),
})

# Facts (12 weeks)
dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=12, freq="W-FRI")
rows = []
for dt in dates:
    for h in hcp["hcp_id"]:
        geo_row = geo.sample(1, random_state=int(rng.integers(0, 1e6))).iloc[0]
        payer_row = payer.sample(1, random_state=int(rng.integers(0, 1e6))).iloc[0]
        channel = rng.choice(["rep","email","webinar","portal"])
        rx = max(0, int(rng.normal(20, 7)))
        revenue = rx * rng.uniform(45, 75)
        rows.append({
            "date": dt.date().isoformat(),
            "hcp_id": h,
            "geo_id": geo_row["geo_id"],
            "channel": channel,
            "payer_id": payer_row["payer_id"],
            "rx": rx,
            "revenue": round(revenue, 2),
            "forecast_rx": max(0, int(rx + rng.normal(0, 5)))  # for under/over performance
        })
fact_sales = pd.DataFrame(rows)

# Write CSVs (simple for now)
hcp.to_csv(root / "dim_hcp.csv", index=False)
geo.to_csv(root / "dim_geo.csv", index=False)
payer.to_csv(root / "dim_payer.csv", index=False)
fact_sales.to_csv(root / "fact_sales.csv", index=False)

print("Wrote CSVs to", root)
