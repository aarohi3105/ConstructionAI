# 🏗️ Multimodal Construction Intelligence Platform

**Skill Wallet Capstone Project 1** | Platform ID: `6ac4c98d1dcde6d7857c1642`

A Generative AI decision-support system for the construction and real estate industry, built with Python, Streamlit, and Google Gemini.

## 🚀 Features

| Tab | Module | Standards |
|---|---|---|
| 🦺 PPE Safety Audit | Multimodal image analysis for worker PPE compliance | OSHA 1926, IS 456 |
| 🔬 Crack Diagnostics | Defect classification, severity scoring, and repair guidance | IS 13311, ACI 224R |
| 💰 Valuation & Planning | INR cost estimation, CAPEX tracking, and architectural rendering | IS 456, market rates |
| 🌤️ Site Assistant | Weather-aware protocols and AI engineering chatbot | Relevant IS/OSHA guidance |

## 🛠️ Tech Stack

- **AI:** Google Gemini multimodal API
- **Frontend:** Streamlit with custom CSS
- **Rendering:** Pollinations AI / Flux
- **Image processing:** Pillow
- **Containerization:** Docker
- **Standards references:** OSHA 1926, IS 456:2000, IS 13311, ACI 224R

## ⚡ Quick Start — Run with Docker

Docker lets you run the application in an isolated container without manually installing Python or the project's dependencies.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- The project files downloaded and extracted into a folder.

### 1. Open the project folder

Extract the project ZIP and open PowerShell in the folder containing the `Dockerfile` and `requirements.txt`.

Your folder should look similar to this:

```text
genAI Project 1/
├── app.py
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── README.md
├── .streamlit/
├── modules/
└── Photos/
```

### 2. Build the Docker image

Run:

```powershell
docker build -t constructionai:1.0 .
```

This builds the application image and installs the required Python packages.

### 3. Start the application

Run:

```powershell
docker run -d --name constructionai-app -p 8502:8501 constructionai:1.0
```

### 4. Open the application

Visit:

**http://localhost:8502**

The Streamlit application should now be available in your browser.

### Useful Docker commands

Check whether the container is running:

```powershell
docker ps
```

View application logs:

```powershell
docker logs constructionai-app
```

Stop the application:

```powershell
docker stop constructionai-app
```

Start it again:

```powershell
docker start constructionai-app
```

Remove the stopped container:

```powershell
docker rm constructionai-app
```

To rebuild after changing the source code, stop and remove the old container, then rebuild the image and create a new container.

## 🔑 Configure the Gemini API Key

The application supports entering a Google Gemini API key through the sidebar, according to the application's current implementation.

1. Obtain your own API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Open the application at `http://localhost:8502`.
3. Enter your key in the sidebar's API-key field, if prompted.

**Security:** Never publish your API key in the source code, README, Docker image, or public repository. Each user should use their own key.

**Demo mode:** The project is designed to support demonstration behavior without an API key. Available features may differ when live AI access is unavailable.

## 🐍 Alternative — Run without Docker

If you prefer running the application directly with Python:

1. Install a compatible Python version and open PowerShell in the project folder.
2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Start Streamlit:

```powershell
streamlit run app.py
```

Open the local URL printed in the terminal, usually `http://localhost:8501`.

## 📁 Project Structure

```text
genAI Project 1/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
├── .streamlit/
│   └── config.toml
├── Photos/
└── modules/
    ├── __init__.py
    ├── styles.py
    ├── gemini_client.py
    ├── tab_ppe.py
    ├── tab_crack.py
    ├── tab_valuation.py
    └── tab_assistant.py
```

## ☁️ Deployment Options

The application can potentially be deployed to a container-capable hosting platform or Streamlit Community Cloud.

For Streamlit Community Cloud, publish the project to GitHub, connect the repository at [share.streamlit.io](https://share.streamlit.io/), select `app.py` as the entry point, and configure required secrets in the platform's settings.

Deployment compatibility depends on the hosting platform and the application's dependencies.

## 📋 Kanban Epics

| Epic | Coverage |
|---|---|
| Pre-requisites | Python, Streamlit, and modular project structure |
| Epic 1 | Requirements and environment setup |
| Epic 2 | PPE Safety Vision and Crack Diagnostics |
| Epic 3 | Project Planning and Real Estate Valuation |
| Epic 4 | Multimodal AI and JSON Data Contracts |
| Epic 5 | Site Chatbot and Weather Advisory |
| Epic 6 | Interface, Testing, and Cloud Deployment |

## ⚠️ Important Disclaimer

This project is intended for educational and decision-support demonstrations. AI-generated safety assessments, crack classifications, repair suggestions, valuations, and construction guidance must be independently verified by qualified professionals before real-world use. The output should not be treated as certified engineering advice or a substitute for applicable codes and professional inspection.

---

*Built with ❤️ as Skill Wallet Capstone Project 1*