import streamlit as st
import requests
import json
import time
from typing import Dict, Any
from app.versecraftAgent import VerseCraftAgent


from app.sqllite_utils import init_db, save_poem, get_poems


#database intialistaion
init_db()


# Page configuration
st.set_page_config(
    page_title="MuseMind - Poetry & Writing Assistant",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Dynamic CSS based on theme
def get_theme_css():
    if st.session_state.theme == 'dark':
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');
            
            /* Dark theme variables */
            :root {
                --bg-primary: #0a0a0a;
                --bg-secondary: #1a1a1a;
                --bg-tertiary: #2a2a2a;
                --text-primary: #ffffff;
                --text-secondary: #b0b0b0;
                --text-muted: #808080;
                --accent-primary: #8b5cf6;
                --accent-secondary: #06b6d4;
                --gradient-primary: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
                --gradient-secondary: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
                --border-color: #3a3a3a;
                --shadow-primary: 0 10px 30px rgba(139, 92, 246, 0.2);
                --shadow-secondary: 0 5px 15px rgba(0, 0, 0, 0.3);
            }
            
            /* Override Streamlit's default dark theme */
            .stApp {
                background: var(--bg-primary);
                color: var(--text-primary);
            }
            
            .main-title {
                font-family: 'Playfair Display', serif;
                font-size: 4rem;
                font-weight: 700;
                text-align: center;
                margin-bottom: 0.5rem;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
                animation: glow 2s ease-in-out infinite alternate;
            }
            
            @keyframes glow {
                from { filter: brightness(1); }
                to { filter: brightness(1.2); }
            }
            
            .subtitle {
                font-family: 'Inter', sans-serif;
                font-size: 1.3rem;
                font-weight: 300;
                text-align: center;
                margin-bottom: 2rem;
                color: var(--text-secondary);
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
            }
            
            .tool-title {
                font-family: 'Playfair Display', serif;
                font-size: 2.5rem;
                font-weight: 600;
                margin-bottom: 1rem;
                color: var(--text-primary);
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .tool-description {
                font-family: 'Inter', sans-serif;
                font-size: 1.1rem;
                color: var(--text-secondary);
                margin-bottom: 2rem;
                line-height: 1.7;
                padding: 1rem;
                background: var(--bg-secondary);
                border-radius: 12px;
                border: 1px solid var(--border-color);
                box-shadow: var(--shadow-secondary);
            }
            
            .poetry-output {
                font-family: 'Crimson Text', serif;
                font-size: 1.2rem;
                line-height: 1.9;
                padding: 2rem;
                background: var(--bg-secondary);
                border-radius: 16px;
                border: 1px solid var(--border-color);
                border-left: 4px solid var(--accent-primary);
                margin: 1rem 0;
                color: var(--text-primary);
                box-shadow: var(--shadow-primary);
                backdrop-filter: blur(10px);
                position: relative;
                overflow: hidden;
            }
            
            .poetry-output::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent 30%, rgba(139, 92, 246, 0.05) 50%, transparent 70%);
                pointer-events: none;
            }
            
            .loading-spinner {
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 2rem;
                color: var(--text-primary);
            }
            
            .stButton > button {
                font-family: 'Inter', sans-serif;
                font-weight: 600;
                background: var(--gradient-primary);
                color: white;
                border: none;
                padding: 0.75rem 2rem;
                border-radius: 30px;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-size: 0.9rem;
                box-shadow: var(--shadow-primary);
            }
            
            .stButton > button:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(139, 92, 246, 0.4);
                filter: brightness(1.1);
            }
            
            .stButton > button:active {
                transform: translateY(-1px);
            }
            
            /* Sidebar styling */
            .css-1d391kg {
                background: var(--bg-secondary);
                border-right: 1px solid var(--border-color);
            }
            
            .css-1d391kg .stSelectbox label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stTextInput label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stTextArea label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stMultiSelect label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stRadio label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stSlider label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stCheckbox label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            /* Input field styling */
            .stTextInput input {
                background: var(--bg-tertiary);
                border: 1px solid var(--border-color);
                color: var(--text-primary);
                border-radius: 8px;
            }
            
            .stTextArea textarea {
                background: var(--bg-tertiary);
                border: 1px solid var(--border-color);
                color: var(--text-primary);
                border-radius: 8px;
            }
            
            .stSelectbox select {
                background: var(--bg-tertiary);
                border: 1px solid var(--border-color);
                color: var(--text-primary);
                border-radius: 8px;
            }
            
            /* Theme toggle button */
            .theme-toggle {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1000;
                background: var(--gradient-primary);
                border: none;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: var(--shadow-primary);
                font-size: 1.5rem;
            }
            
            .theme-toggle:hover {
                transform: scale(1.1);
                box-shadow: 0 15px 35px rgba(139, 92, 246, 0.4);
            }
            
            /* Floating elements */
            .floating-decoration {
                position: fixed;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: var(--gradient-primary);
                opacity: 0.1;
                animation: float 6s ease-in-out infinite;
                z-index: -1;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
            }
            
            .floating-decoration:nth-child(1) {
                top: 10%;
                left: 10%;
                animation-delay: 0s;
            }
            
            .floating-decoration:nth-child(2) {
                top: 20%;
                right: 10%;
                animation-delay: 2s;
            }
            
            .floating-decoration:nth-child(3) {
                bottom: 10%;
                left: 20%;
                animation-delay: 4s;
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--bg-secondary);
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--accent-primary);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--accent-secondary);
            }
            
            /* Footer styling */
            .footer {
                margin-top: 4rem;
                padding: 2rem;
                text-align: center;
                border-top: 1px solid var(--border-color);
                color: var(--text-muted);
                font-family: 'Inter', sans-serif;
            }
            
        </style>
        """
    else:
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');
            
            /* Light theme variables */
            :root {
                --bg-primary: #ffffff;
                --bg-secondary: #f8fafc;
                --bg-tertiary: #f1f5f9;
                --text-primary: #1a1a1a;
                --text-secondary: #4a5568;
                --text-muted: #718096;
                --accent-primary: #8b5cf6;
                --accent-secondary: #06b6d4;
                --gradient-primary: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
                --gradient-secondary: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                --border-color: #e2e8f0;
                --shadow-primary: 0 10px 30px rgba(139, 92, 246, 0.15);
                --shadow-secondary: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            
            .stApp {
                background: var(--bg-primary);
                color: var(--text-primary);
            }
            
            .main-title {
                font-family: 'Playfair Display', serif;
                font-size: 4rem;
                font-weight: 700;
                text-align: center;
                margin-bottom: 0.5rem;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
                animation: glow 2s ease-in-out infinite alternate;
            }
            
            @keyframes glow {
                from { filter: brightness(1); }
                to { filter: brightness(1.2); }
            }
            
            .subtitle {
                font-family: 'Inter', sans-serif;
                font-size: 1.3rem;
                font-weight: 300;
                text-align: center;
                margin-bottom: 2rem;
                color: var(--text-secondary);
            }
            
            .tool-title {
                font-family: 'Playfair Display', serif;
                font-size: 2.5rem;
                font-weight: 600;
                margin-bottom: 1rem;
                color: var(--text-primary);
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .tool-description {
                font-family: 'Inter', sans-serif;
                font-size: 1.1rem;
                color: var(--text-secondary);
                margin-bottom: 2rem;
                line-height: 1.7;
                padding: 1rem;
                background: var(--bg-secondary);
                border-radius: 12px;
                border: 1px solid var(--border-color);
                box-shadow: var(--shadow-secondary);
            }
            
            .poetry-output {
                font-family: 'Crimson Text', serif;
                font-size: 1.2rem;
                line-height: 1.9;
                padding: 2rem;
                background: var(--bg-secondary);
                border-radius: 16px;
                border: 1px solid var(--border-color);
                border-left: 4px solid var(--accent-primary);
                margin: 1rem 0;
                color: var(--text-primary);
                box-shadow: var(--shadow-primary);
                backdrop-filter: blur(10px);
                position: relative;
                overflow: hidden;
            }
            
            .poetry-output::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent 30%, rgba(139, 92, 246, 0.03) 50%, transparent 70%);
                pointer-events: none;
            }
            
            .loading-spinner {
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 2rem;
                color: var(--text-primary);
            }
            
            .stButton > button {
                font-family: 'Inter', sans-serif;
                font-weight: 600;
                background: var(--gradient-primary);
                color: white;
                border: none;
                padding: 0.75rem 2rem;
                border-radius: 30px;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-size: 0.9rem;
                box-shadow: var(--shadow-primary);
            }
            
            .stButton > button:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(139, 92, 246, 0.4);
                filter: brightness(1.1);
            }
            
            .stButton > button:active {
                transform: translateY(-1px);
            }
            
            /* Sidebar styling */
            .css-1d391kg {
                background: var(--bg-secondary);
                border-right: 1px solid var(--border-color);
            }
            
            .css-1d391kg .stSelectbox label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stTextInput label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stTextArea label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stMultiSelect label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stRadio label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stSlider label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            .css-1d391kg .stCheckbox label {
                color: var(--text-primary);
                font-weight: 500;
            }
            
            /* Input field styling */
            .stTextInput input {
                background: var(--bg-tertiary);
                border: 1px solid var(--border-color);
                color: var(--text-primary);
                border-radius: 8px;
            }
            
            .stTextArea textarea {
                background: var(--bg-tertiary);
                border: 1px solid var(--border-color);
                color: var(--text-primary);
                border-radius: 8px;
            }
            
            .stSelectbox select {
                background: var(--bg-tertiary);
                border: 1px solid var(--border-color);
                color: var(--text-primary);
                border-radius: 8px;
            }
            
            /* Theme toggle button */
            .theme-toggle {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1000;
                background: var(--gradient-primary);
                border: none;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: var(--shadow-primary);
                font-size: 1.5rem;
            }
            
            .theme-toggle:hover {
                transform: scale(1.1);
                box-shadow: 0 15px 35px rgba(139, 92, 246, 0.4);
            }
            
            /* Floating elements */
            .floating-decoration {
                position: fixed;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: var(--gradient-primary);
                opacity: 0.05;
                animation: float 6s ease-in-out infinite;
                z-index: -1;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
            }
            
            .floating-decoration:nth-child(1) {
                top: 10%;
                left: 10%;
                animation-delay: 0s;
            }
            
            .floating-decoration:nth-child(2) {
                top: 20%;
                right: 10%;
                animation-delay: 2s;
            }
            
            .floating-decoration:nth-child(3) {
                bottom: 10%;
                left: 20%;
                animation-delay: 4s;
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--bg-secondary);
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--accent-primary);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--accent-secondary);
            }
            
            /* Footer styling */
            .footer {
                margin-top: 4rem;
                padding: 2rem;
                text-align: center;
                border-top: 1px solid var(--border-color);
                color: var(--text-muted);
                font-family: 'Inter', sans-serif;
            }
        </style>
        """

