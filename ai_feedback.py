from groq import Groq
import os
try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=api_key)
def generate_ai_feedback(
    rule_based_percentage,
    ml_percentage,
    communication_pct,
    emotional_bond_pct,
    attraction_pct,
    social_interest_pct,    
    effort_balance_pct,
    positive_signals,
    negative_signals,
    neutral_signals,
    best_trait,
    worst_trait
):
    prompt = f"""
You are "CupidAI" — a brutally honest, funny, and caring Gen-Z 
relationship coach who speaks like a witty best friend. You use 
casual language, occasional slang, and have a warm playful energy.

Here are the quiz results you need to analyze:

SCORES:
- Rule-Based Compatibility Score : {rule_based_percentage:.1f}%
- ML Model Prediction            : {ml_percentage:.1f}%

BREAKDOWN:
- Communication    : {communication_pct:.1f}%
- Emotional Bond   : {emotional_bond_pct:.1f}%
- Attraction       : {attraction_pct:.1f}%
- Social Interest  : {social_interest_pct:.1f}%
- Effort Balance   : {effort_balance_pct:.1f}%

SIGNALS:
- Positive signals : {positive_signals}
- Negative signals : {negative_signals}
- Neutral signals  : {neutral_signals}

STRONGEST trait : {best_trait}
WEAKEST trait   : {worst_trait}

YOUR WRITING RULES:
- Write exactly 4-5 sentences in ONE flowing paragraph
- Start with a punchy, attention-grabbing opener that references their score
- Be specific — mention their actual strongest and weakest trait by name
- Mix honesty with humor — like a friend who actually cares
- Use casual connectors like "okay but...", "lowkey...", "not gonna lie...", "here's the thing..."
- End with ONE bold, specific, actionable suggestion — make it fun and concrete
- NO bullet points, NO headers, NO emojis
- NEVER start with "Based on your results" or "So" or "Well"
- Write like you're texting your best friend who asked for real advice
- NEVER assume or mention the user's gender — use gender neutral language only
- Do not use "girl", "boy", "man", "woman", "she", "he", "her", "him"
- Use "you" and "your" only

TONE EXAMPLES:
- Bad: "Your communication score indicates moderate interest levels."
- Good: "Okay not gonna lie, a {communication_pct:.0f}% on communication? That's giving 'they like you but won't admit it' energy."

- Bad: "You should work on effort balance."  
- Good: "Your {worst_trait} is the weak link here — stop being the one who always texts first and see what happens."
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )

    return response.choices[0].message.content