from pydantic import BaseModel, Field, ConfigDict

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from core.httpx_client import HTTPClientBuilder

from typing import Any, List

class AgentConfigBase(BaseModel):
    """
    Base model for all agent-related configurations.
    
    Defines the common fields required across all agent types.
    """
    model_config = ConfigDict(extra="allow")

    name: str = Field(..., description="Name of the agent")
    model: str = Field(..., description="LLM model to use")
    system_prompt: str = Field(..., description="System prompt for the agent")
    
    instrument: bool = Field(default=True, description="Whether to enable instrumentation for the agent")


class ResultTool(BaseModel):
    """
    Configuration for the result tool used by an agent.
    
    Defines the function to process and validate agent outputs.
    """
    name: str = Field(..., description="Name of the result tool")
    func: Any = Field(..., description="Function to process agent results")
    expected_type: BaseModel = Field(..., description="Expected response type model")


class SimpleAgentConfig(AgentConfigBase):
    """
    Pydantic model representing a simple agent configuration.
    
    Extends the base configuration with tools and result processing.
    """
    tools: List[Any] = Field(default_factory=list, description="List of tools available to the agent")
    result_tool: ResultTool = Field(..., description="Tool used to process agent results")
    

class AgentFactory:
    """
    Factory class for creating different types of agents.
    
    Provides utilities to build properly configured agent instances.
    """
    
    @staticmethod
    def build_async_pydantic(agent_config: AgentConfigBase) -> Agent:
        """
        Builds an asynchronous Pydantic-powered agent based on the provided configuration.
        
        Args:
            agent_config: Configuration containing agent parameters
            
        Returns:
            Agent: A configured agent instance ready for use
            
        Raises:
            AssertionError: If any required configuration values are missing
        """
        import os
        
        _name = getattr(agent_config, 'name', None)
        _model = getattr(agent_config, 'model', None)
        _system_prompt = getattr(agent_config, 'system_prompt', None)
        _openai_provider_base_url = os.environ.get('OPENAI_PROVIDER_BASE_URL', None)
        _openai_provider_api_key = os.environ.get('OPENAI_PROVIDER_API_KEY', None)
        
        for required_value in [_name, _model, _system_prompt, _openai_provider_base_url, _openai_provider_api_key]:
            assert required_value is not None, f'ValueError: Missing `{required_value}` from ENV'
        
        httpx_client = HTTPClientBuilder.get_httpx_client()
        httpx_client.headers = {
            'X-Title': _name,
            'User-Agent': f'pydantic-ai/{_name}',
        }
        
        model = OpenAIModel(
            _model,
            provider=OpenAIProvider(
                base_url=_openai_provider_base_url,
                api_key=_openai_provider_api_key,
                http_client=httpx_client
            )
        )
        
        result_tool = getattr(agent_config, 'result_tool')
        res_tool_name = getattr(result_tool, 'name')
        
        agent = Agent(
            model=model,
            name=_name,
            tools=getattr(agent_config, 'tools'),
            instrument=getattr(agent_config, 'instrument'),
            result_tool_name=res_tool_name,
            result_type=str,  # type: ignore
            system_prompt=_system_prompt
        )
        
        res_tool_func = getattr(result_tool, 'func')
        agent.output_validator(res_tool_func)
        
        return agent


__all__ = ["AgentFactory", "SimpleAgentConfig", "AgentConfigBase", "ResultTool"]