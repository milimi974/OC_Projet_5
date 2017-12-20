-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u2
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Dim 10 Décembre 2017 à 13:26
-- Version du serveur :  5.5.58-0+deb8u1
-- Version de PHP :  5.6.30-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données :  `c1python`
--

-- --------------------------------------------------------

--
-- Structure de la table `Categories`
--

CREATE TABLE IF NOT EXISTS `Categories` (
`PK_id` int(10) unsigned NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `Foods`
--

CREATE TABLE IF NOT EXISTS `Foods` (
`PK_id` int(10) unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  `uri` varchar(255) NOT NULL,
  `description` text,
  `link` varchar(255) DEFAULT NULL,
  `level` varchar(1) NOT NULL,
  `code` varchar(128) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `Food_has_Categories`
--

CREATE TABLE IF NOT EXISTS `Food_has_Categories` (
  `FK_food_id` int(10) unsigned NOT NULL,
  `FK_categorie_id` int(10) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `Food_has_Shops`
--

CREATE TABLE IF NOT EXISTS `Food_has_Shops` (
  `FK_food_id` int(10) unsigned NOT NULL,
  `FK_shop_id` int(10) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `Shops`
--

CREATE TABLE IF NOT EXISTS `Shops` (
`PK_id` int(10) unsigned NOT NULL,
  `name` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `Users`
--

CREATE TABLE IF NOT EXISTS `Users` (
`PK_id` int(10) unsigned NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `lastname` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `User_has_Foods`
--

CREATE TABLE IF NOT EXISTS `User_has_Foods` (
  `FK_user_id` int(10) unsigned NOT NULL,
  `FK_food_id` int(10) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `Categories`
--
ALTER TABLE `Categories`
 ADD PRIMARY KEY (`PK_id`), ADD UNIQUE KEY `idCategories_UNIQUE` (`PK_id`);

--
-- Index pour la table `Foods`
--
ALTER TABLE `Foods`
 ADD PRIMARY KEY (`PK_id`), ADD UNIQUE KEY `idfoods_UNIQUE` (`PK_id`), ADD UNIQUE KEY `code_UNIQUE` (`code`);

--
-- Index pour la table `Food_has_Categories`
--
ALTER TABLE `Food_has_Categories`
 ADD PRIMARY KEY (`FK_food_id`,`FK_categorie_id`), ADD KEY `fk_Foods_has_Categories_Categories1_idx` (`FK_categorie_id`), ADD KEY `fk_Foods_has_Categories_Foods1_idx` (`FK_food_id`);

--
-- Index pour la table `Food_has_Shops`
--
ALTER TABLE `Food_has_Shops`
 ADD PRIMARY KEY (`FK_food_id`,`FK_shop_id`), ADD KEY `fk_Foods_has_Shops_Shops1_idx` (`FK_shop_id`), ADD KEY `fk_Foods_has_Shops_Foods1_idx` (`FK_food_id`);

--
-- Index pour la table `Shops`
--
ALTER TABLE `Shops`
 ADD PRIMARY KEY (`PK_id`), ADD UNIQUE KEY `idShops_UNIQUE` (`PK_id`);

--
-- Index pour la table `Users`
--
ALTER TABLE `Users`
 ADD PRIMARY KEY (`PK_id`), ADD UNIQUE KEY `idUsers_UNIQUE` (`PK_id`);

--
-- Index pour la table `User_has_Foods`
--
ALTER TABLE `User_has_Foods`
 ADD PRIMARY KEY (`FK_user_id`,`FK_food_id`), ADD KEY `fk_Users_has_Foods_Foods1_idx` (`FK_food_id`), ADD KEY `fk_Users_has_Foods_Users_idx` (`FK_user_id`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `Categories`
--
ALTER TABLE `Categories`
MODIFY `PK_id` int(10) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `Foods`
--
ALTER TABLE `Foods`
MODIFY `PK_id` int(10) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `Shops`
--
ALTER TABLE `Shops`
MODIFY `PK_id` int(10) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `Users`
--
ALTER TABLE `Users`
MODIFY `PK_id` int(10) unsigned NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
