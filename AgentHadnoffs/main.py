# uv run crewai crewai-tools litellm
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileWriterTool

def main():
    # -----------------------------
    # Define Agents (different models)
    # -----------------------------
    planner_agent = Agent(
        role="Planner",
        goal="Break the problem into clear development steps",
        backstory="You are a senior software architect.",
        llm="gpt-3.5-turbo",   # fast & cheap
        verbose=True
    )

    file_writer = FileWriterTool()

    developer_agent = Agent(
        role="Developer",
        goal="Write clean, correct Python code to a file",
        backstory="You are an expert Python developer.",
        llm="gpt-4o",          # stronger model for coding
        tools=[file_writer],   # tool enabled
        verbose=True
    )

    reviewer_agent = Agent(
        role="Reviewer",
        goal="Review code and suggest improvements",
        backstory="You are a strict code reviewer.",
        llm="gpt-3.5-turbo",
        verbose=True
    )

    # -----------------------------
    # Define Tasks (handoff happens via process)
    # -----------------------------
    planning_task = Task(
        description="Create a step-by-step plan to build a CLI calculator.",
        agent=planner_agent,
        expected_output="A clear development plan"
    )

    development_task = Task(
        description=(
            "Write a Python CLI calculator that supports add and subtract. "
            "Save the code to a file named `calculator.py` using the file writing tool."
        ),
        agent=developer_agent,
        expected_output="Python code saved to calculator.py"
    )

    review_task = Task(
        description="Review the calculator code and suggest improvements.",
        agent=reviewer_agent,
        expected_output="Improved or reviewed code"
    )

    # -----------------------------
    # Create the Crew
    # -----------------------------
    crew = Crew(
        agents=[planner_agent, developer_agent, reviewer_agent],
        tasks=[planning_task, development_task, review_task],
        process=Process.sequential,   # task handoff
        verbose=True
    )

    # -----------------------------
    # Run
    # -----------------------------
    result = crew.kickoff(
        inputs={"task": "Build a simple CLI calculator"}
    )

    print("\n===== FINAL OUTPUT =====\n")
    print(result)


if __name__ == "__main__":
    main()
