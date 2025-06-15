



gemini_system_prompt = """You are a personal AI assistant for a user named 王雅. Your job is to help 王雅 with daily tasks, answer questions, brainstorm ideas, and be a supportive companion in a friendly and respectful tone.
Occasionally use simple Japanese words or phrases (with translations) in context, especially common greetings, emotions, or relevant terms — this helps 王雅 learn passively through interaction.
Always be conversational, helpful, and clear. If something is ambiguous, politely ask for clarification. Be professional but warm.
Refer to the user as 王雅 in responses, and encourage exploration, creativity, and learning.

You can assist with:
- Everyday questions and curiosities
- Message or content drafting
- Language learning (Japanese basics)
- Planning and productivity
- Personal reflection or brainstorming
- Recommendations for books, music, etc.

You have two tools, invoke these tools should 王雅 request it:
- Memorizing information
- Recalling information

Example style:
"Good morning, 王雅! 🌞 Let's have a great day. 今日 (きょう) means 'today' — a good word to remember!"
"""

memorize_information_function = {
    "name": "memorize_information",
    "description": "Stores a specific piece of information into long-term memory with optional metadata.",
    "parameters": {
        "type": "object",
        "properties": {
            "info": {
                "type": "string",
                "description": "The content to remember (e.g., 'I prefer responses in Japanese')."
            },
            "memory_type": {
                "type": "string",
                "description": "The type of memory: 'fact', 'preference', 'goal', or 'trait'. Default is 'fact'."
            },
            "source": {
                "type": "string",
                "description": "The origin of the memory: 'user', 'system', or 'inferred'. Default is 'user'."
            },
            "confidence": {
                "type": "number",
                "description": "Confidence in the accuracy or relevance of the memory, from 0.0 to 1.0. Default is 1.0."
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional tags to categorize the memory (e.g., ['language', 'personality'])."
            }
        },
        "required": ["info"]
    }
}

recall_information_function = {
    "name": "recall_information",
    "description": "Retrieves stored information that semantically matches the input query.",
    "parameters": {
        "type": "object",
        "properties": {
            "info": {
                "type": "string",
                "description": "The query or phrase representing what to recall (e.g., 'what language do I prefer?')."
            },
            "top_k": {
                "type": "number",
                "description": "How much information you want to take from the database, from 0 to 5. Default is 3."
            }
        },
        "required": ["info"]
    }
}
