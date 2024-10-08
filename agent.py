# agent.py
import requests
from bs4 import BeautifulSoup
from google_scraper import GoogleScraper
from llama_service import LlamaService
import streamlit as st

class IterativeAgent:
    def __init__(self, llama_service):
        self.google_scraper = GoogleScraper()
        self.llama_service = llama_service
        self.search_history = []

    def search_and_evaluate(self, query, iterations=3):
        results = []
        for i in range(iterations):
            st.info(f"**Iteration {i+1}**: Searching for '{query}'")
            
            search_results = self.google_scraper.search(query)
            if not search_results:
                st.warning("No results found in this iteration.")
                continue

            st.write(f"**Found {len(search_results)} results**. Processing links...")
            results.extend(self.process_links(search_results))

            # Display intermediate results after each iteration
            self.display_intermediate_results(results)

            # Check if the user wants to stop the search
            if st.button("Stop Search"):
                st.warning("Search stopped by user.")
                break
            
            # Refine query based on evaluated results
            query = self.refine_search_query(results)
            st.info(f"Refining search query to: '{query}'")

        return results

    def process_links(self, links):
        contests = []
        progress = st.progress(0)  # Initialize a progress bar
        
        for idx, link in enumerate(links):
            progress.progress((idx + 1) / len(links))  # Update progress bar
            st.write(f"Processing {link}")
            
            contest_details = self.scrape_contest_details(link)
            if contest_details:
                interpretation = self.llama_service.interpret_contest(contest_details)
                st.write(f"Llama Interpretation: {interpretation}")
                
                if "Brazil" in interpretation:
                    contests.append({
                        'url': link,
                        'details': contest_details,
                        'interpretation': interpretation
                    })
                    st.success(f"Added contest from {link}")
                else:
                    st.info(f"Contest from {link} is not eligible.")
            else:
                st.warning(f"Failed to scrape {link}.")
        
        return contests

    def scrape_contest_details(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('h1').text if soup.find('h1') else "Unknown Title"
            content = soup.find('p').text if soup.find('p') else "No details available"
            
            return f"{title} - {content}"
        except Exception as e:
            st.error(f"Error scraping {url}: {e}")
            return None

    def refine_search_query(self, results):
        if results:
            st.info("Refining query based on successful results...")
            return "macro nature photography contests open for Brazilians"
        else:
            st.info("No successful results. Refining search query more broadly...")
            return "photography contests open for Brazilians"

    def display_intermediate_results(self, results):
        st.subheader("Intermediate Results:")
        for result in results:
            st.write(f"Contest: {result['details']}")
            st.write(f"Interpretation: {result['interpretation']}")
            st.write(f"Link: {result['url']}")
            st.write("---")
