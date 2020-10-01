rm(list = ls())

library(httr)
library(xml2)
library(tidyverse)
library(stringr)

no.xml <- GET("https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/ObtenerIndicadoresEconomicos?Indicador=317&FechaInicio=01/01/2019&FechaFinal=25/09/2020&Nombre=BraulioVillalobos&SubNiveles=N&CorreoElectronico=baluca26@gmail.com&Token=########")

contenido.texto <- content(no.xml, as = "text")

contenido.texto <- sub('.*</xs:schema>\r\n  ','',contenido.texto)
contenido.texto <- str_remove(contenido.texto,"</DataSet>")

cat(contenido.texto,file = "outfile2.txt",sep="\n")


