label labyrinthe:
    "test"
    # Cacher la barre de texte
    window hide
    
    # Initialisation des positions de l'image en pourcentage de la largeur et hauteur de l'écran
    if not hasattr(store, 'xpos'):
        $ xpos = 0.43
        $ ypos = 0.9

    # Taille de l'écran en pixels
    $ screen_width = 1920
    $ screen_height = 1000

    # Définition des blocs de labyrinthe (lab_block) et leur position
    $ lab_blocks = [
        (650, 650),  # Position du premier lab_block
        (850, 650),  # Position du second lab_block
        # Ajoutez d'autres positions selon votre labyrinthe
    ]

    # Taille d'un lab_block en pourcentage de l'écran
    $ lab_block_width = 225 / screen_width
    $ lab_block_height = 225 / screen_height
    
    # Construction de la liste des hotspots (zones de collision)
    $ hotspots = [(x / screen_width, y / screen_height, lab_block_width, lab_block_height) for (x, y) in lab_blocks]

    # Initialiser les variables `show_cover` et `show_position` si elles ne le sont pas déjà
    if not hasattr(store, 'show_cover'):
        $ show_cover = False
    if not hasattr(store, 'show_position'):
        $ show_position = True

    # Fonction pour vérifier si la nouvelle position est dans un hotspot (zone de collision)
    python:
        def is_in_hotspot(new_x_percent, new_y_percent):
            player_width = 0.05  # Largeur du joueur en pourcentage de l'écran
            player_height = 0.05  # Hauteur du joueur en pourcentage de l'écran
            
            for (x1, y1, width, height) in hotspots:
                x2 = x1 + width
                y2 = y1 + height

                # Vérifier si le joueur entrerait en collision avec un bloc
                if (new_x_percent + player_width > x1 and new_x_percent < x2 and
                    new_y_percent + player_height > y1 and new_y_percent < y2):
                    print(f"Collision detected: {new_x_percent}, {new_y_percent} with block at ({x1}, {y1})")
                    return True
            print(f"No collision at: {new_x_percent}, {new_y_percent}")
            return False

        def move_player(direction):
            new_x_percent = xpos
            new_y_percent = ypos

            if direction == "right":
                new_x_percent += 0.01
            elif direction == "left":
                new_x_percent -= 0.01
            elif direction == "down":
                new_y_percent += 0.01
            elif direction == "up":
                new_y_percent -= 0.01

            # Vérifier la collision
            if not is_in_hotspot(new_x_percent, new_y_percent):
                print(f"Moving player to: {new_x_percent}, {new_y_percent}")
                renpy.store.xpos = new_x_percent
                renpy.store.ypos = new_y_percent
            else:
                print("Movement blocked by collision.")

        # Fonction pour centrer la vue sur le joueur
        def center_view_on_player():
            center_x = int(renpy.store.xpos * screen_width) - (screen_width // 2)
            center_y = int(renpy.store.ypos * screen_height) - (screen_height // 2)
            renpy.call_in_new_context("labyrinthe_screen", center_x=center_x, center_y=center_y)

    # Initialisation des variables pour centrer la vue
    if not hasattr(store, 'center_x'):
        $ center_x = int(xpos * screen_width) - (screen_width // 2)
    if not hasattr(store, 'center_y'):
        $ center_y = int(ypos * screen_height) - (screen_height // 2)

    # Écran pour afficher l'image de fond et la position du joueur
    screen labyrinthe_screen(center_x=center_x, center_y=center_y):
        if show_cover:
            add "images/labyrinthe_cover.png"  # Affiche la couverture si activé
            textbutton "Fermer la carte" action [SetVariable("show_cover", False), SetVariable("show_position", True)] xpos 10 ypos 50
        else:
            if show_position:
                # Utilisation du viewport pour permettre le défilement
                viewport id "viewport":
                    draggable True
                    mousewheel True
                    xinitial center_x
                    yinitial center_y
                    xmaximum screen_width
                    ymaximum screen_height

                    # Ajouter tous les blocs de labyrinthe (lab_block) selon leur position
                    for (x, y) in lab_blocks:
                        add "images/lab_block.png" xpos (x / screen_width) ypos (y / screen_height)

                    add "images/shawn_pixel.png" pos (xpos, ypos) at petit  # Position du joueur

                    scrollbars "both"  # Activer les barres de défilement horizontales et verticales

            textbutton "Afficher la carte" action [SetVariable("show_cover", True), SetVariable("show_position", False), Jump("afficher_carte")] xpos 10 ypos 10
            textbutton "Sortie" action Return() xpos 10 ypos 100  # Bouton pour quitter le labyrinthe
            textbutton "Centrer sur le joueur" action Function(center_view_on_player) xpos 10 ypos 150  # Bouton pour centrer sur le joueur

    # Écran de gestion des touches pour le déplacement du joueur
    screen position_labyrinthe():
        key "K_d" action Function(move_player, "right")
        key "K_q" action Function(move_player, "left")
        key "K_s" action Function(move_player, "down")
        key "K_z" action Function(move_player, "up")
        key "K_ESCAPE" action Return()
        imagebutton:
            xpos 1200
            ypos 750
            idle "arrow_top_idle.png"
            hover "arrow_top_hover.png"
            at petit
            action Function(move_player, "up")
        imagebutton:
            xpos 1200
            ypos 850
            idle "arrow_bot_idle.png"
            hover "arrow_bot_hover.png"
            at petit
            action Function(move_player, "down")
        imagebutton:
            xpos 1250
            ypos 800
            idle "arrow_left_idle.png"
            hover "arrow_left_droite_hover.png"
            at petit
            action Function(move_player, "right")
        imagebutton:
            xpos 1150
            ypos 800
            idle "arrow_right_idle.png"
            hover "arrow_right_hover.png"
            at petit
            action Function(move_player, "left")

    # Afficher les écrans
    show screen labyrinthe_screen(center_x=center_x, center_y=center_y)
    show screen position_labyrinthe

    $ renpy.pause(0.05)

    # Répéter l'écran pour capturer continuellement les touches
    jump labyrinthe

label afficher_carte:
    # Attend que l'utilisateur ferme la carte manuellement
    
    $ renpy.pause()
    return

label labyrinthe_screen:
    show screen labyrinthe_screen(center_x=center_x, center_y=center_y)