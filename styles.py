import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styling with red and white theme"""
    
    custom_css = """
    <style>
    /* Main app styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .main-header {
        color: #dc2626;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
        border-radius: 10px;
        border-left: 5px solid #dc2626;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #b91c1c 0%, #991b1b 100%);
        box-shadow: 0 4px 8px rgba(220, 38, 38, 0.3);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
        color: #dc2626;
        border: 2px solid #dc2626;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(220, 38, 38, 0.2);
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
        border: 2px dashed #dc2626;
        border-radius: 10px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #b91c1c;
        background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #fef2f2 0%, #ffffff 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
        border: 2px solid #fee2e2;
        border-radius: 8px;
        color: #dc2626;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        border-color: #dc2626;
        color: white;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #16a34a;
        border-radius: 8px;
        color: #15803d;
    }
    
    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #dc2626;
        border-radius: 8px;
        color: #dc2626;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #f59e0b;
        border-radius: 8px;
        color: #d97706;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #3b82f6;
        border-radius: 8px;
        color: #2563eb;
    }
    
    /* Question container styling */
    .question-container {
        background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
        border: 1px solid #fee2e2;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(220, 38, 38, 0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
        border: 1px solid #fee2e2;
        border-radius: 8px;
        color: #dc2626;
        font-weight: 600;
    }
    
    /* Metric styling */
    .css-1xarl3l {
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
        border: 1px solid #fee2e2;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border: 2px solid #fee2e2;
        border-radius: 8px;
        padding: 0.5rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #dc2626;
        box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.2);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border: 2px solid #fee2e2;
        border-radius: 8px;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%);
    }
    
    /* Container spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #dc2626 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #dc2626 !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%);
    }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Add custom JavaScript for enhanced interactions
    custom_js = """
    <script>
    // Add smooth scrolling for better UX
    document.addEventListener('DOMContentLoaded', function() {
        // Add click animations to buttons
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 100);
            });
        });
    });
    </script>
    """
    
    st.markdown(custom_js, unsafe_allow_html=True)

def add_question_styling():
    """Add specific styling for question display"""
    question_css = """
    <style>
    .question-card {
        background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
        border: 2px solid #fee2e2;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(220, 38, 38, 0.1);
        transition: all 0.3s ease;
    }
    
    .question-card:hover {
        border-color: #fecaca;
        box-shadow: 0 6px 12px rgba(220, 38, 38, 0.15);
        transform: translateY(-2px);
    }
    
    .question-text {
        color: #374151;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    
    .correct-option {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border: 2px solid #16a34a;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.25rem 0;
        font-weight: 600;
        color: #15803d;
    }
    
    .option {
        background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.25rem 0;
        color: #374151;
    }
    
    .explanation {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #3b82f6;
        border-radius: 6px;
        padding: 1rem;
        margin-top: 1rem;
        color: #1e40af;
        font-style: italic;
    }
    </style>
    """
    st.markdown(question_css, unsafe_allow_html=True)
