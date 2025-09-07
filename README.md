# AI-Fact-Checker-using-CREWAI
# 🕵️ FactCheck

FactCheck is a Python-based tool that automatically **summarizes, verifies, and generates fact-checking reports** from different sources of information.  
It is designed to help researchers, journalists, and developers evaluate the credibility of content.

---

## ✨ Features
- **Text Verification** → Input a text statement and get a summary + fact-check verdict.  
- **Web URL Analysis** → Extract content from web pages, summarize, and check for factual accuracy.  
- **YouTube Fact-Checking** → Retrieve transcripts, analyze content, and generate reports even when captions are limited.  
- **Reports** → Generate detailed analysis with verdicts, supporting evidence, and explanations.  
- **Modular Design** → Easy to extend with more sources or fact-checking models.  

---

## 📂 Project Structure
factcheck/
├── pyproject.toml # Project metadata & dependencies (Poetry/PDM)
├── req.txt # Python dependencies list
├── src/ # Main application source code
│ ├── factcheck/ # Core modules
│ ├── app.py # Streamlit web app
│ ├── main.py # CLI entry point
│ └── tools/ # Utility & helper functions
├── .idea/ # IDE configs (ignore in GitHub)
├── .venv/ # Local virtual environment (ignore in GitHub)


## 🛠️ Installation

Clone the repository:
```bash
git clone https://github.com/your-username/factcheck.git
cd factcheck
Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Install dependencies:

pip install -r req.txt
Or if you are using Poetry:

poetry install
▶️ Usage
CLI (Command Line)
Run the main fact-checker:

python -m factcheck.main "Your text or URL here"
Streamlit Web App
Launch the web interface:

streamlit run factcheck/src/factcheck/app.py
📊 Example
Input:
bash
Copy code
python -m factcheck.main "KCR is the Chief Minister of Andhra Pradesh."
Output:
pgsql
Copy code
🎯 VERDICT: ❌ FALSE
📖 Report: K. Chandrashekar Rao (KCR) is associated with Telangana, not Andhra Pradesh. 
The current CM of Andhra Pradesh is Y. S. Jagan Mohan Reddy.
🤝 Contributing
Contributions are welcome! Please fork the repository and open a pull request with improvements.

🔄 Workflow
flowchart TD
    A[Input Source] --> B{Type?}
    B -->|Text Statement| C[Summarizer + Fact Checker]
    B -->|Web URL| D[Web Scraper + Analyzer]
    B -->|YouTube URL| E[Transcript Extractor + Analyzer]
    
    C --> F[Fact Verification Engine]
    D --> F
    E --> F
    
    F --> G[Generate Report]
    G --> H[Output Verdict + Explanation]
  
