# 🎙️ Jarvis Voice Assistant (Windows 11 Production Edition)

An asynchronous, object-oriented Python voice assistant engineered specifically for Windows 11 Home/Pro environments. Running on a lightweight, thread-safe wake-word architecture, it integrates seamless online speech evaluation, system sound matrices redirection, application management, and live browser querying.

---

## 🚀 Key Features

* **Wake-Word Processing Layer:** Listens natively in background mode until "Jarvis" or "Jar" is spoken, preventing buffer overflows and log flooding.
* **Advanced Dynamic NLP Parsing:** Evaluates search expressions like *"Jarvis, find the fastest car in the world"* safely via deep sub-string inspection.
* **OS Automation API Hooks:** Controls sound mixer devices natively via Windows shell endpoints and forces instant workstation desktop locking.
* **Process Orchestration:** Instantly spins up target system diagnostics software (e.g., Task Manager) or local text layout applications.

---

## 🛠️ Tech Stack

* **Runtime:** Python 3.11+
* **Speech-to-Text Layer:** SpeechRecognition (Google API Web-Backend)
* **Text-to-Speech Engine:** PyTTSx3 (Native Windows SAPI5 Offline Engine)
* **Audio I/O Framework:** PyAudio (PortAudio binaries)

---

## 📦 Production Deployment

### 1. Clone the environment layout:
```bash
git clone [https://github.com/lev173/Jarvis-Voice-Assistant.git](https://github.com/lev173/Jarvis-Voice-Assistant.git)
cd Jarvis-Voice-Assistant
