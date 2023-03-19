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

amn_create['amn__SuperMarket'] = ('''
    licence_num     varchar(50)          NOT NULL,
    licensee_name   varchar(50)          NOT NULL,
    building_name   varchar(50)          NOT NULL,
    block_house_num varchar(50)          NOT NULL,
    level_num       varchar(50)          NOT NULL,
    unit_num        varchar(50)          NOT NULL,
    street_name     varchar(50)          NOT NULL,           
    postal_code     varchar(50)          NOT NULL,
    PRIMARY KEY (licence_num)
)
''')

amn_insert['amn__SuperMarket'] = ('''
    INSERT INTO `amn__SuperMarket`
    (licence_num, licensee_name, building_name, block_house_num, level_num, unit_num, street_name, postal_code)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s)
''')
