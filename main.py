import streamlit as st 
from database import update_review,add_questions,fetch_for_rev,del_entry,debug_dump
import datetime 

st.title("Revision Tracker")

menu=["Add questions","Review Questions","Delete Questions","Review Schedule"]
choice=st.sidebar.selectbox("Menu",menu)

if choice=="Add questions":
    st.subheader("Add a Question")

    question=st.text_input("Enter the question")
    description=st.text_area("Enter description/explanation/URL of the question(This is optional)")
    difficulty=st.selectbox("Select difficulty",["Easy","Medium","Hard"])

    if st.button("Add Question"):
        add_questions(question,difficulty,description)
        st.success("Succesfully added")

elif choice=="Review Questions":
    st.subheader("Revise a Question")

    questions=fetch_for_rev()
    if questions:
        for q in questions:
            id,ques,desc,_=q
            st.markdown(f"**ID:** {id}")
            st.markdown(f"**Question:** {ques}") 
            st.markdown(f"**Description:** {desc}")


            quality=st.radio(f"Rate your recall for this question (ID:{id})",[0,1,2,3,4,5],key=id)
            if st.button(f"Submit Review for the question ID: {id}"):
                update_review(quality,id)
                st.success("Review Updated") 
    else:
        st.info("No questions due for review today!")            
elif choice=="Delete Questions":
    st.subheader("Delete a Question")

    id=st.text_input("Enter the id the of the question you want to delete")

    if st.button("Delete Entry"):
        del_entry(id) 
        st.info("Entry Deleted")

elif choice=="Review Schedule":
    st.subheader("Review Schedule")

    questions = debug_dump()

    if questions:
        st.markdown("""
            <style>
                .ques_sty {
                    background-color:#242124;
                    padding: 16px;
                    border-radius: 12px;
                    margin-bottom: 12px;                
                }
            </style>
        """, unsafe_allow_html=True)

        for q in questions:
            try:
                id, ques, desc, added_date, next_rev_date = q
                st.markdown(f"""
                    <div class="ques_sty">
                        <strong>ID:</strong> {id}<br>
                        <strong>Added Date:</strong> {added_date}<br>
                        <strong>Next Review Date:</strong> {next_rev_date}<br>
                        <strong>Question:</strong> {ques}<br>
                        <strong>Description:</strong> {desc}
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error displaying question: {e}")
    else:
        st.info("No questions found.")





            






