#uv init
# uv add requests, mcp
from weather import fetch_weather
from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("weather-mcp-server")

@mcp.tool()
def getWeather(city:str):
    """
    Fetch weather for the a city
    
    :param city: City value for call
    :type city: str
    """
    return fetch_weather(city)

#run the server
if __name__ == "__main__":
    uvicorn.run(
        mcp,
        host="0.0.0.0", # <--- Correct place to set the host
        port=8000       # <--- Correct place to set the port
    ) 