"""
Claude API Client for Meeting Notes Summarization

This module handles all interactions with Claude's API, including:
- Summarization
- Sentiment analysis
- Topic extraction
- Error handling
- Rate limit management
"""

import os
import time
import json
from datetime import datetime
from anthropic import Anthropic, APIError, RateLimitError, APIConnectionError


class ClaudeClient:
    """
    Client for interacting with Claude API.

    PM Learning Notes:
    - This class encapsulates API logic, making it reusable
    - Error handling is centralized here
    - Cost tracking happens at the API boundary
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the Claude client.

        Args:
            api_key: Anthropic API key (if None, reads from environment)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = Anthropic(api_key=self.api_key)
        # Using Claude 3 Haiku - fastest, most widely available model
        self.model = "claude-3-haiku-20240307"

        # PM Insight: These are real pricing numbers for Claude 3 Haiku
        # Input: $0.25 per million tokens
        # Output: $1.25 per million tokens
        self.input_cost_per_token = 0.25 / 1_000_000
        self.output_cost_per_token = 1.25 / 1_000_000

    def summarize_meeting(self, notes: str, include_topics: bool = True) -> dict:
        """
        Summarize meeting notes using Claude API.

        Args:
            notes: The meeting transcript or notes
            include_topics: Whether to include topic extraction

        Returns:
            dict with summary, sentiment, topics, and metadata

        PM Insight: This single function makes multiple "asks" of the AI.
        We could split this into 3 API calls (summary, sentiment, topics),
        but that would be slower and more expensive. This is a common optimization.
        """
        start_time = time.time()

        try:
            # Build the prompt based on what's requested
            prompt = self._build_prompt(notes, include_topics)

            # PM Insight: This is the actual API call - everything before was prep
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,  # PM Insight: This caps how much the AI can write back
                temperature=0.7,  # PM Insight: Controls randomness (0=deterministic, 1=creative)
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Calculate costs and timing
            processing_time = time.time() - start_time
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            # PM Insight: Real cost calculation - this is what you'd pay
            estimated_cost = (
                (input_tokens * self.input_cost_per_token) +
                (output_tokens * self.output_cost_per_token)
            )

            # Parse the response
            result = self._parse_response(response.content[0].text, include_topics)

            # Add metadata that PMs care about
            result['metadata'] = {
                'processing_time': f"{processing_time:.2f}s",
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'estimated_cost': f"{estimated_cost:.6f}",
                'model': self.model,
                'timestamp': datetime.now().isoformat()
            }

            return result

        except RateLimitError as e:
            # PM Insight: This happens when you make too many requests too fast
            raise Exception(
                "Rate limit exceeded. This means you're making too many requests. "
                "In production, you'd implement a queue system or retry logic. "
                f"Technical details: {str(e)}"
            )

        except APIConnectionError as e:
            # PM Insight: Network issues - could be user's internet or API downtime
            raise Exception(
                "Failed to connect to Claude API. This could be a network issue "
                "or API downtime. In production, you'd retry with exponential backoff. "
                f"Technical details: {str(e)}"
            )

        except APIError as e:
            # PM Insight: Something went wrong on Claude's side
            raise Exception(
                f"Claude API error: {str(e)}. This could be due to invalid input, "
                "service issues, or hitting context limits."
            )

        except Exception as e:
            # Catch-all for unexpected errors
            raise Exception(f"Unexpected error: {str(e)}")

    def _build_prompt(self, notes: str, include_topics: bool) -> str:
        """
        Build the prompt to send to Claude.

        PM Insight: Prompt engineering is a real skill. The way you phrase
        the request dramatically affects the quality of results. This is why
        "Prompt Engineer" is now a job title.
        """
        prompt = f"""You are an AI assistant specialized in analyzing meeting notes.

Please analyze the following meeting transcript and provide:

1. **Summary**: A concise bullet-point summary of the key points discussed (3-7 bullets)

2. **Sentiment Analysis**:
   - Overall sentiment: Positive, Neutral, Negative, or Mixed
   - Brief explanation of why you categorized it this way

"""

        if include_topics:
            prompt += """3. **Topics & Keywords**:
   - Main topics discussed (3-5 topics)
   - Key keywords (5-10 single words or short phrases)

"""

        prompt += f"""Meeting Notes:
{notes}

Please format your response as JSON with this structure:
{{
    "summary": "bullet point summary here",
    "sentiment": {{
        "overall": "Positive/Neutral/Negative/Mixed",
        "explanation": "brief explanation"
    }}"""

        if include_topics:
            prompt += """,
    "topics": {
        "main_topics": ["topic1", "topic2", ...],
        "keywords": ["keyword1", "keyword2", ...]
    }"""

        prompt += "\n}\n"

        return prompt

    def _parse_response(self, response_text: str, include_topics: bool) -> dict:
        """
        Parse Claude's response into structured data.

        PM Insight: AI responses can be unpredictable. We need robust parsing
        that handles variations. This is why "structured outputs" are a hot topic
        in AI development.
        """
        try:
            # Try to extract JSON from the response
            # Sometimes Claude wraps JSON in markdown code blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                json_text = response_text[start:end].strip()
            else:
                json_text = response_text.strip()

            parsed = json.loads(json_text)

            # Validate structure
            if 'summary' not in parsed or 'sentiment' not in parsed:
                raise ValueError("Missing required fields in response")

            if include_topics and 'topics' not in parsed:
                # Provide default if topics weren't included
                parsed['topics'] = {
                    'main_topics': [],
                    'keywords': []
                }

            return parsed

        except json.JSONDecodeError:
            # PM Insight: When JSON parsing fails, we need a fallback
            # This is a common pattern in production systems
            return {
                'summary': response_text,
                'sentiment': {
                    'overall': 'Unknown',
                    'explanation': 'Could not parse sentiment from response'
                },
                'topics': {
                    'main_topics': [],
                    'keywords': []
                } if include_topics else None
            }


def get_token_estimate(text: str) -> int:
    """
    Rough estimate of token count.

    PM Insight: Tokens ≈ words * 1.3 for English text.
    Claude uses a different tokenizer than GPT, but this is close enough
    for planning purposes.

    Why this matters: If you know a feature will process 1000-word documents,
    you can estimate costs before building anything.
    """
    word_count = len(text.split())
    return int(word_count * 1.3)


def check_context_window(text: str, max_tokens: int = 200000) -> dict:
    """
    Check if text fits within Claude's context window.

    PM Insight: Claude 3.5 Sonnet has a 200k token context window.
    That's roughly 150,000 words - enough for a short book!
    But longer contexts cost more and take longer to process.
    """
    estimated_tokens = get_token_estimate(text)
    percentage = (estimated_tokens / max_tokens) * 100

    return {
        'estimated_tokens': estimated_tokens,
        'max_tokens': max_tokens,
        'percentage_used': round(percentage, 2),
        'fits': estimated_tokens < max_tokens,
        'warning': percentage > 80  # Warn if using >80% of context
    }
