# TimeAndDate Test Automation Framework

## Set up the environment for the Development

1. Clone the Repo
  
        git clone https://github.kyndryl.net/kyndryl-platform/kb-ist-automation

2. Navigate to the Repo folder

        cd kb-ist-automation

3. Create Virtual Environment

      ```sh
        python -m venv venv
      ```

4. Activate virtual environment

    Windows

    - Powershell

    ```ps
        .\venv\Scripts\Activate.ps1
    ```

    - (OR) CMD

        ```cmd
        venv\Scripts\activate.bat
        ```

    - (OR) Git Bash

        ```sh
        source venv/Scripts/activate
        ```

    **Mac**

    - Terminal or Bash

        ```sh
        source venv/bin/activate
        ```

5. Finally install the framework dependencies

    ```
    pip install -r requirements.txt
    ```
