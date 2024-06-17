<center>

# The Slay Girlies : Smart Grid
Smart Grid Summer Project for Imperial EEE/EIE 2023/24

---

**_Jennifer Emezie, Dhruv Ruda, Sophie Jayson, Rares Yousif, Adam El Jaafari, Arundhathi Pasquereau_**

---

</center>

![Logo](./client/src/assets/logo.png)

## Build instructions
In order to build the project once must follow the following instructions.

Firstly:
- ensure [`gridweb.py`](Grid/gridweb.py) is loaded into the main memory of the Grid SMPS.
- ensure [`final.py`](Storage/final.py) is loaded into the main memory of the Storage SMPS.
- ensure [`mppt final.py`](PV/mppt%20final.py) is loaded into the main memory of the PV SMPS.
- ensure  same with LED code.
- ensure all requirements are installed, this can be done by running in the root of the project the command `pip install -r requirements.txt`.

Secondly run the command `cd server` and run `python3 flaskBackendServer.py` now open another terminal and go back to the root of the project.

Lastly run  the command `cd multithreadserver ` and run the command  `python3 trialserver.py` TODO CHANGE FILE NAMES

## Contribution Table

**Key:** o = Main Contributor; v = Co-Author


| Task                | Files                                                                                                                                     | Jennifer | Dhruv | Sophie | Rares | Adam | Arundhathi |
|:--------------------|:------------------------------------------------------------------------------------------------------------------------------------------|:--------:|:-----:|:------:|:-----:|:----:|:----------:|
| Grid                | [`gridweb.py`](Grid/gridweb.py)                                                                                                            |          |       |        |   o   |      |            |
| Storage             | [`final.py`](Storage/final.py)                                                                                                                       |    o     |       |        |       |      |            |
| PV                  | [`mppt final.py`](PV/mppt%20final.py), [`irradience tracker.py`](PV/irradience%20tracker.py)                                                                                                             |          |   o   |        |       |      |            |
| LED (Load)          |                                                                                                                     |          |       |        |       |      |     o      |
| Socket Server       | [`trialserver.py`](multithreadserver/trialserver.py)                                                                                                                     |          |       |   o    |       |      |            |
| Web Frontend        | [`client`](client)                                                                                                                       |          |       |        |       |   o  |            |
| Web Backend         | [`flaskBackendServer.py`](server/flaskBackendServer.py)                                                                                                             |          |       |        |       |   o  |            |
| Algorithm           | [`mltraining.py`](ml/mltraining.py), [`helper.py`](multithreadserver/helper.py)                                                                                                                     |          |       |   o    |       |   o  |            |

___
## Directory Structure
This is the directory structure that was used for the project.

Directory    | Use
:-----------:|:------------------------------------------------
[`client`](./client/)     | React webpage
[`server`](./server/)     | Flask Server
[`multithreadedserver`](./multithreadserver/)         | Socket Server - Communication with picos
[`ml`](./ml/)         | Machine Learning 
[`Storage`](./Storage/)    | Capacitor Code
[`PV`](./PV/)         | PV Code
[`Grid`](./Grid/)       | Grid Code
___
