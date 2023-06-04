import pathlib
import base64
import streamlit as st
from pathlib import Path
import process

st.title("PDF Question Answer")

# check directory
SAVE_FOLDER = './assets'
pathlib.Path(SAVE_FOLDER).mkdir(parents=True, exist_ok=True) 

def display_pdf(file):
	with open(file, "rb") as f:
		base64_pdf = base64.b64encode(f.read()).decode('utf-8')
	pdf_display =  F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
	st.markdown(pdf_display, unsafe_allow_html=True)

# Input file upload
pdf_uploaded = st.file_uploader(label = "Upload PDF File", type=["pdf"])

if pdf_uploaded:
	save_path = Path(SAVE_FOLDER, pdf_uploaded.name)
	with open(save_path, mode='wb') as w:
		w.write(pdf_uploaded.getvalue())

	if save_path.exists():
		st.success(f'File {pdf_uploaded.name} is successfully saved!')
		display_pdf(f'{SAVE_FOLDER}/{pdf_uploaded.name}')

		# Display input Question
		st.markdown("**Please fill the below form :**")
		with st.form(key="Form :", clear_on_submit = False):
			question_input      = st.text_input('Question : ')
			token_openai_input  = st.text_input('Token OpenAI : ')
			submit_btn = st.form_submit_button(label='Submit')

		if submit_btn:
			answer = process.main_process(
						pdf_path=f'{SAVE_FOLDER}/{pdf_uploaded.name}',
						question= question_input,
						openai_key=token_openai_input
					)
			st.markdown("Answer : ")
			st.markdown(answer)