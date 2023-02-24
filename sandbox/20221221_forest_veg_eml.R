

## Script Overview -----------------------------------------------------------------------------------------------------
# Title: NPS EML Creation Script
#
# Summary: This code creates an EML file for a data package by leveraging several functions within the EMLassemblyline
# package. In this case the example inputs are for a EVER Veg Map AA dataset and are meant to either be run as a test
# of the process or to be replaced with your own content. This is a step by step process where each section (indicated
# by dashed lines) should be reviewed, edited if necessary, and run one at a time. After completing a section there is
# often something to do external to R (e.g. open a text file and add content). Several EMLassemblyline functions are
# decision points and may only apply to certain data packages. The 'Create an EML File' section has the make_eml()
# function to put together a validated EML metadata file. Future updates to this script will help bring in additional
# functions from the EMLeditor package (part of the NPSdataverse) that are used to populate NPS DataStore specific tags.

# Contributors: Judd Patterson (judd_patterson@nps.gov) and Rob Baker (robert_baker@nps.gov)
# Last Updated: November 30, 2022

## Install and Load R Packages -----------------------------------------------------------------------------------------
# Install packages - uncomment the next three lines if you've never installed EMLassemblyline before
# install.packages("devtools")
# If you run into errors installing packages from github on NPS computers you
#may first need to run:
# options(download.file.method="libcurl") # https://stackoverflow.com/questions/53845962/having-trouble-getting-devtoolsinstall-github-to-work-in-r-on-win-7-64bit-ma
# options(download.file.method="wininet")
# devtools::install_github("EDIorg/EMLassemblyline")


# example files from here: https://nationalparkservice.github.io/NPS_EML_Script/comprehensive_guide.html
# example files are saved here: ./NPS_EML_Script/NPS_EML_Script/Example_files

# installing github repo from .zip
# 1) download .zip of repo # https://stackoverflow.com/questions/2751227/how-to-download-source-in-zip-format-from-github
## put this in  your browser: github.com/EDIorg/EMLassemblyline/zipball/main/
# 2) devtools::install_local() # https://stackoverflow.com/questions/17366772/install-r-packages-from-github-downloading-master-zip
# devtools::install_local("EMLassemblyline.zip")

# Load packages
library(EMLassemblyline)
library(lubridate)
library(tidyverse)

## Set Overall Package Details -----------------------------------------------------------------------------------------
# All of the following items should be reviewed and updated to fit the package at hand. For vectors with more than one
# item, keep the order the same (i.e. item #1 should correspond to the same file in each vector)

# Metadata filename - becomes the filename, so make sure it ends in _metadata to comply with data package specifications
metadata_id <- "2022_NCRN_forest_vegetation_metadata"

# Overall package title
package_title <- "NCRN Forest Vegetation Monitoring Data 2006-2022"

# Description of data collection status - choose from 'ongoing' or 'complete'
data_type <- "complete"

# Path to data file(s)
# working_folder <- paste0(str_trim(getwd()),"/NPS_EML_Script/NPS_EML_Script/Example_files") # this varies depending on where you saved the example files
# working_folder <- "C:\\Users\\cwainright\\OneDrive - DOI\\General\\Annual-Data-Packages\\2022\\NCRN_Cumulative_ForestVeg"
working_folder <- "C:\\Users\\cwainright\\OneDrive - DOI\\Documents - NPS-NCRN-Forest  Veg\\General\\Annual-Data-Packages\\2022\\20221221\\EML"
setwd(working_folder)
save_folder <- paste0(working_folder)# created a new folder to avoid accidental over-writing
# Vector of dataset filenames:
# data_files <- c("qry_Export_AA_Points.csv",
#                 "qry_Export_AA_VegetationDetail.csv")
# If the only .csv files in your working_folder are datasets for your data package, you can use:
data_files <- list.files(pattern="*.csv")

# Vector of dataset names (brief name for each file)
# data_names <- c("TEST_AA Point Data",
#                 "TEST_AA Vegetation Data")
data_names <- gsub(".csv", "", data_files)

