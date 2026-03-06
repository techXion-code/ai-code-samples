import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { fetchWeather } from "./api-caller.js";

// Create an MCP server
const serverVarNameChangedAtAllPlaces = new McpServer({
    name: 'fetch-weather',
    version: '1.0.0'
});

const config ={
  title:"fetch-weather",
  description:"fetch-weather by city from api",
  inputSchema:{
    city: z.string()
  }
};

async function callback({ city }) {
  try {
    const resp = await fetchWeather(city);
    return {
      content: [
        {
          type: "text",
          text: `The weather in ${city} is ${resp.temperature}°C with a wind speed of ${resp.windspeed} km/h.`,
        },
      ],
    };
  } catch (e) {
    console.log(e);
  }
}

serverVarNameChangedAtAllPlaces.registerTool("fetchWeather_tool", config, callback);

export {serverVarNameChangedAtAllPlaces};