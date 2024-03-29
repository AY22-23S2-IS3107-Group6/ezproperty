amn_create = {}
amn_insert = {}

amn_create['amn__TrainStation'] = ('''
    CREATE TABLE `amn__TrainStation` (
    _id             varchar(24)     NOT NULL,
    stationName     varchar(50)     NOT NULL,
    stationNo       varchar(6)      NOT NULL,
    x               decimal(9,4)    NOT NULL,
    y               decimal(9,4)    NOT NULL,
    latitude        decimal(10,9)   NOT NULL,
    longitude       decimal(12,9)   NOT NULL,
    colour          varchar(10)     NOT NULL,
    district        int             NULL,
    PRIMARY KEY (_id),
    FOREIGN KEY(district) REFERENCES ref__District(id)
)
''')

amn_insert['amn__TrainStation'] = ('''
    INSERT INTO `amn__TrainStation`
    (_id, stationName, stationNo, x, y, latitude, longitude, colour, district)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
''')

amn_create['amn__PrimarySchool'] = ('''
    CREATE TABLE `amn__PrimarySchool` (
    _id                     varchar(24)                       NOT NULL,
    schoolName              varchar(50)                       NOT NULL,
    schoolChineseName       varchar(30)                       NOT NULL,
    sap                     boolean                           NOT NULL,
    gep                     boolean                           NOT NULL,
    gender                  ENUM('Girls', 'Boys', 'Mixed')    NOT NULL,
    affiliatedSecondary     varchar(100)                      NOT NULL,
    area                    varchar(20)                       NOT NULL,
    address                 varchar(100)                      NOT NULL,
    district                int                               NULL,
    PRIMARY KEY (_id,schoolName),
    FOREIGN KEY(district) REFERENCES ref__District(id)
)
''')

amn_insert['amn__PrimarySchool'] = ('''
    INSERT INTO `amn__PrimarySchool`
    (_id, schoolName, schoolChineseName, sap, gep, gender, affiliatedSecondary, area, address, district)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
''')

amn_create['amn__Supermarket'] = ('''
    CREATE TABLE `amn__Supermarket` (
    licenceNo       varchar(50)          NOT NULL,
    licenseeName    varchar(50)          NOT NULL,
    buildingName    varchar(50)          NOT NULL,
    blockHouseNo    varchar(50)          NOT NULL,
    level           varchar(50)          NOT NULL,
    unitNo          varchar(50)          NOT NULL,
    streetName      varchar(50)          NOT NULL,           
    postalCode      int                  NOT NULL,
    district        int                  NULL,
    PRIMARY KEY (licenceNo),
    FOREIGN KEY(district) REFERENCES ref__District(id)
)
''')

amn_insert['amn__Supermarket'] = ('''
    INSERT INTO `amn__Supermarket`
    (licenceNo, licenseeName, buildingName, blockHouseNo, level, unitNo, streetName, postalCode, district)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
''')
    
amn_create['amn__HawkerCentre'] = ('''
    CREATE TABLE `amn__HawkerCentre` (
    name                    varchar(50)  NOT NULL,
    location                varchar(100) NOT NULL,
    type                    varchar(50)  NOT NULL,
    owner                   varchar(50)  NOT NULL,
    noOfStalls              int          NOT NULL,
    noOfCookedFoodStalls    int          NOT NULL,
    noOfMktProduceStalls    int          NOT NULL,
    district                int          NULL,
    PRIMARY KEY (name),
    FOREIGN KEY(district) REFERENCES ref__District(id)
)
''')

amn_insert['amn__HawkerCentre'] = ('''
    INSERT INTO `amn__HawkerCentre`
    (name, location, type, owner, noOfStalls, noOfCookedFoodStalls, noOfMktProduceStalls, district)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s)
''')


amn_create['amn__CarparkPublic'] = ('''
    CREATE TABLE `amn__CarparkPublic` (
    _id                 varchar(24)     NOT NULL,
    weekdayMin          int             NOT NULL,
    weekdayRate         decimal(7,2)    NOT NULL,
    ppCode              varchar(20)     NOT NULL,
    parkingSystem       varchar(20)     NOT NULL,
    ppName              varchar(50)     NOT NULL,
    vehCat              varchar(20)     NOT NULL,
    satdayMin           int             NOT NULL,
    satdayRate          decimal(7,2)    NOT NULL,
    sunPHMin            int             NOT NULL,
    sunPHRate           decimal(7,2)    NOT NULL,
    startTime           varchar(50)     NOT NULL,
    parkCapacity        int             NOT NULL,
    endTime             varchar(50)     NOT NULL,
    x                   decimal(7,2)    NOT NULL,
    y                   decimal(7,2)    NOT NULL,
    district            int             NULL,
    PRIMARY KEY (_id),
    FOREIGN KEY(district) REFERENCES ref__District(id)
)
''')

# don't think this is a suitable primary key - but will figure out an alternative down the road

amn_insert['amn__CarparkPublic'] = ('''
    INSERT INTO `amn__CarparkPublic`
    (_id, weekdayMin, weekdayRate, ppCode, parkingSystem, ppName, vehCat, satdayMin, satdayRate, sunPHMin, sunPHRate, startTime, parkCapacity, endTime, x, y, district)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
''')

amn_create['amn__CarparkSeason'] = ('''
    CREATE TABLE `amn__CarparkSeason` (
    _id                 varchar(24)     NOT NULL,
    ppCode              varchar(20)     NOT NULL,
    ppName              varchar(50)     NOT NULL,
    vehCat              varchar(20)     NOT NULL,
    monthlyRate         int             NOT NULL,
    parkingHrs          varchar(100)    NOT NULL,
    ticketType          varchar(20)     NOT NULL,
    x                   decimal(7,2)    NOT NULL,
    y                   decimal(7,2)    NOT NULL,
    district            int             NULL,
    PRIMARY KEY (_id),
    FOREIGN KEY(district) REFERENCES ref__District(id)
)
''')

amn_insert['amn__CarparkSeason'] = ('''
    INSERT INTO `amn__CarparkSeason`
    (_id, ppCode, ppName, vehCat, monthlyRate, parkingHrs, ticketType, x, y, district)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
''')
