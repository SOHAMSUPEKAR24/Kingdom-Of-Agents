# Kingdom of Agents 👑🤖

![Kingdom of Agents](https://img.shields.io/badge/Status-Active%20Development-success) ![Python](https://img.shields.io/badge/Backend-FastAPI%20%28Python%29-blue) ![Next.js](https://img.shields.io/badge/Frontend-Next.js%20%28React%29-black)

Kingdom of Agents is a highly advanced, autonomous, continuous self-improving super-intelligence platform. Designed to mimic a functional civilization, the architecture runs independent scientific experiments, manages specialized autonomous agents, and continually distills experiences to bypass redundant LLM calls using a deeply integrated capability-driven memory loop.

## 🚀 Core Features

- **Autonomous Execution Engine**: Executes complex generative tasks autonomously while self-monitoring for objective alignment.
- **Scientific Laboratory & Heartbeat**: A live `ScientificExperimentSandbox` proposes hypotheses, runs controlled automated experiments, and calculates success bounds in a continuous world-model background loop.
- **Intelligent Learning Governor**: Through Capability-Driven Mastery Campaigns, the civilization determines what it needs to learn.
- **Experience Reuse & LLM Bypass**: Before invoking external LLMs (Groq), the execution engine queries the Vector Database for existing high-confidence historical *doctrines* and *workflows*. If a match is found, the system intelligently bypasses the API call, executing the task directly from memory to save resources.
- **Knowledge Distillation Protocol**: Outputs from generative models are broken down into `extracted_facts`, `workflow_improvements`, and `doctrines_derived`, which are forever persisted in the system's memory topology.

## 🏗️ Architecture Stack

### Backend (Python / FastAPI)
- **FastAPI**: Asynchronous web framework managing the Kingdom's orchestrators, engines, and APIs.
- **PostgreSQL / SQLAlchemy**: Relational persistence tracking `ResearchCampaigns`, `ScientificExperiments`, and `ExecutionTraces`.
- **Qdrant (Vector DB)**: Embeds and stores distilled knowledge, capabilities, and semantic memories for the LLM bypass architecture.
- **Neo4j**: Stores topological graph networks mapping causality, lineages, and interactions.
- **Groq API**: Primary LLM integration for rapid intelligence inference.

### Frontend (Next.js / React)
- **Next.js 14+ (Turbopack)**: Real-time UI dashboard connecting users to the Kingdom's active scientific state.
- **Execution Dashboard**: Monitor the active execution traces, capability upgrades, and view how many **Model Calls** were avoided due to the Intelligence Governor's memory retrieval.
- **Civilization Parliament**: Visualization of hypothesis generation, causal reasoning loops, and multi-agent interaction.

## 🛠️ Getting Started

### Prerequisites
- Python 3.11+
- Node.js & npm
- PostgreSQL, Qdrant, and Neo4j instances running
- Groq API Key

### Running the Backend
1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Boot the FastAPI server (this initializes the background autonomous processes):
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Running the Frontend
1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
4. Access the dashboard at `http://localhost:3000`.

## 📜 Principles of the Civilization

1. **No objective = no experiment**. The system runs goal-directed infinite loops.
2. **Capability-First Learning**. Every hypothesis targets a designated capability gap.
3. The civilization becomes smarter when: **fewer model calls are needed** and **more knowledge is reused**, *not* just when more experiments run.

## 🛡️ License

This project is licensed under the MIT License.