st.markdown("""
<style>
    .poem-container {
        background: #2b2b2b;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        min-height: 200px;
    }
    
    .poem-text {
        font-family: 'Georgia', serif;
        font-size: 1.1rem;
        line-height: 1.8;
        color: #ffffff;
        white-space: pre-line;  /* This preserves line breaks */
    }
    
    /* Better column spacing */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #2b2b2b;
        color: white;
        border-radius: 10px;
    }
    
    .stSelectbox > div > div {
        background-color: #2b2b2b;
        color: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# API Base URL (you can make this configurable)
API_BASE_URL = "http://localhost:8000"  # Change this to your backend URL

# Helper function to make API calls
def make_api_call(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Make API call to backend with error handling"""
    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return {"error": str(e)}

# Loading animation
def show_loading():
    """Display loading animation"""
    with st.spinner("✨ Your muse is working..."):
        time.sleep(1)  # Simulate processing time

# Theme toggle component
def theme_toggle():
    """Add floating theme toggle button"""
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    st.markdown(f"""
    <div class="theme-toggle" onclick="toggleTheme()">
        {theme_icon}
    </div>
    <script>
        function toggleTheme() {{
            // This will be handled by the Streamlit button
        }}
    </script>
    """, unsafe_allow_html=True)

# Floating decorations
def add_floating_decorations():
    """Add floating decorative elements"""
    st.markdown("""
    <div class="floating-decoration"></div>
    <div class="floating-decoration"></div>
    <div class="floating-decoration"></div>
    """, unsafe_allow_html=True)

# Main App
def main():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)
    
    # Add floating decorations
    add_floating_decorations()
    
    # Header with enhanced styling
    st.markdown('<h1 class="main-title">🎭 MuseMind</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI-Powered Poetry & Writing Companion</p>', unsafe_allow_html=True)
    
    # Sidebar for tool selection with enhanced styling
    st.sidebar.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: {'#ffffff' if st.session_state.theme == 'dark' else '#1a1a1a'}; font-family: 'Playfair Display', serif;">
            🎨 Writing Tools
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    tools = {
        "🔍 Poet Analysis": "analyze_poet",
        "📚 Plot-Based Writing": "plot_writing", 
        "✍️ Poetry Generation": "poetry_gen",
        "📖 Vocabulary Help": "vocab_help",
        "💭 Content from Ideas": "content_gen",
        "🎓 Beginner's Guide": "beginner_guide",
        "🔧 Poetry Correction": "poetry_correction"
    }
    
    selected_tool = st.sidebar.selectbox("Choose your writing tool:", list(tools.keys()))
    
    # Theme toggle in sidebar
    st.sidebar.markdown("---")
    theme_button_text = "🌙 Switch to Dark Mode" if st.session_state.theme == 'light' else "☀️ Switch to Light Mode"
    if st.sidebar.button(theme_button_text):
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
        st.rerun()
    
    # Tool implementations
    tool_key = tools[selected_tool]
    
    if tool_key == "analyze_poet":
        poet_analysis_tool()
    elif tool_key == "plot_writing":
        plot_based_writing_tool()
    elif tool_key == "poetry_gen":
        poetry_generation_tool()
    elif tool_key == "vocab_help":
        vocabulary_help_tool()
    elif tool_key == "content_gen":
        content_generation_tool()
    elif tool_key == "beginner_guide":
        beginner_guide_tool()
    elif tool_key == "poetry_correction":
        poetry_correction_tool()

