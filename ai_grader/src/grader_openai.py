import openai
import pandas as pd
import random

openai.api_key = open("src/key.txt").read().strip()

filepath = "src/database.csv"
df = pd.read_csv(filepath)
before_learning_indexes = random.sample(range(0, 20), 5)
before_learning_results = {}

# Function to grade a student answer using OpenAI gpt-3.5-turbo
def grade_with_gpt(question, model_answers, student_answer):
    model_answers_str = "\n".join([f"- {ans}" for ans in model_answers])
    prompt = f"""
You are an expert C++ grader. Grade the student's answer using the scale 0 to 10.

Grading scale:
0 = completely wrong, 1 = very bad, 2-3 = poor, 4 = bad, 5 = medium, 6-7 = good, 8-9 = great, 10 = absolutely correct.

Question: {question}

Model Answers:
{model_answers_str}

Student Answer: {student_answer}

Respond with:
Grade: X
Feedback: Y
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    reply = response['choices'][0]['message']['content']
    try:
        lines = reply.strip().split('\n')
        grade_line = [line for line in lines if "Grade:" in line][0]
        feedback_line = [line for line in lines if "Feedback:" in line][0]
        grade = grade_line.split(":")[1].strip()
        feedback = feedback_line.split(":")[1].strip()
    except:
        grade = "?"
        feedback = "Could not parse response"
    return grade, feedback

# Grade 5 random questions BEFORE learning
print("\n--- Grading BEFORE Learning ---\n")
for i in before_learning_indexes:
    row = df.iloc[i]
    question = row['Question']
    student_answer = row['Student Answer']
    model_answers = [row[f"Model Answer {j}"] for j in range(1, 6)]
    grade, feedback = grade_with_gpt(question, model_answers, student_answer)
    before_learning_results[i] = grade
    print(f"Question = {question}")
    print(f"Student answer = {student_answer}")
    print(f"Q{i}: Grade = {grade} | Feedback: {feedback}")

# Simulate LEARNING from the other 15 questions
print("\n--- Learning Process (simulated) ---\n")
learn_indexes = [i for i in range(len(df)) if i not in before_learning_indexes]
for i in learn_indexes:
    row = df.iloc[i]
    question = row['Question']
    student_answer = row['Student Answer']
    model_answers = [row[f"Model Answer {j}"] for j in range(1, 6)]
    _ = grade_with_gpt(question, model_answers, student_answer)

# Grade the SAME 5 questions AGAIN after learning
print("\n--- Grading AFTER Learning ---\n")
after_learning_results = {}
for i in before_learning_indexes:
    row = df.iloc[i]
    question = row['Question']
    student_answer = row['Student Answer']
    model_answers = [row[f"Model Answer {j}"] for j in range(1, 6)]
    grade, feedback = grade_with_gpt(question, model_answers, student_answer)
    after_learning_results[i] = grade
    print(f"Question = {question}")
    print(f"Student answer = {student_answer}")
    print(f"Q{i}: Grade = {grade} | Feedback: {feedback}")

# Compare BEFORE and AFTER grades
print("\n--- Grade Comparison ---\n")
for i in before_learning_indexes:
    before = before_learning_results[i]
    after = after_learning_results[i]
    print(f"Question {i}: Before = {before} | After = {after} | Change = {int(after)-int(before) if before.isdigit() and after.isdigit() else 'N/A'}")
