# 🤖 RandyAI Personal Assistant

**Complete Autonomous AI System for Randy Jordan**

A sophisticated personal AI assistant that learns, adapts, and operates autonomously while integrating with multiple AI platforms and managing daily tasks.

## 🌟 Features

### Core Capabilities
- **Autonomous Learning**: Self-improving AI that learns from interactions
- **Multi-Platform Integration**: Seamlessly connects to Perplexity, Abacus.AI, DeepAgent
- **Daily Updates**: Automatic daily reports and insights
- **Task Management**: Intelligent task creation, prioritization, and reminders
- **Persistent Memory**: SQLite-based memory system with pattern recognition
- **GitHub Integration**: Automated repository monitoring and project tracking

### Autonomous Features
- **Self-Directed Learning**: Analyzes patterns and improves performance
- **Question Generation**: Proactively asks relevant questions
- **Scheduled Operations**: Automatic daily, weekly, and monthly tasks
- **Memory Management**: Intelligent cleanup and optimization
- **Error Recovery**: Self-healing and error reporting

### Personal Context
- **Location Aware**: Mobile, Alabama context for local searches
- **Work Integration**: Uber, Lyft, Spark delivery optimization
- **Interest Tracking**: AI development, car modifications, tech gadgets
- **Preference Learning**: Adapts to Randy's communication style and needs

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Joker5514/RandyAI-PersonalAssistant.git
cd RandyAI-PersonalAssistant

# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

### Initial Setup

1. **Configure API Keys**:
   ```bash
   python main.py --config
   ```
   Add your API keys for:
   - Perplexity AI
   - Abacus.AI
   - DeepAgent
   - GitHub Personal Access Token

2. **First Run**:
   ```bash
   python main.py --welcome
   ```

3. **Start Autonomous Mode**:
   ```bash
   python main.py --start
   ```

## 📱 Usage

### Command Line Interface

```bash
# Start autonomous operation
python main.py --start

# Interactive chat mode
python main.py --interactive

# Check system status
python main.py --status

# Force daily update
python main.py --update

# Configure settings
python main.py --config
```

### Interactive Mode Commands

```
# Basic commands
exit                    # Quit interactive mode
status                  # Show system status
help                    # Show available commands

# Task management
task list               # List pending tasks
task create <title>     # Create new task

# Memory operations
memory list             # Show recent memory
memory save <key> <val> # Save to memory
memory get <key>        # Retrieve memory item

# Natural language
Just type naturally for AI responses!
```

## 🏗️ Architecture

### Core Components

- **`core/randy_ai.py`**: Main AI class with learning and memory
- **`integrations/multi_platform.py`**: API integrations and orchestration
- **`autonomous/scheduler.py`**: Autonomous operations and scheduling
- **`main.py`**: Application launcher and CLI interface

### Database Schema

- **Memory Table**: Persistent key-value storage with categories
- **Learning Table**: Interaction history with success scoring
- **Tasks Table**: Task management with priorities and due dates
- **Integrations Table**: API configurations and status

### Multi-Platform Architecture

```
RandyAI Core
    ├── Perplexity Integration (Research & Analysis)
    ├── Abacus.AI Integration (Advanced Processing)
    ├── DeepAgent Integration (Project Handoffs)
    ├── GitHub Integration (Code Management)
    └── Autonomous Scheduler (Self-Management)
```

## 🔧 Configuration

### API Keys Setup

The system requires API keys for full functionality:

1. **Perplexity AI**: Get from [perplexity.ai](https://perplexity.ai)
2. **Abacus.AI**: Get from [abacus.ai](https://abacus.ai)
3. **DeepAgent**: Get from [deepagent.ai](https://deepagent.ai)
4. **GitHub**: Personal Access Token from GitHub Settings

### Personal Preferences

The system automatically configures for Randy Jordan with:
- Location: Mobile, Alabama (ZIP: 36605)
- Vehicle: 2020 Toyota Corolla LE
- Work: Uber, Lyft, Spark delivery
- Interests: AI Development, Car Mods, Tech Gadgets, Gaming

## 🤖 Autonomous Operations

### Daily Schedule
- **9:00 AM**: Daily update generation
- **Every 3 hours**: Learning analysis
- **Every 6 hours**: GitHub repository checks
- **Every 12 hours**: Self-improvement assessment
- **Weekly**: Memory cleanup and optimization

### Learning System
- Tracks interaction success rates
- Identifies improvement patterns
- Generates contextual questions
- Adapts responses based on feedback

### Task Automation
- Creates tasks based on patterns
- Prioritizes urgent items automatically
- Generates reminders and follow-ups
- Learns from completion patterns

## 🔌 Integration Examples

### Perplexity Query
```python
result = await enhanced_ai.enhanced_query(
    "Find the best car modifications for 2020 Toyota Corolla LE"
)
```

### Abacus.AI Processing
```python
processed = await integrator.send_to_abacus(
    {"project_data": data}, 
    "ai_development"
)
```

### DeepAgent Handoff
```python
handoff = await integrator.handoff_to_deepagent(
    project_data, 
    "Continue development with these specifications"
)
```

## 📊 Status Monitoring

### System Health
- Memory usage and growth
- API integration status
- Scheduler operation status
- Task completion rates
- Learning success metrics

### Performance Metrics
- Response times
- Error rates
- Integration availability
- Autonomous operation uptime

## 🛠️ Development

### Adding New Features

1. **New Integrations**: Add to `integrations/` directory
2. **Autonomous Tasks**: Extend `AutonomousScheduler` class
3. **Learning Algorithms**: Enhance `learn_from_interaction` method
4. **Memory Categories**: Add new categories to database schema

### Testing

```bash
# Run tests
pytest tests/

# Code formatting
black .

# Linting
flake8 .
```

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is a personal AI system for Randy Jordan. Feel free to fork and adapt for your own use case.

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Email: randy.ej.jordan7827@gmail.com

---

**Built with ❤️ for autonomous AI assistance**