feature_map = {
    "eye_contact" : "attr",
    "compliments" : "attr",
    "personal_questions" : "prob",
    "shares_personal": "sinc",
    "accepts_plan" : "fun",
    "initiates"  : "prob",
    "chat_daily" : "int_corr", 
    "close_friends"  : "shar", 
    "physical_closeness" : "attr",
    "emoji_freq" : "fun",
    "message_length" : "prob",
    "fast_replies" : "prob",
    "insta_friends" : "shar",
    "likes_stories" : "shar"
}
negative_key_inversions = {
    "seen_ignore" : {
        "never" : 1.0,
        "rarely" : 0.5,
        "often" : 0.0
    },
    "dry_replies" : {
        "never" : 1.0,
        "rarely" : 0.5,
        "often" : 0.0
    }
}
def normalize_to_dataset_scale(value,original_min,original_max,dataset_min = 1  ,dataset_max = 10):
    return dataset_min + ((value-original_min)/(original_max-original_min)) * (dataset_max - dataset_min)
def convert_quiz_answers(key,value):
    if key in negative_key_inversions:
        inverted = negative_key_inversions[key][value]
        return inverted * 9 + 1
    if key == "chat_daily":
        return 0.8 if value == 1 else -0.5
    if isinstance(value,int) and value in [0,1]:
        return normalize_to_dataset_scale(value,0,1)
    if isinstance(value,int) and 0<= value <= 5 : 
        return normalize_to_dataset_scale(value,0,5)
    str_map = {
        "never" : 0.0,
        "rarely" : 0.5,
        "often" : 1.0
    }
    return str_map[value] * 9 + 1