SHOW COLLATION;
CREATE DATABASE `sistema_de_biblioteca_C3_grupo_21` /*!40100 COLLATE 'utf8mb4_general_ci' */;
SHOW DATABASES;
/* Entrando a la sesión "Local" */

USE `sistema_de_biblioteca_C3_grupo_21`;
SHOW ENGINES;
SHOW VARIABLES;
CREATE TABLE `book` (
	`ID_BOOK` CHAR(5) NOT NULL,
	`TITULO` VARCHAR(50) NOT NULL,
	`FECHA_PUBLICACION` CHAR(10) NOT NULL,
	`ID_AUTHOR` CHAR(5) NOT NULL,
	`SECUELA` VARCHAR(2000) NOT NULL DEFAULT 'No Posee Secuela',
	`PRECUELA` VARCHAR(2000) NOT NULL DEFAULT 'No Posee Precuela',
	PRIMARY KEY (`ID_BOOK`)
)
COMMENT='tabla para guardar libros'
COLLATE='utf8mb4_general_ci'
;
SELECT `DEFAULT_COLLATION_NAME` FROM `information_schema`.`SCHEMATA` WHERE `SCHEMA_NAME`='sistema_de_biblioteca_C3_grupo_21';
SHOW TABLE STATUS FROM `sistema_de_biblioteca_C3_grupo_21`;
SHOW FUNCTION STATUS WHERE `Db`='sistema_de_biblioteca_C3_grupo_21';
SHOW PROCEDURE STATUS WHERE `Db`='sistema_de_biblioteca_C3_grupo_21';
SHOW TRIGGERS FROM `sistema_de_biblioteca_C3_grupo_21`;
SELECT *, EVENT_SCHEMA AS `Db`, EVENT_NAME AS `Name` FROM information_schema.`EVENTS` WHERE `EVENT_SCHEMA`='sistema_de_biblioteca_C3_grupo_21';
SELECT * FROM `information_schema`.`COLUMNS` WHERE TABLE_SCHEMA='sistema_de_biblioteca_C3_grupo_21' AND TABLE_NAME='book' ORDER BY ORDINAL_POSITION;
SHOW INDEXES FROM `book` FROM `sistema_de_biblioteca_C3_grupo_21`;
SELECT * FROM information_schema.REFERENTIAL_CONSTRAINTS WHERE   CONSTRAINT_SCHEMA='sistema de biblioteca'   AND TABLE_NAME='book'   AND REFERENCED_TABLE_NAME IS NOT NULL;
SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE   TABLE_SCHEMA='sistema de biblioteca'   AND TABLE_NAME='book'   AND REFERENCED_TABLE_NAME IS NOT NULL;
SHOW CREATE TABLE `sistema_de_biblioteca_C3_grupo_21`.`book`;
SELECT CONSTRAINT_NAME, CHECK_CLAUSE FROM `information_schema`.`CHECK_CONSTRAINTS` WHERE CONSTRAINT_SCHEMA='sistema_de_biblioteca_C3_grupo_21' AND TABLE_NAME='book';
/* Entrando a la sesión "Local" */
SHOW CREATE TABLE `sistema_de_biblioteca_C3_grupo_21`.`book`;

USE `sistema_de_biblioteca_C3_grupo_21`;
SHOW ENGINES;
SHOW VARIABLES;
CREATE TABLE `author` (
	`ID_AUTHOR` CHAR(5) NOT NULL,
	`NOMBRES` VARCHAR(50) NOT NULL,
	`APELLIDOS` VARCHAR(50) NOT NULL,
	`FECHA_NACIMIENTO` CHAR(10) NOT NULL,
	PRIMARY KEY (`ID_AUTHOR`)
)
COMMENT='tabla para guardar a los autores'
COLLATE='utf8mb4_general_ci'
;
SELECT `DEFAULT_COLLATION_NAME` FROM `information_schema`.`SCHEMATA` WHERE `SCHEMA_NAME`='sistema_de_biblioteca_C3_grupo_21';
SHOW TABLE STATUS FROM `sistema_de_biblioteca_C3_grupo_21`;
SHOW FUNCTION STATUS WHERE `Db`='sistema_de_biblioteca_C3_grupo_21';
SHOW PROCEDURE STATUS WHERE `Db`='sistema_de_biblioteca_C3_grupo_21';
SHOW TRIGGERS FROM `sistema_de_biblioteca_C3_grupo_21`;
SELECT *, EVENT_SCHEMA AS `Db`, EVENT_NAME AS `Name` FROM information_schema.`EVENTS` WHERE `EVENT_SCHEMA`='sistema_de_biblioteca_C3_grupo_21';
SELECT * FROM `information_schema`.`COLUMNS` WHERE TABLE_SCHEMA='sistema_de_biblioteca_C3_grupo_21' AND TABLE_NAME='author' ORDER BY ORDINAL_POSITION;
SHOW INDEXES FROM `author` FROM `sistema_de_biblioteca_C3_grupo_21`;
SELECT * FROM information_schema.REFERENTIAL_CONSTRAINTS WHERE   CONSTRAINT_SCHEMA='sistema_de_biblioteca_C3_grupo_21'   AND TABLE_NAME='author'   AND REFERENCED_TABLE_NAME IS NOT NULL;
SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE   TABLE_SCHEMA='sistema_de_biblioteca_C3_grupo_21'   AND TABLE_NAME='author'   AND REFERENCED_TABLE_NAME IS NOT NULL;
SHOW CREATE TABLE `sistema_de_biblioteca_C3_grupo_21`.`author`;
SELECT CONSTRAINT_NAME, CHECK_CLAUSE FROM `information_schema`.`CHECK_CONSTRAINTS` WHERE CONSTRAINT_SCHEMA='sistema_de_biblioteca_C3_grupo_21' AND TABLE_NAME='author';
/* Entrando a la sesión "Local" */
SHOW CREATE TABLE `sistema_de_biblioteca_C3_grupo_21`.`author`;

FLUSH PRIVILEGES;
SHOW COLUMNS FROM `mysql`.`user`;
SELECT `user`, `host`, IF(LENGTH(password)>0, password, authentication_string) AS `password` FROM `mysql`.`user`;
CREATE USER 'User_prueba'@'127.0.0.1' IDENTIFIED BY 'User_prueb@_2023';
GRANT USAGE ON *.* TO 'User_prueba'@'127.0.0.1';
GRANT EXECUTE, SELECT, CREATE, DELETE, INSERT, UPDATE, SHOW VIEW, INDEX  ON `sistema_de_biblioteca_C3_grupo_21`.* TO 'User_prueba'@'127.0.0.1';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'User_prueba'@'127.0.0.1';
