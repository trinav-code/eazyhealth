"""
Token counter utility for managing LLM token limits.
"""
import tiktoken
from typing import List, Dict, Any


class TokenCounter:
    """
    Counts tokens to stay within LLM limits.
    """

    def __init__(self, model: str = "gpt-4", max_input_tokens: int = 8000):
        """
        Initialize token counter.

        Args:
            model: Model name for token encoding
            max_input_tokens: Maximum tokens to send (leaves room for response)
        """
        self.model = model
        self.max_input_tokens = max_input_tokens
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.

        Args:
            text: Text to count

        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))

    def count_tokens_dict(self, data: Dict[str, Any]) -> int:
        """
        Count tokens in a dictionary (converts to string).

        Args:
            data: Dictionary to count

        Returns:
            Number of tokens
        """
        import json
        text = json.dumps(data, indent=2)
        return self.count_tokens(text)

    def select_articles_within_limit(
        self,
        articles: List[Dict[str, Any]],
        base_prompt_tokens: int = 500,
    ) -> List[Dict[str, Any]]:
        """
        Select as many articles as possible without exceeding token limit.
        Skips articles that are too long and continues checking others.

        Args:
            articles: List of articles with 'text' field
            base_prompt_tokens: Estimated tokens for system prompt/instructions

        Returns:
            Subset of articles that fit within token limit
        """
        selected = []
        total_tokens = base_prompt_tokens

        for i, article in enumerate(articles, 1):
            article_text = article.get("text", "")
            article_tokens = self.count_tokens(article_text)

            # Check if adding this article would exceed limit
            if total_tokens + article_tokens <= self.max_input_tokens:
                selected.append(article)
                total_tokens += article_tokens
                print(
                    f"✓ Added article #{i} ({article_tokens} tokens). "
                    f"Total: {total_tokens}/{self.max_input_tokens}"
                )
            else:
                print(
                    f"✗ Skipping article #{i} ({article_tokens} tokens) - would exceed limit. "
                    f"Current: {total_tokens}/{self.max_input_tokens}"
                )
                # Continue checking remaining articles instead of breaking
                # This allows us to skip overly long articles and still use shorter ones

        print(f"Final: Selected {len(selected)}/{len(articles)} articles, {total_tokens} total tokens")
        return selected


# Global token counter instance
# Leave room for completion: 8192 total - 4096 completion = 4096 for input
token_counter = TokenCounter(model="gpt-4", max_input_tokens=4000)
