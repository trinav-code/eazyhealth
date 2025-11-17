"""
LLM Client service for interacting with language models.
Supports both Anthropic (Claude) and OpenAI with abstraction.
"""
import json
from typing import Optional, Dict, Any, List
from app.config import settings, ReadingLevel, READING_LEVEL_PROMPTS


class LLMClient:
    """
    Abstracted LLM client supporting multiple providers.
    """

    def __init__(self):
        self.provider = settings.llm_provider
        self.model = settings.llm_model

        if self.provider == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            import anthropic
            self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        elif self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            import openai
            self.client = openai.OpenAI(api_key=settings.openai_api_key)

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _call_anthropic(self, prompt: str, system_prompt: str = "") -> str:
        """Call Anthropic's Claude API."""
        messages = [{"role": "user", "content": prompt}]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=settings.llm_max_tokens,
            temperature=settings.llm_temperature,
            system=system_prompt if system_prompt else None,
            messages=messages,
        )

        return response.content[0].text

    def _call_openai(self, prompt: str, system_prompt: str = "") -> str:
        """Call OpenAI's GPT API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=settings.llm_max_tokens,
            temperature=settings.llm_temperature,
            messages=messages,
        )

        return response.choices[0].message.content

    def call(self, prompt: str, system_prompt: str = "") -> str:
        """
        Call the configured LLM provider with the given prompt.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt (instructions)

        Returns:
            The LLM's response text
        """
        if self.provider == "anthropic":
            return self._call_anthropic(prompt, system_prompt)
        elif self.provider == "openai":
            return self._call_openai(prompt, system_prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate_explainer(
        self,
        input_text: str,
        topic_hint: Optional[str] = None,
        reading_level: ReadingLevel = ReadingLevel.GRADE_6,
    ) -> Dict[str, Any]:
        """
        Generate a patient-friendly health explainer.

        Args:
            input_text: The article text or information to explain
            topic_hint: Optional hint about the topic (e.g., "atrial fibrillation")
            reading_level: Target reading comprehension level

        Returns:
            Dictionary with title, sections, and disclaimer
        """
        reading_instruction = READING_LEVEL_PROMPTS.get(
            reading_level,
            READING_LEVEL_PROMPTS[ReadingLevel.GRADE_6]
        )

        system_prompt = """You are a medical writing assistant specializing in health education.
Your job is to take complex health information and make it accessible to general audiences.
You NEVER provide personalized medical advice or diagnosis.
You always include appropriate disclaimers."""

        user_prompt = f"""Task: Rewrite the following health information for a general audience.

Reading Level: {reading_instruction}

Topic Hint: {topic_hint if topic_hint else 'General health information'}

Structure your response as a JSON object with this exact format:
{{
  "title": "Clear, engaging title for this topic",
  "sections": [
    {{"heading": "Overview", "content": "Brief overview paragraph"}},
    {{"heading": "Key Points", "content": "Bullet points or short paragraphs with main takeaways"}},
    {{"heading": "Symptoms & Warning Signs", "content": "If applicable, describe symptoms"}},
    {{"heading": "What Patients Can Do", "content": "General guidance, NOT personalized advice"}},
    {{"heading": "When to Seek Medical Care", "content": "If applicable, when to contact a doctor"}}
  ],
  "disclaimer": "This information is for general educational purposes only and is not medical advice. Please consult a healthcare professional for personalized medical guidance."
}}

Important rules:
- Do NOT hallucinate information not present in the source
- Do NOT provide personalized medical advice
- Use hedging language ("may", "can", "generally", etc.)
- Always include the disclaimer
- Omit sections if not applicable (e.g., no symptoms for a general wellness topic)

Here is the input text to rewrite:

{input_text}

