import sys
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
import os
from dotenv import load_dotenv
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any

load_dotenv()

class VerseCraftAgent:
    def __init__(self):
        """Initialize the VerseCraft agent with enhanced capabilities"""
        self.name = "VerseCraft"
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        # Initialize LLM with better parameters for poetry
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=self.google_api_key,
            temperature=0.8,
            top_p=0.95,
            max_retries=4,
            max_tokens=700
        )
        
        # Style-specific prompt templates
        self.style_templates = {
            "Free Verse": self._get_free_verse_template(),
            "Sonnet": self._get_sonnet_template(),
            "Haiku": self._get_haiku_template(),
            "Limerick": self._get_limerick_template(),
            "Ballad": self._get_ballad_template(),
            "Acrostic": self._get_acrostic_template()
        }
        
        # Initialize embedding model
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Vector stores and retrievers
        self.vector_stores = {}
        self.retrievers = {}
        
        # Author mapping
        self.authors = {
            'kafka': './vectorstores/kafka',
            'dostoyevsky': './vectorstores/dostovesky',
            'rumi': './vectorstores/rumi'
        }
        
        # Load vector stores
        self._load_vector_stores()
    
    def _get_free_verse_template(self):
        """Template for free verse poetry"""
        return PromptTemplate(
            input_variables=["context", "keywords", "emotion", "line_count"],
            template="""
You are a renowned poet creating free verse poetry. Free verse has no regular rhyme scheme or meter.
Focus on natural speech patterns, imagery, and emotional expression.

Context from literary works:
{context}

Keywords to incorporate: {keywords}
Primary emotion to convey: {emotion}
Number of lines: {line_count}

Create a free verse poem that:
- Uses natural speech rhythms
- Incorporates all the given keywords naturally
- Strongly conveys the {emotion} emotion
- Has exactly {line_count} lines
- Uses vivid imagery and metaphors

generate only {line_count} only ,do not exceed the {line_count} count as the required poem should be this much big only .
Poem:
"""
        )
    
    def _get_sonnet_template(self):
        """Template for sonnet poetry"""
        return PromptTemplate(
            input_variables=["context", "keywords", "emotion", "line_count"],
            template="""
You are a master sonnet writer. Create a Shakespearean sonnet with 14 lines in iambic pentameter.
Rhyme scheme: ABAB CDCD EFEF GG

Context from literary works:
{context}

Keywords to incorporate: {keywords}
Primary emotion to convey: {emotion}
Lines requested: {line_count} (Note: Sonnets traditionally have 14 lines)

Create a sonnet that:
- Follows ABAB CDCD EFEF GG rhyme scheme
- Uses iambic pentameter (10 syllables per line)
- Incorporates the keywords naturally
- Expresses the {emotion} emotion powerfully
- Has a clear volta (turn) around line 9
- Ends with a strong couplet


generate only {line_count} only ,do not exceed the {line_count} count as the required poem should be this much big only .
Poem:
"""
        )
    
    def _get_haiku_template(self):
        """Template for haiku poetry"""
        return PromptTemplate(
            input_variables=["context", "keywords", "emotion", "line_count"],
            template="""
You are a haiku master. Create a traditional haiku with 3 lines following 5-7-5 syllable pattern.
Focus on nature, seasons, and moments of enlightenment.

Context from literary works:
{context}

Keywords to incorporate: {keywords}
Primary emotion to convey: {emotion}
Lines requested: {line_count} (Note: Haiku traditionally has 3 lines)

Create a haiku that:
- Follows 5-7-5 syllable pattern
- Incorporates nature imagery
- Uses the keywords subtly
- Captures the {emotion} emotion
- Has a seasonal reference or natural imagery
- Creates a moment of insight or beauty

generate only {line_count} only ,do not exceed the {line_count} count as the required poem should be this much big only .
Poem:
"""
        )
    
    def _get_limerick_template(self):
        """Template for limerick poetry"""
        return PromptTemplate(
            input_variables=["context", "keywords", "emotion", "line_count"],
            template="""
You are a limerick writer. Create a humorous limerick with AABBA rhyme scheme.
Lines 1, 2, and 5 have 7-10 syllables. Lines 3 and 4 have 5-7 syllables.

Context from literary works:
{context}

Keywords to incorporate: {keywords}
Primary emotion to convey: {emotion}
Lines requested: {line_count} (Note: Limericks traditionally have 5 lines)

Create a limerick that:
- Follows AABBA rhyme scheme
- Has the proper syllable count
- Is humorous and light-hearted
- Incorporates the keywords cleverly
- Reflects the {emotion} emotion
- Has a punchy, memorable ending

generate only {line_count} only ,do not exceed the {line_count} count as the required poem should be this much big only .
Poem:
"""
        )
    
    def _get_ballad_template(self):
        """Template for ballad poetry"""
        return PromptTemplate(
            input_variables=["context", "keywords", "emotion", "line_count"],
            template="""
You are a ballad composer. Create a narrative ballad that tells a story.
Use ABAB or ABCB rhyme scheme with alternating lines of 8 and 6 syllables.

Context from literary works:
{context}

Keywords to incorporate: {keywords}
Primary emotion to convey: {emotion}
Number of lines: {line_count}

Create a ballad that:
- Tells a compelling story
- Uses ABAB or ABCB rhyme scheme
- Incorporates the keywords into the narrative
- Strongly conveys the {emotion} emotion
- Has exactly {line_count} lines
- Uses simple, clear language
- Has a memorable refrain or chorus

generate only {line_count} only ,do not exceed the {line_count} count as the required poem should be this much big only .
Poem:
"""
        )
    
    def _get_acrostic_template(self):
        """Template for acrostic poetry"""
        return PromptTemplate(
            input_variables=["context", "keywords", "emotion", "line_count"],
            template="""
You are an acrostic poet. Create an acrostic poem where the first letter of each line spells out a word.
Use the primary emotion or main keyword as the acrostic word.

Context from literary works:
{context}

Keywords to incorporate: {keywords}
Primary emotion to convey: {emotion}
Number of lines: {line_count}

Create an acrostic poem that:
- Uses the emotion "{emotion}" or main keyword as the acrostic word
- Each line starts with the corresponding letter
- Incorporates all keywords naturally
- Expresses the {emotion} emotion throughout
- Has exactly {line_count} lines
- Maintains poetic flow and meaning

generate only {line_count} only ,do not exceed the {line_count} count as the required poem should be this much big only .
Poem:
"""
        )
    
    def _load_vector_stores(self):
        """Load all vector stores and create retrievers"""
        try:
            for author, path in self.authors.items():
                if os.path.exists(path):
                    self.vector_stores[author] = FAISS.load_local(
                        path, 
                        self.embedding_model, 
                        allow_dangerous_deserialization=True
                    )
                    self.retrievers[author] = self.vector_stores[author].as_retriever()
                    print(f"✅ Loaded {author} vector store")
                else:
                    print(f"⚠️ Vector store not found: {path}")
        except Exception as e:
            print(f"❌ Error loading vector stores: {e}")
            traceback.print_exc()
    
    def build_vectorstore(self, author_file_path, store_path):
        """Build a new vector store from a text file"""
        try:
            loader = TextLoader(author_file_path, encoding='utf-8')
            documents = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(documents)

            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = FAISS.from_documents(chunks, embeddings)
            vectorstore.save_local(store_path)
            print(f"✅ Vector store saved at {store_path}")
            return True
        except Exception as e:
            print(f"❌ Error building vector store: {e}")
            return False
    
    def get_available_authors(self):
        """Get list of available authors"""
        return list(self.retrievers.keys())
    
    def get_available_styles(self):
        """Get list of available poetry styles"""
        return list(self.style_templates.keys())
    
    def parse_keywords(self, keywords_input):
        """Parse comma-separated keywords"""
        if isinstance(keywords_input, str):
            return [kw.strip() for kw in keywords_input.split(',') if kw.strip()]
        elif isinstance(keywords_input, list):
            return keywords_input
        return []
    
    def generate_poem(self, keywords, emotion, style, line_count, author='kafka'):
        """Enhanced poem generation with all UI functionalities"""
        try:
            # Input validation
            if not keywords:
                return {
                    'status': 'error',
                    'error': 'Keywords cannot be empty',
                    'poem': None
                }
            
            # Parse keywords
            keyword_list = self.parse_keywords(keywords)
            if not keyword_list:
                return {
                    'status': 'error',
                    'error': 'Please provide valid keywords',
                    'poem': None
                }
            
            # Validate author
            if author not in self.retrievers:
                return {
                    'status': 'error',
                    'error': f'Author {author} not available. Available authors: {list(self.retrievers.keys())}',
                    'poem': None
                }
            
            # Validate style
            if style not in self.style_templates:
                return {
                    'status': 'error',
                    'error': f'Style {style} not available. Available styles: {list(self.style_templates.keys())}',
                    'poem': None
                }
            
            # Validate line count
            if line_count < 1 or line_count > 50:
                return {
                    'status': 'error',
                    'error': 'Line count must be between 1 and 50',
                    'poem': None
                }
            
            # Create search query from keywords and emotion
            search_query = f"{emotion} {' '.join(keyword_list)}"
            
            # Get relevant documents
            retriever = self.retrievers[author]
            docs = retriever.get_relevant_documents(search_query)
            
            if not docs:
                return {
                    'status': 'error',
                    'error': 'No relevant context found for the given keywords and emotion',
                    'poem': None
                }
            
            # Create context from documents
            context = "\n".join([doc.page_content for doc in docs])
            
            # Get appropriate template for the style
            template = self.style_templates[style]
            
            # Create chain with style-specific template
            chain = LLMChain(llm=self.llm, prompt=template)
            
            # Generate poem
            result = chain.invoke({
                "context": context,
                "keywords": ", ".join(keyword_list),
                "emotion": emotion,
                "line_count": line_count
            })
            
            generated_poem = result["text"].strip()
            actual_lines = len([line for line in generated_poem.split('\n') if line.strip()])
            
            return {
                'status': 'success',
                'poem': generated_poem,
                'author': author,
                'style': style,
                'emotion': emotion,
                'keywords': keyword_list,
                'line_count': line_count,
                'actual_lines': actual_lines,
                'context_docs': len(docs),
                'metadata': {
                    'author': author,
                    'style': style,
                    'emotion': emotion,
                    'keywords': keyword_list,
                    'requested_lines': line_count,
                    'actual_lines': actual_lines,
                    'context_length': len(context),
                    'retrieved_docs': len(docs),
                    'timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            print(f"❌ ERROR in generate_poem: {e}")
            traceback.print_exc()
            return {
                'status': 'error',
                'error': f'Poem generation failed: {str(e)}',
                'poem': None
            }
    
    # Backward compatibility methods
    def generate_poem_kafka(self, theme):
        """Generate poem in Kafka style (backward compatibility)"""
        return self.generate_poem(theme, 'melancholy', 'Free Verse', 8, 'kafka')
    
    def generate_poem_dostoyevsky(self, theme):
        """Generate poem in Dostoyevsky style (backward compatibility)"""
        return self.generate_poem(theme, 'despair', 'Free Verse', 12, 'dostoyevsky')
    
    def generate_poem_rumi(self, theme):
        """Generate poem in Rumi style (backward compatibility)"""
        return self.generate_poem(theme, 'love', 'Free Verse', 10, 'rumi')
    
    def get_author_info(self, author):
        """Get information about a specific author's vector store"""
        if author not in self.vector_stores:
            return None
        
        try:
            vectorstore = self.vector_stores[author]
            return {
                'author': author,
                'available': True,
                'document_count': vectorstore.index.ntotal if hasattr(vectorstore, 'index') else 'Unknown'
            }
        except Exception as e:
            return {
                'author': author,
                'available': False,
                'error': str(e)
            }
    
    def get_system_info(self):
        """Get system information about the agent"""
        return {
            'name': self.name,
            'available_authors': self.get_available_authors(),
            'available_styles': self.get_available_styles(),
            'embedding_model': 'all-MiniLM-L6-v2',
            'llm_model': 'gemini-2.0-flash',
            'vector_stores_loaded': len(self.vector_stores),
            'python_executable': sys.executable
        }
    
    def process_request(self, request):
        """Process a request from the agent manager or UI"""
        try:
            action = request.get('action', 'generate_poem')
            
            if action == 'generate_poem':
                keywords = request.get('keywords', '')
                emotion = request.get('emotion', 'neutral')
                style = request.get('style', 'Free Verse')
                line_count = request.get('line_count', 8)
                author = request.get('author', 'kafka')
                
                return self.generate_poem(keywords, emotion, style, line_count, author)
            
            elif action == 'get_authors':
                return {
                    'status': 'success',
                    'authors': self.get_available_authors()
                }
            
            elif action == 'get_styles':
                return {
                    'status': 'success',
                    'styles': self.get_available_styles()
                }
            
            elif action == 'get_author_info':
                author = request.get('author', '')
                info = self.get_author_info(author)
                return {
                    'status': 'success' if info else 'error',
                    'info': info
                }
            
            elif action == 'get_system_info':
                return {
                    'status': 'success',
                    'info': self.get_system_info()
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


# Example usage and testing
if __name__ == "__main__":
    # Initialize agent
    agent = VerseCraftAgent()
    
    # Test system info
    print("📊 System Info:")
    print(agent.get_system_info())
    
    # Test enhanced poem generation
    print("\n📝 Generating enhanced poem...")
    
    # Test with UI-like parameters
    test_params = {
        'keywords': 'love, ocean, mystery, moonlight',
        'emotion': 'Love',
        'style': 'Free Verse',
        'line_count': 8,
        'author': 'rumi'
    }
    
    result = agent.generate_poem(
        keywords=test_params['keywords'],
        emotion=test_params['emotion'],
        style=test_params['style'],
        line_count=test_params['line_count'],
        author=test_params['author']
    )
    
    if result['status'] == 'success':
        print(f"\n📜 Generated Poem ({result['style']} style by {result['author']}):\n")
        print(result['poem'])
        print(f"\nRequested lines: {result['line_count']}, Actual lines: {result['actual_lines']}")
        print(f"Keywords used: {', '.join(result['keywords'])}")
        print(f"Emotion: {result['emotion']}")
        print(f"Context docs: {result['context_docs']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Test different style
    print("\n📝 Testing Haiku style...")
    haiku_result = agent.generate_poem(
        keywords='nature, spring, cherry blossom',
        emotion='Joy',
        style='Haiku',
        line_count=3,
        author='rumi'
    )
    
    if haiku_result['status'] == 'success':
        print(f"\n📜 Generated Haiku:\n")
        print(haiku_result['poem'])
    else:
        print(f"❌ Error: {haiku_result['error']}")
