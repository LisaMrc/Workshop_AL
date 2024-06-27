-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 27 juin 2024 à 12:42
-- Version du serveur : 8.3.0
-- Version de PHP : 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `diverdb`
--

-- --------------------------------------------------------

--
-- Structure de la table `dive`
--

DROP TABLE IF EXISTS `dive`;
CREATE TABLE IF NOT EXISTS `dive` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dive_mins` int DEFAULT NULL,
  `dive_secs` int DEFAULT NULL,
  `dive_depth` int DEFAULT NULL,
  `dive_date` date DEFAULT NULL,
  `rating` int NOT NULL DEFAULT '1',
  `diver_id` int NOT NULL,
  `place_id` int NOT NULL,
  `fish_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `diver_id` (`diver_id`),
  KEY `place_id` (`place_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `dive`
--

INSERT INTO `dive` (`id`, `dive_mins`, `dive_secs`, `dive_depth`, `dive_date`, `rating`, `diver_id`, `place_id`, `fish_id`) VALUES
(10, 35, 20, 15, '2024-06-27', 4, 1, 1, 1),
(9, 100, 30, 75, '2024-06-05', 3, 1, 1, 1),
(11, 30, 20, 9, '2024-06-03', 4, 1, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `diver`
--

DROP TABLE IF EXISTS `diver`;
CREATE TABLE IF NOT EXISTS `diver` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(14) NOT NULL,
  `password` varchar(14) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `diver`
--

INSERT INTO `diver` (`id`, `username`, `password`) VALUES
(1, 'Jason_Momoa', 'Aquaman_du77!'),
(2, 'Jason_Derulo', 'TrumpetBoy93'),
(3, 'TestUser', 'lala'),
(4, 'TestUser2', 'Hello');

-- --------------------------------------------------------

--
-- Structure de la table `fish`
--

DROP TABLE IF EXISTS `fish`;
CREATE TABLE IF NOT EXISTS `fish` (
  `id_fish` int DEFAULT NULL,
  `common_name` varchar(20) NOT NULL,
  `scientific_name` varchar(20) NOT NULL,
  `family` varchar(20) NOT NULL,
  `average_size` float NOT NULL,
  `img` varchar(40) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `place`
--

DROP TABLE IF EXISTS `place`;
CREATE TABLE IF NOT EXISTS `place` (
  `place_id` int NOT NULL AUTO_INCREMENT,
  `country` varchar(14) NOT NULL,
  `town` varchar(14) NOT NULL,
  `type` varchar(14) NOT NULL,
  PRIMARY KEY (`place_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `place`
--

INSERT INTO `place` (`place_id`, `country`, `town`, `type`) VALUES
(1, 'Australia', 'Cairns', 'Sea'),
(2, 'Belize', 'San Pedro', 'Sea'),
(3, 'Maldives', 'Maafushi', 'Ocean'),
(4, 'Malawi', 'Monkey Bay', 'Lake'),
(5, 'USA', 'Crystal River', 'River');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
