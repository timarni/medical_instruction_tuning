import random


# Multiturn Class that represents one interaction mode
# Methodes to get system prompt for Meditron and User, both simulated by gpt-4o

class MultiturnStyle:
    def __init__(self, id, country, setting = "high", nbr_of_turns = 1, mode = "normal",
                 cb_style = "flat text", cb_length = "short", cb_scientific = "standard",
                 u_length = "short",  u_scientific = "standard", u_specialty = "physician", u_bad_grammar = False):
         
        # Initialize situational attributes
        self.id = id # based on prompt origin and prompt number
        self.country = country # country the user is working in
        self.setting = setting  # Can be 'high', 'low', or 'war' -> not used so far
        self.number_of_turns = nbr_of_turns # Number of turns (1 = 1 question + 1 answer)
        self.mode = mode # Three different modes: "chat", "normal", "emergency"

        # Initizalize attributes that determine system prompt of Meditron
        self.chatbot_length = cb_length # Length of chatbots answer -> possibilities: short, long, exactly_2_sentences, exactly_4_sentences
        self.chatbot_style = cb_style # Style of chatbots answer -> possibilities: flat text, bullets, step by step
        self.chatbot_scientific = cb_scientific # If chatbot uses a lot of scientific term -> possibilities: popularization, standard, scientific

        # Initialize attributes that determine system prompt of user
        self.user_length = u_length # Length of user questions -> possibilities: short, long, exactly_1_sentence, exactly_3_sentences
        self.user_scientific = u_scientific # User uses a lot of very scientific terms -> not used so far
        self.user_specialty = u_specialty
        self.bad_grammar = u_bad_grammar # user has bad grammar / does a lot of spelling mistakes -> not used so far

        # Fixed attributes
        self.base_system_prompt_chatbot = f'''You are a medical AI chatbot designed to assist health care workers working in {self.country} by answering their questions. \nThe style of your answers must follow these rules: \n'''
        self.base_system_prompt_user = f'''You are a {self.user_specialty} working in {self.country} using a medical AI chatbot to help you taking care of your patients. \nThe initial question that you ask the medical AI chatbot has already been provided. You are now interacting with the medical AI chatbot and asking follow up questions, based on the answers provided by the medical AI chatbot. \nThe style of the follow up question you ask must follow these rules: \n'''

        self.number_of_turns_done = 0

    # methods

    # adds sytle specification to the system prompt of meditron
    def system_prompt_chatbot(self) -> str:
        prompt_parts = [self.base_system_prompt_chatbot]
        # Chatbot can be used in chat, normal or emergency mode
        match self.mode:
            case "chat":
                prompt_parts.append("The user is using you (the medical AI chatbot) in chat mode. Provide short and concise answers that make it possible for the user to chat with you. Ask the user follow up questions about their question if their question is not clear enough. \n")
            case "emergency":
                prompt_parts.append("The user is using you (the medical AI chatbot) during a medical emergency. Provide short, concises and well structured answers. Your answers have to be clear and very easy to understand quickly in a high presure and stres environment \n")
            case "normal":
                # Set epected length of chatbots answer
                match self.chatbot_length:
                    case "short":
                        prompt_parts.append("Provide short and concises answers. \n")
                    case "long":
                        prompt_parts.append("Provide long and detailed answers. \n")
                    case "exactly_2_sentences":
                        prompt_parts.append("All your answers should be exactly 2 sentences long. \n")
                    case "exactly_4_sentences":
                        prompt_parts.append("All your answers should be exactly 4 sentences long. \n")
                    case _:
                        raise ValueError(f"Invalid chatbot_length: '{self.chatbot_length}'")
                
                # Set expected style of chatbots answer
                match self.chatbot_style:
                    case "flat text":
                        prompt_parts.append("Provide your answers in flat text. \n")
                    case "bullets":
                        prompt_parts.append("Provide your answers using bullet points. \n")
                    case "step by step":
                        prompt_parts.append("Provide your answers by giving the physician step by step advice on how to solve the question they asked. \n")
                    case _:
                        raise ValueError(f"Invalid chatbot_style: '{self.chatbot_style}'")
            
        # Add if the style of the answers should be very scientific
        match self.chatbot_scientific:
            case "popularization":
                prompt_parts.append("Provide your answers using easy to understand terms and avoid using scientific terms that are difficult to understand. \n")
            case "standard":
                prompt_parts.append("") # Don't add anything if standard
            case "scientific":
                prompt_parts.append("Provide your answers using a lot of very specific scientific terms. \n")
            case _:
                raise ValueError(f"Invalid chatbot_scientific: '{self.chatbot_scientific}'")

        return ''.join(prompt_parts)
    
    def system_prompt_user(self) -> str:
        prompt_parts = [self.base_system_prompt_user]

        # User behavior is characterized by 3 different modes: chat, normal or emergency mode
        match self.mode:
            case "chat":
                prompt_parts.append(f"You (the {self.user_specialty} using the medical AI chatbot) are using the medical AI chatbot in chat mode. Ask short and concise questions that make it possible for the chatbot to chat with you. Ask follow up questions about the answers from the chatbot if the answers are not clear enough. \n")
            case "emergency":
                prompt_parts.append(f"You (the {self.user_specialty} using the medical AI chatbot) are using the medical AI chatbot during a medical emergency. Ask short and fastly written questions. \n")
            case "normal":
                # Set epected length of chatbots answer
                match self.user_length:
                    case "short":
                        prompt_parts.append("Ask short and concises questions. \n")
                    case "long":
                        prompt_parts.append("Ask long and detailed questions. \n")
                    case "exactly_1_sentence":
                        prompt_parts.append("All your questions should be exactly 1 sentence long. \n")
                    case "exactly_3_sentences":
                        prompt_parts.append("All your questions should be exactly 3 sentences long. \n")
                    case _:
                        raise ValueError(f"Invalid user_length: '{self.user_length}'")
                
            
        # Add if the style of the answers should be very scientific
        match self.user_scientific:
            case "popularization":
                prompt_parts.append("Ask follow up questions using easy to understand terms and avoid using scientific terms that are difficult. \n")
            case "standard":
                prompt_parts.append("") # Don't add anything if standard
            case "scientific":
                prompt_parts.append("Ask follow up questions using a lot of very specific scientific terms. \n")
            case _:
                raise ValueError(f"Invalid user_scientific: '{self.user_scientific}'")
                                        
        return ''.join(prompt_parts)
    


