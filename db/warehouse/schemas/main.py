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

main_create['main__PropertyInformation'] = ('''
    CREATE TABLE `main__PropertyInformation` (
    id                      int             AUTO_INCREMENT,
    block                   varchar(50)     NOT NULL,
    street                  varchar(100)    NOT NULL,
    maxFloorLevel           int             NOT NULL,
    yearCompleted           date            NOT NULL,
    residentialTag          boolean         NOT NULL,
    commericalTag           boolean         NOT NULL,
    marketHawkerTag         boolean         NOT NULL,
    miscTag                 boolean         NOT NULL,
    mscpTag                 boolean         NOT NULL,
    precinctPavilionTag     boolean         NOT NULL,
    bldgContractTown        enum(
        'ANG MO KIO',
        'BUKIT BATOK',
        'BEDOK',
        'BISHAN',
        'BUKIT MERAH',
        'BUKIT PANJANG',
        'BUKIT TIMAH',
        'CHOA CHU KANG',
        'CLEMENTI',
        'CENTRAL AREA',
        'GEYLANG',
        'HOUGANG',
        'JURONG EAST',
        'JURONG WEST',
        'KALLANG/WHAMPOA',
        'MARINE PARADE',
        'PUNGGOL',
        'PASIR RIS',
        'QUEENSTOWN',
        'SEMBAWANG',
        'SERANGOON',
        'SENGKANG',
        'TAMPINES',
        'TENGAH',
        'TOA PAYOH',
        'WOODLANDS',
        'YISHUN'
    )                                       NOT NULL,
    totalDwellingUnits      int             NOT NULL,
    oneRoomSold             int             NOT NULL,
    twoRoomSold             int             NOT NULL,
    threeRoomSold           int             NOT NULL,
    fourRoomSold            int             NOT NULL,
    fiveRoomSold            int             NOT NULL,
    execSold                int             NOT NULL,
    multigenSold            int             NOT NULL,
    studioAptSold           int             NOT NULL,
    oneRoomRental           int             NOT NULL,
    twoRoomRental           int             NOT NULL,
    threeRoomRental         int             NOT NULL,
    otherRoomRental         int             NOT NULL,
    PRIMARY KEY (id)
)
''')

main_insert['main__PropertyInformation'] = ('''
    INSERT INTO `main__PropertyInformation`
    (block, street, maxFloorLevel, yearCompleted, residentialTag, commericalTag, marketHawkerTag, miscTag, mscpTag, precinctPavilionTag, bldgContractTown,
    totalDwellingUnits, oneRoomSold, twoRoomSold, threeRoomSold, fourRoomSold, fiveRoomSold, execSold, multigenSold, studioAptSold, oneRoomRental, twoRoomRental, threeRoomRental, otherRoomRental)  
    VALUES
    (%s, %s, %d, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)
''')