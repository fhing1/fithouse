/*
SQLyog Community v13.2.1 (64 bit)
MySQL - 8.0.36 : Database - fit_db
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`fit_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `fit_db`;

/*Table structure for table `administrators` */

DROP TABLE IF EXISTS `administrators`;

CREATE TABLE `administrators` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `PASSWORD` varchar(100) NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `administrators` */

insert  into `administrators`(`id`,`username`,`PASSWORD`,`role`) values 
(1,'admin','123456','admin');

/*Table structure for table `coaches` */

DROP TABLE IF EXISTS `coaches`;

CREATE TABLE `coaches` (
  `CoachID` int NOT NULL AUTO_INCREMENT,
  `CoachName` varchar(50) DEFAULT NULL,
  `Sex` varchar(10) DEFAULT NULL,
  `Birth` date DEFAULT NULL,
  PRIMARY KEY (`CoachID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `coaches` */

/*Table structure for table `coursecoaches` */

DROP TABLE IF EXISTS `coursecoaches`;

CREATE TABLE `coursecoaches` (
  `CourseID` int NOT NULL,
  `CoachID` int NOT NULL,
  PRIMARY KEY (`CourseID`,`CoachID`),
  KEY `CoachID` (`CoachID`),
  CONSTRAINT `coursecoaches_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `courses` (`CourseID`),
  CONSTRAINT `coursecoaches_ibfk_2` FOREIGN KEY (`CoachID`) REFERENCES `coaches` (`CoachID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `coursecoaches` */

/*Table structure for table `courseequipment` */

DROP TABLE IF EXISTS `courseequipment`;

CREATE TABLE `courseequipment` (
  `CourseID` int NOT NULL,
  `EquipmentID` int NOT NULL,
  PRIMARY KEY (`CourseID`,`EquipmentID`),
  KEY `EquipmentID` (`EquipmentID`),
  CONSTRAINT `courseequipment_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `courses` (`CourseID`),
  CONSTRAINT `courseequipment_ibfk_2` FOREIGN KEY (`EquipmentID`) REFERENCES `equipments` (`EquipmentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `courseequipment` */

/*Table structure for table `courses` */

DROP TABLE IF EXISTS `courses`;

CREATE TABLE `courses` (
  `CourseID` int NOT NULL AUTO_INCREMENT,
  `CourseName` varchar(100) DEFAULT NULL,
  `TrainingLocation` varchar(100) DEFAULT NULL,
  `CourseTime` varchar(100) DEFAULT NULL,
  `CourseCoach` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CourseID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `courses` */

insert  into `courses`(`CourseID`,`CourseName`,`TrainingLocation`,`CourseTime`,`CourseCoach`) values 
(1,'瑜伽入门','瑜伽室','周四18:00','王教练'),
(2,'瘦子增肌','健身房','周五19:00','李教练');

/*Table structure for table `equipments` */

DROP TABLE IF EXISTS `equipments`;

CREATE TABLE `equipments` (
  `EquipmentID` int NOT NULL AUTO_INCREMENT,
  `EquipmentName` varchar(100) DEFAULT NULL,
  `TrainingLocation` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`EquipmentID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `equipments` */

insert  into `equipments`(`EquipmentID`,`EquipmentName`,`TrainingLocation`) values 
(1,'跑步机','健身房'),
(2,'哑铃','力量训练区'),
(3,'跑步机','跑步区');

/*Table structure for table `membercourses` */

DROP TABLE IF EXISTS `membercourses`;

CREATE TABLE `membercourses` (
  `MemberID` int NOT NULL,
  `CourseID` int NOT NULL,
  PRIMARY KEY (`MemberID`,`CourseID`),
  KEY `CourseID` (`CourseID`),
  CONSTRAINT `membercourses_ibfk_1` FOREIGN KEY (`MemberID`) REFERENCES `members` (`MemberID`),
  CONSTRAINT `membercourses_ibfk_2` FOREIGN KEY (`CourseID`) REFERENCES `courses` (`CourseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `membercourses` */

/*Table structure for table `memberlog` */

DROP TABLE IF EXISTS `memberlog`;

CREATE TABLE `memberlog` (
  `LogID` int NOT NULL AUTO_INCREMENT,
  `MemberID` int DEFAULT NULL,
  `ChangeDate` datetime DEFAULT NULL,
  `Action` varchar(50) DEFAULT NULL,
  `OldName` varchar(50) DEFAULT NULL,
  `NewName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`LogID`),
  KEY `MemberID` (`MemberID`),
  CONSTRAINT `memberlog_ibfk_1` FOREIGN KEY (`MemberID`) REFERENCES `members` (`MemberID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `memberlog` */

/*Table structure for table `members` */

DROP TABLE IF EXISTS `members`;

CREATE TABLE `members` (
  `MemberID` int NOT NULL,
  `MemberName` varchar(50) DEFAULT NULL,
  `RegisterDate` date DEFAULT NULL,
  `Sex` varchar(10) DEFAULT NULL,
  `Birth` date DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Height` float DEFAULT NULL,
  `Weight` float DEFAULT NULL,
  PRIMARY KEY (`MemberID`),
  KEY `idx_member_name` (`MemberName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `members` */

insert  into `members`(`MemberID`,`MemberName`,`RegisterDate`,`Sex`,`Birth`,`Phone`,`Height`,`Weight`) values 
(1,'王某昊','2024-06-15','男','2024-06-01','666',166,62),
(2,'李四','2024-06-02','男','2024-06-01','666',172,62),
(3,'王某','2024-06-16','男','2024-06-01','666',169,67);

/*Table structure for table `worker` */

DROP TABLE IF EXISTS `worker`;

CREATE TABLE `worker` (
  `WorkerID` int NOT NULL AUTO_INCREMENT,
  `WorkerName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Birth` date DEFAULT NULL,
  `Sex` varchar(10) DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Job` varchar(50) DEFAULT NULL,
  `WorkTime` date DEFAULT NULL,
  PRIMARY KEY (`WorkerID`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `worker` */

insert  into `worker`(`WorkerID`,`WorkerName`,`Birth`,`Sex`,`Phone`,`Job`,`WorkTime`) values 
(23,'李明','2024-06-01','男','66666','普通员工','2024-06-09');

/* Trigger structure for table `members` */

DELIMITER $$

/*!50003 DROP TRIGGER*//*!50032 IF EXISTS */ /*!50003 `trg_after_member_update` */$$

/*!50003 CREATE */ /*!50017 DEFINER = 'root'@'localhost' */ /*!50003 TRIGGER `trg_after_member_update` AFTER UPDATE ON `members` FOR EACH ROW BEGIN
    INSERT INTO MemberLog (MemberID, ChangeDate, Action, OldName, NewName)
    VALUES (OLD.MemberID, NOW(), 'UPDATE', OLD.MemberName, NEW.MemberName);
END */$$


DELIMITER ;

/* Procedure structure for procedure `AddMember` */

/*!50003 DROP PROCEDURE IF EXISTS  `AddMember` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `AddMember`(
    IN p_MemberName VARCHAR(50),
    IN p_RegisterDate DATE,
    IN p_Sex VARCHAR(10),
    IN p_Birth DATE,
    IN p_Phone VARCHAR(20),
    IN p_Height FLOAT,
    IN p_Weight FLOAT
)
BEGIN
    INSERT INTO Members (MemberName, RegisterDate, Sex, Birth, Phone, Height, Weight)
    VALUES (p_MemberName, p_RegisterDate, p_Sex, p_Birth, p_Phone, p_Height, p_Weight);
END */$$
DELIMITER ;

/*Table structure for table `membersinfo` */

DROP TABLE IF EXISTS `membersinfo`;

/*!50001 DROP VIEW IF EXISTS `membersinfo` */;
/*!50001 DROP TABLE IF EXISTS `membersinfo` */;

/*!50001 CREATE TABLE  `membersinfo`(
 `MemberID` int ,
 `MemberName` varchar(50) ,
 `RegisterDate` date ,
 `Sex` varchar(10) ,
 `Birth` date ,
 `Phone` varchar(20) ,
 `Height` float ,
 `Weight` float 
)*/;

/*View structure for view membersinfo */

/*!50001 DROP TABLE IF EXISTS `membersinfo` */;
/*!50001 DROP VIEW IF EXISTS `membersinfo` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `membersinfo` AS select `members`.`MemberID` AS `MemberID`,`members`.`MemberName` AS `MemberName`,`members`.`RegisterDate` AS `RegisterDate`,`members`.`Sex` AS `Sex`,`members`.`Birth` AS `Birth`,`members`.`Phone` AS `Phone`,`members`.`Height` AS `Height`,`members`.`Weight` AS `Weight` from `members` */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
