import csv

INPUT_CSV = "walletswithweight.csv"
OUTPUT_CSV = "wallets_cleaned.csv"
MAX_VALUES = 26
MAX_OUTPUTS = 26

with open(INPUT_CSV, "r", newline="") as infile, open(OUTPUT_CSV, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write header
    header = ["Input"] + [f"Value{i+1}" for i in range(MAX_VALUES)] + [f"Output{i+1}" for i in range(MAX_OUTPUTS)]
    writer.writerow(header)

    for row in reader:
        if not row or not row[0].strip():
            continue  # Skip empty rows

        input_wallet = row[0].strip()
        rest = [item.strip() for item in row[1:] if item.strip() != ""]

        values = [x for x in rest if "." in x]
        outputs = [x for x in rest if "." not in x]

        # Pad with empty strings to ensure 26 values and 26 outputs
        values = values[:MAX_VALUES] + [""] * (MAX_VALUES - len(values))
        outputs = outputs[:MAX_OUTPUTS] + [""] * (MAX_OUTPUTS - len(outputs))

        cleaned_row = [input_wallet] + values + outputs
        writer.writerow(cleaned_row)

print(f"✅ Cleaned CSV written to {OUTPUT_CSV}")
