# Video Streaming & File Explorer Server

A lightweight and efficient Flask-based server that allows you to browse, stream, and share files with a clean UI. Now supports **persistent storage**, **directory navigation**, and **hash-based URL shortening**.

## 🚀 Features

### **🔒 Persistent Storage**
- File mappings **survive server restarts**.
- Efficient indexing of files and directories.
- Hash-based short URLs for quick sharing.

### **📂 Efficient Directory Navigation**
- Handles **nested directories** seamlessly.
- Maintains **URL structure** when navigating.
- Provides a **file explorer-like interface**.

### **📁 File Type Support**
- **Media:** Videos, images, and audio files.
- **Documents:** PDFs, text files, and code files.
- **Generic handling** for unsupported formats.

### **🎨 User Interface**
- **Clean file explorer design** with icons.
- **Breadcrumb navigation** for easy folder access.
- **File type icons** for quick recognition.
- **Direct access to files and folders**.
- **Link sharing capabilities** with clipboard copy support.

## 🔧 Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/Geez14/Streaming-Server.git
cd Streaming-Server
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Run the Server**
```sh
python app.py
```
The server will start at `http://localhost:5000`.

>note see the .env file for PORT and ADDRESS configuration

## 🛠️ Future Enhancements
You can extend the project with additional features:
- 🔑 **User Authentication**
- 📊 **File Upload/Download Tracking**
- 🔎 **Search Functionality**
- 👁️ **File Preview Capabilities**
- 🖼️ **Custom Thumbnail Generation**
- 🎨 **Multiple Theme Support**
- 🖥️ **API Endpoints for Programmatic Access**

---

Enjoy streaming! 🎬📂

