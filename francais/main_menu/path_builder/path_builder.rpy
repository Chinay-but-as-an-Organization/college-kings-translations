init python:
    class PathBuilderCatagories(Enum):
        START_LOCATION = {
            1: "Pick your starting location (Act 1 Start skips steps 3-5)",
            "background": "main_menu/path_builder/images/path_builder_step_1.webp"
        }
        KCT = {
            2: "Pick your starting KCT",
            "background": "main_menu/path_builder/images/path_builder_step_2.webp"
        }
        FRATERNITY = {
            3: "Pick a fraternity",
            "background": "main_menu/path_builder/images/path_builder_step_3.webp"
        }
        GIRL = {
            4: "Pick which girls you want to be romantically involved with",
            "background": "main_menu/path_builder/images/path_builder_step_4.webp"
        }
        HOMECOMING_DATE = {
            5: "Pick your homecoming date",
            "background": "main_menu/path_builder/images/path_builder_step_5.webp"
        }

    class PathBuilderItem:
        items = []

        def __init__(self, catagory, name, actions=None):
            self.catagory = catagory
            self.name = name

            if actions is None: self.actions = []
            elif isinstance(actions, list): self.actions = actions
            else: self.actions = [actions]

            PathBuilderItem.items.append(self)


    class PathBuilderGirl(PathBuilderItem):
        def __init__(self, catagory, name, kct, actions, frat_requirement=None, act_requirement=2):
            PathBuilderItem.__init__(self, catagory, name, actions)

            self.kct = kct
            self.frat_requirement = frat_requirement
            self.act_requirement = act_requirement


    def get_catagory(step):
        for catagory in PathBuilderCatagories:
            if step in catagory.value:
                return catagory
        return None


screen path_builder_alert():
    modal True
    style_prefix "path_builder_alert"

    default image_path = "main_menu/path_builder/images/"

    add "darker_80"

    add image_path + "alert_background.webp" align (0.5, 0.5)

    fixed:
        xysize (742, 356)
        pos (587, 364)

        text "LE CRÉATEUR DE VOIES CONTIENT DES SPOILERS DE L'HISTOIRE\nDU JEU. ÊTES-VOUS SÛR DE VOULOIR CONTINUER ?\nVOUS N'OBTENEZ AUCUN SUCCÈS DANS CE MODE.":
            xsize 572
            xalign 0.5
            ypos 66


        hbox:
            pos (217, 258)
            spacing 5

            fixed:
                xysize (132, 61)

                imagebutton:
                    idle "path_builder_button_idle"
                    hover "path_builder_button_hover"
                    action [Hide("path_builder_alert"), Show("path_builder")]
                text "OUI" align (0.5, 0.5)

            fixed:
                xysize (132, 61)

                imagebutton:
                    idle "path_builder_button_idle"
                    hover "path_builder_button_hover"
                    action Hide("path_builder_alert")
                text "NON" align (0.5, 0.5)


style path_builder_alert_text is bebas_neue_30

