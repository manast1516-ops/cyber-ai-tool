import json
import re
from core.llm import get_llm
from core.registry import get_tool_descriptions, execute_tool

SYSTEM_PROMPT = """You are an elite cybersecurity assistant named CyberAI.
You assist with network defense, incident response, packet auditing, and system hardening.
You have access to the following diagnostic tools:
{tool_descriptions}

If a user query requires diagnostic checks, respond ONLY with a JSON object in this format:
{{"tool": "tool_name", "args": {{"arg_name": "value"}}}}

If no tool is required, respond conversationally, directly, and helpfully without mentioning whether a tool was used or skipped.
"""

class AgentOrchestrator:
    def __init__(self):
        self.llm = get_llm()

    def process_query(self, user_query: str) -> str:
        prompt = SYSTEM_PROMPT.format(tool_descriptions=get_tool_descriptions())
        full_prompt = f"{prompt}\n\nUser Query: {user_query}\nResponse:"
        
        print("[orchestrator] 🧠 Reasoning with Llama 3.2...")
        raw_response = self.llm.invoke(full_prompt).strip()

        # Check for tool invocation JSON
        match = re.search(r'\{.*"tool".*\}', raw_response, re.DOTALL)
        if match:
            try:
                action = json.loads(match.group(0))
                tool_name = action.get("tool")
                args = action.get("args", {})
                
                print(f"[orchestrator] ⚙️  Running tool: '{tool_name}' ({args})...")
                tool_result = execute_tool(tool_name, **args)
                print(f"[orchestrator] 📥 Tool output: {tool_result}")
                
                print("[orchestrator] 📝 Synthesizing final security summary...")
                synthesis_prompt = (
                    f"User asked: {user_query}\n"
                    f"Tool '{tool_name}' returned: {tool_result}\n"
                    "Provide a clear, professional summary and security assessment based on this result."
                )
                return self.llm.invoke(synthesis_prompt).strip()
            except json.JSONDecodeError:
                return raw_response

        return raw_response
