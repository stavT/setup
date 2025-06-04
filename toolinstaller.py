import subprocess
import os
import sys
import re
import threading
import time

class ProgressBar:
    """Simple progress bar implementation with true single-line animation"""
    def __init__(self, total=100, length=40, prefix="Progress"):
        self.total = total
        self.length = length
        self.prefix = prefix
        self.current = 0
        self.running = False
        self.first_update = True
        
    def update(self, current, message=None):
        """Update progress bar with current value - true single line animation"""
        if current is not None:
            self.current = min(current, self.total)
        percent = (self.current / self.total) * 100
        filled_length = int(self.length * self.current // self.total)
        bar = '█' * filled_length + '-' * (self.length - filled_length)
        
        # Build display string
        if message:
            message = message[:30] if len(message) > 30 else message
            display = f'{self.prefix}: |{bar}| {percent:5.1f}% - {message}'
        else:
            display = f'{self.prefix}: |{bar}| {percent:5.1f}%'
        
        # Use ANSI escape codes for better compatibility
        if not self.first_update:
            # Move cursor to beginning of line and clear it
            sys.stdout.write('\033[2K\033[1G')
        else:
            self.first_update = False
            
        sys.stdout.write(display)
        sys.stdout.flush()
        
    def finish(self):
        """Complete the progress bar"""
        self.update(self.total)
        print()  # Add newline when finished

class Spinner:
    """Simple spinner for indeterminate progress"""
    def __init__(self, message="Installing"):
        self.message = message
        self.running = False
        self.thread = None
        self.chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.index = 0
        
    def _spin(self):
        """Internal spinning method"""
        while self.running:
            print(f'\r{self.message} {self.chars[self.index]}', end='', flush=True)
            self.index = (self.index + 1) % len(self.chars)
            time.sleep(0.1)
            
    def start(self):
        """Start the spinner"""
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self, final_message=None):
        """Stop the spinner"""
        self.running = False
        if self.thread:
            self.thread.join()
        if final_message:
            print(f'\r{final_message}' + ' ' * 20)
        else:
            print('\r' + ' ' * 50 + '\r', end='')

def run_command_with_progress(command, message="Installing", capture_output=True, shell=True):
    """Run a command with progress indication"""
    
    # Try to detect if we can show real progress
    if "pip install" in command:
        return run_pip_with_progress(command)
    elif "winget install" in command:
        return run_winget_with_progress(command)
    elif "docker run" in command or "docker pull" in command:
        return run_docker_with_progress(command)
    elif "ollama pull" in command or "ollama run" in command:
        return run_ollama_with_progress(command)
    else:
        return run_command_with_spinner(command, message)

def run_pip_with_progress(command):
    """Run pip command with progress tracking"""
    try:
        print(f"📦 {command}")
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            shell=True,
            universal_newlines=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        progress = ProgressBar(prefix="Installing package")
        output_lines = []
        
        for line in iter(process.stdout.readline, ''):
            output_lines.append(line)
            line_lower = line.lower()
            
            # Look for download progress
            if "downloading" in line_lower and "%" in line:
                try:
                    # Extract percentage from pip output
                    percent_match = re.search(r'(\d+)%', line)
                    if percent_match:
                        percent = int(percent_match.group(1))
                        progress.update(percent)
                except:
                    pass
            elif "installing" in line_lower:
                progress.update(80)
            elif "successfully installed" in line_lower:
                progress.update(100)
                
        process.wait()
        progress.finish()
        
        return process.returncode == 0, ''.join(output_lines), ""
        
    except Exception as e:
        return False, "", str(e)

def run_winget_with_progress(command):
    """Run winget command with progress tracking"""
    try:
        print(f"📦 {command}")
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            shell=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        progress = ProgressBar(prefix="Installing application")
        output_lines = []
        
        for line in iter(process.stdout.readline, ''):
            output_lines.append(line)
            line_lower = line.lower()
            
            if "downloading" in line_lower:
                progress.update(25)
            elif "installing" in line_lower:
                progress.update(60)
            elif "successfully installed" in line_lower:
                progress.update(100)
                
        process.wait()
        progress.finish()
        
        return process.returncode == 0, ''.join(output_lines), ""
        
    except Exception as e:
        return False, "", str(e)

