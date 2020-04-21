\set ON_ERROR_STOP on
\c aj8186

drop database if exists woman-up;
create database woman-up;
\c woman-up;

create table user(
    first_name text,
    last_name text,
    tel_num int,
    password varchar(20) ,
    email text,
    
    primary key (email)
);

create table message(
    from_user int,
    to_user int,
    message text,
    date date,
    time time,

    primary key(from_user, to_user, date),
    foreign key(from_user) REFERENCES user(pnr),
    foreign key(to_user) REFERENCES user(pnr)

);

create table status(
    pnr int,
    lat int,
    long int,
    first_name text,
    status text,
    date date,
    time time,

    primary key(pnr),
    foreign key(pnr) REFERENCES user(pnr)

);