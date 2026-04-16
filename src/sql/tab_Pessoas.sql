DROP TABLE db_users.users;

CREATE TABLE db_users.users (
    Id_users int not null auto_increment,
    Name varchar(255) NOT NULL,
    Email varchar(255) NOT NULL UNIQUE,
    Phone varchar(20),
    Password varchar(255) NOT NULL,
    primary key (id_users)
);