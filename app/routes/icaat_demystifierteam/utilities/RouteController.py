"""
Author: Mihai Criveti, Santhana Krishnan, Thomas Chang, Kasra Amirtahmasebi
Description: Autogen Integration
"""

import inspect
from functools import wraps
from fastapi import HTTPException
from app.routes.icaat_demystifierteam.utilities.Helper import ConfigUtility
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def getRouteFlag(agent_name):
    configUti = ConfigUtility()
    agent_config = configUti.get_agent_config(agent_name=agent_name)[0]
    route_enabled = agent_config.get("route_enabled")
    logger.debug(f" {agent_name} is enabled : {route_enabled}")
    return route_enabled


def validateAgentIsEnabled(agent_name, resolver=getRouteFlag):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            should_allow_route = resolver(agent_name)
            if should_allow_route.lower() == "false":
                raise HTTPException(status_code=400, detail="Route not enabled.")

            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator