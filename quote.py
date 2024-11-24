import json
from typing import List, Optional, Dict, Union
import random
from datetime import datetime

class QuoteGenerator:
    def __init__(self, json_file: str = 'quotes.json'):
        """Initialize the QuoteGenerator with a JSON file containing quotes."""
        self.quotes = self._load_quotes(json_file)
        self.metadata = self._load_metadata(json_file)
        self.used_quotes = set()  # Track used quotes
        self._load_used_quotes()  # Load previously used quotes

    def _load_quotes(self, json_file: str) -> List[Dict]:
        """Load quotes from JSON file."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data['quotes']
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find quotes file: {json_file}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {json_file}")

    def _load_metadata(self, json_file: str) -> Dict:
        """Load metadata from JSON file."""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['metadata']

    def _load_used_quotes(self):
        """Load previously used quotes from a tracking file."""
        try:
            with open('used_quotes.json', 'r') as f:
                self.used_quotes = set(json.load(f))
        except FileNotFoundError:
            self.used_quotes = set()

    def _save_used_quotes(self):
        """Save used quotes to a tracking file."""
        with open('used_quotes.json', 'w') as f:
            json.dump(list(self.used_quotes), f)


    def get_random_quote(self) -> tuple:
        """Get a random unused quote from the database."""
        available_quotes = [q for q in self.quotes if q["text"] not in self.used_quotes]
        
        # If all quotes have been used, reset the tracking
        if not available_quotes:
            self.used_quotes.clear()
            available_quotes = self.quotes
        
        quote = random.choice(available_quotes)
        self.used_quotes.add(quote["text"])
        self._save_used_quotes()
        
        return (
            quote["text"],
            quote["author"],
            quote["categories"],
            quote["year"],
            quote["source"]
        )

def format_quote(quote_tuple: tuple) -> str:
    """Format a quote tuple for display."""
    text, author, categories, year, source = quote_tuple
    year_str = f" ({year})" if year else ""
    categories_str = f"Categories: {', '.join(categories)}"
    return f'"{text}"\n- {author}{year_str}\nSource: {source}\n{categories_str}'

def get_random_quote():
    generator = QuoteGenerator()
    return format_quote(generator.get_random_quote())

def main():    
    generator = QuoteGenerator()
    print(format_quote(generator.get_random_quote()))
    
if __name__ == "__main__":
    main() 