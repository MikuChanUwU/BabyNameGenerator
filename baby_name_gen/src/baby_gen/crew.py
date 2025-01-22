from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool
from dotenv import load_dotenv

load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class BabyNameGen():
	"""AiNews crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# running ollama locally
	ollama_llm = LLM(
		model='ollama/llama3.2:3b',
		base_url='http://localhost:11434',
	)


	@tool('search_tool')
	def search(search_query: str):
		"""Search the web for information on a given topic"""
		response = SerperDevTool().run(search_query=search_query)
		return response
        
        
	search_tool = search
	# serper_dev_tool = SerperDevTool()
	scrape_website_tool = ScrapeWebsiteTool()
	file_writer_tool = FileWriterTool()

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def baby_name_retriever(self) -> Agent:
		return Agent(
			config=self.agents_config['baby_name_retriever'],
			tools=[self.search_tool],
			verbose=True,
			llm=self.ollama_llm,
			function_calling_llm=self.ollama_llm
		)

	@agent
	def baby_name_website_scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['baby_name_website_scraper'],
			tools=[self.scrape_website_tool],
			verbose=True,
			llm=self.ollama_llm
		)

	@agent
	def baby_name_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['baby_name_writer'],
			tools=[],
			verbose=True,
			llm=self.ollama_llm
		)

	@agent
	def file_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['file_writer'],
			tools=[self.file_writer_tool],
			verbose=True,
			llm=self.ollama_llm
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def retrieve_news_task(self) -> Task:
		return Task(
			config=self.tasks_config['retrieve_baby_names_task'],
		)

	@task
	def website_scrape_task(self) -> Task:
		return Task(
			config=self.tasks_config['scrape_baby_websites_task'],
			output_file='report.md'
		)

	@task
	def article_write_task(self) -> Task:
		return Task(
			config=self.tasks_config['baby_names_write_task'],
			output_file='report.md'
		)

	@task
	def file_write_task(self) -> Task:
		return Task(
			config=self.tasks_config['file_write_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AiNews crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential, # TODO: I wanna see whether a different process sequence would benefit baby name searching
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
