<<<<<<< HEAD
An interactive Multiple Choice Question (MCQ) online examination system built using Python.
The app dynamically loads questions from a CSV file, conducts the exam, and automatically evaluates user answers.

🗂 Project Structure
File Name	Description
question.csv	Stores questions, options, and correct answers
question_master.py	Handles loading and managing questions
exam_client.py	Provides the user interface for taking the exam

📝 Example question.csv

Below is the format for adding questions:

num,question,option1,option2,option3,option4,correctoption
1,10+20 ans is,op1=20,op2=30,op3=40,op4=10,op2
2,20-10 ans is,op1=20,op2=30,op3=40,op4=10,op4
3,2*2 ans is,op1=4,op2=5,op3=6,op4=7,op1
4,5/2 ans is,op1=2.5,op2=3,op3=6,op4=7,op1
5,capital of india,op1=delhi,op2=blr,op3=mum,op4=chn,op1
6,linux is a,op1=os,op2=app,op3=game,op4=antivirus,op1

✨ Key Features

Dynamic loading of questions from a CSV file

Interactive multiple-choice exam interface

Automatic validation of user responses

Final score display at the end of the test

⚙️ Tech Stack

Language: Python 3

Library: CSV Module (to handle question data)

🚀 Getting Started

Follow these steps to run the project locally:

1️⃣ Clone the Repository
git clone https://github.com/your-username/mcq-exam-app.git
cd mcq-exam-app

2️⃣ Ensure CSV File is Present

Make sure question.csv exists in the project folder.

3️⃣ Run the Exam
python exam_client.py

🔮 Future Enhancements

Timer for each question

Store results and history in a separate file

GUI version using Tkinter or a web version using Flask

User authentication and role management

📖 Summary

This project is perfect for understanding:

File handling in Python

CSV data management

Building basic console-based applications
=======
# schoolWebsite
>>>>>>> 25018357c7c671c822ac21312be41e45208da1b0
