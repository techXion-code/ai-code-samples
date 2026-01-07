#uv init
#uv add mcp, uvicorn, google-api-python-client, google-auth-httplib2, google-auth-oauthlib

import base64
import uvicorn
from email.message import EmailMessage
from mcp.server.fastmcp import FastMCP
from gmail_auth import get_gmail_service

mcp = FastMCP("GmailDemo")

@mcp.tool()
def send_email(recipient: str, subject: str, body: str) -> str:
    """
    Sends a plain text email via Gmail.
    :param recipient: Email address of the receiver.
    :param subject: The subject line of the email.
    :param body: The main content of the email.
    """  
    msg = prepareMessag(recipient, subject, body)

    #send message
    service = get_gmail_service()
    send_request = service.users().messages().send(userId="me", body=msg)
    result = send_request.execute()
    
    return f"Success! Message ID: {result.get('id')}"      

def prepareMessag(recipient: str, subject: str, body: str):
    message = EmailMessage()
    message.set_content(body)
    message['To'] = recipient
    message['Subject'] = subject

    # Encode to base64url
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def dummy():
    a = 1
    b = 2
    c = a + b
    return c

if __name__ == "__main__":
    print(dummy())
    # Start the MCP Server
    # 1. Create the ASGI application from your MCP instance
    #app = mcp.streamable_http_app()
    
    # 2. Run the 'app' object, NOT the 'mcp' object
    #print("Starting Gmail MCP Server on http://0.0.0.0:8000")
    #uvicorn.run(app, host="0.0.0.0", port=8000)
