import re

def extract_patient_info(text, interactive=False):
    """
    Extract patient information from text
    
    Args:
        text (str): Raw extracted text from PDF
        interactive (bool): If True, prompts user for missing info. If False, returns empty string.
    """
    def extract(pattern, fallback_label, fallback_patterns=None):
        # Try primary pattern
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Try fallback patterns if provided
        if fallback_patterns:
            for fallback_pattern in fallback_patterns:
                match = re.search(fallback_pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    return match.group(1).strip()
        
        # Interactive fallback or empty string
        if interactive:
            return input(f"{fallback_label}: ").strip()
        else:
            print(f"⚠️ Could not find: {fallback_label}")
            return ""

    return {
        "Patient ID": extract(
            r"Patient\s*ID[:\s]*([A-Za-z0-9\-]+)", 
            "Enter Patient ID",
            [r"ID[:\s]*([A-Za-z0-9\-]+)", r"Patient\s*No[:\s]*([A-Za-z0-9\-]+)"]
        ),
        "Name": extract(
            r"Name[:\s]*([A-Za-z\s]+(?:\n[A-Za-z\s]+)*)", 
            "Enter Patient Name",
            [r"Patient[:\s]*([A-Za-z\s]+)", r"Mr\.|Ms\.|Mrs\.\s*([A-Za-z\s]+)"]
        ),
        "Gender": extract(
            r"Gender[:\s]*([A-Za-z]+)", 
            "Enter Gender",
            [r"Sex[:\s]*([A-Za-z]+)", r"\b(Male|Female|M|F)\b"]
        ),
        "Age": extract(
            r"Age[:\s]*([\d]+)", 
            "Enter Age",
            [r"(\d+)\s*(?:years?|yrs?|Y)", r"Age:\s*(\d+)"]
        ),
        "Height": extract(
            r"Height[:\s]*([\d.]+)", 
            "Enter Height (cm)",
            [r"(\d+\.?\d*)\s*cm", r"Height:\s*([\d.]+)"]
        ),
        "Weight": extract(
            r"Weight[:\s]*([\d.]+)", 
            "Enter Weight (kg)",
            [r"(\d+\.?\d*)\s*kg", r"Weight:\s*([\d.]+)"]
        ),
        "Test Date": extract(
            r"Test Date[:\s]*([\d\-\/\.]+)", 
            "Enter Test Date",
            [r"Date[:\s]*([\d\-\/\.]+)", r"(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})"]
        ),
        "Previous Test Date": extract(
            r"Previous Test Date[:\s]*([\d\-\/\.]+)", 
            "Enter Previous Test Date",
            [r"Last Test[:\s]*([\d\-\/\.]+)", r"Previous[:\s]*([\d\-\/\.]+)"]
        )
    }

def extract_test_values(text):
    """
    Extract test values from text with improved pattern matching
    """
    # Enhanced patterns with multiple variations
    patterns = {
        "Hemoglobin": {
            "patterns": [
                r"Hemoglobin[:\s]+([\d.]+)",
                r"Hb[:\s]+([\d.]+)", 
                r"HGB[:\s]+([\d.]+)"
            ],
            "unit": "g/dL",
            "reference": "12-16"
        },
        "WBC": {
            "patterns": [
                r"WBC[:\s]+([\d,]+)",
                r"White Blood Cell[s]?[:\s]+([\d,]+)",
                r"Total WBC[:\s]+([\d,]+)"
            ],
            "unit": "cells/cu mm",
            "reference": "4000-11000"
        },
        "Creatinine": {
            "patterns": [
                r"Creatinine[:\s]+([\d.]+)",
                r"Serum Creatinine[:\s]+([\d.]+)"
            ],
            "unit": "mg/dL",
            "reference": "0.6-1.2"
        },
        "Blood Urea Nitrogen": {
            "patterns": [
                r"Blood Urea Nitrogen[:\s]+([\d.]+)",
                r"BUN[:\s]+([\d.]+)"
            ],
            "unit": "mg/dL",
            "reference": "7-20"
        },
        "Alkaline Phosphatase": {
            "patterns": [
                r"Alkaline Phosphatase[:\s]+([\d.]+)",
                r"ALP[:\s]+([\d.]+)"
            ],
            "unit": "U/L",
            "reference": "44-147"
        },
        "Bilirubin": {
            "patterns": [
                r"Bilirubin[:\s]+([\d.]+)",
                r"Total Bilirubin[:\s]+([\d.]+)"
            ],
            "unit": "mg/dL",
            "reference": "0.1-1.2"
        },
        "Platelet Count": {
            "patterns": [
                r"Platelet Count[:\s]+([\d.]+)",
                r"Platelets[:\s]+([\d.]+)",
                r"PLT[:\s]+([\d.]+)"
            ],
            "unit": "lakh/cu mm",
            "reference": "1.5-4.0"
        },
        "Blood Sugar (Fasting)": {
            "patterns": [
                r"Blood Sugar \(Fasting\)[:\s]+([\d.]+)",
                r"Fasting Blood Sugar[:\s]+([\d.]+)",
                r"FBS[:\s]+([\d.]+)",
                r"Glucose \(Fasting\)[:\s]+([\d.]+)"
            ],
            "unit": "mg/dL",
            "reference": "70-110"
        },
        "Cholesterol": {
            "patterns": [
                r"Cholesterol[:\s]+([\d.]+)",
                r"Total Cholesterol[:\s]+([\d.]+)",
                r"CHOL[:\s]+([\d.]+)"
            ],
            "unit": "mg/dL",
            "reference": "<200"
        },
        "HDL Cholesterol": {
            "patterns": [
                r"HDL Cholesterol[:\s]+([\d.]+)",
                r"HDL[:\s]+([\d.]+)"
            ],
            "unit": "mg/dL",
            "reference": ">40"
        },
        "LDL Cholesterol": {
            "patterns": [
                r"LDL Cholesterol[:\s]+([\d.]+)",
                r"LDL[:\s]+([\d.]+)"
            ],
            "unit": "mg/dL",
            "reference": "<100"
        },
        "Triglycerides": {
            "patterns": [
                r"Triglycerides[:\s]+([\d.]+)",
                r"TG[:\s]+([\d.]+)"
            ],
            "unit": "mg/dL",
            "reference": "<150"
        }
    }

    results = []
    found_tests = []

    for test_name, test_info in patterns.items():
        for pattern in test_info["patterns"]:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                value = match.group(1).replace(',', '')  # Remove commas from numbers
                results.append({
                    "Test Name": test_name,
                    "Value": value,
                    "Unit": test_info["unit"],
                    "Reference Range": test_info["reference"]
                })
                found_tests.append(test_name)
                break  # Stop after first match for this test
    
    print(f"✅ Found {len(results)} test results: {', '.join(found_tests)}")
    
    # Look for any other numeric values that might be tests
    additional_tests = find_additional_tests(text, found_tests)
    results.extend(additional_tests)
    
    return results

def find_additional_tests(text, already_found):
    """
    Look for additional test patterns that weren't caught by main patterns
    """
    additional_results = []
    
    # Generic pattern for test_name: value unit
    generic_pattern = r"([A-Za-z\s]+)[:\s]+([\d.]+)\s*([A-Za-z\/]+)?"
    matches = re.findall(generic_pattern, text, re.IGNORECASE)
    
    for test_name, value, unit in matches:
        test_name = test_name.strip()
        
        # Skip if already found or if it's not likely a test
        if (test_name in already_found or 
            len(test_name) < 3 or 
            any(skip_word in test_name.lower() for skip_word in ['patient', 'name', 'age', 'date', 'time'])):
            continue
        
        # Only include if it looks like a medical test
        if any(keyword in test_name.lower() for keyword in ['level', 'count', 'rate', 'ratio', 'index']):
            additional_results.append({
                "Test Name": test_name,
                "Value": value,
                "Unit": unit if unit else "",
                "Reference Range": "Not specified"
            })
    
    if additional_results:
        additional_names = [test["Test Name"] for test in additional_results]
        print(f"🔍 Found additional tests: {', '.join(additional_names)}")
    
    return additional_results

def debug_extraction(text):
    """
    Debug function to help identify what's in the extracted text
    """
    print("=== DEBUG: Text Analysis ===")
    print(f"Text length: {len(text)} characters")
    print(f"Number of lines: {len(text.split('\\n'))}")
    
    # Look for common medical test keywords
    keywords = ['hemoglobin', 'wbc', 'platelet', 'glucose', 'cholesterol', 'patient', 'name', 'age']
    found_keywords = []
    
    for keyword in keywords:
        if re.search(keyword, text, re.IGNORECASE):
            found_keywords.append(keyword)
    
    print(f"Found keywords: {', '.join(found_keywords)}")
    
    # Show first few lines of text
    lines = text.split('\\n')[:10]
    print("\\nFirst 10 lines of extracted text:")
    for i, line in enumerate(lines, 1):
        print(f"{i:2d}: {line[:80]}...")  # Show first 80 chars of each line