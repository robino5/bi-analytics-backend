
# How to Deploy this project on Windows Server 2019
## Prerequisites
-  **[Python3.13](https://www.python.org/downloads/)**
-  **[Microsoft C++ Build Tools](https://www.microsoft.com/en-us/download/details.aspx?id=48159)**
- **[Apache 2.4](https://www.apachelounge.com/download/)**
# Python Installation Guide for Windows Server
This guide will walk you through the steps to install Python on a Windows Server machine.
## Step 1: Download Python Installer
1. Navigate to the official Python website at [python.org](https://www.python.org/downloads/).
2. Click on the "Downloads" tab.
3. Choose the latest version of Python that is compatible with your system architecture (32-bit or 64-bit).
## Step 2: Run the Python Installer
1. Once the installer is downloaded, double-click on it to run.
2. Check the box that says "Add Python x.x to PATH". This will ensure that Python is added to the system PATH environment variable, making it easier to run Python scripts from the command line.
3. Click "Install Now" to begin the installation process.
## Step 3: Verify Python Installation
1. Open Command Prompt by searching for "cmd" in the Start menu.
2. Type `python --version` and press Enter.
3. You should see the version number of Python printed to the console, confirming that Python has been successfully installed.


# Installing Microsoft Build Tools on Windows Server
Microsoft Build Tools are required for building and compiling certain Python packages, especially those with C/C++ extensions. Follow these steps to install Microsoft Build Tools on your Windows Server machine:
## Step 1: Download Microsoft Build Tools Installer
1. Visit the official Microsoft Build Tools download page at [Microsoft Build Tools](https://www.microsoft.com/en-us/download/details.aspx?id=48159).
2. Scroll down to the "All Downloads" section.
3. Under the "Tools for Visual Studio 2019" category, locate and click on "Build Tools for Visual Studio 2019".
## Step 2: Run the Installer
1. Once the installer is downloaded, double-click on it to run.
2. In the Visual Studio Installer window, select "Individual Components" from the left sidebar.
3. Look for "C++ build tools" and ensure it's checked.
4. Click on the "Install" button to begin the installation process.
## Step 3: Installation Progress
1. The installer will download and install the necessary components. This may take some time depending on your internet connection speed and system performance.
2. Follow any on-screen instructions if prompted during the installation process.
3. Once the installation is complete, you can close the Visual Studio Installer window.
Congratulations! You have successfully installed Microsoft Build Tools on your Windows Server machine.

# Install the Microsoft SQL Driver 17

Download and install from here: [Microsoft SQL Driver 17](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#version-17)

# Installing Apache HTTP Server 2.4 from Apache Lounge
This guide will help you install Apache HTTP Server 2.4 on your Windows Server machine from Apache Lounge, a popular source for precompiled Apache binaries.
## Step 1: Download Apache Binary
1. Visit the Apache Lounge website at [https://www.apachelounge.com/download/](https://www.apachelounge.com/download/).
2. Scroll down to the "Apache 2.4" section.
3. Choose the appropriate version of Apache 2.4 based on your system architecture (32-bit or 64-bit).
4. Click on the download link to save the Apache binary file to your local machine.
## Step 2: Extract Apache Files
1. Once the download is complete, navigate to the location where the Apache binary file was saved.
2. Right-click on the file and select "Extract All..." to extract its contents.
3. Choose a destination folder(preferred `C:/Apache24`) for the extracted files and click "Extract".
## Step 3: Configure Apache
1. Navigate to the folder where Apache was extracted and navigate to bin folder.
2. Run command `httpd.exe -k install` to install the apache2 service for windows.
3. Open the "conf" folder and create a new file named `httpd-backend.conf`.
4. Edit the `httpd-backend.conf` file using a text editor like Notepad.
5. Configure Apache according to your requirements, such as specifying server settings, listening ports, and document root directory.
6. Add the configuration file in the root `httpd.conf` located in `C:/Apache24/conf/httpd.conf` for apache with below line

```
Include conf/extra/httpd-backend.conf
```


## Step 4: Start Apache Server
1. Open Command Prompt with administrative privileges by searching for "cmd" in the Start menu, right-clicking on it, and selecting "Run as administrator".
2. Navigate to the "bin" folder within the Apache directory using the `cd` command.
3. Run the following command to start Apache:
```bash
httpd.exe -k start
```

### Step 1: Install `UV` dependency management tools for python globally.

```bash
pip install uv
```
### Step 2: Navigate to the `backend` directory and run below commands.
```bash
uv python install 3.13 # to install the latest version of python at the moment
uv venv # to create the virtual env in the backend directory
uv sync # to install the dependencies. check documentation for extra args
```
### Step 3: Install the `mod_wsgi` package for Apache2.4
```bash
uv add mod_wsgi
```
### Step 4: On the terminal run the below command to get the apache vhost configuration(With Virtual Env Activated)
```bash
mod_wsgi-express module-config
```
### Step 5: Copy the output of the above command and place it in `apache-vhosts.conf` which is on `backend` directory.

### Step 6: Restart the apache server with below command
```bash
httpd.exe -k restart
```

Now, the project has been succefully deployed to the server.
