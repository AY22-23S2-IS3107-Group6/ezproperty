main_create = {}
main_insert = {}

# included x and y for testing
main_create['main__PropertyTransaction'] = ('''
    CREATE TABLE `main__PropertyTransaction` (
    _id             int            AUTO_INCREMENT,
    district        int             NOT NULL,
    street          varchar(100)    NOT NULL,
    floorRangeStart int             NOT NULL,
    floorRangeEnd   int             NOT NULL,
    propertyType    varchar(50)     NOT NULL,
    area            decimal(12,2)   NOT NULL,
    price           decimal(12,2)   NOT NULL,
    transactionDate varchar(10)             ,
    tenure          int                     ,
    resale          boolean                 ,
    x               decimal(9,4)    NULL,
    y               decimal(9,4)    NULL,
    PRIMARY KEY (_id)
)
''')

# included x and y for testing
main_insert['main__PropertyTransaction'] = ('''
    INSERT INTO `main__PropertyTransaction`
    (district, street, floorRangeStart, floorRangeEnd, propertyType, area, price, transactionDate, tenure, resale, x, y) 
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
''')

main_create['main__RentalProject'] = ('''
    CREATE TABLE `main__RentalProject` (
    _id             varchar(24)     NOT NULL,
    street          varchar(100)    NOT NULL,
    x               decimal(9,4)    NOT NULL,
    project         varchar(100)    NOT NULL,   
    y               decimal(9,4)    NOT NULL,
    PRIMARY KEY (_id)
)
''')

main_insert['main__RentalProject'] = ('''
    INSERT INTO `main__RentalProject`
    (_id, street, x, project, y) 
    VALUES
    (%s, %s, %s, %s, %s)
''')

main_create['main__RentalMedian'] = ('''
    CREATE TABLE `main__RentalMedian` (
    _id              int             AUTO_INCREMENT,
    refPeriod        varchar(24)     NOT NULL,
    psf75            decimal(12,2)   NOT NULL,
    median           decimal(12,2)   NOT NULL,
    psf25            decimal(12,2)   NOT NULL,   
    district         varchar(10)     NOT NULL,
    rentalProjectId  varchar(24)     NOT NULL,
    PRIMARY KEY (_id)
)
''')

main_insert['main__RentalMedian'] = ('''
    INSERT INTO `main__RentalMedian`
    (refPeriod, psf75, median, psf25, district, rentalProjectId) 
    VALUES
    (%s, %s, %s, %s, %s, %s)
''')

# main_create['main__PropertyTransaction'] = ('''
#     CREATE TABLE `main__PropertyTransaction` (
#     id              int             AUTO_INCREMENT,
#     district        int             NOT NULL,
#     street          varchar(100)    NOT NULL,
#     block           varchar(50)     NOT NULL,
#     floorRangeStart int             NOT NULL,
#     floorRangeEnd   int             NOT NULL,
#     propertyType    enum(
#         'STRATA DETACHED',
#         'STRATA SEMIDETACHED',
#         'STRATA TERRACE',
#         'DETACHED',
#         'SEMI-DETACHED',
#         'TERRACE',
#         'APARTMENT',
#         'CONDOMINIUM',
#         'EXECUTIVE CONDOMINIUM',
#         '1 ROOM HDB',
#         '2 ROOM HDB',
#         '3 ROOM HDB',
#         '4 ROOM HDB',
#         '5 ROOM HDB',
#         'EXECUTIVE HDB',
#         'MULTI-GENERATION HDB'
#     )                               NOT NULL,
#     noOfRoom        int                     ,
#     area            int             NOT NULL,
#     price           decimal(12,2)   NOT NULL,
#     transactionDate date                    ,
#     tenure          int                     ,
#     resale          boolean                 ,
#     x               decimal(9,4)    NOT NULL,
#     y               decimal(9,4)    NOT NULL,
#     PRIMARY KEY (id)
# )
# ''')

# main_create['main__RentalTransaction'] = ('''
#     CREATE TABLE `main__RentalTransaction` (
#     id              int             AUTO_INCREMENT,
#     district        int             NOT NULL,
#     street          varchar(100)    NOT NULL,
#     block           varchar(50)     NOT NULL,
#     propertyType    enum(
#         'STRATA DETACHED',
#         'STRATA SEMIDETACHED',
#         'STRATA TERRACE',
#         'DETACHED',
#         'SEMI-DETACHED',
#         'TERRACE',
#         'APARTMENT',
#         'CONDOMINIUM',
#         'EXECUTIVE CONDOMINIUM',
#         '1 ROOM HDB',
#         '2 ROOM HDB',
#         '3 ROOM HDB',
#         '4 ROOM HDB',
#         '5 ROOM HDB',
#         'EXECUTIVE HDB',
#         'MULTI-GENERATION HDB'
#     )                               NOT NULL,
#     noOfRoom        int                     ,
#     area            int             NOT NULL,
#     rent            decimal(12,2)   NOT NULL,
#     psf25           decimal(12,2)           ,
#     median          decimal(12,2)           ,
#     psf75           decimal(12,2)           ,
#     transactionDate date                    ,
#     x               decimal(9,4)    NOT NULL,
#     y               decimal(9,4)    NOT NULL,
#     PRIMARY KEY (id)
# )
# ''')

# main_insert['main__RentalTransaction'] = ('''
#     INSERT INTO `main__RentalTransaction`
#     (district, street, block, propertyType, noOfRoom, area, rent, psf25, median, psf75, transactionDate, x, y)
#     VALUES
#     (%d, %s, %s, %s, %d, %d, %d, %d, %d, %d, %s, %d, %d)
# ''')