# import os
# import easyocr
# from pdf2image import convert_from_path
# import pypdf
# from parser import extract_patient_info, extract_test_values
# from utils import save_to_csv
# from preprocessor import preprocess_image

# def extract_text_from_pdf_pypdf(pdf_path):
#     """Fallback method using PyPDF for text extraction only"""
#     print("🔄 Using PyPDF fallback method...")
#     extracted_text = ""
#     try:
#         with open(pdf_path, 'rb') as file:
#             pdf_reader = pypdf.PdfReader(file)
#             for page_num, page in enumerate(pdf_reader.pages):
#                 page_text = page.extract_text()
#                 if page_text:
#                     extracted_text += f"--- Page {page_num + 1} ---\n"
#                     extracted_text += page_text + "\n\n"
#         return extracted_text
#     except Exception as e:
#         print(f"❌ PyPDF extraction failed: {e}")
#         return ""

# def extract_text_from_pdf(pdf_path, output_folder):
#     """Main OCR extraction function with preprocessing"""
#     reader = easyocr.Reader(['en'], gpu=False)

#     # ✅ Poppler path - update this to your actual path
#     poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"

#     try:
#         print("🔄 Converting PDF to images...")
#         pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        
#         full_text = ""
#         for i, page in enumerate(pages):
#             # Save original image
#             image_path = os.path.join(output_folder, f"page_{i+1}.png")
#             page.save(image_path, "PNG")
#             print(f"📄 Saved page {i+1} as image")
            
#             # ✅ Preprocess image for better OCR
#             preprocessed_path = preprocess_image(image_path, method="medical")
            
#             # ✅ Run OCR on preprocessed image
#             result = reader.readtext(preprocessed_path, detail=0)
#             page_text = "\n".join(result)
#             full_text += f"--- Page {i+1} (OCR) ---\n" + page_text + "\n\n"
            
#             print(f"📝 Extracted {len(page_text)} characters from page {i+1}")
        
#         print("✅ PDF to image conversion and OCR successful!")
#         return full_text
        
#     except Exception as e:
#         print(f"❌ PDF to image conversion failed: {e}")
#         print("🔄 Falling back to PyPDF text extraction...")
        
#         # ✅ Fallback to PyPDF method
#         pypdf_text = extract_text_from_pdf_pypdf(pdf_path)
        
#         if pypdf_text:
#             print("✅ PyPDF extraction successful!")
#             return pypdf_text
#         else:
#             print("❌ Both extraction methods failed. Please check your PDF file.")
#             return ""

# if __name__ == "__main__":
#     print("🏥 MediVision-BI OCR Module Started")
#     print("=" * 50)
    
#     # ✅ Get absolute paths to avoid file not found issues
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     pdf_path = os.path.join(base_dir, "sample_reports", "Jane_Smith_Lab_Report.pdf")
#     output_folder = os.path.join(base_dir, "sample_reports")
#     output_csv = os.path.join(output_folder, "extracted_lab_data.csv")

#     # ✅ Create output folder if it doesn't exist
#     os.makedirs(output_folder, exist_ok=True)

#     print(f"📂 Input PDF: {pdf_path}")
#     print(f"📂 Output folder: {output_folder}")

#     # ✅ Check if PDF file exists
#     if not os.path.exists(pdf_path):
#         print(f"❌ PDF file not found: {pdf_path}")
#         print("Please place your PDF file in the sample_reports folder")
#         exit(1)

#     # ✅ Extract text from PDF
#     print(f"\n📄 Processing PDF...")
#     extracted_text = extract_text_from_pdf(pdf_path, output_folder)
    
#     if not extracted_text:
#         print("❌ No text could be extracted from the PDF.")
#         exit(1)

#     print(f"📝 Total extracted text length: {len(extracted_text)} characters")

#     # ✅ Parse patient info and test results using regex
#     print(f"\n🔍 Parsing extracted data...")
#     patient_info = extract_patient_info(extracted_text, interactive=False)
#     test_results = extract_test_values(extracted_text)

#     # ✅ Display extraction summary
#     print(f"\n📊 Extraction Summary:")
#     print(f"   Patient Name: {patient_info.get('Name', 'Not found')}")
#     print(f"   Patient ID: {patient_info.get('Patient ID', 'Not found')}")
#     print(f"   Gender: {patient_info.get('Gender', 'Not found')}")
#     print(f"   Age: {patient_info.get('Age', 'Not found')}")
#     print(f"   Test Date: {patient_info.get('Test Date', 'Not found')}")
#     print(f"   Number of lab tests found: {len(test_results)}")
    
#     if test_results:
#         print(f"   Test names: {', '.join([test['Test Name'] for test in test_results])}")