def run_docker_with_progress(command):
    """Run docker command with progress tracking"""
    try:
        print(f"🐳 {command}")
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            shell=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        progress = ProgressBar(prefix="Docker operation")
        output_lines = []
        layers_total = 0
        layers_complete = 0
        
        for line in iter(process.stdout.readline, ''):
            output_lines.append(line)
            
            # Track docker layer progress
            if "Pull complete" in line:
                layers_complete += 1
                if layers_total > 0:
                    percent = (layers_complete / layers_total) * 100
                    progress.update(percent)
            elif "Pulling from" in line:
                progress.update(10)
            elif re.search(r'[a-f0-9]{12}:', line):
                layers_total += 1
                
        process.wait()
        progress.finish()
        
        return process.returncode == 0, ''.join(output_lines), ""
        
    except Exception as e:
        return False, "", str(e)

def run_ollama_with_progress(command):
    """Run ollama command with progress tracking"""
    try:
        print(f"🤖 {command}")
        print("📥 Starting Ollama model download (this may take several minutes for large models)...")
        
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            shell=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        progress = ProgressBar(prefix="Downloading model")
        output_lines = []
        last_update_time = time.time()
        download_started = False
        
        try:
            for line in iter(process.stdout.readline, ''):
                if not line:  # Empty line means end of output
                    break
                    
                line = line.strip()
                if line:
                    output_lines.append(line)
                    line_lower = line.lower()
                    current_time = time.time()
                    
                    # Check for download progress indicators
                    if any(keyword in line_lower for keyword in ['pulling', 'downloading', 'digest:', 'status:']):
                        download_started = True
                        
                        # Look for percentage information
                        if '%' in line:
                            try:
                                import re
                                percent_match = re.search(r'(\d+)%', line)
                                if percent_match:
                                    percent = int(percent_match.group(1))
                                    progress.update(percent, f"Downloading: {percent}%")
                                    last_update_time = current_time
                                    continue
                            except:
                                pass
                        
                        # Look for size information (MB/GB)
                        if any(unit in line_lower for unit in ['mb', 'gb', 'bytes']):
                            size_info = line.split()[-2:] if len(line.split()) >= 2 else ['', '']
                            progress.update(None, f"Downloading: {' '.join(size_info)}")
                            last_update_time = current_time
                            continue
                    
                    # Show periodic updates even without specific progress
                    if download_started and current_time - last_update_time > 10:  # Update every 10 seconds
                        progress.update(None, "Downloading... (large model, please wait)")
                        last_update_time = current_time
                    
                    # Check for completion
                    if any(keyword in line_lower for keyword in ['success', 'complete', 'finished']):
                        progress.update(100, "Download complete!")
                        break
                        
                    # Check for errors
                    if any(keyword in line_lower for keyword in ['error', 'failed', 'not found']):
                        progress.finish()
                        print(f"❌ Error: {line}")
                        return False, output_lines
                        
        except KeyboardInterrupt:
            print(f"⚠️ Download interrupted by user")
            process.terminate()
            progress.finish()
            return False, output_lines
        
        # Wait for process to complete
        return_code = process.wait()
        progress.finish()
        
        if return_code == 0:
            print("✅ Ollama model download completed successfully!")
            return True, output_lines
        else:
            print(f"❌ Ollama command failed with return code {return_code}")
            return False, output_lines
            
    except Exception as e:
        print(f"❌ Error running Ollama command: {e}")
        return False, []

def run_command_with_spinner(command, message="Processing"):
    """Run command with spinner for indeterminate progress"""
    spinner = Spinner(message)
    spinner.start()
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, encoding='utf-8', errors='ignore')
        success = result.returncode == 0
        spinner.stop(f"✅ {message} completed!" if success else f"❌ {message} failed!")
        return success, result.stdout, result.stderr
    except Exception as e:
        spinner.stop(f"❌ {message} failed!")
        return False, "", str(e)

