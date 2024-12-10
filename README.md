# Medical Instruction Tuning

This repositroy contains scripts and resources to create synthetical dataset for medical instruction tuning of Meditron-70B and MultiMeditron. 

Content:
* Scripts to generate prompts that health care workers might ask to Meditron.
* Scripts to generate multiturn chats, which will be used for instruction tuning of Meditron.

scripts:
* `genera_batch_of_prompts.ipynb` -> Generate prompts in format required for openai batch mode
* `gpt_batch_mode.ipynb` -> lauch jobs in openai batch mode and retrieve results
* `interact_with_gpt_batch_version.py` -> functions that are called in gpt_batch_mode.ipynb
* `interact_with_gpt.ipynb` -> use openai API in "normal" mode
* `parse_gpt_response.ipynb` -> parse results from openai batch mode
* `multiturn_modul.py` -> contains the class and methods necessary to generate system prompts for gpt. The system prompts tell gpt to either be Meditron or a health care worker
* `multiturn_get_batch_prompt.ipynb` -> generate batch of prompts to get the next conversation step in a multitun chat using the openai batch mode
* `multiturn_test.ipynb` -> test the code used for multiturn chat generation on a single example
* `parse_multiturn_gpt_response.ipynb` -> parse results from openai batch mode and add the response as the next step in the conversation in a .jsonl

results:
* The prompts are stored in `parsed_prompts_specialty_x_domain.json`, `parsed_prompts_tasks_x_subtopics.json` and `parsed_prompts_tasks_x_subtopics_part2.json`
* The multiturn chats are stored in `multiturn_tasks_x_subtopics.jsonl` and `multiturn_specialty_x_domain.jsonl`
* The situations file contain the system prompts that were generated at random (following given distributions)

resources:
* Contains useful lists of medical professions, medical topics and tasks a chatbot can be useful for in the medical domain: `medical_professions.json`, `medical_topics.json`, `medical_subtopics.json`, `medical_ai_tasks.json` and `medical_settings.json`
* [IBM instruction tuning](https://www.ibm.com/topics/instruction-tuning)


code written by Tim Arni in the context of a semester research project during a Master's in Data Science at EPFL