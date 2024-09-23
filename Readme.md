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
- ensure [`LED1.py`](./LED/LED1.py) is loaded into the main memory of the LED SMPS.
- ensure all requirements are installed, this can be done by running in the root of the project the command `pip install -r requirements.txt`.

Secondly run the command `cd server` and run `python3 webserver.py` now open another terminal and run the command `python3 dataserver.py` .

Lastly run the commands `cd client`, then run `npm install` and finally run `npm start` to start the webpage.

## Contribution Table

**Key:** o = Main Contributor; v = Co-Author


| Task                | Files                                                                                                                                     | Jennifer | Dhruv | Sophie | Rares | Adam | Arundhathi |
|:--------------------|:------------------------------------------------------------------------------------------------------------------------------------------|:--------:|:-----:|:------:|:-----:|:----:|:----------:|
| Grid                | [`gridweb.py`](Grid/gridweb.py)                                                                                                            |          |       |        |   o   |      |            |
| Storage             | [`final.py`](Storage/final.py)                                                                                                                       |    o     |       |        |       |      |            |
| PV                  | [`mppt final.py`](PV/mppt%20final.py), [`irradience tracker.py`](PV/irradience%20tracker.py)                                                                                                             |          |   o   |        |       |      |            |
| LED (Load)          | [`LED1.py`](./LED/LED1.py)                                                                                                                 |          |       |        |       |      |     o      |
| Socket Server       | [`dataserver.py`](server/dataserver.py)                                                                                                                     |          |       |   o    |       |      |            |
| Web Frontend        | [`client`](client)                                                                                                                       |          |       |        |       |   o  |            |
| Web Backend         | [`webserver.py`](server/webserver.py)                                                                                                             |          |       |        |       |   o  |            |
| Algorithm           | [`mltraining.py`](ml/mltraining.py), [`helper.py`](multithreadserver/helper.py)                                                                                                                     |          |       |   o    |       |   o  |            |

___
## Directory Structure
This is the directory structure that was used for the project.

Directory    | Use
:-----------:|:------------------------------------------------
[`client`](./client/)     | React webpage
[`server`](./server/)     | Flask web server and data server
[`ml`](./ml/)         | Machine learning 
[`Storage`](./Storage/)    | Capacitor code
[`PV`](./PV/)         | PV code
[`Grid`](./Grid/)       | Grid code
[`LED`](./LED/)       | LED code
[`db`](./db/)       | Data base code

___
## Documents 
Please see our project write up for more detail regarding the engineering behind the teams design [`Smart_Grid.pdf`](./Smart_Grid.pdf) and our [Interim Presentation](https://www.canva.com/design/DAGGnyTdIyU/v3l1MlDU6QnrnRmbECQcOQ/view?utm_content=DAGGnyTdIyU&utm_campaign=designshare&utm_medium=link&utm_source=editor).
___

## Results
Below you can see a video of the smart grid running. 
[![Smart Grid Video](https://img.youtube.com/vi/qLZ7yFC_RUk/0.jpg)](https://youtu.be/qLZ7yFC_RUk)
