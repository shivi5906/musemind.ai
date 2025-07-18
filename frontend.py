import streamlit as st
import requests
import json
import time
from typing import Dict, Any

from app.versecraftAgent import VerseCraftAgent
from app.plotweaaver import PlotWeaver
from app.lexifix import LexiFix
from app.poetanalysis import PoetAnalysisAgent
from app.musemorph import MuseMorphAgent





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

#base class css theme not dynamic 
def get_theme_css():
    base_css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');
            
            /* Common styles that work for both themes */
            .main-title {
                font-family: 'Playfair Display', serif !important;
                font-size: 4rem !important;
                font-weight: 700 !important;
                text-align: center !important;
                margin-bottom: 0.5rem !important;
                background: var(--gradient-primary) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                background-clip: text !important;
                text-shadow: 0 0 30px rgba(139, 92, 246, 0.3) !important;
                animation: glow 2s ease-in-out infinite alternate !important;
            }
            
            @keyframes glow {
                from { filter: brightness(1); }
                to { filter: brightness(1.2); }
            }
            
            .subtitle {
                font-family: 'Inter', sans-serif !important;
                font-size: 1.3rem !important;
                font-weight: 300 !important;
                text-align: center !important;
                margin-bottom: 2rem !important;
                color: var(--text-secondary) !important;
            }
            
            .tool-title {
                font-family: 'Playfair Display', serif !important;
                font-size: 2.5rem !important;
                font-weight: 600 !important;
                margin-bottom: 1rem !important;
                color: var(--text-primary) !important;
                background: var(--gradient-primary) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                background-clip: text !important;
            }
            
            .tool-description {
                font-family: 'Inter', sans-serif !important;
                font-size: 1.1rem !important;
                color: var(--text-secondary) !important;
                margin-bottom: 2rem !important;
                line-height: 1.7 !important;
                padding: 1rem !important;
                background: var(--bg-secondary) !important;
                border-radius: 12px !important;
                border: 1px solid var(--border-color) !important;
                box-shadow: var(--shadow-secondary) !important;
            }
            
            .poetry-output {
                font-family: 'Crimson Text', serif !important;
                font-size: 1.2rem !important;
                line-height: 1.9 !important;
                padding: 2rem !important;
                background: var(--bg-secondary) !important;
                border-radius: 16px !important;
                border: 1px solid var(--border-color) !important;
                border-left: 4px solid var(--accent-primary) !important;
                margin: 1rem 0 !important;
                color: var(--text-primary) !important;
                box-shadow: var(--shadow-primary) !important;
                backdrop-filter: blur(10px) !important;
                position: relative !important;
                overflow: hidden !important;
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
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                padding: 2rem !important;
                color: var(--text-primary) !important;
            }
            
            /* Button styling */
            .stButton > button {
                font-family: 'Inter', sans-serif !important;
                font-weight: 600 !important;
                background: var(--gradient-primary) !important;
                color: white !important;
                border: none !important;
                padding: 0.75rem 2rem !important;
                border-radius: 30px !important;
                transition: all 0.3s ease !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
                font-size: 0.9rem !important;
                box-shadow: var(--shadow-primary) !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 15px 35px rgba(139, 92, 246, 0.4) !important;
                filter: brightness(1.1) !important;
            }
            
            .stButton > button:active {
                transform: translateY(-1px) !important;
            }
            
            /* Universal label styling - targets all possible label selectors */
            .stSelectbox label,
            .stTextInput label,
            .stTextArea label,
            .stMultiSelect label,
            .stRadio label,
            .stSlider label,
            .stCheckbox label,
            .stNumberInput label,
            .stFileUploader label,
            .stDateInput label,
            .stTimeInput label,
            .stColorPicker label,
            div[data-testid="stWidgetLabel"],
            div[data-testid="stWidgetLabel"] > div,
            div[data-testid="stWidgetLabel"] > div > div,
            div[data-testid="stWidgetLabel"] p,
            label,
            .stSidebar label,
            .stSidebar .stSelectbox label,
            .stSidebar .stTextInput label,
            .stSidebar .stTextArea label,
            .stSidebar .stMultiSelect label,
            .stSidebar .stRadio label,
            .stSidebar .stSlider label,
            .stSidebar .stCheckbox label,
            .stSidebar .stNumberInput label {
                color: var(--text-primary) !important;
                font-weight: 500 !important;
                font-family: 'Inter', sans-serif !important;
            }
            
            /* Input field styling */
            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox select,
            .stNumberInput input,
            .stDateInput input,
            .stTimeInput input,
            .stSidebar .stTextInput input,
            .stSidebar .stTextArea textarea,
            .stSidebar .stSelectbox select,
            .stSidebar .stNumberInput input {
                background: var(--bg-tertiary) !important;
                border: 1px solid var(--border-color) !important;
                color: var(--text-primary) !important;
                border-radius: 8px !important;
            }
            
            /* Radio button styling */
            .stRadio > div,
            .stSidebar .stRadio > div {
                background: var(--bg-secondary) !important;
                border-radius: 8px !important;
                padding: 0.5rem !important;
            }
            
            .stRadio > div > label,
            .stSidebar .stRadio > div > label {
                color: var(--text-primary) !important;
            }
            
            /* Checkbox styling */
            .stCheckbox > label,
            .stSidebar .stCheckbox > label {
                color: var(--text-primary) !important;
            }
            
            /* Multiselect styling */
            .stMultiSelect > label,
            .stSidebar .stMultiSelect > label {
                color: var(--text-primary) !important;
            }
            
            /* Sidebar styling - using more generic selectors */
            .stSidebar {
                background: var(--bg-secondary) !important;
                border-right: 1px solid var(--border-color) !important;
            }
            
            .stSidebar > div {
                background: var(--bg-secondary) !important;
            }
            
            /* General text elements */
            .stMarkdown,
            .stMarkdown p,
            .stMarkdown div,
            .stText,
            .stText p,
            .stText div,
            div[data-testid="stMarkdownContainer"],
            div[data-testid="stMarkdownContainer"] p,
            div[data-testid="stMarkdownContainer"] div {
                color: var(--text-primary) !important;
            }
            
            .stMarkdown h1,
            .stMarkdown h2,
            .stMarkdown h3,
            .stMarkdown h4,
            .stMarkdown h5,
            .stMarkdown h6 {
                color: var(--text-primary) !important;
            }
            
            /* Metric styling */
            .stMetric label,
            .stMetric > div,
            .stMetric > div > div {
                color: var(--text-primary) !important;
            }
            
            /* Expander styling */
            .stExpander > div > div > div > div,
            .stExpander label {
                color: var(--text-primary) !important;
            }
            
            /* Tab styling */
            .stTabs > div > div > div > div {
                color: var(--text-primary) !important;
            }
            
            /* Theme toggle button */
            .theme-toggle {
                position: fixed !important;
                top: 20px !important;
                right: 20px !important;
                z-index: 1000 !important;
                background: var(--gradient-primary) !important;
                border: none !important;
                border-radius: 50% !important;
                width: 60px !important;
                height: 60px !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
                box-shadow: var(--shadow-primary) !important;
                font-size: 1.5rem !important;
            }
            
            .theme-toggle:hover {
                transform: scale(1.1) !important;
                box-shadow: 0 15px 35px rgba(139, 92, 246, 0.4) !important;
            }
            
            /* Floating elements */
            .floating-decoration {
                position: fixed !important;
                width: 100px !important;
                height: 100px !important;
                border-radius: 50% !important;
                background: var(--gradient-primary) !important;
                opacity: 0.05 !important;
                animation: float 6s ease-in-out infinite !important;
                z-index: -1 !important;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
            }
            
            .floating-decoration:nth-child(1) {
                top: 10% !important;
                left: 10% !important;
                animation-delay: 0s !important;
            }
            
            .floating-decoration:nth-child(2) {
                top: 20% !important;
                right: 10% !important;
                animation-delay: 2s !important;
            }
            
            .floating-decoration:nth-child(3) {
                bottom: 10% !important;
                left: 20% !important;
                animation-delay: 4s !important;
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
                margin-top: 4rem !important;
                padding: 2rem !important;
                text-align: center !important;
                border-top: 1px solid var(--border-color) !important;
                color: var(--text-muted) !important;
                font-family: 'Inter', sans-serif !important;
            }
        </style>
        """
    
    if st.session_state.theme == 'dark':
        theme_vars = """
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
                background: var(--bg-primary) !important;
                color: var(--text-primary) !important;
            }
            
            .subtitle {
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
            }
            
            .tool-title {
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
            }
            
            .floating-decoration {
                opacity: 0.1 !important;
            }
            
            .poetry-output::before {
                background: linear-gradient(45deg, transparent 30%, rgba(139, 92, 246, 0.05) 50%, transparent 70%) !important;
            }
        """
    else:
        theme_vars = """
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
                background: var(--bg-primary) !important;
                color: var(--text-primary) !important;
            }
            
            .floating-decoration {
                opacity: 0.05 !important;
            }
            
            .poetry-output::before {
                background: linear-gradient(45deg, transparent 30%, rgba(139, 92, 246, 0.03) 50%, transparent 70%) !important;
            }
        """
    
    return f"""
        <style>
            {theme_vars}
        </style>
        {base_css}
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
    st.markdown("""
<script>
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
}
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
        "🔧 Poetry Correction": "poetry_correction",
         "💭 Content from Ideas": "content_gen",
        "📖 Vocabulary Help": "vocab_help",
       
        "🎓 Beginner's Guide": "beginner_guide"
        
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
        poetname = st.text_input(
            "Enter Poet Name :",
            placeholder="FRANZ KAFKA , FYODER DOSTOVESKY ...."
        )
        
        
        
        
        
        if st.button("🔍 Analyze Poet"):
            show_loading()
            agent4 = PoetAnalysisAgent()
            
            
            if poetname:
                context = agent4.search_poet_context(poetname)
                summary = agent4.generate_summary(poetname, context)
                final_summary = agent4.refine_summary(summary)
                
                result = final_summary.content
                
            
            if "error" not in result:
                st.session_state.poet_analysis_result = result
    
    
        if 'poet_analysis_result' in st.session_state:
            st.markdown("### Analysis Results")
            result = st.session_state.poet_analysis_result
            
            # Display results in elegant format
            with st.spinner("✨ Crafting your poetic analysis... Please wait."):
                time.sleep(3)
                st.markdown(f'<div class="poetry-output">{result}</div>', unsafe_allow_html=True)
                
          
            with st.expander("📊 Generation Details"):
                st.write(f"**Tools:** web search and refining facts")
                st.download_button(
                label="📥 Download analysis summary",
                data=result.encode('utf-8'),
                file_name="result.txt",
                mime="text/plain"
            )
                st.write(f"**Agent:** PoetAnalysisAgent..")
        
        
        

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
    # Initialize MuseMorphAgent lazily (only when needed)
    def initialize_agent():
        if 'musemorph_agent' not in st.session_state:
            try:
                with st.spinner("🔄 Initializing MuseMorph Agent... Please wait."):
                    
                    st.session_state.musemorph_agent = MuseMorphAgent()
                    st.session_state.agent_loaded = True
                    st.success("✅ MuseMorph Agent initialized successfully!")
            except Exception as e:
                st.session_state.agent_loaded = False
                st.session_state.error_message = str(e)
                st.error(f"❌ Failed to initialize MuseMorph Agent: {str(e)}")
        return st.session_state.get('agent_loaded', False)
    
    # Function to show loading
    def show_loading():
        with st.spinner("Transforming your thoughts..."):
            import time
            time.sleep(0.5)
    
    # Function to process with MuseMorphAgent
    def process_with_musemorph(raw_thoughts: str, output_style: str) -> dict:
        try:
            # Map UI options to MuseMorphAgent expected formats
            style_mapping = {
                "Free Verse": "freeverse",
                "Structured Poem": "structuredpoem", 
                "Philosophical Reflection": "philosophicalreflection"
            }
            
            desired_output = style_mapping.get(output_style, "freeverse")
            
            # Call the MuseMorphAgent
            result = st.session_state.musemorph_agent.morph(raw_thoughts, desired_output)
            
            # Handle different return formats based on output type
            if desired_output == "philosophicalreflection":
                content = result.get('reflection', result) if isinstance(result, dict) else result
            else:
                content = result.get('poem', result) if isinstance(result, dict) else result
                
            return {
                "content": content,
                "status": "success",
                "output_type": output_style
            }
            
        except Exception as e:
            return {
                "error": f"Error processing your thoughts: {str(e)}",
                "status": "error"
            }
    
    # Main UI
    st.markdown('<h2 class="tool-title">💭 Content from Ideas</h2>', unsafe_allow_html=True)
    st.markdown('<p class="tool-description">Transform your raw thoughts and ideas into beautiful poetic expressions.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        raw_thoughts = st.text_area(
            "Share your raw thoughts:",
            placeholder="Write down whatever comes to mind - memories, feelings, observations...",
            height=200,
            key="raw_thoughts_input"
        )
        
        output_style = st.selectbox(
            "Desired output style:",
            ["Free Verse", "Structured Poem", "Philosophical Reflection"],
            key="output_style_select"
        )
        
        # Optional tone selector
        tone = st.selectbox(
            "Tone (optional):",
            ["Default", "Melancholic", "Uplifting", "Contemplative", "Passionate"],
            key="tone_select"
        )
        
        if st.button("💭 Transform Ideas", key="transform_button"):
            if not raw_thoughts.strip():
                st.warning("⚠️ Please enter some thoughts to transform.")
            else:
                # Initialize agent only when transform button is clicked
                if initialize_agent():
                    show_loading()
                    
                    # Process with MuseMorphAgent
                    result = process_with_musemorph(raw_thoughts, output_style)
                    
                    if "error" not in result:
                        st.session_state.content_result = result
                        st.success("✅ Transformation complete!")
                    else:
                        st.error(result["error"])
                else:
                    st.error("❌ Cannot transform thoughts. Agent initialization failed.")
                    st.info("Please check your imports and ensure VerseCraftAgent and PlotWeaver are properly configured.")
    
    with col2:
        if 'content_result' in st.session_state:
            st.markdown("### Transformed Content")
            result = st.session_state.content_result
            
            # Display the transformed content
            content = result.get("content", "Your transformed content will appear here...")
            st.markdown(f'<div class="poetry-output">{content}</div>', unsafe_allow_html=True)
            
            # Add metadata
            st.markdown(f"**Style:** {result.get('output_type', 'Unknown')}")
            
            # Add download option
            if content and content != "Your transformed content will appear here...":
                st.download_button(
                    label="📥 Download Content",
                    data=content,
                    file_name=f"transformed_content_{result.get('output_type', 'output').lower().replace(' ', '_')}.txt",
                    mime="text/plain",
                    key="download_content"
                )
                
                # Clear result button
                if st.button("🗑️ Clear Result", key="clear_result"):
                    if 'content_result' in st.session_state:
                        del st.session_state.content_result
                    st.rerun()
        else:
            st.markdown("### Transformed Content")
            st.markdown('<div class="poetry-output">Your transformed content will appear here...</div>', unsafe_allow_html=True)


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
            if poem_text.strip():  # Check if poem text is not empty
                show_loading()
                
                agent3 = LexiFix()
                
                data = {
                    "text": poem_text,
                    "correction_focus": ", ".join(correction_focus) if correction_focus else "General",
                    "preserve_structure": preserve_style,
                    "output_format": "text"
                }
                
                with st.spinner("WORKING ON THE POEM...."):
                    result = agent3.fix_text(data)
                    
                    # Store result in session state
                    st.session_state.correction_result = result
                    
                    if result.get("success"):
                        st.success("✅ Poem corrected successfully!")
                    else:
                        st.error("❌ Error occurred during correction")
            else:
                st.warning("⚠️ Please enter a poem before clicking correct!")
    
    # Define display_results function outside of columns
    def display_results(result):
        if result.get("success"):
            # Success message
            st.markdown('<div class="success-message">✅ Poem successfully corrected!</div>', unsafe_allow_html=True)
            
            # Display corrected poem
            st.markdown("### 📝 Corrected Poem")
            corrected_text = result.get("fixed_text", "")
            st.markdown(f'<div class="poetry-output">{corrected_text}</div>', unsafe_allow_html=True)
            
            # Display correction statistics
            st.markdown("### 📊 Correction Details")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Word Count", result.get("word_count", 0))
            
            with col2:
                st.metric("Focus Area", result.get("correction_focus", "N/A"))
            
            with col3:
                structure_status = "✅ Preserved" if result.get("structure_preserved") else "🔄 Restructured"
                st.markdown(f"**Structure:** {structure_status}")
            
            # Show original vs corrected comparison
            with st.expander("🔍 View Original vs Corrected"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Original:**")
                    st.markdown(f'<div class="poetry-output" style="background: #fff3cd;">{result.get("original_text", "")}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown("**Corrected:**")
                    st.markdown(f'<div class="poetry-output" style="background: #d1ecf1;">{corrected_text}</div>', unsafe_allow_html=True)
            
            # Download button
            st.download_button(
                label="📥 Download Corrected Poem",
                data=corrected_text,
                file_name="corrected_poem.txt",
                mime="text/plain"
            )
        else:
            # Display error message
            st.error("❌ Error occurred during correction")
            error_message = result.get("error", "Unknown error occurred")
            st.markdown(f"**Error details:** {error_message}")
    
    with col2:
        st.markdown("### 📖 Results")
        
        # Display results if available
        if 'correction_result' in st.session_state:
            display_results(st.session_state.correction_result)
        else:
            # Placeholder when no results
            st.markdown("""
            <div class="poetry-output" style="text-align: center; color: #666;">
                <h4>🎭 Your corrected poem will appear here...</h4>
                <p>Enter your poem in the left panel and click "Correct Poem" to get started!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer with tips
    st.markdown("---")
    st.markdown("### 💡 Tips for Better Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📝 Input Tips:**
        - Paste your complete poem
        - Include line breaks as intended
        - Don't worry about perfect grammar
        """)
    
    with col2:
        st.markdown("""
        **🎯 Focus Areas:**
        - Grammar: Fix punctuation & syntax
        - Flow: Improve rhythm & pace
        - Imagery: Enhance metaphors & visuals
        """)
    
    with col3:
        st.markdown("""
        **⚙️ Settings:**
        - Preserve style: Keep original structure
        - Multiple focuses: Select 2-3 areas
        - Download results for future use
        """)
    
    # Clear results button
    if st.button("🗑️ Clear Results"):
        if 'correction_result' in st.session_state:
            del st.session_state.correction_result
        st.rerun()

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
        # Initialize PlotWeaver if not available
        if 'plotweaver' not in st.session_state:
            try:
                with st.spinner("Initializing PlotWeaver..."):
                    st.session_state.plotweaver = PlotWeaver()
                    st.success("PlotWeaver initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize PlotWeaver: {str(e)}")
                st.info("Please check your environment setup and API keys.")
                return

        # Get available options from PlotWeaver
        try:
            available_genres = st.session_state.plotweaver.get_available_genres()
            available_moods = st.session_state.plotweaver.get_available_moods()
            complexity_info = st.session_state.plotweaver.get_complexity_info()
        except Exception as e:
            st.error(f"Error loading options: {str(e)}")
            # Fallback to default options
            available_genres = ["Romance", "Mystery", "Adventure", "Fantasy", "Drama", "Horror", "Slice of Life"]
            available_moods = ["Melancholic", "Joyful", "Mysterious", "Passionate", "Serene", "Intense", "Whimsical"]
            complexity_info = {"simple": "Basic plot", "moderate": "Moderate complexity", "complex": "Complex plot"}
        
        # Genre selection with expanded options
        genre = st.selectbox(
            "Choose a genre:",
            ["Romance", "Mystery", "Adventure", "Fantasy", "Drama", "Horror", "Slice of Life"]
        )
        
        # Mood selection with expanded options
        mood = st.selectbox(
            "Desired mood:",
            ["Melancholic", "Joyful", "Mysterious", "Passionate", "Serene", "Intense", "Whimsical"]
           
        )
        
        # Plot complexity with descriptions
        complexity_options = list(complexity_info.keys())
        complexity_display = [f"{key.title()}" for key in complexity_options]
        
        length = st.radio(
            "Plot complexity:",
            complexity_display
        )
        
        # Convert display back to internal format
        complexity_key = complexity_options[complexity_display.index(length)]
        
        # Show complexity description
        if complexity_key in complexity_info:
            st.info(f"**{complexity_key.title()}**: {complexity_info[complexity_key]}")
        

        data={
            "genre" : genre,
            "mood" : mood,
            "complexity" : length 
        }
        # Generate button
        if st.button("📚 Generate Plot", type="primary"):
            show_loading()
            
          
            agent2 = PlotWeaver()

 
            try:
                # Use PlotWeaver as an agent
                with st.spinner("🧠 Agent analyzing themes... 📚 Retrieving context... 🧩 Composing plot..."):
                    plot_result = agent2.generate_plot(genre,mood,length)
                
                if plot_result:
                    # Store result in session state
                    st.session_state.plot_result = {
                        'plot': plot_result,
                        'genre': genre,
                        'mood': mood,
                        'complexity': complexity_key,
                        
                    }
                    
                    st.success("Plot generated successfully by PlotWeaver Agent!")
                else:
                    st.error("Agent failed to generate plot. Please try again.")
                    
            except Exception as e:
                st.error(f"Agent execution failed: {str(e)}")
                st.info("Please check your setup and try again.")
    
    with col2:
        if 'plot_result' in st.session_state:
            st.markdown("### Your Plot Foundation")
            result = st.session_state.plot_result
            
            # Display plot with better formatting
            plot_content = result.get("plot", "Your plot will appear here...")
            
            # Style the output
            st.markdown(f'<div class="poetry-output">{plot_content}</div>', unsafe_allow_html=True)
            
            # Plot tools
            with st.expander("🔧 Plot Tools"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    # Download button
                    st.download_button(
                        label="📥 Download Plot",
                        data=plot_content,
                        file_name=f"plot_{result.get('timestamp', 'generated').replace(':', '-').replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                
                with col_b:
                    # Regenerate with same parameters using agent
                    if st.button("🔄 Regenerate", help="Generate a new plot with the same parameters"):
                        try:
                            with st.spinner("Agent regenerating plot..."):
                                new_plot = st.session_state.plotweaver.generate_plot(genre,mood,length)
                            
                            if new_plot:
                                st.session_state.plot_result['plot'] = new_plot
                                st.rerun()
                            else:
                                st.error("Agent regeneration failed. Please try again.")
                        except Exception as e:
                            st.error(f"Agent regeneration failed: {str(e)}")
            
            # Show generation parameters
            with st.expander("📊 Generation Details"):
                st.write(f"**Genre:** {result.get('genre', 'N/A')}")
                st.write(f"**Mood:** {result.get('mood', 'N/A')}")
                st.write(f"**Complexity:** {result.get('complexity', 'N/A').title()}")
                st.write(f"**Agent:** PlotWeaver")
        else:
            st.markdown("### Your Plot Foundation")
            st.info("👆 Configure your preferences and click 'Generate Plot' to get started!")



def poetry_generation_tool():
    """Poetry Generation Tool"""
    st.markdown('<h2 class="tool-title">✍️ Poetry Generation</h2>', unsafe_allow_html=True)
    st.markdown('<p class="tool-description"><b>Generate beautiful poems and quotes from your KEYWORDS and EMOTIONS.</b></p>', unsafe_allow_html=True)
    st.markdown('<p class="tool-description"><i>NOTE:</i> Please remember the linecount does not work on haiku (traditionalscheme)  .</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        keywords = st.text_input(
            "Enter keywords (comma-separated):",
            placeholder="love, ocean, mystery, moonlight..."
        )
        author = st.selectbox(
            "Enter author name :",
            ["kafka" , "dostovesky" , "rumi"]
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
