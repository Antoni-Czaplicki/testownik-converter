import json
import os

def get_user_input(prompt, default=None):
    value = input(f"{prompt}{f' (default: {default})' if default else ''}: ").strip()
    return value if value else default

def process_question(file, path):
    template = file[0].strip()
    question = file[1].strip()
    answers = []

    for i in range(2, len(file)):
        try:
            answers.append({
                "answer": file[i].strip(),
                "correct": template[i - 2] == "1"
            })
        except IndexError:
            print(f"Error in file {path} at line {i}. Setting unknown value to False.")
            answers.append({
                "answer": file[i].strip(),
                "correct": False
            })

    is_true_false = (
        template in ("X01", "X10") and
        len(answers) == 2 and
        all(ans["answer"].lower() in {"prawda", "tak", "true", "fałsz", "nie", "false"} for ans in answers)
    )

    return {
        "question": question,
        "answers": answers,
        "multiple": not is_true_false,
        "explanation": None,
    }

def read_file(path, encodings):
    for encoding in encodings:
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read().strip().splitlines()
        except UnicodeDecodeError:
            continue
    print(f"Error reading file {path}. Skipping.")
    return None

def main():
    input_folder = get_user_input("Enter the input folder name", "stary_format")
    quiz_title = get_user_input("Enter the quiz title", "Baza " + input_folder)

    questions = []
    question_set = set()
    index = 1

    properties = {
        "title": quiz_title,
        "description": get_user_input("Enter a description for the quiz (optional)"),
        "version": 1
    }

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)
                lines = read_file(path, ["utf-8", "windows-1250"])

                if not lines:
                    continue

                question = process_question(lines, path)
                question_str = json.dumps(question, ensure_ascii=False)

                if question_str in question_set:
                    print(f"Duplicate question in file {path}. Skipping.")
                    continue

                question["id"] = index
                questions.append(question)
                question_set.add(question_str)
                index += 1

    properties["questions"] = questions

    output_file = quiz_title.lower().replace(" ", "_") + ".json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(properties, f, ensure_ascii=False, indent=4)

    print(f"Quiz successfully created and saved as {output_file}")

if __name__ == "__main__":
    main()