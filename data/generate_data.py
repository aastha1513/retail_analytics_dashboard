import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)

BRANDS = ["NestleCo", "UnileverX", "PepsiMax", "KraftPlus", "GeneralFoods"]
CATEGORIES = ["Snacks", "Beverages", "Dairy", "Frozen", "Household"]
REGIONS = ["West", "East", "Midwest", "South"]
NUM_STORES = 50

records = []
for _ in range(2000):
    store_id = f"S{random.randint(1, NUM_STORES):03d}"
    brand = random.choice(BRANDS)
    category = random.choice(CATEGORIES)
    region = random.choice(REGIONS)
    date = datetime.today() - timedelta(days=random.randint(0, 365))
    units = random.randint(10, 500)
    price = round(random.uniform(1.5, 25.0), 2)
    revenue = round(units * price, 2)
    freshness_lag = random.randint(0, 10)

    records.append({
        "store_id": store_id,
        "brand": brand,
        "category": category,
        "region": region,
        "date": date.strftime("%Y-%m-%d"),
        "units_sold": units,
        "price": price,
        "revenue": revenue,
        "data_freshness_lag_days": freshness_lag
    })

df = pd.DataFrame(records)
df.to_csv("data/sample_data.csv", index=False)
print(f"Generated {len(df)} rows → data/sample_data.csv")
