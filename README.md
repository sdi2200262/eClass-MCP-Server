# eClass MCP Server

This project provides a Model Context Protocol (MCP) server for interacting with a college's eClass platform. It uses a custom eClass client specifically tailored for the University of Athens (UoA) eClass system, which uses a Central Authentication Service (CAS) for Single Sign-On (SSO).

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io) allows applications to provide context for Large Language Models (LLMs) in a standardized way. This project implements an MCP server that exposes eClass functionality to LLMs like Claude through tools and resources.

## Features

The eClass MCP Server provides:

- **Authentication**: Secure login to UoA's eClass through the SSO system
- **Course Access**: Retrieve lists of enrolled courses
- **LLM Integration**: Connect Claude or other LLMs directly to your eClass account
- **Structured Interactions**: Pre-defined prompts for common eClass tasks
- **Secure Credential Management**: Local storage of credentials through environment variables

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/sdi2200262/eClass-MCP-Server.git
   cd eClass-MCP-Server
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure your environment by creating a `.env` file:
   ```
   ECLASS_URL=https://eclass.uoa.gr
   ECLASS_USERNAME=your_username  # Your UoA SSO username
   ECLASS_PASSWORD=your_password  # Your UoA SSO password
   ```

## Using with Cursor MCP 





## Manual Testing

To test the server directly without Claude Desktop:

```bash
# Activate your virtual environment first
mcp dev mcp_server.py
```

This opens the MCP Inspector, allowing you to test the server's functionality.

## Authentication Flow

This client handles the multi-step authentication process required by UoA's eClass:

1. Access the eClass login form at `/main/login_form.php`
2. Click on the UoA login button (redirects to the CAS SSO service)
3. Authenticate with the UoA SSO service (sso.uoa.gr)
4. Upon successful authentication, the user is redirected back to eClass

## MCP Server Components

The server provides the following MCP components:

### Resources

- `course://list` - Returns a formatted list of enrolled courses
- `auth://status` - Returns the current authentication status

### Tools

- `login(username, password)` - Authenticate with eClass
- `logout()` - End the current session
- `get_courses()` - Retrieve a list of enrolled courses
- `get_connection_info()` - Get information about the current connection

### Prompts

- `login_prompt()` - A prompt to assist with logging in
- `course_list_prompt()` - A prompt to retrieve course listings
- `help_prompt()` - A prompt explaining server capabilities

## Project Structure

- `eclass_client.py`: Main client implementation for interacting with eClass
- `mcp_server.py`: MCP server implementation
- `install_server.py`: Helper script for installing in Claude Desktop
- `latex/`: Directory containing the Technical Report of the Project using LaTeX document generation
- `test_login.py`: Script to test the authentication flow
- `requirements.txt`: Python dependencies
- `.env`: Configuration file for storing credentials and settings

## Security Notes

- All private data are stored locally
- The server is being booted locally and on-command whenever an appropriate request is sent to the LLM Assistant which has access to it.
- Credentials are stored in a local `.env` file, which should be kept secure and never committed to version control
- The application stores session cookies in memory only
- Always use HTTPS URLs for the eClass instance to ensure secure transmission of credentials
- This client simulates a browser-based authentication flow, which means it needs your actual UoA credentials


## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details. 