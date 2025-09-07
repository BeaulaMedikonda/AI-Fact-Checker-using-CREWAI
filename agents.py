from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from tools.youtube_caption import youtube_caption_tool

search_tool = SerperDevTool()

def build_crew(inputs):
    input_statement = inputs.get("input_statement", "")
    input_url = inputs.get("input_url", "")
    input_youtube = inputs.get("input_youtube_url", "")

    fact_researcher = Agent(
        role="Fact Researcher",
        goal="Use tools and reasoning to gather evidence and facts.",
        backstory="You are a highly reliable fact researcher skilled at using web and video tools.",
        tools=[search_tool, youtube_caption_tool],
        verbose=True,
    )

    fact_analyst = Agent(
        role="Fact Analyst",
        goal="Analyze the transcript and evidence to give a verdict.",
        backstory="Expert in evaluating factual accuracy based on given transcripts and sources.",
        tools=[],
        verbose=True,
    )

    tasks = []

    if input_statement:
        tasks.append(Task(
            description=f"Fact-check this claim: '{input_statement}' using web search.",
            expected_output="Verdict (TRUE/FALSE/MIXED) with explanation and sources.",
            agent=fact_researcher
        ))

    elif input_url:
        tasks.append(Task(
            description=f"Summarize and fact-check the content from this webpage: {input_url}.",
            expected_output="Summary + Verdict (TRUE/FALSE/MIXED) with explanation and sources.",
            agent=fact_researcher
        ))

    elif input_youtube:
        # Task 1: Get transcript
        tasks.append(Task(
            description=f"Use your tool to extract and return the full transcript from this YouTube video: {input_youtube}.",
            expected_output="Full transcript of the video.",
            agent=fact_researcher
        ))
        # Task 2: Fact-check based on transcript
        tasks.append(Task(
            description="Using the transcript, analyze the video's key factual claims and give a verdict (TRUE/FALSE/MIXED) with reasoning.",
            expected_output="Verdict and explanation based on transcript.",
            agent=fact_analyst
        ))

    return Crew(
        agents=[fact_researcher, fact_analyst],
        tasks=tasks,
        process=Process.sequential
    )
