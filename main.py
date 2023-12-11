import backend.db_ops as dbops  
import backend.llm_ops as llm 
import streamlit as st

#Initialization of temp session variables 
if 'chat_sessions' not in st.session_state:
    st.session_state['chat_sessions'] = {}
if 'session_count' not in st.session_state:
    st.session_state['session_count'] = 0
if 'selected_session' not in st.session_state:
    st.session_state['selected_session'] = None

chat_history =  dbops.get_chat_history_obj( '*' )

#Create the first session "Query 1" if no sessions exist
if len(st.session_state.chat_sessions) == 0:
    new_session_id = dbops.generate_session_id()
    st.session_state.session_count += 1
    new_session_name = f'Query {st.session_state.session_count}'
    st.session_state.chat_sessions[new_session_id] = {"session_name": new_session_name}
    st.session_state.selected_session = new_session_id

# Handle new query creation
with st.sidebar.title("Text2SQL Generator"):
    if st.sidebar.button('+ New Query'):
        new_session_id = dbops.generate_session_id()
        st.session_state.session_count += 1
        new_session_name = f'Query {st.session_state.session_count}'
        st.session_state.chat_sessions[new_session_id] = {"session_name": new_session_name}
        st.session_state.selected_session = new_session_id

# Use a for loop to create buttons for session selection
for session_id, session_info in st.session_state.chat_sessions.items():
    if st.sidebar.button(session_info["session_name"]):
        st.session_state.selected_session = session_id

# Chat input
user_input = st.chat_input("Type your message here...", key="chat_input")
if user_input:
    with st.spinner('Generating response...'):
        # Generate response and store chat in Redis
        _ = llm.generate_response(user_input, st.session_state.selected_session)

# Display chat history for the selected session
if st.session_state.selected_session:
    # Getting chat_history_obj for session from Redis
    chat_history = dbops.get_chat_history_obj(session_id).messages
    if chat_history:
        for chat_item in chat_history:
        # Check the type of the chat item and display accordingly
            if chat_item.type == 'human':
                # Assuming 'content' is the attribute that holds the message
                with st.chat_message("User"):st.write(chat_item.content)
            else:
                with st.chat_message("Assistant"):st.write(chat_item.content)
            