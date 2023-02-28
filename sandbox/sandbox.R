# --------------------------------------------------------------------------------------------
#------ Recreate a minimal workflow in EMLeditor
# --------------------------------------------------------------------------------------------

#------ load external libraries
# followed `#individual install:` in '20230210_iss135_emleditor/vignettes/EMLeditor.Rmd'
renv::install("devtools")
devtools::install_github("nationalparkservice/EMLeditor")
renv::install("EML")
library(EML)
library(EMLeditor)
library(stringr)
library(xml2)

#------ load project functions
rm(list = ls())
source("R/set_cui2.R")

#####
# run a function
my_metadata <- EML::read_eml("sandbox/2022_NCRN_forest_vegetation_metadata.xml", from = "xml")
my_xml <- xml2::read_xml("sandbox/2022_NCRN_forest_vegetation_metadata.xml")

mytest <- EMLeditor::set_cui(my_metadata, cui_code = "PUBLIC")
EML::write_eml(my_metadata, "sandbox/my_metadata.xml")