def run_command(command, capture_output=True, shell=True):
    """Run a command and return result"""
    try:
        result = subprocess.run(command, capture_output=capture_output, text=True, shell=shell, encoding='utf-8', errors='ignore')
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
            if not success:
                # Check if running as docker container
                success, stdout, _ = run_command("docker ps --filter name=n8n")
                return success and "n8n" in stdout
        return success
        
    elif tool_name.lower() == "langflow":
        # Check if Docker is available first
        docker_available, _, _ = run_command("docker --version")
        if not docker_available:
            return False
            
        # Check for running Langflow containers (by name first, then by image)
        success, stdout, _ = run_command("docker ps --filter name=langflow")
        if success and "langflow" in stdout:
            return True
            
        # Check for running containers by image name
        success, stdout, _ = run_command("docker ps")
        if success and "langflowai/langflow" in stdout:
            return True
            
        # Also check for stopped containers (might just need to be restarted)
        success, stdout, _ = run_command("docker ps -a --filter name=langflow")
        if success and "langflow" in stdout:
            return True
            
        # Final check for any langflow containers by image
        success, stdout, _ = run_command("docker ps -a")
        return success and "langflowai/langflow" in stdout
    
    # LLM Model checking (Ollama models)
    elif tool_type == "LLM":
        success, stdout, _ = run_command("ollama list")
        if success:
            # Clean up model name for checking
            model_name = tool_name.replace("‑", "-").replace("–", "-").lower()
            
            # Handle special model name mappings
            model_mappings = {
                "llama3.3": "llama3.3",
                "phi4": "phi4", 
                "llama3.2": "llama3.2",
                "qwen2.5": "qwen2.5",
                "llava": "llava",
                "gemma3": "gemma2",  # Ollama uses gemma2 not gemma3
                "llama3.2-vision": "llama3.2-vision",
                "mixtral": "mixtral",
                "llava-llama3": "llava-llama3",
                "mistral": "mistral",
                "nomic-embed-text": "nomic-embed-text",
                "microsoft/phi-3-mini-4k-instruct": "phi3",
                "mistralai/mistral-7b-instruct-v0.2": "mistral",
                "meta-llama/llama-3.2-3b-instruct": "llama3.2",
                "qwen/qwen2.5-7b-instruct": "qwen2.5",
                "google/gemma-3-1b-it": "gemma2",
                "llama3.2 vision": "llama3.2-vision",
                "llava llama3": "llava-llama3",
                "mixtral 8×7b": "mixtral",
                "nomic‑embed‑text": "nomic-embed-text"
            }
            
            # Get the actual model name to check
            check_name = model_mappings.get(model_name, model_name)
            
            # Check if model exists (with or without :latest suffix)
            stdout_lower = stdout.lower()
            return (check_name in stdout_lower or 
                   f"{check_name}:latest" in stdout_lower or
                   f"{check_name}:" in stdout_lower)
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
        success, stdout, stderr = run_winget_with_progress("winget install Ollama.Ollama")
        if not success:
            print("Trying direct download...")
            success, stdout, stderr = run_command_with_spinner("curl -L https://ollama.com/download/OllamaSetup.exe -o OllamaSetup.exe && start OllamaSetup.exe", "Downloading Ollama")
        
    elif tool_name.lower() == "docker":
        print("Installing Docker Desktop via winget...")
        success, stdout, stderr = run_winget_with_progress("winget install Docker.DockerDesktop")
        
    elif "open webui" in tool_name.lower():
        print("Installing Open WebUI via Docker...")
        success, stdout, stderr = run_docker_with_progress("docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main")
        
    elif tool_name.lower() == "anythingllm":
        print("Installing AnythingLLM via winget...")
        success, stdout, stderr = run_winget_with_progress("winget install Mintplex-Labs.AnythingLLM")
        if not success:
            print("Please download manually from: https://anythingllm.com/desktop")
            return True  # Manual installation
            
    elif tool_name.lower() == "n8n":
        print("Installing n8n via npm...")
        success, stdout, stderr = run_command_with_spinner("npm install -g n8n", "Installing n8n")
        if not success:
            print("Installing n8n via Docker...")
            success, stdout, stderr = run_docker_with_progress("docker run -d -p 5678:5678 --name n8n n8nio/n8n")
        
    elif tool_name.lower() == "langflow":
        print("Installing Langflow via Docker...")
        # First check if a langflow container already exists (stopped)
        existing_check, stdout, _ = run_command("docker ps -a --filter name=langflow")
        if "langflow" in stdout:
            print("Existing Langflow container found. Starting it...")
            success, stdout, stderr = run_command_with_spinner("docker start langflow", "Starting Langflow")
        else:
            success, stdout, stderr = run_docker_with_progress("docker run -d -p 7860:7860 --name langflow --restart unless-stopped langflowai/langflow:latest")
        
    # LLM Model installations
    elif tool_type == "LLM":
        model_name = tool_name.replace("‑", "-").replace("–", "-").lower()
        
        # Handle special model name mappings for installation
        model_mappings = {
            "llama3.3": "llama3.3",
            "phi4": "phi4", 
            "llama3.2": "llama3.2",
            "qwen2.5": "qwen2.5",
            "llava": "llava",
            "gemma3": "gemma2",  # Ollama uses gemma2 not gemma3
            "llama3.2-vision": "llama3.2-vision",
            "mixtral": "mixtral",
            "llava-llama3": "llava-llama3",
            "mistral": "mistral",
            "nomic-embed-text": "nomic-embed-text",
            "microsoft/phi-3-mini-4k-instruct": "phi3",
            "mistralai/mistral-7b-instruct-v0.2": "mistral",
            "meta-llama/llama-3.2-3b-instruct": "llama3.2",
            "qwen/qwen2.5-7b-instruct": "qwen2.5",
            "google/gemma-3-1b-it": "gemma2",
            "llama3.2 vision": "llama3.2-vision",
            "llava llama3": "llava-llama3",
            "mixtral 8×7b": "mixtral",
            "nomic‑embed‑text": "nomic-embed-text"
        }
        
        actual_model = model_mappings.get(model_name, model_name)
        print(f"Installing {actual_model} via Ollama...")
        print(f"Note: Large models may take 10-30 minutes to download")
        success, stdout = run_ollama_with_progress(f"ollama pull {actual_model}")
        stderr = ""  # Ollama progress function doesn't return stderr separately
        
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
        success, stdout, stderr = run_pip_with_progress(f"pip install {package_name}")
        
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