# Helper function get sample with specified disctirbution (weights)
def get_sample(choices, weights):
    if not choices or not weights:
        raise ValueError("choices and weights cannot be empty.")
    
    if len(choices) != len(weights):
        raise ValueError("choices and weights must have the same length.")
    
    return random.choices(choices, weights, k=1)[0]

# Function that creates the multiturn_style objects, following the distributions specified


# Tasks
# 0 - "Diagnosing Symptoms", 1 - "Predictive Analytics", 2 - "Drug Interaction Checks", 3 - "Treatment Recommendations"
# 4 - "Medication Management", 5 - "Patient Education", 6 - "Clinical Documentation", 7 - "Lab Test Interpretation"
# 8 - "Health Risk Assessment", 9 - "Nutrition and Diet Planning", 10 - "Language Translation", 11 - "Emergency Triage"
# 12 - "Health Policy Guidance", 20 - Specialty times domain prompts

def get_multiturn_style(id, sampled_country, profession = "no", specialty = "no", domain = "no"): # id is task_id - specialty_id

    # Usage mode: chat, normal, emergency (depening on id -> since )
    mode_choices = ["chat", "normal", "emergency"]
    match int(id.split("-")[0]):
        case n if n in [1, 4, 5, 8, 9, 10, 12]: # Non Emergency cases
            mode = get_sample(choices=mode_choices, weights=[0.4, 0.6, 0])
        case 6: # Non Emergency and non chat option
              mode = "normal"
        case n if n in [0, 2, 3, 7]: # All cases possible
            mode = get_sample(choices=mode_choices, weights=[0.4, 0.5, 0.1])
        case 11: # Very good for emergency
            mode = get_sample(choices=mode_choices, weights=[0.3, 0.3, 0.4])
        case 20: # specialties x domains prompts
            if specialty == "Emergency Medicine" or domain == "Emergency Medicine":
                mode = "emergency"
            else:
                mode = get_sample(choices=mode_choices, weights=[0.4, 0.6, 0])
        case _:
            raise ValueError(f"Invalid id: '{id}'")     
    
    # Number of turn
    nbr_of_turns_choices = [1, 2, 3]
    match mode:
        case s if s in ["chat", "emergency"]:
            nbr_of_turns = get_sample(choices=nbr_of_turns_choices, weights=[0.2, 0.3, 0.5])
        case "normal":
            nbr_of_turns = get_sample(choices=nbr_of_turns_choices, weights=[0.4, 0.3, 0.3])

    # Length of chatbots answer -> possibilities: short, long, exactly_2_sentences, exactly_4_sentences
    chatbot_length_choices = ["short", "long", "exactly_2_sentences", "exactly_4_sentences"]
    cb_length = get_sample(choices=chatbot_length_choices, weights=[0.3, 0.5, 0.1, 0.1])

    # Style of chatbot's answer -> possibilities: chat, flat text, bullets, step by step
    chatbot_style_choices = ["flat text", "bullets", "step by step"]
    cb_style = get_sample(choices=chatbot_style_choices, weights=[0.5, 0.25, 0.25])

    # If chatbot uses a lot of scientific term -> possibilities: popularization, standard, scientific
    chatbot_scientific_choices = ["popularization", "standard", "scientific"]
    cb_scientific = get_sample(choices=chatbot_scientific_choices, weights=[0.1, 0.8, 0.1])

    # Length of user questions -> possibilities: chat, short, long, exactly_1_sentence, exactly_3_sentences
    user_length_choices = ["short", "long", "exactly_1_sentence", "exactly_3_sentences"]
    u_length = get_sample(choices=user_length_choices, weights=[0.4, 0.3, 0.2, 0.1])

    # If the user uses a lot of scientific term -> possibilities: popularization, standard, scientific
    user_scientific_choices = ["popularization", "standard", "scientific"]
    u_scientific = get_sample(choices=user_scientific_choices, weights=[0.1, 0.8, 0.1])

    if profession == "no": # task_x_subtopics case
        return MultiturnStyle(id=id, country=sampled_country, nbr_of_turns=nbr_of_turns, mode=mode,
                            cb_length=cb_length, cb_style=cb_style, cb_scientific=cb_scientific,
                            u_length=u_length, u_scientific=u_scientific)
    else:
        return MultiturnStyle(id=id, country=sampled_country, nbr_of_turns=nbr_of_turns, mode=mode,
                            cb_length=cb_length, cb_style=cb_style, cb_scientific=cb_scientific,
                            u_length=u_length, u_scientific=u_scientific, u_specialty= profession + "specialized in " + specialty)


