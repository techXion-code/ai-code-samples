from fastapi import FastAPI
import uvicorn
import threading

app = FastAPI(title="Weather API")

@app.get("/weather")
def http_weather(city: str):
    return get_weather_tool(city)

if __name__ == "__main__":
    # Start MCP stdio listener in background
    def run_mcp():
        mcp.run(transport="stdio")

    threading.Thread(target=run_mcp, daemon=True).start()

    # Start HTTP server
    uvicorn.run(app, host="0.0.0.0", port=1081)

    uvicorn.run(app, host="0.0.0.0", port=1081)
