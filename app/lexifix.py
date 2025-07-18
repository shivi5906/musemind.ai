from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from functools import wraps
import time
from typing import Dict, Optional, Any

class LexiFix:
    def __init__(self):
        self._setup_env()
        self._initialize_llm()
        self._setup_chain()
        self._cache = {}  # Simple caching for efficiency

    def _setup_env(self):
        """Load environment variables"""
        load_dotenv()
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

    def _initialize_llm(self):
        """Initialize the Google Generative AI model"""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=self.google_api_key,
                temperature=0.8,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {e}")

    def _setup_chain(self):
        """Set up the prompt template and chain"""
        self.prompt_lexi = PromptTemplate(
            input_variables=["text", "correction_focus", "preserve_structure"],
            template="""
You are LexiFix, an expert creative editor with a poetic tone. You can detect and fix grammatical errors and linguistic errors .


Here is a user-submitted piece of writing:
"{text}"

Your task is to:
- Correct any grammatical issues
- Enhance readability
- Adjust the tone to be more poetic
- Preserve the original artistic intent
- Don't explain the poem or grammar, just give the output

Return only the improved version.

"""
        )
        
        try:
            self.lexi_chain = LLMChain(llm=self.llm, prompt=self.prompt_lexi)
        except Exception as e:
            raise RuntimeError(f"Failed to create LLMChain: {e}")

    # Wrapper Functions for Efficiency
    def _performance_monitor(func):
        """Wrapper to monitor performance of functions"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            result = func(self, *args, **kwargs)
            end_time = time.time()
            print(f"⏱️ {func.__name__} executed in {end_time - start_time:.2f} seconds")
            return result
        return wrapper

    def _cache_results(func):
        """Wrapper to cache results for repeated inputs"""
        @wraps(func)
        def wrapper(self, input_dict: Dict[str, Any]):
            # Create cache key from input dictionary
            cache_key = str(sorted(input_dict.items()))
            
            if cache_key in self._cache:
                print("📋 Using cached result")
                return self._cache[cache_key]
            
            result = func(self, input_dict)
            self._cache[cache_key] = result
            return result
        return wrapper

    def _validate_input(func):
        """Wrapper to validate input dictionary"""
        @wraps(func)
        def wrapper(self, input_dict: Dict[str, Any]):
            if not isinstance(input_dict, dict):
                return {"error": "Input must be a dictionary"}
            
            if not input_dict.get("text", "").strip():
                return {"error": "Please provide valid text to fix"}
            
            # Set default values for missing keys
            defaults = {
                "correction_focus": "grammar and flow",
                "preserve_structure": True,
                "output_format": "text"
            }
            
            for key, default_value in defaults.items():
                if key not in input_dict:
                    input_dict[key] = default_value
            
            return func(self, input_dict)
        return wrapper

    def _error_handler(func):
        """Wrapper for comprehensive error handling"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                return {
                    "error": f"❌ Error in {func.__name__}: {str(e)}",
                    "success": False
                }
        return wrapper

    # Main processing method with all wrappers
    @_error_handler
    @_performance_monitor
    @_cache_results
    @_validate_input
    def fix_text(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fix and enhance text using dictionary input
        
        Args:
            input_dict: Dictionary containing:
                - text (str): Text to fix (required)
                - correction_focus (str): Focus area for corrections (default: "grammar and flow")
                - preserve_structure (bool): Whether to preserve original structure (default: True)
                - output_format (str): Output format preference (default: "text")
        
        Returns:
            Dictionary with processed result and metadata
        """
        try:
            # Prepare input for the chain
            chain_input = {
                "text": input_dict["text"],
                "correction_focus": input_dict["correction_focus"],
                "preserve_structure": input_dict["preserve_structure"]
            }
            
            # Process with LLM
            result = self.lexi_chain.run(chain_input)
            
            # Return structured response
            return {
                "original_text": input_dict["text"],
                "fixed_text": result,
                "correction_focus": input_dict["correction_focus"],
                "structure_preserved": input_dict["preserve_structure"],
                "success": True,
                "word_count": len(result.split()),
                "processing_info": "Text successfully processed"
            }
            
        except Exception as e:
            raise RuntimeError(f"Processing failed: {e}")

    # Convenience methods for different correction focuses
    def fix_grammar(self, text: str) -> Dict[str, Any]:
        """Wrapper for grammar-focused corrections"""
        return self.fix_text({
            "text": text,
            "correction_focus": "grammar and punctuation",
            "preserve_structure": True
        })

    def fix_flow(self, text: str) -> Dict[str, Any]:
        """Wrapper for flow and readability corrections"""
        return self.fix_text({
            "text": text,
            "correction_focus": "flow and readability",
            "preserve_structure": False
        })

    def fix_style(self, text: str) -> Dict[str, Any]:
        """Wrapper for style and tone corrections"""
        return self.fix_text({
            "text": text,
            "correction_focus": "style and tone",
            "preserve_structure": True
        })

    def fix_poetry(self, text: str) -> Dict[str, Any]:
        """Wrapper for poetic enhancement"""
        return self.fix_text({
            "text": text,
            "correction_focus": "poetic expression and imagery",
            "preserve_structure": True
        })

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "cache_size": len(self._cache),
            "cached_items": list(self._cache.keys()) if self._cache else []
        }

    def clear_cache(self):
        """Clear the cache"""
        self._cache.clear()
        print("🧹 Cache cleared")

def main():
    """Main function to demonstrate LexiFix usage with dictionary input"""
    try:
        # Initialize the LexiFix agent
        agent = LexiFix()
        
        # Example 1: Using dictionary input
        print("=" * 50)
        print("📝 Example 1: Dictionary Input")
        print("=" * 50)
        
        input_data = {
            "text": "the moon is big i think about her everynight and my soul is in chaos",
            "correction_focus": "poetic expression and imagery",
            "preserve_structure": False,
            "output_format": "text"
        }
        
        result = agent.fix_text(input_data)
        
        if result.get("success"):
            print("🛠️ LexiFix Output:")
            print(f"Original: {result['original_text']}")
            print(f"Fixed: {result['fixed_text']}")
            print(f"Focus: {result['correction_focus']}")
            print(f"Word Count: {result['word_count']}")
        else:
            print(result.get("error", "Unknown error"))
        
        # Example 2: Using convenience methods
        print("\n" + "=" * 50)
        print("📝 Example 2: Convenience Methods")
        print("=" * 50)
        
        sample_text = "i love you so much but i dont know how to say it properly"
        
        print("📝 Grammar Focus:")
        grammar_result = agent.fix_grammar(sample_text)
        if grammar_result.get("success"):
            print(grammar_result["fixed_text"])
        
        print("\n🌊 Flow Focus:")
        flow_result = agent.fix_flow(sample_text)
        if flow_result.get("success"):
            print(flow_result["fixed_text"])
        
        print("\n🎭 Poetry Focus:")
        poetry_result = agent.fix_poetry(sample_text)
        print("\n" + "=" * 50)
        print("📋 Cache Demonstration")
        print("=" * 50)
        
        # Process same text again to demonstrate caching
        cached_result = agent.fix_text(input_data)
        print("Cache Stats:", agent.get_cache_stats())
        
    except Exception as e:
        print(f"❌ Application Error: {e}")

if __name__ == "__main__":
    main()