# Vector of dataset descriptions (about 10 words describing each file). Descriptions will be used in auto-generated
# tables within the ReadMe and DRR. If you need to use more than about 10 words, consider putting that information in
# the abstract, methods, or additional info sections.
# data_descriptions <- c(rep("ADD REAL TEXT", length(data_names))) # if we want the same info for all CSVs
data_descriptions <- c("CommonNames_20221220 provides plant taxonomy data. One row is one species.",
                       "CWD_20221220 provides coarse woody debris (CWD) I&M data. One row is one piece of CWD.",
                       "Events_20221220 provides sample event I&M data. One row is one sample event.",
                       "Foliage_Conditions_202021220 provides foliage I&M data. One row is foliage data for one species during one sample event.",
                       "Herbs_20221220 provides herb I&M data. One row is herb data for one species during one sample event.",
                       "Plot_Floor_20221220 provides plot floor I&M data. One row is plot floor data for one sample event.",
                       "Plots_20221220 provides plot location data. One row is one sampling plot.",
                       "Quadrat_Conditions_20221220 provides quadrat habitat data. One row is quadrat data for one sample event.",
                       "Saplings_20221220 provides woody plant sapling I&M data. One row is sapling data for one species for one sample event.",
                       "Seedlings_20221220 provides tree seedling I&M data. One row is tree seedling data for one species for one sample event.",
                       "Shrub_Seedlings_20221220 provides shrub seedling I&M data. One row is shrub seedling data for one species for one sample event.",
                       "Shrubs_20221220 provides shrub I&M data. One row is shrub data for one species for one sample event.",
                       "Stems_20221220 provides plant stem I&M data. One row is stem data for one species for one sample event.",
                       "Tag_History_20221220 provides the disposition of tagged plants. One row is one tagged plant.",
                       "Tree_Sapling_Conditions_20221220 provides tree sapling I&M data. One row is the condition of one sapling for one sample event.",
                       "Trees_20221220 provides tree I&M data. One row is one tree for one sample event.",
                       "Vines_20221220 provides vine I&M data. One row is one vine for one sample event.")

# Tell EMLassemblyline where your files will ultimately be located. Create a vector of dataset URLs - for DataStore. I
# recommend setting this to the main reference page. All data files from a single data package can be accessed from the
# same page so the URLs are the same.

# The code from the draft reference you initiated above (replace 293181 with your code)
DSRefCode<-2296604

# No need to edit this
DSURL<-paste0("https://irma.nps.gov/DataStore/Reference/Profile/", DSRefCode)

# No need to edit this
data_urls <-c(rep(DSURL, length(data_files)))

# Single file or Vector (list) of tables and fields with scientific names that can be used to fill the taxonomic coverage metadata. Add
# additional items as necessary. Comment these out and do not run FUNCTION 5 (below) if your data package does not
# contain species information.
# data_taxa_tables <- c("qry_Export_AA_VegetationDetail.csv")
data_taxa_tables <- c("CommonNames_20221220.csv")
#alternatively, if you have multiple files with taxanomic info:
# data_taxa_tables <-c("qry_Export_AA_VegetationDetails1.csv", "qry_Export_AA_VegetationDetails2.csv", "etc.csv")
data_taxa_fields <- c("Latin_Name")

# Table and fields that contain geographic coordinates and site names to fill the geographic coverage metadata
# Comment these out and do not run FUNCTION 4 (below) if your data package does not contain geographic information.
# data_coordinates_table <- "Sites_20221215.csv"
# data_latitude <- "Y" # COMMENTED OUT TO BREAK FUNCTION 4 BELOW (i.e., avoid over-writing the existing geographic_coverage.txt file)
# data_longitude <- "X" # DO WE NEED THIS OR DO WE JUST USE:
# data_sitename <- "IMLOCID" # "C:\Users\cwainright\OneDrive - DOI\Documents - NPS-NCRN-Forest  Veg\General\Annual-Data-Packages\2022\20221220\EML\geographic_coverage.txt"

# Start date and end date. This should indicate the first and last data point in the data package (across all files) and
# does not include any planning, pre- or post-processing time. The format should be one that complies with the
# International Standards Organization's standard 8601. The recommended format for EML is: YYYY-MM-DD, where Y is the
# four digit year, M is the two digit month code (01 - 12 for example, January = 01), and D is the two digit day of the
# month (01 - 31).
startdate <- ymd("2006-06-27") # 2006-06-27
enddate <- ymd("2022-09-22") # 2022-09-22

