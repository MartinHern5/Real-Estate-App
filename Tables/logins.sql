CREATE TABLE `logins` (
  `ID` INT NOT NULL,
  `Username` VARCHAR(255) NOT NULL,
  `Password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (ID)
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
COMMENT = 'Database to store login information';

ALTER TABLE `logins` 
  ADD UNIQUE INDEX Username_UNIQUE(Username);