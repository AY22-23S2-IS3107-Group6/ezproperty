amn_create = {}
amn_insert = {}

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
    address                 varchar(50)      NOT NULL
    PRIMARY KEY (id,schoolName)
)
''')

amn_insert['amn__PrimarySchool'] = ('''
    INSERT INTO `amn__PrimarySchool`
    (id, schoolName, schoolChineseName, sap, gep, gender, affiliatedSecondary, area, address)
    VALUES
    (%d, %s, %s, %s, %s, %s, %s, %s, %s)
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
    PRIMARY KEY (name_of_centre)
)
''')

amn_insert['amn__HawkerCenter'] = ('''
    INSERT INTO `amn__HawkerCenter`
    (name_of_centre, location_of_centre, type_of_centre, block, owner, no_of_stalls, no_of_cooked_food_stalls, no_of_mkt_produce_stalls)
    VALUES
    (%s, %s, %s, %s, %s, %d, %d, %d)
''')
