import backend.db_ops as dbops  
import backend.llm_ops as llm 
import streamlit as st

#Initialization of temp session variables 
st.session_state.chat_sessions = {}
st.session_state.session_count = 0

#Create the first session "Query 1" if no sessions exist
new_session_id = dbops.generate_session_id()
st.session_state.session_count += 1
new_session_name = f'Query {st.session_state.session_count}'
st.session_state.chat_sessions[new_session_id] = {
    "session_name": new_session_name,
    "chat_history": [],
}
st.session_state.selected_session = new_session_id

# Handle new query creation
with st.sidebar.title("Text2SQL Generator"):
    if st.sidebar.button('+ New Query'):
        new_session_id = dbops.generate_session_id()
        st.session_state.session_count += 1
        new_session_name = f'Query {st.session_state.session_count}'
        st.session_state.chat_sessions[new_session_id] = {
            "session_name": new_session_name,
            "chat_history": [],
        }
        st.session_state.selected_session = new_session_id

# Use a for loop to create buttons for session selection
for session_id, session_info in st.session_state.chat_sessions.items():
    if st.sidebar.button(session_info["session_name"]):
        st.session_state.selected_session = session_id

# Chat input
user_input = st.chat_input("Type your message here...", key="chat_input")
if user_input:
    with st.spinner("Generating response..."):
        # Generate response and store chat in Redis
        response = llm.generate_response(user_input, st.session_state.selected_session)
        # Update temp session chat history
        #st.session_state.chat_sessions[st.session_state.selected_session]["chat_history"].append((user_input, response))

# Display chat history for the selected session
if st.session_state.selected_session:
    # Getting chat_history_obj for session from Redis
    redis_history_obj = dbops.get_chat_history_obj(session_id)
    chat_history = redis_history_obj.messages
    print(chat_history)
    for user_input, bot_response in chat_history:
        with st.chat_message("User"):
            st.write(user_input)
        with st.chat_message("Assistant"):
            st.write(bot_response)