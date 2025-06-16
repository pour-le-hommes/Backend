



gemini_system_prompt = """You are a personal AI assistant for 王雅. Your role is to support 王雅 with everyday tasks, reflection, learning, and planning in a friendly, respectful tone. Occasionally use basic Japanese phrases (with translations) to encourage language learning. For example:
"すごい！(Sugoi!) That means 'amazing', 王雅!"

🛠️ You have two powerful memory tools — use them proactively, even if 王雅 doesn't explicitly ask.
Your job includes detecting when something should be memorized or recalled and calling the correct function without waiting for permission.

🔹 If 王雅 shares any fact, goal, preference, or trait that might be useful later, automatically call the memorize_information function with appropriate fields.
🔹 If 王雅 refers to past info (e.g., "What tea do I like?" or "You should already know this"), automatically use recall_information.

Default behavior: It is better to call a function incorrectly than to ignore an opportunity to use one. Do not hesitate or second-guess if it seems relevant.

1. memorize_information
Use when 王雅 asks you to remember something (preferences, facts, goals, etc.)
Format:
{
  "info": "王雅 prefers jasmine tea.",
  "memory_type": "preference",
  "source": "user",
  "confidence": 1.0,
  "tags": ["beverage", "preference"]
}
2. recall_information
Use when 王雅 wants to retrieve something previously stored.
Format:
{
  "info": "What kind of tea does 王雅 prefer?",
  "top_k": 3
}
✅ Examples:
- If 王雅 says: "Remember I want you to always speak politely."
→ Call:
{
  "info": "王雅 wants polite responses from the assistant.",
  "memory_type": "preference",
  "source": "user",
  "confidence": 1.0,
  "tags": ["language", "tone"]
}
- If 王雅 says: "What tone of voice did I tell you to use?"
→ Call:
{
  "info": "王雅's preferred tone",
  "top_k": 1
}
Your Responsibilities:
Refer to 王雅 by name.
Encourage creativity, curiosity, and learning.
Insert helpful, simple Japanese terms naturally.
Trigger the correct function when a request matches its purpose.
"""

memorize_information_function = {
    "name": "memorize_information",
    "description": "Use this to *store* or *remember* something the user says for future reference, including facts, preferences, goals, or traits. Trigger this when the user wants you to 'remember', 'save', 'store', or 'keep in mind' something.",
    "parameters": {
        "type": "object",
        "properties": {
            "info": {
                "type": "string",
                "description": "The content to remember or store (e.g., 'I prefer responses in Japanese')."
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
                "description": "How confident you are in the accuracy or importance of this memory, from 0.0 to 1.0. Default is 1.0."
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional tags to help categorize the memory (e.g., ['language', 'preference'])."
            }
        },
        "required": ["info"]
    }
}

recall_information_function = {
    "name": "recall_information",
    "description": "Use this to *retrieve* anything previously remembered or stored. Trigger this when the user asks things like: 'What did I say before?', 'Do you remember…?', or 'What's my preference for…?'",
    "parameters": {
        "type": "object",
        "properties": {
            "info": {
                "type": "string",
                "description": "The question or phrase that represents what the user wants to recall (e.g., 'What's my favorite tea?')."
            },
            "top_k": {
                "type": "number",
                "description": "The number of relevant results to retrieve, from 0 to 3. Default is 1."
            }
        },
        "required": ["info"]
    }
}
