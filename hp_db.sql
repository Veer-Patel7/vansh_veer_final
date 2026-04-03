-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: hp_db
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_passwordresettoken`
--

DROP TABLE IF EXISTS `accounts_passwordresettoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_passwordresettoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(64) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `accounts_passwordresettoken_user_id_2789bc5c_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `accounts_passwordresettoken_user_id_2789bc5c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_passwordresettoken`
--

LOCK TABLES `accounts_passwordresettoken` WRITE;
/*!40000 ALTER TABLE `accounts_passwordresettoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_passwordresettoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `otp` varchar(6) DEFAULT NULL,
  `profile_photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=141 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$1200000$Qk5VSufBSgUCLzBEwFlNh8$kCYDacbcXDEi1gd3N1WQaotckp9DDZ53K/KCIc6+GXw=','2026-03-31 10:34:56.126145',0,'PATEL','VANSH',0,1,'2026-03-12 04:44:08.584822','vansh','vanshpatel3175@gmail.com',NULL,'hotel_admin',1,'951878',''),(2,'pbkdf2_sha256$1200000$5tPfkdWrvK28DPwKtOs7Nb$RAhbC1TTB4RKyGYo/9I8A0JapC+WBQRWjLfNhNynM50=','2026-04-01 17:14:43.240285',1,'','',1,1,'2026-03-12 04:59:46.713932','vansh31','vansh31@gmail.com',NULL,'super_admin',1,NULL,'profiles/nature-background-high-resolution-wallpaper-for-a-serene-and-stunning-view-free-photo.jpg'),(3,'pbkdf2_sha256$1200000$xV5i9dUa66IdfAHveyi6EA$mWXIOsTM30KHcnWu7lOxyDLJO7Z8ubYZZ3s+hFC6JTE=','2026-04-01 17:16:27.322825',0,'bunty','patel',0,1,'2026-03-12 11:00:04.182159','buntyp200@gmail.com','buntyp200@gmail.com',NULL,'customer',1,'',''),(134,'pbkdf2_sha256$1200000$1Q4t8un9imkqdrZCZiOJIS$zXGLvjOSCCjZ9e94KSopMYMkcqHWNBD/++dx9Er4fR0=','2026-03-31 10:40:10.532818',0,'test','[atel',0,1,'2026-03-31 10:39:50.241104','tets','test123@gmail.com',NULL,'hotel_admin',1,'',''),(135,'pbkdf2_sha256$1200000$y0PUoohcAGqZwIcgKKOUS2$YFBbpDOQOsIiHLLttFJ3sRBGWwZyMDVwK3NoJ0tsC6o=','2026-04-01 09:37:29.501115',0,'test','patel',0,1,'2026-04-01 09:11:07.924737','admin','test@gmail.com',NULL,'hotel_admin',1,'',''),(136,'pbkdf2_sha256$1200000$SCyeZdLQxPLvovnZUVMU2V$Nx5dqAroYhssJafpFPDC7VwTgSXH6zTvw/ymvUAXbDI=','2026-04-01 12:06:42.573066',1,'','',1,1,'2026-04-01 09:25:03.771959','veerptl','220140107054veerpatel@gmail.com',NULL,'super_admin',1,NULL,''),(137,'pbkdf2_sha256$1200000$36Z3VaZUsSgJaZXPCsU2nG$R6sQGUP6YCFScP5euTdChLpiOboD/3aH5z3cthy2anw=','2026-04-01 11:24:12.104172',0,'test','hello',0,1,'2026-04-01 11:23:22.016012','test123124','virptl176@gmail.com',NULL,'hotel_admin',1,'',''),(138,'pbkdf2_sha256$1200000$g5fXf2lYT8WzJkTyaFtZF6$VJMbgBN4YhtUgHA/yXfNJlVYB3G8CovD2zGJJhSEUEg=',NULL,0,'vansh','patell',0,0,'2026-04-01 12:03:40.859667','vansh123','vansu@gmail.com',NULL,'hotel_admin',0,'672819',''),(139,'pbkdf2_sha256$1200000$EPHb2o7EfF4t1Q08R3dkL6$EpEXculhHiLwAbv6pmwpc99I4Vs8a9ccbNhNZKNbS44=','2026-04-01 12:04:44.276717',0,'vansh','patell',0,1,'2026-04-01 12:04:00.972720','vansh1233','vansuu@gmail.com',NULL,'hotel_admin',1,'',''),(140,'pbkdf2_sha256$1200000$UcKFw3nGk6OyPULE60Ivk2$NVkZK6T7R1ZyFRBGHNoA/WOO22yTPSFm6GxkL4tNr8A=','2026-04-01 17:12:03.032064',0,'rohan','ptl',0,1,'2026-04-01 17:10:13.807544','rohan','rp@gmail.com',NULL,'hotel_admin',1,'','');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',7,'add_user'),(22,'Can change user',7,'change_user'),(23,'Can delete user',7,'delete_user'),(24,'Can view user',7,'view_user'),(25,'Can add password reset token',6,'add_passwordresettoken'),(26,'Can change password reset token',6,'change_passwordresettoken'),(27,'Can delete password reset token',6,'delete_passwordresettoken'),(28,'Can view password reset token',6,'view_passwordresettoken'),(29,'Can add hotel',9,'add_hotel'),(30,'Can change hotel',9,'change_hotel'),(31,'Can delete hotel',9,'delete_hotel'),(32,'Can view hotel',9,'view_hotel'),(33,'Can add change request',8,'add_changerequest'),(34,'Can change change request',8,'change_changerequest'),(35,'Can delete change request',8,'delete_changerequest'),(36,'Can view change request',8,'view_changerequest'),(37,'Can add Hotel Image',10,'add_hotelimage'),(38,'Can change Hotel Image',10,'change_hotelimage'),(39,'Can delete Hotel Image',10,'delete_hotelimage'),(40,'Can view Hotel Image',10,'view_hotelimage'),(41,'Can add location history',11,'add_locationhistory'),(42,'Can change location history',11,'change_locationhistory'),(43,'Can delete location history',11,'delete_locationhistory'),(44,'Can view location history',11,'view_locationhistory'),(45,'Can add offer',12,'add_offer'),(46,'Can change offer',12,'change_offer'),(47,'Can delete offer',12,'delete_offer'),(48,'Can view offer',12,'view_offer'),(49,'Can add room type',14,'add_roomtype'),(50,'Can change room type',14,'change_roomtype'),(51,'Can delete room type',14,'delete_roomtype'),(52,'Can view room type',14,'view_roomtype'),(53,'Can add room photo',13,'add_roomphoto'),(54,'Can change room photo',13,'change_roomphoto'),(55,'Can delete room photo',13,'delete_roomphoto'),(56,'Can view room photo',13,'view_roomphoto'),(57,'Can add booking',15,'add_booking'),(58,'Can change booking',15,'change_booking'),(59,'Can delete booking',15,'delete_booking'),(60,'Can view booking',15,'view_booking'),(61,'Can add hotel commission',16,'add_hotelcommission'),(62,'Can change hotel commission',16,'change_hotelcommission'),(63,'Can delete hotel commission',16,'delete_hotelcommission'),(64,'Can view hotel commission',16,'view_hotelcommission'),(65,'Can add review',17,'add_review'),(66,'Can change review',17,'change_review'),(67,'Can delete review',17,'delete_review'),(68,'Can view review',17,'view_review'),(69,'Can add room',21,'add_room'),(70,'Can change room',21,'change_room'),(71,'Can delete room',21,'delete_room'),(72,'Can view room',21,'view_room'),(73,'Can add notification',19,'add_notification'),(74,'Can change notification',19,'change_notification'),(75,'Can delete notification',19,'delete_notification'),(76,'Can view notification',19,'view_notification'),(77,'Can add review',20,'add_review'),(78,'Can change review',20,'change_review'),(79,'Can delete review',20,'delete_review'),(80,'Can view review',20,'view_review'),(81,'Can add booking',18,'add_booking'),(82,'Can change booking',18,'change_booking'),(83,'Can delete booking',18,'delete_booking'),(84,'Can view booking',18,'view_booking'),(85,'Can add Room Photo',22,'add_roomimage'),(86,'Can change Room Photo',22,'change_roomimage'),(87,'Can delete Room Photo',22,'delete_roomimage'),(88,'Can view Room Photo',22,'view_roomimage');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookings_booking`
