# Asynchronous TCP Port Scanner
<p align="center">
 <img src="https://github.com/user-attachments/assets/d0684c48-6d07-4363-b927-25adf1cad48f" width="968" height="578" alt="image"/>
</p>

A high-performance asynchronous TCP port scanner developed using Python’s asyncio, designed for ethical security testing, network reconnaissance, and academic cybersecurity projects.
The tool supports IPv4 and IPv6, configurable concurrency, timeout handling, and exportable scan results (JSON / CSV).

### Project Overview:

This project implements a non-blocking TCP port scanner that efficiently scans multiple ports concurrently without relying on traditional threading. It is optimized for speed, scalability, and clarity, making it suitable for students, security researchers, and network administrators.

### Features:

- Asynchronous TCP scanning using `asyncio`.
- IPv4 and IPv6 support with automatic detection
- Custom port ranges and single-port scanning
- Adjustable concurrency (async-based)
- Configurable timeout (expiry time)
- Verbose and clean output modes
- Result export in JSON and CSV
- Scan summary with statistics
- Graceful interruption handling (Ctrl + C)
- Ethical-use oriented design

### Installation:
To run this project locally, follow these steps:

- __Clone the repository:__ <br>


         git clone https://github.com/Shaikh-Aiman/Asynchronous-TCP-Port-Scanner

- __Navigate to the project directory:__
cd Asynchronous-TCP-Port-Scanner
- __Ensure you have Python installed on your system.__
- __Install the required dependencies.__
- __Run the application:__
    `python main.py`

---

### Execution Guide:

- __Basic Execution:__ Scans common ports (1–1024) on localhost. <br>

         python main.py

- __Scan a Target IP or Domain:__

         python main.py -i 192.168.1.1
         python main.py -i example.com

- __Scan a Port Range:__

         python main.py -p 1-1024
         python main.py -i 192.168.1.1 -p 80-443

- __Scan a Single Port:__

         python main.py -i example.com -p 443

- __IPv6 Scanning:__ The scanner automatically detects IPv6 and uses the appropriate socket configuration.

         python main.py -i ::1 -p 22-80

- __Control Scan Speed (Concurrency):__ Higher values increase scanning speed, very high values may stress the network or system.

         python main.py -t 300

- __Configure Timeout (Expiry Time):__ Waits 5 seconds per port before marking it as filtered.

         python main.py -e 5

- __Verbose Mode (Detailed Output):__ It displays Open ports, Closed ports, Filtered ports and Errors (if any).

         python main.py -v

- __Show Only Open Ports:__

         python main.py --open-only

- __Export Scan Results: The scanner supports exporting results in JSON and CSV formats.__

- __JSON Export:__ Exports all scan results in structured JSON format.

          python main.py -o results.json

- __CSV Export (export.csv):__ Exports scan results in spreadsheet-friendly CSV format.

          python main.py -o export.csv --format csv

### ⚠️ Ethical Usage Disclaimer

This tool is intended strictly for educational purposes and authorized security testing.
Scan only systems you own or have explicit permission to test.
Unauthorized scanning may violate laws and regulations.

<p align="center">
  <img src="https://github.com/user-attachments/assets/db4f8484-de61-4e03-8dd3-e85deaefa6ff" alt="scan-complete-alan-walker">
</p>



  

