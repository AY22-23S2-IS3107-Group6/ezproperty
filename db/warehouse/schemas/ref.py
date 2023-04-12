ref_create = {}
ref_insert = {}

ref_create['ref__PropertyInformation'] = ('''
    CREATE TABLE `ref__PropertyInformation` (
    id                      int             NOT NULL,
    block                   varchar(50)     NOT NULL,
    street                  varchar(100)    NOT NULL,
    maxFloorLevel           int             NOT NULL,
    yearCompleted           int             NOT NULL,
    residentialTag          boolean         NOT NULL,
    commercialTag           boolean         NOT NULL,
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

# ref_create['ref__PropertyInformation'] = ('''
#     CREATE TABLE `ref__PropertyInformation` (
#     id                      int             AUTO_INCREMENT,
#     block                   varchar(50)     NOT NULL,
#     street                  varchar(100)    NOT NULL,
#     maxFloorLevel           int             NOT NULL,
#     yearCompleted           date            NOT NULL,
#     residentialTag          boolean         NOT NULL,
#     commercialTag           boolean         NOT NULL,
#     marketHawkerTag         boolean         NOT NULL,
#     miscTag                 boolean         NOT NULL,
#     mscpTag                 boolean         NOT NULL,
#     precinctPavilionTag     boolean         NOT NULL,
#     bldgContractTown        enum(
#         'ANG MO KIO',
#         'BUKIT BATOK',
#         'BEDOK',
#         'BISHAN',
#         'BUKIT MERAH',
#         'BUKIT PANJANG',
#         'BUKIT TIMAH',
#         'CHOA CHU KANG',
#         'CLEMENTI',
#         'CENTRAL AREA',
#         'GEYLANG',
#         'HOUGANG',
#         'JURONG EAST',
#         'JURONG WEST',
#         'KALLANG/WHAMPOA',
#         'MARINE PARADE',
#         'PUNGGOL',
#         'PASIR RIS',
#         'QUEENSTOWN',
#         'SEMBAWANG',
#         'SERANGOON',
#         'SENGKANG',
#         'TAMPINES',
#         'TENGAH',
#         'TOA PAYOH',
#         'WOODLANDS',
#         'YISHUN'
#     )                                       NOT NULL,
#     totalDwellingUnits      int             NOT NULL,
#     oneRoomSold             int             NOT NULL,
#     twoRoomSold             int             NOT NULL,
#     threeRoomSold           int             NOT NULL,
#     fourRoomSold            int             NOT NULL,
#     fiveRoomSold            int             NOT NULL,
#     execSold                int             NOT NULL,
#     multigenSold            int             NOT NULL,
#     studioAptSold           int             NOT NULL,
#     oneRoomRental           int             NOT NULL,
#     twoRoomRental           int             NOT NULL,
#     threeRoomRental         int             NOT NULL,
#     otherRoomRental         int             NOT NULL,
#     PRIMARY KEY (id)
# )
# ''')

ref_insert['ref__PropertyInformation'] = ('''
    INSERT INTO `ref__PropertyInformation`
    (street, id, block, yearCompleted, totalDwellingUnits, maxFloorLevel, oneRoomSold, twoRoomSold, threeRoomSold, fourRoomSold,
    fiveRoomSold, execSold, multigenSold, studioAptSold, oneRoomRental, twoRoomRental, threeRoomRental, otherRoomRental, 
    residentialTag, commercialTag, mscpTag, marketHawkerTag, precinctPavilionTag, miscTag, bldgContractTown)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
''')

ref_create['ref__District'] = ('''
    CREATE TABLE `ref__District` (
    id         int     AUTO_INCREMENT,
    district   int     NOT NULL,
    PRIMARY KEY (id)
)
''')

ref_insert['ref__District'] = ('''
    INSERT INTO `ref__District`
    (district)
    VALUES
    (%s)
''')

ref_create['ref__Town'] = ('''
    CREATE TABLE `ref__Town` (
    id               int             AUTO_INCREMENT,
    town             varchar(20)     NOT NULL,
    district         int             NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(district) REFERENCES ref__District(id)
)
''')

ref_insert['ref__Town'] = ('''
    INSERT INTO `ref__Town`
    (town, district)
    VALUES
    (%s, (SELECT id from ref__District WHERE district=%s))
''')

ref_create['ref__PostalCode'] = ('''
    CREATE TABLE `ref__PostalCode` (
    id               int             AUTO_INCREMENT,
    district         int             NOT NULL,
    postalCodeStart  int             NOT NULL,
    postalCodeEnd    int             NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(district) REFERENCES ref__District(id)
)
''')

ref_insert['ref__PostalCode'] = ('''
    INSERT INTO `ref__PostalCode`
    (district, postalCodeStart, postalCodeEnd)
    VALUES
    ((SELECT id from ref__District WHERE district=%s), %s, %s)
''')

# ref_create['ref__District'] = ('''
#     CREATE TABLE `ref__District` (
#     id               int             AUTO_INCREMENT,
#     district         int             NOT NULL,
#     towns            varchar(60)     NOT NULL,
#     x                decimal(9,4)    NOT NULL,
#     y                decimal(9,4)    NOT NULL,
#     postalCodeStart  int             NOT NULL,
#     postalCodeEnd    int             NOT NULL,
#     PRIMARY KEY (id)
# )
# ''')

# ref_insert['ref__District'] = ('''
#     INSERT INTO `ref__District`
#     (district, towns, x, y, postalCodeStart, postalCodeEnd)
#     VALUES
#     (%s, %s, %s, %s, %s, %s)
# ''')