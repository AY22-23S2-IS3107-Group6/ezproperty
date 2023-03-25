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

amn_create['test__Test2'] = ('''
    CREATE TABLE `test__Test2` (
    id           int     NOT NULL,
    district             int      NULL,
    x            int     NULL,
    y            int      NULL,
    PRIMARY KEY (id)
)
''')

amn_insert['test__Test2'] = ('''
    INSERT INTO `test__Test2`
    (id, district, x, y)
    VALUES
    (%d, %d, %d, %d)
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

# primary keys will be both ppCode and boolean
# amn_create['amn__Carpark'] = ('''
#     CREATE TABLE `amn__Carpark` (
#     ppCode              int             NOT NULL,
#     ppName              varchar(50)     NOT NULL,
#     vehCat              enum(
#         'C',
#         'M',
#         'H'
#     )                                   NOT NULL,
#     startTime           varchar(50)     NOT NULL,
#     endTime             varchar(50)     NOT NULL,
#     weekdayRate         decimal(7,2)    NOT NULL,
#     weekdayMin          int             NOT NULL,
#     satdayRate          decimal(7,2)    NOT NULL,
#     satdayMin           int             NOT NULL,
#     sunPHRate           decimal(7,2)    NOT NULL,
#     sunPHMin            int             NOT NULL,
#     remarks             varchar(100)    NOT NULL,
#     parkingSystem       enum(
#         'C',
#         'B'
#     )                                   NOT NULL,
#     parkCapacity        int             NOT NULL,
#     seasonParkingHrs    varchar(100)    NOT NULL, # might want to grab the time out of this
#     seasonTicketType    enum(
#         'Commercial',
#         'Residential',
#     )                                   NOT NULL,
#     seasonMonthlyRate   int             NOT NULL,
#     x                   decimal(7,2)    NOT NULL,
#     y                   decimal(7,2)    NOT NULL,
#     isSeasonParking     boolean         NOT NULL
# )
# ''')