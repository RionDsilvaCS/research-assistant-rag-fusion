import streamlit as st
from utils.chain import ChatWithOllama
import base64
import time

st.title("Research Assistant 🧑‍🔬")

def displayPDF(bytes_data, width):

    base64_pdf = base64.b64encode(bytes_data).decode("utf-8", 'ignore')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(width)} height={str(width*4/3)} type="application/pdf"></iframe>'

    st.markdown(pdf_display, unsafe_allow_html=True)

with st.sidebar:

    multi_flag = st.toggle('Multi Retrival')

    if 'pdf_ref' not in st.session_state:
        st.session_state.pdf_ref = None

    st.file_uploader("Choose a PDF file", type=('pdf'), key='pdf')
    if st.session_state.pdf:
        st.session_state.pdf_ref = st.session_state.pdf

    if st.session_state.pdf_ref:
        binary_data = st.session_state.pdf_ref.getvalue()
        displayPDF(bytes_data=binary_data, width=280)

chat_bot = ChatWithOllama(multi_retrival=multi_flag)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    start = time.time()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(chat_bot.GetResponse(prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})
    end = time.time()
    print(end - start)
    print(st.session_state.messages)
    