--

DROP TABLE IF EXISTS `bookings_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings_booking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `checkin_date` date NOT NULL,
  `checkout_date` date NOT NULL,
  `total_guests` smallint NOT NULL,
  `adults` smallint NOT NULL,
  `children` smallint NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `booking_status` varchar(20) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `cancel_reason` longtext,
  `created_at` datetime(6) NOT NULL,
  `hotel_id` bigint NOT NULL,
  `room_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `applied_offer_id` bigint DEFAULT NULL,
  `base_price` decimal(10,2) NOT NULL,
  `discount_amount` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bookings_booking_hotel_id_e1f8132f_fk_hotels_hotel_id` (`hotel_id`),
  KEY `bookings_booking_room_id_6f0fa517_fk_hotels_roomtype_id` (`room_id`),
  KEY `bookings_booking_user_id_834dfc23_fk_accounts_user_id` (`user_id`),
  KEY `bookings_booking_applied_offer_id_82c9529a_fk_hotels_offer_id` (`applied_offer_id`),
  CONSTRAINT `bookings_booking_applied_offer_id_82c9529a_fk_hotels_offer_id` FOREIGN KEY (`applied_offer_id`) REFERENCES `hotels_offer` (`id`),
  CONSTRAINT `bookings_booking_hotel_id_e1f8132f_fk_hotels_hotel_id` FOREIGN KEY (`hotel_id`) REFERENCES `hotels_hotel` (`id`),
  CONSTRAINT `bookings_booking_room_id_6f0fa517_fk_hotels_roomtype_id` FOREIGN KEY (`room_id`) REFERENCES `hotels_roomtype` (`id`),
  CONSTRAINT `bookings_booking_user_id_834dfc23_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings_booking`
--

LOCK TABLES `bookings_booking` WRITE;
/*!40000 ALTER TABLE `bookings_booking` DISABLE KEYS */;
INSERT INTO `bookings_booking` VALUES (77,'2026-04-01','2026-04-03',3,2,1,'cash','confirmed',12404.00,NULL,'2026-03-31 08:17:02.954964',71,137,3,NULL,12404.00,0.00),(78,'2026-04-02','2026-04-04',2,2,0,'cash','confirmed',6814.00,NULL,'2026-03-31 08:48:36.085697',71,122,3,NULL,6814.00,0.00),(79,'2026-04-03','2026-04-04',2,2,0,'cash','confirmed',1450.00,NULL,'2026-04-01 17:16:31.639903',85,145,3,NULL,1450.00,0.00),(80,'2026-04-03','2026-04-04',4,3,1,'cash','confirmed',1450.00,NULL,'2026-04-01 17:17:10.552118',85,145,3,NULL,1450.00,0.00),(81,'2026-04-30','2026-05-02',3,1,2,'cash','confirmed',2900.00,NULL,'2026-04-01 17:18:59.194214',85,145,3,NULL,2900.00,0.00),(82,'2026-04-03','2026-04-04',3,3,0,'cash','confirmed',1450.00,NULL,'2026-04-01 17:19:30.390129',85,145,3,NULL,1450.00,0.00);
/*!40000 ALTER TABLE `bookings_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_booking`
--

DROP TABLE IF EXISTS `core_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_booking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `discount_amount` decimal(10,2) NOT NULL,
  `base_price` decimal(10,2) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `check_in` date NOT NULL,
  `check_out` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `applied_offer_id` bigint DEFAULT NULL,
  `hotel_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `room_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_booking_applied_offer_id_c991e29e_fk_hotels_offer_id` (`applied_offer_id`),
  KEY `core_booking_hotel_id_ace2bc08_fk_hotels_hotel_id` (`hotel_id`),
  KEY `core_booking_user_id_55d9bfa8_fk_accounts_user_id` (`user_id`),
  KEY `core_booking_room_id_a3e37e85_fk_core_room_id` (`room_id`),
  CONSTRAINT `core_booking_applied_offer_id_c991e29e_fk_hotels_offer_id` FOREIGN KEY (`applied_offer_id`) REFERENCES `hotels_offer` (`id`),
  CONSTRAINT `core_booking_hotel_id_ace2bc08_fk_hotels_hotel_id` FOREIGN KEY (`hotel_id`) REFERENCES `hotels_hotel` (`id`),
  CONSTRAINT `core_booking_room_id_a3e37e85_fk_core_room_id` FOREIGN KEY (`room_id`) REFERENCES `core_room` (`id`),
  CONSTRAINT `core_booking_user_id_55d9bfa8_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_booking`
--

LOCK TABLES `core_booking` WRITE;
/*!40000 ALTER TABLE `core_booking` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_notification`
--

