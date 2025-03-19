# eClass MCP Server

This project provides a client for interacting with an eClass platform instance, designed to be used as part of a Model Context Protocol (MCP) server that will connect an LLM directly to a college's eClass instance. It is specifically tailored for the University of Athens (UoA) eClass system, which uses a Central Authentication Service (CAS) for Single Sign-On (SSO).

## Authentication Flow

This client handles the multi-step authentication process required by UoA's eClass:

1. Access the eClass login form at `/main/login_form.php`
2. Click on the UoA login button (redirects to the CAS SSO service)
3. Authenticate with the UoA SSO service (sso.uoa.gr)
4. Upon successful authentication, the user is redirected back to eClass

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd eclass-mcp-server
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure your environment by editing the `.env` file:
   ```
   ECLASS_URL=https://eclass.uoa.gr
   ECLASS_USERNAME=your_username  # Your UoA SSO username
   ECLASS_PASSWORD=your_password  # Your UoA SSO password
   ```

## Usage

Run the test script to verify that you can authenticate with UoA's eClass:

```
python test_login.py
```

If successful, you should see a list of your enrolled courses.

Alternatively, you can use the client in your own Python code:

```python
from eclass_client import EClassClient

# Initialize client
client = EClassClient()

# Login
if client.login("your_username", "your_password"):
    # Get list of courses
    courses = client.get_courses()
    
    # Print courses
    for course in courses:
        print(f"Course: {course['name']}")
    
    # Logout
    client.logout()
```

## Features

The current implementation includes:

- Authentication with UoA's SSO system (CAS)
- Fetching the list of enrolled courses
- Session management (login/logout)
- Robust error handling and logging

## Project Structure

- `eclass_client.py`: Main client implementation for interacting with eClass
- `test_login.py`: Script to test the authentication flow
- `requirements.txt`: Python dependencies
- `.env`: Configuration file for storing credentials and settings

## Future Development

This client will be integrated with FastMCP to create an MCP server that allows students to access eClass data directly from an LLM chatbox or AI-assisted IDE.

## Security Notes

- Credentials are stored in a local `.env` file, which should be kept secure and never committed to version control
- The application stores session cookies in memory only
- Always use HTTPS URLs for the eClass instance to ensure secure transmission of credentials
- This client simulates a browser-based authentication flow, which means it needs your actual UoA credentials 