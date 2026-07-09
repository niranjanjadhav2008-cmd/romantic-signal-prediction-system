import matplotlib.pyplot as plt
import numpy as np
def process_signals(form_values,questions):
    user_signals = {}
    for key,_,dtype,rule,weight,_,_,_,_ in questions:
        value = form_values[key]
        user_signals[key] = (value,weight,dtype,rule)
    return user_signals
def calculate_score_with_breakdown(questions,user_input):
    score = 0  
    contributions = {}
    for key,text,dtype,rule,weight,direction,_,positive_label,negative_label in questions:
        value = user_input[key]
        if dtype == int:
            raw_score = value * direction
            signal_score = raw_score * weight
        else:
            value = value.lower().strip()
            raw_score = rule[value] * direction
            signal_score = raw_score*weight
        score += signal_score
        contributions[key] = (text,signal_score,raw_score,dtype,rule,positive_label,negative_label)
    return score,contributions
def max_possible_score(questions):
    max_score = 0

    for key, text, dtype, rule, weight, direction,_,_,_ in questions:
        if dtype == int:
            values = [v * direction for v in rule]
            max_score += max(values) * weight
        else:
            best_key = max(rule, key=lambda k: rule[k] * direction)
            max_score += rule[best_key] * weight * direction
    return max_score
def min_possible_score(questions):
    min_score = 0
    for key, text, dtype, rule, weight, direction,_,_,_ in questions:
        if dtype == int:
            worst_value = min(rule)
            min_score += worst_value * weight * direction
        else:
           worst_value = min(rule,key = lambda k : rule[k]*direction)
           min_score += rule[worst_value] * weight * direction
    return min_score
def normalize(maximum,minimum,actual):
    if maximum!=minimum:
        percentage = ((actual-minimum)/(maximum-minimum))*100
    else:
        percentage = 0
    return percentage
def calculate_percentage(max_score,min_score,actual_score):
    percentage = normalize(max_score,min_score,actual_score)
    return percentage
def title(percentage):
    if percentage >= 90:
        title = "💍 Romantic Energy"
    elif percentage >= 75:
        title = "❤️ High Attraction"
    elif percentage >= 60:
        title = "😏 Flirting Zone"
    elif percentage >= 40:
        title = "🤔 Mixed Signals"
    else:
        title = "🧊 Stranger Zone"
    return title
def is_positive(user_input,key,dtype,rule,direction):
    if direction == 1:
        if dtype == int:
            if rule == [0,1]:
                if user_input[key] == 1:
                    return True
            else:
                if user_input[key]>2:
                    return True
        else:
            value_score = rule[user_input[key]]
            if value_score>0.5:
                return True
    else:
        if dtype == int:
            if rule == [0,1]:
                if user_input[key] == 0:
                    return True
            else:
                if user_input[key]<2:
                    return True
        else:
            value_score = rule[user_input[key]]
            if value_score<0:
                return True
    return False
def is_negative(user_input,key,dtype,rule,direction):
    if direction == 1:
        if dtype == int:
            if rule == [0,1]:
                if user_input[key] == 0:
                    return True
            else:
                if user_input[key]<2:
                    return True
        else:
            value_score = rule[user_input[key]]
            if value_score<0:
                return True
    else:
        if dtype == int:
            if rule == [0,1]:
                if user_input[key] == 1:
                    return True
            else:
                if user_input[key]>2:
                    return True
        else:
            value_score = rule[user_input[key]]
            if value_score>=0.5:
                return True
    return False
def signal_breakdown(user_input,questions):
    positive = 0
    negative = 0
    neutral = 0
    for key,_,dtype,rule,_,direction,_,_,_ in questions:
        if direction == 1:
            if dtype == int:
                if rule == [0,1]:
                    if user_input[key] == 0:
                        negative+=1
                    else:
                        positive+=1
                else:
                    if user_input[key]==2:
                        neutral+=1
                    elif user_input[key]<2:
                        negative+=1
                    else:
                        positive+=1
            else:
                value_score = rule[user_input[key]]
                if value_score == 0.5:
                    neutral+=1
                elif value_score<0:
                    negative+=1
                else:
                    positive+=1
        else:
            if dtype == int:
                if rule == [0,1]:
                    if user_input[key] == 0:
                        positive+=1
                    else:
                        negative+=1
                else:
                    if user_input[key]==2:
                        neutral+=1
                    elif user_input[key]<2:
                        positive+=1
                    else:
                        negative+=1
            else:
                value_score = rule[user_input[key]]
                if value_score == 0.25:
                    neutral+=1
                elif value_score<0:
                    positive+=1
                else:
                    negative+=1
    return positive,negative,neutral
