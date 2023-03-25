main_create = {}
main_insert = {}

main_create['main__PropertyTransaction'] = ('''
    CREATE TABLE `main__PropertyTransaction` (
    id              int             AUTO_INCREMENT,
    district        int             NOT NULL,
    street          varchar(100)    NOT NULL,
    block           varchar(50)     NOT NULL,
    floorRangeStart int             NOT NULL,
    floorRangeEnd   int             NOT NULL,
    propertyType    enum(
        'STRATA DETACHED',
        'STRATA SEMIDETACHED',
        'STRATA TERRACE',
        'DETACHED',
        'SEMI-DETACHED',
        'TERRACE',
        'APARTMENT',
        'CONDOMINIUM',
        'EXECUTIVE CONDOMINIUM',
        '1 ROOM HDB',
        '2 ROOM HDB',
        '3 ROOM HDB',
        '4 ROOM HDB',
        '5 ROOM HDB',
        'EXECUTIVE HDB',
        'MULTI-GENERATION HDB'
    )                               NOT NULL,
    noOfRoom        int                     ,
    area            int             NOT NULL,
    price           decimal(12,2)   NOT NULL,
    transactionDate date                    ,
    tenure          int                     ,
    resale          boolean                 ,
    x               decimal(9,4)    NOT NULL,
    y               decimal(9,4)    NOT NULL,
    PRIMARY KEY (id)
)
''')

main_insert['main__PropertyTransaction'] = ('''
    INSERT INTO `main__PropertyTransaction`
    (district, street, block, floorRangeStart, floorRangeEnd, propertyType, noOfRoom, area, price, transactionDate, tenure, resale, x, y) 
    VALUES
    (%s, %d, %d, %s, %s, %d, %s, %s, %s, %d, %s, %d, %s, %s)
''')