screen path_builder():
    tag menu
    modal True

    default image_path = "main_menu/path_builder/images/"
    default grid_size = { # item_count : (rows, cols)
        2: (2, 1),
        3: (3, 1),
        4: (4, 1),
        6: (4, 2),
        11: (4, 3),
        12: (4, 3),
    }

    default catagory_step = 1
    default start_label = "start"
    default act_number = 1

    $ catagory = get_catagory(catagory_step)
    $ items = [item for item in PathBuilderItem.items if item.catagory == catagory]
    $ heading = catagory.value[catagory_step]

    $ cols, rows = grid_size[len(items)]

    add image_path + "path_builder_background.webp"
    add image_path + "path_builder_box_background.webp" align (0.5, 0.5)

    vbox:
        align (0.95,0.05)

        imagebutton:
            idle image_path + "button_idle.webp"
            hover image_path + "button_hover.webp"
            selected_idle image_path + "button_hover.webp"
            action ShowMenu("path_builder_advanced_settings")

        text "Avancé":
            align (0.5, 0.5)
            yoffset -50
            color "#FFF"

    imagebutton:
        idle "gui/common/return_idle.webp"
        hover "gui/common/return_hover.webp"
        action ShowMenu("main_menu")
        align (0.015, 0.015)

    vbox:
        align (0.5, 0.215)

        add catagory.value["background"]

    vbox:
        spacing 20
        align (0.5, 0.5)

        text heading xalign 0.5

        vpgrid:
            cols cols
            rows rows
            xspacing 10
            xalign 0.5
            yoffset 40

            for item in items:
                if catagory == PathBuilderCatagories.GIRL or catagory == PathBuilderCatagories.HOMECOMING_DATE:
                    button:
                        idle_background image_path + "girls/{}_idle.webp".format(item.name)
                        hover_background image_path + "girls/{}.webp".format(item.name)
                        selected_idle_background image_path + "girls/{}.webp".format(item.name)
                        insensitive_background Transform(image_path + "girls/{}_idle.webp".format(item.name), matrixcolor=SaturationMatrix(0))
                        selected all([a.get_selected() for a in item.actions])
                        if isinstance(item, PathBuilderGirl):
                            sensitive ((item.frat_requirement is None or item.frat_requirement.value == int(joinwolves)) and (item.act_requirement <= act_number))
                        action item.actions
                        xysize (307, 112)

                        vbox:
                            xpos 120
                            yalign 0.5

                            text item.name:
                                size 30
                                color "#FFF"

                            if isinstance(item, PathBuilderGirl) and pb_kct_shown:
                                text item.kct: # This could show the kct for each girl
                                    size 15
                                    color "#FFD166"



                elif catagory == PathBuilderCatagories.START_LOCATION:
                    vbox:
                        xalign 0.5

                        default start_image_path = image_path + "starts/"

                        imagebutton:
                            idle Transform(start_image_path + item.name +".webp", zoom=.8)
                            selected all([a.get_selected() for a in item.actions])
                            action [a for a in item.actions]
                            xalign 0.5

                        imagebutton:
                            idle image_path + "button_idle_dark.webp"
                            hover image_path + "button_hover.webp"
                            selected_idle image_path + "button_hover.webp"
                            selected all([a.get_selected() for a in item.actions])
                            action [a for a in item.actions]
                            xalign 0.5
                            yoffset -35

                        text item.name:
                            align (0.5, 0.5)
                            yoffset -87
                            size 30
                            color "#FFF"

                else:
                    vbox:
                        xalign 0.5

                        imagebutton:
                            idle image_path + "button_idle.webp"
                            hover image_path + "button_hover.webp"
                            selected_idle image_path + "button_hover.webp"
                            selected all([a.get_selected() for a in item.actions])
                            action [a for a in item.actions]

                        text item.name:
                            align (0.5, 0.5)
                            yoffset -50
                            color "#FFF"

        # Option to lock KCT
        if catagory == PathBuilderCatagories.KCT:
            hbox:
                spacing 20
                yoffset 40

                imagebutton:
                    idle image_path + "pb_tick.webp"
                    hover image_path + "pb_ticked.webp"
                    selected_idle image_path + "pb_ticked.webp"
                    action ToggleVariable("locked_kct")

                text "Verrouiller le KCT (l'empêcher de changer)":
                    yoffset -7

        elif catagory == PathBuilderCatagories.START_LOCATION and not config.enable_steam:
            button:
                idle_background image_path + "button_idle.webp"
                hover_background image_path + "button_hover.webp"
                selected_idle_background image_path + "button_hover.webp"
                selected False
                action [
                    SetScreenVariable("start_label", "v{}_start".format(config.version.split(' ')[0].split('.')[0])),
                    SetScreenVariable("catagory_step", catagory_step + 1),
                    SetScreenVariable("act_number", int(config.version.split(' ')[0].split('.')[0]))
                    ]
                xysize (270, 61)
                xalign 0.5

                text "Dernière mise à jour" align (0.5, 0.5)

    hbox:
        spacing 50
        align (0.5, 0.9)

        default button_img_path = "main_menu/path_builder/images/"

        if catagory_step > 1:

            imagebutton:
                idle button_img_path + "back.webp"
                action SetScreenVariable("catagory_step", catagory_step - 1)
        else:
            imagebutton:
                idle button_img_path + "back_blocked.webp"
                action ShowMenu("main_menu")


        imagebutton:
            idle button_img_path + "continue.webp"

            if catagory_step >= len(PathBuilderCatagories):
                action [Function(setup), Start(start_label)]
            else:
                action SetScreenVariable("catagory_step", catagory_step + 1)