DROP TABLE IF EXISTS `core_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `message` longtext NOT NULL,
  `notification_type` varchar(20) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_notification_user_id_6e341aac_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `core_notification_user_id_6e341aac_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_notification`
--

LOCK TABLES `core_notification` WRITE;
/*!40000 ALTER TABLE `core_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_review`
--

DROP TABLE IF EXISTS `core_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_review` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `rating` int NOT NULL,
  `comment` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `hotel_id` bigint DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_review_hotel_id_8ca8188b_fk_hotels_hotel_id` (`hotel_id`),
  KEY `core_review_user_id_b6106194_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `core_review_hotel_id_8ca8188b_fk_hotels_hotel_id` FOREIGN KEY (`hotel_id`) REFERENCES `hotels_hotel` (`id`),
  CONSTRAINT `core_review_user_id_b6106194_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_review`
--

LOCK TABLES `core_review` WRITE;
/*!40000 ALTER TABLE `core_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_room`
--

DROP TABLE IF EXISTS `core_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_room` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `room_number` varchar(10) NOT NULL,
  `room_type` varchar(20) NOT NULL,
  `price_per_night` decimal(10,2) NOT NULL,
  `description` longtext NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `capacity` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `room_number` (`room_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_room`
--

LOCK TABLES `core_room` WRITE;
/*!40000 ALTER TABLE `core_room` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts','passwordresettoken'),(7,'accounts','user'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(15,'bookings','booking'),(4,'contenttypes','contenttype'),(18,'core','booking'),(19,'core','notification'),(20,'core','review'),(21,'core','room'),(8,'hotels','changerequest'),(9,'hotels','hotel'),(10,'hotels','hotelimage'),(11,'hotels','locationhistory'),(12,'hotels','offer'),(22,'hotels','roomimage'),(13,'hotels','roomphoto'),(14,'hotels','roomtype'),(16,'payments','hotelcommission'),(17,'reviews','review'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-03-12 04:37:56.352522'),(2,'contenttypes','0002_remove_content_type_name','2026-03-12 04:37:56.480957'),(3,'auth','0001_initial','2026-03-12 04:37:56.825082'),(4,'auth','0002_alter_permission_name_max_length','2026-03-12 04:37:56.914351'),(5,'auth','0003_alter_user_email_max_length','2026-03-12 04:37:56.920286'),(6,'auth','0004_alter_user_username_opts','2026-03-12 04:37:56.928484'),(7,'auth','0005_alter_user_last_login_null','2026-03-12 04:37:56.938456'),(8,'auth','0006_require_contenttypes_0002','2026-03-12 04:37:56.945347'),(9,'auth','0007_alter_validators_add_error_messages','2026-03-12 04:37:56.958867'),(10,'auth','0008_alter_user_username_max_length','2026-03-12 04:37:56.966851'),(11,'auth','0009_alter_user_last_name_max_length','2026-03-12 04:37:56.977475'),(12,'auth','0010_alter_group_name_max_length','2026-03-12 04:37:57.001960'),(13,'auth','0011_update_proxy_permissions','2026-03-12 04:37:57.012431'),(14,'auth','0012_alter_user_first_name_max_length','2026-03-12 04:37:57.021707'),(15,'accounts','0001_initial','2026-03-12 04:37:57.680100'),(16,'accounts','0002_user_profile_photo','2026-03-12 04:37:57.759068'),(17,'admin','0001_initial','2026-03-12 04:37:57.949688'),(18,'admin','0002_logentry_remove_auto_add','2026-03-12 04:37:57.959743'),(19,'admin','0003_logentry_add_action_flag_choices','2026-03-12 04:37:57.972909'),(20,'hotels','0001_initial','2026-03-12 04:37:58.685072'),(21,'hotels','0002_remove_hotel_account_holder_and_more','2026-03-12 04:37:59.450022'),(22,'bookings','0001_initial','2026-03-12 04:37:59.729866'),(23,'bookings','0002_booking_applied_offer_booking_base_price_and_more','2026-03-12 04:37:59.993175'),(24,'core','0001_initial','2026-03-12 04:38:00.649983'),(25,'core','0002_alter_booking_applied_offer','2026-03-12 04:38:00.652003'),(26,'hotels','0003_roomcategory_hotelgallery_roomphoto','2026-03-12 04:38:00.910110'),(27,'hotels','0004_roomcategory_hotel_alter_offer_hotel','2026-03-12 04:38:01.026033'),(28,'hotels','0005_remove_roomphoto_room_category_and_more','2026-03-12 04:38:01.568820'),(29,'hotels','0006_alter_hotelimage_options_alter_hotel_check_in_and_more','2026-03-12 04:38:01.630319'),(30,'hotels','0007_hotel_onboarding_step','2026-03-12 04:38:01.737310'),(31,'payments','0001_initial','2026-03-12 04:38:01.858620'),(32,'reviews','0001_initial','2026-03-12 04:38:02.048090'),(33,'sessions','0001_initial','2026-03-12 04:38:02.102045'),(34,'hotels','0008_offer_combinable_offers_offer_targeted_hotels_and_more','2026-03-17 05:43:35.363287'),(35,'bookings','0003_alter_booking_booking_status','2026-03-23 04:11:13.583193'),(36,'hotels','0009_remove_roomtype_room_image_roomimage','2026-04-01 12:01:07.651574'),(37,'hotels','0010_delete_roomphoto','2026-04-01 17:05:11.946676');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0n15chzmhsspucqsyrnu3yqhsx797nrr','.eJxVjMsOwiAQRf-FtSE8LBSX7vsNZIYZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mLMOL0uyGkB9cd0B3qrcnU6rrMKHdFHrTLqRE_r4f7d1Cgl2_tjKJMDA7Q-pCDA229d2jYp6Bc1meyTHpklXigAQMi-QB2yAhhRCPeH_3YOM8:1w7rhA:SjXYNC6JW5ZEkbCpEjwDuPZ-gvUcIrVwSpcnZaW_lo8','2026-04-15 09:17:04.127669'),('1u54x78btrtu5n0vgr7rfuqpz1k3x14w','e30:1w0w0D:AOg4bKDobFoYeq1BCTrnqJuaNiVvsRzUuyyI8uIvotE','2026-03-27 06:28:05.546945'),('66rlnkhkro74x1tffgd0e88vni7mqkao','.eJxVjMEOwiAQRP-FsyFbKAU8eu83kC27SNVAUtqT8d-1pgc9TTLvzTxFwG3NYWu8hJnEWWhx-u0mjHcuO6AblmuVsZZ1mSe5K_KgTY6V-HE53L-DjC1_1r53CSl1JjJ4Y3UCRc7piD4hd4qhR8OU1GBdAv9Nsn4AiKxtH7V4vQHx5zft:1w7sTD:_l9I4JZp9xqSO1SW-YvMe7g7jCbiIQQDlto_D4Lh9HA','2026-04-15 10:06:43.718711'),('alveiubkg80lrtz14l0yqwpvqsu637b5','.eJxVjMsOwiAQRf-FtSE8LBSX7vsNZIYZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mLMOL0uyGkB9cd0B3qrcnU6rrMKHdFHrTLqRE_r4f7d1Cgl2_tjKJMDA7Q-pCDA229d2jYp6Bc1meyTHpklXigAQMi-QB2yAhhRCPeH_3YOM8:1w7rkG:fv4XNM0QEUz6si--w6fHlJwWYrHGg_jWUQgK2SaTGkU','2026-04-15 09:20:16.992137'),('bcxsf2vo1ipwqmhe539uuyupzjw0k7wf','.eJxVjMsOwiAQRf-FtSE8LBSX7vsNZIYZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mLMOL0uyGkB9cd0B3qrcnU6rrMKHdFHrTLqRE_r4f7d1Cgl2_tjKJMDA7Q-pCDA229d2jYp6Bc1meyTHpklXigAQMi-QB2yAhhRCPeH_3YOM8:1w2OlT:azUoC8co3KVYC_fDssVQoAzTCBjQJi_mTJ5PtYPFMl8','2026-03-31 07:22:55.886343'),('cdx3gele4oihqkbia79frsv2elb0848i','.eJxVjMsOwiAQRf-FtSE8LBSX7vsNZIYZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mLMOL0uyGkB9cd0B3qrcnU6rrMKHdFHrTLqRE_r4f7d1Cgl2_tjKJMDA7Q-pCDA229d2jYp6Bc1meyTHpklXigAQMi-QB2yAhhRCPeH_3YOM8:1w2062:HG_8a5lFaw0ytpkLhOT5aWski5-XOLur9Sh2gtNB1HY','2026-03-30 05:02:30.290342'),('hh1qec4zszru7gjdf8jlw11o5dcnxxb3','.eJxVjMsOwiAQRf-FtSHlMTxcuvcbyMCAVA0kpV0Z_12bdKHbe865LxZwW2vYRl7CTOzMhAJ2-l0jpkduO6I7tlvnqbd1mSPfFX7Qwa-d8vNyuH8HFUf91iiNwzgpSLYoqXJ0NBmDFkEbJ4lM8VZFzI4QMiYQ2nspbCoetSkQ2fsDNUA4pA:1w7rc1:-REfLa4UMYxsRPSPqWUTfVDaZAIFMxSBFnDxc_ISNHw','2026-04-15 09:11:45.773005'),('iq1iu4tudctcpvyzv7pnwbxz37ajuvx1','.eJxlkMFuwyAMht-FcxsRQhLocfc9A3LAhKwETwk5TFXffRBV06ad0OfvxzY8mIEjB3PsuJnFsRvr2OV3bQJ7x1SF-4A0U2Mp5W2ZmhppXnZv3slhfHtl_zQIsIdyW0vlwfm2t8h1P3aeC6dUZ0F7wFYgl9Cj82IYlef6PN2oB84tdqO0dauJ6L6k2TjIwG4PFihjPJdW_YVtROsJrSxkA9oSrlks0wUXw5XLK699TkdH_idlkZkyRDMfuOe9ulICd8QfsGGJbsNUkBf8hK8VUzYr5kD1l2x97vP5DdhsbWY:1w7zEO:CGkgIXQBMxYs7dTxa6jIG83qDrpgRoAkWbSK42ESv-U','2026-04-15 17:19:52.392624'),('jcktymsjvudkq5mi2lvr0w2mdr52a7cm','.eJxVjEEOwiAQRe_C2hAYCk5duvcMZBhGqRpISrsy3l2bdKHb_977LxVpXUpcu8xxyuqkrAvq8Lsm4ofUDeU71VvT3OoyT0lvit5p15eW5Xne3b-DQr18axDGkAyLQeDBknfgRoeSgBnEhwQIksGi9aOho0exWeAaYLCMJrB6fwAkrDfL:1w7rt6:OQCxiIs-4eBZu-M1n0k9BMMP6W5e6GLvzz-LziaSfBU','2026-04-15 09:29:24.675590'),('lhedrte9yunrv929bffjej4rkx8ygf82','.eJxVjMsOwiAQRf-FtSE8LBSX7vsNZIYZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mLMOL0uyGkB9cd0B3qrcnU6rrMKHdFHrTLqRE_r4f7d1Cgl2_tjKJMDA7Q-pCDA229d2jYp6Bc1meyTHpklXigAQMi-QB2yAhhRCPeH_3YOM8:1w7rej:iF2Fdoy9_LbilPbIij_ziamS8W3ETozT8ASe6yp26JE','2026-04-15 09:14:33.114938'),('nqo07xwaypywo2car8h3juy2yjjyph9y','.eJxVjMsOwiAQRf-FtSE8LBSX7vsNZIYZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mLMOL0uyGkB9cd0B3qrcnU6rrMKHdFHrTLqRE_r4f7d1Cgl2_tjKJMDA7Q-pCDA229d2jYp6Bc1meyTHpklXigAQMi-QB2yAhhRCPeH_3YOM8:1w7rjH:jXksy81XUZ9Yh9rIXN-LcZvO95TrC5nLKYbTvUFHnCs','2026-04-15 09:19:15.220937'),('rqukdc0yf3k41xmwwi4fmgy5clcyr61k','.eJxVjMsOwiAQRf-FtSE8LBSX7vsNZIYZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mLMOL0uyGkB9cd0B3qrcnU6rrMKHdFHrTLqRE_r4f7d1Cgl2_tjKJMDA7Q-pCDA229d2jYp6Bc1meyTHpklXigAQMi-QB2yAhhRCPeH_3YOM8:1w7rfL:hvJaaHZT4u_5cWnRpaigoWMmcTbc46PookX_CSuQEYs','2026-04-15 09:15:11.666274'),('u71691bwxd54enzqwd6jhia6hhnts8d8','.eJxVjMsOwiAQRf-FtSE8LBSX7vsNZIYZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mLMOL0uyGkB9cd0B3qrcnU6rrMKHdFHrTLqRE_r4f7d1Cgl2_tjKJMDA7Q-pCDA229d2jYp6Bc1meyTHpklXigAQMi-QB2yAhhRCPeH_3YOM8:1w7rg6:tQIZQ5FoOU_bMA5SMUstiwM5tO5TpmLePIgILLb05kI','2026-04-15 09:15:58.137209'),('xdy91ldffoq2qucpaqqhyvfqdclpinwu','.eJxVjMEOwiAQRP-FsyFbKAU8eu83kC27SNVAUtqT8d-1pgc9TTLvzTxFwG3NYWu8hJnEWWhx-u0mjHcuO6AblmuVsZZ1mSe5K_KgTY6V-HE53L-DjC1_1r53CSl1JjJ4Y3UCRc7piD4hd4qhR8OU1GBdAv9Nsn4AiKxtH7V4vQHx5zft:1w7sGS:Uhq7gyedd2JYt5fZboKilRKQrJzhIQEg01NSzB5WwVs','2026-04-15 09:53:32.194873'),('xhg6g6vuiq4xc79448yv89oamkkak1rv','e30:1w0vzs:ptbtdgzJu9tpLsbB-33LFZj5eHyi6NtdE2xJZtwPdDU','2026-03-27 06:27:44.015997'),('xr7v8kkbh3d1dmsii3opv7mljhktv792','.eJxVjDEOwjAMRe-SGUVO1NgJIztniJzaJQXUSk07Ie4OlTrA-t97_2Uyb2vNW9Mlj2LOBs3pdyvcP3Tagdx5us22n6d1GYvdFXvQZq-z6PNyuH8HlVv91gU9oHhIIAXIYfCuA_HqMBYijto7BE2BByUilAGGROSgi8wcyJn3B79eNxE:1w5NCa:itZgvLS_cvV2LOo3UEuYkFU-OPX6qqFR9ppDd9Ch-Bk','2026-04-08 12:19:12.103572');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels_changerequest`
--

