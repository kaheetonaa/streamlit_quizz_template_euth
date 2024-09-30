from pymongo import MongoClient
import streamlit as st
import json

def run():
    st.set_page_config(
        page_title="🌐 EuthMappers quizz",
        page_icon="❓",
    )

if __name__ == "__main__":
    run()

@st.cache_resource
def init_connection():
    return MongoClient("mongodb+srv://kuquanghuy:quanghuy123456@cluster0.6mzug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = init_connection()

db=client['EuthMappers']
collection=db['EuthMappers']


# Custom CSS for the buttons
st.markdown("""
<style>
    [role=radiogroup]{
        gap: 1rem;
    }
    h1 {
        text-align: center
    }
    h2 {
        text-align: center
    }
    h3 {
        text-align: center
    }
    div[data-testid='stAppViewBlockContainer']{
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session variables if they do not exist
answer=[]
default_values = {'current_index': int(st.query_params['index']), 'current_question': 0, 'score': 0, 'selected_option': [], 'answer_submitted': False}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Load quiz data
with open('content/quiz_data.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

#def restart_quiz():
#    st.session_state.current_index = 0
#    st.session_state.score = 0
#    st.session_state.selected_option = None
#    st.session_state.answer_submitted = False

def submit_answer():

    # Check if an option has been selected
    if st.session_state.selected_option is not None and school is not None:
        # Mark the answer as submitted
        st.session_state.answer_submitted = True
        for selection in st.session_state.selected_option:
            post={'question':st.session_state.current_index,'school':school,'selection':selection}
            collection.insert_one(post)
        
        # Check if the selected option is correct
        #if st.session_state.selected_option == quiz_data[st.session_state.current_index]['answer']:
        #    st.session_state.score += 10
    else:
        # If no option selected, show a message and do not mark as submitted
        st.warning("Please select an option before submitting.")

#def next_question():
#    st.session_state.current_index += 1
#    st.session_state.selected_option = None
#    st.session_state.answer_submitted = False

# Title and description
container1 = st.container()
div = """<div class = 'test1'>"""
divEnd = """</div>"""


with container1:
    st.html("<img src='asset/logo.png' width='5%'/>")

    # Progress bar
    #progress_bar_value = (st.session_state.current_index + 1) / len(quiz_data)
    #st.metric(label="Score", value=f"{st.session_state.score} / {len(quiz_data) * 10}")
    #st.progress(progress_bar_value)

    # Display the question and answer options


    question_item = quiz_data[st.session_state.current_index]

    st.subheader(f"Question {st.session_state.current_index + 1}")
    st.header(f"{question_item['question']}")
    st.write(question_item['information'])

    st.markdown(""" ___""")
    # Answer selection
    options = question_item['options']
    correct_answer = question_item['answer']

    if st.session_state.answer_submitted:
        if correct_answer=='Free':
            st.write('You have submitted as '+str(st.session_state.selected_option)[1:-1])
        else:
            if st.session_state.selected_option==correct_answer:
                st.success("Correct!")
            else:
                st.error("Not really...")
                st.write('The correct answer should be:'+str(correct_answer)[1:-1])
        #for i, option in enumerate(options):
        #    label = option
        #   if option == correct_answer:
        #       st.success(f"{label} (Correct answer)")
        #    elif option == st.session_state.selected_option:
        #        st.error(f"{label} (Incorrect answer)")
        #    else:
        #        st.write(label)
    else:
        school = st.selectbox(
        "Where is your school",
        ("🇮🇹Italy", "🇵🇹Portugal", "🇷🇴Romania", "🇸🇰Slovakia", "🇪🇸Spain"),index=None
        )
        match question_item['type']:
                case 'single':
                    answer=st.radio(label='',options=options)
                    st.session_state.selected_option=[answer]
                case 'multiple':
                    for i, option in enumerate(options):
                        answer.append(st.checkbox(option))
                        if (answer[i]):
                            if option not in st.session_state.selected_option:
                                st.session_state.selected_option.append(option)
                                st.session_state.selected_option=sorted(st.session_state.selected_option)
                        if (answer[i]==False):
                            if option in st.session_state.selected_option:
                                st.session_state.selected_option.remove(option)
                        #if st.button(option, key=i, use_container_width=True):
                        #    st.session_state.selected_option = option
        st.markdown(""" ___""")
        if len(st.session_state.selected_option)>0:
            st.write('You have selected **'+ str(st.session_state.selected_option)[1:-1]+'**')



    # Submission button and response logic
    #if st.session_state.answer_submitted:
    #    if st.session_state.current_index < len(quiz_data) - 1:
    #        st.button('Next', on_click=next_question)
    #    else:
    #        st.write(f"Quiz completed! Your score is: {st.session_state.score} / {len(quiz_data) * 10}")
    #        if st.button('Restart', on_click=restart_quiz):
    #            pass
    #else:
    if not st.session_state.answer_submitted:
        st.button('Submit', on_click=submit_answer)
        