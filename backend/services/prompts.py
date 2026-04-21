# backend/services/prompts.py

SYSTEM_PROMPTS = {
    "wealth_advisor": """# ~60 tokens
    You are a concise Indian personal finance assistant. 
    Give specific, actionable advice. Use ₹ for amounts.
    Never guarantee returns. Always say "for simulation purposes."
    Respond in 2-3 sentences max unless asked for more.
    """,

    "narrator": """# ~40 tokens
    Rewrite the provided financial insight in a warm, encouraging tone.
    Keep all numbers exact. Maximum 3 sentences. No jargon.
    """,

    "goal_advisor": """# ~50 tokens
    You help users set and achieve financial goals in India.
    Be specific with amounts and timelines. 
    When suggesting SIPs, reference real fund categories (not specific funds).
    """,
}

USER_PROMPT_TEMPLATES = {
    "chat_response": """# ~30 tokens + context
    User: {user_message}
    Context: {context_json}
    Answer in 2-3 sentences. If calculation needed, show it briefly.
    """,

    "explain_recommendation": """# ~20 tokens + action
    Explain this in simple terms: {action_description}
    One sentence why, one sentence what to do.
    """,

    "narrator_rewrite": """# ~15 tokens + text
    Original: {template_output}
    Rewrite warmer. Keep all numbers. Max 3 sentences.
    """,

    "goal_setup": """# ~25 tokens + goal
    User wants: {goal_description}
    Suggest: target amount, timeline, monthly saving needed.
    Format as JSON: {{"amount": value, "months": value, "monthly_saving": value, "rationale": "text"}}
    """,

    "weekly_nudge": """# ~30 tokens + summary
    Financial week summary: {summary_data}
    Write one encouraging sentence highlighting {positive_metric}.
    Start with the user's name: {user_name}.
    """,
}

def build_prompt(template_key: str, **kwargs) -> str:
    template = USER_PROMPT_TEMPLATES.get(template_key)
    if not template:
        raise ValueError(f"Prompt template {template_key} not found")
    return template.format(**kwargs)

def estimate_tokens(text: str) -> int:
    return len(text) // 4
