# import os
# from PIL import Image, ImageEnhance, ImageFilter

# def preprocess_image(image_path, method="basic"):
#     """
#     Preprocess image for better OCR accuracy
#     """
#     try:
#         if method == "basic":
#             return preprocess_basic(image_path)
#         elif method == "medical":
#             return preprocess_medical_report(image_path)
#         else:
#             return image_path
#     except Exception as e:
#         print(f"Preprocessing failed: {e}")
#         return image_path

# def preprocess_basic(image_path):
#     """Basic preprocessing using PIL only"""
#     try:
#         base, ext = os.path.splitext(image_path)
#         output_path = f"{base}_preprocessed{ext}"
        
#         with Image.open(image_path) as img:
#             if img.mode != 'L':
#                 img = img.convert('L')
            
#             enhancer = ImageEnhance.Contrast(img)
#             img = enhancer.enhance(1.5)
            
#             img.save(output_path)
#             print(f"Basic preprocessing completed: {os.path.basename(output_path)}")
#             return output_path
            
#     except Exception as e:
#         print(f"Basic preprocessing failed: {e}")
#         return image_path

# def preprocess_medical_report(image_path):
#     """Medical report preprocessing using PIL only"""
#     try:
#         base, ext = os.path.splitext(image_path)
#         output_path = f"{base}_medical{ext}"
        
#         with Image.open(image_path) as img:
#             if img.mode != 'L':
#                 img = img.convert('L')
            
#             enhancer = ImageEnhance.Contrast(img)
#             img = enhancer.enhance(1.5)
            
#             enhancer = ImageEnhance.Sharpness(img)
#             img = enhancer.enhance(2.0)
            
#             img = img.filter(ImageFilter.MedianFilter(size=3))
            
#             img.save(output_path)
#             print(f"Medical preprocessing completed: {os.path.basename(output_path)}")
#             return output_path
            
#     except Exception as e:
#         print(f"Medical preprocessing failed: {e}")
#         return image_path
# class ImagePreprocessor:
#     """
#     Simple wrapper class for your existing preprocessing functions
#     This is what your medical_ocr_service.py is trying to import
#     """
    
#     def __init__(self):
#         pass
    
#     def enhance_image(self, image_path, method="basic"):
#         """Use your existing preprocess_image function"""
#         return preprocess_image(image_path, method)
    
#     def preprocess_medical_document(self, image_path):
#         """Use your existing preprocess_medical_report function"""
#         return preprocess_medical_report(image_path)

import os
import tempfile
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(image_path, method="basic"):
    """
    Preprocess image for better OCR accuracy
    """
    try:
        if method == "basic":
            return preprocess_basic(image_path)
        elif method == "medical":
            return preprocess_medical_report(image_path)
        else:
            return image_path
    except Exception as e:
        print(f"Preprocessing failed: {e}")
        return image_path

def preprocess_basic(image_path):
    """Basic preprocessing using PIL only"""
    try:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_preprocessed{ext}"
        
        with Image.open(image_path) as img:
            if img.mode != 'L':
                img = img.convert('L')
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
            
            img.save(output_path)
            print(f"Basic preprocessing completed: {os.path.basename(output_path)}")
            return output_path
            
    except Exception as e:
        print(f"Basic preprocessing failed: {e}")
        return image_path

def preprocess_medical_report(image_path):
    """Medical report preprocessing using PIL only"""
    try:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_medical{ext}"
        
        with Image.open(image_path) as img:
            if img.mode != 'L':
                img = img.convert('L')
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
            
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
            
            img = img.filter(ImageFilter.MedianFilter(size=3))
            
            img.save(output_path)
            print(f"Medical preprocessing completed: {os.path.basename(output_path)}")
            return output_path
            
    except Exception as e:
        print(f"Medical preprocessing failed: {e}")
        return image_path

class ImagePreprocessor:
    """
    Image preprocessor class that handles both PIL Image objects and file paths
    """
    
    def __init__(self):
        self.temp_files = []  # Keep track of temporary files for cleanup
    
    def preprocess(self, image, method="medical"):
        """
        Main preprocess method that your medical_ocr_service.py expects
        
        Args:
            image: Can be either a PIL Image object or a file path string
            method: "basic" or "medical" preprocessing
            
        Returns:
            PIL Image object (preprocessed)
        """
        try:
            # Handle PIL Image objects (from pdf2image)
            if hasattr(image, 'save'):  # It's a PIL Image object
                return self._preprocess_pil_image(image, method)
            
            # Handle file paths
            elif isinstance(image, str) and os.path.exists(image):
                processed_path = preprocess_image(image, method)
                processed_image = Image.open(processed_path)
                return processed_image
            
            else:
                print("⚠️  Unknown image type, returning original")
                return image
                
        except Exception as e:
            print(f"⚠️  Preprocessing failed: {e}, returning original image")
            return image
    
    def _preprocess_pil_image(self, pil_image, method="medical"):
        """
        Preprocess a PIL Image object directly (no file I/O)
        
        Args:
            pil_image: PIL Image object
            method: "basic" or "medical" preprocessing
            
        Returns:
            PIL Image object (preprocessed)
        """
        try:
            # Create a copy to avoid modifying original
            img = pil_image.copy()
            
            # Convert to grayscale if needed
            if img.mode != 'L':
                img = img.convert('L')
            
            if method == "basic":
                # Basic enhancement
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.5)
                
            elif method == "medical":
                # Medical report enhancement
                # Increase contrast
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.5)
                
                # Increase sharpness
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(2.0)
                
                # Apply median filter to reduce noise
                img = img.filter(ImageFilter.MedianFilter(size=3))
            
            return img
            
        except Exception as e:
            print(f"PIL preprocessing failed: {e}")
            return pil_image
    
    def enhance_image(self, image_path, method="basic"):
        """Use your existing preprocess_image function (for backward compatibility)"""
        return preprocess_image(image_path, method)
    
    def preprocess_medical_document(self, image_path):
        """Use your existing preprocess_medical_report function (for backward compatibility)"""
        return preprocess_medical_report(image_path)
    
    def cleanup_temp_files(self):
        """Clean up any temporary files created during processing"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Could not remove temp file {temp_file}: {e}")
        self.temp_files.clear()
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.cleanup_temp_files()