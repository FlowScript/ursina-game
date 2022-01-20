import random
from ursina import *    
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

window.exit_button.visible = False
window.title = "Ursina Game | Flow"

ost = random.randint(0,4)

#assets_texture
dirt = load_texture('assets/texture/dirt.png')
cobblestone = load_texture('assets/texture/cobblestone.png')
planks = load_texture('assets/texture/planks.png')
glass = load_texture('assets/texture/glass.png')
brick = load_texture('assets/texture/brick.png')
diamond = load_texture('assets/texture/diamond.png')
void = load_texture('assets/texture/void.png')
bedrock = load_texture('assets/texture/bedrock.png')
#assets_audio
placeblocksound = Audio('assets/sound/stone1.ogg', loop=False, autoplay=False)
destroyblocksound = Audio('assets/sound/stone2.ogg', loop=False, autoplay=False)
clicksound = Audio('assets/sound/click.ogg', loop=False, autoplay=False)
voidsound = Audio('assets/sound/void.ogg', loop=False, autoplay=False)
tp = Audio('assets/sound/tp.ogg', loop=False, autoplay=False)
osts = [Audio('assets/sound/ost/ost1.ogg', loop=False, autoplay=False), Audio('assets/sound/ost/ost2.ogg', loop=False, autoplay=False), Audio('assets/sound/ost/ost3.ogg', loop=False, autoplay=False), Audio('assets/sound/ost/ost4.ogg', loop=False, autoplay=False), Audio('assets/sound/ost/ost5.ogg', loop=False, autoplay=False)]

osts[ost].play()

block_select = 1
blocksplaced = 0
blocksdestroyed = 0

# ─── FUNCTION ───────────────────────────────────────────────────────────────────

gametext = Text(text="<blue>v:0.0.9 <white>Made By Flow", position=(-0.88, 0.5, 0))
blocksplacedtext = Text(text="Blocks Placed: <green>0", position=(-0.88, -0.42, 0))
blocksdestroyedtext = Text(text="Blocks Destroyed: <red>0", position=(-0.88, -0.47, 0))
blocktext = Text(text="Block: <red>White Block", position=(-0.88, 0.45, 0))

def blockselection(blockselected):
    global block_select
    if blockselected == '1':
        clicksound.play()
        selection.position = Vec2(-0.44,0)
        hand.texture = 'white_cube'
        blocktext.text="Block: <red>White Block"
        block_select = 1
    if blockselected == '2':
        clicksound.play()
        selection.position = Vec2(-0.33,0)
        hand.texture = 'grass'
        blocktext.text="Block: <red>Grass Block"
        block_select = 2
    if blockselected == '3':
        clicksound.play()
        selection.position = Vec2(-0.22,0)
        hand.texture = brick
        blocktext.text="Block: <red>Brick"
        block_select = 3
    if blockselected == '4':
        clicksound.play()
        selection.position = Vec2(-0.11,0)
        hand.texture = cobblestone
        blocktext.text="Block: <red>Cobblestone"
        block_select = 4
    if blockselected == '5':
        clicksound.play()
        selection.position = Vec2(0,0)
        hand.texture = dirt
        blocktext.text="Block: <red>Dirt"
        block_select = 5
    if blockselected == '6':
        clicksound.play()
        selection.position = Vec2(0.11,0)
        hand.texture = planks
        blocktext.text="Block: <red>Planks"
        block_select = 6
    if blockselected == '7':
        clicksound.play()
        selection.position = Vec2(0.22,0)
        hand.texture = glass
        blocktext.text="Block: <red>Glass"
        block_select = 7
    if blockselected == '8':
        clicksound.play()
        selection.position = Vec2(0.33,0)
        hand.texture = diamond
        blocktext.text="Block: <red>Diamond Block"
        block_select = 8
    if blockselected == '9':
        clicksound.play()
        selection.position = Vec2(0.44,0)
        hand.texture = void
        blocktext.text="Block: <violet>???"
        block_select = 9

def input(key):
    global block_select
    if key == 'escape':
        quit()

    if key == 'scroll up':
        if block_select == 9:
            blockselection('1')
        else:
            block_select += 1 
            blockselection(str(block_select))

    if key == 'scroll down':
        if block_select == 1:
            blockselection('9')
        else:
            block_select -= 1
            blockselection(str(block_select))

    blockselection(key)

