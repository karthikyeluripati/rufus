# src/frontend/app.py
import streamlit as st
import asyncio
import os
from typing import Dict, Any
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state
if 'client' not in st.session_state:
    try:
        from rufus import RufusClient
        api_key = os.getenv("RUFUS_API_KEY")
        if not api_key:
            st.error("Please set RUFUS_API_KEY in your .env file")
            st.stop()
        st.session_state.client = RufusClient(api_key=api_key)
    except ImportError as e:
        st.error(f"Failed to import required modules: {str(e)}")
        st.error("Please install required packages using: pip install -r requirements.txt")
        st.stop()

def display_json_tree(data: Dict):
    """Display JSON data in a collapsible tree structure."""
    if isinstance(data, dict):
        for key, value in data.items():
            with st.expander(f"▶ {key}", expanded=True):
                display_json_tree(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            with st.expander(f"▶ Item {i+1}", expanded=True):
                display_json_tree(item)
    else:
        st.write(data)

def main():
    st.title("Rufus Web Scraper")
    
    # Scraping form
    with st.form("scraping_form"):
        url = st.text_input(
            "Website URL",
            "https://example.com",
            help="Enter the website URL you want to scrape"
        )
        
        instructions = st.text_area(
            "Extraction Instructions",
            "Extract main content and important information",
            help="Describe what information you want to extract"
        )
        
        with st.expander("Advanced Options"):
            col1, col2 = st.columns(2)
            with col1:
                max_depth = st.slider(
                    "Maximum Crawl Depth",
                    1, 5, 2,
                    help="How many levels deep to crawl"
                )
            with col2:
                view_mode = st.selectbox(
                    "View Mode",
                    ["JSON", "Formatted", "Tree"],
                    help="Choose how to display the results"
                )
        
        submitted = st.form_submit_button("Start Extraction")
    
    if submitted:
        try:
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                st.error("Please enter a valid URL starting with http:// or https://")
                return
            
            # Show progress
            progress = st.progress(0)
            status = st.empty()
            
            async def run_scraping():
                status.text("Initializing scraper...")
                progress.progress(10)
                
                results = await st.session_state.client.scrape(
                    url=url,
                    instructions=instructions,
                    max_depth=max_depth
                )
                
                progress.progress(100)
                status.text("Extraction completed!")
                return results
            
            # Execute scraping
            with st.spinner("Processing website..."):
                results = asyncio.run(run_scraping())
            
            # Display results
            st.success("Extraction completed successfully!")
            
            # Show statistics
            st.subheader("Extraction Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pages Crawled", results["metadata"]["pages_crawled"])
            with col2:
                st.metric("Content Items", results["metadata"]["content_items"])
            with col3:
                st.metric("Processing Time", results["metadata"]["processing_time"])
            
            # Show content based on view mode
            st.subheader("Extracted Content")
            
            if view_mode == "JSON":
                # Show raw JSON with syntax highlighting
                st.code(json.dumps(results, indent=2), language="json")
                
            elif view_mode == "Tree":
                # Show collapsible JSON tree
                display_json_tree(results)
                
            else:  # Formatted view
                if results["content"].get("title"):
                    st.markdown(f"### {results['content']['title']}")
                
                if results["content"].get("headings"):
                    st.markdown("### Headings")
                    for heading in results["content"]["headings"]:
                        st.markdown(f"- {heading}")
                
                if results["content"].get("paragraphs"):
                    st.markdown("### Content")
                    for para in results["content"]["paragraphs"]:
                        st.markdown(para)
                        st.markdown("---")
            
            # Add copy button for JSON
            st.text_area(
                "Raw JSON (Copy)",
                value=json.dumps(results, indent=2),
                height=100,
                help="Copy the raw JSON data"
            )
            
            # Download options
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "Download JSON",
                    data=json.dumps(results, indent=2),
                    file_name=f"rufus_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            with col2:
                # Export as CSV option
                if st.button("Export as CSV"):
                    # Convert to CSV format
                    csv_data = "Type,Content\n"
                    for item_type, items in results["content"].items():
                        if isinstance(items, list):
                            for item in items:
                                csv_data += f"{item_type},{item.replace(',', ' ')}\n"
                        else:
                            csv_data += f"{item_type},{str(items).replace(',', ' ')}\n"
                    
                    st.download_button(
                        "Download CSV",
                        data=csv_data,
                        file_name=f"rufus_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
        except Exception as e:
            st.error(f"Extraction failed: {str(e)}")
            st.error("Please check your inputs and try again")
            st.exception(e)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Rufus Web Scraper",
        page_icon="🌐",
        layout="wide"
    )
    main()