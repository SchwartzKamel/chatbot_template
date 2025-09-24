# This file ensures 'app' is treated as a package by Python
# and explicitly exposes root_agent for the ADK loader.

from . import root_agent as _root_agent_module

root_agent = _root_agent_module.root_agent

__all__ = ["root_agent"]
