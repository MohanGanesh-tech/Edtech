from questionGenerator import IntialQuestionGenerator, NextQuestionGenerator
from evaluator import EachQuestionEvaluator, OverallStudentEvaluator
from redisConnection import RedisConnection
from mongoConnection import MongodbConnections
from messageFormator import convert_conversation

inMemory = RedisConnection()
inMemory.flushdb()

mongoClient = MongodbConnections()
db_collections = mongoClient['edtech']
students_collection = db_collections['Student']
quiz_collection = db_collections['Quiz']

eachQuestionEvaluatorResponseList = []

student = students_collection.find_one({'student_id': 1})
print(f"Welcome to Quiz {student["first_name"]} {student["last_name"]}")

# Intialization
print(f"\nQuestion: 1")
intialQuestionResponse = IntialQuestionGenerator(student)
print(f"""Subject = {intialQuestionResponse['subject']}
Question = {intialQuestionResponse['question']}
Options = {intialQuestionResponse['options']}
Question-level = {intialQuestionResponse['current_question_level']}""")

answer = str(input("\nEnter your Answer:\n"))
eachQuestionEvaluatorResponse = EachQuestionEvaluator(student["student_id"], answer)
eachQuestionEvaluatorResponseList.append(eachQuestionEvaluatorResponse)
print(f"""Review = {eachQuestionEvaluatorResponse['review']}
Feedback = {eachQuestionEvaluatorResponse['feedback']}
Student Knowledge Level = {eachQuestionEvaluatorResponse['student_knowledge_level']}""")

#Next question based on student performance
for i in range(2,3):
    print(f"\nQuestion: {i}")
    nextQuestionGeneratoResponse = NextQuestionGenerator(student["student_id"])
    print(f"""Subject = {nextQuestionGeneratoResponse['subject']}
    Question = {nextQuestionGeneratoResponse['question']}
    Options = {nextQuestionGeneratoResponse['options']}
    Question-level = {nextQuestionGeneratoResponse['current_question_level']}""")

    answer = str(input("\nEnter your Answer:\n"))
    eachQuestionEvaluatorResponse = EachQuestionEvaluator(student["student_id"], answer)
    eachQuestionEvaluatorResponseList.append(eachQuestionEvaluatorResponse)
    print(f"""Review = {eachQuestionEvaluatorResponse['review']}
    Feedback = {eachQuestionEvaluatorResponse['feedback']}
    Student Knowledge Level = {eachQuestionEvaluatorResponse['student_knowledge_level']}""")

#Overall student performace
overallStudentEvaluatorResponse,conversation = OverallStudentEvaluator(student["student_id"])
print(f"""\n\nTotal number of questions attempted = {overallStudentEvaluatorResponse['total_number_of_questions']}
Total number of correct answers = {overallStudentEvaluatorResponse['total_number_of_correct_answers']}
Feedback on each subject = {overallStudentEvaluatorResponse['review_on_each_subject']}
Overall Student Knowledge Level = {overallStudentEvaluatorResponse['overall_student_knowledge_level']}""")

converted_conversation = convert_conversation(conversation)
quiz = {
    "Student_id": student["student_id"],
    "Quiz_conversation": converted_conversation,
    "Overall_student_performance": overallStudentEvaluatorResponse,
    "eachQuestionEvaluatorResponseList": eachQuestionEvaluatorResponseList
}
quiz_collection.insert_one(quiz)
print("\nQuiz completed! Thank you for taking the quiz.")