def poet_analysis_tool():
    """Poet Analysis Tool"""
    st.markdown('<h2 class="tool-title">🔍 Poet Analysis</h2>', unsafe_allow_html=True)
    st.markdown('<p class="tool-description">Analyze the tone, grammar, and style of famous poets to understand their unique voice.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        poet_name = st.selectbox(
            "Choose a poet to analyze:",
            ["Franz Kafka", "Rumi", "Sylvia Plath", "Emily Dickinson", "Pablo Neruda", "Maya Angelou", "William Shakespeare"]
        )
        
        analysis_type = st.multiselect(
            "What aspects to analyze:",
            ["Tone", "Grammar", "Style", "Themes", "Imagery", "Rhythm"],
            default=["Tone", "Style"]
        )
        
        sample_text = st.text_area(
            "Paste a sample poem (optional):",
            placeholder="Enter a poem by the selected poet for detailed analysis...",
            height=150
        )
        
        if st.button("🔍 Analyze Poet"):
            show_loading()
            
            data = {
                "poet_name": poet_name,
                "analysis_type": analysis_type,
                "sample_text": sample_text
            }
            
            result = make_api_call("/api/analyze-poet", data)
            
            if "error" not in result:
                st.session_state.poet_analysis_result = result
    
    with col2:
        if 'poet_analysis_result' in st.session_state:
            st.markdown("### Analysis Results")
            result = st.session_state.poet_analysis_result
            
            # Display results in elegant format
            st.markdown(f'<div class="poetry-output">{result.get("poem", "Your poem will appear here...")}</div>', unsafe_allow_html=True)

