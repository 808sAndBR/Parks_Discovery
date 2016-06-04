# setwd("Projects/Parks_Discovery")
library(readr)
library(dplyr)

parks <- read_csv('data/parks_info_with_size_neighborhood.csv')
feature_data <- read_csv('parks_review.csv')

feature_data$`Annual Score` <- NULL
feature_data$`Annual Score number format` <- NULL
feature_data$District <- NULL
feature_data$Instance <- NULL
feature_data$`Total Elements` <- NULL
feature_data$`Passing Elements` <- NULL
feature_data$`Number of Records`<- NULL
feature_data$`Top or Bottom 10` <- NULL


View(feature_data[!toupper(feature_data$Park) %in% unique(parks$ParkName),])

parks$park_match <- parks$ParkName
feature_data$park_match <- feature_data$Park

parks$park_match <- gsub("RECREATION",'REC',parks$park_match)
parks$park_match <- gsub("[[:punct:]]", '', parks$park_match)

feature_data$park_match <- toupper(feature_data$park_match)
feature_data$park_match <- gsub("( \\().*",'',feature_data$park_match)
feature_data$park_match <- gsub("( AT).*",'',feature_data$park_match)
feature_data$park_match <- gsub("-", '/' ,feature_data$park_match)
feature_data$park_match <- gsub("RECREATION",'REC',feature_data$park_match)
feature_data$park_match <- gsub("[[:punct:]]", '', feature_data$park_match)
feature_data$park_match <- gsub("10TH AVENUECLEMENT MINI PARK", '10TH AVECLEMENT MINI PARK', feature_data$park_match)
feature_data$park_match <- gsub("BETTY ANN ONG CHINESE REC CENTER", 'CHINESE REC CENTER', feature_data$park_match)
feature_data$park_match <- gsub("INA COOLBRITH PARK", "INA COOLBRITH MINI PARK", feature_data$park_match)
feature_data$park_match <- gsub("JOE DIMAGGIO NORTH BEACH PLAYGROUND", "JOE DIMAGGIO PLAYGROUND", feature_data$park_match)
feature_data$park_match <- gsub("MINNIE  LOVIE WARD PLAYGROUND", "MINNIE  LOVIE WARD REC CENTER", feature_data$park_match)
feature_data$park_match <- gsub("PALOUPHELPS MINI PARK" , "PALOUPHELPS PARK", feature_data$park_match)
feature_data$park_match <- gsub("PARK PRESIDIO BOULEVARD" , "PARK PRESIDIO BLVD", feature_data$park_match)
feature_data$park_match <- gsub("PATRICIAS GREEN", "PATRICIAS GREEN IN HAYES VALLEY", feature_data$park_match)
feature_data$park_match <- gsub("ROOSEVELT  HENRY STAIRS", "ROOSEVELTHENRY STEPS", feature_data$park_match)
feature_data$park_match <- gsub("UTAH18TH STREET MINI PARK", "UTAH18TH MINI PARK", feature_data$park_match)
feature_data$park_match <- gsub("YACHT HARBOR  MARINA GREEN", "YACHT HARBOR AND MARINA GREEN", feature_data$park_match)

View(feature_data[!feature_data$park_match %in% unique(parks$park_match),]%>%
         arrange(park_match))

# trouble makers
# I dont think any of them 
sort(unique(feature_data[!feature_data$park_match %in% unique(parks$park_match),]$park_match))
# [3] "EUGENE FRIEND REC CENTER"           
# [4] "GOLDEN GATE PARK  SEC 1"            
# [5] "GOLDEN GATE PARK  SEC 2"            
# [6] "GOLDEN GATE PARK  SEC 3"            
# [7] "GOLDEN GATE PARK  SEC 4"            
# [8] "GOLDEN GATE PARK  SEC 5"            
# [9] "GOLDEN GATE PARK  SEC 6"            
# [17] "SOMA WEST DOG PARK"                 
# [18] "SOMA WEST SKATEPARK"                


table(unique(feature_data$park_match) %in% unique(parks$park_match))
sort(unique(parks$park_match))

features_final <- merge(select(parks, ParkName, park_match), 
      select(feature_data, park_match, Feature)) %>%
         select(ParkName, Feature)

write_csv(unique(features_final), 'data/features.csv')