#     # ✅ Save to CSV format (as required by task)
#     print(f"\n💾 Saving data to CSV...")
#     save_to_csv(patient_info, test_results, output_csv)

#     # ✅ Save extracted text for debugging
#     text_debug_file = os.path.join(output_folder, "debug_extracted_text.txt")
#     with open(text_debug_file, 'w', encoding='utf-8') as f:
#         f.write("=== RAW EXTRACTED TEXT ===\n\n")
#         f.write(extracted_text)
#     print(f"🐛 Debug text file saved: {text_debug_file}")

#     print(f"\n✅ OCR Processing Complete!")
#     print(f"📁 CSV file ready for Member 2 (Database/Backend): {output_csv}")
#     print("=" * 50)
# import os
# import easyocr
# from pdf2image import convert_from_path
# import pypdf
# from parser import extract_patient_info, extract_test_values
# from utils import save_to_csv
# from preprocessor import preprocess_image

# def extract_text_from_pdf_pypdf(pdf_path):
#     """Fallback method using PyPDF for text extraction only"""
#     print("🔄 Using PyPDF fallback method...")
#     extracted_text = ""
#     try:
#         with open(pdf_path, 'rb') as file:
#             pdf_reader = pypdf.PdfReader(file)
#             for page_num, page in enumerate(pdf_reader.pages):
#                 page_text = page.extract_text()
#                 if page_text:
#                     extracted_text += f"--- Page {page_num + 1} ---\n"
#                     extracted_text += page_text + "\n\n"
#         return extracted_text
#     except Exception as e:
#         print(f"❌ PyPDF extraction failed: {e}")
#         return ""

# def extract_text_from_pdf(pdf_path, output_folder):
#     """Main OCR extraction function with preprocessing"""
#     reader = easyocr.Reader(['en'], gpu=False)

#     # ✅ Poppler path - update this to your actual path
#     poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"

#     try:
#         print("🔄 Converting PDF to images...")
#         pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        
#         full_text = ""
#         for i, page in enumerate(pages):
#             # Save original image
#             image_path = os.path.join(output_folder, f"page_{i+1}.png")
#             page.save(image_path, "PNG")
#             print(f"📄 Saved page {i+1} as image")
            
#             # ✅ Preprocess image for better OCR
#             preprocessed_path = preprocess_image(image_path, method="medical")
            
#             # ✅ Run OCR on preprocessed image
#             result = reader.readtext(preprocessed_path, detail=0)
#             page_text = "\n".join(result)
#             full_text += f"--- Page {i+1} (OCR) ---\n" + page_text + "\n\n"
            
#             print(f"📝 Extracted {len(page_text)} characters from page {i+1}")
        
#         print("✅ PDF to image conversion and OCR successful!")
#         return full_text
        
#     except Exception as e:
#         print(f"❌ PDF to image conversion failed: {e}")
#         print("🔄 Falling back to PyPDF text extraction...")
        
#         # ✅ Fallback to PyPDF method
#         pypdf_text = extract_text_from_pdf_pypdf(pdf_path)
        
#         if pypdf_text:
#             print("✅ PyPDF extraction successful!")
#             return pypdf_text
#         else:
#             print("❌ Both extraction methods failed. Please check your PDF file.")
#             return ""

# def prompt_for_missing_info(patient_info):
#     """Prompt user for missing patient information"""
#     print("\n🔍 Checking for missing patient information...")
    
#     required_fields = {
#         'Name': 'Patient Name',
#         'Patient ID': 'Patient ID/Medical Record Number', 
#         'Gender': 'Gender (M/F/Other)',
#         'Age': 'Age',
#         'Test Date': 'Test Date (YYYY-MM-DD or DD/MM/YYYY)'
#     }
    
#     missing_fields = []
#     for field, description in required_fields.items():
#         if not patient_info.get(field) or patient_info.get(field) == 'Not found':
#             missing_fields.append((field, description))
    
#     if missing_fields:
#         print(f"\n⚠️  {len(missing_fields)} patient details could not be extracted automatically.")
#         print("Please provide the missing information manually:\n")
        
#         for field, description in missing_fields:
#             while True:
#                 value = input(f"Enter {description}: ").strip()
#                 if value:
#                     patient_info[field] = value
#                     break
#                 else:
#                     print("❌ This field cannot be empty. Please try again.")
        
#         print("\n✅ All patient information completed!")
#     else:
#         print("✅ All required patient information was extracted successfully!")
    
#     return patient_info

# def validate_and_correct_test_results(test_results):
#     """Allow manual correction of test results if needed"""
#     if not test_results:
#         print("\n⚠️  No test results were extracted automatically.")
#         add_manual = input("Would you like to add test results manually? (y/n): ").strip().lower()
        
#         if add_manual == 'y':
#             test_results = []
#             print("\nEnter test results (press Enter with empty test name to finish):")
            
