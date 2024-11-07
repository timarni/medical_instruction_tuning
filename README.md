# Medical Instruction Tuning

Scripts to generate prompts that health care workers might ask to Meditron. Will later be used for multi-turn instruction tuning of Meditron.

scripts:
* `genera_batch_of_prompts.ipynb` -> Generate prompts in format required for openai batch mode
* `gpt_batch_mode.ipynb` -> lauch jobs in openai batch mode and retrieve results
* `interact_with_gpt_batch_version.py` -> functions that are called in gpt_batch_mode.ipynb
* `interact_with_gpt.ipynb` -> use openai API in "normal" mode
* `parse_gpt_response.ipynb` -> parse results from openai batch mode

results:
* The final results are stored in `parsed_prompts_specialty_x_domain.json` and `parsed_prompts_tasks_x_subtopics.json`
* Useful lists of topics are: `medical_professions.json`, `medical_topics.json`, `medical_subtopics.json`, `medical_ai_tasks.json` (not used yet), `medical_settings.json` (not used yet)

[InternetShortcut]
URL=https://www.ibm.com/topics/instruction-tuning
