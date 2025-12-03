# RxShield: AI-Powered Prescription Safety & DDI Checker

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Kivy](https://img.shields.io/badge/Kivy-2.3.0-orange?style=for-the-badge&logo=kivy&logoColor=white)
![Gemini AI](https://img.shields.io/badge/AI-Gemini%20Pro-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Prototype-yellow?style=for-the-badge)

**RxShield** is a desktop application designed to enhance medication safety by analyzing prescriptions for potential Drug-Drug Interactions (DDIs). Built with Python and Kivy, it leverages Google's **Gemini AI** to interpret handwritten prescriptions (OCR) and provide detailed safety analyses.

## 🚀 Features

*   **AI-Powered OCR**: Extract medication names from images of handwritten prescriptions using Google Gemini Vision.
*   **Drug Interaction Checker**: Analyze medication lists for potential interactions, side effects, and contraindications.
*   **Text-to-Speech (TTS)**: Listen to the analysis results for better accessibility.
*   **Secure Authentication**: User registration and login system with encrypted passwords (bcrypt).
*   **Report Generation**: Export analysis results to PDF or Word documents.
*   **History Tracking**: View past analyses and scanned prescriptions.
*   **Pharmacy Locator**: (Planned/Prototype) Find nearby pharmacies.

## 🛠️ Tech Stack

*   **Language**: Python
*   **Framework**: Kivy (UI)
*   **AI Model**: Google Gemini Pro & Gemini Pro Vision
*   **Database**: SQLite
*   **Authentication**: bcrypt
*   **Utilities**: gTTS (Google Text-to-Speech), ReportLab (PDF), python-docx (Word)

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/JayanthSD2003/Rx_Shield-A-Prescription-DDI-checker-v1.git
    cd Rx_Shield-A-Prescription-DDI-checker-v1
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory and add your Google Gemini API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## 🖥️ Usage

Run the application using:
```bash
python main.py
```

1.  **Register/Login**: Create an account to access the dashboard.
2.  **New Analysis**:
    *   Upload an image of a prescription.
    *   Or manually enter medication names.
3.  **View Results**: Read the AI-generated safety report or use the "Listen" button.
4.  **Export**: Save the report as a PDF or Word file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Developed by Jayanth SD*
