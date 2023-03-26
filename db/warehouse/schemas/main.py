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
    (%d, %s, %s, %d, %d, %s, %d, %d, %d, %s, %d, %s, %d, %d)
''')

main_create['main__RentalTransaction'] = ('''
    CREATE TABLE `main__RentalTransaction` (
    id              int             AUTO_INCREMENT,
    district        int             NOT NULL,
    street          varchar(100)    NOT NULL,
    block           varchar(50)     NOT NULL,
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
    rent            decimal(12,2)   NOT NULL,
    psf25           decimal(12,2)           ,
    median          decimal(12,2)           ,
    psf75           decimal(12,2)           ,
    transactionDate date                    ,
    x               decimal(9,4)    NOT NULL,
    y               decimal(9,4)    NOT NULL,
    PRIMARY KEY (id)
)
''')

main_insert['main__RentalTransaction'] = ('''
    INSERT INTO `main__RentalTransaction`
    (district, street, block, propertyType, noOfRoom, area, rent, psf25, median, psf75, transactionDate, x, y) 
    VALUES
    (%d, %s, %s, %s, %d, %d, %d, %d, %d, %d, %s, %d, %d)
''')