CREATE TABLE Cash (
    id Serial PRIMARY KEY,
    uf varchar,
    euro varchar,
    dolar varchar,
    time float,
    date varchar
);

CREATE TABLE Weather (
    id Serial PRIMARY KEY,
    temp varchar,
    time float,
    date varchar
);