#             while True:
#                 test_name = input("\nTest Name: ").strip()
#                 if not test_name:
#                     break
                
#                 test_value = input("Test Value: ").strip()
#                 test_unit = input("Unit (optional): ").strip()
#                 reference_range = input("Reference Range (optional): ").strip()
                
#                 test_results.append({
#                     'Test Name': test_name,
#                     'Value': test_value,
#                     'Unit': test_unit if test_unit else '',
#                     'Reference Range': reference_range if reference_range else ''
#                 })
                
#                 print(f"✅ Added: {test_name} = {test_value} {test_unit}")
    
#     elif test_results:
#         print(f"\n📋 Found {len(test_results)} test results:")
#         for i, test in enumerate(test_results, 1):
#             print(f"   {i}. {test.get('Test Name', 'Unknown')} = {test.get('Value', 'N/A')} {test.get('Unit', '')}")
        
#         correct = input("\nAre these test results correct? (y/n): ").strip().lower()
#         if correct != 'y':
#             print("You can manually review and correct the CSV file after generation.")
    
#     return test_results

# if __name__ == "__main__":
#     print("🏥 MediVision-BI OCR Module Started")
#     print("=" * 50)
    
#     # ✅ Get absolute paths to avoid file not found issues
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     pdf_path = os.path.join(base_dir, "sample_reports", "Priya_Kumar_lab_report.pdf")
#     output_folder = os.path.join(base_dir, "sample_reports")
    
#     # ✅ Updated CSV output path
#     csv_output_folder = os.path.join(base_dir, "data", "processed")
#     output_csv = os.path.join(csv_output_folder, "sample_output.csv")

#     # ✅ Create output folders if they don't exist
#     os.makedirs(output_folder, exist_ok=True)
#     os.makedirs(csv_output_folder, exist_ok=True)

#     print(f"📂 Input PDF: {pdf_path}")
#     print(f"📂 Output folder: {output_folder}")
#     print(f"📂 CSV output: {output_csv}")

#     # ✅ Check if PDF file exists
#     if not os.path.exists(pdf_path):
#         print(f"❌ PDF file not found: {pdf_path}")
#         print("Please place your PDF file in the sample_reports folder")
#         exit(1)

#     # ✅ Extract text from PDF
#     print(f"\n📄 Processing PDF...")
#     extracted_text = extract_text_from_pdf(pdf_path, output_folder)
    
#     if not extracted_text:
#         print("❌ No text could be extracted from the PDF.")
#         exit(1)

#     print(f"📝 Total extracted text length: {len(extracted_text)} characters")

#     # ✅ Parse patient info and test results using regex
#     print(f"\n🔍 Parsing extracted data...")
#     patient_info = extract_patient_info(extracted_text, interactive=False)
#     test_results = extract_test_values(extracted_text)

#     # ✅ NEW: Prompt for missing patient information
#     patient_info = prompt_for_missing_info(patient_info)
    
#     # ✅ NEW: Validate and potentially correct test results
#     test_results = validate_and_correct_test_results(test_results)

#     # ✅ Display final extraction summary
#     print(f"\n📊 Final Extraction Summary:")
#     print(f"   Patient Name: {patient_info.get('Name', 'Not found')}")
#     print(f"   Patient ID: {patient_info.get('Patient ID', 'Not found')}")
#     print(f"   Gender: {patient_info.get('Gender', 'Not found')}")
#     print(f"   Age: {patient_info.get('Age', 'Not found')}")
#     print(f"   Test Date: {patient_info.get('Test Date', 'Not found')}")
#     print(f"   Number of lab tests: {len(test_results)}")
    
#     if test_results:
#         print(f"   Test names: {', '.join([test['Test Name'] for test in test_results])}")

#     # ✅ Save to CSV format (as required by task)
#     print(f"\n💾 Saving data to CSV...")
#     save_to_csv(patient_info, test_results, output_csv)

#     # ✅ Save extracted text for debugging
#     text_debug_file = os.path.join(output_folder, "debug_extracted_text.txt")
#     with open(text_debug_file, 'w', encoding='utf-8') as f:
#         f.write("=== RAW EXTRACTED TEXT ===\n\n")
#         f.write(extracted_text)
#     print(f"🐛 Debug text file saved: {text_debug_file}")

#     print(f"\n✅ OCR Processing Complete!")
#     print(f"📁 CSV file ready for Member 2 (Database/Backend): {output_csv}")
#     print("=" * 50)

# import os
# import easyocr
# from pdf2image import convert_from_path
# import pypdf
# from parser import extract_patient_info, extract_test_values
# from utils import save_to_csv
# from preprocessor import preprocess_image

