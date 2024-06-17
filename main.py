import json
import os

questions = []
question_set = set()
index = 1

true_false_strings = {
    "prawda": True, "tak": True, "true": True,
    "fałsz": False, "nie": False, "false": False
}

properties = {
    "title": None,
    "description": None,
    "author": None,
    "report_url": None,
    "report_email": None,
    "source_url": None,
    "version": 1
}


def process_question(file, path):
    template = file[0].strip()
    question = file[1].strip()
    answers = []
    for s in range(2, len(file)):
        try:
            answers.append({
                "answer": file[s].strip(),
                "correct": False if template[s - 1] == "0" else True
            })
        except IndexError:
            print(f"Error in file {path} at line {s}. Replacing the unknown value with False.")
            answers.append({
                "answer": file[s].strip(),
                "correct": False
            })

    is_true_false = (template == "X01" or template == "X10") and \
                    true_false_strings.get(answers[0]["answer"].lower()) is not None and \
                    true_false_strings.get(answers[1]["answer"].lower()) is not None

    return {
        "question": question,
        "answers": answers,
        "multiple": not is_true_false
    }


def read_file(path, encodings):
    for encoding in encodings:
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read().strip().splitlines()
        except UnicodeDecodeError:
            continue
    print(f"Error in file {path}. Skipping.")
    return None


for root, dirs, files in os.walk("stary_format"):
    for file in files:
        if file.endswith(".txt"):
            lines = read_file(os.path.join(root, file), ["utf-8", "windows-1250"])
            if lines is None:
                continue

            question = process_question(lines, os.path.join(root, file))
            question_str = json.dumps(question, ensure_ascii=False)

            if question_str in question_set:
                print(f"Duplicate question in file {os.path.join(root, file)}. Skipping.")
                continue

            question["id"] = index
            questions.append(question)
            question_set.add(question_str)
            index += 1

properties["questions"] = questions

with open((properties.get("title") or "baza").lower().replace(" ", "_") + ".json", "w", encoding="utf-8") as f:
    json.dump(properties, f, ensure_ascii=False, indent=4)
