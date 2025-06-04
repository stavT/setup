import subprocess
import os
import sys
import re

def run_command(command, capture_output=True, shell=True):
    """Run a command and return result"""
    try:
        result = subprocess.run(command, capture_output=capture_output, text=True, shell=shell)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_installed(tool_name, tool_type):
    """Check if a tool is installed using various methods"""
    
    # Framework checking
    if tool_name.lower() == "ollama":
        success, stdout, _ = run_command("ollama --version")
        return success
    
    elif tool_name.lower() == "docker":
        success, stdout, _ = run_command("docker --version")
        return success
        
    elif "open webui" in tool_name.lower():
        success, stdout, _ = run_command("docker ps --filter name=open-webui")
        return success and "open-webui" in stdout
        
    elif tool_name.lower() == "anythingllm":
        # Check if AnythingLLM is installed via winget or in common locations
        success, stdout, _ = run_command("winget list --name AnythingLLM")
        return success and "AnythingLLM" in stdout
        
    elif tool_name.lower() == "n8n":
        success, stdout, _ = run_command("n8n --version")
        if not success:
            success, stdout, _ = run_command("npm list -g n8n")
        return success
        
    elif tool_name.lower() == "langflow":
        success, stdout, _ = run_command("langflow --version")
        if not success:
            success, stdout, _ = run_command("python -c \"import langflow; print('installed')\"")
        return success
    
    # LLM Model checking (Ollama models)
    elif tool_type == "LLM":
        success, stdout, _ = run_command("ollama list")
        if success:
            # Clean up model name for checking
            model_name = tool_name.replace("‑", "-").replace("–", "-")
            return model_name.lower() in stdout.lower()
        return False
    
    # Python package checking
    elif tool_type == "ספריית פייתון" or tool_type == "חבילת פייתון":
        package_name = tool_name.lower()
        # Handle special cases
        if package_name == "smolagent":
            package_name = "smolagents"
        elif package_name in ["os", "traceback"]:  # Built-in modules
            return True
        elif package_name == "automodelforquestionanswering":
            package_name = "transformers"  # This is part of transformers
            
        success, stdout, _ = run_command(f"python -c \"import {package_name}; print('installed')\"")
        return success
    
    return False

def install_tool(tool_name, tool_type):
    """Install a tool using the most efficient Windows method"""
    
    print(f"\n🔧 Installing {tool_name}...")
    
    # Framework installations
    if tool_name.lower() == "ollama":
        print("Installing Ollama via winget...")
        success, stdout, stderr = run_command("winget install Ollama.Ollama")
        if not success:
            print("Trying direct download...")
            success, stdout, stderr = run_command("curl -L https://ollama.com/download/OllamaSetup.exe -o OllamaSetup.exe && start OllamaSetup.exe")
        
    elif tool_name.lower() == "docker":
        print("Installing Docker Desktop via winget...")
        success, stdout, stderr = run_command("winget install Docker.DockerDesktop")
        
    elif "open webui" in tool_name.lower():
        print("Installing Open WebUI via Docker...")
        success, stdout, stderr = run_command("docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main")
        
    elif tool_name.lower() == "anythingllm":
        print("Installing AnythingLLM via winget...")
        success, stdout, stderr = run_command("winget install Mintplex-Labs.AnythingLLM")
        if not success:
            print("Please download manually from: https://anythingllm.com/desktop")
            return True  # Manual installation
            
    elif tool_name.lower() == "n8n":
        print("Installing n8n via npm...")
        success, stdout, stderr = run_command("npm install -g n8n")
        if not success:
            print("Installing n8n via Docker...")
            success, stdout, stderr = run_command("docker run -d -p 5678:5678 --name n8n n8nio/n8n")
        
    elif tool_name.lower() == "langflow":
        print("Installing Langflow via pip...")
        success, stdout, stderr = run_command("pip install langflow")
        
    # LLM Model installations
    elif tool_type == "LLM":
        model_name = tool_name.replace("‑", "-").replace("–", "-")
        print(f"Installing {model_name} via Ollama...")
        success, stdout, stderr = run_command(f"ollama pull {model_name}")
        
    # Python package installations
    elif tool_type == "ספריית פייתון" or tool_type == "חבילת פייתון":
        package_name = tool_name.lower()
        if package_name == "smolagent":
            package_name = "smolagents"
        elif package_name in ["os", "traceback"]:  # Built-in modules
            return True
        elif package_name == "automodelforquestionanswering":
            package_name = "transformers"
            
        print(f"Installing {package_name} via pip...")
        success, stdout, stderr = run_command(f"pip install {package_name}")
        
    else:
        print(f"⚠️  Unknown installation method for {tool_name}")
        return False
    
    if success:
        print(f"✅ Successfully installed {tool_name}")
    else:
        print(f"❌ Failed to install {tool_name}")
        if stderr:
            print(f"Error: {stderr}")
            
    return success

def parse_markdown_requirements():
    """Parse the markdown file to get tool requirements"""
    tools = []
    
    try:
        with open("Installation_Checklist_Prompt.md", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Find all tool entries
        pattern = r'- \*\*(.*?)\*\* \((.*?)\)'
        matches = re.findall(pattern, content)
        
        for name, tool_type in matches:
            # Skip duplicates and invalid entries
            if name and tool_type and name not in [t['name'] for t in tools]:
                tools.append({
                    'name': name.strip(),
                    'type': tool_type.strip()
                })
                
    except FileNotFoundError:
        print("❌ Installation_Checklist_Prompt.md not found!")
        return []
    except Exception as e:
        print(f"❌ Error parsing markdown file: {e}")
        return []
        
    return tools

def main():
    print("🚀 AI Development Environment Installer")
    print("=" * 50)
    
    # Parse requirements from markdown
    tools = parse_markdown_requirements()
    if not tools:
        print("❌ No tools found to install!")
        return
        
    print(f"Found {len(tools)} tools to check/install\n")
    
    # Check and install each tool
    for tool in tools:
        name = tool['name']
        tool_type = tool['type']
        
        print(f"🔍 Checking: {name} ({tool_type})")
        
        if check_installed(name, tool_type):
            print(f"✅ {name} is already installed.")
            continue
            
        # Ask user for installation
        response = input(f"❓ {name} is not installed. Install it? (y/n/all): ").strip().lower()
        
        if response in ['y', 'yes']:
            install_tool(name, tool_type)
        elif response == 'all':
            # Install all remaining tools
            install_tool(name, tool_type)
            for remaining_tool in tools[tools.index(tool)+1:]:
                if not check_installed(remaining_tool['name'], remaining_tool['type']):
                    install_tool(remaining_tool['name'], remaining_tool['type'])
            break
        else:
            print(f"⏩ Skipping {name}")
            
    print("\n🎉 Installation process completed!")
    print("Note: Some tools may require a system restart to work properly.")

if __name__ == "__main__":
    main()
