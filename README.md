# AI Crew System

A modular AI system that manages multiple AI agents and their tasks.

## Project Structure

. ├── app/ │ ├── ai/ │ │ ├── config/ │ │ │ ├── agents.yaml # Agent definitions and capabilities │ │ │ └── tasks.yaml #
Task configurations and workflows │ │ └── crew.py # Core AI crew management logic │ ├── models/ │ │ └──
request_models.py # Request/response data models │ └── main.py # Application entry point └── sample_request.json #
Example request format

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ai-crew-system
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

#### Agents Configuration

In `app/ai/config/agents.yaml`, define your AI agents:

```yaml
agent_name:
  capabilities:
    - capability1
    - capability2
  parameters:
    key: value
```

#### Tasks Configuration

In `app/ai/config/tasks.yaml`, specify available tasks:

```yaml
task_name:
  required_capabilities:
    - capability1
  parameters:
    key: value
```

### Usage

1. Prepare your request following the format in `sample_request.json`:

```json
{
  "task": "task_name",
  "parameters": {
    "key": "value"
  }
}
```

2. Run the application:

```bash
python app/main.py
```

## API Reference

### Request Models

The system uses Pydantic models defined in `app/models/request_models.py` for request validation and processing.

### Core Components

- `crew.py`: Manages AI agent coordination and task execution
- `main.py`: Handles HTTP requests and system initialization
- Configuration files: Define system behavior and capabilities

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[MIT License](LICENSE)

## Contact

Project Link: [https://github.com/barackm/task-view-backend](https://github.com/barackm/task-view-backend)
