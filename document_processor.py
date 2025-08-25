import os
import tempfile
from typing import Union
import PyPDF2

class DocumentProcessor:
    """Handle processing of PDF and text files using PyPDF2 and native text reading"""
    
    def __init__(self):
        pass
    
    def process_file(self, file_path: str, file_type: str) -> str:
        """
        Process uploaded file and extract text content
        
        Args:
            file_path (str): Path to the uploaded file
            file_type (str): MIME type of the file
        
        Returns:
            str: Extracted text content
        """
        try:
            if file_type == "application/pdf" or file_path.endswith('.pdf'):
                return self._process_pdf(file_path)
            elif file_type == "text/plain" or file_path.endswith('.txt'):
                return self._process_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")
    
    def _process_pdf(self, file_path: str) -> str:
        """
        Process PDF file and extract text
        
        Args:
            file_path (str): Path to PDF file
        
        Returns:
            str: Extracted text content
        """
        try:
            # Use PyPDF2 to extract text from PDF
            text_content = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract text from each page
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_content.append(page_text.strip())
            
            if not text_content:
                raise Exception("No text content could be extracted from the PDF")
            
            # Join all text content
            full_text = "\n\n".join(text_content)
            
            # Basic cleaning
            full_text = self._clean_text(full_text)
            
            return full_text
        
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")
    
    def _process_text(self, file_path: str) -> str:
        """
        Process text file
        
        Args:
            file_path (str): Path to text file
        
        Returns:
            str: Processed text content
        """
        try:
            # Read text file directly
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if not content.strip():
                raise Exception("The text file appears to be empty")
            
            # Basic cleaning
            full_text = self._clean_text(content)
            
            return full_text
        
        except Exception as e:
            raise Exception(f"Failed to process text file: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text content
        
        Args:
            text (str): Raw text content
        
        Returns:
            str: Cleaned text content
        """
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Remove multiple consecutive newlines
        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")
        
        # Ensure minimum length
        if len(text.strip()) < 100:
            raise Exception("The extracted text is too short to generate meaningful questions (minimum 100 characters required)")
        
        # Ensure maximum length for API limits
        if len(text) > 8000:
            text = text[:8000] + "..."
        
        return text.strip()
    
    def validate_file(self, file_path: str, max_size_mb: int = 10) -> bool:
        """
        Validate uploaded file
        
        Args:
            file_path (str): Path to file
            max_size_mb (int): Maximum file size in MB
        
        Returns:
            bool: True if valid, raises exception if invalid
        """
        if not os.path.exists(file_path):
            raise Exception("File does not exist")
        
        # Check file size
        file_size = os.path.getsize(file_path)
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if file_size > max_size_bytes:
            raise Exception(f"File size ({file_size / 1024 / 1024:.1f} MB) exceeds maximum allowed size ({max_size_mb} MB)")
        
        if file_size == 0:
            raise Exception("File is empty")
        
        return True
