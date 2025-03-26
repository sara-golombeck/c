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

def test_convert_directory_with_jpg(setup_output_directory):
    """Test converting a directory containing JPG files to a single PDF"""
    # Arrange
    test_dir = "tests/test_data/multiple"
    output_file = "output/output.pdf"
    
    # Assert directory exists before test
    assert os.path.isdir(test_dir), f"Test directory {test_dir} not found"
    
    # Assert directory contains JPG files
    jpg_files = [f for f in os.listdir(test_dir) if f.endswith(".JPG")]
    assert len(jpg_files) > 0, f"No JPG files found in {test_dir}"
    
    # Act
    result = subprocess.run(
        ["python", "convert_image_to_pdf.py", test_dir],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode == 0, f"Process failed with: {result.stderr}"
    assert os.path.exists(output_file), "Output PDF file was not created"
    
    # PDF should be larger than the smallest JPG file
    pdf_size = os.path.getsize(output_file)
    assert pdf_size > 0, "Output PDF file is empty"
    
    # Additional verification: PDF size should roughly correspond to the number of images
    min_expected_size = min(os.path.getsize(os.path.join(test_dir, f)) for f in jpg_files) * 0.5
    assert pdf_size > min_expected_size, "PDF file is suspiciously small"

def test_convert_directory_with_custom_name(setup_output_directory):
    """Test converting a directory to PDF with custom output name"""
    # Arrange
    test_dir = "tests/test_data/multiple"
    custom_name = "custom_directory_output"
    output_file = f"output/{custom_name}.pdf"
    
    # Act
    os.environ["PDF_NAME"] = custom_name
    result = subprocess.run(
        ["python", "convert_image_to_pdf.py", test_dir],
        capture_output=True,
        text=True
    )
    os.environ.pop("PDF_NAME")  # Clean up environment
    
    # Assert
    assert result.returncode == 0, f"Process failed with: {result.stderr}"
    assert os.path.exists(output_file), f"Output PDF file {output_file} was not created"
    assert os.path.getsize(output_file) > 0, "Output PDF file is empty"