## EMLassemblyline Functions -------------------------------------------------------------------------------------------
# The next set of functions are meant to be considered one by one and only run if applicable to a particular
# data package. The first year will typically see all of these run, but if the data format and protocol stay constant
# over time it may be possible to skip some in future years. Additionally some datasets may not have geographic or
# taxonomic component.

# FUNCTION 1 - Core Metadata Information
# Creates blank TXT template files for the abstract, additional information, custom units, intellectual
# rights, keywords, methods, and personnel. Be sure the edit the personnel text file in Excel as it has columns.
# Typically these files can be reused between years. Currently this inserts a Creative Common 0 license.
# NOTE that if these files already exist from a previous run, they are not overwritten.
template_core_metadata(path = save_folder,
                       license = "CC0")

# FUNCTION 2 - Data Table Attributes
# Creates an "attributes_datafilename.txt" file for each data file. This can be opened in Excel
# (we recommend against trying to update these in a text editor) and fill in/adjust the columns for attributeDefinition,
# class, unit, etc. refer to https://ediorg.github.io/EMLassemblyline/articles/edit_tmplts.html for helpful hints and
# view_unit_dictionary() for potential units. This will only need to be run again if the attributes (name, order or
# new/deleted fields) are modified from the previous year.
# NOTE that if these files already exist from a previous run, they are not overwritten.
template_table_attributes(path = save_folder,
                          data.table = data_files,
                          write.file = TRUE)

# FUNCTION 3 - Data Table Categorical Variable
# Creates a "catvars_datafilename.txt" file for each data file that has columns with a class = categorical.
# These txt files will include each unique 'code' and allow input of the corresponding 'definition'.NOTE that since the
# list of codes is harvested from the data itself, it's possible that additional codes may have been relevant/possible
# but they are not automatically included here. Consider your lookup lists carefully to see if additional options should
# be included (e.g if your dataset DPL values are all set to "Accepted" this function will not include "Raw" or
# "Provisional" in the resulting file and you may want to add those manually).
# NOTE that if these files already exist from a previous run, they are not overwritten.
template_categorical_variables(path = save_folder,
                               data.path = working_folder,
                               write.file = TRUE)

# FUNCTION 4 - Geographic Coverage
# Creates a geographic_coverage.txt file that lists your sites as points as long as your coordinates are
# in lat/long. If your coordinates are in UTM it is probably easiest to convert them first or create the
# geographic_coverage.txt file another way (see https://github.com/nationalparkservice/QCkit for R functions that will
# convert UTM to lat/long).
# template_geographic_coverage(path = save_folder,
#                              data.path = working_folder,
#                              data.table = data_coordinates_table,
#                              lat.col = data_latitude,
#                              lon.col = data_longitude,
#                              site.col = data_sitename,
#                              write.file = TRUE)

# FUNCTION 5 - Taxonomic Coverage
# Creates a taxonomic_coverage.txt file if you have taxonomic data. Currently supported authorities are
# 3 = ITIS, 9 = WORMS, and 11 = GBIF.
template_taxonomic_coverage(path = save_folder,
                            data.path = working_folder,
                            taxa.table = data_taxa_tables,
                            taxa.col = data_taxa_fields,
                            taxa.authority = c(3,11),
                            taxa.name.type = 'scientific',
                            write.file = TRUE)

## Create an EML File --------------------------------------------------------------------------------------------------
# Run this (it may take a little while) and see if it validates (you should see 'Validation passed'). Additionally there
# could be some issues to review as well. Run the function 'issues()' at the end of the process to get feedback on items
# that might be missing or need attention.
make_eml(path = save_folder,
         dataset.title = package_title,
         data.table = data_files,
         data.table.name = data_names,
         data.table.description = data_descriptions,
         data.table.url = data_urls,
         temporal.coverage = c(startdate, enddate),
         maintenance.description = data_type,
         package.id = metadata_id)

## EMLeditor Functions (COMING SOON!) ----------------------------------------------------------------------------------
# Now that you have valid EML metadata, you need to add NPS-specific elements and fields. For instance, unit
# connections, DOIs, referencing a DRR, etc. To do that, use the R/EMLeditor package at
# https://github.com/nationalparkservice/EML_editor.

# Some functions from EMLeditor that will be critical to run include:
# set_cui, set_doi, set_drr and set_content_units, set_producing_units (with more to come soon).
