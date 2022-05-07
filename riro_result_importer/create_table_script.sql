CREATE TABLE `2022_Flugsaison_Hirschi` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `taubennr` varchar(255) NOT NULL,
  `mmin` varchar(255) NOT NULL,
  `prs_fg` varchar(255) DEFAULT NULL,
  `prs_rv` varchar(255) DEFAULT NULL,
  `aspkt_fg` varchar(255) DEFAULT NULL,
  `aspkt_rv` varchar(255) DEFAULT NULL,
  `insert_dttm` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `km` varchar(255) NOT NULL,
  `prs` varchar(255) NOT NULL,
  `auflassort` varchar(255) NOT NULL,
  `prs_zt` varchar(255) NOT NULL,
  `flugnummer` varchar(255) NOT NULL,
  `prs_tb` varchar(255) DEFAULT NULL,
  `flugdatum` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=693 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;