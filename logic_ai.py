import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

def analyze_part_risk(part_number, description):
    """
    Analyze BOM component lifecycle risk using an LLM.
    Returns: (status, reason) tuple
    """
    
    # 1. Check API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Config Error", "❌ OPENAI_API_KEY not found in .env file."

    # # 2. Setup Model
    # llm = ChatOpenAI(
    #     model="gpt-3.5-turbo", 
    #     temperature=0,
    #     api_key=api_key
    # )
    # ✅ Correct way to instantiate ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # modern, fast, cheap; swap later if needed
        temperature=0
    )

    # 3. Define Prompt
    # We ask for a simple pipe-separated format which is easier to parse than JSON
    template = """
    System Role:
You are a Senior Component Engineer at a Tier-1 Defense Contractor with responsibility for lifecycle risk, obsolescence management, and supply-chain continuity.

Task:
Assess the lifecycle status of the electronic component listed below using engineering judgment and industry norms.

Component Information:
- Part Number: {part}
- Description: {desc}

Classification Rules (apply conservatively):
1. Generic passives (e.g., resistors, capacitors, inductors, ferrites) → ACTIVE
2. Legacy interfaces or packaging (e.g., VGA, RS-232, Parallel, DIP, PLCC) → OBSOLETE
3. Modern digital or RF components (e.g., USB-C, Cortex-M, Wi-Fi 6) → ACTIVE
4. If uncertain:
   - Default to ACTIVE
   - Explicitly state uncertainty

Constraints:
- Do NOT invent manufacturer lifecycle data
- Base conclusions on technology relevance only

Output Requirements:
- Output MUST be valid JSON
- EXACT format only

JSON Output Format:
{{
  "{part}": "STATUS | BRIEF REASON"
}}
    """

    prompt = PromptTemplate(template=template, input_variables=["part", "desc"])

    try:
        # 4. Run AI
        chain = prompt | llm
        response = chain.invoke({"part": part_number, "desc": description})


        # content = response.content.strip() # Clean up whitespace

        # # 5. Parse the Output (The Critical Fix)
        # # Handle case where content might be a list
        # if isinstance(content, list):
        #     content = content[0] if content else ""
        # --- FIX STARTS HERE ---
        # 1. robustly extract content regardless of response type
        if hasattr(response, 'content'):
            content = response.content  # It's an AIMessage object
        elif isinstance(response, str):
            content = response          # It's already a string
        elif isinstance(response, dict) and 'text' in response:
            content = response['text']  # It's a legacy dictionary
        else:
            return "Error", f"Unexpected response format: {type(response)}"
            
        content = str(content).strip()
        
        if "|" in content:
            # Split "ACTIVE | It is good" into two variables
            status, reason = content.split("|", 1)
            return status.strip(), reason.strip()
        else:
            # Fallback if AI messes up formatting
            return "Active", f"AI Result: {content}"

    except Exception as e:
        return "Error", f"AI Failed: {str(e)}"