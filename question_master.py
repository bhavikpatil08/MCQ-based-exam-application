import csv
import logging
import re

 
logging.basicConfig(
    filename="question_master.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CSV_FILE = "questions.csv"
FIELDS = ["num", "question", "option1", "option2", "option3", "option4", "correctoption"]

# -----------------------------
def normalize_correct_option(val):
    """Accept '1'..'4', 'op1'..'op4', 'option1'..'option4' and return 'opN' or None."""
    if val is None:
        return None
    v = val.strip().lower()
    if v in ("1", "2", "3", "4"):
        return "op" + v
    m = re.fullmatch(r"op([1-4])", v)
    if m:
        return "op" + m.group(1)
    m2 = re.fullmatch(r"option([1-4])", v)
    if m2:
        return "op" + m2.group(1)
    return None

 
def read_questions():
    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            questions = []
            invalid_count = 0

            for row in reader:
                
                cleaned = {k: (row.get(k, "") or "").strip() for k in FIELDS}

                
                norm_corr = normalize_correct_option(cleaned.get("correctoption", ""))
                cleaned["correctoption"] = norm_corr or ""

                
                if (
                    not cleaned["question"]
                    or not cleaned["option1"]
                    or not cleaned["option2"]
                    or not cleaned["option3"]
                    or not cleaned["option4"]
                    or cleaned["correctoption"] not in ("op1", "op2", "op3", "op4")
                ):
                    logging.warning(f"Skipping invalid/empty row in {CSV_FILE}: {row}")
                    invalid_count += 1
                    continue

                questions.append(cleaned)

            if invalid_count > 0:
                 
                for i, q in enumerate(questions):
                    q["num"] = str(i + 1)
                write_questions(questions)
                logging.info(f"Sanitized {invalid_count} invalid rows and rewrote {CSV_FILE}.")

            return questions

    except FileNotFoundError:
        logging.warning(f"{CSV_FILE} not found.")
        return []
    except Exception as e:
        logging.error(f"Error reading {CSV_FILE}: {e}")
        return []

 
def write_questions(questions):
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(questions)
        logging.info("Questions written successfully.")
    except Exception as e:
        logging.error(f"Error writing {CSV_FILE}: {e}")

 
def load_questions_nested():
    nested = {}
    try:
        questions_list = read_questions()
        for q in questions_list:
            nested[q["num"]] = {
                "question": q["question"],
                "options": [q["option1"], q["option2"], q["option3"], q["option4"]],
                "answer": q["correctoption"]
            }
        logging.info("Nested questions loaded successfully.")
    except Exception as e:
        logging.error(f"Error creating nested questions: {e}")
    return nested

 
def add_question():
    try:
        questions = read_questions()
        next_num = max([int(q["num"]) for q in questions], default=0) + 1

         
        while True:
            question = input("Enter question: ").strip()
            if not question:
                print("❌ Question cannot be empty. Try again.")
                continue
            break

         
        options = []
        for i in range(1, 5):
            while True:
                opt = input(f"Enter option {i}: ").strip()
                if not opt:
                    print(f"❌ Option {i} cannot be empty. Try again.")
                    continue
                options.append(opt)
                break

         
        while True:
            correct_raw = input("Enter correct option (op1/op2/op3/op4 OR 1/2/3/4): ").strip()
            correct = normalize_correct_option(correct_raw)
            if correct is None:
                print("❌ Invalid correct option! Must be one of: op1, op2, op3, op4 or 1-4.")
                continue
            break

        new_q = {
            "num": str(next_num),
            "question": question,
            "option1": options[0],
            "option2": options[1],
            "option3": options[2],
            "option4": options[3],
            "correctoption": correct
        }

        questions.append(new_q)
        write_questions(questions)
        logging.info(f"Question {next_num} added successfully.")
        print("✅ Question added!")
    except Exception as e:
        logging.error(f"Error adding question: {e}")
        print("❌ Failed to add question.")

 
def search_question():
    try:
        num = input("Enter question number to search: ").strip()
        questions = read_questions()
        for q in questions:
            if q["num"] == num:
                print(f"\n{q['num']}) {q['question']}")
                for i in range(1, 5):
                    print("   ", q[f"option{i}"])
                print("Correct:", q["correctoption"])
                logging.info(f"Question {num} found.")
                return
        print(" Question not found")
        logging.warning(f"Question {num} not found.")
    except Exception as e:
        logging.error(f"Error searching question: {e}")

 
def delete_question():
    try:
        num = input("Enter question number to delete: ").strip()
        questions = read_questions()
        new_qs = [q for q in questions if q["num"] != num]
        if len(new_qs) == len(questions):
            print(" Question not found")
            logging.warning(f"Delete failed. Question {num} not found.")
        else:
             
            for i, q in enumerate(new_qs):
                q["num"] = str(i + 1)
            write_questions(new_qs)
            print(" Question deleted!")
            logging.info(f"Question {num} deleted successfully.")
    except Exception as e:
        logging.error(f"Error deleting question: {e}")

 
def modify_question():
    try:
        num = input("Enter question number to modify: ").strip()
        questions = read_questions()
        for q in questions:
            if q["num"] == num:
                print("Leave blank to keep old value")

                 
                while True:
                    new_text = input(f"Question [{q['question']}]: ").strip()
                    if new_text == "":
                        new_text = q["question"]
                    if not new_text:
                        print("❌ Question cannot be empty.")
                        continue
                    break

                 
                new_options = []
                for i in range(1, 5):
                    while True:
                        new_opt = input(f"Option{i} [{q[f'option{i}']}]: ").strip()
                        if new_opt == "":
                            new_opt = q[f"option{i}"]
                        if not new_opt:
                            print(f"❌ Option {i} cannot be empty.")
                            continue
                        new_options.append(new_opt)
                        break

                 
                while True:
                    new_correct_raw = input(f"Correct option [{q['correctoption']}]: ").strip()
                    if new_correct_raw == "":
                        new_correct = q["correctoption"]
                    else:
                        new_correct = normalize_correct_option(new_correct_raw)
                        if new_correct is None:
                            print("❌ Correct option must be one of: op1, op2, op3, op4 or 1-4.")
                            continue
                    break

                 
                q.update({
                    "question": new_text,
                    "option1": new_options[0],
                    "option2": new_options[1],
                    "option3": new_options[2],
                    "option4": new_options[3],
                    "correctoption": new_correct
                })

                write_questions(questions)
                print("✅ Question modified!")
                logging.info(f"Question {num} modified successfully.")
                return
        print(" Question not found")
        logging.warning(f"Modify failed. Question {num} not found.")
    except Exception as e:
        logging.error(f"Error modifying question: {e}")
        print("❌ Error modifying question.")

 
def display_all():
    try:
        questions = read_questions()
        if not questions:
            print("No questions available.")
            return
        for q in questions:
            print(f"\n{q['num']}) {q['question']}")
            for i in range(1, 5):
                print("   ", q[f"option{i}"])
            print("Correct:", q["correctoption"])
        logging.info("Displayed all questions successfully.")
    except Exception as e:
        logging.error(f"Error displaying questions: {e}")

 
def menu():
    while True:
        print("\n=== Question Master Menu ===")
        print("1) Add Question")
        print("2) Search Question")
        print("3) Delete Question")
        print("4) Modify Question")
        print("5) Display All Questions")
        print("6) Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_question()
        elif choice == "2":
            search_question()
        elif choice == "3":
            delete_question()
        elif choice == "4":
            modify_question()
        elif choice == "5":
            display_all()
        elif choice == "6":
            print("Exiting... ")
            break
        else:
            print(" Invalid choice")

if __name__ == "__main__":
    menu()
