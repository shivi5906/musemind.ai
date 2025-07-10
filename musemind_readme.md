# MuseMind.ai 🎭✨

**A Multi-Agent Framework for Poetic Expression and Creative Writing**

MuseMind.ai is an intelligent poetry creation and enhancement platform that leverages a sophisticated multi-agent system built on LangGraph. It empowers poets and creative minds to express themselves through AI-assisted writing, style analysis, and iterative improvement processes.

## 🚀 Overview

MuseMind.ai transforms the creative writing process through a collaborative ecosystem of specialized AI agents, each designed to handle specific aspects of poetry creation, critique, and enhancement. The system uses advanced RAG (Retrieval-Augmented Generation) techniques, vector databases, and recursive feedback loops to create compelling, stylistically-aware poetry.

## 🧠 Agent Architecture

### Core Creative Agents

#### 📝 `VerseCraftAgent` (Creator)
- **Primary Function**: Generates original poetry with emotional depth
- **Technologies**: RAG-enabled with author-based vector database
- **Capabilities**:
  - Accepts emotional arcs from `PlotWeaverAgent`
  - Incorporates feedback for iterative improvement
  - Adapts style based on historical poet data
  - Handles retry mechanisms for quality assurance

#### 🧠 `CritiFixAgent` (Critic)
- **Primary Function**: Quality assurance and structural analysis
- **Capabilities**:
  - Grammar and syntax checking
  - Flow and rhythm analysis
  - Metaphor coherence evaluation
  - Flags major issues for revision
  - Provides constructive feedback loops

#### 🧬 `LexiGuideAgent` (Lexical Enhancer)
- **Primary Function**: Vocabulary and linguistic enhancement
- **Capabilities**:
  - Suggests rich synonyms and metaphors
  - Identifies bland or weak word choices
  - **Recursive self-calling** for continuous improvement
  - Semantic richness optimization

### Structural & Analysis Agents

#### 🎭 `PlotWeaverAgent` (Plot Engine)
- **Primary Function**: Narrative structure and emotional arc design
- **Capabilities**:
  - Suggests compelling arcs (e.g., "Hope → Conflict → Resolution")
  - Provides structural guidance to `VerseCraftAgent`
  - Ensures emotional coherence throughout poems
  - Creates dynamic plot templates

#### 🧾 `PoetAnalyzerAgent` (Style Detector)
- **Primary Function**: Style analysis and comparison
- **Technologies**: RAG + vector similarity matching
- **Capabilities**:
  - Compares user output to historical poet databases
  - Identifies stylistic influences (Kafka, Rogue, etc.)
  - Provides style recommendations
  - Enables style-based poem categorization

#### 🧑‍🏫 `BeginnerGuideAgent` (Writing Coach)
- **Primary Function**: User growth and development tracking
- **Data Storage**: SQLite-based progress logging
- **Capabilities**:
  - Tracks user writing evolution
  - Suggests progressive writing challenges
  - Provides motivational support
  - Addresses creative blocks
  - Maintains style and frequency analytics

#### 🧪 `Data2PoetryAgent` (Journaling Transmuter)
- **Primary Function**: Transforms personal data into poetic form
- **Capabilities**:
  - Converts logs, thoughts, and conversations into poetry
  - Emotional diary stylization
  - Integrates with `VerseCraftAgent` in specialized mode
  - Personal narrative transformation

## 🧱 LangGraph Integration

### Complex Multi-Agent Workflow

The system utilizes LangGraph to create sophisticated agent interactions:

#### Core Architecture
- **Runnable Nodes**: Each agent implemented as `RunnableLambda`
- **State Management**: Seamless state passing between agents
- **Feedback Loops**: Intelligent routing based on agent decisions

#### Decision Agents
- **`FixRequiredDecider`**: Determines if `CritiFixAgent` flagged critical issues
- **`RetryComposer`**: Decides whether `VerseCraftAgent` should retry with new parameters
- **`StyleMatchDecider`**: Evaluates if style adjustments are needed based on analyzer feedback

## 🛠️ Technical Stack

- **Framework**: LangGraph for agent orchestration
- **Database**: 
  - Vector database for RAG operations
  - SQLite for user progress tracking
- **AI/ML**: Advanced language models with retrieval capabilities
- **Architecture**: Multi-agent system with recursive feedback loops

## 🎯 Key Features

### For Poets & Writers
- **Intelligent Poetry Generation**: AI-assisted creation with emotional depth
- **Style Analysis**: Compare your work to famous poets
- **Progressive Learning**: Personalized growth tracking and challenges
- **Creative Unblocking**: Overcome writer's block with guided inspiration

### For Developers
- **Modular Agent Design**: Easy to extend and customize
- **Robust Feedback Systems**: Multi-layered quality assurance
- **Scalable Architecture**: LangGraph-based for complex workflows
- **Data Integration**: Transform any text data into poetic form

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- LangGraph
- Vector database setup
- SQLite

### Installation
```bash
git clone https://github.com/shivi5906/musemind.ai.git
cd musemind.ai
pip install -r requirements.txt
```

### Quick Start
```python
from musemind import MuseMindFramework

# Initialize the multi-agent system
muse = MuseMindFramework()

# Create a poem with emotional arc
poem = muse.create_poem(
    theme="love and loss",
    style="romantic",
    emotional_arc="joy → melancholy → acceptance"
)

print(poem)
```

## 🤝 Contributing

We welcome contributions to MuseMind.ai! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Adding new agents
- Improving existing functionality
- Extending the LangGraph workflow
- Enhancing the RAG capabilities

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- Inspired by the rich tradition of computational creativity
- Dedicated to poets and creative minds everywhere

## 📞 Support

For questions, issues, or collaboration opportunities, please:
- Open an issue on GitHub
- Contact: [Shivam_Sharma@github](https://github.com/shivi5906) [Shivam_Sharma@twitter](https://x.com/btwits_ss31)
- Join our community discussions

---

*MuseMind.ai - Where artificial intelligence meets poetic soul* 🎭✨