def vocabulary_help_tool():
    """Vocabulary Help Tool"""
    st.markdown('<h2 class="tool-title">📖 Vocabulary Help</h2>', unsafe_allow_html=True)
    st.markdown('<p class="tool-description">Discover deeper, more poetic alternatives for your words and lines.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        word_or_line = st.text_input(
            "Enter a word or line:",
            placeholder="Enter a word or line you want to improve..."
        )
        
        context = st.selectbox(
            "Context:",
            ["Romantic", "Nature", "Spiritual", "Dark", "Joyful", "Melancholic", "Mystical"]
        )
        
        suggestion_type = st.radio(
            "Type of suggestions:",
            ["Synonyms", "Metaphors", "Imagery", "All"]
        )
        
        if st.button("📖 Get Suggestions"):
            show_loading()
            
            data = {
                "text": word_or_line,
                "context": context,
                "suggestion_type": suggestion_type
            }
            
            result = make_api_call("/api/vocab", data)
            
            if "error" not in result:
                st.session_state.vocab_result = result
    
    with col2:
        if 'vocab_result' in st.session_state:
            st.markdown("### Vocabulary Suggestions")
            result = st.session_state.vocab_result
            
            st.markdown(f'<div class="poetry-output">{result.get("suggestions", "Suggestions will appear here...")}</div>', unsafe_allow_html=True)

