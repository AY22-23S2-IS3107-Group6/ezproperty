test_create = {}
test_insert = {}

test_create['test__Test'] = ('''
    CREATE TABLE `test__Test` (
    _id             varchar(50)     NOT NULL,
    col1            varchar(50)     NOT NULL,
    col2            varchar(50)     NOT NULL,
    PRIMARY KEY (_id)
)
''')

test_insert['test__Test'] = ('''
    INSERT INTO `test__Test`
    (_id, col1, col2)
    VALUES
    (%s, %s, %s)
''')

test_create['test__Test2'] = ('''
    CREATE TABLE `test__Test2` (
    id           int     NOT NULL,
    district             int      NULL,
    x            int     NULL,
    y            int      NULL,
    PRIMARY KEY (id)
)
''')

test_insert['test__Test2'] = ('''
    INSERT INTO `test__Test2`
    (id, district, x, y)
    VALUES
    (%s, %s, %s, %s)
''')