def return_suggestion(percentage):
    if percentage>=85:
        suggestion = "Broo..Stop lying broo..You are already in a relationship.. 👀😏💀"
    elif percentage >= 80:
        suggestion = "PROPOSE!!💍❤️"
    elif percentage >=60:
        suggestion = "Ask her out on a coffee date ☕😏"
    elif percentage>=40:
        suggestion = "There's something… don't mess it up 😏"
    else:
        suggestion = "Focus on yourself king 👑 — build your value first, everything else follows 💪"
    return suggestion
def show_signals_frequency(positive_signals,negative_signals,neutral_signals):
    return positive_signals,negative_signals,neutral_signals
def show_pie_chart(positive_signals, negative_signals, neutral_signals):
    signals   = ["Positive", "Negative", "Neutral"]
    frequency = np.array([positive_signals, negative_signals, neutral_signals])
    colors = ["#ff4b91", "#2D2D2D", "#7C3AED"]

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    wedges, texts, autotexts = ax.pie(
        frequency,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        pctdistance=0.75,
        wedgeprops={
            "edgecolor"  : "white",
            "linewidth"  : 3,
            "width"      : 0.6,      # ← donut style
        },
        shadow=False,
    )

    # ── Percentage text styling ──
    for autotext in autotexts:
        autotext.set_fontsize(13)
        autotext.set_fontweight("bold")
        autotext.set_color("white")

    # ── Center text ──
    total = sum(frequency)
    ax.text(
        0, 0,
        f"{positive_signals}\nPositives",
        ha="center", va="center",
        fontsize=16, fontweight="bold",
        color="#ff4b91"
    )

    # ── Custom legend ──
    legend_labels = [
        f"Positive  —  {positive_signals}",
        f"Negative  —  {negative_signals}",
        f"Neutral    —  {neutral_signals}",
    ]
    ax.legend(
        wedges,
        legend_labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=3,
        fontsize=10,
        frameon=False,
        labelcolor="#111111",
    )

    ax.set_title(
        "Signal Distribution",
        fontsize=18,
        fontweight="bold",
        pad=20,
        color="#111111"
    )

    plt.tight_layout()
    return fig
def max_compatibility_breakdown_system_scores(communication,emotional_bond,attraction,social_interest,effort_balance,questions):
    max_communication_score = 0
    max_emotional_bond_score = 0
    max_attraction_score = 0
    max_social_interest_score = 0
    max_effort_balance_score = 0
    for key,_,dtype,rule,weight,direction,_,_,_ in questions:
            max_score = 0
            if dtype == int:
                value = [v * direction for v in rule]
                max_score = max(value) * weight
            else:
                best_key = max(rule,key = lambda x : rule[x] * direction)
                max_score = rule[best_key] * weight * direction
            if key in communication:
                max_communication_score += max_score
            elif key in emotional_bond:
                max_emotional_bond_score += max_score
            elif key in attraction:
                max_attraction_score += max_score
            elif key in social_interest:
                max_social_interest_score += max_score
            else:
                max_effort_balance_score += max_score
    return max_communication_score,max_emotional_bond_score,max_attraction_score,max_social_interest_score,max_effort_balance_score
def min_compatibility_breakdown_system_score(communication,emotional_bond,attraction,social_interest,effort_balance,questions):
    min_communication_score = 0
    min_emotional_bond_score = 0
    min_attraction_score = 0
    min_social_interest_score = 0
    min_effort_balance_score = 0
    for key,_,dtype,rule,weight,direction,_,_,_ in questions:
            min_score = 0
            if dtype == int:
                value = [v * direction for v in rule]
                min_score = min(value) * weight
            else:
                worst_key = min(rule,key = lambda x : rule[x] * direction)
                min_score = rule[worst_key] * weight * direction
            if key in communication:
                min_communication_score += min_score
            elif key in emotional_bond:
                min_emotional_bond_score += min_score
            elif key in attraction:
                min_attraction_score += min_score
            elif key in social_interest:
                min_social_interest_score += min_score
            else:
                min_effort_balance_score += min_score
    return min_communication_score,min_emotional_bond_score,min_attraction_score,min_social_interest_score,min_effort_balance_score
