import streamlit as st
import os
from dotenv import load_dotenv
import time
from datetime import datetime
from agents import build_crew

# Load API keys from .env
load_dotenv()


# Streamlit UI setup
st.set_page_config(page_title="AI Fact Checker", page_icon="🔍", layout="wide")
st.title("🔍 AI Fact Checker")
st.markdown("Analyze the factual accuracy of a statement, website content, or YouTube video.")

# Input box
user_input = st.text_area("Paste a statement, website URL, or YouTube link here:", height=150)

# Detect input type
def detect_input_type(text):
    if not text.strip():
        return None
    if "youtube.com" in text or "youtu.be" in text:
        return "youtube"
    elif text.startswith("http"):
        return "url"
    return "statement"

input_type = detect_input_type(user_input)

# Run analysis
if st.button("🔍 Analyze"):
    if not os.environ["OPENAI_API_KEY"] or not os.environ["SERPER_API_KEY"]:
        st.error("❌ Missing API keys. Check your .env file.")
    elif not user_input.strip():
        st.warning("⚠️ Please enter valid input.")
    else:
        st.info("🤖 Running fact-checking analysis...")
        try:
            # Prepare input for Crew
            if input_type == "statement":
                input_data = {"input_statement": user_input}
            elif input_type == "url":
                input_data = {"input_url": user_input}
            elif input_type == "youtube":
                input_data = {"input_youtube_url": user_input}
            else:
                st.error("❌ Could not detect input type.")
                st.stop()

            # Build and run crew
            crew = build_crew(input_data)
            result = crew.kickoff(inputs=input_data)

            # Show results
            st.markdown("---")
            st.subheader("📊 Final Verdict")

            if isinstance(result, list):
                for task in result:
                    agent = getattr(task, "agent", "Unknown Agent")
                    description = getattr(task, "description", "No description")
                    raw = getattr(task, "raw", str(task))

                    st.markdown(f"**🧠 Agent:** `{agent}`")
                    st.markdown(f"**📌 Task:** {description}")
                    st.text_area("Result", raw.strip(), height=300)
                    st.markdown("---")
            else:
                st.text_area("Result", str(result).strip(), height=400)

            # Download button
            report_content = ""
            if isinstance(result, list):
                for task in result:
                    report_content += f"Agent: {getattr(task, 'agent', 'Unknown')}\n"
                    report_content += f"Task: {getattr(task, 'description', '')}\n"
                    report_content += f"Result:\n{getattr(task, 'raw', str(task))}\n\n"
            else:
                report_content = str(result)

            st.download_button(
                label="💾 Download Full Report",
                data=report_content,
                file_name=f"fact_check_{int(time.time())}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"❌ Error during analysis: {e}")
            st.stop()

# Footer
st.markdown("---")
st.markdown("<center style='color: gray;'>AI Fact Checker — Developed by Beaula | Powered by CrewAI · OpenAI · Streamlit</center>", unsafe_allow_html=True)
