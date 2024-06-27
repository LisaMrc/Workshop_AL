-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 27 juin 2024 à 20:57
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
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `dive`
--

INSERT INTO `dive` (`id`, `dive_mins`, `dive_secs`, `dive_depth`, `dive_date`, `rating`, `diver_id`, `place_id`, `fish_id`) VALUES
(10, 35, 20, 15, '2024-06-27', 4, 1, 1, 1),
(9, 100, 30, 75, '2024-06-05', 3, 1, 1, 1),
(11, 30, 20, 9, '2024-06-03', 4, 1, 1, 1),
(12, 20, 10, 5, '2024-06-14', 0, 3, 0, 0),
(16, 2, 4, 0, '2024-06-17', 4, 3, 5, 0),
(17, 22, 22, 22, '2024-06-22', 2, 3, 3, 0);

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
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `diver`
--

INSERT INTO `diver` (`id`, `username`, `password`) VALUES
(1, 'Jason_Momoa', 'Aquaman_du77!'),
(2, 'Jason_Derulo', 'TrumpetBoy93'),
(3, 'TestUser', 'lala'),
(4, 'TestUser2', 'Hello'),
(5, 'Chris_Martins', 'lolelo');

-- --------------------------------------------------------

--
-- Structure de la table `fish`
--

DROP TABLE IF EXISTS `fish`;
CREATE TABLE IF NOT EXISTS `fish` (
  `id` int NOT NULL AUTO_INCREMENT,
  `common_name` varchar(20) NOT NULL,
  `scientific_name` varchar(20) NOT NULL,
  `family` varchar(20) NOT NULL,
  `average_size` float NOT NULL,
  `img` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `fish`
--

INSERT INTO `fish` (`id`, `common_name`, `scientific_name`, `family`, `average_size`, `img`) VALUES
(1, 'Clownfish', 'Amphiprioninae', 'Pomacentridae', 0.1, 'clownfish.jpg'),
(2, 'Blue Tang', 'Paracanthurus hepatu', 'Acanthuridae', 0.3, 'blue-tang.jpg'),
(3, 'Mandarinfish', 'Synchiropus splendid', 'Callionymidae', 0.08, 'mandarinfish.jpg'),
(4, 'Lionfish', 'Pterois', 'Scorpaenidae', 0.4, 'lionfish.jpg'),
(5, 'Moorish Idol', 'Zanclus cornutus', 'Zanclidae', 0.2, 'moorish-idol.jpg'),
(6, 'Butterflyfish', 'Chaetodontidae', 'Chaetodontidae', 0.2, 'butterflyfish.jpg'),
(7, 'Angelfish', 'Pomacanthidae', 'Pomacanthidae', 0.4, 'angelfish.jpg'),
(8, 'Damselfish', 'Pomacentridae', 'Pomacentridae', 0.1, 'damselfish.jpg'),
(9, 'Wrasse', 'Labridae', 'Labridae', 0.2, 'wrasse.jpg'),
(10, 'Triggerfish', 'Balistidae', 'Balistidae', 0.5, 'triggerfish.jpg'),
(11, 'Hawkfish', 'Cirrhitidae', 'Cirrhitidae', 0.3, 'hawkfish.jpg'),
(12, 'Boxfish', 'Ostraciidae', 'Ostraciidae', 0.4, 'boxfish.jpg'),
(13, 'Cardinalfish', 'Apogonidae', 'Apogonidae', 0.1, 'cardinalfish.jpg'),
(14, 'Anthias', 'Anthiadinae', 'Serranidae', 0.15, 'anthias.jpg'),
(15, 'Surgeonfish', 'Acanthuridae', 'Acanthuridae', 0.3, 'surgeonfish.jpg'),
(16, 'Fairy Basslet', 'Gramma loreto', 'Grammatidae', 0.1, 'fairy-basslet.jpg'),
(17, 'Filefish', 'Monacanthidae', 'Monacanthidae', 0.5, 'filefish.jpg'),
(18, 'Yellow Tang', 'Zebrasoma flavescens', 'Acanthuridae', 0.2, 'yellow-tang.jpg');

-- --------------------------------------------------------

--
-- Structure de la table `place`
--

DROP TABLE IF EXISTS `place`;
CREATE TABLE IF NOT EXISTS `place` (
  `place_id` int NOT NULL AUTO_INCREMENT,
  `country` varchar(14) NOT NULL,
  `place_name` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` varchar(14) NOT NULL,
  PRIMARY KEY (`place_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `place`
--

INSERT INTO `place` (`place_id`, `country`, `place_name`, `type`) VALUES
(1, 'Australia', 'Great Barrier Reef', 'Sea'),
(2, 'Belize', 'Belize Barrier Reef', 'Sea'),
(3, 'Maldives', 'Indian Ocean', 'Ocean'),
(4, 'Malawi', 'Lake Malawi', 'Lake'),
(5, 'USA', 'Crystal River', 'River');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
