INDaaS has three main components:

- collector is responsible for collecting data dependency information
- pia aims to quantify independence while preserving privacy (NOT IN THE SCOPE OF THIS PROJECT)
- sia provides a structural independence analysis

The related source code could be found from these three directories 
respectively.


Analysis was both done in SIA and on the collectors, the SIA folder contains the improvements already implemented.

To run the tests applicable in this project, one must go to sia/test/hard/ and run demo.py, within demo.py one must specify the location of the xml file to be analysed (included in folder, they range from result0.xml to result5.xml

Resulting graph will be created, and textual output with the risk groups and their probabilities will be displayed in the terminal.

Please refer to the report for the meaning of this.