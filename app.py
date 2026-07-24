# UI of the app
import streamlit as st
import matplotlib.pyplot as plt
from logic import * 
import time
from ml_predictor import predict_ml_compatibility
from ai_feedback import generate_ai_feedback
import base64
from ai_feedback import chat_with_cupidai
def svg_to_img(svg_string):
    b64 = base64.b64encode(svg_string.encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" width="220" height="220"/>'
CATEGORY_SVG = {
    "💬 Communication": """
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="90" fill="#1a1025" opacity="0.5"/>
        <rect x="30" y="50" width="120" height="70" rx="20" fill="#ff4b91" opacity="0.9"/>
        <polygon points="50,120 35,145 75,120" fill="#ff4b91" opacity="0.9"/>
        <circle cx="65" cy="85" r="8" fill="white"/>
        <circle cx="95" cy="85" r="8" fill="white"/>
        <circle cx="125" cy="85" r="8" fill="white"/>
        <rect x="55" y="130" width="110" height="45" rx="15" fill="#c026d3" opacity="0.7"/>
        <polygon points="145,130 160,110 130,130" fill="#c026d3" opacity="0.7"/>
        <circle cx="85" cy="153" r="6" fill="white" opacity="0.8"/>
        <circle cx="110" cy="153" r="6" fill="white" opacity="0.8"/>
        <circle cx="135" cy="153" r="6" fill="white" opacity="0.8"/>
    </svg>
    """,
    "❤️ Emotional Bond": """
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="90" fill="#1a1025" opacity="0.5"/>
        <path d="M100 160 C100 160 30 120 30 75 C30 50 50 35 70 35 
                 C85 35 100 50 100 50 C100 50 115 35 130 35 
                 C150 35 170 50 170 75 C170 120 100 160 100 160Z" 
              fill="#ff4b91"/>
        <path d="M55 55 C55 55 40 48 40 38 C40 30 48 25 55 30 
                 C62 25 70 30 70 38 C70 48 55 55 55 55Z" 
              fill="#c026d3" opacity="0.8"/>
        <path d="M150 45 C150 45 138 39 138 31 C138 24 145 20 150 24 
                 C155 20 162 24 162 31 C162 39 150 45 150 45Z" 
              fill="#c026d3" opacity="0.8"/>
        <circle cx="160" cy="80" r="5" fill="white" opacity="0.7"/>
        <circle cx="40" cy="100" r="4" fill="white" opacity="0.5"/>
        <circle cx="130" cy="50" r="3" fill="white" opacity="0.6"/>
    </svg>
    """,
    "👀 Attraction": """
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="90" fill="#1a1025" opacity="0.5"/>
        <path d="M20 100 C20 100 60 45 100 45 C140 45 180 100 180 100 
                 C180 100 140 155 100 155 C60 155 20 100 20 100Z" 
              fill="white" opacity="0.95"/>
        <circle cx="100" cy="100" r="35" fill="#ff4b91"/>
        <circle cx="100" cy="100" r="20" fill="#1a1025"/>
        <circle cx="112" cy="88" r="8" fill="white" opacity="0.8"/>
        <circle cx="90" cy="110" r="4" fill="white" opacity="0.4"/>
        <line x1="60" y1="60" x2="55" y2="45" 
              stroke="#ff4b91" stroke-width="3" stroke-linecap="round"/>
        <line x1="80" y1="50" x2="78" y2="35" 
              stroke="#ff4b91" stroke-width="3" stroke-linecap="round"/>
        <line x1="100" y1="46" x2="100" y2="30" 
              stroke="#ff4b91" stroke-width="3" stroke-linecap="round"/>
        <line x1="120" y1="50" x2="122" y2="35" 
              stroke="#ff4b91" stroke-width="3" stroke-linecap="round"/>
        <line x1="140" y1="60" x2="145" y2="45" 
              stroke="#ff4b91" stroke-width="3" stroke-linecap="round"/>
    </svg>
    """,
    "📱 Social Interest": """
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="90" fill="#1a1025" opacity="0.5"/>
        <rect x="65" y="30" width="70" height="140" rx="15" fill="#2a1a2e" stroke="#ff4b91" stroke-width="3"/>
        <rect x="72" y="50" width="56" height="95" rx="5" fill="#1a1025"/>
        <circle cx="100" cy="158" r="6" fill="#ff4b91" opacity="0.7"/>
        <rect x="77" y="55" width="16" height="16" rx="3" fill="#ff4b91" opacity="0.8"/>
        <rect x="97" y="55" width="16" height="16" rx="3" fill="#c026d3" opacity="0.8"/>
        <rect x="117" y="55" width="16" height="16" rx="3" fill="#ff4b91" opacity="0.6"/>
        <rect x="77" y="75" width="16" height="16" rx="3" fill="#c026d3" opacity="0.6"/>
        <rect x="97" y="75" width="16" height="16" rx="3" fill="#ff4b91" opacity="0.9"/>
        <rect x="117" y="75" width="16" height="16" rx="3" fill="#c026d3" opacity="0.8"/>
        <circle cx="148" cy="48" r="14" fill="#ff4b91"/>
        <path d="M148 56 C148 56 138 50 138 44 C138 40 142 37 148 41 
                 C154 37 158 40 158 44 C158 50 148 56 148 56Z" 
              fill="white"/>
        <circle cx="65" cy="50" r="8" fill="#ff4b91"/>
        <text x="65" y="54" text-anchor="middle" fill="white" font-size="9" font-weight="bold">3</text>
    </svg>
    """,
    "🤝 Effort Balance": """
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="90" fill="#1a1025" opacity="0.5"/>
        <rect x="95" y="60" width="10" height="90" rx="5" fill="#ff4b91"/>
        <rect x="70" y="148" width="60" height="10" rx="5" fill="#ff4b91"/>
        <rect x="30" y="85" width="140" height="8" rx="4" fill="#c026d3"/>
        <path d="M30 93 Q55 115 80 93" fill="none" stroke="#ff4b91" stroke-width="3"/>
        <ellipse cx="55" cy="115" rx="25" ry="6" fill="#ff4b91" opacity="0.7"/>
        <path d="M120 93 Q145 115 170 93" fill="none" stroke="#ff4b91" stroke-width="3"/>
        <ellipse cx="145" cy="115" rx="25" ry="6" fill="#ff4b91" opacity="0.7"/>
        <path d="M55 109 C55 109 42 100 42 92 C42 86 48 82 55 87 
                 C62 82 68 86 68 92 C68 100 55 109 55 109Z" 
              fill="white"/>
        <path d="M145 109 C145 109 132 100 132 92 C132 86 138 82 145 87 
                 C152 82 158 86 158 92 C158 100 145 109 145 109Z" 
              fill="white"/>
        <circle cx="165" cy="65" r="4" fill="white" opacity="0.6"/>
        <circle cx="35" cy="70" r="3" fill="white" opacity="0.4"/>
    </svg>
    """,
    "💘 Compatibility": """
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="90" fill="#1a1025" opacity="0.5"/>
        <path d="M100 160 C100 160 30 120 30 75 C30 50 50 35 70 35 
                 C85 35 100 50 100 50 C100 50 115 35 130 35 
                 C150 35 170 50 170 75 C170 120 100 160 100 160Z" 
              fill="#ff4b91" opacity="0.9"/>
        <circle cx="100" cy="100" r="25" fill="white" opacity="0.2"/>
        <circle cx="165" cy="65" r="5" fill="white" opacity="0.6"/>
        <circle cx="35" cy="70" r="4" fill="white" opacity="0.4"/>
        <circle cx="150" cy="150" r="3" fill="white" opacity="0.5"/>
    </svg>
    """
}
st.markdown("""
<style>
.left-panel {
    position: fixed;
    left: 0;
    top: 100px;
    width: 240px;
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
}
.right-panel {
    position: fixed;
    right: 0;
    top: 120px;
    width: 200px;
    z-index: 999;
    background: linear-gradient(145deg, #1E1E2E, #2a1a2e);
    border: 1px solid rgba(255,75,145,0.3);
    border-radius: 16px 0 0 16px;
    padding: 18px;
    color: white;
}
.right-panel-label {
    color: #ff4b91;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 10px;
    text-transform: uppercase;
}
.right-panel-text {
    font-size: 12px;
    line-height: 1.7;
    color: #DDDDDD;
}
.right-panel-category {
    margin-top: 12px;
    font-size: 11px;
    color: #ff4b91;
    font-weight: 600;
}</style>""", unsafe_allow_html=True)
with st.sidebar:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1025 0%, #0E1117 100%);
        border-right: 1px solid rgba(255,75,145,0.2);
    }
    .sidebar-title {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(90deg, #ff4b91, #c026d3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .sidebar-subtitle {
        font-size: 12.5px;
        font-weight: 600;
        color: #ff9ac6;
        letter-spacing: 0.3px;
        margin-bottom: 18px;
        line-height: 1.4;
    }
    .sidebar-desc {
        font-size: 13px;
        color: #cccccc;
        line-height: 1.7;
        margin-bottom: 18px;
    }
    .sidebar-divider {
        border: none;
        border-top: 1px solid rgba(255,75,145,0.25);
        margin: 14px 0;
    }
    .sidebar-tag {
        display: inline-block;
        background: rgba(255,75,145,0.12);
        border: 1px solid rgba(255,75,145,0.3);
        color: #ff9ac6;
        font-size: 10.5px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 12px;
        margin: 3px 4px 3px 0;
    }
    </style>

    <div class="sidebar-title">SignalIQ</div>
    <div class="sidebar-subtitle">AI-Based Behavioural Pattern Recognition<br>& Likeability Index Predictor</div>
    <hr class="sidebar-divider">
    <div class="sidebar-desc">
        SignalIQ analyzes everyday behavioral signals — texting habits, 
        social media activity, and in-person cues — using a rule-based 
        scoring engine, a machine learning model trained on real 
        relationship-research data, and a conversational AI coach, 
        to estimate compatibility and interest level.
    </div>
    <hr class="sidebar-divider">
    <div>
        <span class="sidebar-tag">🌲 Random Forest</span>
        <span class="sidebar-tag">🤖 Llama 3.1</span>
        <span class="sidebar-tag">🎙️ Whisper</span>
        <span class="sidebar-tag">📊 Streamlit</span>
    </div>
    """, unsafe_allow_html=True)
def main_percentage_progress_bar(percentage):
    st.markdown(f"""
    <style>
    .progress-container {{
        width:100%;
        height:34px;
        background:#262730;
        border-radius:40px;
        overflow:hidden;
        position:relative;
        margin-top:25px;
        margin-bottom:35px;
    }}
    .progress-fill {{
        height:100%;
        width:{percentage}%;
        border-radius:40px;
        background:linear-gradient(90deg,#ff4b91,#ff6bb3,#ff9ac6);
        background-size:300% 300%;
        animation:fillAnimation 2s ease,gradientMove 4s ease infinite;
        box-shadow:0 0 8px #ff4b91,0 0 18px #ff4b91,0 0 28px #ff4b91;
        position:relative;
        overflow:hidden;
    }}
    .progress-fill::after {{
        content:"";
        position:absolute;
        top:0;
        left:-30%;
        width:30%;
        height:100%;
        background:rgba(255,255,255,0.25);
        transform:skewX(-25deg);
        animation:shine 2s infinite;
    }}
    @keyframes fillAnimation {{
        from {{
            width:0%;
        }}
        to {{
            width:{percentage}%;
        }}
    }}
    @keyframes shine {{
        0% {{
            left:-30%;
        }}
        100% {{
            left:130%;
        }}
    }}
    @keyframes gradientMove {{
        0% {{
            background-position:0% 50%;
        }}
        50% {{
            background-position:100% 50%;
        }}
        100% {{
            background-position:0% 50%;
        }}
    }}
    </style>
    <div class="progress-container">
        <div class="progress-fill"></div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("""
<style>
.main{
    background-color :  #0E1117; 
}
.question_card{
    background-color:#1E1E1E;
    padding : 30px;
    border-radius : 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
    margin-top : 20px;
    margin-bottom : 20px;
}
.question-title {
    font-size: 34px;
    font-weight: 700;
    line-height: st1.4;
    margin-bottom: 25px;
    color: white;
}
.small-text{
    color: #BBBBBB;
    font-size: 14px;
}                       
</style>
""",unsafe_allow_html=True)
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if st.session_state.step>=len(questions):
    st.balloons()
    user_input = st.session_state.answers
    signals = process_signals(user_input,questions)
    actual_score,contributions = calculate_score_with_breakdown(questions,user_input)
    max_score = max_possible_score(questions)
    min_score = min_possible_score(questions)
    percentage = calculate_percentage(max_score,min_score,actual_score)
    overview_title = title(percentage)
    communication_percentage,emotional_bond_percentage,attraction_percentage,social_interest_percentage,effort_balance_percentage = calculate_compatibility_breakdown_system_percentage(contributions)
    st.divider()
    st.markdown(f"# {overview_title}")
    ml_percentage = predict_ml_compatibility(user_input)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📐 Rule-Based Score")
        placeholder_percentage = st.empty()
        for i in np.linspace(0, percentage, 50):
            placeholder_percentage.markdown(f"# 💖 {i:.1f}%")
            time.sleep(0.01)
        main_percentage_progress_bar(percentage)
    with col2:
        st.markdown("### 🤖 ML Model Score")
        placeholder_ml = st.empty()
        for i in np.linspace(0, ml_percentage, 50):
            placeholder_ml.markdown(f"# 🧠 {i:.1f}%")
            time.sleep(0.01)
        main_percentage_progress_bar(ml_percentage)
    score_diff = abs(percentage - ml_percentage)
    if score_diff <= 10:
        st.info("✅ Both scores agree — this is a reliable result")
    elif percentage > ml_percentage:
        st.warning("⚠️ Rule-based score is higher — you might be slightly optimistic")
    else:
        st.warning("⚠️ ML score is higher — signals are stronger than they seem")
    suggestion = return_suggestion(percentage) 
    placeholder_suggestion = st.empty()
    for i in range(0,(len(suggestion)+1)):
        placeholder_suggestion.markdown(f"### {suggestion[0:i]}")
        time.sleep(0.02)
    st.divider()
    best_trait,worst_trait,best_trait_score,worst_trait_score = best_worst_trait(communication_percentage,emotional_bond_percentage,attraction_percentage,social_interest_percentage,effort_balance_percentage)
    positive_signals,negative_signals,neutral_signals = signal_breakdown(user_input,questions)
    st.markdown("## 🤖 AI Relationship Analysis")
    if "ai_analysis" not in st.session_state:
        with st.spinner("Analyzing your signals..."):
            try:
                st.session_state.ai_analysis = generate_ai_feedback(percentage,ml_percentage,communication_percentage,emotional_bond_percentage,
                    attraction_percentage,social_interest_percentage,effort_balance_percentage,positive_signals,negative_signals,neutral_signals,
                    best_trait,worst_trait)
            except Exception as e:
                st.session_state.ai_analysis = f"Analysis unavailable: {str(e)}"
    ai_analysis = st.session_state.ai_analysis
    st.markdown(f"""
    <div style="
        background-color:#1E1E1E;
        padding:25px;
        border-radius:15px;
        border-left:4px solid #ff4b91;
        font-size:16px;
        line-height:1.7;
        color:white;
    ">
    {ai_analysis}
    </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown("## 💬 Chat With CupidAI")
    st.markdown("*Ask me anything about your results...*")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                margin-bottom: 10px;
            ">
                <div style="
                    background: linear-gradient(90deg, #ff4b91, #c026d3);
                    color: white;
                    padding: 12px 18px;
                    border-radius: 18px 18px 4px 18px;
                    max-width: 70%;
                    font-size: 14px;
                    line-height: 1.5;
                ">
                {msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                display: flex;
                justify-content: flex-start;
                margin-bottom: 10px;
            ">
                <div style="
                    background: #1E1E2E;
                    border: 1px solid rgba(255,75,145,0.3);
                    color: white;
                    padding: 12px 18px;
                    border-radius: 18px 18px 18px 4px;
                     max-width: 70%;
                     font-size: 14px;
                    line-height: 1.5;
                ">
                    <span style="color:#ff4b91; font-weight:700; 
                    font-size:12px;">CupidAI</span><br>
                    {msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
    suggestions = ["Should I text first?","What's my biggest green flag?","Am I overthinking this?","What should I do next?"]
    cols = st.columns(4)
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, key=f"suggestion_{i}",use_container_width=True):
                st.session_state.chat_history.append({"role": "user","content": suggestion})
                with st.spinner("CupidAI is thinking..."):
                    reply = chat_with_cupidai(suggestion,st.session_state.chat_history[:-1],percentage,ml_percentage,communication_percentage,
                        emotional_bond_percentage,attraction_percentage,social_interest_percentage,effort_balance_percentage,
                        best_trait,worst_trait)
                st.session_state.chat_history.append({"role": "assistant","content": reply})
                st.rerun()
    user_message = st.chat_input("Ask CupidAI anything...")
    if user_message:
        st.session_state.chat_history.append({"role": "user","content": user_message})
        with st.spinner("CupidAI is thinking..."):
            try:
                reply = chat_with_cupidai(user_message,st.session_state.chat_history[:-1],percentage,ml_percentage,
                    communication_percentage,emotional_bond_percentage,attraction_percentage,social_interest_percentage,effort_balance_percentage,best_trait,worst_trait)
                st.session_state.chat_history.append({"role": "assistant","content": reply})
            except Exception as e:
                st.error(f"Chat error: {str(e)}")
        st.rerun()
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    st.divider()
    st.markdown("## 💘 Compatibility Radar")
    radar = show_radar_chart(communication_percentage,emotional_bond_percentage,attraction_percentage,social_interest_percentage,effort_balance_percentage)
    st.pyplot(radar)
    st.write(f"🏆 Best Trait: {best_trait} ({best_trait_score:.1f}%)")
    st.write(f"⚠️ Weakest Trait: {worst_trait} ({worst_trait_score:.1f}%)")
    st.divider()
    st.markdown("## 💘 Signal Distribution")
    st.write(f"💚Positive Signals: {positive_signals}")
    st.write(f"💔Negative Signals: {negative_signals}")
    st.write(f"🤍Neutral Signals: {neutral_signals}")
    fig = show_pie_chart(positive_signals,negative_signals,neutral_signals)
    st.pyplot(fig)
    st.divider()
    st.markdown("## 📊 Compatibility Breakdown")
    st.write(f"💬 Communication — {communication_percentage:.1f}%")
    st.progress(communication_percentage/100)
    st.write(f"❤️ Emotional Bond — {emotional_bond_percentage:.1f}%")
    st.progress(emotional_bond_percentage/100)
    st.write(f"👀 Attraction — {attraction_percentage:.1f}%")
    st.progress(attraction_percentage/100)
    st.write(f"📱 Social Interest — {social_interest_percentage:.1f}%")
    st.progress(social_interest_percentage/100)
    st.write(f"🤝 Effort Balance — {effort_balance_percentage:.1f}%")
    st.progress(effort_balance_percentage/100)
    st.divider()
    count_positive = 0
    for key,_,dtype,rule,_,direction,_,positive_label,_ in questions:
        if count_positive==3:
            break
        if is_positive(user_input,key,dtype,rule,direction):
            if count_positive == 0:
                st.write("### 💚 Strong positives:")
            st.write(f"✔ {positive_label}")
            count_positive += 1
    count_negative = 0
    for key,_,dtype,rule,_,direction,_,_,negative_label in questions:
            if count_negative == 3:
                break
            if is_negative(user_input,key,dtype,rule,direction):
                if count_negative == 0:
                    st.write("### 💔 Weak areas:")
                st.write(f"✖ {negative_label}")
                count_negative += 1
    st.divider()
    left,center,right = st.columns([1,1,1])
    with center:
        if st.button("🔄 RESTART",use_container_width=True): 
            st.session_state.step = 0
            st.session_state.answers = {}
            st.session_state.chat_history = []
            st.session_state.ai_analysis = None
            if "ai_analysis" in st.session_state:
                del st.session_state["ai_analysis"]
            st.rerun()
    st.stop()
q = questions[st.session_state.step]
progress = (st.session_state.step)/len(questions)
key,text,dtype,rule,weight,direction,labels,positive_label,negative_label = q
widget_key = f"{key}_{st.session_state.step}"
q = questions[st.session_state.step]
key, text, dtype, rule, weight, direction, labels, positive_label, negative_label = q

widget_key = f"{key}_{st.session_state.step}"
QUESTION_TIPS = {
    "insta_friends"      : "Being Instagram friends is a modern trust signal — people curate their followers carefully. Getting accepted means they're comfortable with you seeing their daily life.",
    "fast_replies"       : "Response time is one of the most honest signals — people always find time for who they prioritize. Speed of reply often reflects how excited they are to talk to you.",
    "personal_questions" : "Asking personal questions means someone is genuinely curious about your inner world, not just making small talk. Curiosity is one of the earliest signs of romantic interest.",
    "likes_stories"      : "Story likes are low-effort but intentional — they had to consciously tap your story and then tap the heart. It's a subtle but consistent way of saying 'I see you'.",
    "close_friends"      : "The Close Friends list is one of Instagram's most intimate features — people add maybe 5-10 people max. Being on it means they want to share things with you they hide from everyone else.",
    "chat_daily"         : "Daily conversation builds emotional intimacy faster than anything else. Consistency in communication is what separates someone who likes you from someone who is just bored.",
    "compliments"        : "Compliments reveal what someone notices about you — and people only notice what they're paying attention to. Specific compliments are especially meaningful because they show real observation.",
    "shares_personal"    : "Sharing personal things requires vulnerability and trust. When someone opens up to you they're subconsciously testing if you're a safe person — it means they want you closer.",
    "eye_contact"        : "Prolonged eye contact triggers the same neural pathways as falling in love. Studies show that sustained eye contact between two people increases feelings of attraction significantly.",
    "physical_closeness" : "Physical proximity is subconsciously controlled — people naturally move closer to those they're attracted to and create distance from those they're not. It's one of the hardest signals to fake.",
    "emoji_freq"         : "Emojis in texting serve the same role as tone of voice in conversation. Someone who texts you with expressive emojis is putting effort into making the conversation feel warm and playful.",
    "message_length"     : "Message length directly reflects investment. A long thoughtful reply means they didn't want the conversation to end — short replies usually mean they're not that engaged.",
    "initiates"          : "Initiation is the clearest effort signal there is — it means they thought of you and acted on it. Someone who never initiates is comfortable receiving your attention but not invested enough to seek it.",
    "accepts_plan"       : "Accepting plans requires giving up time — the most limited resource anyone has. Someone who consistently makes time to meet you is showing you where you rank in their priorities.",
    "seen_ignore"        : "Being left on seen is a conscious choice — notifications make it impossible to miss a message. It signals that responding to you is not a priority in that moment, which is data worth paying attention to.",
    "dry_replies"        : "Dry replies are a form of soft rejection — they keep the conversation alive just enough to avoid conflict but don't actually invest in it. Enthusiasm in texting is very hard to fake consistently.",
}
category_map = {
    "fast_replies"       : "💬 Communication",
    "message_length"     : "💬 Communication",
    "emoji_freq"         : "💬 Communication",
    "chat_daily"         : "💬 Communication",
    "personal_questions" : "❤️ Emotional Bond",
    "shares_personal"    : "❤️ Emotional Bond",
    "eye_contact"        : "👀 Attraction",
    "physical_closeness" : "👀 Attraction",
    "compliments"        : "👀 Attraction",
    "likes_stories"      : "📱 Social Interest",
    "close_friends"      : "📱 Social Interest",
    "insta_friends"      : "📱 Social Interest",
    "initiates"          : "🤝 Effort Balance",
    "accepts_plan"       : "🤝 Effort Balance",
    "seen_ignore"        : "🤝 Effort Balance",
    "dry_replies"        : "🤝 Effort Balance",
}
category = category_map.get(key, "💘 Compatibility")
st.write(f"{int(progress*100)}% completed")
st.progress(progress)
ai_tip = QUESTION_TIPS.get(key, "Pay close attention to patterns over time — consistency across multiple signals is what reveals true interest.")
svg    = CATEGORY_SVG.get(category, CATEGORY_SVG["💘 Compatibility"])
img_tag = svg_to_img(svg)
st.markdown(f"""
<div class="left-panel">
    {img_tag}
</div>
""", unsafe_allow_html=True)
st.markdown(f"""
<div class="right-panel">
    <div class="right-panel-label">🔍 Signal Decoder</div>
    <div class="right-panel-text">{ai_tip}</div>
    <div class="right-panel-category">{category}</div>
</div>
""", unsafe_allow_html=True)
left,center,right = st.columns([1,2,1])
with center:
    st.markdown(f"""<div class = "question-card">
                       <div class = "small-text"> 
                           Question {st.session_state.step+1}/{len(questions)}
                        </div> 
                           <div class = "question-title">
                               {text}
                           </div> 
                            """,unsafe_allow_html=True)
    voice_key = f"voice_{key}"
    voice_mapped_value = st.session_state.get(voice_key, None)
    if dtype == int and rule == [0,1]:
        previous_value = voice_mapped_value if voice_mapped_value is not None else st.session_state.answers.get(key,0)
        index = 0 if previous_value == 1 else 1
        choice = st.radio("",["Yes","No"],index=index,key=widget_key)
        value = 1 if choice == "Yes" else 0
    elif dtype == str:
        options = ["Never","Rarely","Often"]
        previous_value = voice_mapped_value if voice_mapped_value is not None else st.session_state.answers.get(key,"rarely")
        if isinstance(previous_value, str):
            index = options.index(previous_value.capitalize())
        else:
            index = 1
        choice = st.selectbox("",options,index=index,key=widget_key)
        value = choice.lower()
    else:
        previous_value = voice_mapped_value if voice_mapped_value is not None else st.session_state.answers.get(key,2)
        if labels:
            value = st.radio("",list(labels.keys()),index=list(labels.keys()).index(previous_value),format_func=lambda x:f"{x} → {labels[x]}",key=widget_key)
        else:
            value = st.slider("",0,5,previous_value,key=widget_key)
    st.markdown("""</div>""",unsafe_allow_html=True)
    audio = st.audio_input("🎤 Speak your answer instead", key=f"audio_{st.session_state.step}")
    if audio is not None:
        audio_bytes = audio.read()
        with st.spinner("🎧 Transcribing..."):
            from voice_input import transcribe_audio, map_transcription_to_answer
            transcription = transcribe_audio(audio_bytes)
        if transcription.startswith("ERROR"):
            st.error(f"Transcription failed: {transcription}")
        else:
            st.markdown("🎤 **I heard:**")
            transcription_key = f"transcription_{st.session_state.step}"
            last_raw_key = f"_last_raw_transcription_{st.session_state.step}"
            if st.session_state.get(last_raw_key) != transcription:
                st.session_state[transcription_key] = transcription
                st.session_state[last_raw_key] = transcription
            edited_transcription = st.text_area("",value=transcription,height=80,key=transcription_key,help="You can edit this if transcription was wrong")
            mapped = map_transcription_to_answer(edited_transcription, dtype, rule, labels)
            if mapped is not None:
                if dtype == int and rule == [0, 1]:
                    display_label = "Yes" if mapped == 1 else "No"
                elif dtype == str:
                    display_label = mapped.capitalize()
                elif labels and mapped in labels:
                    display_label = f"{mapped} → {labels[mapped]}"
                else:
                    display_label = str(mapped)
                st.success(f"✅ Auto selected: **{display_label}**")
                st.caption("✏️ Not what you meant? Edit the text above — the selected answer updates automatically.")
                st.session_state[voice_key] = mapped
                if st.button("✅ Confirm & Next",use_container_width=True,key=f"confirm_{key}"):
                    st.session_state.answers[key] = mapped
                    if voice_key in st.session_state:
                        del st.session_state[voice_key]
                    st.session_state.step += 1
                    st.rerun()
            else:
                st.warning("⚠️ Couldn't map — please select manually above")        
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️Back") and st.session_state.step > 0:
            st.session_state.step -= 1
            st.rerun()
    with col2:
        if st.button("Next➡️"):
            st.session_state.answers[key] = value
            if voice_key in st.session_state:
                del st.session_state[voice_key]
            st.session_state.step += 1
            st.rerun()