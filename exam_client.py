
from datetime import datetime
from question_master import load_questions_nested
import logging
import re

 
logging.basicConfig(
    filename="exam_client.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

 
def normalize_answer(ans):
    ans = ans.strip().lower()
    if ans in ["op1", "op2", "op3", "op4"]:
        return ans
    if ans in ["1", "2", "3", "4"]:
        return f"op{ans}"
    return None

 
def validate_name(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z ]+", name.strip()))

def validate_university(university: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z ]+", university.strip()))

 
def exam():
    student = None
    university = None
    try:
         
        now = datetime.now().strftime("%d/%b/%Y %H.%M.%S")
        print("Date & Time:", now)

         
        while True:
            student = input("Enter student name: ").strip()
            if validate_name(student):
                break
            print("❌ Invalid name! Use only alphabets and spaces (full name required).")
            logging.warning("Invalid student name entered.")

        while True:
            university = input("Enter university: ").strip()
            if validate_university(university):
                break
            print("❌ Invalid university name! Use only alphabets and spaces.")
            logging.warning("Invalid university entered.")

         
        questions = load_questions_nested()
        if not questions:
            print("❌ No questions available!")
            logging.warning("No questions available for exam.")
            return

        score = 0
        total = len(questions)

         
        for qid, qinfo in questions.items():
            print(f"\n{qid}) {qinfo['question']}")
            for idx, option in enumerate(qinfo["options"], start=1):
                print(f"   {idx}. {option}")

            while True:
                ans = input("Enter your answer (op1-op4 or 1-4): ").strip()
                choice = normalize_answer(ans)
                if choice:
                    break
                print("❌ Invalid choice, try again...")

            if choice == qinfo["answer"]:
                score += 1

         
        print("\n=== Test Summary ===")
        print("Student name =", student)
        print("University   =", university)
        print(f"Marks scored = {score} correct out of {total} questions")
        logging.info(f"Exam completed for student {student} ({university}). Score: {score}/{total}")

    except KeyboardInterrupt:
        
        if student and university:
            logging.warning(f"Exam interrupted by user {student} ({university}) via Ctrl+C.")
        else:
            logging.warning("Exam interrupted by user before providing details (Ctrl+C).")
        print("\n⚠️ Exam interrupted by user. Progress not saved.")
    except Exception as e:
        logging.error(f"Error during exam: {e}")
        print("❌ An error occurred during the exam.")

 
if __name__ == "__main__":
    exam()