screen path_builder_advanced_settings():
    zorder 100
    modal True

    default image_path = "main_menu/path_builder/images/"

    add image_path + "path_builder_background.webp"

    text "Paramètres avancés" align (0.5, 0.15)

    imagebutton:
        idle "gui/common/return_idle.webp"
        hover "gui/common/return_hover.webp"
        action Hide("path_builder_advanced_settings")
        align (0.015, 0.015)


    hbox:
        align (0.5, 0.5)
        spacing 100
        vbox:
            spacing 20

            text "Extras" color "#FFD166" size 50

            if renpy.loadable("v10/scene1.rpy"):
                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        action ToggleVariable("emily_europe")

                    text "Invitez Emily en Europe":
                        yoffset -7

            if renpy.loadable("v11/scene1.rpy"):
                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        action ToggleVariable("v11s1_courtpoints", 100, 0)

                    text "Gagnez le procès de Pénélope":
                        yoffset -7

            if renpy.loadable("v14/scene1.rpy"):
                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        action ToggleVariable("v14_help_chloe")

                    text "Aidez Chloé dans sa campagne":
                        yoffset -7

                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        action ToggleVariable("v14_help_lindsey")

                    text "Aidez Lindsey dans sa campagne":
                        yoffset -7

                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        action ToggleVariable("v14_SamanthaDrugs", False, True)

                    text "Encouragez Sam à être clean":
                        yoffset -7

                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        action ToggleVariable("v14_amber_clean")

                    text "Encouragez Amber à être clean":
                        yoffset -7

                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        action ToggleVariable("v14_emily_ily")

                    text "Dites à Emily que vous l'aimez":
                        yoffset -7

                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        action ToggleVariable("AutumnTrust")

                    text "Autumn a confiance en vous":
                        yoffset -7

                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        selected "v14_threesome" in sceneList
                        if "v14_threesome" in sceneList:
                            action RemoveFromSet(sceneList, "v14_threesome")
                        else:
                            action AddToSet(sceneList, "v14_threesome")

                    text "Avoir un plan à trois avec Riley et Aubrey":
                        yoffset -7

                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        action ToggleField(lauren, "relationship", Relationship.KISS, Relationship.FRIEND)

                    text "A embrassé Lauren":
                        yoffset -7

        vbox:
            spacing 20

            text "Modifications de la jouabilité" color "#FFD166" size 50

            if renpy.loadable("v14/scene1.rpy"):
                hbox:
                    spacing 20

                    imagebutton:
                        idle image_path + "pb_tick.webp"
                        hover image_path + "pb_ticked.webp"
                        selected_idle image_path + "pb_ticked.webp"
                        action [ToggleVariable("lindsey_board.money", 10000, 200), ToggleVariable("chloe_board.money", 10000, 1500)]

                    text "Budget illimité pour la campagne présidentielle":
                        yoffset -7

            hbox:
                spacing 20

                imagebutton:
                    idle image_path + "pb_tick.webp"
                    hover image_path + "pb_ticked.webp"
                    selected_idle image_path + "pb_ticked.webp"
                    action ToggleVariable("pb_kct_shown")

                text "Montrer quel est le KCT préféré de chaque fille":
                    yoffset -7

            hbox:
                spacing 20

                imagebutton:
                    idle image_path + "pb_tick.webp"
                    hover image_path + "pb_ticked.webp"
                    selected_idle image_path + "pb_ticked.webp"
                    action ToggleVariable("pb_kct_notification")

                text "Afficher une notification chaque fois que vous gagnez des points KCT":
                    yoffset -7


style path_builder_advanced_settings_text is bebas_neue_30
