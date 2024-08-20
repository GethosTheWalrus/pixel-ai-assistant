# Pixel AI Assistant
Pixel was designed to be small, extensible, easy to read, and totally offline at its core. It is designed to communicate with LLMs running with Ollama utilizing the Ollama Python Library. 

With the ability to provide natural sounding replies to questions, you can talk to Pixel in a similar way to how you would talk to ChatGPT.

It is possible to run everything that Pixel needs to operate on a single machine, disconnected from the internet (post install).

# Quickstart

* Install Python 
* Clone the repository to your machine
* Install Ollama 
* Create a Python virtual environment for this project and activate it
* Run the following commands

```
ollama run llama3.1 # type /bye to exit interactive mode
cd pixel-ai-assistant
pip install -r requirements.txt # also install pi_requirements.txt on Raspberry Pi
python main.py
```
