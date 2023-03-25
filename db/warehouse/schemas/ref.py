ref_create = {}
ref_insert = {}

ref_create['ref__PropertyInformation'] = ('''
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

ref_insert['main__PropertyInformation'] = ('''
    INSERT INTO `main__PropertyInformation`
    (block, street, maxFloorLevel, yearCompleted, residentialTag, commericalTag, marketHawkerTag, miscTag, mscpTag, precinctPavilionTag, bldgContractTown,
    totalDwellingUnits, oneRoomSold, twoRoomSold, threeRoomSold, fourRoomSold, fiveRoomSold, execSold, multigenSold, studioAptSold, oneRoomRental, twoRoomRental, threeRoomRental, otherRoomRental)  
    VALUES
    (%s, %s, %d, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)
''')

ref_create['ref__District'] = ('''
    CREATE TABLE `ref__District` (
    id               int             NOT NULL,
    district         int             NOT NULL,
    towns            varchar(60)     NOT NULL,
    x                decimal(9,4)    NOT NULL,
    y                decimal(9,4)    NOT NULL,
    postalCodeStart  int             NOT NULL,
    postalCodeEnd    int             NOT NULL,
    PRIMARY KEY (id,districtNo)
)
''')

ref_insert['ref__District'] = ('''
    INSERT INTO `ref__District`
    (id, district, towns, x, y, postalCodeStart, postalCodeEnd)
    VALUES
    (%d, %d, %s, %d, %d, %d, %d)
''')