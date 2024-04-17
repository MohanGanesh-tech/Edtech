import streamlit as st
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

st.set_page_config(page_title="Adaptive Questionnaire System")
st.header("Adaptive Questionnaire System")

st.sidebar.markdown("# Main page")

def display_question():
    st.text('Current question Level: Intermediate')
    st.text(st.session_state.question)
    answer = st.text_input("Your Answer", key=f"answer_{st.session_state.counter}")
    submit_button = st.button("Submit", key=f"submit_{st.session_state.counter}")
    st.text_area(value=st.session_state.conversation, label="Conversations", height=1000)
    if submit_button:
        st.session_state.conversation, st.session_state.question = app.generate_new_question_based_on_evalutation(st.session_state.conversation, answer)
        st.session_state.counter += 1

def main():
    if 'counter' not in st.session_state:
        st.session_state.init = True
    student = students_collection.find_one({'student_id': 1})
    print(f"Welcome to Quiz {student["first_name"]} {student["last_name"]}")
    
    init = 1 
    if(init == 1):
        questionResponse = IntialQuestionGenerator(student)
    else:
        questionResponse = NextQuestionGenerator(student)
    
if __name__ == "__main__":
    main()
