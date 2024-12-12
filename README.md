# Medical Instruction Tuning

This repositroy contains scripts and resources to create synthetical datasets for medical instruction tuning of Meditron-70B and MultiMeditron. Instruction tuning is a technique for fine-tuning large language models (LLMs) on a labeled dataset of instructional prompts and corresponding outputs. It improves model performance not only on specific tasks, but on following instructions in general, thus helping adapt pre-trained models for practical use. [Source: IBM instruction tuning](https://www.ibm.com/topics/instruction-tuning)

The dataset for medical instruction tuning consists of three parts:
* Part 1: multiturn_specialty_x_domain (6'321 samples)
* Part 2: multiturn_tasks_x_subtopics (12'687 samples)
* Part 3: parsed_prompts_task_x_specialties_x_demographic_x_answerstyle (20'395 samples)

The x in the name signifies the different information that was combined to generate the initial prompt, which is always the start of one multiturn interaction.

## Scripts:
#### Scripts to generate prompts that health care workers might ask Meditron:
* `genera_batch_of_prompts.ipynb` -> Generate prompts in format required for openai batch mode (Part 1 and 2)
* `generate_additional_batch_of_prompts.ipynb` -> Generate prompts in format required for openai batch mode (Part 3)
* `helper.py` -> helper function for `generate_additional_batch_of_prompts.ipynb`
* `gpt_batch_mode.ipynb` -> lauch jobs in openai batch mode and retrieve results
* `interact_with_gpt_batch_version.py` -> functions that are called in gpt_batch_mode.ipynb
* `parse_gpt_response.ipynb` -> parse results from openai batch mode
* `parse_n_gpt_responses.ipynb` -> parse results from openai batch mode, if one response contains several answers (Part 3 only)

#### Scripts to generate multiturn chat situations:
* `multiturn_modul.py` -> contains the class and methods necessary to generate system prompts for gpt. The system prompts tell gpt to either be Meditron or a health care worker
* `multiturn_get_batch_prompt.ipynb` -> generate batch of prompts to get the next conversation step in a multitun chat using the openai batch mode
* `parse_multiturn_gpt_response.ipynb` -> parse results from openai batch mode and add the response as the next step in the conversation in a .jsonl

#### Scripts for testing:
* `interact_with_gpt.ipynb` -> use openai API in "normal" mode, used for testing
* `multiturn_test.ipynb` -> test the code used for multiturn chat generation on a single example
* `test.ipynb` -> code to visually examine important .jsonl files before processing them by gpt

## Results
* The prompts are stored in `parsed_prompts_specialty_x_domain.json`, `parsed_prompts_tasks_x_subtopics.json`, `parsed_prompts_tasks_x_subtopics_part2.json` and `parsed_prompts_task_x_specialties_x_demographic_x_answerstyle.json`
* The multiturn chats are stored in `multiturn_tasks_x_subtopics.jsonl`, `multiturn_specialty_x_domain.jsonl` and `multiturn_task_x_specialties_x_demographic_x_answerstyle.jsonl`
* The situations file contain the system prompts that were generated at random (following given distributions)

## Resources
* Contains useful lists of medical professions, medical topics and tasks a chatbot can be useful for in the medical domain: `medical_professions.json`, `medical_topics.json`, `medical_subtopics.json`, `medical_ai_tasks.json` and `medical_settings.json`
* Contains style and format instruction for instruction following: `answer_styles.json`
* Contains information about patient demographics and treatments limited to a certain age category: `age_categories.json`, `patient_age_medical_profession.json` and `sex_and_gender.json`

## Contributions
Code written by Tim Arni in the context of a semester research project during a Master's in Data Science at EPFL. Supervised by Etienne Boisson, Bastien and Alexandre Sallinen (EPFL).