def actual_compatibility_breakdown_system_scores(communication,emotional_bond,attraction,social_interest,effort_balance,contributions):
    actual_communication_score = 0
    actual_emotional_bond_score = 0
    actual_attraction_score = 0
    actual_social_interest_score = 0
    actual_effort_balance_score = 0
    for key,(text,signal_score,raw_score,dtype,rule,positive_label,negative_label) in contributions.items():
        if key in communication:
            actual_communication_score += signal_score
        elif key in emotional_bond:
            actual_emotional_bond_score += signal_score
        elif key in attraction:
            actual_attraction_score += signal_score
        elif key in social_interest:
            actual_social_interest_score += signal_score
        else:
            actual_effort_balance_score += signal_score
    return actual_communication_score,actual_emotional_bond_score,actual_attraction_score,actual_social_interest_score,actual_effort_balance_score 
def calculate_compatibility_breakdown_system_percentage(contributions):
    min_communication_score,min_emotional_bond_score,min_attraction_score,min_social_interest_score,min_effort_balance_score = min_compatibility_breakdown_system_score(communication,emotional_bond,attraction,social_interest,effort_balance,questions)
    max_communication_score,max_emotional_bond_score,max_attraction_score,max_social_interest_score,max_effort_balance_score = max_compatibility_breakdown_system_scores(communication,emotional_bond,attraction,social_interest,effort_balance,questions)
    actual_communication_score,actual_emotional_bond_score,actual_attraction_score,actual_social_interest_score,actual_effort_balance_score = actual_compatibility_breakdown_system_scores(communication,emotional_bond,attraction,social_interest,effort_balance,contributions)
    communication_percentage = normalize(max_communication_score,min_communication_score,actual_communication_score)
    emotional_bond_percentage = normalize(max_emotional_bond_score,min_emotional_bond_score,actual_emotional_bond_score)
    attraction_percentage = normalize(max_attraction_score,min_attraction_score,actual_attraction_score)
    social_interest_percentage = normalize(max_social_interest_score,min_social_interest_score,actual_social_interest_score)
    effort_balance_percentage = normalize(max_effort_balance_score,min_effort_balance_score,actual_effort_balance_score)
    return communication_percentage,emotional_bond_percentage,attraction_percentage,social_interest_percentage,effort_balance_percentage
def show_radar_chart(communication_percentage, emotional_bond_percentage,
                     attraction_percentage, social_interest_percentage,
                     effort_balance_percentage):
    categories = ["Communication", "Emotional Bond", "Attraction",
                  "Social Interest", "Effort Balance"]
    values = [communication_percentage, emotional_bond_percentage,
              attraction_percentage, social_interest_percentage,
              effort_balance_percentage]

    num_vars = len(categories)
    angles   = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    values  += values[:1]
    angles  += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # ✅ White background
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # ✅ Pink line and fill
    ax.plot(angles, values, linewidth=3, color="#ff4b91",
            marker="o", markersize=8)
    ax.fill(angles, values, alpha=0.25, color="#ff4b91")

    # ✅ Black labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12,
                       fontweight="bold", color="#111111")
    ax.tick_params(axis="x", pad=15, colors="#111111")

    # ✅ Dark tick marks on radial axis
    ax.yaxis.set_tick_params(labelcolor="#444444")
    ax.set_ylim(0, 100)

    # ✅ Subtle dark grid
    ax.grid(color="#CCCCCC", alpha=0.6)

    # ✅ Spine color
    ax.spines["polar"].set_color("#CCCCCC")
    ax.spines["polar"].set_alpha(0.8)

    ax.set_title(" ", fontsize=22, fontweight="bold", pad=35)

    return fig
