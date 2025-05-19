import os
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

def call_agent(agent: Agent, message_text: str, *, api_key=None, vertexai=None, project=None, location=None) -> str:
    if api_key is None:
        api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API key não fornecida! Defina a variável de ambiente GOOGLE_API_KEY ou passe api_key explicitamente.")
    # Garante que a variável de ambiente está definida antes de criar o Runner
    os.environ["GOOGLE_API_KEY"] = api_key

    session_service = InMemorySessionService()
    session_service.create_session(
        app_name=agent.name, user_id="user1", session_id="session1"
    )
    runner_kwargs = {"agent": agent, "app_name": agent.name, "session_service": session_service}
    # Não passa api_key diretamente para Runner

    runner = Runner(**runner_kwargs)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])
    final_response = ""
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text is not None:
                    final_response += part.text
                    final_response += "\n"
    return final_response.strip()
