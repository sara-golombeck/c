import os
import pytest
import subprocess
import shutil
from pathlib import Path

@pytest.fixture
def setup_output_directory():
    """Setup and clean the output directory before and after tests"""
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Cleanup before test
    for file in os.listdir("output"):
        os.remove(os.path.join("output", file))
    
    yield
    
    # Cleanup after test
    for file in os.listdir("output"):
        os.remove(os.path.join("output", file))

def test_convert_single_jpg(setup_output_directory):
    """Test converting a single JPG file to PDF"""
    # Arrange
    test_file = "tests/test_data/joseph-corl-iFg78nqsMho-unsplash.jpg"
    output_file = "output/output.pdf"
    
    # Assert file exists before test
    assert os.path.exists(test_file), f"Test file {test_file} not found"
    
    # Act
    result = subprocess.run(
        ["python", "convert_image_to_pdf.py", test_file],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode == 0, f"Process failed with: {result.stderr}"
    assert os.path.exists(output_file), "Output PDF file was not created"
    assert os.path.getsize(output_file) > 0, "Output PDF file is empty"

def test_convert_single_jpg_with_custom_name(setup_output_directory):
    """Test converting a single JPG file to PDF with custom name"""
    # Arrange
    test_file = "tests/test_data/joseph-corl-iFg78nqsMho-unsplash.jpg"
    custom_name = "custom_output"
    output_file = f"output/{custom_name}.pdf"
    
    # Act
    os.environ["PDF_NAME"] = custom_name
    result = subprocess.run(
        ["python", "convert_image_to_pdf.py", test_file],
        capture_output=True,
        text=True
    )
    os.environ.pop("PDF_NAME")  # Clean up environment
    
    # Assert
    assert result.returncode == 0, f"Process failed with: {result.stderr}"
    assert os.path.exists(output_file), f"Output PDF file {output_file} was not created"
    assert os.path.getsize(output_file) > 0, "Output PDF file is empty"