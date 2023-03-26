amn_create = {}
amn_insert = {}

amn_create['test__Test'] = ('''
    CREATE TABLE `test__Test` (
    _id             varchar(50)     NOT NULL,
    col1            varchar(50)     NOT NULL,
    col2            varchar(50)     NOT NULL,
    PRIMARY KEY (_id)
)
''')

amn_insert['test__Test'] = ('''
    INSERT INTO `test__Test`
    (_id, col1, col2)
    VALUES
    (%s, %s, %s)
''')

amn_create['amn__TrainStation'] = ('''
    CREATE TABLE `amn__TrainStation` (
    id              int             NOT NULL,
    stationName     varchar(50)     NOT NULL,
    stationNo       varchar(6)      NOT NULL,
    x               decimal(9,4)    NOT NULL,
    y               decimal(9,4)    NOT NULL,
    latitude        decimal(10,9)   NOT NULL,
    longitude       decimal(10,9)   NOT NULL,
    color           varchar(10)     NOT NULL,
    PRIMARY KEY (id,stationNo)
)
''')

amn_insert['amn__TrainStation'] = ('''
    INSERT INTO `amn__TrainStation`
    (id, stationName, stationNo, x, y, latitude, longitude, color)
    VALUES
    (%d, %s, %s, %d, %d, %d, %d, %s)
''')

amn_create['amn__PrimarySchool'] = ('''
    CREATE TABLE `amn__PrimarySchool` (
    id                      int              NOT NULL,
    schoolName              varchar(50)      NOT NULL,
    schoolChineseName       varchar(30)      NOT NULL,
    sap                     varchar(3)       NULL,
    gep                     varchar(3)       NULL,
    gender                  varchar(5)       NOT NULL,
    affiliatedSecondary     varchar(100)     NOT NULL,
    area                    varchar(20)      NOT NULL,
    address                 varchar(50)      NOT NULL,
    PRIMARY KEY (id,schoolName)
)
''')

amn_insert['amn__PrimarySchool'] = ('''
    INSERT INTO `amn__PrimarySchool`
    (id, schoolName, schoolChineseName, sap, gep, gender, affiliatedSecondary, area, address)
    VALUES
    (%d, %s, %s, %s, %s, %s, %s, %s, %s)
''')

amn_create['amn__SuperMarket'] = ('''
    licence_num     varchar(50)          NOT NULL,
    licensee_name   varchar(50)          NOT NULL,
    building_name   varchar(50)          NOT NULL,
    block_house_num varchar(50)          NOT NULL,
    level_num       varchar(50)          NOT NULL,
    unit_num        varchar(50)          NOT NULL,
    street_name     varchar(50)          NOT NULL,           
    postal_code     int                  NOT NULL,
    district        int                  NULL,
    PRIMARY KEY (licence_num)
)
''')

amn_insert['amn__SuperMarket'] = ('''
    INSERT INTO `amn__SuperMarket`
    (licence_num, licensee_name, building_name, block_house_num, level_num, unit_num, street_name, postal_code, district)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %d, %d)
''')
    
amn_create['amn__HawkerCenter'] = ('''
    name_of_centre  varchar(50)          NOT NULL,
    location_of_centre varchar(50)       NOT NULL,
    type_of_centre  varchar(50)          NOT NULL,
    block           varchar(50)          NOT NULL,
    owner           varchar(50)          NOT NULL,
    no_of_stalls    int             NOT NULL,
    no_of_cooked_food_stalls int    NOT NULL,
    no_of_mkt_produce_stalls int    NOT NULL,
    district        int                  NULL,
    PRIMARY KEY (name_of_centre)
)
''')

amn_insert['amn__HawkerCenter'] = ('''
    INSERT INTO `amn__HawkerCenter`
    (name_of_centre, location_of_centre, type_of_centre, block, owner, no_of_stalls, no_of_cooked_food_stalls, no_of_mkt_produce_stalls, district)
    VALUES
    (%s, %s, %s, %s, %s, %d, %d, %d, %d)
''')
                                   
amn_create['amn__Carpark'] = ('''
    CREATE TABLE `amn__Carpark` (
    ppCode              int             NOT NULL,
    ppName              varchar(50)     NOT NULL,
    vehCat              enum(
        'C',
        'M',
        'H'
    )                                   NOT NULL,
    startTime           varchar(50)     NOT NULL,
    endTime             varchar(50)     NOT NULL,
    weekdayRate         decimal(7,2)    NOT NULL,
    weekdayMin          int             NOT NULL,
    satdayRate          decimal(7,2)    NOT NULL,
    satdayMin           int             NOT NULL,
    sunPHRate           decimal(7,2)    NOT NULL,
    sunPHMin            int             NOT NULL,
    remarks             varchar(100)    NOT NULL, 
    parkingSystem       enum(
        'C',
        'B'
    )                                   NOT NULL,
    parkCapacity        int             NOT NULL,
    seasonParkingHrs    varchar(100)    NOT NULL,
    seasonTicketType    enum(
        'Commercial',
        'Residential',
    )                                   NOT NULL,
    seasonMonthlyRate   int             NOT NULL,
    x                   decimal(7,2)    NOT NULL,
    y                   decimal(7,2)    NOT NULL,
    isSeasonParking     boolean         NOT NULL,
    PRIMARY KEY (ppCode, isSeasonParking)
)
''')

amn_insert['amn__Carpark'] = ('''
    INSERT INTO `amn__Carpark`
    (ppCode, ppName, vehCat, startTime, endTime, weekdayRate, weekdayMin, satdayRate, satdayMin, sunPHRate, sunPHMin, remarks, parkingSystem, parkCapacity, seasonParkingHrs, seasonTicketType, seasonMonthlyRate, x, y, isSeasonParking)
    VALUES
    (%d, %d, %s, %s, %s, %d, %d, %d, %d, %d, %d, %s, %s, %d, %s, %s, %d, %d, %d, %s)
''')
