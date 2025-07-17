from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
from dotenv import load_dotenv
from typing import Dict, Optional, List
from pathlib import Path
import json
from langchain.chains import LLMChain

class PlotWeaver:
    """
    An advanced agentic RAG system for generating creative plots based on user preferences.
    
    Uses three specialized agents:
    1. Theme Analyzer - Breaks down user inputs into structured theme components
    2. Context Retriever - Finds relevant literary examples and patterns
    3. Plot Composer - Generates final structured plot
    """
    
    def __init__(self, vectorstore_path: str = "./vectorstores/plot_ideas"):
        """
        Initialize the PlotWeaver system.
        
        Args:
            vectorstore_path: Path to the FAISS vectorstore containing plot ideas
        """
        self.vectorstore_path = vectorstore_path
        self._setup_environment()
        self._initialize_llm()
        self._setup_agents()
        self._load_vectorstore()
        self._initialize_options()
    
    def _setup_environment(self):
        """Load environment variables and API keys."""
        load_dotenv()
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    def _initialize_llm(self):
        """Initialize the Google Generative AI model."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", 
            google_api_key=self.google_api_key
        )
    
    def _initialize_options(self):
        """Initialize available options for genres, moods, and complexity levels."""
        self.available_genres = [
            "Romance", "Mystery", "Adventure", "Fantasy", "Drama", "Horror", "Slice of Life"]
        
        self.available_moods = [
            "Melancholic", "Joyful", "Mysterious", "Passionate", "Serene", "Intense", "Whimsical"
        ] 
        
        self.complexity_levels = {
            "simple": "Single protagonist, linear plot, one main conflict",
            "moderate": "Multiple characters, subplots, character development arcs",
            "complex": "Multiple POVs, intricate plotting, layered themes, complex world-building"
        }
    
    def _setup_agents(self):
        """Setup the three specialized agents with their prompts."""
        
        # Agent 1: Theme Analyzer
        self.theme_prompt = PromptTemplate(
            input_variables=["genre", "mood", "complexity"],
            template="""
You are a sophisticated theme analysis agent. Analyze the user's creative preferences:

Genre: {genre}
Desired Mood: {mood}
Plot Complexity: {complexity}

Based on these inputs, provide a structured analysis including:
- Primary genre characteristics and conventions
- Emotional tone and atmosphere
- Suggested setting and world-building elements
- Main character archetype suggestions
- Core internal/external conflict types
- Thematic depth based on complexity level

Format your response as a clear, structured analysis that will guide plot generation.
"""
        )
        self.theme_agent = self.theme_prompt | self.llm | StrOutputParser()
        
        # Agent 3: Plot Composer
        self.plot_prompt = PromptTemplate(
            input_variables=["analysis", "context", "genre", "mood", "complexity"],
            template="""
You are PlotWeaver, an advanced plot generation specialist. You can create stories that are imaginative yet a blend of facts and logic, consider yourself a great player of words.

User Requirements:
- Genre: {genre}
- Mood: {mood}
- Complexity: {complexity}

Theme Analysis: {analysis}

Retrieved Literary Context: {context}

Generate a compelling plot with the following structure:

**TITLE:** [Creative, genre-appropriate title]

**PLOT SUMMARY:**
[2-3 sentence overview]

**ACT I - SETUP:**
[Detailed setup including character introduction, world establishment, and inciting incident]

**ACT II - CONFRONTATION:**
[Rising action, conflicts, obstacles, and character development]

**ACT III - RESOLUTION:**
[Climax, resolution, and character transformation]

**KEY THEMES:**
[Major themes explored in the story]

