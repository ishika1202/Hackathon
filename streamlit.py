import streamlit as st

def main():
    st.title('Chatbot with Document Upload')
    st.write('Upload your documents and ask questions about them.')

    # Create a list to store chat messages
    chat_messages = []

    # Create a file uploader widget for users to upload files
    st.markdown(
        "<label style='display: block; font-size: 20px; margin-top: 20px;'>Upload Files:</label>",
        unsafe_allow_html=True
    )
    uploaded_files = st.file_uploader(
        label="",
        type=['pdf'],
        accept_multiple_files=True,
        key='uploader'
    )

    if uploaded_files:
        # Process the uploaded files and display their names
        st.write("Uploaded Files:")
        for file in uploaded_files:
            st.write(file.name)

        # Create a chatbox to ask questions about the documents
        st.markdown("<h2>Chatbox</h2>", unsafe_allow_html=True)
        user_question = st.text_input("You: ")
        if st.button("Ask"):
            # Implement the chatbot logic here (not included in this example)
            # For this simple frontend, we'll just echo back the user's question
            chat_messages.append(("You", user_question))
            # Add the chatbot's response here (modify as per your chatbot's logic)
            chat_messages.append(("Bot", "You asked: " + user_question))

    # Display the chat messages
    st.markdown("<h2>Chat</h2>", unsafe_allow_html=True)
    for sender, message in chat_messages:
        st.write(f"{sender}: {message}")

if __name__ == '__main__':
    main()
