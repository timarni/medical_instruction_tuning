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
        self.chatbot_length = cb_length # Length of chatbots answer -> possibilities: no_specification, short, long, exactly_n_sentences
        self.chatbot_style = cb_style # Style of chatbots answer -> possibilities: no_specification, markdown, plain text, bullets, step by step
        self.chatbot_scientific = cb_scientific # If chatbot uses a lot of scientific term -> possibilities: popularization, standard, scientific

        # Initialize attributes that determine system prompt of user
        self.user_length = u_length # Length of user questions -> possibilities: no_specification, short, long, exactly_n_sentences
        self.user_scientific = u_scientific # User uses a lot of very scientific terms -> not used so far
        self.user_specialty = u_specialty
        self.bad_grammar = u_bad_grammar # user has bad grammar / does a lot of spelling mistakes -> not used so far

        # Fixed attributes
        self.base_system_prompt_chatbot = f'''You are a medical AI chatbot designed to assist health care workers working in {self.country} by answering their questions. \nThe style of your answers must follow these rules: \n'''
        self.base_system_prompt_user = f'''You are a {self.user_specialty} working in {self.country} using a medical AI chatbot to help you taking care of your patients. \nThe initial question that you ask the medical AI chatbot has already been provided. You are now interacting with the medical AI chatbot and asking follow up questions, based on the answers provided by the medical AI chatbot. \nThe style of the follow up question you ask must follow these rules: \n'''

        self.number_of_turns_done = 0

    # methods
    def get_all_system_prompts_atributes(self):
        return [self.mode, self.chatbot_length, self.chatbot_style, self.chatbot_scientific,
                self.user_length, self.user_scientific, self.user_specialty]

    # adds sytle specification to the system prompt of meditron
    def system_prompt_chatbot(self) -> str:
        prompt_parts = [self.base_system_prompt_chatbot]
        general_guidelines = '''- Respectful, polite interaction: You must always engage in a respectful, polite, and courteous manner, maintaining professionalism in all interactions.
- Honest, evidence-based information: All responses have to be based on the latest medical evidence and guidelines
- Ethical and safe content: Under no circumstances should you provide fake, harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. If a question is unclear or factually incorrect, you should explain why rather than attempting to answer it inaccurately.
- Dosage: If asked about dosage medication, provide a ballpark estimate of the dosage but always provide a concise warning that this should be checked in the form of “(dosages should be verified)”.
- Tailor responses to the geographical context, resource setting, level of care, seasonality/epidemiology, and medical specialty as relevant.'''
        prompt_parts.append(general_guidelines)
        # Chatbot can be used in chat, normal or emergency mode
        match self.mode:
            case "chat":
                prompt_parts.append("- The user is using you (the medical AI chatbot) in chat mode. Provide short and concise answers to facilitate conversation. Ask follow-up questions if the user input is unclear. \n")
            case "emergency":
                prompt_parts.append("- The user is using you (the medical AI chatbot) during a medical emergency. Provide short, concise, and well-structured answers. Your responses must be clear and easy to understand in high-pressure and stressful environments. \n")
            case "normal":
                # Set epected length of chatbots answer
                match self.chatbot_length:
                    case "no_specification":
                        pass
                    case "short":
                        prompt_parts.append("- Provide short and concises answers. \n")
                    case "long":
                        prompt_parts.append("- Provide long and detailed answers. \n")
                    case "exactly_n_sentences":
                        n = random.randint(2, 10)
                        prompt_parts.append(f"- All your answers should be exactly {n} sentences long. \n")
                    case _:
                        raise ValueError(f"Invalid chatbot_length: '{self.chatbot_length}'")
                
                # Set expected style of chatbots answer
                match self.chatbot_style:
                    case "no_specification":
                        pass
                    case "markdown":
                        prompt_parts.append("- Break down the response into clear sections with headings and subheadings in markdown format. Use bulleted or numbered lists to organize information logically and clearly. Provide all output in a nice markdown format.")
                    case "plain text":
                        prompt_parts.append("- Provide your answers as plain text. \n")
                    case "bullets":
                        prompt_parts.append("- Present your answers using bullet points. \n")
                    case "step by step":
                        prompt_parts.append("- Provide step-by-step advice to help the physician address their question. \n")
                    case _:
                        raise ValueError(f"Invalid chatbot_style: '{self.chatbot_style}'")
            case _:
                raise ValueError(f"Invalid chatbot_style: '{self.mode}'")


            
        # Add if the style of the answers should be very scientific
        match self.chatbot_scientific:
            case "popularization":
                prompt_parts.append("- Use simple and easy-to-understand language, avoiding overly complex scientific terms. \n")
            case "standard":
                pass # Don't add anything if standard
            case "scientific":
                prompt_parts.append("- Use highly specific and technical scientific terminology in your responses. \n")
            case _:
                raise ValueError(f"Invalid chatbot_scientific: '{self.chatbot_scientific}'")
        
        if self.mode in ["chat", "emergency"]:
            prompt_parts.append("In the prompt you see the whole chat history. You are (chatbot). Your task is to answer the questions and only ask follow up questions, if the user did not provide enough information in its input. \n")
            prompt_parts.append("Your (chatbot) tag is added manually, don't write it in your output. Just generate an answer to the users input")
        
        return ''.join(prompt_parts)
    
    def system_prompt_user(self) -> str:
        prompt_parts = [self.base_system_prompt_user]

        # User behavior is characterized by 3 different modes: chat, normal or emergency mode
        match self.mode:
            case "chat":
                prompt_parts.append(f"- You (the {self.user_specialty} using the medical AI chatbot) are using the medical AI chatbot in chat mode. Ask short and concise questions to facilitate conversation. Pose follow-up questions if the chatbot answers are unclear. \n")
            case "emergency":
                prompt_parts.append(f"- You (the {self.user_specialty} using the medical AI chatbot) are using the medical AI chatbot during a medical emergency. Ask short and quickly written questions. \n")
            case "normal":
                # Set epected length of chatbots answer
                match self.user_length:
                    case "no_specification":
                        pass
                    case "short":
                        prompt_parts.append("- Ask short and concises questions. \n")
                    case "long":
                        prompt_parts.append("- Ask long and detailed questions. \n")
                    case "exactly_n_sentences":
                        n = random.randint(1, 10)
                        if n == 1:
                            prompt_parts.append("- All your questions should be exactly 1 sentence long. \n")
                        else:
                            prompt_parts.append(f"- All your questions should be exactly {n} sentences long. \n")
                    case _:
                        raise ValueError(f"Invalid user_length: '{self.user_length}'")
                
        # Add if the style of the answers should be very scientific
        match self.user_scientific:
            case "popularization":
                prompt_parts.append("- Ask follow-up questions using simple and easy-to-understand terms. Avoid overly complex scientific language. \n")
            case "standard":
                pass
            case "scientific":
                prompt_parts.append("- Ask follow-up questions using precise and highly specific scientific terminology. \n")
            case _:
                raise ValueError(f"Invalid user_scientific: '{self.user_scientific}'")

        if self.mode in ["chat", "emergency"]:
            prompt_parts.append("In the prompt you see the whole chat history. You are (user). You want to get an answer to the first question you asked. Your task is to ask followup questions and to interact with the chatbot to get a clear answer to your initial, as a health care worker would do. \n")
            prompt_parts.append("Your (user) tag is added manually, don't write it in your output. Just generate a question or an instruction for the chatbot, based on the conversation history")

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
                mode = get_sample(choices=mode_choices, weights=[0.35, 0.55, 0.1])
        case _:
            raise ValueError(f"Invalid id: '{id}'")     
    
    # Number of turn
    nbr_of_turns_choices = [1, 2, 3]
    match mode:
        case s if s in ["chat", "emergency"]:
            nbr_of_turns = get_sample(choices=nbr_of_turns_choices, weights=[0.2, 0.3, 0.5])
        case "normal":
            nbr_of_turns = get_sample(choices=nbr_of_turns_choices, weights=[0.5, 0.3, 0.2])

    # Length of chatbots answer -> possibilities: short, long, exactly_2_sentences, exactly_4_sentences
    chatbot_length_choices = ["no_specification", "short", "long", "exactly_n_sentences"]
    cb_length = get_sample(choices=chatbot_length_choices, weights=[0.4, 0.2, 0.3, 0.1])

    # Style of chatbot's answer -> possibilities: chat, flat text, bullets, step by step
    chatbot_style_choices = ["no_specification", "markdown", "plain text", "bullets", "step by step"]
    cb_style = get_sample(choices=chatbot_style_choices, weights=[0.4, 0.15, 0.15, 0.15, 0.15])

    # If chatbot uses a lot of scientific term -> possibilities: popularization, standard, scientific
    chatbot_scientific_choices = ["popularization", "standard", "scientific"]
    cb_scientific = get_sample(choices=chatbot_scientific_choices, weights=[0.1, 0.8, 0.1])

    # Length of user questions -> possibilities: chat, short, long, exactly_1_sentence, exactly_3_sentences
    user_length_choices = ["no_specification", "short", "long", "exactly_n_sentences"]
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
                            u_length=u_length, u_scientific=u_scientific, u_specialty= profession + " specialized in " + specialty)
    

