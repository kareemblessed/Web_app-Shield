"""
PayShield Challenge Generator
Single source of truth for all challenge phrases
"""

import json
import secrets
import os
import logging
from typing import List, Dict, Any
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChallengeGenerator:
    """Generates secure challenge phrases using Diceware wordlist"""
    
    def __init__(self, wordlist_path: str = "diceware.txt"):
        """
        Initialize the challenge generator
        
        Args:
            wordlist_path: Path to the Diceware wordlist file
        """
        self.wordlist_path = wordlist_path
        self._wordlist: List[str] = []
        self._load_wordlist()
    
    def _load_wordlist(self) -> None:
        """Load the 2048-word Diceware list from file"""
        try:
            wordlist_file = Path(self.wordlist_path)
            if not wordlist_file.exists():
                logger.error(f"Diceware wordlist not found at {self.wordlist_path}")
                raise FileNotFoundError(f"Diceware wordlist not found at {self.wordlist_path}")
            
            with open(wordlist_file, 'r', encoding='utf-8') as f:
                self._wordlist = [line.strip() for line in f if line.strip()]
            
            logger.info(f"Loaded {len(self._wordlist)} words from Diceware wordlist")
            
            if len(self._wordlist) != 2048:
                logger.warning(f"Expected 2048 words, but loaded {len(self._wordlist)} words")
                
        except Exception as e:
            logger.error(f"Failed to load wordlist: {e}")
            raise
    
    def generate_challenge(self, word_count: int = 3) -> Dict[str, Any]:
        """
        Generate a challenge phrase with specified number of words
        
        Args:
            word_count: Number of words in the challenge (3 or 6)
            
        Returns:
            Dictionary with the challenge phrase
        """
        if word_count not in [3, 6]:
            logger.warning(f"Unusual word count requested: {word_count}. Recommended: 3 or 6")
        
        if not self._wordlist:
            raise RuntimeError("Wordlist not loaded. Cannot generate challenge.")
        
        # Use secrets.choice for cryptographically secure random selection
        selected_words = [secrets.choice(self._wordlist) for _ in range(word_count)]
        phrase = " ".join(selected_words)
        
        logger.info(f"Generated {word_count}-word challenge phrase")
        
        return {"phrase": phrase}
    
    def generate_challenge_json(self, word_count: int = 3) -> str:
        """
        Generate a challenge phrase and return as JSON string
        
        Args:
            word_count: Number of words in the challenge (3 or 6)
            
        Returns:
            JSON string containing the challenge phrase
        """
        challenge = self.generate_challenge(word_count)
        return json.dumps(challenge)
    
    def reload_wordlist(self) -> None:
        """Reload the wordlist from file (useful for updates)"""
        logger.info("Reloading Diceware wordlist")
        self._load_wordlist()
    
    @property
    def wordlist_size(self) -> int:
        """Get the current wordlist size"""
        return len(self._wordlist)


# Global instance for use by FastAPI routes
challenge_generator = ChallengeGenerator()


def get_challenge(word_count: int = 3) -> Dict[str, Any]:
    """
    Convenience function for FastAPI route usage
    
    Args:
        word_count: Number of words in the challenge (3 or 6)
        
    Returns:
        Dictionary with the challenge phrase
    """
    return challenge_generator.generate_challenge(word_count)


def get_challenge_json(word_count: int = 3) -> str:
    """
    Convenience function for FastAPI route usage (JSON response)
    
    Args:
        word_count: Number of words in the challenge (3 or 6)
        
    Returns:
        JSON string containing the challenge phrase
    """
    return challenge_generator.generate_challenge_json(word_count)


if __name__ == "__main__":
    # Test the challenge generator
    generator = ChallengeGenerator()
    
    print("Testing 3-word challenge:")
    print(generator.generate_challenge_json(3))
    
    print("\nTesting 6-word challenge:")
    print(generator.generate_challenge_json(6))
    
    print(f"\nWordlist contains {generator.wordlist_size} words")