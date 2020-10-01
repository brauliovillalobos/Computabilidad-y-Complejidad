#!/bin/bash

#Manera 1 - Invariable, no interactivo, sin parametros
Rscript BCCR.R		#Ejecuta el R
python3 Parser.py	#Ejecuta el Python
rm outfile2.txt	#Borra el archivo creado en R


#Manera 2 - Pasa como parametros
#Rscript $1
#python3 $2
#rm outfile2.txt
