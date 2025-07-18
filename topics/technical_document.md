## Topic Injector: Technical Documentation

### Overview
`topic-injector.py` is an asynchronous Python module designed to enhance conversational agents by detecting specific topics in user input and injecting relevant responses. It leverages Azure OpenAI for natural language understanding and response generation.

### Key Features
- **Topic Detection:** Identifies if a user's message matches or closely resembles predefined topic phrases.
- **Action Injection:** Executes custom actions (e.g., returning the current date/time) when a topic is detected.
- **Async Azure OpenAI Integration:** Uses `AsyncAzureOpenAI` for scalable, non-blocking API calls.
- **Extensible Topics:** Easily add new topics and associated actions.

### Main Components
- **Environment Setup:** Loads Azure OpenAI credentials from environment variables using `dotenv`.
- **Client Management:** Lazily initializes a singleton Azure OpenAI client for efficiency.
- **Topic Definition:** Topics are defined as dictionaries with a name, trigger phrases, and an action function.
- **Topic Check Agent:** Uses LLM to check if user input matches any topic phrases.
- **Topic Injector:** Scans the latest user message and triggers the corresponding action if a topic is detected.
- **Completion Function:** Handles message flow, topic injection, and LLM completion.

### Usage Example
1. **Define Topics:**
   - Each topic includes a name, a list of trigger phrases, and an action function.
   - Example: `get_date_topic` returns the current date/time if the user asks for it.
2. **Run the Main Function:**
   - The script's `main()` function demonstrates a chat loop, sending user messages and printing responses.
   - If a message matches a topic, the corresponding action is executed; otherwise, the LLM generates a response.

### Extending Functionality
- Add new topics by appending to the `topics` list with custom phrases and actions.
- Modify the `topic_check_agent` logic to refine phrase matching or add more complex topic detection.

### Example Topics
- **get_date:** Responds to queries about the current date and time.

### Integration
- Can be imported as a module or run as a standalone script.
- Designed for use in chatbots, assistants, or any conversational AI system requiring topic-based response injection.

### Dependencies
- `openai`, `dotenv`, `os`, `datetime`

### Running the Script
```bash
python topic-injector.py
```
This will execute the main chat loop and demonstrate topic injection in action.
