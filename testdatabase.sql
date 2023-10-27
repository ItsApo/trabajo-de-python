create database testdatabase;
use testdatabase;
create table people(
id_user int primary key not null,
name varchar (45) not null,
last_name varchar(45) not null);

create table products(
id_product int not null,
client_name varchar(45) not null,
products_amount varchar(100) not null);
