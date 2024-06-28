from dataclasses import dataclass


@dataclass
class ApiEndpoints:
    PING: str = "/ping"
    HEALTH: str = "/health"
    ASSISTANTS: str = "/assistants"
    AGENT_ASSISTANTS: str = "/agent-assistants"


endpoints = ApiEndpoints()
