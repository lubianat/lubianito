# main.py
import streamlit as st
from agent import IterativeAgent
from llama_service import LlamaService

# Streamlit setup
st.title("Smart Photography Contest Search Agent")

# Llama Service Setup
llama_service = LlamaService()

# Initialize the agent
agent = IterativeAgent(llama_service=llama_service)

# Search query input
search_query = st.text_input("Enter a search query", "macro photography contests open for Brazilians")

# Perform the iterative search and display results
if st.button("Search"):
    with st.spinner("Searching for contests..."):
        results = agent.search_and_evaluate(search_query)
    
    if results:
        st.success(f"Found {len(results)} eligible contests!")
        for result in results:
            st.subheader(result['details'])
            st.write(f"Interpretation: {result['interpretation']}")
            st.write(f"Link: {result['url']}")
    else:
        st.warning("No contests found for the given query.")
