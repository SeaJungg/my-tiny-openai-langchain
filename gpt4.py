import streamlit as st
import openai
import re
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler


st.set_page_config(
    page_title='Private Chat',
    layout='wide'
)
st.title("PrivateChat")
api_key = st.secrets['OPENAI_API_KEY']
openai.api_key = api_key

chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)

# 자체api가 또 출시가 되었네.. https://github.com/hwchase17/chat-langchain/issues/39
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text=initial_text
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text+=token
        self.container.markdown(self.text) 


with st.form("form"):
    user_input = st.text_area("질문을 입력하세요", key='user_input')
    if 'user_input' not in st.session_state:
        st.session_state['질문을 입력하세요'] = user_input
    gpt4submit = st.form_submit_button("gpt-4에게 질문하기")


# Function for modifying filenames
def modify_fname(fname):
    illegal_chars = r"[\/\\\:\*\?\"\<\>\|]" # Add other characters here if needed
    return re.sub(illegal_chars, "", fname)

if gpt4submit and user_input :

    chat_box=st.empty() 
    stream_handler = StreamHandler(chat_box)
    chat = ChatOpenAI(max_tokens=25, streaming=True, callbacks=[stream_handler])
    response = chat([HumanMessage(content=user_input)])    
    llm_response = response.content

    # Save Q&A set into a txt file
    filename = modify_fname(user_input[:40]) + ".txt"
    with open('./history/' + filename, "w") as f:
        f.write("Question: " + user_input + "\n")
        f.write("Answer: " + llm_response + "\n")

    st.markdown("----")
else :
    st.write('질문을 확인하세요')
