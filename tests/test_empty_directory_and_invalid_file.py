# import os
# import pytest
# import subprocess
# import shutil
# import tempfile
# from pathlib import Path

# @pytest.fixture
# def setup_output_directory():
#     """Setup and clean the output directory before and after tests"""
#     # Create output directory if it doesn't exist
#     os.makedirs("output", exist_ok=True)
    
#     # Cleanup before test
#     for file in os.listdir("output"):
#         os.remove(os.path.join("output", file))
    
#     yield
    
#     # Cleanup after test
#     for file in os.listdir("output"):
#         os.remove(os.path.join("output", file))

# @pytest.fixture
# def empty_directory():
#     """Create a temporary empty directory for testing"""
#     temp_dir = tempfile.mkdtemp()
#     yield temp_dir
#     # Cleanup
#     shutil.rmtree(temp_dir)

# @pytest.fixture
# def invalid_file():
#     """Create a temporary invalid file for testing"""
#     temp_file = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
#     temp_file.write(b"This is not a valid JPG file")
#     temp_file.close()
#     yield temp_file.name
#     # Cleanup
#     os.unlink(temp_file.name)

# def test_convert_empty_directory(setup_output_directory, empty_directory):
#     """Test converting an empty directory - should not create a PDF"""
#     # Arrange
#     output_file = "output/output.pdf"
    
#     # Act
#     result = subprocess.run(
#         ["python", "convert_image_to_pdf.py", empty_directory],
#         capture_output=True,
#         text=True
#     )
    
#     # Assert
#     # Script should not create an output file since there are no images
#     assert not os.path.exists(output_file), "Output PDF file was created for an empty directory"
    
#     # The script should exit with code 0 (success) but not create a file
#     # or alternatively, it might return a non-zero code indicating no files were found
#     # The exact behavior depends on the implementation of convert_image_to_pdf.py
#     # We can check both possibilities:
#     assert result.returncode == 0 or "please input file or dir" in result.stdout.lower(), \
#         f"Process failed with unexpected result: {result.stderr}"

# def test_convert_invalid_file(setup_output_directory, invalid_file):
#     """Test converting an invalid file (not a JPG) - should not create a PDF"""
#     # Arrange
#     output_file = "output/output.pdf"
    
#     # Act
#     result = subprocess.run(
#         ["python", "convert_image_to_pdf.py", invalid_file],
#         capture_output=True,
#         text=True
#     )
    
#     # Assert
#     # The script should not create an output file since the input isn't a valid JPG
#     assert not os.path.exists(output_file), "Output PDF file was created for an invalid file"
    
#     # The script should either exit with a non-zero code or display an error message
#     # Depending on the implementation, we can check both possibilities:
#     expected_behavior = (result.returncode != 0) or \
#         ("please input file or dir" in result.stdout.lower()) or \
#         ("not a valid image" in result.stdout.lower() or "not a valid image" in result.stderr.lower())
    
#     assert expected_behavior, f"Process executed without expected error for invalid file: {result.stdout}"

# def test_nonexistent_path(setup_output_directory):
#     """Test converting a non-existent path - should handle error gracefully"""
#     # Arrange
#     nonexistent_path = "/path/that/definitely/does/not/exist"
#     output_file = "output/output.pdf"
    
#     # Act
#     result = subprocess.run(
#         ["python", "convert_image_to_pdf.py", nonexistent_path],
#         capture_output=True,
#         text=True
#     )
    
#     # Assert
#     # The script should not create an output file since the input path doesn't exist
#     assert not os.path.exists(output_file), "Output PDF file was created for a non-existent path"
    
#     # The script should either exit with a non-zero code or display an error message
#     assert result.returncode != 0 or \
#         "please input file or dir" in result.stdout.lower() or \
#         "no such file" in result.stderr.lower() or \
#         "no such file" in result.stdout.lower(), \
#         f"Process executed without expected error for non-existent path: {result.stdout}"