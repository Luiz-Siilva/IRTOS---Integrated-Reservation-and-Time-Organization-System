DROP TABLE db_teste.pessoas;

CREATE TABLE db_teste.pessoas (
    Id int not null auto_increment,
    Nome varchar(255),
    Email varchar(255),
    primary key (id)
);
    