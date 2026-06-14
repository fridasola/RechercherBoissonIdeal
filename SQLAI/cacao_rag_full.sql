-- Création de la table
CREATE TABLE IF NOT EXISTS BoissonsBienEtre (
    BoissonID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom TEXT NOT NULL,
    Type TEXT NOT NULL,
    Description TEXT NOT NULL,
    VectorText TEXT NULL
);

-- Insertion du catalogue de départ
INSERT INTO BoissonsBienEtre (Nom, Type, Description, VectorText) VALUES
('Aurore Énergisante', 'Cacao', 'Alternative douce au café pour le matin. Stimule la concentration et réveille le corps en douceur pour un rituel sans stress.', NULL),
('Sérénité du Soir', 'Infusion', 'Cacao extra-fin aux notes florales et de vanille. Aide à relâcher l''anxiété et prépare à un sommeil profond.', NULL),
('Matcha Focus Ultra', 'Thé Vert', 'Thé vert moulu idéal pour une concentration prolongée l''après-midi sans le pic de stress du café. Riche en antioxydants.', NULL),
('Élixir Baies de Goji & Hibiscus', 'Infusion Fruitée', 'Une boisson profondément acidulée et rafraîchissante, véritable cocktail antioxydant grâce aux baies de goji et aux fleurs d''hibiscus.', NULL);

INSERT INTO BoissonsBienEtre (Nom, Type, Description, VectorText) VALUES
('Latté Adaptogène au Reishi', 'Café Bien-Être', 'Substitut de café crémeux au cacao et champignon Reishi. Régule le système nerveux et apporte une clarté mentale stable sans l''excitation de la caféine.', NULL),
('Infusion Détox Menthe & Chardon-Marie', 'Tisane Digestive', 'Infusion rafraîchissante de menthe, chardon-marie et gingembre. Idéale après un repas pour stimuler la digestion et purifier l''organisme.', NULL),
('Limonade Noire au Charbon Actif', 'Élixir Détox', 'Boisson au jus de citron et charbon végétal actif. Conçue pour piéger les toxines et nettoyer le système digestif pour retrouver de la légèreté.', NULL);