# def extract_text_from_pdf_pypdf(pdf_path):
#     """Fallback method using PyPDF for text extraction only"""
#     print("🔄 Using PyPDF fallback method...")
#     extracted_text = ""
#     try:
#         with open(pdf_path, 'rb') as file:
#             pdf_reader = pypdf.PdfReader(file)
#             for page_num, page in enumerate(pdf_reader.pages):
#                 page_text = page.extract_text()
#                 if page_text:
#                     extracted_text += f"--- Page {page_num + 1} ---\n"
#                     extracted_text += page_text + "\n\n"
#         return extracted_text
#     except Exception as e:
#         print(f"❌ PyPDF extraction failed: {e}")
#         return ""

# def extract_text_from_pdf(pdf_path, output_folder):
#     """Main OCR extraction function with preprocessing"""
#     reader = easyocr.Reader(['en'], gpu=False)

#     # ✅ Poppler path - update this to your actual path
#     poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"

#     try:
#         print("🔄 Converting PDF to images...")
#         pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        
#         full_text = ""
#         for i, page in enumerate(pages):
#             # Save original image
#             image_path = os.path.join(output_folder, f"page_{i+1}.png")
#             page.save(image_path, "PNG")
#             print(f"📄 Saved page {i+1} as image")
            
#             # ✅ Preprocess image for better OCR
#             preprocessed_path = preprocess_image(image_path, method="medical")
            
#             # ✅ Run OCR on preprocessed image
#             result = reader.readtext(preprocessed_path, detail=0)
#             page_text = "\n".join(result)
#             full_text += f"--- Page {i+1} (OCR) ---\n" + page_text + "\n\n"
            
#             print(f"📝 Extracted {len(page_text)} characters from page {i+1}")
        
#         print("✅ PDF to image conversion and OCR successful!")
#         return full_text
        
#     except Exception as e:
#         print(f"❌ PDF to image conversion failed: {e}")
#         print("🔄 Falling back to PyPDF text extraction...")
        
#         # ✅ Fallback to PyPDF method
#         pypdf_text = extract_text_from_pdf_pypdf(pdf_path)
        
#         if pypdf_text:
#             print("✅ PyPDF extraction successful!")
#             return pypdf_text
#         else:
#             print("❌ Both extraction methods failed. Please check your PDF file.")
#             return ""

# def prompt_for_missing_info(patient_info):
#     """Prompt user for missing patient information"""
#     print("\n🔍 Checking for missing patient information...")
    
#     required_fields = {
#         'Name': 'Patient Name',
#         'Patient ID': 'Patient ID/Medical Record Number', 
#         'Gender': 'Gender (M/F/Other)',
#         'Age': 'Age',
#         'Test Date': 'Test Date (YYYY-MM-DD or DD/MM/YYYY)'
#     }
    
#     missing_fields = []
#     for field, description in required_fields.items():
#         if not patient_info.get(field) or patient_info.get(field) == 'Not found':
#             missing_fields.append((field, description))
    
#     if missing_fields:
#         print(f"\n⚠️  {len(missing_fields)} patient details could not be extracted automatically.")
#         print("Please provide the missing information manually:\n")
        
#         for field, description in missing_fields:
#             while True:
#                 value = input(f"Enter {description}: ").strip()
#                 if value:
#                     patient_info[field] = value
#                     break
#                 else:
#                     print("❌ This field cannot be empty. Please try again.")
        
#         print("\n✅ All patient information completed!")
#     else:
#         print("✅ All required patient information was extracted successfully!")
    
#     return patient_info

# def validate_and_correct_test_results(test_results):
#     """Allow manual correction of test results if needed"""
#     if not test_results:
#         print("\n⚠️  No test results were extracted automatically.")
#         add_manual = input("Would you like to add test results manually? (y/n): ").strip().lower()
        
#         if add_manual == 'y':
#             test_results = []
#             print("\nEnter test results (press Enter with empty test name to finish):")
            
#             while True:
#                 test_name = input("\nTest Name: ").strip()
#                 if not test_name:
#                     break
                
#                 test_value = input("Test Value: ").strip()
#                 test_unit = input("Unit (optional): ").strip()
#                 reference_range = input("Reference Range (optional): ").strip()
                
#                 test_results.append({
#                     'Test Name': test_name,
#                     'Value': test_value,
#                     'Unit': test_unit if test_unit else '',
#                     'Reference Range': reference_range if reference_range else ''
#                 })
                
#                 print(f"✅ Added: {test_name} = {test_value} {test_unit}")
    
#     elif test_results:
#         print(f"\n📋 Found {len(test_results)} test results:")
#         for i, test in enumerate(test_results, 1):
#             print(f"   {i}. {test.get('Test Name', 'Unknown')} = {test.get('Value', 'N/A')} {test.get('Unit', '')}")
        
#         correct = input("\nAre these test results correct? (y/n): ").strip().lower()
#         if correct != 'y':
#             print("\n🔧 Let's correct the test results...")
            
#             # Option to start fresh or edit existing
#             choice = input("Do you want to (1) Edit existing results or (2) Start fresh? Enter 1 or 2: ").strip()
            
#             if choice == '2':
#                 # Start fresh
#                 test_results = []
#                 print("\nEnter new test results (press Enter with empty test name to finish):")
                
#                 while True:
#                     test_name = input("\nTest Name: ").strip()
#                     if not test_name:
#                         break
                    
#                     test_value = input("Test Value: ").strip()
#                     test_unit = input("Unit (optional): ").strip()
#                     reference_range = input("Reference Range (optional): ").strip()
                    
#                     test_results.append({
#                         'Test Name': test_name,
#                         'Value': test_value,
#                         'Unit': test_unit if test_unit else '',
#                         'Reference Range': reference_range if reference_range else ''
#                     })
                    
#                     print(f"✅ Added: {test_name} = {test_value} {test_unit}")
            
#             else:
#                 # Edit existing results
#                 print("\nEditing existing results (press Enter to keep current value):")
#                 for i, test in enumerate(test_results):
#                     print(f"\n--- Editing Test {i+1} ---")
#                     print(f"Current: {test.get('Test Name', '')} = {test.get('Value', '')} {test.get('Unit', '')}")
                    
#                     new_name = input(f"Test Name [{test.get('Test Name', '')}]: ").strip()
#                     new_value = input(f"Test Value [{test.get('Value', '')}]: ").strip()
#                     new_unit = input(f"Unit [{test.get('Unit', '')}]: ").strip()
#                     new_range = input(f"Reference Range [{test.get('Reference Range', '')}]: ").strip()
                    
#                     # Update only if new values provided
#                     if new_name:
#                         test_results[i]['Test Name'] = new_name
#                     if new_value:
#                         test_results[i]['Value'] = new_value
#                     if new_unit:
#                         test_results[i]['Unit'] = new_unit
#                     if new_range:
#                         test_results[i]['Reference Range'] = new_range
                
#                 print("\n✅ Test results updated!")
    
#     return test_results

# if __name__ == "__main__":
#     print("🏥 MediVision-BI OCR Module Started")
#     print("=" * 50)
    
#     # ✅ Get absolute paths to avoid file not found issues
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     pdf_path = os.path.join(base_dir, "sample_reports", "Jane_Smith_Lab_Report.pdf")
#     output_folder = os.path.join(base_dir, "sample_reports")
    
#     # ✅ Generate unique CSV filename based on PDF name and timestamp
#     import datetime
    
#     pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]  # Get PDF name without extension
#     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#     csv_filename = f"{pdf_filename}_{timestamp}.csv"
    
#     csv_output_folder = os.path.join(base_dir, "data", "processed")
#     output_csv = os.path.join(csv_output_folder, csv_filename)

#     # ✅ Create output folders if they don't exist
#     os.makedirs(output_folder, exist_ok=True)
#     os.makedirs(csv_output_folder, exist_ok=True)

#     print(f"📂 Input PDF: {pdf_path}")
#     print(f"📂 Output folder: {output_folder}")
#     print(f"📂 CSV output: {output_csv}")

#     # ✅ Check if PDF file exists
#     if not os.path.exists(pdf_path):
#         print(f"❌ PDF file not found: {pdf_path}")
#         print("Please place your PDF file in the sample_reports folder")
#         exit(1)

#     # ✅ Extract text from PDF
#     print(f"\n📄 Processing PDF...")
#     extracted_text = extract_text_from_pdf(pdf_path, output_folder)
    
#     if not extracted_text:
#         print("❌ No text could be extracted from the PDF.")
#         exit(1)

#     print(f"📝 Total extracted text length: {len(extracted_text)} characters")

#     # ✅ Parse patient info and test results using regex
#     print(f"\n🔍 Parsing extracted data...")
#     patient_info = extract_patient_info(extracted_text, interactive=False)
#     test_results = extract_test_values(extracted_text)

#     # ✅ NEW: Prompt for missing patient information
#     patient_info = prompt_for_missing_info(patient_info)
    
#     # ✅ NEW: Validate and potentially correct test results
#     test_results = validate_and_correct_test_results(test_results)

#     # ✅ Display final extraction summary
#     print(f"\n📊 Final Extraction Summary:")
#     print(f"   Patient Name: {patient_info.get('Name', 'Not found')}")
#     print(f"   Patient ID: {patient_info.get('Patient ID', 'Not found')}")
#     print(f"   Gender: {patient_info.get('Gender', 'Not found')}")
#     print(f"   Age: {patient_info.get('Age', 'Not found')}")
#     print(f"   Test Date: {patient_info.get('Test Date', 'Not found')}")
#     print(f"   Number of lab tests: {len(test_results)}")
    
