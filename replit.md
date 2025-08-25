# Overview

The AI Quiz Generator is a Streamlit-based web application that automatically generates multiple-choice and true/false questions from uploaded documents using OpenAI's GPT models. The application processes PDF and text files, extracts content, and creates educational quizzes with configurable difficulty levels and question counts. Users can upload documents, generate quizzes, review questions with explanations, and export results in various formats.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses **Streamlit** as the primary web framework, providing a simple and interactive user interface. The UI is organized into three main tabs:
- Document Upload: File handling and text extraction
- Quiz Generation: AI-powered question creation
- Review & Export: Question review and result export

Custom CSS styling is applied through a dedicated styles module, implementing a red and white theme with gradient effects and hover animations.

## Backend Architecture
The system follows a **modular component-based architecture** with three core modules:

**DocumentProcessor**: Handles file processing using the `unstructured` library for PDF and text file parsing. This design choice provides robust document parsing capabilities while maintaining simplicity for supported file types.

**QuizGenerator**: Manages AI-powered question generation through OpenAI's API. The module creates structured prompts for generating both multiple-choice and true/false questions with explanations, ensuring educational value through comprehension-focused questions rather than memorization.

**Styles Module**: Centralizes UI styling and theming, separating presentation logic from business logic for better maintainability.

## State Management
Streamlit's session state is used for maintaining application state across user interactions, storing processed text and generated quiz data to prevent re-processing during user navigation.

## Data Processing Pipeline
1. File upload and validation
2. Content extraction using unstructured library
3. Text preprocessing and preparation
4. AI-powered question generation via OpenAI API
5. Result formatting and export preparation

# External Dependencies

## AI Services
- **OpenAI API**: Core dependency for question generation using GPT models. API key required for functionality.

## Document Processing
- **Unstructured Library**: Handles PDF and text file parsing with configurable strategies for performance optimization.

## Web Framework
- **Streamlit**: Provides the web interface, file upload capabilities, and interactive components.

## Data Handling
- **Pandas**: Used for data manipulation and export functionality.
- **JSON**: For structured data storage and quiz format standardization.

## File I/O
- **tempfile**: Manages temporary file storage for uploaded documents.
- **StringIO/BytesIO**: Handles in-memory file operations for export features.

The application requires an OpenAI API key as the primary external service dependency, with all other dependencies being Python libraries for local processing.