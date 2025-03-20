#!/usr/bin/env python3
"""
eClass MCP Server

This module implements a Model Context Protocol (MCP) server for interacting with eClass.
It provides tools and resources for authenticating with eClass and retrieving course information.
"""

import os
import sys
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

# Import MCP SDK
from mcp.server.fastmcp import FastMCP
import mcp.types as types

# Import our eClass client
from eclass_client import EClassClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('eclass_mcp_server')

# Define app context
@dataclass
class AppContext:
    """Application context with initialized resources."""
    eclass_client: Optional[EClassClient] = None


# Define lifespan management
@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context."""
    # Initialize on startup
    logger.info("Initializing eClass MCP Server")
    
    # Create app context
    app_ctx = AppContext()
    
    # Store it for global access
    if hasattr(mcp, "_app_context"):
        del mcp._app_context
    mcp._app_context = app_ctx
    
    try:
        yield app_ctx
    finally:
        # Cleanup on shutdown
        logger.info("Shutting down eClass MCP Server")
        if app_ctx.eclass_client and app_ctx.eclass_client.logged_in:
            logger.info("Logging out active session")
            app_ctx.eclass_client.logout()


# Create the MCP server with lifespan management
mcp = FastMCP(
    "eClass MCP Server",
    lifespan=app_lifespan,
    dependencies=["requests", "beautifulsoup4", "python-dotenv"]
)

# Add a method to get the lifespan context from anywhere
def get_lifespan_context():
    """Access the current lifespan context."""
    if not hasattr(mcp, "_app_context"):
        # Create a placeholder for first initialization
        mcp._app_context = AppContext()
    return mcp._app_context


# ----- Resources -----

@mcp.resource("course://list")
def get_course_list() -> str:
    """
    Returns a list of enrolled courses for the authenticated user.
    
    Returns:
        A formatted markdown list of courses or an error message.
    """
    app_ctx = get_lifespan_context()
    
    if not app_ctx.eclass_client or not app_ctx.eclass_client.logged_in:
        return "Error: Not logged in to eClass. Please use the login tool first."
    
    courses = app_ctx.eclass_client.get_courses()
    
    if not courses:
        return "No courses found."
    
    courses_text = "# Your eClass Courses\n\n"
    for i, course in enumerate(courses, 1):
        courses_text += f"{i}. [{course['name']}]({course['url']})\n"
    
    return courses_text


# ----- Tools -----

@mcp.tool()
def login(random_string: str = "") -> str:
    """
    Log in to eClass using credentials from .env file.
    
    Returns:
        A message indicating whether login was successful
    """
    app_ctx = get_lifespan_context()
    
    # Initialize client if not already initialized
    if not app_ctx.eclass_client:
        app_ctx.eclass_client = EClassClient()
        logger.info("Initialized eClass client")
    
    # Log in using environment variables only
    try:
        logger.info("Attempting to log in using environment variables")
        success = app_ctx.eclass_client.login(None, None)  # This will use env vars
        
        if success:
            logger.info("Login successful")
            return "Successfully logged in to eClass using credentials from environment variables."
        else:
            logger.error("Login failed")
            return "Login failed. Please check your credentials in the .env file."
    except ValueError as e:
        logger.error(f"Login error: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return f"Unexpected error during login: {str(e)}"


@mcp.tool()
def logout(random_string: str = "") -> str:
    """
    Log out from eClass.
    
    Returns:
        A message indicating whether logout was successful
    """
    app_ctx = get_lifespan_context()
    
    if not app_ctx.eclass_client or not app_ctx.eclass_client.logged_in:
        return "Not logged in."
    
    logger.info("Logging out from eClass")
    success = app_ctx.eclass_client.logout()
    
    if success:
        return "Successfully logged out from eClass."
    else:
        return "Logout failed."


@mcp.tool()
def get_courses(random_string: str = "") -> str:
    """
    Get a formatted list of enrolled courses as text.
    
    Returns:
        A formatted string listing all enrolled courses
    """
    app_ctx = get_lifespan_context()
    
    if not app_ctx.eclass_client or not app_ctx.eclass_client.logged_in:
        return "Error: Not logged in to eClass. Please use the login tool first."
    
    logger.info("Fetching courses for text display")
    courses = app_ctx.eclass_client.get_courses()
    
    if not courses:
        return "No courses found."
    
    courses_text = "Your eClass Courses:\n\n"
    for i, course in enumerate(courses, 1):
        courses_text += f"{i}. {course['name']}\n"
    
    return courses_text


@mcp.tool()
def authstatus(random_string: str = "") -> str:
    """
    Get the current authentication status as a simple string.
    
    Returns:
        A string indicating the authentication status
    """
    app_ctx = get_lifespan_context()
    
    if not app_ctx.eclass_client:
        return "Not initialized. Please use the login tool first."
    
    if app_ctx.eclass_client.logged_in:
        return "Logged in to eClass"
    else:
        return "Not logged in to eClass"


# ----- Prompts -----

@mcp.prompt()
def login_prompt() -> str:
    """
    Create a prompt for logging in to eClass.
    """
    return """
    I need to log in to my eClass account. Please help me with the login process.
    
    Note: You can use the login tool to help me authenticate. The system will 
    use credentials from the .env file.
    """


@mcp.prompt()
def course_list_prompt() -> str:
    """
    Create a prompt for listing courses.
    """
    return """
    Please show me a list of my enrolled courses in eClass.
    
    Note: I need to be logged in first to see my courses. If I'm not logged in yet,
    please help me with the login process first using the login tool.
    """


# ----- Main Function -----

def main():
    """Main function to run the MCP server."""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the eClass MCP Server')
    parser.add_argument(
        '--web', 
        action='store_true',
        help='Run as a web server instead of stdio'
    )
    parser.add_argument(
        '--port', 
        type=int,
        default=8000,
        help='Port to use for web server mode (default: 8000)'
    )
    args = parser.parse_args()
    
    # Start the server
    logger.info("Starting eClass MCP Server")
    
    if args.web:
        # For web server mode, we'll use the MCP CLI to start the server
        logger.info(f"Web server mode requested. Please use the following command instead:")
        logger.info(f"mcp dev {__file__}")
        logger.info(f"This will start the MCP Inspector and connect to this server.")
        sys.exit(0)
    else:
        # Run in stdio mode for Claude Desktop
        logger.info("Starting in stdio mode")
        mcp.run()


if __name__ == "__main__":
    main() 