#     if test_results:
#         print(f"   Test names: {', '.join([test['Test Name'] for test in test_results])}")

#     # ✅ Save to CSV format (as required by task)
#     print(f"\n💾 Saving data to CSV...")
#     save_to_csv(patient_info, test_results, output_csv)

#     # ✅ Save extracted text for debugging
#     text_debug_file = os.path.join(output_folder, "debug_extracted_text.txt")
#     with open(text_debug_file, 'w', encoding='utf-8') as f:
#         f.write("=== RAW EXTRACTED TEXT ===\n\n")
#         f.write(extracted_text)
#     print(f"🐛 Debug text file saved: {text_debug_file}")

#     print(f"\n✅ OCR Processing Complete!")
#     print(f"📁 CSV file ready for Member 2 (Database/Backend): {output_csv}")
#     print("=" * 50)

import os
import easyocr
from pdf2image import convert_from_path
import pypdf
from parser import extract_patient_info, extract_test_values
from utils import save_to_csv
from preprocessor import preprocess_image
import datetime
import glob
import re

def extract_text_from_pdf_pypdf(pdf_path):
    """Fallback method using PyPDF for text extraction only"""
    print("🔄 Using PyPDF fallback method...")
    extracted_text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_text += f"--- Page {page_num + 1} ---\n"
                    extracted_text += page_text + "\n\n"
        return extracted_text
    except Exception as e:
        print(f"❌ PyPDF extraction failed: {e}")
        return ""

def extract_text_from_pdf(pdf_path, output_folder):
    """Main OCR extraction function with preprocessing"""
    reader = easyocr.Reader(['en'], gpu=False)

    # ✅ Poppler path - update this to your actual path
    poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"

    try:
        print("🔄 Converting PDF to images...")
        pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        
        full_text = ""
        for i, page in enumerate(pages):
            # Save original image
            image_path = os.path.join(output_folder, f"page_{i+1}.png")
            page.save(image_path, "PNG")
            print(f"📄 Saved page {i+1} as image")
            
            # ✅ Preprocess image for better OCR
            preprocessed_path = preprocess_image(image_path, method="medical")
            
            # ✅ Run OCR on preprocessed image
            result = reader.readtext(preprocessed_path, detail=0)
            page_text = "\n".join(result)
            full_text += f"--- Page {i+1} (OCR) ---\n" + page_text + "\n\n"
            
            print(f"📝 Extracted {len(page_text)} characters from page {i+1}")
        
        print("✅ PDF to image conversion and OCR successful!")
        return full_text
        
    except Exception as e:
        print(f"❌ PDF to image conversion failed: {e}")
        print("🔄 Falling back to PyPDF text extraction...")
        
        # ✅ Fallback to PyPDF method
        pypdf_text = extract_text_from_pdf_pypdf(pdf_path)
        
        if pypdf_text:
            print("✅ PyPDF extraction successful!")
            return pypdf_text
        else:
            print("❌ Both extraction methods failed. Please check your PDF file.")
            return ""

def prompt_for_missing_info(patient_info, pdf_filename):
    """Prompt user for missing patient information"""
    print(f"\n🔍 Checking for missing patient information for {pdf_filename}...")
    
    required_fields = {
        'Name': 'Patient Name',
        'Patient ID': 'Patient ID/Medical Record Number', 
        'Gender': 'Gender (M/F/Other)',
        'Age': 'Age',
        'Test Date': 'Test Date (YYYY-MM-DD or DD/MM/YYYY)'
    }
    
    missing_fields = []
    for field, description in required_fields.items():
        if not patient_info.get(field) or patient_info.get(field) == 'Not found':
            missing_fields.append((field, description))
    
    if missing_fields:
        print(f"\n⚠️  {len(missing_fields)} patient details could not be extracted automatically.")
        print("Please provide the missing information manually:\n")
        
        for field, description in missing_fields:
            while True:
                value = input(f"Enter {description}: ").strip()
                if value:
                    patient_info[field] = value
                    break
                else:
                    print("❌ This field cannot be empty. Please try again.")
        
        print("\n✅ All patient information completed!")
    else:
        print("✅ All required patient information was extracted successfully!")
    
    return patient_info