def get_installation_warning(tool_name, tool_type):
    """Get warning message for installations that take a long time or are very large"""
    
    # Large LLM model warnings
    if tool_type == "LLM":
        model_warnings = {
            "llama3.3": "⚠️  WARNING: llama3.3 is ~8GB and may take 15-30 minutes to download",
            "phi4": "⚠️  WARNING: phi4 is ~8GB and may take 15-30 minutes to download", 
            "llama3.2": "⚠️  WARNING: llama3.2 is ~2GB and may take 5-15 minutes to download",
            "qwen2.5": "⚠️  WARNING: qwen2.5 is ~4GB and may take 10-25 minutes to download",
            "llava": "⚠️  WARNING: llava is ~4GB and may take 10-25 minutes to download",
            "mixtral": "⚠️  WARNING: mixtral is ~26GB and may take 45-90 minutes to download",
            "llava-llama3": "⚠️  WARNING: llava-llama3 is ~8GB and may take 15-30 minutes to download",
            "llama3.2-vision": "⚠️  WARNING: llama3.2-vision is ~8GB and may take 15-30 minutes to download"
        }
        
        model_name = tool_name.replace("‑", "-").replace("–", "-").lower()
        return model_warnings.get(model_name, None)
    
    # Framework warnings
    framework_warnings = {
        "docker": "⚠️  WARNING: Docker Desktop is ~500MB and may take 5-10 minutes to download and install",
        "anythingllm": "⚠️  WARNING: AnythingLLM is ~200MB and may take 2-5 minutes to download and install"
    }
    
    return framework_warnings.get(tool_name.lower(), None)

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

        # Show warning for large installations
        warning = get_installation_warning(name, tool_type)
        if warning:
            print(warning)
            
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
