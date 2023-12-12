import backend.util as util  
import backend.llm_ops as llm 
import streamlit as st

# Initialization of temporary session variables to manage chat sessions and counts
if 'chat_sessions' not in st.session_state:
    st.session_state['chat_sessions'] = {}  # Dictionary to hold chat session data
if 'session_count' not in st.session_state:
    st.session_state['session_count'] = 0  # Counter for the number of sessions created
if 'selected_session' not in st.session_state:
    st.session_state['selected_session'] = None  # Currently selected chat session
if 'session_log' not in st.session_state:
    st.session_state['session_log'] = {} # Dictionary to hold session logs

# Automatically create the first session if no sessions exist
if len(st.session_state.chat_sessions) == 0:
    new_session_id = util.generate_session_id()  # Generate a unique session ID
    st.session_state.session_count += 1  # Increment the session count
    # Naming the session using the session count
    new_session_name = f'Query {st.session_state.session_count}'
    # Storing the new session in the session dictionary
    st.session_state.chat_sessions[new_session_id] = {"session_name": new_session_name}
    st.session_state.selected_session = new_session_id  # Set the new session as selected

# Sidebar for additional features and session management
with st.sidebar:
    # Display the application logo in the sidebar
    st.sidebar.image(util.display_logo())
    st.sidebar.divider()  # Visual divider for better UI
    st.sidebar.header("🎯 Actions")

    # Button to create a new chat session
    if st.sidebar.button('➕ New Chat'): 
        new_session_id = util.generate_session_id()  # Generate a new unique session ID
        st.session_state.session_count += 1  # Increment the session count
        # Naming the new session
        new_session_name = f'Query {st.session_state.session_count}'
        # Storing the new session
        st.session_state.chat_sessions[new_session_id] = {"session_name": new_session_name}
        st.session_state.selected_session = new_session_id  # Set the new session as selected

    # Button to get insights from the current chat session
    if st.sidebar.button("💡 Get Insight" ):
        result = util.get_insights_from_pandas(st.session_state.selected_session)
        if result == None:
            st.warning("No chat history found.")  # Warning if no chat history is available
        else:
            # Display insights as popup notifications
            util.display_popup("Pandas Insights", result)
    # Button to show application logs
    if st.sidebar.button("📋 Show Logs"):
        util.display_popup("LLM Call Logs", st.session_state.session_log)
        
    st.sidebar.divider()  # Visual divider
    st.sidebar.header("💬 Chat Sessions")

# Loop to create buttons for each chat session in the sidebar
for session_id, session_info in st.session_state.chat_sessions.items():
    if st.sidebar.button(session_info["session_name"]):
        st.session_state.selected_session = session_id  # Update the selected session

# Chat input area
user_input = st.chat_input("Type your message here...", key="chat_input")
if user_input:
    with st.spinner('Generating response...'):
        # Generate response using the AI model and update the session state
        st.session_state.session_log = llm.generate_response(user_input, st.session_state.selected_session)

# Display the chat history for the selected session
if st.session_state.selected_session:
    # Retrieve the chat history object for the current session
    chat_history = util.get_chat_history_obj(st.session_state.selected_session).messages
    if chat_history:
        for chat_item in chat_history:
            # Display each chat message according to its type (human or assistant)
            if chat_item.type == 'human':
                with st.chat_message("User"): st.write(chat_item.content)
            else:
                with st.chat_message("Assistant"): st.write(chat_item.content)
