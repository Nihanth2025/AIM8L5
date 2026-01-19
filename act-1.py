import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import re
import io
import config


client=genai.Client(api_key=config.GEMINI_API_KEY)


def run_ai_teaching_assistant():
    st.title("AI Teaching Assistant")
    st.write("Ask me anything about various subjects, and I'll provide an insightful answer.")

    if "history_ata" not in st.session_state:
        st.session_state.history_ata=[]
    

    col_clear, col_export=st.columns([1,2])

    with col_clear:
        if st.button("Clear Conversation", key="clear_ata"):
            st.session_state.history_ata=[]
    
    with col_export:
        if st.session_state.history_ata:
            export_text= ""
            for idx, qa in enumerate(st.session_state.history_ata, start=1):
                export_text += f"Q{idx}: {qa['question']}\n"
                export_text += f"A{idx}: {qa['answer']}\n\n"

                bio=io.BytesIO()
                bio.write(export_text.encode("utf-8"))
                bio.seek(0)

                st.download_button(
                    label="Export Chat history",
                    data=bio,
                    file_name="AI_Taching_Assistant_Conversation.txt",
                    mime="text/plain",
                )

    user_input=st.text_input("Enter your question here:", key="input_ata")

    if st.button("Ask", key="ask_ata"):
        if user_input.strip():
            with st.spinner("Generating AI response..."):
                response=generate_response(user_input.strip(), temperature=0.3)
            st.session_state.history_ata.append({"question": user_input.strip(), "answer": response})
            st.experimental_rerun()
        else:
            st.warning("Please enter a question before cliking Ask.")
    

    st.markdown("### Conversation History")
    for idx, qa in enumerate(st.session_state.history_ata, start=1):
        st.markdown(f"**Q{idx}:** {qa['question']}")
        st.markdown(f"**A{idx}:** {qa['answer']}")


def run_math_master_mind():
    st.title("Math Mastermind")
    st.write("**Your Expert Mathematical Problem solver** - From basic arithmetic to advanced calulus. I'll solve any math problem with detailed step-by-step explanations!")

    if "history_mm" not in st.session_state:
        st.session_state.history_mm=[]
    if "input_key_mm" not in st.session_state:
        st.session_state.input_key_mm=0
    
    col_clear, col_expert=st.columns([1,2])

    with col_clear:
        if st.button("Clear conversation", key="clear_mm"):
            st.session_state.history_mm=[]
            st.experimental_rerun()
    
    with col_expert:
        if st.session_state.history_mm:
            export_text= ""
            for idx, qa in enumerate(st.session_state.history_ata, start=1):
                export_text += f"Q{idx}: {qa['question']}\n"
                export_text += f"A{idx}: {qa['answer']}\n\n"

                bio=io.BytesIO()
                bio.write(export_text.encode("utf-8"))
                bio.seek(0)

                st.download_button(
                    label="Export Math Solutions",
                    data=bio,
                    file_name="Math_Mastermind_Solutions.txt",
                    mime="text/plain",
                )
    
    with st.form(key="math_form", clear_on_submit=True):
        user_input=st.text_area(
            "Enter your math problem here",
            height=100,
            placeholder="Example: Solve x + 5x + 6 = 0 or Find the integral of 2x + 3",
            key=f"user_input_{st.session_state.input_key_mm}"
        )

        col1, col2=st.columns([3,1])
        with col1:
            submitted=st.form_submit_button("Solve Problem")
        with col2:
            difficulty= st.selectbox("Level", ["Basic", "Intermediate", "Advanced"], index=1)

        if submitted and user_input.strip():
            enhanced_prompt=f"[{difficulty} Level] {user_input.strip()}"
            with st.spinner("Analyzing and solving your math problem..."):
                response= generate_math_response(enhanced_prompt)
            st.session_state.history_mm.insert(0, {
                "question": user_input.strip(),
                "answer": response,
                "difficulty":difficulty
            })
            st.session_state.input_key_mm +=1
            st.experimental_rerun()
        elif submitted and not user_input.strip():
            st.warning("Please enter a math problem before clicking Solve problem.")
    
    if st.session_state.history_mm:
        st.markdown("### Solution History (Latest First)")
        for idx, qa in enumerate(st.session_state.history_mm):
            question_num=len(st.session_state.history_mm) - idx
            difficulty_badge=f"[{qa.get('difficulty', 'N/A')}]"
            st.markdown(f"**Problem {question_num} {difficulty_badge}:** {qa['question']}")
            st.markdown(f"**Solution {question_num}: **\n{qa['answer']}")