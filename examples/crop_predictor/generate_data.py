import pandas as pd
import numpy as np

# Generate realistic mock crop recommendation dataset
np.random.seed(42)

crops_data = {
    'Rice':        {'N': (60, 100), 'P': (35, 60),  'K': (35, 45),  'temp': (20, 27), 'hum': (80, 90), 'ph': (6.0, 7.0), 'rain': (180, 300)},
    'Maize':       {'N': (60, 100), 'P': (35, 60),  'K': (15, 25),  'temp': (18, 27), 'hum': (55, 75), 'ph': (5.8, 7.0), 'rain': (60, 110)},
    'Chickpea':    {'N': (20, 50),  'P': (55, 80),  'K': (75, 85),  'temp': (17, 20), 'hum': (14, 20), 'ph': (5.9, 8.8), 'rain': (60, 90)},
    'Kidneybeans': {'N': (15, 40),  'P': (60, 80),  'K': (15, 25),  'temp': (15, 24), 'hum': (18, 24), 'ph': (5.5, 5.9), 'rain': (60, 150)},
    'Cotton':      {'N': (100, 140),'P': (35, 60),  'K': (15, 25),  'temp': (22, 26), 'hum': (75, 85), 'ph': (6.0, 8.0), 'rain': (60, 110)},
    'Coffee':      {'N': (80, 120), 'P': (15, 35),  'K': (25, 35),  'temp': (23, 28), 'hum': (50, 70), 'ph': (6.0, 7.2), 'rain': (110, 200)},
    'Watermelon':  {'N': (80, 120), 'P': (5, 30),   'K': (45, 55),  'temp': (24, 27), 'hum': (80, 90), 'ph': (6.0, 7.0), 'rain': (40, 60)},
    'Banana':      {'N': (90, 120), 'P': (70, 95),  'K': (45, 55),  'temp': (25, 30), 'hum': (75, 85), 'ph': (5.5, 6.5), 'rain': (90, 120)}
}

rows = []
for crop, params in crops_data.items():
    for _ in range(150): # 150 samples per crop = 1200 total samples
        n = np.random.uniform(params['N'][0], params['N'][1])
        p = np.random.uniform(params['P'][0], params['P'][1])
        k = np.random.uniform(params['K'][0], params['K'][1])
        temp = np.random.uniform(params['temp'][0], params['temp'][1])
        hum = np.random.uniform(params['hum'][0], params['hum'][1])
        ph = np.random.uniform(params['ph'][0], params['ph'][1])
        rain = np.random.uniform(params['rain'][0], params['rain'][1])
        rows.append({
            'N': round(n, 1),
            'P': round(p, 1),
            'K': round(k, 1),
            'temperature': round(temp, 2),
            'humidity': round(hum, 2),
            'ph': round(ph, 2),
            'rainfall': round(rain, 2),
            'crop': crop
        })

df = pd.DataFrame(rows)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv('d:/enlangg/examples/crop_predictor/crop_recommendation.csv', index=False)
print(f"Generated dataset with {len(df)} samples across {len(crops_data)} crops!")
