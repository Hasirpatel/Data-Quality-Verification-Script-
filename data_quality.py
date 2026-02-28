import csv
import json

REQUIRED_FIELDS = ["id", "name", "email", "age"]

def validate_record(record, index):
    errors = []
    for field in REQUIRED_FIELDS:
        value = record.get(field)
        if value is None or str(value).strip() == "":
            errors.append(f"Missing value in field: '{field}'")
    if record.get("email") and "@" not in str(record.get("email")):
        errors.append("Invalid email format")
    if record.get("age"):
        try:
            int(float(str(record.get("age"))))
        except:
            errors.append("Invalid age format")
    return errors

def validate_csv(filepath):
    print(f"\nValidating CSV: {filepath}")
    total = valid = invalid = 0
    results = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            total += 1
            errors = validate_record(row, i)
            if errors:
                invalid += 1
                results.append({"record": i, "status": "Invalid", "errors": ", ".join(errors)})
            else:
                valid += 1
                results.append({"record": i, "status": "Valid", "errors": ""})
    print(f"Total: {total} | Valid: {valid} | Invalid: {invalid}")
    return results, total, valid, invalid

def validate_json(filepath):
    print(f"\nValidating JSON: {filepath}")
    total = valid = invalid = 0
    results = []
    with open(filepath) as f:
        data = json.load(f)
    for i, record in enumerate(data, start=1):
        total += 1
        errors = validate_record(record, i)
        if errors:
            invalid += 1
            results.append({"record": i, "status": "Invalid", "errors": ", ".join(errors)})
        else:
            valid += 1
            results.append({"record": i, "status": "Valid", "errors": ""})
    print(f"Total: {total} | Valid: {valid} | Invalid: {invalid}")
    return results, total, valid, invalid

def export_report(results, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["record", "status", "errors"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Report exported: {filename}")

def main():
    csv_results, csv_total, csv_valid, csv_invalid = validate_csv("sample.csv")
    export_report(csv_results, "csv_quality_report.csv")

    json_results, json_total, json_valid, json_invalid = validate_json("sample.json")
    export_report(json_results, "json_quality_report.csv")

    print("\n--- SUMMARY ---")
    print(f"CSV  → Total: {csv_total} | Valid: {csv_valid} | Invalid: {csv_invalid}")
    print(f"JSON → Total: {json_total} | Valid: {json_valid} | Invalid: {json_invalid}")

main()