def content_generation_tool():
    """Content Generation from Ideas Tool"""
    st.markdown('<h2 class="tool-title">💭 Content from Ideas</h2>', unsafe_allow_html=True)
    st.markdown('<p class="tool-description">Transform your raw thoughts and ideas into beautiful poetic expressions.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        raw_thoughts = st.text_area(
            "Share your raw thoughts:",
            placeholder="Write down whatever comes to mind - memories, feelings, observations...",
            height=200
        )
        
        output_style = st.selectbox(
            "Desired output style:",
            ["Poetic Prose", "Free Verse", "Structured Poem", "Philosophical Reflection"]
        )
        
        tone = st.selectbox(
            "Tone:",
            ["Contemplative", "Passionate", "Gentle", "Bold", "Nostalgic", "Hopeful"]
        )
        
        if st.button("💭 Transform Ideas"):
            show_loading()
            
            data = {
                "raw_thoughts": raw_thoughts,
                "output_style": output_style,
                "tone": tone
            }
            
            result = make_api_call("/api/gen-from-idea", data)
            
            if "error" not in result:
                st.session_state.content_result = result
    
    with col2:
        if 'content_result' in st.session_state:
            st.markdown("### Transformed Content")
            result = st.session_state.content_result
            
            st.markdown(f'<div class="poetry-output">{result.get("content", "Your transformed content will appear here...")}</div>', unsafe_allow_html=True)

def beginner_guide_tool():
    """Beginner's Guide Tool"""
    st.markdown('<h2 class="tool-title">🎓 Beginner\'s Guide</h2>', unsafe_allow_html=True)
    st.markdown('<p class="tool-description">Learn writing tips, practices, and discover how to express your emotions through poetry.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        topic = st.selectbox(
            "What would you like to learn?",
            ["Basic Poetry Structure", "Expressing Emotions", "Using Imagery", "Rhythm and Flow", "Finding Your Voice", "Editing Techniques"]
        )
        
        experience_level = st.selectbox(
            "Your experience level:",
            ["Complete Beginner", "Some Experience", "Intermediate"]
        )
        
        specific_emotion = st.text_input(
            "Any specific emotion you want to explore? (optional):",
            placeholder="e.g., heartbreak, joy, confusion..."
        )
        
        if st.button("🎓 Get Guidance"):
            show_loading()
            
            data = {
                "topic": topic,
                "experience_level": experience_level,
                "specific_emotion": specific_emotion
            }
            
            result = make_api_call("/api/beginner-guide", data)
            
            if "error" not in result:
                st.session_state.guide_result = result
    
    with col2:
        if 'guide_result' in st.session_state:
            st.markdown("### Writing Guide")
            result = st.session_state.guide_result
            
            st.markdown(f'<div class="poetry-output">{result.get("guide", "Your personalized guide will appear here...")}</div>', unsafe_allow_html=True)

def poetry_correction_tool():
    """Poetry Correction Tool"""
    st.markdown('<h2 class="tool-title">🔧 Poetry Correction</h2>', unsafe_allow_html=True)
    st.markdown('<p class="tool-description">Submit your poem for improvements in tone, grammar, and poetic flow.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        poem_text = st.text_area(
            "Paste your poem:",
            placeholder="Enter your poem here for correction and improvement...",
            height=250
        )
        
        correction_focus = st.multiselect(
            "What aspects to focus on:",
            ["Grammar", "Tone", "Flow", "Imagery", "Structure", "Word Choice"],
            default=["Grammar", "Flow"]
        )
        
        preserve_style = st.checkbox("Preserve original style", value=True)
        
        if st.button("🔧 Correct Poem"):
            show_loading()
            
            data = {
                "poem": poem_text,
                "correction_focus": correction_focus,
                "preserve_style": preserve_style
            }
            
            result = make_api_call("/api/fix-poem", data)
            
            if "error" not in result:
                st.session_state.correction_result = result
    
    with col2:
        if 'correction_result' in st.session_state:
            st.markdown("### Corrected Poem")
            result = st.session_state.correction_result
            
            st.markdown(f'<div class="poetry-output">{result.get("corrected_poem", "Your corrected poem will appear here...")}</div>', unsafe_allow_html=True)
            
            if "suggestions" in result:
                st.markdown("### Suggestions")
                st.markdown(f'<div class="poetry-output">{result.get("suggestions", "")}</div>', unsafe_allow_html=True)

