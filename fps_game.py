"""
Enhanced 3D First-Person Shooter Game
Built with Pygame + PyOpenGL (Python 3.12+ Compatible)

Controls:
- WASD: Move
- Mouse: Look around
- Left Click: Shoot
- R: Reload
- 1/2/3: Switch weapons
- P or ESC: Pause menu
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
from dataclasses import dataclass
from typing import List
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FOV = 70
MOUSE_SENSITIVITY = 0.2
MOVE_SPEED = 5.0

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

@dataclass
class WeaponConfig:
    name: str
    damage: float
    fire_rate: float
    max_ammo: int
    reload_time: float
    spread: float
    pellets: int = 1

# Weapon configurations
WEAPONS = {
    'pistol': WeaponConfig('Pistol', 35, 0.3, 12, 1.5, 0.01),
    'rifle': WeaponConfig('Rifle', 25, 0.15, 30, 2.0, 0.005),
    'shotgun': WeaponConfig('Shotgun', 20, 0.8, 8, 2.5, 0.05, 6)
}

class Vector3:
    """3D Vector class"""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        l = self.length()
        if l > 0:
            return Vector3(self.x/l, self.y/l, self.z/l)
        return Vector3(0, 0, 0)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

class Camera:
    """First-person camera"""
    def __init__(self, pos=Vector3(0, 2, 0)):
        self.position = pos
        self.yaw = 0.0
        self.pitch = 0.0
    
    def get_forward(self):
        x = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        y = math.sin(math.radians(self.pitch))
        z = -math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        return Vector3(x, y, z).normalize()
    
    def get_right(self):
        forward = self.get_forward()
        up = Vector3(0, 1, 0)
        return Vector3(
            forward.z * up.y - forward.y * up.z,
            forward.x * up.z - forward.z * up.x,
            forward.y * up.x - forward.x * up.y
        ).normalize()
    
    def apply(self):
        glRotatef(-self.pitch, 1, 0, 0)
        glRotatef(-self.yaw, 0, 1, 0)
        glTranslatef(-self.position.x, -self.position.y, -self.position.z)

class Enemy:
    """Enemy entity"""
    def __init__(self, position, enemy_type='normal'):
        self.position = position
        self.enemy_type = enemy_type
        self.alive = True
        
        if enemy_type == 'fast':
            self.health = 50
            self.max_health = 50
            self.speed = 2.0
            self.size = 0.8
            self.color = (1.0, 0.5, 0.0)  # Orange
            self.score = 5
        elif enemy_type == 'tank':
            self.health = 150
            self.max_health = 150
            self.speed = 0.5
            self.size = 1.5
            self.color = (0.5, 0.0, 1.0)  # Purple
            self.score = 15
        else:  # normal
            self.health = 100
            self.max_health = 100
            self.speed = 1.0
            self.size = 1.0
            self.color = (1.0, 0.0, 0.0)  # Red
            self.score = 10
        
        self.move_timer = 0
        self.move_target = None
    
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def update(self, dt, player_pos):
        if not self.alive:
            return
        
        self.move_timer += dt
        if self.move_timer > 2.0:
            self.move_timer = 0
            offset = Vector3(random.uniform(-5, 5), 0, random.uniform(-5, 5))
            self.move_target = player_pos + offset
        
        if self.move_target:
            direction = self.move_target - self.position
            direction.y = 0
            dist = direction.length()
            if dist > 0.5:
                move = direction.normalize() * self.speed * dt
                self.position = self.position + move
    
    def render(self):
        if not self.alive:
            return
        
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        
        # Draw enemy cube
        glColor3f(*self.color)
        draw_cube(self.size, self.size * 2, self.size)
        
        # Draw health bar above enemy
        health_percent = self.health / self.max_health
        glPushMatrix()
        glTranslatef(0, self.size * 2.5, 0)
        
        # Billboard effect (always face camera) - simplified
        glRotatef(90, 1, 0, 0)
        
        # Background bar
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(-0.6, 0, 0)
        glVertex3f(0.6, 0, 0)
        glVertex3f(0.6, 0.15, 0)
        glVertex3f(-0.6, 0.15, 0)
        glEnd()
        
        # Health bar
        if health_percent > 0.6:
            glColor3f(0.0, 1.0, 0.0)
        elif health_percent > 0.3:
            glColor3f(1.0, 1.0, 0.0)
        else:
            glColor3f(1.0, 0.0, 0.0)
        
        glBegin(GL_QUADS)
        glVertex3f(-0.6, 0, -0.01)
        glVertex3f(-0.6 + 1.2 * health_percent, 0, -0.01)
        glVertex3f(-0.6 + 1.2 * health_percent, 0.15, -0.01)
        glVertex3f(-0.6, 0.15, -0.01)
        glEnd()
        
        glPopMatrix()
        glPopMatrix()

class Particle:
    """Particle effect"""
    def __init__(self, position, velocity, color, lifetime):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alive = True
    
    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
            return
        
        self.position = self.position + self.velocity * dt
        self.velocity.y -= 10.0 * dt
    
    def render(self):
        if not self.alive:
            return
        
        alpha = self.lifetime / self.max_lifetime
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glColor4f(self.color[0], self.color[1], self.color[2], alpha)
        draw_cube(0.15, 0.15, 0.15)
        glPopMatrix()

class Game:
    """Main game controller"""
    def __init__(self):
        self.state = GameState.MENU
        self.camera = Camera()
        self.enemies: List[Enemy] = []
        self.particles: List[Particle] = []
        
        self.score = 0
        self.kills = 0
        self.wave = 0
        self.player_health = 100
        self.max_health = 100
        
        self.current_weapon = 'pistol'
        self.weapons = {
            'pistol': {'ammo': 12, 'reserve': 36, 'cooldown': 0, 'reloading': 0},
            'rifle': {'ammo': 30, 'reserve': 90, 'cooldown': 0, 'reloading': 0},
            'shotgun': {'ammo': 8, 'reserve': 24, 'cooldown': 0, 'reloading': 0}
        }
        
        self.game_mode = None
        self.enemies_per_wave = 5
        self.shake_amount = 0
        self.shake_timer = 0
        self.kill_feed = []
    
    def start_game(self, mode):
        self.game_mode = mode
        self.state = GameState.PLAYING
        self.score = 0
        self.kills = 0
        self.wave = 0
        self.player_health = 100
        self.enemies.clear()
        self.particles.clear()
        self.kill_feed.clear()
        
        self.weapons['pistol'] = {'ammo': 12, 'reserve': 36, 'cooldown': 0, 'reloading': 0}
        self.weapons['rifle'] = {'ammo': 30, 'reserve': 90, 'cooldown': 0, 'reloading': 0}
        self.weapons['shotgun'] = {'ammo': 8, 'reserve': 24, 'cooldown': 0, 'reloading': 0}
        self.current_weapon = 'pistol'
        
        self.camera.position = Vector3(0, 2, 0)
        self.camera.yaw = 0
        self.camera.pitch = 0
        
        if mode == 'target':
            self.spawn_targets()
        else:
            self.wave = 1
            self.spawn_wave()
    
    def spawn_targets(self):
        positions = [
            Vector3(0, 1, 10), Vector3(-5, 1, 8), Vector3(5, 1, 8),
            Vector3(-3, 1, 12), Vector3(3, 1, 12), Vector3(0, 1, 15),
            Vector3(-7, 1, 10), Vector3(7, 1, 10),
        ]
        for pos in positions:
            self.enemies.append(Enemy(pos, 'normal'))
    
    def spawn_wave(self):
        self.add_kill_feed(f'Wave {self.wave} Starting!')
        enemy_types = ['normal', 'fast', 'tank']
        
        for i in range(self.enemies_per_wave):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(10, 20)
            x = distance * math.cos(angle)
            z = distance * math.sin(angle)
            
            enemy_type = random.choice(enemy_types)
            self.enemies.append(Enemy(Vector3(x, 1, z), enemy_type))
        
        self.enemies_per_wave += 2
    
    def shoot(self):
        weapon_data = self.weapons[self.current_weapon]
        config = WEAPONS[self.current_weapon]
        
        if weapon_data['cooldown'] > 0 or weapon_data['reloading'] > 0 or weapon_data['ammo'] <= 0:
            return
        
        weapon_data['ammo'] -= 1
        weapon_data['cooldown'] = config.fire_rate
        self.screen_shake(0.15)
        
        for _ in range(config.pellets):
            forward = self.camera.get_forward()
            spread_x = random.uniform(-config.spread, config.spread)
            spread_y = random.uniform(-config.spread, config.spread)
            
            direction = Vector3(
                forward.x + spread_x,
                forward.y + spread_y,
                forward.z
            ).normalize()
            
            hit_enemy = self.raycast(self.camera.position, direction)
            if hit_enemy:
                killed = hit_enemy.hit(config.damage)
                if killed:
                    self.score += hit_enemy.score
                    self.kills += 1
                    self.add_kill_feed(f'Eliminated {hit_enemy.enemy_type.title()} Enemy')
                    self.create_explosion(hit_enemy.position)
    
    def reload(self):
        weapon_data = self.weapons[self.current_weapon]
        config = WEAPONS[self.current_weapon]
        
        if weapon_data['reloading'] > 0 or weapon_data['ammo'] == config.max_ammo or weapon_data['reserve'] <= 0:
            return
        
        weapon_data['reloading'] = config.reload_time
    
    def finish_reload(self):
        weapon_data = self.weapons[self.current_weapon]
        config = WEAPONS[self.current_weapon]
        
        ammo_needed = config.max_ammo - weapon_data['ammo']
        ammo_to_reload = min(ammo_needed, weapon_data['reserve'])
        
        weapon_data['ammo'] += ammo_to_reload
        weapon_data['reserve'] -= ammo_to_reload
        weapon_data['reloading'] = 0
    
    def raycast(self, origin, direction):
        closest_enemy = None
        closest_dist = float('inf')
        
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            
            to_enemy = enemy.position - origin
            proj = to_enemy.dot(direction)
            
            if proj < 0:
                continue
            
            closest_point = origin + direction * proj
            dist_to_enemy = (closest_point - enemy.position).length()
            
            if dist_to_enemy < enemy.size and proj < closest_dist:
                closest_dist = proj
                closest_enemy = enemy
        
        return closest_enemy
    
    def create_explosion(self, position):
        for i in range(15):
            velocity = Vector3(
                random.uniform(-3, 3),
                random.uniform(0, 3),
                random.uniform(-3, 3)
            )
            color = random.choice([
                (1.0, 0.5, 0.0),
                (1.0, 0.0, 0.0),
                (1.0, 1.0, 0.0)
            ])
            self.particles.append(Particle(position, velocity, color, random.uniform(0.3, 0.7)))
    
    def screen_shake(self, amount):
        self.shake_amount = amount
        self.shake_timer = 0.2
    
    def add_kill_feed(self, message):
        self.kill_feed.append({'message': message, 'time': 3.0})
    
    def update(self, dt):
        if self.state != GameState.PLAYING:
            return
        
        for weapon_data in self.weapons.values():
            if weapon_data['cooldown'] > 0:
                weapon_data['cooldown'] -= dt
            if weapon_data['reloading'] > 0:
                weapon_data['reloading'] -= dt
                if weapon_data['reloading'] <= 0:
                    self.finish_reload()
        
        weapon_data = self.weapons[self.current_weapon]
        if weapon_data['ammo'] == 0 and weapon_data['reloading'] == 0 and weapon_data['reserve'] > 0:
            self.reload()
        
        for enemy in self.enemies:
            enemy.update(dt, self.camera.position)
        
        self.enemies = [e for e in self.enemies if e.alive]
        
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.alive]
        
        for item in self.kill_feed:
            item['time'] -= dt
        self.kill_feed = [item for item in self.kill_feed if item['time'] > 0]
        
        if self.shake_timer > 0:
            self.shake_timer -= dt
        
        if self.game_mode == 'survival' and len(self.enemies) == 0:
            self.wave += 1
            self.spawn_wave()
        elif self.game_mode == 'target' and len(self.enemies) == 0:
            self.spawn_targets()

def draw_cube(width, height, depth):
    """Draw a cube with proper lighting"""
    w, h, d = width/2, height/2, depth/2
    
    glBegin(GL_QUADS)
    
    # Front face (towards +Z)
    glNormal3f(0, 0, 1)
    glVertex3f(-w, -h, d)
    glVertex3f(w, -h, d)
    glVertex3f(w, h, d)
    glVertex3f(-w, h, d)
    
    # Back face (towards -Z)
    glNormal3f(0, 0, -1)
    glVertex3f(-w, -h, -d)
    glVertex3f(-w, h, -d)
    glVertex3f(w, h, -d)
    glVertex3f(w, -h, -d)
    
    # Top face (towards +Y)
    glNormal3f(0, 1, 0)
    glVertex3f(-w, h, -d)
    glVertex3f(-w, h, d)
    glVertex3f(w, h, d)
    glVertex3f(w, h, -d)
    
    # Bottom face (towards -Y)
    glNormal3f(0, -1, 0)
    glVertex3f(-w, -h, -d)
    glVertex3f(w, -h, -d)
    glVertex3f(w, -h, d)
    glVertex3f(-w, -h, d)
    
    # Right face (towards +X)
    glNormal3f(1, 0, 0)
    glVertex3f(w, -h, -d)
    glVertex3f(w, h, -d)
    glVertex3f(w, h, d)
    glVertex3f(w, -h, d)
    
    # Left face (towards -X)
    glNormal3f(-1, 0, 0)
    glVertex3f(-w, -h, -d)
    glVertex3f(-w, -h, d)
    glVertex3f(-w, h, d)
    glVertex3f(-w, h, -d)
    
    glEnd()

def draw_ground():
    """Draw ground with grid"""
    # Main ground
    glColor3f(0.3, 0.5, 0.3)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-100, 0, -100)
    glVertex3f(100, 0, -100)
    glVertex3f(100, 0, 100)
    glVertex3f(-100, 0, 100)
    glEnd()
    
    # Grid lines
    glColor3f(0.2, 0.4, 0.2)
    glBegin(GL_LINES)
    for i in range(-100, 101, 5):
        glVertex3f(i, 0.01, -100)
        glVertex3f(i, 0.01, 100)
        glVertex3f(-100, 0.01, i)
        glVertex3f(100, 0.01, i)
    glEnd()

def draw_obstacles():
    """Draw obstacles/walls"""
    obstacles = [
        (5, 1.5, 10, 2, 3, 2),
        (-5, 1.5, 8, 2, 3, 2),
        (0, 1.5, 15, 3, 3, 3),
        (-10, 1.5, 12, 2, 4, 2),
        (10, 1.5, 12, 2, 4, 2),
        (-3, 1.5, 6, 2, 3, 2),
        (3, 1.5, 6, 2, 3, 2),
    ]
    
    glColor3f(0.4, 0.4, 0.4)
    for x, y, z, w, h, d in obstacles:
        glPushMatrix()
        glTranslatef(x, y, z)
        draw_cube(w, h, d)
        glPopMatrix()

def setup_lighting():
    """Setup OpenGL lighting"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Ambient light
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 20, 0, 1])
    
    # Global ambient
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0])

