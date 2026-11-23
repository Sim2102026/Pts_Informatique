"""Un parcours original de 160 colonnes (8 écrans de 20 cases).

Inspiré du rythme de SMB 1-1 : départ sûr, obstacles bas, fossés,
plateformes optionnelles, escaliers, arrivée. Les images restent celles du groupe.
X : terrain, P : départ, E : ennemi, F : fruit, D : arrivée, H : soin.
"""


def creer_carte():
    largeur, hauteur = 160, 13
    grille = [["."] * largeur for _ in range(hauteur)]
    grille[12] = ["X"] * largeur

    # Fossés de 2 ou 3 cases, compatibles avec le saut actuel.
    for debut, fin in [(32, 35), (62, 64), (92, 95), (132, 135)]:
        for x in range(debut, fin):
            grille[12][x] = "."

    # Obstacles bas, puis doubles : pas de saut de quatre cases imposé.
    for x, largeur_bloc, h in [(18, 2, 1), (25, 2, 2), (48, 2, 2),
                               (77, 2, 1), (85, 2, 2), (112, 2, 2)]:
        for col in range(x, x + largeur_bloc):
            for ligne in range(12 - h, 12):
                grille[ligne][col] = "X"

    # Plateformes hautes optionnelles et fruits qui indiquent une autre route.
    for debut, fin in [(8, 13), (39, 44), (69, 74), (100, 105)]:
        for x in range(debut, fin):
            grille[8][x] = "X"
        for x in range(debut + 1, fin, 2):
            grille[7][x] = "F"
        # Petite marche pour accéder à la plateforme.
        grille[10][debut - 2] = "X"
        grille[10][debut - 1] = "X"

    # Escalier d'entraînement, puis escalier final avec descente progressive.
    for debut in [120, 142]:
        for i, h in enumerate([1, 2, 3, 3, 2, 1]):
            for ligne in range(12 - h, 12):
                grille[ligne][debut + i] = "X"

    grille[11][1] = "P"
    for x in [6, 15, 22, 37, 46, 56, 67, 80, 98, 108, 117, 138, 151]:
        grille[11][x] = "F"
    for x in [16, 42, 57, 72, 82, 103, 116, 137]:
        # Les ennemis sur les plateformes sont posés dessus.
        ligne = 7 if x in [42, 72, 103] else 11
        grille[ligne][x] = "E"
    for x in [29, 60, 89, 118, 139]:
        grille[11][x] = "H"
    grille[11][156] = "T"  # Porte vers la salle du boss (Haut pour entrer).
    return ["".join(ligne) for ligne in grille]


CARTE_LONGUE = creer_carte()
