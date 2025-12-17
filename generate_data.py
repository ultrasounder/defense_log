# generate_data.py
import pandas as pd

# Create mock data that triggers every rule in your logic.py
data = {
    "Part Number": [
        "NE555",           # Should be Active
        "OBS-2000-X",      # Should be Obsolete (matches "OBS")
        "LM7805",          # Should be Active
        "LEGACY-CHIP-99",  # Should be Obsolete (matches "LEGACY")
        "ATMEGA328P"       # Should be NRND/Warning (matches "ATMEGA")
    ],
    "Description": [
        "Timer IC",
        "Old VGA Controller",
        "Voltage Regulator 5V",
        "Discontinued Memory",
        "Microcontroller 8-bit"
    ]
}

# Create DataFrame and save
df = pd.DataFrame(data)
df.to_csv("input_bom.csv", index=False)

print("✅ 'input_bom.csv' has been generated successfully.")