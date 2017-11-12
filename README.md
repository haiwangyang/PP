# PP
* Parse PicoGreen/RiboGreen results from from Gemini XPS Microplate Reader
* Convert 384 well plate format to 96 well plate format
* Write to different excel spreadsheets
# Four positions of 96-well plate in a 384-well plate
 a1 | a2
---- ----
 b1 | b2
 
1st | 2nd
---- ----
3rd | 4th
# Input
* -f (data/pico.reads.txt)
main data file of PicoGreen (or RiboGreen) reads from Gemini XPS Microplate Reader in 384-well plate format (16 row x 24 column)
* -s (data/standards.txt)
standard data file of Well IDs (of 384-well plate) and their corresponding known concentration of DNA/RNA standards (ng/ul)
* -a1 (1st_plate)
Spreadsheet name of the 1st plate
* -a2 (2nd_plate)
Spreadsheet name of the 2nd plate
* -b1 (3rd_plate)
Spreadsheet name of the 3rd plate
* -b2 (4th_plate)
Spreadsheet name of the 4th plate
# Output file
* data/pico.reads.xlsx
An excel file with six spreadsheets:
(1) raw data in 384-well plate; 
(2) reads of standard and their known concentration; 
(3) 1st_plate; 
(4) 2nd_plate; 
(5) 3rd_plate; 
(6) 4th_plate; 
# Usage
python Parse.Pico.Ribo.Reads.py -f data/pico.reads.txt -s data/standards.txt -a1 1st_plate -a2 2nd_plate -b1 3rd_plate -b2 4th_plate
