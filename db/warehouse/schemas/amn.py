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
