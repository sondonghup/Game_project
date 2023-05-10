import streamlit as st
from streamlit_chat import message
import os
import openai
from dataset import make_dataset
from inference import chat
import argparse

openai.api_key = os.environ["openai_api_key"]

data = make_dataset('./data/npc_data_2/npc_data_list.tsv')

st.title('MAPLE NPC CHAT')
st.info('choose npc what you wants to talk with! ')

npc_name = st.selectbox('choice npc!', ('나인하트', '주먹펴고 일어서', '지그문트'))


if 'npc' not in st.session_state:
    st.session_state.npc = ''

if st.session_state.npc != npc_name:
    st.session_state.npc = npc_name
    st.session_state.history = []
    user_input = ''

npc_data = data.npc_load(npc_name)
chat = chat(npc_data, npc_name)

if 'history' not in st.session_state:
    st.session_state.history = []

user_input = st.text_input('input : ')
user_input_prompt =  user_input + f'\n{npc_name} : '
response = chat.npc_chat(user_input_prompt)

st.session_state.history.append({"message" : user_input, "is_user" : True})
st.session_state.history.append({"message" : response})

for chat in st.session_state.history:
    message(**chat)
    