# Enhanced Footer
def show_footer():
    st.markdown(f"""
    <div class="footer">
        <p style="font-size: 1.1rem; margin-bottom: 1rem;">
            Made with ❤️ for poets and writers everywhere
        </p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            "Poetry is the spontaneous overflow of powerful feelings: it takes its origin from emotion recollected in tranquility." - William Wordsworth
        </p>
        <div style="margin-top: 1rem;">
            <span style="font-size: 1.2rem;">🎭</span>
            <span style="margin: 0 1rem;">✨</span>
            <span style="font-size: 1.2rem;">📖</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Additional UI enhancements
def add_custom_components():
    """Add custom interactive components"""
    # Add a subtle animation for the main title
    st.markdown("""
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const title = document.querySelector('.main-title');
            if (title) {
                title.style.animation = 'fadeInUp 1s ease-out';
            }
        });
    </script>
    <style>
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    """, unsafe_allow_html=True)


def plot_based_writing_tool():
    """Plot-Based Writing Tool"""
    st.markdown('<h2 class="tool-title">📚 Plot-Based Writing</h2>', unsafe_allow_html=True)
    st.markdown('<p class="tool-description">Get inspiring plots and themes to kickstart your poetic writing journey.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        genre = st.selectbox(
            "Choose a genre:",
            ["Romance", "Mystery", "Adventure", "Fantasy", "Drama", "Horror", "Slice of Life"]
        )
        
        mood = st.selectbox(
            "Desired mood:",
            ["Melancholic", "Joyful", "Mysterious", "Passionate", "Serene", "Intense", "Whimsical"]
        )
        
        length = st.radio(
            "Plot complexity:",
            ["Simple", "Moderate", "Complex"]
        )
        
        if st.button("📚 Generate Plot"):
            show_loading()
            
            data = {
                "genre": genre,
                "mood": mood,
                "length": length
            }
            
            result = make_api_call("/api/plot", data)
            
            if "error" not in result:
                st.session_state.plot_result = result
    
    with col2:
        if 'plot_result' in st.session_state:
            st.markdown("### Your Plot Foundation")
            result = st.session_state.plot_result
            
            st.markdown(f'<div class="poetry-output">{result.get("plot", "Your plot will appear here...")}</div>', unsafe_allow_html=True)

def poetry_generation_tool():
    """Poetry Generation Tool"""
    st.markdown('<h2 class="tool-title">✍️ Poetry Generation</h2>', unsafe_allow_html=True)
    st.markdown('<p class="tool-description">Generate beautiful poems and quotes from your keywords and emotions.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        keywords = st.text_input(
            "Enter keywords (comma-separated):",
            placeholder="love, ocean, mystery, moonlight..."
        )
        author = st.selectbox(
            "Enter author name :",
            ["kafka" , "dostovesky" , "rumi "]
        )
        emotion = st.selectbox(
            "Primary emotion:",
            ["Love", "Sadness", "Joy", "Anger", "Peace", "Longing", "Wonder", "Fear"]
        )
        
        style = st.selectbox(
            "Poetry style:",
            ["Free Verse", "Sonnet", "Haiku", "Limerick", "Ballad", "Acrostic"]
        )
        
        length = st.slider("Number of lines:", 4, 20, 8)
        
        if st.button("✍️ Generate Poetry"):
            show_loading()
            
            data = {
                "keywords": keywords.split(",") if keywords else [],
                "emotion": emotion,
                "style": style,
                "length": length,
                "author": author
            }
            agent1 = VerseCraftAgent()
            if keywords.strip():
             with st.spinner("Crafting your poem..."):
              result = agent1.generate_poem(keywords, emotion, style, length, author)

            
              if result['status'] == 'success':
               # Format the poem with proper line breaks
                    
                    st.session_state.poem_result = result["poem"]
                    st.session_state.show_poem = True
              else:
                    st.error(result['error'])     
    
    with col2:
         st.markdown("### Your Generated Poetry")
    
    # Check if poem exists in session state
         if hasattr(st.session_state, 'show_poem') and st.session_state.show_poem:
        # Format poem with proper line breaks
          formatted_poem = st.session_state.poem_result.replace('\n', '<br>')
          st.markdown(f'''
           <div class="poem-container">
            <div class="poem-text">{formatted_poem}</div>
           </div>
           ''', unsafe_allow_html=True)
         else:
        # Placeholder when no poem is generated
           st.markdown('''
            <div class="poem-container">
            <div class="poem-text" style="color: #888; font-style: italic;">
                Your generated poem will appear here...
            </div>
           </div>
          ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    add_custom_components()
    show_footer()