Return ONLY the JSON object, no other text."""

        response_text = self.call(user_prompt, system_prompt)

        # Parse JSON response
        try:
            # Try to extract JSON if wrapped in markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            result = json.loads(response_text)
            return result
        except json.JSONDecodeError as e:
            # Fallback if JSON parsing fails
            return {
                "title": topic_hint or "Health Information",
                "sections": [
                    {
                        "heading": "Content",
                        "content": response_text
                    }
                ],
                "disclaimer": "This information is for general educational purposes only and is not medical advice. Please consult a healthcare professional for personalized medical guidance."
            }

    def generate_briefing(
        self,
        source_type: str,
        data: Dict[str, Any],
        reading_level: ReadingLevel = ReadingLevel.GRADE_8,
    ) -> Dict[str, Any]:
        """
        Generate an auto-briefing post.

        Args:
            source_type: "data_analysis" or "article_summary"
            data: Input data (stats for analysis, article content for summary)
            reading_level: Target reading comprehension level

        Returns:
            Dictionary with title, summary, body_markdown, and disclaimer
        """
        reading_instruction = READING_LEVEL_PROMPTS.get(
            reading_level,
            READING_LEVEL_PROMPTS[ReadingLevel.GRADE_8]
        )

        if source_type == "data_analysis":
            return self._generate_data_analysis_briefing(data, reading_instruction)
        elif source_type == "article_summary":
            return self._generate_article_summary_briefing(data, reading_instruction)
        else:
            raise ValueError(f"Unknown source_type: {source_type}")

    def _generate_data_analysis_briefing(
        self,
        stats_data: Dict[str, Any],
        reading_instruction: str
    ) -> Dict[str, Any]:
        """Generate briefing from disease data analysis."""
        system_prompt = """You are a public health communicator writing weekly summaries for the general public.
You analyze disease surveillance data and explain trends in accessible language.
You avoid alarmism and always provide context."""

        user_prompt = f"""Task: Write a weekly health briefing based on disease surveillance data.

Reading Level: {reading_instruction}

Data Summary:
{json.dumps(stats_data, indent=2)}

Structure your response as a JSON object:
{{
  "title": "Engaging title for this week's briefing",
  "summary": "1-2 sentence snapshot for preview",
  "body_markdown": "Full briefing in markdown format with sections:\\n\\n## Snapshot\\n...\\n\\n## What's Trending\\n...\\n\\n## Context & Factors\\n...\\n\\n## How to Stay Informed\\n...",
  "tags": ["covid", "flu", "respiratory"],
  "disclaimer": "This information is for general educational purposes only and is not medical advice. Data may change as more information becomes available."
}}

Important:
- Use cautious language ("data suggests", "appears to show", etc.)
- Provide context (seasonal patterns, data limitations)
- Do NOT provide personalized medical advice
- Do NOT cause unnecessary alarm
- Focus on trends, not individual risk

Return ONLY the JSON object."""

        response_text = self.call(user_prompt, system_prompt)

        try:
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            return json.loads(response_text)
        except json.JSONDecodeError:
            return {
                "title": "Weekly Health Briefing",
                "summary": "Analysis of current health trends.",
                "body_markdown": response_text,
                "tags": [],
                "disclaimer": "This information is for general educational purposes only and is not medical advice."
            }

    def _generate_article_summary_briefing(
        self,
        article_data: Dict[str, Any],
        reading_instruction: str
    ) -> Dict[str, Any]:
        """Generate briefing from summarizing news articles."""
        system_prompt = """You are a health news summarizer for general audiences.
You take recent health research or news articles and create accessible summaries.
You cite sources and distinguish between preliminary research and established facts."""

        articles_text = "\n\n---\n\n".join([
            f"Source: {article.get('url', 'N/A')}\nTitle: {article.get('title', 'N/A')}\nContent: {article.get('content', 'N/A')}"
            for article in article_data.get("articles", [])
        ])

        user_prompt = f"""Task: Write a briefing summarizing recent health news articles.

Reading Level: {reading_instruction}

Articles:
{articles_text}

Structure your response as a JSON object:
{{
  "title": "Engaging title summarizing the news",
  "summary": "1-2 sentence overview",
  "body_markdown": "Full summary in markdown with sections:\\n\\n## Overview\\n...\\n\\n## Key Findings\\n...\\n\\n## What This Means\\n...\\n\\n## Sources\\n...",
  "tags": ["research", "treatment", "etc"],
  "disclaimer": "This information is for general educational purposes only and is not medical advice. Research findings may be preliminary."
}}

Important:
- Distinguish between correlation and causation
- Note if research is preliminary, in animals, or small sample
- Cite all sources
- Do NOT overstate findings
- Do NOT provide medical advice

Return ONLY the JSON object."""

        response_text = self.call(user_prompt, system_prompt)

        try:
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            return json.loads(response_text)
        except json.JSONDecodeError:
            return {
                "title": "Health News Summary",
                "summary": "Recent developments in health research.",
                "body_markdown": response_text,
                "tags": [],
                "disclaimer": "This information is for general educational purposes only and is not medical advice."
            }


# Global LLM client instance
llm_client = LLMClient()
