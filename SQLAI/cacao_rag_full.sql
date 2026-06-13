-- 1. Nettoyage de l'ancienne structure si elle existe
DROP TABLE IF EXISTS dbo.BoissonsBienEtre;
GO

-- 2. Création de la table simplifiée pour ton catalogue
CREATE TABLE dbo.BoissonsBienEtre (
    BoissonID INT IDENTITY(1,1) PRIMARY KEY,
    Nom NVARCHAR(150) NOT NULL,
    Type NVARCHAR(100) NOT NULL, -- Cacao, Infusion, Thé Vert, Matcha...
    Description NVARCHAR(MAX) NOT NULL,
    VectorText NVARCHAR(MAX) NULL -- Stockage du vecteur généré par Ollama sous format JSON
);
GO

-- 3. Insertion de ton jeu de données de départ
INSERT INTO dbo.BoissonsBienEtre (Nom, Type, Description, VectorText) VALUES
(N'Aurore Énergisante', N'Cacao', N'Alternative douce au café pour le matin. Stimule la concentration et réveille le corps en douceur pour un rituel sans stress.', NULL),
(N'Sérénité du Soir', N'Infusion', N'Cacao extra-fin aux notes florales et de vanille. Aide à relâcher l''anxiété et prépare à un sommeil profond.', NULL),
(N'Matcha Focus Ultra', N'Thé Vert', N'Thé vert moulu idéal pour une concentration prolongée l''après-midi sans le pic de stress du café. Riche en antioxydants.', NULL);
GO

-- 4. Une petite requête pour vérifier que tes boissons sont bien là
SELECT * FROM dbo.BoissonsBienEtre;
GO