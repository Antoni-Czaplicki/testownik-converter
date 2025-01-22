import json
import os


def save_question_to_file(question, output_folder, index):
    """Saves a single question to a text file."""
    file_name = f"{index:03}.txt"
    file_path = os.path.join(output_folder, file_name)

    template = ''.join(['1' if ans['correct'] else '0' for ans in question['answers']])
    lines = [
        (question['question'].count("\n") + 1) * "X" + template,
        question['question'],
        *[ans['answer'] for ans in question['answers']]
    ]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Saved: {file_path}")


def main():
    input_file = input("Enter the JSON file name: ").strip()
    output_folder = input(f"Enter the output folder name (default: {input_file}_output): ").strip()

    if not input_file.endswith(".json"):
        input_file += ".json"

    if not output_folder:
        output_folder = input_file.replace(".json", "_output")

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Read the JSON file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file: {e}")
        return

    questions = data.get("questions", [])
    if not questions:
        print("No questions found in the JSON file.")
        return

    # Save each question to a separate text file
    for index, question in enumerate(questions, start=1):
        save_question_to_file(question, output_folder, index)

    print(f"All questions have been saved in the folder: {output_folder}")


if __name__ == "__main__":
    main()