def update():
    global ost, osts, block_select
    if osts[ost].playing == False:
        if ost == 4:
            osts[0].play()
            ost = 0
        else:
            tempost = ost + 1
            osts[tempost].play()
            ost += 1

    if held_keys['left control']:
        player.speed = 10
    else:
        player.speed = 5

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.anim_act()
    else:
        hand.anim_pas()
    
    if player.Y < -4:
        tp.play()
        player.world_position = Vec3(0,2,0)

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture = 'grass'):
        super().__init__(
            parent = scene,
            position = position, 
            model = 'cube',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            highlight_color = color.gray
        )
    
    def input(self,key):
        if self.hovered:
            positionofvolex = self.position + mouse.normal
            positionofplayer = Vec3(round(player.x), round(player.y)+1, round(player.z))
            positionofplayer2 = Vec3(round(player.x), round(player.y)+2, round(player.z))
            #print(positionofvolex)
            #print(positionofplayer)
            if key == 'right mouse down' and positionofvolex.y > 0 and positionofvolex != positionofplayer and positionofvolex != positionofplayer2:
                global blocksplaced
                blocksplaced += 1
                blocksplacedtext.text="Blocks Placed: <green>" + str(blocksplaced)
                placeblocksound.play()
                if block_select == 1:
                    voxel = Voxel(positionofvolex, texture='white_cube')
                if block_select == 2:
                    voxel = Voxel(positionofvolex, texture='grass')
                if block_select == 3:
                    voxel = Voxel(positionofvolex, texture=brick)
                if block_select == 4:
                    voxel = Voxel(positionofvolex, texture=cobblestone)
                if block_select == 5:
                    voxel = Voxel(positionofvolex, texture=dirt)
                if block_select == 6:
                    voxel = Voxel(positionofvolex, texture=planks)
                if block_select == 7:
                    voxel = Voxel(positionofvolex, texture=glass)
                if block_select == 8:
                    voxel = Voxel(positionofvolex, texture=diamond)
                if block_select == 9:
                    voxel = Voxel(positionofvolex, texture=void)
                    for y in range(-1,2):
                        for z in range(-1,2):
                            for x in range(-1,2):
                                voidpostion = (self.position + mouse.normal) + Vec3(x,y,z)
                                #print(voidpostion)
                                voxel = Voxel(voidpostion, texture=void)
            if key == 'left mouse down' and self.texture != bedrock:
                global blocksdestroyed
                blocksdestroyed += 1
                blocksdestroyedtext.text="Blocks Destroyed: <red>" + str(blocksdestroyed)
                if self.texture == void:
                    voidsound.play()
                destroyblocksound.play()
                destroy(self)


class skybox(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = 'sky_default',
            scale = 300,
            double_sided = True
        )


class hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'cube',
            texture = 'white_cube',
            scale = (0.2, 0.2, 0.2),
            position = Vec2(0.5, -0.48),
            rotation = Vec3(150, -50, 60)
        )

        #super().__init__(
        #    parent = camera.ui,
        #    model = 'cube',
        #    texture = 'white_cube',
        #    color = color.rgb(255, 178, 102),
        #    scale = (0.2, 0.2, 0.5),
        #    position = Vec2(0.5, -0.48),
        #    rotation = Vec3(150, -50, 60)
        #)
        
    
    def anim_act(self):
        self.position = Vec2(0.3, -0.5)
        self.rotation = Vec3(180, -35, 60)

    def anim_pas(self):
        self.position = Vec2(0.5, -0.48)
        self.rotation = Vec3(150, -50, 60)

class hud(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'cube',
            texture = 'assets/texture/hud.png',
            scale = (0.782, 0.094, 0.1),
            position = Vec2(0,-0.45)
        )

class selection(Entity):
    def __init__(self):
        super().__init__(
            parent = hud,
            model = 'cube',
            texture = 'assets/texture/selection.png',
            scale = (1/9, 1, 0.1),
            position = Vec2(-0.44,0)
        )


# ────────────────────────────────────────────────────────────────────────────────

for z in range(20):
    for x in range(20):
        for y in range(3):
            if y == 0:
                voxel = Voxel(position=(x,y,z), texture=bedrock)
            else:
                voxel = Voxel(position=(x,y,z))

player = FirstPersonController(
    mouse_sensitivity = Vec2(40, 40),
    speed = 5,
    jump_duration = 0.23,
    jump_height = 1
)

sky_box = skybox()
hand = hand()
hud = hud()
selection = selection()

player.add_script(NoclipMode(speed=10))

app.run()