def validate_and_correct_test_results(test_results, pdf_filename):
    """Allow manual correction of test results if needed"""
    print(f"\n📋 Processing test results for {pdf_filename}...")
    
    if not test_results:
        print("\n⚠️  No test results were extracted automatically.")
        add_manual = input("Would you like to add test results manually? (y/n): ").strip().lower()
        
        if add_manual == 'y':
            test_results = []
            print("\nEnter test results (press Enter with empty test name to finish):")
            
            while True:
                test_name = input("\nTest Name: ").strip()
                if not test_name:
                    break
                
                test_value = input("Test Value: ").strip()
                test_unit = input("Unit (optional): ").strip()
                reference_range = input("Reference Range (optional): ").strip()
                
                test_results.append({
                    'Test Name': test_name,
                    'Value': test_value,
                    'Unit': test_unit if test_unit else '',
                    'Reference Range': reference_range if reference_range else ''
                })
                
                print(f"✅ Added: {test_name} = {test_value} {test_unit}")
    
    elif test_results:
        print(f"\n📋 Found {len(test_results)} test results:")
        for i, test in enumerate(test_results, 1):
            print(f"   {i}. {test.get('Test Name', 'Unknown')} = {test.get('Value', 'N/A')} {test.get('Unit', '')}")
        
        correct = input("\nAre these test results correct? (y/n): ").strip().lower()
        if correct != 'y':
            print("\n🔧 Let's correct the test results...")
            
            # Option to start fresh or edit existing
            choice = input("Do you want to (1) Edit existing results or (2) Start fresh? Enter 1 or 2: ").strip()
            
            if choice == '2':
                # Start fresh
                test_results = []
                print("\nEnter new test results (press Enter with empty test name to finish):")
                
                while True:
                    test_name = input("\nTest Name: ").strip()
                    if not test_name:
                        break
                    
                    test_value = input("Test Value: ").strip()
                    test_unit = input("Unit (optional): ").strip()
                    reference_range = input("Reference Range (optional): ").strip()
                    
                    test_results.append({
                        'Test Name': test_name,
                        'Value': test_value,
                        'Unit': test_unit if test_unit else '',
                        'Reference Range': reference_range if reference_range else ''
                    })
                    
                    print(f"✅ Added: {test_name} = {test_value} {test_unit}")
            
            else:
                # Edit existing results
                print("\nEditing existing results (press Enter to keep current value):")
                for i, test in enumerate(test_results):
                    print(f"\n--- Editing Test {i+1} ---")
                    print(f"Current: {test.get('Test Name', '')} = {test.get('Value', '')} {test.get('Unit', '')}")
                    
                    new_name = input(f"Test Name [{test.get('Test Name', '')}]: ").strip()
                    new_value = input(f"Test Value [{test.get('Value', '')}]: ").strip()
                    new_unit = input(f"Unit [{test.get('Unit', '')}]: ").strip()
                    new_range = input(f"Reference Range [{test.get('Reference Range', '')}]: ").strip()
                    
                    # Update only if new values provided
                    if new_name:
                        test_results[i]['Test Name'] = new_name
                    if new_value:
                        test_results[i]['Value'] = new_value
                    if new_unit:
                        test_results[i]['Unit'] = new_unit
                    if new_range:
                        test_results[i]['Reference Range'] = new_range
                
                print("\n✅ Test results updated!")
    
    return test_results

def sanitize_filename(filename):
    """Remove or replace invalid characters for filenames"""
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove extra spaces and replace with underscores
    filename = re.sub(r'\s+', '_', filename.strip())
    
    # Limit length to avoid filesystem issues
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename

def generate_output_filename(patient_info, timestamp):
    """Generate CSV filename based on patient name and ID"""
    name = patient_info.get('Name', 'Unknown_Patient')
    patient_id = patient_info.get('Patient ID', 'Unknown_ID')
    
    # Sanitize the name and ID for filename use
    safe_name = sanitize_filename(name)
    safe_id = sanitize_filename(str(patient_id))
    
    # Create filename: PatientName_PatientID_timestamp.csv
    filename = f"{safe_name}_{safe_id}_{timestamp}.csv"
    
    return filename

def get_pdf_files(directory):
    """Get all PDF files from the specified directory"""
    pdf_pattern = os.path.join(directory, "*.pdf")
    pdf_files = glob.glob(pdf_pattern)
    return pdf_files

