import streamlit as st
def main():
    st.set_page_config(page_title = "chat with multiple PDFs", page_icon = ":books")
    st.header("chat with multiple pdfs :books:")
    st.text_input("Ask a question about your documents:")

    with st.sidebar:
        st.subheader("your documents")
        st.file_uploader("upload your pdfs here and click process")
        st.button("process")

if __name__ == '__main__':
    main()