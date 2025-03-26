import os
import pytest
import shutil
import subprocess
from pathlib import Path

class TestDirectoryWithJpg:
    """בדיקת המרת תיקייה עם קבצי JPG לקובץ PDF אחד"""
    
    @pytest.fixture(scope="function")
    def setup_test_env(self):
        """הכנת סביבת הבדיקה - יצירת תיקייה עם מספר קבצי JPG לבדיקה"""
        # יצירת תיקיית temp לקבצי הבדיקה
        test_dir = Path("test_files") / "jpg_directory"
        if test_dir.exists():
            shutil.rmtree(test_dir)
        test_dir.mkdir(parents=True)
            
        # יצירת מספר קבצי JPG לבדיקה
        jpg_files = []
        for i in range(1, 4):  # יצירת 3 קבצים
            test_jpg = test_dir / f"test_image_{i}.JPG"
            jpg_files.append(test_jpg)
            
            # יצירת קובץ JPG מינימלי
            with open(test_jpg, "wb") as f:
                f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xdb\x00C\x01\t\t\t\x0c\x0b\x0c\x18\r\r\x182!\x1c!22222222222222222222222222222222222222222222222222\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xfc\x00\xff\xd9')
        
        # יצירת קובץ שאינו JPG בתיקייה (לבדיקת פילטור נכון)
        non_jpg_file = test_dir / "not_an_image.txt"
        with open(non_jpg_file, "w") as f:
            f.write("This is not a JPG file")
        
        # ניקוי תיקיית output
        output_dir = Path("output")
        if not output_dir.exists():
            output_dir.mkdir()
            
        # מחיקת קבצי PDF קודמים
        for pdf_file in output_dir.glob("*.pdf"):
            pdf_file.unlink()
            
        yield {"test_dir": test_dir, "jpg_files": jpg_files}
    
    def test_directory_conversion(self, setup_test_env):
        """בדיקה שהמרה של תיקייה עם קבצי JPG לPDF עובדת כראוי"""
        test_dir = setup_test_env["test_dir"]
        
        # הפעלת הסקריפט באמצעות הפקודה על התיקייה
        result = subprocess.run(
            ["python", "convert_image_to_pdf.py", str(test_dir)],
            capture_output=True,
            text=True
        )
        
        # בדיקה שהפקודה הסתיימה בהצלחה
        assert result.returncode == 0, f"התוכנית נכשלה עם קוד שגיאה {result.returncode}: {result.stderr}"
        
        # בדיקה שקובץ ה-PDF נוצר (ברירת מחדל output/output.pdf)
        output_pdf = Path("output") / "output.pdf"
        assert output_pdf.exists(), f"קובץ ה-PDF לא נוצר בנתיב {output_pdf}"
        
        # בדיקה שקובץ ה-PDF אינו ריק
        assert output_pdf.stat().st_size > 0, "קובץ ה-PDF נוצר אבל הוא ריק"
    
    def test_directory_with_custom_name(self, setup_test_env):
        """בדיקה שהמרה של תיקייה עם קבצי JPG לPDF עם שם מותאם עובדת כראוי"""
        test_dir = setup_test_env["test_dir"]
        custom_name = "dir_output"
        
        # הפעלת הסקריפט עם משתנה סביבה לשם מותאם
        env = os.environ.copy()
        env["PDF_NAME"] = custom_name
        
        result = subprocess.run(
            ["python", "convert_image_to_pdf.py", str(test_dir)],
            capture_output=True,
            text=True,
            env=env
        )
        
        # בדיקה שהפקודה הסתיימה בהצלחה
        assert result.returncode == 0, f"התוכנית נכשלה עם קוד שגיאה {result.returncode}: {result.stderr}"
        
        # בדיקה שקובץ ה-PDF נוצר עם השם המותאם
        output_pdf = Path("output") / f"{custom_name}.pdf"
        assert output_pdf.exists(), f"קובץ ה-PDF לא נוצר בנתיב {output_pdf}"
        
        # בדיקה שקובץ ה-PDF אינו ריק
        assert output_pdf.stat().st_size > 0, "קובץ ה-PDF נוצר אבל הוא ריק"