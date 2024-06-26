-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mer. 26 juin 2024 à 10:03
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
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `dive`
--

INSERT INTO `dive` (`id`, `dive_mins`, `dive_secs`, `dive_depth`, `dive_date`, `rating`) VALUES
(1, 12, 30, 58, '2024-02-18', 5),
(2, 22, 24, 64, '2024-05-12', 2),
(3, 54, 41, 77, '2024-05-22', 3),
(4, 41, 42, 97, '2024-06-02', 1),
(5, 2, 34, 43, '2024-06-19', 4),
(6, 70, 40, 80, '2024-06-22', 5);

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
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `diver`
--

INSERT INTO `diver` (`id`, `username`, `password`) VALUES
(1, 'Jason_Momoa', 'Aquaman_du77!'),
(2, 'Jason_Derulo', 'TrumpetBoy93'),
(3, 'TestUser', 'lala');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