**CHARACTER ARC:**
[Brief description of protagonist's journey]

Ensure the complexity matches the user's request: simple plots should be straightforward, while complex plots should include subplots, multiple character arcs, and layered themes.
"""
        )
        self.plot_agent = self.plot_prompt | self.llm | StrOutputParser()
    
    def _load_vectorstore(self):
        """Load the FAISS vectorstore for context retrieval."""
        try:
            self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            self.vectorstore = FAISS.load_local(
                self.vectorstore_path, 
                self.embedding_model,
                allow_dangerous_deserialization=True
            )
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
            print(f"✅ Vectorstore loaded successfully from {self.vectorstore_path}")
        except Exception as e:
            print(f"⚠️ Warning: Could not load vectorstore from {self.vectorstore_path}")
            print(f"Error: {str(e)}")
            print("🔧 You need to create the vectorstore first. See setup instructions below.")
            self.vectorstore = None
            self.retriever = None
    
    def _retrieve_context(self, theme_analysis: str) -> str:
        """
        Retrieve relevant context from the vectorstore.
        
        Args:
            theme_analysis: The analyzed theme information
            
        Returns:
            Concatenated relevant document content
        """
        if not self.retriever:
            return "No vectorstore context available."
        
        try:
            docs = self.retriever.get_relevant_documents(theme_analysis)
            context = "\n\n".join([doc.page_content for doc in docs[:3]])
            return context if context else "No relevant context found."
        except Exception as e:
            return f"Error retrieving context: {str(e)}"
    
    def generate_plot(self, genre: str, desired_mood: str, plot_complexity: str) -> str:
        """
        Generate a complete plot using the agentic RAG system.
        
        Args:
            genre: The story genre (e.g., "science fiction", "fantasy", "mystery")
            desired_mood: The emotional tone (e.g., "dark", "hopeful", "suspenseful")
            plot_complexity: Complexity level ("simple", "moderate", "complex")
            
        Returns:
            Generated plot as a formatted string
        """
        try:
            print("🧠 Agent 1: Analyzing theme and preferences...")
            theme_analysis = self.theme_agent.invoke({
                "genre": genre,
                "mood": desired_mood,
                "complexity": plot_complexity
            })
            
            print("📚 Agent 2: Retrieving relevant context...")
            context = self._retrieve_context(theme_analysis)
            
            print("🧩 Agent 3: Composing final plot...")
            final_plot = self.plot_agent.invoke({
                "genre": genre,
                "mood": desired_mood,
                "complexity": plot_complexity,
                "analysis": theme_analysis,
                "context": context
            })
            
            return final_plot
            
        except Exception as e:
            return f"❌ Plot Generation Failed: {str(e)}"
    
    def create_vectorstore(self, documents_path: str):
        """
        Create a vectorstore from text documents.
        
        Args:
            documents_path: Path to directory containing text files with plot ideas
        """
        try:
            # Load documents
            documents = []
            for filename in os.listdir(documents_path):
                if filename.endswith('.txt'):
                    file_path = str(Path(documents_path) / filename).replace('\\', '/')
                    loader = TextLoader(file_path)
                    docs = loader.load()
                    documents.extend(docs)
            
            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(documents)
            
            # Create vectorstore
            embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = FAISS.from_documents(splits, embedding_model)
            
            # Save vectorstore
            os.makedirs(os.path.dirname(self.vectorstore_path), exist_ok=True)
            vectorstore.save_local(self.vectorstore_path)
            
            print(f"✅ Vectorstore created and saved to {self.vectorstore_path}")
            
            # Reload the vectorstore
            self._load_vectorstore()
            
        except Exception as e:
            print(f"❌ Error creating vectorstore: {str(e)}")

    def get_available_genres(self) -> List[str]:
        """Return list of available genres."""
        return self.available_genres

    def get_available_moods(self) -> List[str]:
        """Return list of available moods."""
        return self.available_moods

    def get_complexity_info(self) -> Dict[str, str]:
        """Return complexity levels with descriptions."""
        return self.complexity_levels

    def process_request(self, request: Dict) -> Dict:
        """Process a request from the agent manager or UI"""
        try:
            action = request.get('action', 'generate_plot')
            
            if action == 'generate_plot':
                genre = request.get('genre', 'Romance')
                mood = request.get('mood', 'Neutral')
                complexity = request.get('complexity', 'simple')
                
                plot = self.generate_plot(genre, mood, complexity)
                return {
                    'status': 'success',
                    'plot': plot,
                    'parameters': {
                        'genre': genre,
                        'mood': mood,
                        'complexity': complexity
                    }
                }
            
            elif action == 'get_genres':
                return {
                    'status': 'success',
                    'genres': self.get_available_genres()
                }
            
            elif action == 'get_moods':
                return {
                    'status': 'success',
                    'moods': self.get_available_moods()
                }
            
            elif action == 'get_complexity':
                return {
                    'status': 'success',
                    'complexity_info': self.get_complexity_info()
                }
            
            elif action == 'health_check':
                return {
                    'status': 'success',
                    'message': 'PlotWeaver is running',
                    'vectorstore_loaded': self.vectorstore is not None
                }
            
            else:
                return {
                    'status': 'error',
                    'error': f'Unknown action: {action}'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': f'Request processing failed: {str(e)}'
            }

    def validate_inputs(self, genre: str, mood: str, complexity: str) -> Dict:
        """Validate user inputs and return validation result."""
        errors = []
        
        if genre not in self.available_genres:
            errors.append(f"Invalid genre. Available genres: {', '.join(self.available_genres)}")
        
        if mood not in self.available_moods:
            errors.append(f"Invalid mood. Available moods: {', '.join(self.available_moods)}")
        
        if complexity not in self.complexity_levels:
            errors.append(f"Invalid complexity. Available levels: {', '.join(self.complexity_levels.keys())}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

# Example usage and testing functions


    def getPhilosophicalPrompt(self):
        template = """You are a profound philosophical thinker and contemplative writer. Your task is to transform raw thoughts and emotions into deep philosophical reflections that explore the fundamental nature of existence, consciousness, and human experience.

Given the following raw thought or emotion:
"{raw_prompt}"

Please create a structured philosophical reflection that:

1. **Examines the deeper meaning** behind the raw thought
2. **Explores universal themes** and existential questions
3. **Connects to broader philosophical concepts** (existence, consciousness, time, meaning, etc.)
4. **Uses contemplative and reflective language**
5. **Provides multiple perspectives** on the core idea
6. **Ends with profound insights** or questions for further contemplation

**Structure Guidelines:**
- Begin with an engaging philosophical opening that reframes the raw thought
- Develop 3-4 main philosophical themes or questions
- Use contemplative, measured prose
- Include references to the human condition
- Incorporate metaphysical and existential elements
- Conclude with deeper wisdom or provocative questions

**Philosophical Approach:**
- Draw connections to timeless philosophical questions
- Explore paradoxes and contradictions
- Examine both subjective and objective perspectives
- Consider the relationship between individual experience and universal truths
- Reflect on the nature of consciousness, reality, and meaning

**Tone and Style:**
- Contemplative and introspective
- Scholarly yet accessible
- Balanced between abstract concepts and concrete examples
- Thought-provoking without being pretentious

**Output the philosophical reflection directly without any additional commentary:**

Reflection:"""

        return PromptTemplate(
        input_variables=["raw_prompt"],
        template=template
    )

# Advanced version with more parameters for deeper control
    def getPhilosophicalPromptAdvanced(self):
    
     template = """You are a profound philosophical thinker drawing from centuries of wisdom traditions. Transform the given raw thought into a deep philosophical reflection.

**Raw Input:** "{raw_prompt}"
**Philosophical Theme:** {theme}
**Key Concepts:** {concepts}
**Target Length:** {reflection_length} words
**Contextual Wisdom:** {context}

**Instructions:**
Create a structured philosophical reflection that examines the raw input through the lens of {theme}, incorporating the specified concepts and drawing from the provided wisdom context.

**Philosophical Framework:**
- **Ontological Layer**: What does this reveal about the nature of being?
- **Epistemological Layer**: How do we know what we know about this experience?
- **Ethical Layer**: What moral or value implications arise?
- **Existential Layer**: How does this relate to meaning and purpose?
- **Phenomenological Layer**: What is the lived experience telling us?

**Reflection Structure:**
1. **Opening Contemplation**: Reframe the raw thought philosophically
2. **Core Exploration**: Examine through multiple philosophical lenses
3. **Universal Connections**: Link to broader human experience
4. **Paradoxes and Tensions**: Explore contradictions and complexities
5. **Synthesis**: Weave insights into coherent understanding
6. **Closing Wisdom**: End with profound insights or questions

**Philosophical Style:**
- Use sophisticated but accessible language
- Balance abstract concepts with concrete examples
- Include rhetorical questions that provoke thought
- Weave in wisdom from various philosophical traditions
- Maintain scholarly rigor while remaining engaging

**Output only the philosophical reflection:**

"""

     return PromptTemplate(
        input_variables=["raw_prompt", "theme", "concepts", "reflection_length", "context"],
        template=template
    )

# Usage in your plotweaver class
    def generate_philosophical_reflection(self, raw_thought):
        try:
         if raw_thought:
            search_query = "philosophical, wisdom, contemplation"
            retriever = self.retriever # Assuming you have a philosophy retriever
            docs = retriever.get_relevant_documents(search_query)
            
            # Use the simple version
            template = self.getPhilosophicalPrompt()
            chain = LLMChain(llm=self.llm, prompt=template)
           
            result = chain.invoke({
                "raw_prompt": raw_thought
            })
            
            generated_reflection = result["text"].strip()
            word_count = len(generated_reflection.split())

            return {
                'reflection': generated_reflection,
                'word_count': word_count,
                'status': 'success'
            }
            
        except Exception as e:
          print(f"Error generating philosophical reflection: {e}")
          return {
            'reflection': None,
            'error': str(e),
            'status': 'failed'
        }

# Advanced version with more philosophical depth
    def generate_philosophical_reflection_advanced(self, raw_thought, theme="existentialism", target_words=300):
        try:
          if raw_thought:
            search_query = f"philosophy, {theme}, wisdom"
            retriever = self.retrievers["philosophy"]
            docs = retriever.get_relevant_documents(search_query)
            
            # Define philosophical concepts based on theme
            concept_mapping = {
                "existentialism": "authenticity, freedom, responsibility, absurdity, choice",
                "stoicism": "virtue, wisdom, acceptance, resilience, duty",
                "phenomenology": "consciousness, experience, intentionality, being-in-the-world",
                "ethics": "morality, virtue, justice, good life, responsibility",
                "metaphysics": "reality, existence, substance, causation, time",
                "epistemology": "knowledge, truth, belief, skepticism, certainty"
            }
            
            template = self.getPhilosophicalPromptAdvanced()
            chain = LLMChain(llm=self.llm, prompt=template)
           
            result = chain.invoke({
                "raw_prompt": raw_thought,
                "theme": theme,
                "concepts": concept_mapping.get(theme, "wisdom, truth, meaning"),
                "reflection_length": target_words,
                "context": docs[:2] if docs else "Draw from your philosophical knowledge"
            })
            
            generated_reflection = result["text"].strip()
            word_count = len(generated_reflection.split())

            return {
                'reflection': generated_reflection,
                'word_count': word_count,
                'target_words': target_words,
                'theme': theme,
                'status': 'success'
            }
            
        except Exception as e:
          print(f"Error generating philosophical reflection: {e}")
        return {
            'reflection': None,
            'error': str(e),
            'status': 'failed'
        }

# Example usage function for your plotweaver agent
    def process_raw_thought_philosophically(self, raw_thought, depth_level="standard"):
       """
       Main method to process raw thoughts into philosophical reflections
       """
       if depth_level == "advanced":
        return self.generate_philosophical_reflection_advanced(
            raw_thought, 
            theme="existentialism",  # You can make this dynamic
            target_words=400
        )
       else:
        return self.generate_philosophical_reflection(raw_thought)


def main():
    """Example usage of PlotWeaver system."""
    try:
        # Initialize PlotWeaver
        plot_weaver = PlotWeaver()
        
        # Example request
        request = {
            'action': 'generate_plot',
            'genre': 'Romance',
            'mood': 'Passionate',
            'complexity': 'complex'
        }
        
        # Process request
        result = plot_weaver.process_request(request)
        
        if result['status'] == 'success':
            print("Generated Plot:")
            print("=" * 50)
            print(result['plot'])
        else:
            print(f"Error: {result['error']}")
            
    except Exception as e:
        print(f"Failed to initialize PlotWeaver: {str(e)}")

if __name__ == "__main__":
    main()
