ref_create = {}
ref_insert = {}

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