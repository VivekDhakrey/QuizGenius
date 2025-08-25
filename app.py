import streamlit as st
import streamlit.components.v1 as components
import os
import tempfile
from quiz_generator import QuizGenerator
from document_processor import DocumentProcessor
from styles import apply_custom_styles
import pandas as pd
from io import StringIO, BytesIO
import json

# Apply custom styling
apply_custom_styles()

# Initialize session state
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'processed_text' not in st.session_state:
    st.session_state.processed_text = None

def main():
    st.title("🎯 AI Quiz Generator")
    st.markdown("Generate multiple-choice and true/false questions from your documents using AI")
    
    # Get API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("❌ Gemini API key not found. Please contact support.")
        st.stop()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.success("🔑 API Key: Connected")
        
        # Question generation settings
        st.subheader("Question Settings")
        num_mcq = st.slider("Multiple Choice Questions", 1, 50, 5)
        num_tf = st.slider("True/False Questions", 1, 50, 5)
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📄 Upload Document", "📝 Generate Quiz", "📋 Review & Export"])
    
    with tab1:
        st.header("Upload Your Document")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF or text file",
            type=['pdf', 'txt'],
            help="Upload a PDF or text file to generate questions from"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                with st.spinner("Processing document..."):
                    processor = DocumentProcessor()
                    text_content = processor.process_file(tmp_file_path, uploaded_file.type)
                    st.session_state.processed_text = text_content
                
                st.success("✅ Document processed successfully!")
                
                # Show preview of extracted text
                with st.expander("📖 Preview Extracted Text"):
                    st.text_area("Extracted Content", text_content[:2000] + "..." if len(text_content) > 2000 else text_content, height=200, disabled=True)
                
            except Exception as e:
                st.error(f"❌ Error processing document: {str(e)}")
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)
    
    with tab2:
        st.header("Generate Quiz Questions")
        
        if st.session_state.processed_text is None:
            st.info("Please upload and process a document first.")
            return
        
        if st.button("🚀 Generate Quiz", type="primary", use_container_width=True):
            
            try:
                with st.spinner("Generating questions using AI... This may take a moment."):
                    generator = QuizGenerator(api_key)
                    quiz_data = generator.generate_quiz(
                        st.session_state.processed_text,
                        num_mcq=num_mcq,
                        num_tf=num_tf,
                        difficulty=difficulty
                    )
                    st.session_state.quiz_data = quiz_data
                
                st.success(f"✅ Generated {len(quiz_data['multiple_choice'])} multiple choice and {len(quiz_data['true_false'])} true/false questions!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error generating quiz: {str(e)}")
    
    with tab3:
        st.header("Review & Export Quiz")
        
        if st.session_state.quiz_data is None:
            st.info("Please generate a quiz first.")
            return
        
        quiz_data = st.session_state.quiz_data
        
        # Multiple Choice Questions Section
        st.subheader("🔤 Multiple Choice Questions")
        
        for i, mcq in enumerate(quiz_data['multiple_choice']):
            with st.container():
                st.markdown(f"**Question {i+1}:** {mcq['question']}")
                
                # Display options
                for j, option in enumerate(mcq['options']):
                    prefix = chr(65 + j)  # A, B, C, D
                    if option == mcq['correct_answer']:
                        st.markdown(f"✅ **{prefix}.** {option}")
                    else:
                        st.markdown(f"{prefix}. {option}")
                
                st.markdown(f"**Explanation:** {mcq.get('explanation', 'No explanation provided')}")
                st.divider()
        
        # True/False Questions Section
        st.subheader("✅❌ True/False Questions")
        
        for i, tf in enumerate(quiz_data['true_false']):
            with st.container():
                st.markdown(f"**Question {i+1}:** {tf['question']}")
                
                if tf['correct_answer']:
                    st.markdown("✅ **Answer: True**")
                else:
                    st.markdown("❌ **Answer: False**")
                
                st.markdown(f"**Explanation:** {tf.get('explanation', 'No explanation provided')}")
                st.divider()
        
        # Export functionality
        st.subheader("📥 Export & Print Options")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Export as JSON
            quiz_json = json.dumps(quiz_data, indent=2)
            st.download_button(
                label="📄 Download JSON",
                data=quiz_json,
                file_name="quiz.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Export as CSV
            csv_data = create_csv_export(quiz_data)
            st.download_button(
                label="📊 Download CSV",
                data=csv_data,
                file_name="quiz.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            # Export as formatted text
            text_data = create_text_export(quiz_data)
            st.download_button(
                label="📝 Download Text",
                data=text_data,
                file_name="quiz.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col4:
            # Print button
            if st.button("🖨️ Print Quiz", use_container_width=True):
                # Create print-friendly version
                print_data = create_print_version(quiz_data)
                components.html(print_data, height=0)

def create_csv_export(quiz_data):
    """Create CSV export of quiz data"""
    rows = []
    
    # Multiple choice questions
    for i, mcq in enumerate(quiz_data['multiple_choice']):
        rows.append({
            'Question_Number': f"MC{i+1}",
            'Type': 'Multiple Choice',
            'Question': mcq['question'],
            'Option_A': mcq['options'][0] if len(mcq['options']) > 0 else '',
            'Option_B': mcq['options'][1] if len(mcq['options']) > 1 else '',
            'Option_C': mcq['options'][2] if len(mcq['options']) > 2 else '',
            'Option_D': mcq['options'][3] if len(mcq['options']) > 3 else '',
            'Correct_Answer': mcq['correct_answer'],
            'Explanation': mcq.get('explanation', '')
        })
    
    # True/False questions
    for i, tf in enumerate(quiz_data['true_false']):
        rows.append({
            'Question_Number': f"TF{i+1}",
            'Type': 'True/False',
            'Question': tf['question'],
            'Option_A': 'True',
            'Option_B': 'False',
            'Option_C': '',
            'Option_D': '',
            'Correct_Answer': 'True' if tf['correct_answer'] else 'False',
            'Explanation': tf.get('explanation', '')
        })
    
    df = pd.DataFrame(rows)
    return df.to_csv(index=False)

def create_text_export(quiz_data):
    """Create formatted text export of quiz data"""
    output = []
    output.append("AI GENERATED QUIZ")
    output.append("=" * 50)
    output.append("")
    
    # Multiple Choice Questions
    output.append("MULTIPLE CHOICE QUESTIONS")
    output.append("-" * 30)
    output.append("")
    
    for i, mcq in enumerate(quiz_data['multiple_choice']):
        output.append(f"Question {i+1}: {mcq['question']}")
        output.append("")
        for j, option in enumerate(mcq['options']):
            prefix = chr(65 + j)  # A, B, C, D
            marker = " [CORRECT]" if option == mcq['correct_answer'] else ""
            output.append(f"{prefix}. {option}{marker}")
        output.append("")
        output.append(f"Explanation: {mcq.get('explanation', 'No explanation provided')}")
        output.append("")
        output.append("-" * 30)
        output.append("")
    
    # True/False Questions
    output.append("TRUE/FALSE QUESTIONS")
    output.append("-" * 20)
    output.append("")
    
    for i, tf in enumerate(quiz_data['true_false']):
        output.append(f"Question {i+1}: {tf['question']}")
        output.append("")
        correct_answer = "True" if tf['correct_answer'] else "False"
        output.append(f"Answer: {correct_answer}")
        output.append("")
        output.append(f"Explanation: {tf.get('explanation', 'No explanation provided')}")
        output.append("")
        output.append("-" * 20)
        output.append("")
    
    return "\n".join(output)

def create_print_version(quiz_data):
    """Create HTML for print-friendly version"""
    html_content = f"""
    <script>
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quiz - Print Version</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 20px; 
                line-height: 1.6;
                color: #333;
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #dc2626;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .question-section {{
                margin-bottom: 40px;
            }}
            .question {{
                background: #f9f9f9;
                padding: 15px;
                border-left: 4px solid #dc2626;
                margin-bottom: 20px;
                border-radius: 5px;
            }}
            .question-title {{
                font-weight: bold;
                margin-bottom: 10px;
                color: #dc2626;
            }}
            .options {{
                margin: 10px 0;
            }}
            .correct {{
                background: #dcfce7;
                font-weight: bold;
                color: #15803d;
            }}
            .explanation {{
                background: #eff6ff;
                padding: 10px;
                margin-top: 10px;
                border-radius: 3px;
                font-style: italic;
            }}
            @media print {{
                .no-print {{ display: none; }}
                body {{ margin: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 AI Generated Quiz</h1>
            <p>Generated on {pd.Timestamp.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="question-section">
            <h2>📝 Multiple Choice Questions</h2>
    """
    
    # Add multiple choice questions
    for i, mcq in enumerate(quiz_data['multiple_choice']):
        html_content += f"""
            <div class="question">
                <div class="question-title">Question {i+1}: {mcq['question']}</div>
                <div class="options">
        """
        for j, option in enumerate(mcq['options']):
            prefix = chr(65 + j)  # A, B, C, D
            correct_class = "correct" if option == mcq['correct_answer'] else ""
            html_content += f'<div class="{correct_class}">{prefix}. {option}</div>'
        
        html_content += f"""
                </div>
                <div class="explanation"><strong>Explanation:</strong> {mcq.get('explanation', 'No explanation provided')}</div>
            </div>
        """
    
    # Add true/false questions
    html_content += """
        </div>
        
        <div class="question-section">
            <h2>✅ True/False Questions</h2>
    """
    
    for i, tf in enumerate(quiz_data['true_false']):
        correct_answer = "True" if tf['correct_answer'] else "False"
        html_content += f"""
            <div class="question">
                <div class="question-title">Question {i+1}: {tf['question']}</div>
                <div class="options correct">Answer: {correct_answer}</div>
                <div class="explanation"><strong>Explanation:</strong> {tf.get('explanation', 'No explanation provided')}</div>
            </div>
        """
    
    html_content += """
        </div>
    </body>
    </html>
    `);
    printWindow.document.close();
    printWindow.print();
    </script>
    """
    
    return html_content

if __name__ == "__main__":
    main()
