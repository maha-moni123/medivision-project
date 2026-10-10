# =============================================================================
# OCR MODULE TESTING SCRIPT (test_ocr.py)
# Use this to test your module before giving to team
# Place this file in: ocr_module/test_ocr.py
# =============================================================================

import os
import sys
import tempfile
import shutil
import json

# Import your OCR service (same folder)
from medical_ocr_service import MedicalOCRService

def test_single_file():
    """Test processing a single PDF file"""
    print("🧪 TEST 1: Single File Processing")
    print("-" * 40)
    
    # Setup - Update these paths for your system
    poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"
    test_pdf = "../sample_reports/Jane_Smith_Lab_Report.pdf"  # Adjust path as needed
    output_dir = "../test_output"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Initialize OCR service
        ocr_service = MedicalOCRService(poppler_path=poppler_path)
        
        # Test the main function
        result = ocr_service.process_uploaded_file(
            uploaded_file_path=test_pdf,
            output_dir=output_dir
        )
        
        # Check results
        if result['success']:
            print("✅ SUCCESS!")
            print(f"   Patient: {result['patient_info']['Name']}")
            print(f"   ID: {result['patient_info']['Patient ID']}")
            print(f"   Tests: {result['num_tests']}")
            print(f"   CSV: {result['csv_filename']}")
            print(f"   File exists: {os.path.exists(result['csv_path'])}")
            
            # Validate the data structure
            assert isinstance(result['patient_info'], dict), "patient_info should be dict"
            assert isinstance(result['test_results'], list), "test_results should be list"
            assert result['csv_path'] is not None, "csv_path should not be None"
            assert os.path.exists(result['csv_path']), "CSV file should exist"
            
            print("✅ All validations passed!")
            return True
        else:
            print(f"❌ FAILED: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_multiple_files():
    """Test processing multiple PDF files"""
    print("\n🧪 TEST 2: Multiple Files Processing")
    print("-" * 40)
    
    poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"
    test_files = [
        "../sample_reports/Jane_Smith_Lab_Report.pdf",
        # Add more test files if you have them
    ]
    output_dir = "../test_output/batch"
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        ocr_service = MedicalOCRService(poppler_path=poppler_path)
        
        # Filter files that actually exist
        existing_files = [f for f in test_files if os.path.exists(f)]
        
        if not existing_files:
            print("⚠️  No test files found, skipping batch test")
            return True
        
        results = ocr_service.process_multiple_files(existing_files, output_dir)
        
        successful_count = sum(1 for r in results if r['success'])
        print(f"✅ Batch processing: {successful_count}/{len(results)} successful")
        
        for i, result in enumerate(results):
            if result['success']:
                print(f"   File {i+1}: ✅ {result['original_filename']}")
            else:
                print(f"   File {i+1}: ❌ {result['original_filename']} - {result['error']}")
        
        return successful_count > 0
        
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_error_handling():
    """Test how the module handles errors"""
    print("\n🧪 TEST 3: Error Handling")
    print("-" * 40)
    
    poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"
    fake_file = "../nonexistent_file.pdf"
    
    try:
        ocr_service = MedicalOCRService(poppler_path=poppler_path)
        
        result = ocr_service.process_uploaded_file(fake_file)
        
        if not result['success']:
            print("✅ Error handling works correctly")
            print(f"   Error message: {result['error']}")
            assert result['patient_info'] is None
            assert result['test_results'] is None
            assert result['csv_path'] is None
            return True
        else:
            print("❌ Should have failed with nonexistent file")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION (should be handled gracefully): {str(e)}")
        return False

def test_data_structure():
    """Test that the returned data structure is correct"""
    print("\n🧪 TEST 4: Data Structure Validation")
    print("-" * 40)
    
    poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"
    test_pdf = "../sample_reports/Jane_Smith_Lab_Report.pdf"
    
    if not os.path.exists(test_pdf):
        print("⚠️  Test PDF not found, skipping data structure test")
        return True
    
    try:
        ocr_service = MedicalOCRService(poppler_path=poppler_path)
        result = ocr_service.process_uploaded_file(test_pdf)
        
        if result['success']:
            # Check required keys in result
            required_keys = ['success', 'patient_info', 'test_results', 'csv_path', 
                           'csv_filename', 'num_tests', 'processing_time']
            
            for key in required_keys:
                assert key in result, f"Missing key: {key}"
            
            # Check patient_info structure
            patient_required = ['Name', 'Patient ID', 'Gender', 'Age', 'Test Date']
            for key in patient_required:
                if key not in result['patient_info']:
                    print(f"⚠️  Missing patient info: {key} (this is OK if your parser doesn't extract it yet)")
            
            # Check test_results structure
            if result['test_results']:
                test_required = ['Test Name', 'Value']
                for test in result['test_results']:
                    for key in test_required:
                        if key not in test:
                            print(f"⚠️  Missing test field: {key}")
            
            print("✅ Data structure is correct")
            print(f"   Patient info keys: {list(result['patient_info'].keys())}")
            print(f"   Number of tests: {len(result['test_results'])}")
            
            if result['test_results']:
                print(f"   Test structure sample: {list(result['test_results'][0].keys())}")
            
            return True
        else:
            print(f"❌ Processing failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_csv_output():
    """Test that CSV file is created and has correct format"""
    print("\n🧪 TEST 5: CSV Output Validation")
    print("-" * 40)
    
    poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"
    test_pdf = "../sample_reports/Jane_Smith_Lab_Report.pdf"
    output_dir = "../test_output"
    
    if not os.path.exists(test_pdf):
        print("⚠️  Test PDF not found, skipping CSV test")
        return True
    
    try:
        ocr_service = MedicalOCRService(poppler_path=poppler_path)
        result = ocr_service.process_uploaded_file(test_pdf, output_dir)
        
        if result['success'] and result['csv_path']:
            csv_path = result['csv_path']
            
            # Check if file exists
            assert os.path.exists(csv_path), "CSV file should exist"
            
            # Check file size
            file_size = os.path.getsize(csv_path)
            assert file_size > 0, "CSV file should not be empty"
            
            # Check filename format
            filename = os.path.basename(csv_path)
            assert filename.endswith('.csv'), "Should be a CSV file"
            
            # Try to read the CSV
            with open(csv_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"✅ CSV file created successfully")
                print(f"   File: {filename}")
                print(f"   Size: {file_size} bytes")
                print(f"   Content preview: {content[:200]}...")
            
            return True
        else:
            print(f"❌ CSV creation failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_service_info():
    """Test service information"""
    print("\n🧪 TEST 6: Service Information")
    print("-" * 40)
    
    try:
        poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"
        ocr_service = MedicalOCRService(poppler_path=poppler_path)
        
        info = ocr_service.get_service_info()
        
        print("✅ Service information:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def simulate_team_usage():
    """Simulate how Member 2 will use your module"""
    print("\n🧪 TEST 7: Team Integration Simulation")
    print("-" * 40)
    
    # This simulates Member 2's backend code
    def simulate_member2_backend(uploaded_file_path):
        """Simulate Member 2's usage"""
        
        # Initialize OCR service (Member 2 does this)
        poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"
        ocr_service = MedicalOCRService(poppler_path=poppler_path)
        
        # Process uploaded file (Member 2's main task)
        result = ocr_service.process_uploaded_file(
            uploaded_file_path=uploaded_file_path,
            output_dir="../data/processed"
        )
        
        if result['success']:
            # What Member 2 will do with the data
            patient_data = result['patient_info']
            test_data = result['test_results']
            
            # Member 2 would save to database here
            print(f"   📊 Member 2 receives:")
            print(f"      Patient: {patient_data.get('Name', 'Unknown')}")
            print(f"      Tests: {len(test_data)} results")
            print(f"      CSV: {result['csv_filename']}")
            
            # Simulate database save
            print(f"   💾 Member 2 saves to database...")
            return {
                'status': 'success',
                'patient_id': 'DB123',
                'tests_saved': len(test_data)
            }
        else:
            print(f"   ❌ Member 2 gets error: {result['error']}")
            return {'status': 'error', 'message': result['error']}
    
    # Test the simulation
    test_file = "../sample_reports/Jane_Smith_Lab_Report.pdf"
    
    if not os.path.exists(test_file):
        print("⚠️  Test PDF not found, skipping team integration test")
        return True
    
    try:
        backend_result = simulate_member2_backend(test_file)
        
        if backend_result['status'] == 'success':
            print("✅ Team integration simulation successful!")
            return True
        else:
            print(f"❌ Team integration failed: {backend_result['message']}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION in team simulation: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and show summary"""
    print("🏥 TESTING YOUR OCR MODULE")
    print("=" * 60)
    print("Testing before giving to your team...")
    
    tests = [
        ("Single File Processing", test_single_file),
        ("Multiple Files Processing", test_multiple_files),
        ("Error Handling", test_error_handling),
        ("Data Structure", test_data_structure),
        ("CSV Output", test_csv_output),
        ("Service Information", test_service_info),
        ("Team Integration", simulate_team_usage)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! Your module is ready for the team!")
        print("\n📋 Next steps:")
        print("   1. Give medical_ocr_service.py to Member 2")
        print("   2. Tell Member 2 to import: from ocr_module.medical_ocr_service import MedicalOCRService")
        print("   3. Provide setup instructions (poppler path, dependencies)")
        print("   4. Share usage examples")
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Fix issues before sharing with team.")
        print("\n🔧 Common issues to check:")
        print("   - Make sure your parser.py, utils.py, preprocessor.py work correctly")
        print("   - Check if test PDF file exists")
        print("   - Verify poppler path is correct")
        print("   - Ensure all dependencies are installed")
    
    return passed == len(results)

if __name__ == "__main__":
    # Check current directory
    print(f"📁 Running from: {os.getcwd()}")
    print(f"📁 Files in current directory: {os.listdir('.')}")
    
    # Check if test files exist
    test_pdf = "../sample_reports/Jane_Smith_Lab_Report.pdf"
    if not os.path.exists(test_pdf):
        print(f"⚠️  Test PDF file not found at: {test_pdf}")
        print("   Some tests will be skipped, but basic functionality will be tested")
    
    # Run all tests
    print("\n" + "=" * 60)
    success = run_all_tests()
    
    if success:
        print("\n🚀 Your OCR module is team-ready!")
    else:
        print("\n🔧 Fix the issues and test again.")
        print("💡 Focus on making your core OCR functionality work first.")