DROP TABLE IF EXISTS `hotels_changerequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels_changerequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category` varchar(20) NOT NULL,
  `requested_data` json NOT NULL,
  `status` varchar(20) NOT NULL,
  `remarks` longtext,
  `requested_at` datetime(6) NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `hotel_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hotels_changerequest_hotel_id_9c055c30_fk_hotels_hotel_id` (`hotel_id`),
  CONSTRAINT `hotels_changerequest_hotel_id_9c055c30_fk_hotels_hotel_id` FOREIGN KEY (`hotel_id`) REFERENCES `hotels_hotel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels_changerequest`
--

LOCK TABLES `hotels_changerequest` WRITE;
/*!40000 ALTER TABLE `hotels_changerequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `hotels_changerequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels_hotel`
--

DROP TABLE IF EXISTS `hotels_hotel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels_hotel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `hotel_name` varchar(255) NOT NULL,
  `hotel_type` varchar(50) NOT NULL,
  `services` json NOT NULL,
  `description` longtext NOT NULL,
  `total_rooms` int unsigned NOT NULL,
  `check_in` time(6) NOT NULL,
  `check_out` time(6) NOT NULL,
  `cancellation_policy` longtext NOT NULL,
  `id_type` varchar(10) NOT NULL,
  `id_number` varchar(20) DEFAULT NULL,
  `doc_mandatory` varchar(100) DEFAULT NULL,
  `govt_reg_number` varchar(50) DEFAULT NULL,
  `doc_certificate` varchar(100) DEFAULT NULL,
  `gst_number` varchar(15) DEFAULT NULL,
  `doc_gst` varchar(100) DEFAULT NULL,
  `address` longtext NOT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `lat` decimal(22,16) DEFAULT NULL,
  `lng` decimal(22,16) DEFAULT NULL,
  `status` varchar(15) NOT NULL,
  `verification_remarks` longtext,
  `is_live` tinyint(1) NOT NULL,
  `submitted_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `owner_id` bigint NOT NULL,
  `onboarding_step` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hotels_hotel_owner_id_dae0ba86_fk_accounts_user_id` (`owner_id`),
  CONSTRAINT `hotels_hotel_owner_id_dae0ba86_fk_accounts_user_id` FOREIGN KEY (`owner_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `hotels_hotel_chk_1` CHECK ((`total_rooms` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels_hotel`
--

LOCK TABLES `hotels_hotel` WRITE;
/*!40000 ALTER TABLE `hotels_hotel` DISABLE KEYS */;
INSERT INTO `hotels_hotel` VALUES (70,'Heritage Resort','LUXURY','[]','',0,'14:00:00.000000','11:00:00.000000','Standard Rules Apply','AADHAAR',NULL,'',NULL,'',NULL,'','Udaipur, Rajasthan','Udaipur','Rajasthan',NULL,NULL,NULL,'LIVE',NULL,1,NULL,'2026-03-31 07:15:18.230786',2,1),(71,'Palm Manor','LUXURY','[]','',0,'14:00:00.000000','11:00:00.000000','Standard Rules Apply','AADHAAR',NULL,'',NULL,'',NULL,'','Jaipur, Rajasthan','Jaipur','Rajasthan',NULL,NULL,NULL,'LIVE',NULL,1,NULL,'2026-03-31 07:15:18.257464',2,1),(72,'Royal Villa','LUXURY','[]','',0,'14:00:00.000000','11:00:00.000000','Standard Rules Apply','AADHAAR',NULL,'',NULL,'',NULL,'','Bangalore, Karnataka','Bangalore','Karnataka',NULL,NULL,NULL,'LIVE',NULL,1,NULL,'2026-03-31 07:15:18.262057',2,1),(73,'Blue Sanctuary','LUXURY','[]','',0,'14:00:00.000000','11:00:00.000000','Standard Rules Apply','AADHAAR',NULL,'',NULL,'',NULL,'','North Goa, Goa','Goa','Goa',NULL,NULL,NULL,'LIVE',NULL,1,NULL,'2026-03-31 07:15:18.264393',2,1),(74,'Emerald Manor','LUXURY','[]','',0,'14:00:00.000000','11:00:00.000000','Standard Rules Apply','AADHAAR',NULL,'',NULL,'',NULL,'','Manali, Himachal Pradesh','Manali','Himachal Pradesh',NULL,NULL,NULL,'LIVE',NULL,1,NULL,'2026-03-31 07:15:18.266390',2,1),(75,'Breeze Suites','LUXURY','[]','',0,'14:00:00.000000','11:00:00.000000','Standard Rules Apply','AADHAAR',NULL,'',NULL,'',NULL,'','Mumbai, Maharashtra','Mumbai','Maharashtra',NULL,NULL,NULL,'LIVE',NULL,1,NULL,'2026-03-31 07:15:18.269517',2,1),(76,'Palace Villa','LUXURY','[]','',0,'14:00:00.000000','11:00:00.000000','Standard Rules Apply','AADHAAR',NULL,'',NULL,'',NULL,'','New Delhi, Delhi','Delhi','Delhi',NULL,NULL,NULL,'LIVE',NULL,1,NULL,'2026-03-31 07:15:18.271776',2,1),(77,'Royal Sanctuary','LUXURY','[]','',0,'14:00:00.000000','11:00:00.000000','Standard Rules Apply','AADHAAR',NULL,'',NULL,'',NULL,'','Pune, Maharashtra','Pune','Maharashtra',NULL,NULL,NULL,'LIVE',NULL,1,NULL,'2026-03-31 07:15:18.273577',2,1),(78,'Imperial Lounge','LUXURY','[]','',0,'14:00:00.000000','11:00:00.000000','Standard Rules Apply','AADHAAR',NULL,'',NULL,'',NULL,'','Ahmedabad, Gujarat','Ahmedabad','Gujarat',NULL,NULL,NULL,'LIVE',NULL,1,NULL,'2026-03-31 07:15:18.277672',2,1),(79,'Heritage Hotel','LUXURY','[]','',0,'14:00:00.000000','11:00:00.000000','Standard Rules Apply','AADHAAR',NULL,'',NULL,'',NULL,'','Hyderabad, Telangana','Hyderabad','Telangana',NULL,NULL,NULL,'LIVE',NULL,1,NULL,'2026-03-31 07:15:18.279683',2,1),(80,'kirish ki property','5_STAR','[]','welcome to hotel the grand kirish',3,'11:00:00.000000','11:00:00.000000','NO refund','AADHAAR','1212-4141-4152','compliance/identity/download.png','rebtf','compliance/certificate/images.jpg','abc123','compliance/gst/nature-background-high-resolution-wallpaper-for-a-serene-and-stunning-vie_GOWInCv.jpg','Surat Gujarat, 300034, India','Majura Taluka','Gujarat','300034',21.1781048762000000,72.8318380432000000,'LIVE','Approved by Super Admin',1,'2026-03-31 09:28:43.243198','2026-03-31 09:28:43.192766',1,1),(81,'test','5_STAR','[]','hiiiii',1,'11:00:00.000000','11:00:00.000000','mo','AADHAAR','1212-4141-4152','compliance/identity/RESIDENTAIL1.jpg','rebtf','compliance/certificate/RESIDENTAIL.jpg','gthbtbrtbt','compliance/gst/RESIDENTAIL1.jpg','Surat',NULL,NULL,NULL,NULL,NULL,'LIVE','Approved by Super Admin',1,'2026-03-31 10:42:30.579282','2026-03-31 10:42:30.322993',134,1),(82,'Kalpavrix pro','5_STAR','[]','hello bhaio',3,'14:00:00.000000','11:00:00.000000','no','AADHAAR','1212-4141-4100','compliance/identity/nature-background-high-resolution-wallpaper-for-a-serene-and-stunnin_k2J3h0T.jpg','NKJ14135EFEFE','compliance/certificate/images.jpg','22AAAAM1412AAZ5','compliance/gst/images.jpg','amalsad',NULL,NULL,NULL,NULL,NULL,'LIVE','Approved by Super Admin',1,'2026-04-01 09:39:35.011391','2026-04-01 09:39:34.958430',135,1),(83,'test1245','4_STAR','[]','hiii vansh',3,'14:00:00.000000','11:00:00.000000','1455','AADHAAR','1212-4141-4152','compliance/identity/nature-background-high-resolution-wallpaper-for-a-serene-and-stunnin_rvo7jDJ.jpg','NKJ14135EFEFE','compliance/certificate/images_1T4jYyd.jpg','22AAAAM1412AAZ5','compliance/gst/images_DVvNq9X.jpg','abhishek nagar',NULL,NULL,NULL,NULL,NULL,'LIVE','Approved by Super Admin',1,'2026-04-01 11:26:46.845020','2026-04-01 11:26:46.793340',137,1),(84,'rohan ka dhaba','BUDGET','[]','hello bro',2,'14:00:00.000000','11:00:00.000000','no','AADHAAR','1212-4141-4152','compliance/identity/download.png','NKJ14135EFEFE','compliance/certificate/download.png','22AAAAM1412AAZ5','compliance/gst/download.png','desra',NULL,NULL,NULL,NULL,NULL,'LIVE','Approved by Super Admin',1,'2026-04-01 12:06:25.591773','2026-04-01 12:06:25.552370',139,1),(85,'pal rostorant','5_STAR','[]','pal na vila ma swagat chhe',3,'11:00:00.000000','11:00:00.000000','NO','AADHAAR','1212-4141-4152','compliance/identity/download_9t0KImZ.png','NKJ14135EFEFE','compliance/certificate/download_y6NpEtG.png','22AAAAM1412AAZ5','compliance/gst/download_dz2kvu5.png','Surat, Gujarat, 300034, India',NULL,NULL,NULL,NULL,NULL,'LIVE','Approved by Super Admin',1,'2026-04-01 17:14:15.520054','2026-04-01 17:14:15.432148',140,1);
/*!40000 ALTER TABLE `hotels_hotel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels_hotelimage`
--

DROP TABLE IF EXISTS `hotels_hotelimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels_hotelimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image_path` varchar(100) NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `hotel_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hotels_hotelimage_hotel_id_ff6c0c35_fk_hotels_hotel_id` (`hotel_id`),
  CONSTRAINT `hotels_hotelimage_hotel_id_ff6c0c35_fk_hotels_hotel_id` FOREIGN KEY (`hotel_id`) REFERENCES `hotels_hotel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=176 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels_hotelimage`
--

LOCK TABLES `hotels_hotelimage` WRITE;
/*!40000 ALTER TABLE `hotels_hotelimage` DISABLE KEYS */;
INSERT INTO `hotels_hotelimage` VALUES (132,'property_gallery/beach_resort_aerial_jpg_1774932218365.png',1,'2026-03-31 08:28:40.751265',70),(133,'property_gallery/luxury_hotel_facade_jpg_1774932202123.png',1,'2026-03-31 08:28:40.755187',71),(134,'property_gallery/mountain_hotel_exterior_jpg_1774932235357.png',1,'2026-03-31 08:28:40.756878',72),(135,'property_gallery/urban_boutique_hotel_jpg_1774932256758.png',1,'2026-03-31 08:28:40.758878',73),(148,'property_gallery/download_1.jpg',0,'2026-03-31 09:28:43.222993',80),(149,'property_gallery/download_2.jpg',0,'2026-03-31 09:28:43.227771',80),(150,'property_gallery/download_4.jpg',0,'2026-03-31 09:28:43.233999',80),(151,'property_gallery/download_5.jpg',0,'2026-03-31 09:28:43.238205',80),(152,'property_gallery/download.jpg',0,'2026-03-31 09:28:43.242148',80),(153,'property_gallery/RESIDENTAIL.jpg',0,'2026-03-31 10:42:30.577495',81),(154,'property_gallery/download_3.jpg',0,'2026-04-01 09:39:34.982517',82),(155,'property_gallery/download_4.jpg',0,'2026-04-01 09:39:34.993327',82),(156,'property_gallery/download_5.jpg',0,'2026-04-01 09:39:34.997509',82),(157,'property_gallery/download.jpg',0,'2026-04-01 09:39:35.000094',82),(158,'property_gallery/nature-background-high-resolution-wallpaper-for-a-serene-and-stunning-v_xHf2H6I.jpg',0,'2026-04-01 09:39:35.010540',82),(159,'property_gallery/download_3_eiTh1Z1.jpg',0,'2026-04-01 11:26:46.827449',83),(160,'property_gallery/download_5_2lenl3o.jpg',0,'2026-04-01 11:26:46.831494',83),(161,'property_gallery/nature-background-high-resolution-wallpaper-for-a-serene-and-stunning-v_iodlvHx.jpg',0,'2026-04-01 11:26:46.837576',83),(162,'property_gallery/WhatsApp_Image_2026-03-23_at_12.31.34_PM.jpeg',0,'2026-04-01 11:26:46.841703',83),(163,'property_gallery/WhatsApp_Image_2026-03-23_at_12.31.35_PM.jpeg',0,'2026-04-01 11:26:46.844339',83),(164,'property_gallery/download_2.jpg',0,'2026-04-01 12:06:25.571243',84),(165,'property_gallery/download_3_459Xkl4.jpg',0,'2026-04-01 12:06:25.574906',84),(166,'property_gallery/download_4_bGxw3D9.jpg',0,'2026-04-01 12:06:25.582428',84),(167,'property_gallery/download_5_C4zAs2G.jpg',0,'2026-04-01 12:06:25.585322',84),(168,'property_gallery/download_MNcH3Sz.jpg',0,'2026-04-01 12:06:25.588839',84),(169,'property_gallery/nature-background-high-resolution-wallpaper-for-a-serene-and-stunning-v_0n4Yitg.jpg',0,'2026-04-01 12:06:25.591102',84),(170,'property_gallery/download_1.jpg',0,'2026-04-01 17:14:15.478602',85),(171,'property_gallery/download_3_NfUMesw.jpg',0,'2026-04-01 17:14:15.484329',85),(172,'property_gallery/download_4_nIDgPHj.jpg',0,'2026-04-01 17:14:15.491692',85),(173,'property_gallery/download_5_WWDDV4M.jpg',0,'2026-04-01 17:14:15.505225',85),(174,'property_gallery/download_xWNmhP2.jpg',0,'2026-04-01 17:14:15.512212',85),(175,'property_gallery/nature-background-high-resolution-wallpaper-for-a-serene-and-stunning-v_8nVkZjA.jpg',0,'2026-04-01 17:14:15.518833',85);
/*!40000 ALTER TABLE `hotels_hotelimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels_locationhistory`
--

DROP TABLE IF EXISTS `hotels_locationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels_locationhistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `lat` decimal(12,9) NOT NULL,
  `lng` decimal(12,9) NOT NULL,
  `formatted_address` longtext NOT NULL,
  `city` varchar(100) DEFAULT NULL,
  `location_name` varchar(255) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `rating` decimal(3,1) DEFAULT NULL,
  `review_count` int unsigned NOT NULL,
  `image_reference` varchar(500) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hotels_locationhistory_user_id_231eb6bd_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `hotels_locationhistory_user_id_231eb6bd_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `hotels_locationhistory_chk_1` CHECK ((`review_count` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels_locationhistory`
--

LOCK TABLES `hotels_locationhistory` WRITE;
/*!40000 ALTER TABLE `hotels_locationhistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `hotels_locationhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels_offer`
--

DROP TABLE IF EXISTS `hotels_offer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels_offer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `offer_type` varchar(20) NOT NULL,
  `discount_type` varchar(20) NOT NULL,
  `discount_value` decimal(10,2) NOT NULL,
  `max_discount_limit` decimal(10,2) DEFAULT NULL,
  `coupon_code` varchar(50) DEFAULT NULL,
  `applicability` varchar(20) NOT NULL,
  `room_categories` json NOT NULL,
  `specific_rooms` json NOT NULL,
  `valid_from` datetime(6) NOT NULL,
  `valid_to` datetime(6) NOT NULL,
  `blackout_dates` json NOT NULL,
  `applicable_days` json NOT NULL,
  `min_amount` decimal(10,2) NOT NULL,
  `min_nights` int unsigned NOT NULL,
  `max_nights` int unsigned DEFAULT NULL,
  `advance_booking_days` int unsigned NOT NULL,
  `last_minute_window` int unsigned NOT NULL,
  `max_usage` int unsigned NOT NULL,
  `per_user_limit` int unsigned NOT NULL,
  `redemption_count` int unsigned NOT NULL,
  `is_stackable` tinyint(1) NOT NULL,
  `status` varchar(15) NOT NULL,
  `rejection_reason` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `hotel_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hotels_offer_hotel_id_c293d680_fk_hotels_hotel_id` (`hotel_id`),
  CONSTRAINT `hotels_offer_hotel_id_c293d680_fk_hotels_hotel_id` FOREIGN KEY (`hotel_id`) REFERENCES `hotels_hotel` (`id`),
  CONSTRAINT `hotels_offer_chk_1` CHECK ((`min_nights` >= 0)),
  CONSTRAINT `hotels_offer_chk_2` CHECK ((`max_nights` >= 0)),
  CONSTRAINT `hotels_offer_chk_3` CHECK ((`advance_booking_days` >= 0)),
  CONSTRAINT `hotels_offer_chk_4` CHECK ((`last_minute_window` >= 0)),
  CONSTRAINT `hotels_offer_chk_5` CHECK ((`max_usage` >= 0)),
  CONSTRAINT `hotels_offer_chk_6` CHECK ((`per_user_limit` >= 0)),
  CONSTRAINT `hotels_offer_chk_7` CHECK ((`redemption_count` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels_offer`
--

LOCK TABLES `hotels_offer` WRITE;
/*!40000 ALTER TABLE `hotels_offer` DISABLE KEYS */;
/*!40000 ALTER TABLE `hotels_offer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels_offer_combinable_offers`
--

DROP TABLE IF EXISTS `hotels_offer_combinable_offers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels_offer_combinable_offers` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `from_offer_id` bigint NOT NULL,
  `to_offer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hotels_offer_combinable__from_offer_id_to_offer_i_e8de3af0_uniq` (`from_offer_id`,`to_offer_id`),
  KEY `hotels_offer_combina_to_offer_id_2948cb54_fk_hotels_of` (`to_offer_id`),
  CONSTRAINT `hotels_offer_combina_from_offer_id_784b252e_fk_hotels_of` FOREIGN KEY (`from_offer_id`) REFERENCES `hotels_offer` (`id`),
  CONSTRAINT `hotels_offer_combina_to_offer_id_2948cb54_fk_hotels_of` FOREIGN KEY (`to_offer_id`) REFERENCES `hotels_offer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels_offer_combinable_offers`
--

LOCK TABLES `hotels_offer_combinable_offers` WRITE;
/*!40000 ALTER TABLE `hotels_offer_combinable_offers` DISABLE KEYS */;
/*!40000 ALTER TABLE `hotels_offer_combinable_offers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels_offer_targeted_hotels`
--

DROP TABLE IF EXISTS `hotels_offer_targeted_hotels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels_offer_targeted_hotels` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `offer_id` bigint NOT NULL,
  `hotel_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hotels_offer_targeted_hotels_offer_id_hotel_id_18177f9d_uniq` (`offer_id`,`hotel_id`),
  KEY `hotels_offer_targete_hotel_id_41bd3a57_fk_hotels_ho` (`hotel_id`),
  CONSTRAINT `hotels_offer_targete_hotel_id_41bd3a57_fk_hotels_ho` FOREIGN KEY (`hotel_id`) REFERENCES `hotels_hotel` (`id`),
  CONSTRAINT `hotels_offer_targete_offer_id_167f13ee_fk_hotels_of` FOREIGN KEY (`offer_id`) REFERENCES `hotels_offer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels_offer_targeted_hotels`
--

LOCK TABLES `hotels_offer_targeted_hotels` WRITE;
/*!40000 ALTER TABLE `hotels_offer_targeted_hotels` DISABLE KEYS */;
/*!40000 ALTER TABLE `hotels_offer_targeted_hotels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels_offer_targeted_rooms`
--

DROP TABLE IF EXISTS `hotels_offer_targeted_rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels_offer_targeted_rooms` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `offer_id` bigint NOT NULL,
  `roomtype_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hotels_offer_targeted_rooms_offer_id_roomtype_id_9680b173_uniq` (`offer_id`,`roomtype_id`),
  KEY `hotels_offer_targete_roomtype_id_0a4a06ea_fk_hotels_ro` (`roomtype_id`),
  CONSTRAINT `hotels_offer_targete_roomtype_id_0a4a06ea_fk_hotels_ro` FOREIGN KEY (`roomtype_id`) REFERENCES `hotels_roomtype` (`id`),
  CONSTRAINT `hotels_offer_targeted_rooms_offer_id_719f27c0_fk_hotels_offer_id` FOREIGN KEY (`offer_id`) REFERENCES `hotels_offer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels_offer_targeted_rooms`
--

LOCK TABLES `hotels_offer_targeted_rooms` WRITE;
/*!40000 ALTER TABLE `hotels_offer_targeted_rooms` DISABLE KEYS */;
/*!40000 ALTER TABLE `hotels_offer_targeted_rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels_roomimage`
--

DROP TABLE IF EXISTS `hotels_roomimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels_roomimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `media_file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `room_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hotels_roomimage_room_id_6a3533da_fk_hotels_roomtype_id` (`room_id`),
  CONSTRAINT `hotels_roomimage_room_id_6a3533da_fk_hotels_roomtype_id` FOREIGN KEY (`room_id`) REFERENCES `hotels_roomtype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels_roomimage`
--

LOCK TABLES `hotels_roomimage` WRITE;
/*!40000 ALTER TABLE `hotels_roomimage` DISABLE KEYS */;
INSERT INTO `hotels_roomimage` VALUES (1,'room_photos/download_7.jpg','2026-04-01 17:14:15.454557',145),(2,'room_photos/download_8.jpg','2026-04-01 17:14:15.465082',145),(3,'room_photos/images.jpg','2026-04-01 17:14:15.472360',145);
/*!40000 ALTER TABLE `hotels_roomimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels_roomtype`
--

DROP TABLE IF EXISTS `hotels_roomtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels_roomtype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `room_type` varchar(20) NOT NULL,
  `price_per_night` int unsigned NOT NULL,
  `max_guest` int unsigned NOT NULL,
  `total_rooms` int unsigned NOT NULL,
  `amenities` json NOT NULL,
  `hotel_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hotels_roomtype_hotel_id_04482498_fk_hotels_hotel_id` (`hotel_id`),
  CONSTRAINT `hotels_roomtype_hotel_id_04482498_fk_hotels_hotel_id` FOREIGN KEY (`hotel_id`) REFERENCES `hotels_hotel` (`id`),
  CONSTRAINT `hotels_roomtype_chk_1` CHECK ((`price_per_night` >= 0)),
  CONSTRAINT `hotels_roomtype_chk_2` CHECK ((`max_guest` >= 0)),
  CONSTRAINT `hotels_roomtype_chk_4` CHECK ((`total_rooms` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=146 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels_roomtype`
--

LOCK TABLES `hotels_roomtype` WRITE;
/*!40000 ALTER TABLE `hotels_roomtype` DISABLE KEYS */;
INSERT INTO `hotels_roomtype` VALUES (121,'DELUXE',3620,2,10,'[]',70,'2026-03-31 07:15:18.283161','','Deluxe Room'),(122,'DELUXE',3407,2,10,'[]',71,'2026-03-31 07:15:18.284743','','Deluxe Room'),(123,'DELUXE',3750,2,10,'[]',72,'2026-03-31 07:15:18.287104','','Deluxe Room'),(124,'DELUXE',4516,2,10,'[]',73,'2026-03-31 07:15:18.290867','','Deluxe Room'),(125,'DELUXE',2952,2,10,'[]',74,'2026-03-31 07:15:18.292865','','Deluxe Room'),(126,'DELUXE',3303,2,10,'[]',75,'2026-03-31 07:15:18.294374','','Deluxe Room'),(127,'DELUXE',2913,2,10,'[]',76,'2026-03-31 07:15:18.296584','','Deluxe Room'),(128,'DELUXE',4870,2,10,'[]',77,'2026-03-31 07:15:18.298158','','Deluxe Room'),(129,'DELUXE',2298,2,10,'[]',78,'2026-03-31 07:15:18.300687','','Deluxe Room'),(130,'DELUXE',4127,2,10,'[]',79,'2026-03-31 07:15:18.301682','','Deluxe Room'),(131,'SUITE',7168,4,3,'[]',71,'2026-03-31 07:17:16.900658','','Suite'),(132,'SUITE',7645,3,2,'[]',76,'2026-03-31 07:17:16.905113','','Suite'),(133,'PREMIUM',5046,3,4,'[]',78,'2026-03-31 07:17:16.905113','','Premium Room'),(134,'ROYAL',10624,3,4,'[]',78,'2026-03-31 07:17:16.909617','','Royal Suite'),(135,'CLUB',3714,2,3,'[]',79,'2026-03-31 07:17:16.912428','','Club Room'),(136,'CLUB',4449,4,3,'[]',77,'2026-03-31 07:17:16.914436','','Club Room'),(137,'EXECUTIVE',6202,3,4,'[]',71,'2026-03-31 07:17:16.916841','','Executive Room'),(138,'EXECUTIVE',6985,4,3,'[]',70,'2026-03-31 07:17:16.919388','','Executive Room'),(139,'EXECUTIVE',5119,4,3,'[]',75,'2026-03-31 07:17:16.919388','','Executive Room'),(140,'LUXURY',5400,4,3,'[\"Air Conditioning\", \"Smart TV\", \"High-speed WiFi\"]',80,'2026-03-31 09:28:43.208267','','Standard City View'),(141,'DELUXE',0,3,1,'[\"Air Conditioning\", \"Smart TV\", \"High-speed WiFi\"]',81,'2026-03-31 10:42:30.327717','','Standard City View'),(142,'DELUXE',4500,3,3,'[\"Air Conditioning\", \"Smart TV\", \"High-speed WiFi\"]',82,'2026-04-01 09:39:34.964111','','Deluxe Balcony Room'),(143,'SUITE',140,4,3,'[\"Air Conditioning\", \"Smart TV\", \"High-speed WiFi\"]',83,'2026-04-01 11:26:46.810137','','Standard Twin Room'),(144,'DELUXE',1420,3,2,'[\"Air Conditioning\", \"Smart TV\", \"High-speed WiFi\"]',84,'2026-04-01 12:06:25.558741','','Standard Garden View'),(145,'SUITE',1450,4,3,'[\"Air Conditioning\", \"Smart TV\", \"High-speed WiFi\"]',85,'2026-04-01 17:14:15.441020','','Standard City View');
/*!40000 ALTER TABLE `hotels_roomtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_hotelcommission`
--

DROP TABLE IF EXISTS `payments_hotelcommission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_hotelcommission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `month` int NOT NULL,
  `year` int NOT NULL,
  `total_bookings` int NOT NULL,
  `total_revenue` decimal(12,2) NOT NULL,
  `commission_percent` int NOT NULL,
  `commission_amount` decimal(12,2) NOT NULL,
  `penalty_amount` decimal(12,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `due_date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `hotel_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_hotelcommission_hotel_id_727c2e32_fk_hotels_hotel_id` (`hotel_id`),
  CONSTRAINT `payments_hotelcommission_hotel_id_727c2e32_fk_hotels_hotel_id` FOREIGN KEY (`hotel_id`) REFERENCES `hotels_hotel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_hotelcommission`
--

LOCK TABLES `payments_hotelcommission` WRITE;
/*!40000 ALTER TABLE `payments_hotelcommission` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_hotelcommission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_review`
--

DROP TABLE IF EXISTS `reviews_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews_review` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` int NOT NULL,
  `comment` longtext NOT NULL,
  `recommend` tinyint(1) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `hotel_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reviews_review_hotel_id_f675fe71_fk_hotels_hotel_id` (`hotel_id`),
  KEY `reviews_review_user_id_875caff2_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `reviews_review_hotel_id_f675fe71_fk_hotels_hotel_id` FOREIGN KEY (`hotel_id`) REFERENCES `hotels_hotel` (`id`),
  CONSTRAINT `reviews_review_user_id_875caff2_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_review`
--

LOCK TABLES `reviews_review` WRITE;
/*!40000 ALTER TABLE `reviews_review` DISABLE KEYS */;
INSERT INTO `reviews_review` VALUES (6,5,'zx. \r\n',1,'active','2026-03-31 08:17:30.942759',71,3),(7,5,'zx. \r\n',1,'active','2026-03-31 08:17:31.171826',71,3),(8,3,'faltu hei',0,'active','2026-03-31 09:50:50.762284',71,3),(9,4,'nhfxghjgkuchjgkjvhk',1,'active','2026-04-01 09:28:16.901416',71,3);
/*!40000 ALTER TABLE `reviews_review` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-02 10:52:16