def best_worst_trait(communication_percentage,emotional_bond_percentage,attraction_percentage,social_interest_percentage,effort_balance_percentage):
    traits = {}
    percentages = [communication_percentage,emotional_bond_percentage,attraction_percentage,social_interest_percentage,effort_balance_percentage]
    compatibility_factors = ["💬 Communication","❤️ Emotional Bond","👀 Attraction","📱 Social Interest","🤝 Effort Balance"]
    for i in range(0,5):
        traits[compatibility_factors[i]] = percentages[i] 
    best_trait = max(traits,key = traits.get)
    worst_trait = min(traits,key = traits.get)
    best_trait_score = traits[best_trait]
    worst_trait_score = traits[worst_trait]
    return best_trait,worst_trait,best_trait_score,worst_trait_score
questions = [("insta_friends","Are you friends on Instagram?",int,[0,1],1,1,None,"Instagram Connection","No Social Connection"),
             ("fast_replies","Does he/she replies fast?(never/rarely/often) ",str,{"never": -0.5,"rarely": 0.5,"often": 1},2,1,None,"Fast Replies","Late Replies"),
             ("personal_questions","Does he/she asks about yourself?(never/rarely/often) ",str,{"never": -0.5,"rarely": 0.5,"often": 1},2,1,None,"Curious About You","Lack Of Interest"),
             ("likes_stories","Does he/she like your insta stories?(never/rarely/often) ",str,{"never": -0.5,"rarely": 0.5,"often": 1},2,1,None,"Engages With Stories","Ignores Your Stories"),
             ("close_friends","Are you added on his/her close friends? ",int,[0,1],3,1,None,"Close Friends Access","Not in Inner Circle"),
             ("chat_daily","Do you both chat daily? ",int,[0,1],2,1,None,"Daily Conversation","Rare Chat Conversation"),
             ("compliments","Does he/she complement you?(never/rarely/often) ",str,{"never": -0.5,"rarely": 0.5,"often": 1},3,1,None,"Gives Compliments","No Appreciation"),
             ("shares_personal","Does he/she shares their personal stuff with you?(never/rarely/often) ",str,{"never": -0.5,"rarely": 0.5,"often": 1},3,1,None,"Emotional Openness","Emotionally Closed"),
             ("eye_contact","How's your eye contact?(never/rarely/often) ",str,{"never": -0.5,"rarely": 0.5,"often": 1},1,1,None,"Strong Eye Contact","Weak Eye Contact"),
             ("physical_closeness","How's your physical closeness?(0-5): ",  int,range(0,6),2,1,{0: "Never touched",1: "Handshake",2: "One-on-one time spent",3: "Hug",4: "Kiss",5: "You know what 😏"},"Physical Comfort","Physical Distance"),
             ("emoji_freq","How he/she uses emoji?(never/rarely/often) ",str,{"never": -0.5,"rarely": 0.5,"often": 1},1,1,None,"Playful Texting","Dry Texting Energy"),
             ("message_length","What is message length?(0-5): ",int,range(0,6),1,1,None,"Detailed Conversations","Short Replies"),
             ("initiates","How often does he/she initiate chat?(never/rarely/often) ",str,{"never": -0.5,"rarely": 0.5,"often": 1},2,1,None,"Initiates Conversation","Low Initiation"),
             ("accepts_plan","How often does he/she accept plan?(never/rarely/often) ",str,{"never": -0.5,"rarely": 0.5,"often": 1},3,1,None,"Excited To Meet","Avoid plans"),
             ("seen_ignore","How often does he/she ignore your text?(never/rarely/often) ",str,{"never": -1,"rarely": 0.25,"often": 0.5},2,-1,None,"Consistent Replies","Seen-Zoning"),
             ("dry_replies","How often does he/she give dry reply?(never/rarely/often) ",str,{"never": -1,"rarely": 0.25,"often": 0.5},2,-1,None,"Engaging Replies","Dry Replies")]
communication = ["fast_replies","message_length","emoji_freq","chat_daily"]
emotional_bond = ["personal_questions","shares_personal"]
attraction = ["eye_contact","physical_closeness"]
social_interest = ["likes_stories","close_friends","insta_friends"]
effort_balance = ["initiates","accepts_plan","seen_ignore","dry_replies"]