def process_single_report(pdf_path, output_folder, csv_output_folder):
    """Process a single PDF report"""
    pdf_filename = os.path.basename(pdf_path)
    print(f"\n{'='*60}")
    print(f"📄 Processing: {pdf_filename}")
    print(f"{'='*60}")
    
    # Create a subfolder for this PDF's images
    pdf_name_without_ext = os.path.splitext(pdf_filename)[0]
    pdf_output_folder = os.path.join(output_folder, pdf_name_without_ext)
    os.makedirs(pdf_output_folder, exist_ok=True)
    
    # ✅ Extract text from PDF
    print(f"📄 Processing PDF...")
    extracted_text = extract_text_from_pdf(pdf_path, pdf_output_folder)
    
    if not extracted_text:
        print(f"❌ No text could be extracted from {pdf_filename}. Skipping...")
        return False
    
    print(f"📝 Total extracted text length: {len(extracted_text)} characters")
    
    # ✅ Parse patient info and test results using regex
    print(f"🔍 Parsing extracted data...")
    patient_info = extract_patient_info(extracted_text, interactive=False)
    test_results = extract_test_values(extracted_text)
    
    # ✅ Prompt for missing patient information
    patient_info = prompt_for_missing_info(patient_info, pdf_filename)
    
    # ✅ Validate and potentially correct test results
    test_results = validate_and_correct_test_results(test_results, pdf_filename)
    
    # ✅ Generate timestamp and output filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = generate_output_filename(patient_info, timestamp)
    output_csv = os.path.join(csv_output_folder, csv_filename)
    
    # ✅ Display final extraction summary
    print(f"\n📊 Final Extraction Summary for {pdf_filename}:")
    print(f"   Patient Name: {patient_info.get('Name', 'Not found')}")
    print(f"   Patient ID: {patient_info.get('Patient ID', 'Not found')}")
    print(f"   Gender: {patient_info.get('Gender', 'Not found')}")
    print(f"   Age: {patient_info.get('Age', 'Not found')}")
    print(f"   Test Date: {patient_info.get('Test Date', 'Not found')}")
    print(f"   Number of lab tests: {len(test_results)}")
    
    if test_results:
        print(f"   Test names: {', '.join([test['Test Name'] for test in test_results])}")
    
    # ✅ Save to CSV format
    print(f"💾 Saving data to CSV: {csv_filename}")
    save_to_csv(patient_info, test_results, output_csv)
    
    # ✅ Save extracted text for debugging
    text_debug_file = os.path.join(pdf_output_folder, "debug_extracted_text.txt")
    with open(text_debug_file, 'w', encoding='utf-8') as f:
        f.write(f"=== RAW EXTRACTED TEXT FROM {pdf_filename} ===\n\n")
        f.write(extracted_text)
    print(f"🐛 Debug text file saved: {text_debug_file}")
    
    print(f"✅ Successfully processed {pdf_filename}")
    return True

if __name__ == "__main__":
    print("🏥 MediVision-BI Multi-Report OCR Module Started")
    print("=" * 60)
    
    # ✅ Get absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    reports_folder = os.path.join(base_dir, "sample_reports")
    output_folder = os.path.join(base_dir, "sample_reports", "extracted_images")
    csv_output_folder = os.path.join(base_dir, "data", "processed")
    
    # ✅ Create output folders if they don't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(csv_output_folder, exist_ok=True)
    
    print(f"📂 Reports folder: {reports_folder}")
    print(f"📂 Images output folder: {output_folder}")
    print(f"📂 CSV output folder: {csv_output_folder}")
    
    # ✅ Get all PDF files from the reports folder
    pdf_files = get_pdf_files(reports_folder)
    
    if not pdf_files:
        print(f"❌ No PDF files found in {reports_folder}")
        print("Please place your PDF files in the sample_reports folder")
        exit(1)
    
    print(f"\n📋 Found {len(pdf_files)} PDF files to process:")
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"   {i}. {os.path.basename(pdf_path)}")
    
    # Ask user if they want to process all files
    process_all = input(f"\nDo you want to process all {len(pdf_files)} files? (y/n): ").strip().lower()
    
    if process_all != 'y':
        print("Operation cancelled by user.")
        exit(0)
    
    # ✅ Process each PDF file
    successful_count = 0
    failed_count = 0
    
    for i, pdf_path in enumerate(pdf_files, 1):
        try:
            print(f"\n🔄 Processing file {i}/{len(pdf_files)}")
            success = process_single_report(pdf_path, output_folder, csv_output_folder)
            
            if success:
                successful_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            print(f"❌ Error processing {os.path.basename(pdf_path)}: {e}")
            failed_count += 1
    
    # ✅ Final summary
    print(f"\n{'='*60}")
    print(f"🎉 BATCH PROCESSING COMPLETE!")
    print(f"{'='*60}")
    print(f"✅ Successfully processed: {successful_count} files")
    print(f"❌ Failed to process: {failed_count} files")
    print(f"📁 All CSV files saved in: {csv_output_folder}")
    print(f"📁 All extracted images saved in: {output_folder}")
    
    if successful_count > 0:
        print(f"\n📄 Generated CSV files:")
        csv_files = glob.glob(os.path.join(csv_output_folder, "*.csv"))
        # Sort by modification time to show most recent first
        csv_files.sort(key=os.path.getmtime, reverse=True)
        
        for csv_file in csv_files[:successful_count]:  # Show only the recently created ones
            print(f"   • {os.path.basename(csv_file)}")
    
    print("=" * 60)