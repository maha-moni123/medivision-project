import csv
import os

def save_to_csv(patient_info, test_data, filename):
    """
    Save patient info and test data to CSV file
    
    Args:
        patient_info (dict): Dictionary containing patient information
        test_data (list): List of dictionaries containing test results
        filename (str): Output CSV filename
    """
    if not test_data:
        print("⚠️ No test data to save.")
        return False

    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = [
                "Patient ID", "Name", "Gender", "Age", "Height", "Weight",
                "Test Date", "Previous Test Date",
                "Test Name", "Value", "Unit", "Reference Range"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # Write data rows
            rows_written = 0
            for row in test_data:
                try:
                    merged = {**patient_info, **row}
                    writer.writerow(merged)
                    rows_written += 1
                except Exception as e:
                    print(f"⚠️ Warning: Could not write row {row}: {e}")
                    continue

        print(f"📁 CSV saved: {filename}")
        print(f"✅ {rows_written} test results saved successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")
        return False

def save_debug_info(extracted_text, patient_info, test_data, output_folder):
    """
    Save debug information to help troubleshoot parsing issues
    
    Args:
        extracted_text (str): Raw extracted text
        patient_info (dict): Parsed patient information
        test_data (list): Parsed test results
        output_folder (str): Output directory
    """
    try:
        # Save raw extracted text
        text_file = os.path.join(output_folder, "debug_extracted_text.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("=== RAW EXTRACTED TEXT ===\n\n")
            f.write(extracted_text)
        
        # Save parsed data summary
        debug_file = os.path.join(output_folder, "debug_parsed_data.txt")
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write("=== PARSED PATIENT INFO ===\n")
            for key, value in patient_info.items():
                f.write(f"{key}: {value}\n")
            
            f.write(f"\n=== PARSED TEST RESULTS ({len(test_data)} tests) ===\n")
            for i, test in enumerate(test_data, 1):
                f.write(f"\nTest {i}:\n")
                for key, value in test.items():
                    f.write(f"  {key}: {value}\n")
        
        print(f"🐛 Debug files saved in: {output_folder}")
        
    except Exception as e:
        print(f"⚠️ Could not save debug info: {e}")

def validate_data(patient_info, test_data):
    """
    Validate extracted data for completeness
    
    Args:
        patient_info (dict): Patient information
        test_data (list): Test results
        
    Returns:
        bool: True if data seems valid, False otherwise
    """
    issues = []
    
    # Check patient info
    required_patient_fields = ["Name", "Patient ID"]
    for field in required_patient_fields:
        if not patient_info.get(field):
            issues.append(f"Missing patient {field}")
    
    # Check test data
    if not test_data:
        issues.append("No test results found")
    else:
        for i, test in enumerate(test_data):
            if not test.get("Test Name"):
                issues.append(f"Test {i+1}: Missing test name")
            if not test.get("Value"):
                issues.append(f"Test {i+1}: Missing test value")
    
    if issues:
        print("⚠️ Data validation issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Data validation passed")
        return True