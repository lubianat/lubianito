import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import streamlit as st
import pandas as pd
import yaml
import time

# Llama Service to evaluate text
class LlamaService:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("andrijdavid/Llama-3-2B-Base")
        self.model = AutoModelForCausalLM.from_pretrained("andrijdavid/Llama-3-2B-Base")
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def interpret_text(self, text):
        prompt = f"Here is some text: {text}. Is it a macro photography contest open for Brazilians?"
        output = self.generator(prompt, max_length=100, num_return_sequences=1)
        return output[0]['generated_text']

# Scraper to extract text from websites
class WebScraper:
    def __init__(self):
        pass

    def scrape_page(self, url):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract all text from the webpage
            text = soup.get_text(separator=' ', strip=True)
            return text
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return None

# Main Agent to search, evaluate, and record results
class SmartSearchAgent:
    def __init__(self, llama_service, scraper, output_file="results.tsv", keyword_criteria="Brazil"):
        self.llama_service = llama_service
        self.scraper = scraper
        self.output_file = output_file
        self.keyword_criteria = keyword_criteria
        self.results = []

    def search_and_evaluate(self, urls):
        for url in urls:
            print(f"Processing {url}")
            text = self.scraper.scrape_page(url)
            if text:
                # Option 1: Simple keyword matching
                if self.keyword_criteria.lower() in text.lower():
                    self.record_result(url, text, "Keyword match")
                # Option 2: Advanced Llama model evaluation
                else:
                    interpretation = self.llama_service.interpret_text(text)
                    if "Brazil" in interpretation:
                        self.record_result(url, text, interpretation)
            time.sleep(1)  # Sleep to avoid being flagged by servers

    def record_result(self, url, text, evaluation):
        print(f"Recording match: {url}")
        self.results.append({
            'url': url,
            'evaluation': evaluation,
            'text': text[:200]  # Shorten text for storage/display
        })
        self.save_to_file()

    def save_to_file(self):
        # Save the results to TSV format
        df = pd.DataFrame(self.results)
        df.to_csv(self.output_file, sep='\t', index=False)

    def save_to_yaml(self):
        with open(self.output_file.replace('.tsv', '.yaml'), 'w') as file:
            yaml.dump(self.results, file)

    def refine_query(self, query):
        # Refine the query for further searches, if needed
        return query + " more results"

# Streamlit interface to run the search agent interactively
def main():
    # Initialize services
    llama_service = LlamaService()
    scraper = WebScraper()
    agent = SmartSearchAgent(llama_service=llama_service, scraper=scraper, output_file="results.tsv")

    st.title("Smart Web Search Agent")
    query_input = st.text_input("Enter a set of URLs (comma-separated) or a search query", "")
    
    # Prepare the input URLs or queries
    urls = []
    if "," in query_input:
        urls = [url.strip() for url in query_input.split(",")]
    else:
        query = query_input
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num=10"
        urls = [search_url]

    if st.button("Run Search"):
        with st.spinner("Running the search..."):
            agent.search_and_evaluate(urls)
        st.success(f"Search completed. Results saved to {agent.output_file}")

        # Option to save as YAML
        if st.button("Save as YAML"):
            agent.save_to_yaml()
            st.success("Results saved as YAML.")

if __name__ == "__main__":
    main()
