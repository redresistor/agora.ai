from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool,
	EXASearchTool
)
from agoraai.tools.custom_tool import ArxivSearcherTool
import hashlib
import random


search_tool = EXASearchTool()
arxiv_searcher = ArxivSearcherTool()

llm = LLM(
	model="openai/llama-3.2-3b-instruct-uncensored",
	base_url="http://localhost:1234/v1",
	# temperature=0.7,        # Higher for more creative outputs
	# timeout=120,           # Seconds to wait for response
	# max_tokens=4000,       # Maximum length of response
	# top_p=0.9,            # Nucleus sampling parameter
	# frequency_penalty=0.1, # Reduce repetition
	# presence_penalty=0.1,  # Encourage topic diversity
	# response_format={"type": "json"},  # For structured outputs
	# seed=42,
	api_key="n/a",
)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Agoraai():
	"""Agoraai crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			tools=[search_tool, arxiv_searcher], #, EXASearchTool()],
			llm=llm,
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
			llm=llm,
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		integer = random.randint(0, 100000)
		id = hashlib.md5(f"{self.tasks_config['reporting_task']['topic']}{str(integer)}".encode()).hexdigest() # generate some unique id based on the topic name.

		return Task(
			config=self.tasks_config['reporting_task'],
			output_file=f'report-{id}.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Agoraai crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
