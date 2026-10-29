# 🌐 Language Translation Tool

A simple and user-friendly language translation web application built using **Python** and **Streamlit**. It uses the **MyMemory Translation API** to translate text between supported languages.

## ✨ Features

- Translate text between supported languages.
- Simple and interactive Streamlit interface.
- Select source and target languages.
- Display translated text in the application.
- Download and save translation results.
- Uses a translation API without requiring an API key for basic use.

## 🛠️ Technologies Used

- Python
- Streamlit
- Requests
- MyMemory Translation API

## 📁 Project Structure

```text
CodeAlpha_LanguageTranslationTool/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Uplakshya2005/CodeAlpha_LanguageTranslationTool.git
```

### 2. Open the project directory

```bash
cd CodeAlpha_LanguageTranslationTool
```

### 3. Create and activate a virtual environment (optional but recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL shown in your terminal to use the application.

## 🔎 How to Use

1. Start the application.
2. Select the source language.
3. Select the target language.
4. Enter the text you want to translate.
5. Click the Translate button.
6. View and download the translated result.

## ⚠️ Limitations

- An internet connection is required to access the translation API.
- The free API may apply usage limits or temporarily become unavailable.
- Translation quality can vary by language and context.
- Very long text may need to be divided into smaller sections.

## 👨‍💻 Author

**Uplakshya2005**

GitHub: [@Uplakshya2005](https://github.com/Uplakshya2005)

## 📄 License

No license has been specified yet. Please add a license if you intend to permit others to reuse or modify this project.
