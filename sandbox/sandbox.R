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
source("sandbox/functions/")

#####
# run a function
my_metadata <- EML::read_eml("sandbox/2022_NCRN_forest_vegetation_metadata.xml", from = "xml")
my_xml <- xml2::read_xml("sandbox/2022_NCRN_forest_vegetation_metadata.xml")

# re-create the output of EML::read_eml()
# create an empty list that matches the length of known-correct list
my_testlist <- vector(mode = 'list', length = length(my_metadata))
names(my_testlist) <- names(my_metadata)
# re-create first element `@context`
my_testlist$`@context` <- vector(mode = 'list', length = length(my_metadata$`@context`))
my_

my_meta2 <- set_cui(my_metadata, "PUBLIC")


mytest <- xml2::xml_find_all(my_xml, ".//creator")
cat(as.character(mytest))
xml2::xml_text(xml2::xml_children(mytest))

# dissect the function
## EML::read_eml
#-- input: a .xml file containing metadata produced by [EMLassemblyline](https://ediorg.github.io/EMLassemblyline/), but will also work with any number of other EML generators (e.g. [ezEML](https://ezeml.edirepository.org/eml/)
#-- output: an R list containing metadata extracted from the function input
#-- calls or depends on:
#---- `emld::as_emld.xml_document()`(https://github.com/ropensci/emld/blob/master/R/as_emld.R) **note** there are functions in `emld::as_emld()` for other data structures (e.g., json) but I'm starting with xml.
#---- `emld::add_context()` line 142 https://github.com/ropensci/emld/blob/master/R/as_emld.R
#---- 'xml2::read_xml()` just find the python library equivalent to `library(xml2)` that reads/writes xml to nodesets
#---- `xml2::as_list()` use `library(xml2)` equivalent, find a python library will return a python dict instead of R list
#####

#####
# run a function
my_meta2 <- EMLeditor::set_cui(my_metadata, "PUBLIC")
# dissect the function
# line 449 here: https://github.com/nationalparkservice/EMLeditor/blob/main/R/editEMLfunctions.R
doc <- my_metadata$additionalMetadata
x <- length(doc)
my_metadata$additionalMetadata$metadata$CUI <- "testtext"
exist_cui <- NULL
for (i in seq_along(doc)) {
  if (suppressWarnings(stringr::str_detect(doc[i], "CUI")) == TRUE) {
    seq <- i
    exist_cui <- doc[[i]]$metadata$CUI
  }
}
#####
