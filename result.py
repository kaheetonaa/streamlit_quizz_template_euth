from pymongo import MongoClient
import streamlit as st
import pandas as pd
import altair as alt

def run():
    st.set_page_config(
        page_title="🌐 EuthMappers quizz result",
        page_icon="✅",
        layout="wide",
        initial_sidebar_state='expanded'
    )


if __name__ == "__main__":
    run()

st.session_state.ws=int(st.query_params['ws'])

match st.session_state.ws:
    case 0:
        database_name='EuthMappers'
        note='<h1>The result of the two workshops</h1>'
    case 1:
        database_name='EuthMappers'
        note='<h1>The result of the workshop on 03/10/2024</h1>'
    case 2:
        database_name='EuthMappers_2'
        note='<h1>The result of the workshop on 09/10/2024</h1>'

if st.session_state.ws!==0:
    @st.cache_resource
    def init_connection():
        return MongoClient("mongodb+srv://kuquanghuy:quanghuy123456@cluster0.6mzug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


    client = init_connection()

    db=client[database_name]
    collection=db[database_name]


# Custom CSS for the buttons
st.markdown("""
<style>
    [role=radiogroup]{
        gap: 1rem;
    }
    div[data-testid="stSidebarContent"] {
    background-color: white;
    border:solid;
    border-color:#62CBEC32;
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
    .center {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width:200px;
    }
</style>
""", unsafe_allow_html=True)


#init
#color_scheme=dict({'🇮🇹Italy':'green',
#'🇵🇹Portugal':'red',
#'🇸🇰Slovakia':'blue',
#'🇷🇴Romania':'yellow'})


# Title and description
container1 = st.container()
placeholder = st.empty()
if (st.session_state.ws!==0):
    result=pd.DataFrame(list(collection.find()))
else:
    result=pd.DataFrame(pd.read_csv('quizz_answer.csv'))
with st.sidebar:
    if st.button('Refresh 🔄'):
        placeholder.empty()
with container1:
    st.html("<img src='https://raw.githubusercontent.com/kaheetonaa/streamlit_quizz_template_euth/refs/heads/main/asset/logo.png' class='center'/>")
    st.markdown(""" ___""")
    st.write(note,unsafe_allow_html=True)
    
    
    if 'question' in result:
    

        result0=result[result['question']==0].groupby(['selection','school']).count().reset_index()
        result1=result[result['question']==1].groupby(['selection','school']).count().reset_index()
        result2=result[result['question']==2].groupby(['selection','school']).count().reset_index()

        #st.write(result0)

        #color
        domain = ["🇮🇹Italy", "🇵🇹Portugal", "🇷🇴Romania", "🇸🇰Slovakia", "🇪🇸Spain"]
        range_ = ['#B9F3E3', '#F5716C', '#F5CC81', '#6799A3', '#F5996F']

        click = alt.selection_point(encodings=['color'])

        color = alt.condition(
        click,
        alt.Color('school:N').scale(domain=domain,range=range_),
        alt.value('lightgray')
    )

        chart1A = alt.Chart(result0,title='question 01').mark_bar().encode(
            x='selection',
            y='question',
            color=color
        ).add_params(
            click
        ).properties(height=300,width=300)

        chart1B = alt.Chart(result0).mark_bar(
        ).encode(
            y='selection',
            x='question',
            row='school',
            color=alt.condition(click, 'school', alt.value('lightgray'))
        ).add_params(
            click
        ).properties(height=300,width=300)
        chart1=alt.hconcat(chart1A,chart1B)
        #alt.condition(click, 'Origin', alt.value('lightgray'))
        chart2A= alt.Chart(result1,title='question 02').mark_bar(
        ).encode(
            x='selection',

            y='question',
            color=alt.condition(click, 'school', alt.value('lightgray'))
        ).add_params(
            click
        ).properties(height=300,width=300)

        chart2B = alt.Chart(result1).mark_bar(
        ).encode(
            y='selection',

            x='question',
            row='school',
            color=alt.condition(click, 'school', alt.value('lightgray'))
        ).add_params(
            click
        ).properties(height=300,width=300)
        chart2=alt.hconcat(chart2A,chart2B)

        chart3A= alt.Chart(result2,title='question 03').mark_bar(
        ).encode(
            x='selection',

            y='question',
            color=alt.condition(click, 'school', alt.value('lightgray'))
        ).add_params(
            click
        ).properties(height=300,width=300)

        chart3B = alt.Chart(result2).mark_bar(
        ).encode(
            y='selection',
            x='question',
            row='school',
            color=alt.condition(click, 'school', alt.value('lightgray'))
        ).add_params(
            click
        ).properties(height=300,width=300)
        chart3=alt.hconcat(chart3A,chart3B) 

        chart = alt.vconcat(chart1,chart2,chart3).configure(background='white',countTitle='number').configure_axis(
        labelFontSize=16,
        titleFontSize=16,
        labelFont='comfortaa',
        titleFont='comfortaa',
        ).configure_legend(
        labelFontSize=16,
        titleFontSize=16,
        labelFont='comfortaa',
        titleFont='comfortaa',
        ).configure_axisY(title=None).configure_headerRow(
        labelFont='comfortaa',
        labelFontSize=12,
        titleFont='comfortaa',
        titleFontSize=16
        ).configure_bar(size=30)
        st.altair_chart(chart,theme=None)
    else:
        st.write('No answers yet')