def render_text_2d(text, x, y, color=(255, 255, 255), size=24):
    """Render 2D text overlay"""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    
    glWindowPos2d(int(x), int(SCREEN_HEIGHT - y - size))
    glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def main():
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D FPS Game - Enhanced Edition")
    
    # OpenGL setup
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Setup lighting
    setup_lighting()
    
    # Perspective
    glMatrixMode(GL_PROJECTION)
    gluPerspective(FOV, SCREEN_WIDTH/SCREEN_HEIGHT, 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)
    
    game = Game()
    clock = pygame.time.Clock()
    
    pygame.mouse.set_visible(True)
    mouse_locked = False
    keys_down = set()
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            elif event.type == KEYDOWN:
                keys_down.add(event.key)
                
                if game.state == GameState.PLAYING:
                    if event.key == K_r:
                        game.reload()
                    elif event.key == K_1:
                        game.current_weapon = 'pistol'
                    elif event.key == K_2:
                        game.current_weapon = 'rifle'
                    elif event.key == K_3:
                        game.current_weapon = 'shotgun'
                    elif event.key == K_p or event.key == K_ESCAPE:
                        game.state = GameState.PAUSED
                        pygame.mouse.set_visible(True)
                        mouse_locked = False
                
                elif game.state == GameState.PAUSED:
                    if event.key == K_p or event.key == K_ESCAPE:
                        game.state = GameState.PLAYING
                        pygame.mouse.set_visible(False)
                        mouse_locked = True
                        pygame.mouse.set_pos(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                    elif event.key == K_m:
                        game.state = GameState.MENU
                        pygame.mouse.set_visible(True)
                        mouse_locked = False
            
            elif event.type == KEYUP:
                keys_down.discard(event.key)
            
            elif event.type == MOUSEBUTTONDOWN:
                if game.state == GameState.MENU:
                    mx, my = pygame.mouse.get_pos()
                    if 440 <= mx <= 840 and 300 <= my <= 380:
                        game.start_game('target')
                        pygame.mouse.set_visible(False)
                        mouse_locked = True
                        pygame.mouse.set_pos(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                    elif 440 <= mx <= 840 and 420 <= my <= 500:
                        game.start_game('survival')
                        pygame.mouse.set_visible(False)
                        mouse_locked = True
                        pygame.mouse.set_pos(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                
                elif game.state == GameState.PLAYING and event.button == 1:
                    game.shoot()
            
            elif event.type == MOUSEMOTION and mouse_locked:
                dx, dy = event.rel
                game.camera.yaw += dx * MOUSE_SENSITIVITY
                game.camera.pitch -= dy * MOUSE_SENSITIVITY
                game.camera.pitch = max(-89, min(89, game.camera.pitch))
        
        game.update(dt)
        
        # Player movement
        if game.state == GameState.PLAYING:
            forward = game.camera.get_forward()
            right = game.camera.get_right()
            
            move = Vector3(0, 0, 0)
            if K_w in keys_down:
                move = move + Vector3(forward.x, 0, forward.z)
            if K_s in keys_down:
                move = move - Vector3(forward.x, 0, forward.z)
            if K_a in keys_down:
                move = move - right
            if K_d in keys_down:
                move = move + right
            
            if move.length() > 0:
                move = move.normalize() * MOVE_SPEED * dt
                game.camera.position = game.camera.position + move
        
        # Clear and render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if game.state == GameState.MENU:
            # Menu rendering
            glClearColor(0.2, 0.2, 0.3, 1.0)
            
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            
            glDisable(GL_LIGHTING)
            glDisable(GL_DEPTH_TEST)
            
            # Draw menu buttons
            mx, my = pygame.mouse.get_pos()
            
            # Title
            render_text_2d("3D FPS GAME", SCREEN_WIDTH//2 - 150, 100, (255, 140, 0), 64)
            render_text_2d("Enhanced Edition", SCREEN_WIDTH//2 - 100, 180, (255, 255, 255), 32)
            
            # Buttons
            color1 = (100, 200, 100) if (440 <= mx <= 840 and 300 <= my <= 380) else (50, 150, 50)
            glColor3ub(*color1)
            glBegin(GL_QUADS)
            glVertex2f(440, 300)
            glVertex2f(840, 300)
            glVertex2f(840, 380)
            glVertex2f(440, 380)
            glEnd()
            render_text_2d("Target Practice", 520, 325, (255, 255, 255), 36)
            
            color2 = (200, 100, 100) if (440 <= mx <= 840 and 420 <= my <= 500) else (150, 50, 50)
            glColor3ub(*color2)
            glBegin(GL_QUADS)
            glVertex2f(440, 420)
            glVertex2f(840, 420)
            glVertex2f(840, 500)
            glVertex2f(440, 500)
            glEnd()
            render_text_2d("Survival Mode", 540, 445, (255, 255, 255), 36)
            
            render_text_2d("WASD: Move | Mouse: Look | Click: Shoot | R: Reload | 1/2/3: Weapons",
                          200, 600, (200, 200, 200), 24)
            
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)
            
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
        
        else:
            # 3D world rendering
            glClearColor(0.5, 0.7, 1.0, 1.0)
            
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            
            # Screen shake
            if game.shake_timer > 0:
                shake_x = random.uniform(-game.shake_amount, game.shake_amount)
                shake_y = random.uniform(-game.shake_amount, game.shake_amount)
                glTranslatef(shake_x, shake_y, 0)
            
            game.camera.apply()
            
            # Draw world
            draw_ground()
            draw_obstacles()
            
            # Draw enemies
            for enemy in game.enemies:
                enemy.render()
            
            # Draw particles
            for particle in game.particles:
                particle.render()
            
            # 2D UI overlay
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            
            glDisable(GL_LIGHTING)
            glDisable(GL_DEPTH_TEST)
            
            if game.state == GameState.PLAYING:
                # Crosshair
                glColor3f(1, 1, 1)
                cx, cy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
                glBegin(GL_LINES)
                glVertex2f(cx - 10, cy)
                glVertex2f(cx + 10, cy)
                glVertex2f(cx, cy - 10)
                glVertex2f(cx, cy + 10)
                glEnd()
                
                # HUD
                weapon_data = game.weapons[game.current_weapon]
                config = WEAPONS[game.current_weapon]
                
                ammo_text = f"{weapon_data['ammo']} / {weapon_data['reserve']}"
                if weapon_data['reloading'] > 0:
                    ammo_text += " [RELOADING]"
                ammo_color = (255, 255, 255) if weapon_data['ammo'] > 5 else (255, 255, 0) if weapon_data['ammo'] > 0 else (255, 0, 0)
                render_text_2d(ammo_text, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60, ammo_color, 32)
                render_text_2d(config.name, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30, (200, 200, 200), 24)
                
                health_percent = game.player_health / game.max_health
                health_color = (0, 255, 0) if health_percent > 0.6 else (255, 255, 0) if health_percent > 0.3 else (255, 0, 0)
                render_text_2d(f"HP: {int(game.player_health)}", 20, SCREEN_HEIGHT - 60, health_color, 28)
                
                render_text_2d(f"Score: {game.score} | Kills: {game.kills}", 20, 20, (255, 255, 255), 28)
                if game.game_mode == 'survival':
                    render_text_2d(f"Wave: {game.wave}", 20, 50, (0, 255, 255), 24)
                
                for i, item in enumerate(game.kill_feed[:5]):
                    render_text_2d(item['message'], SCREEN_WIDTH - 350, 100 + i * 30, (255, 255, 255), 20)
            
            elif game.state == GameState.PAUSED:
                glColor4ub(0, 0, 0, 180)
                glBegin(GL_QUADS)
                glVertex2f(390, 200)
                glVertex2f(890, 200)
                glVertex2f(890, 500)
                glVertex2f(390, 500)
                glEnd()
                
                render_text_2d("PAUSED", SCREEN_WIDTH//2 - 80, 250, (255, 255, 0), 48)
                render_text_2d("P/ESC: Resume", SCREEN_WIDTH//2 - 100, 350, (255, 255, 255), 32)
                render_text_2d("M: Main Menu", SCREEN_WIDTH//2 - 100, 400, (255, 255, 255), 32)
            
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)
            
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