def get_multiturn_style_additional(id, context): # id is "A-0-2E-Cameroon"
                                                        # which is Version-number-answerstyle-countrs
    id_parts = id.split('-', 3)  # Split into three parts: letter, number, and the rest (country)

    version = id_parts[0]
    number = int(id_parts[1])
    answer_style = id_parts[2]
    country = id_parts[3]

    ai_task_nbr = int(context[0]) - 1

    # Usage mode: chat, normal, emergency (depening on id -> since )
    mode_choices = ["chat", "normal", "emergency"]
    match ai_task_nbr:
        case n if n in [1, 4, 5, 8, 9, 10, 12]: # Non Emergency cases
            mode = get_sample(choices=mode_choices, weights=[0.4, 0.6, 0])
        case 6: # Non Emergency and non chat option
              mode = "normal"
        case n if n in [0, 2, 3, 7]: # All cases possible
            mode = get_sample(choices=mode_choices, weights=[0.4, 0.5, 0.1])
        case 11: # Very good for emergency
            mode = get_sample(choices=mode_choices, weights=[0.3, 0.3, 0.4])
        case _:
            raise ValueError(f"Invalid id: '{id}'")     
    
    # Number of turn
    nbr_of_turns_choices = [1, 2, 3]
    match mode:
        case s if s in ["chat", "emergency"]:
            nbr_of_turns = get_sample(choices=nbr_of_turns_choices, weights=[0.2, 0.3, 0.5])
        case "normal":
            nbr_of_turns = get_sample(choices=nbr_of_turns_choices, weights=[0.5, 0.3, 0.2])

    # Length of chatbots answer -> possibilities: short, long, exactly_2_sentences, exactly_4_sentences
    chatbot_length_choices = ["no_specification", "short", "long", "exactly_n_sentences"]
    cb_length = get_sample(choices=chatbot_length_choices, weights=[0.6, 0.15, 0.2, 0.05])

    # Style of chatbot's answer -> possibilities: chat, flat text, bullets, step by step
    chatbot_style_choices = ["no_specification", "markdown", "plain text", "bullets", "step by step"]
    cb_style = get_sample(choices=chatbot_style_choices, weights=[0.6, 0.1, 0.1, 0.1, 0.1])

    # If chatbot uses a lot of scientific term -> possibilities: popularization, standard, scientific
    chatbot_scientific_choices = ["popularization", "standard", "scientific"]
    cb_scientific = get_sample(choices=chatbot_scientific_choices, weights=[0.1, 0.8, 0.1])

    # Length of user questions -> possibilities: chat, short, long, exactly_1_sentence, exactly_3_sentences
    user_length_choices = ["no_specification", "short", "long", "exactly_n_sentences"]
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
                            u_length=u_length, u_scientific=u_scientific, u_specialty= profession + " specialized in " + specialty)

def find_profession_by_specialty(file_path, specialty):
    """
    Takes a JSON file path and a specialty string, and returns the associated profession.

    Parameters:
        file_path (str): Path to the JSON file.
        specialty (str): The specialty to search for.

    Returns:
        str: The profession associated with the specialty, or None if not found.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        for entry in data:
            if specialty in entry.get("specialties", []):
                return entry.get("profession")

        return None  # Specialty not found in any profession

    except FileNotFoundError:
        print(f"Error: File at {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from file at {file_path}.")
        return None