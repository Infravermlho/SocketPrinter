from ursina import *
import random
from Recursos.Scripts.SaveManager import SaveManager

window.borderless = False
app = Ursina()


# Cubo class
class Cubo(Entity):
    def __init__(self, position=(0, 0, 0), texture='Recursos/textures/blue_wool', destructible=True):
        super().__init__(
            model='cube',
            texture=texture,
            collider='box',
            origin_y=.5,
            position=position,
            color=color.white,
            scale=(2, 2, 2),
            destructible=destructible,
        )


###################
# HUD
class Hud(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='quad',
            scale=(.7, .2),
            origin=window.bottom_right,
            position=(0, .4),
            texture='Recursos/textures/barrel_side',
            texture_scale=(5, 2),
            color=color.gray,
        )
        self.selectedtexture = 'Recursos/textures/blue_wool'

        self.buttons = []
        self.buttons.append(TextureButton('Recursos/textures/blue_wool', (-1, .60)))
        self.buttons.append(TextureButton('Recursos/textures/green_wool', (-3, .60)))
        self.buttons.append(TextureButton('Recursos/textures/brown_wool', (-5, .60)))
        self.buttons.append(TextureButton('Recursos/textures/gray_wool', (-7, .60)))


class TextureButton(Button):
    def __init__(self, texture, pos=(0, 0, 0)):
        super().__init__(
            color=color.azure,
            icon=texture,
            scale=.08,
            origin=pos,
            position=window.top_left,
            pressed_scale=.9,
            on_click=self.swaptexture
        )
        self.textureheld = texture

    def swaptexture(self):
        hud.selectedtexture = self.textureheld
        click.play()


####################
# Baseplate generation
for z in range(4):
    for x in range(4):
        Cubo(position=(x * 2, 0, z * 2), texture='Recursos/textures/bedrock', destructible=False)


#####################
# Game tick updates
def update():
    if mouse.hovered_entity:
        if isinstance(mouse.hovered_entity, Cubo):
            selectionCursor.enable()
            selectionCursor.position = mouse.hovered_entity.position
    else:
        selectionCursor.disable()


def input(key):
    if mouse.hovered_entity:
        target = mouse.hovered_entity
        if isinstance(target, Cubo):
            if key == 'right mouse down':
                newpos = target.position + (mouse.normal * 2)
                xy = (newpos[0], newpos[2])
                if all((-0 <= z <= 6) for z in xy) and 2 <= newpos[1] <= 8:
                    blockregistry.append(Cubo(position=newpos, texture=hud.selectedtexture))
                    placeSound[random.randrange(3)].play()

            elif key == 'left mouse down':
                if target.destructible:
                    blockregistry.remove(target)
                    destroy(target)
                    placeSound[random.randrange(3)].play()


#########################
# Random functions

def clearactiveblocks():
    click.play()
    for i in blockregistry:
        destroy(i)
    blockregistry.clear()  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< LEMBRAR

def SalvarBlocos():
    click.play()
    Saving.save(blockregistry)

def Imprimir():
    weeumm.play()
    Saving.transfer(blockregistry)
    mmueew.play()


#########################

if __name__ == '__main__':
    Sky(texture='Recursos/textures/skybox')
    window.borderless = False
    window.exit_button.visible = False

    camera.rotation.y = 90
    EditorCamera(rotation=(30, 15, 0))

    hud = Hud()
    Saving = SaveManager()
    blockregistry = []

    selectionCursor = Entity(model='cube', color=color.rgba(0, 0, 0, 128), scale=(2.05, 2.05, 2.05), origin_y=.49)
    ambient = Audio('Recursos/Som/menu4', pitch=1, loop=True, autoplay=True)

    placeSound = [Audio('Recursos/Som/cloth1', pitch=1, loop=False, autoplay=False),
                  Audio('Recursos/Som/cloth2', pitch=1, loop=False, autoplay=False),
                  Audio('Recursos/Som/cloth3', pitch=1, loop=False, autoplay=False),
                  Audio('Recursos/Som/cloth1', pitch=1, loop=False, autoplay=False)]

    click = Audio('Recursos/Som/click', pitch=1, loop=False, autoplay=False)
    weeumm = Audio('Recursos/Som/trigger', pitch=1, loop=False, autoplay=False)
    mmueew = Audio('Recursos/Som/travel', pitch=1, loop=False, autoplay=False)

    debug = Button(color=color.white, texture='Recursos/textures/barrel_side', icon='Recursos/textures/writable_book',
                   scale=.1, on_click=SalvarBlocos, position=(window.top_right[0] - .08, window.top_right[1] - .08),
                   tooltip=Tooltip('Salvar'))

    debug2 = Button(color=color.white, texture='Recursos/textures/barrel_side', icon='Recursos/textures/written_book',
                   scale=.1, on_click=Imprimir, position=(window.top_right[0] - .08, window.top_right[1] - .2),
                   tooltip=Tooltip('Imprimir'))

    debug3 = Button(color=color.white, texture='Recursos/textures/barrel_side', icon='brick',
                   scale=.1, on_click=clearactiveblocks, position=(window.top_right[0] - .08, window.top_right[1] - .32),
                   tooltip=Tooltip('Apagar'))

    app.run()
