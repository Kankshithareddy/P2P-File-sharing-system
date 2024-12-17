
# **P2P LAN File Sharing System**

## **Objective**
Design and implement a Peer-to-Peer (P2P) file-sharing system that allows users to **share**, **search**, **download**, and **upload** files over a **Local Area Network (LAN)**.

---

## **Features**
1. **User Registration**  
   - Users can create a unique account using a username and password.

2. **File Sharing**  
   - Allows users to share files directly from their local machine.

3. **Search Functionality**  
   - Search for shared files by name, type, or description.

4. **File Download and Upload**  
   - Users can download shared files and upload new files to share with others.

5. **File Transfer**  
   - A robust file transfer protocol ensures successful peer-to-peer file sharing.

6. **LAN Connectivity**  
   - Connects peers over LAN using **IP addresses** or **hostnames**.

7. **User-Friendly Interface**  
   - The system provides a simple and intuitive interface for easy interaction.

---

## **Project Structure**
The project contains the following key components:
```
P2P-LAN-File-Sharing/
│
├── templates/             # HTML templates for the UI
│
├── peer_network.db        # SQLite database file
│
├── peer_server.py         # Python server implementation using Flask
│
└── requirements.txt       # Dependencies for the project
```

---

## **Dependencies**
The following libraries are required to run the project:
- **Flask**: Web framework for managing routes and rendering templates.
- **SQLite3**: Database for user registration and file metadata.
- **Mimetypes**: Library to detect file types for validation.
- **os**: For file path and system operations.
- **logging**: For logging server activities.

Install all dependencies using the following command:
```bash
pip install -r requirements.txt
```

---

## **How to Run**
1. **Clone the Repository**  
   ```bash
   git clone <repository_link>
   cd P2P-LAN-File-Sharing
   ```

2. **Set Up Database**  
   - The database is created automatically on the first run.

3. **Run the Server**  
   - Start the server using:
   ```bash
   python peer_server.py
   ```
   - By default, the server will run on `http://127.0.0.1:5000`.

4. **Access the Application**  
   - Open a browser and go to `http://127.0.0.1:5000`.

---

## **Endpoints**

| Route                | Method   | Description                             |
|-----------------------|----------|-----------------------------------------|
| `/`                  | GET      | Home page with login/register form      |
| `/register`          | POST     | Register a new user                     |
| `/login`             | POST     | Log in an existing user                 |
| `/dashboard`         | GET      | User dashboard                          |
| `/logout`            | GET      | Log out the current user                |
| `/share`             | POST     | Share a file (add to database)          |
| `/search?query=<q>`  | GET      | Search for files by name or type        |
| `/download/<file_id>`| GET      | Download a file from the server         |

---

## **File Sharing Workflow**
1. **Register/Login**  
   - Users must create an account or log in to access the dashboard.

2. **Share Files**  
   - Upload file paths to share with others.

3. **Search for Files**  
   - Search for files shared by others using keywords.

4. **Download Files**  
   - Click on available files to download them to the local machine.

---

## **Security Measures**
- Users are authenticated before sharing or downloading files.
- File paths are validated to ensure only accessible files are shared.
- SQLite is used securely with parameterized queries to prevent SQL injection.

---

## **Future Enhancements**
- Add file encryption for secure transfer.
- Implement a chat system for peer communication.
- Add file upload progress tracking.

---

## **Contributor**
- **P. Kankshitha Reddy**  
  Roll Number: **2201CS51**  
  Institution: **IIT Patna**  

---

## **License**
This project is licensed under the MIT License.

---
