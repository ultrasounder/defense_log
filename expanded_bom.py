import random
import pandas as pd

INPUT_CSV = "input_bom.csv"
OUTPUT_CSV = "input_bom_expanded.csv"
N_NEW_PARTS = 100

# ----------------------------
# Curated part library
# ----------------------------

PART_LIBRARY = [
    # TTL / CMOS Logic
    ("SN74LS00", "TTL NAND gate"),
    ("SN74HC04", "CMOS hex inverter"),
    ("SN74HCT245", "CMOS bus transceiver"),
    ("CD4011B", "CMOS NAND gate"),
    ("CD4069UB", "CMOS hex inverter"),

    # Analog (TI / Burr-Brown)
    ("OPA2134", "Low-noise audio operational amplifier"),
    ("OPA627", "Precision operational amplifier"),
    ("TL072", "JFET-input operational amplifier"),
    ("LM358", "Dual operational amplifier"),
    ("INA128", "Instrumentation amplifier"),

    # Mixed-signal / Data converters
    ("ADS1115", "16-bit ADC with I2C interface"),
    ("DAC8562", "16-bit dual DAC"),
    ("PCM1794A", "24-bit audio DAC"),
    ("ADC0804", "8-bit ADC"),

    # Power management
    ("TPS62130", "Step-down DC-DC converter"),
    ("LM2596", "Buck regulator"),
    ("LT1763", "Low-noise LDO regulator"),

    # Dallas Semiconductor (Maxim legacy)
    ("DS1307", "Real-time clock with I2C"),
    ("DS18B20", "Digital temperature sensor"),
    ("MAX232", "RS-232 level shifter"),

    # Cypress
    ("CY7C68013A", "USB 2.0 FX2LP controller"),
    ("CY8C5888", "PSoC 5LP mixed-signal MCU"),

    # STMicroelectronics
    ("STM32F103C8", "ARM Cortex-M3 microcontroller"),
    ("STM32G431", "ARM Cortex-M4 microcontroller"),
    ("L298N", "Dual H-bridge motor driver"),

    # Freescale / NXP
    ("MC9S12DG256", "16-bit automotive microcontroller"),
    ("MPC5604B", "PowerPC automotive MCU"),
    ("LPC1768", "ARM Cortex-M3 microcontroller"),

    # FPGA / CPLD
    ("XC9572XL", "Xilinx CPLD"),
    ("XC6SLX9", "Spartan-6 FPGA"),
    ("EP2C5T144", "Altera Cyclone II FPGA"),
    ("MAX7000S", "Altera CPLD"),
]

# ----------------------------
# Load existing BOM
# ----------------------------

df_existing = pd.read_csv(INPUT_CSV)
existing_parts = set(df_existing["Part Number"].astype(str))

# ----------------------------
# Generate new BOM rows
# ----------------------------

rows = []

# while len(rows) < N_NEW_PARTS:
#     part, desc = random.choice(PART_LIBRARY)

#     # Avoid duplicates when possible
#     if part in existing_parts:
#         continue

#     rows.append({
#         "Part Number": part,
#         "Description": desc
#     })
rows = []

for _ in range(N_NEW_PARTS):
    part, desc = random.choice(PART_LIBRARY)
    rows.append({
        "Part Number": part,
        "Description": desc
    })

    existing_parts.add(part)

df_new = pd.DataFrame(rows)

# ----------------------------
# Combine and save
# ----------------------------

df_out = pd.concat([df_existing, df_new], ignore_index=True)
df_out.to_csv(OUTPUT_CSV, index=False)

print(f"✅ BOM expanded: {len(df_existing)} → {len(df_out)} parts")
print(f"📄 Output written to {OUTPUT_CSV}")
