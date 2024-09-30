from pymongo import MongoClient
import streamlit as st
import pandas as pd

def run():
    st.set_page_config(
        page_title="🌐 EuthMappers quizz result",
        page_icon="✅",
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
color_scheme=dict({'🇮🇹Italy':'green',
'🇵🇹Portugal':'red',
'🇸🇰Slovakia':'blue',
'🇷🇴Romania':'yellow'})
# Title and description
container1 = st.container()
result=pd.DataFrame(list(collection.find()))

with container1:
    st.html("<img src='https://raw.githubusercontent.com/kaheetonaa/streamlit_quizz_template_euth/refs/heads/main/asset/logo.png' class='center'/>")
    
result0=result[result['question']==0].groupby(['selection','school']).count().reset_index()
result1=result[result['question']==1].groupby(['selection','school']).count().reset_index()
result2=result[result['question']==2].groupby(['selection','school']).count().reset_index()

#color=[{i:color_scheme[i]} for i in result0['school']]
#st.write(len(color),len(result0['question']))
st.bar_chart(
    result0,
    y="question",
    x="selection",
    color='school'
)



#st.write(len(color),len(result0['question']))
st.bar_chart(
    result1,
    y="question",
    x="selection",
    color='school'
)
st.bar_chart(
    result2,
    y="question",
    x="selection",
    color='school'
)