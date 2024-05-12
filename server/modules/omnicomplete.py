import json
import os

PROMPT_ROOT_DIR = os.getenv("PROMPT_ROOT_DIR")


def build_omni_complete_prompt(input_value, topic="Vue.js", topic_dir="vuejs"):

    prompt = open(f"{PROMPT_ROOT_DIR}/prompt.txt", "r").read()

    previous_completions = open(
        f"{PROMPT_ROOT_DIR}/knowledge_bases/{topic_dir}/previous_completions.json", "r"
    ).read()

    domain_knowledge = open(
        f"{PROMPT_ROOT_DIR}/knowledge_bases/{topic_dir}/domain_knowledge.txt", "r"
    ).read()

    prompt = prompt.replace("{{topic}}", topic)
    prompt = prompt.replace("{{previous_completions}}", previous_completions)
    prompt = prompt.replace("{{domain_knowledge}}", domain_knowledge)
    prompt = prompt.replace("{{input_value}}", input_value)
    return prompt


def increment_or_create_previous_completions(input, completion, topic_dir):

    previous_completions_file = (
        f"{PROMPT_ROOT_DIR}/knowledge_bases/{topic_dir}/previous_completions.json"
    )

    """
    [
        {
            "input": "style this button with",
            "completions": [
                "tailwindcss and make it look like a switch",
                "unocss and make it look like a switch"
            ],
            "hits": 5
        },
    ...
    ]
    """
    previous_completions = open(previous_completions_file, "r").read()

    previous_completions = json.loads(previous_completions)
    matching_icase = [
        item
        for item in previous_completions
        if item["input"].lower() == input.lower()
        and any(
            completion.lower() in completion.lower()
            for completion in item["completions"]
        )
    ]

    if matching_icase:
        matching_icase[0]["hits"] += 1
    else:
        new_completion = {"input": input, "completions": [completion], "hits": 1}
        previous_completions.append(new_completion)

    completions_sorted_by_hits = sorted(
        previous_completions, key=lambda x: x["hits"], reverse=True
    )

    # write back to file
    with open(previous_completions_file, "w") as f:
        json.dump(completions_sorted_by_hits, f, indent=4)
