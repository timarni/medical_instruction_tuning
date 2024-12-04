import json
from tqdm import tqdm
from multiturn_modul import MultiturnStyle, get_multiturn_style
import pandas as pd
import random
import math

# prompt and context
def get_prompt(nbr_of_questions, task, description, additional_instruction, demographics, profession="physician", specialty="no", topic="no"):
    prompt_parts = []
    prompt_parts.append(f"Generate {nbr_of_questions} different prompts that a {profession} ")
    if specialty != "no":
        prompt_parts.append(f"specializing in {specialty} ")
    prompt_parts.append(f"might ask an AI chatbot when tasked with {task} ")
    if topic != "no":
        prompt_parts.append(f"in the context of the medical field \"{topic}\".\n")
    else:
        prompt_parts.append(f".\n")
    prompt_parts.append(f"{task} is described as: {description}\n")
    prompt_parts.append(f"To create a realistic prompt, follow these additional instructions: {additional_instruction}\n")
    for i, enum_word in enumerate(["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth"]):
        if i >= nbr_of_questions:
            break
        prompt_parts.append(f"The {enum_word} question you generate has to be about a patient seeing a {profession} in {demographics[i]["country"]}. The patient has the following demographic attributes:\n")
        prompt_parts.append(f"age range: {demographics[i]["age"][0]} ({demographics[i]["age"][1]} old)\n")
        prompt_parts.append(f"sex: {demographics[i]["sex"]}\n")
        prompt_parts.append(f"gender: {demographics[i]["gender"]}\n")
    prompt_parts.append("Only include the generated prompts, adding extra details only if specified. Focus solely on the realistic prompts the health care workers working in the specified countries might ask a medical AI chatbot.\n")
    prompt_parts.append("Separate each prompt you generate in the output by ###\n")
    prompt = "".join(prompt_parts)
    return prompt

def fill_line(prompt_id, gpt_model, content, prompt, max_tokens):
    line = {
        "custom_id": prompt_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": gpt_model,
            "messages": [
                {"role": "system", "content": content},
                {"role": "user", "content": f"{prompt}"}
            ],
            "max_tokens": max_tokens
        }
    }
    return line

def get_countries(countries_df, nbr_samples):
    # Step 1: Group by 'Income Category'
    groups = countries_df.groupby("Income Category")
    nbr_of_groups = groups.ngroups
    samples_per_group = math.ceil(nbr_samples / nbr_of_groups)

    # Step 2: Randomly sample countries from the different categories
    sampled_countries = []
    for category, group in groups:
        sampled_countries.append(group.sample(n=samples_per_group))
    sampled_countries_df = pd.concat(sampled_countries).reset_index(drop=True).sample(nbr_samples)
    sampled_countries = sampled_countries_df["Country"].to_list()

    if len(sampled_countries) != nbr_samples:
        raise ValueError(f"lenght of countires is not as expected: {sampled_countries}")

    return sampled_countries

def get_ages(age_categories, possible_ages, nbr_sample):
    all_ages = [dict["category"] for dict in age_categories]
    if possible_ages[0] == "All age categories":
        possible_ages = all_ages
    sampled_ages = random.choices(possible_ages, k=nbr_sample)
    ages = []
    for age in sampled_ages:
        for entry in age_categories:
            if entry["category"] == age:
                ages.append([age, entry["range"]])
    if len(ages) != nbr_sample:
        raise ValueError(f"lenght of ages is not as expected: {ages}")

    return ages

def adjust_ages(age_categories, possible_ages, medical_topic):
    all_ages = set([dict["category"] for dict in age_categories])
    if possible_ages[0] == "All age categories":
        possible_ages = all_ages

    possible_ages_set = set(possible_ages)
    # special cases
    if medical_topic == "Pediatrics":
        adjusted_possible_ages = possible_ages_set & {"Infants", "Toddlers", "Preschoolers", "School-age Children", "Adolescents"}
    elif medical_topic == "Geriatrics":
        adjusted_possible_ages = possible_ages_set & {"Older Adults", "Elderly", "Centenarians"}
    elif medical_topic == "Neonatology":
        adjusted_possible_ages = possible_ages_set & {"Infants"}
    elif medical_topic == "Pain Management":
        adjusted_possible_ages = possible_ages_set & {"Adults", "Middle-aged Adults", "Older Adults", "Elderly"}
    elif medical_topic == "Physical Medicine and Rehabilitation":
        adjusted_possible_ages = possible_ages_set & {"Adults", "Middle-aged Adults", "Older Adults", "Elderly"}
    elif medical_topic == "Occupational Health":
        adjusted_possible_ages = possible_ages_set & {"Adolescents", "Young Adults", "Adults", "Middle-aged Adults", "Older Adults"}
    else:
        adjusted_possible_ages = possible_ages_set
    if len(adjusted_possible_ages) == 0:
        adjusted_possible_ages.add("no specification")
    if adjusted_possible_ages.issubset(all_ages):
        return list(adjusted_possible_ages)
    else:
        raise ValueError(f"Not allowed values in: {adjusted_possible_ages}")

def get_sex_gender(sex_and_gender, specialty, nbr_samples):
    sexes = ["Male", "Female", "Intersex"]
    sexes_rate = [0.49, 0.49, 0.02]
    sampled_sexes, sampled_genders = [], []
    sampled_sexes = random.choices(sexes, sexes_rate, k=nbr_samples)
    if specialty == "Obstetrics and Gynecology":
        sampled_sexes = random.choices(sexes[1:], sexes_rate[1:], k=nbr_samples)
    for sex in sampled_sexes:
        genders, rates = [], []
        for entry in sex_and_gender:
            if entry["sex"] == sex:
                genders = entry["gender"]
                rates = entry["rates"]
                break
        sampled_genders.append(random.choices(genders, rates, k=1)[0])
        
    if (len(sampled_genders) != nbr_samples) or (len(sampled_sexes) != nbr_samples):
        raise ValueError(f'''lenght of sexes: {sampled_sexes} or genders: {sampled_genders} is not as expected''')

    return sampled_sexes, sampled_genders




def get_demographics(countries_df, age_categories, sex_and_gender, nbr_samples,
                     possible_ages = ["All age categories"], medical_topic="no", specialty="no"):
    adjusted_possible_ages = adjust_ages(age_categories, possible_ages, medical_topic)
    countries = get_countries(countries_df, nbr_samples)
    ages = get_ages(age_categories, adjusted_possible_ages, nbr_samples)
    sex, gender = get_sex_gender(sex_and_gender, specialty, nbr_samples)

    if len(countries) == len(ages) == len(sex) == len(gender) == nbr_samples:

        list_of_patients = []
        for i in range(nbr_samples):
            dict = {}
            dict["country"] = countries[i]
            dict["age"] = ages[i]
            dict["sex"] = sex[i]
            dict["gender"] = gender[i]
            list_of_patients.append(dict)
        
        return list_of_patients

    else:
        raise ValueError(f'''the lengths are not the same:
                         {countries}, {ages}, {sex}, {gender}''')