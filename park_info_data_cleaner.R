# data originally from:
# https://data.sfgov.org/Culture-and-Recreation/Recreation-Park-Department-Park-Info-Dataset
parks <- read_csv('data/Recreation___Park_Department_Park_Info_Dataset.csv')


# Things I want to fix:
#   Remove double header row
#   Get missing location data
#   Split Lat and Long into own columns
#   Get street numbers for the missing (reverse geo code)


# remove extra header row
parks <- parks[2:nrow(parks),]

dim(subset(parks, is.na(`Location 1`)))

address_fixer <- function(park,location){
                    parks[parks$ParkName == park,]$`Location 1` <<- location
                }

# You can actually get all these from the JSON verson, they are stored
# differently from the rest for some reason.
pairs <- list(c('Arkansas Friendship Garden',
                '22nd/Arkansas, San Francisco, CA, (37.75737790, -122.39766207)'),
            c('BAY VIEW PARK',
              "LeConte Ave, San Francisco, CA, (37.71513230, -122.39227019)"),
            c('BERNAL HEIGHTS PARK',
              "Bernal Heights Blvd, San Francisco, CA, (37.74313167, -122.41425204)"),
            c('Connecticut Friendship Garden',
              "22nd/Connecticut, San Francisco, CA, (37.75739852, -122.39731712)"),
            c('CRAGS COURT GARDEN',
              'Crags Ct, San Francisco, CA, (37.74141960, -122.44067225)'),
            c('Dog Patch-Miller Memorial Comm. Garden',
              'Brewster/Rutledge St, San Francisco, CA, (37.74503985, -122.40715464)'),
            c('ESPRIT PARK',
              'Minnesota St, San Francisco, CA, (37.76098611, -122.39099369)'),
            c('Garden for the Environment',
              '7th Ave North of Lawton, San Francisco, CA, (37.75911093, -122.46357301'),
            c('HOLLY PARK',
              'Holly Park Cir, San Francisco, CA, (37.73720955, -122.41994010'),
            c('Hooker Alley Community Garden',
              'Hooker Aly, San Francisco, CA, (37.79043353, -122.41017264)'),
            c('LAKE MERCED PARK',
              'Lake Merced Blvd, San Francisco, CA, (37.72183556, -122.49238175)'),
            c('MT DAVIDSON PARK',
              'Myra Wy, San Francisco, CA, (37.73906280, -122.45465821)'),
            c('MT OLYMPUS',
              'Upper Terrace, San Francisco, CA, (37.76330762, -122.44554051)' ),
            c("O'SHAUGHNESSY HOLLOW",
              "O'Shaughnessy Blvd, San Francisco, CA, (37.74016899, -122.44487598)"),
            c('PARK PRESIDIO BLVD',
              'Park Presidio Blvd, San Francisco, CA, (37.78012283, -122.47228457)'),
            c('RIDGETOP PLAZA',
              'Whitney Young Cire, San Francisco, CA, (37.73379832, -122.38345175)'),
            c('TELEGRAPH HILL/PIONEER PARK',
              'Telegraph Hill Blvd, San Francisco, CA, (37.80278413, -122.40583596)'),
            c('TOPAZ OPEN SPACE',
              'Diamond Heights, San Francisco, CA, (37.74170413, -122.43616246)'),
            c('TWIN PEAKS',
              'Twin Peaks Blvd, San Francisco, CA, (37.75279086, -122.44748390)'),
            c('WILLIE WOO WOO WONG PLAYGROUND',
              'Sacramento St, San Francisco, CA, (37.79358605, -122.40718489)'),
            c('YACHT HARBOR AND MARINA GREEN',
              'Marina Blvd, San Francisco, CA, (37.80677550, -122.44076019)')
            )

# Convert to dataframe
locations <- do.call(rbind, sapply(pairs, data.frame, stringsAsFactors=FALSE))

# OH NOOOOOOO A LOOP!!! Apply was fighting me and this runs fast.
for(p_row in 1:nrow(locations)){
    address_fixer(locations[p_row,1],locations[p_row,2])
}

# Only ones left are the GGP sections
dim(subset(parks, is.na(`Location 1`)))

# General cleaning
parks$`Location 1` <- gsub('\n',' ',parks$`Location 1`)
parks$`Location 1` <- gsub('&amp;', '&', parks$`Location 1`)
    
# Split Lat and Long to own columns
parks$Lat <- gsub( '.*[(]','', parks$`Location 1`) %>%
    gsub('[,].*','',.)

parks$Long <- gsub( '.*[, ]','',parks$`Location 1`) %>%
    gsub('[)].*','',.)

write_csv(parks, 'data/cleaned_parks_info.csv')


quantile(parks$Acreage, c(.2,.4,.6,.8,1))
test <- function(row){
    if(row['Acreage'] <.210){
            'size_tiny'
        }else if(row['Acreage']  > .210 & row['Acreage'] < .800){
            'size_small'
        }else if(row['Acreage']  > .800 & row['Acreage'] < 2.186){
            'size_average'
        }else if(row['Acreage']  > 2.186 & row['Acreage'] < 6.266){
            'size_large'
        }else{
            'size_huge'
        }
}

park_size <- c()
for(x in 1: nrow(parks)){
    park_size <- c(park_size,test(parks[x,]))
    
}

parks$size <- park_size

# read in data for mapping to neighborhoods
zip2hood <- read_csv('data/zipcode_to_neighborhood.csv')

# This will drop the sections of Golden Gate, fine for our use
parks_neighborhoods <- merge(parks, zip2hood, by.x='Zipcode', by.y='zipcode')

write_csv(parks_neighborhoods, 'data/parks_info_with_size_neighborhood.csv')

