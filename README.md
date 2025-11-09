# 3D First-Person Shooter Game - Enhanced Edition
## Python 3.14 Compatible (Pygame + PyOpenGL)

A fully-featured 3D FPS game built with Pygame and PyOpenGL, featuring multiple weapons, ammo system, health mechanics, AI enemies, and polished gameplay.

## ✨ Python 3.14 Compatible!

This version uses **Pygame + PyOpenGL** instead of Ursina, making it fully compatible with Python 3.14 and future versions!

## 🎮 Features

### Weapon System
- **Pistol**: Balanced weapon (35 damage, 12 rounds, medium fire rate)
- **Rifle**: Fast firing (25 damage, 30 rounds, high fire rate)  
- **Shotgun**: Close range powerhouse (120 max damage with 6 pellets, 8 rounds)
- Magazine-based ammo with reserve ammunition
- Reload mechanics (press R)
- Auto-reload when empty
- Weapon switching (1/2/3 keys)

### Combat System
- **3 Enemy Types**:
  - Normal (Red): 100 HP, medium speed, 10 points
  - Fast (Orange): 50 HP, high speed, 5 points  
  - Tank (Purple): 150 HP, slow, 15 points
- Enemy AI with movement and player tracking
- Health bars above enemies
- Raycast-based shooting
- Weapon spread mechanics

### Game Modes
- **Target Practice**: Static targets for aim training
- **Survival Mode**: Endless waves with increasing difficulty

### Visual Effects
- Screen shake on shooting
- Particle explosion effects
- Color-coded health and ammo displays
- Enemy damage feedback
- Professional crosshair

### UI Features
- Main menu with mode selection
- Pause menu (P or ESC)
- Real-time HUD (health, ammo, score, kills)
- Wave counter (survival mode)
- Kill feed notifications
- Color-coded indicators

## 📋 Installation

### Requirements
- Python 3.7+ (including Python 3.14!)
- Pygame 2.6.0+
- PyOpenGL 3.1.7+

### Quick Install

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pygame PyOpenGL PyOpenGL-accelerate numpy
```

## 🎯 How to Run

```bash
python fps_game.py
```

## 🎮 Controls

| Action | Key/Input |
|--------|-----------|
| Move Forward | W |
| Move Left | A |
| Move Backward | S |
| Move Right | D |
| Look Around | Mouse |
| Shoot | Left Click |
| Reload | R |
| Switch to Pistol | 1 |
| Switch to Rifle | 2 |
| Switch to Shotgun | 3 |
| Pause | P or ESC |

## 🎲 Game Modes

### Target Practice Mode
- Perfect for practicing aim and weapon handling
- Static red targets spawn around the map
- New targets appear when all are destroyed
- No time pressure, focus on accuracy
- Great for learning weapon characteristics

### Survival Mode
- Wave-based endless combat
- Enemies spawn in increasing numbers each wave
- Mix of all three enemy types
- Enemies move and pursue the player
- Test your skills - how long can you survive?

## 🔫 Weapons Guide

### Pistol (Key: 1)
- **Damage**: 35 per shot
- **Magazine**: 12 rounds
- **Reserve**: 36 rounds
- **Fire Rate**: 0.3 seconds
- **Reload**: 1.5 seconds
- **Spread**: Very low
- **Best For**: Accuracy, medium range, balanced combat

### Rifle (Key: 2)
- **Damage**: 25 per shot
- **Magazine**: 30 rounds
- **Reserve**: 90 rounds
- **Fire Rate**: 0.15 seconds (FAST!)
- **Reload**: 2.0 seconds
- **Spread**: Low
- **Best For**: Multiple enemies, sustained fire, suppression

### Shotgun (Key: 3)
- **Damage**: 20 per pellet × 6 = 120 max damage
- **Magazine**: 8 rounds
- **Reserve**: 24 rounds
- **Fire Rate**: 0.8 seconds (slow)
- **Reload**: 2.5 seconds
- **Spread**: High
- **Best For**: Close range, high burst damage, tank enemies

## 👾 Enemy Guide

### Normal Enemy (Red Cubes)
- **Health**: 100 HP
- **Speed**: Medium (1.0)
- **Size**: Normal
- **Score**: 10 points
- **Strategy**: Standard targets, 3 pistol shots or 1-2 shotgun blasts

### Fast Enemy (Orange Cubes)
- **Health**: 50 HP
- **Speed**: Fast (2.0)
- **Size**: Smaller
- **Score**: 5 points
- **Strategy**: Hard to hit but fragile. Use rifle for tracking or shotgun up close

### Tank Enemy (Purple Cubes)
- **Health**: 150 HP
- **Speed**: Slow (0.5)
- **Size**: Large
- **Score**: 15 points
- **Strategy**: High value target. Use shotgun at close range or focus rifle fire

## 🎨 Technical Features

### Graphics
- Full 3D rendering with OpenGL
- First-person camera with smooth mouse look
- Dynamic lighting and depth
- Grid-based ground plane
- 3D obstacles and cover
- Particle effects system

### Game Mechanics
- Raycast-based hit detection
- Weapon spread simulation
- Enemy AI pathfinding
- Auto-reload system
- Screen shake feedback
- Kill feed system

## ⚙️ Customization

### Modify Weapon Stats
Edit the `WEAPONS` dictionary:
```python
WEAPONS = {
    'pistol': WeaponConfig(
        name='Pistol',
        damage=35,        # Damage per shot
        fire_rate=0.3,    # Seconds between shots
        max_ammo=12,      # Magazine size
        reload_time=1.5,  # Reload duration
        spread=0.01       # Bullet spread
    ),
    # ... more weapons
}
```

### Adjust Game Settings
```python
# At the top of fps_game.py
MOVE_SPEED = 5.0           # Player movement speed
MOUSE_SENSITIVITY = 0.2    # Mouse look sensitivity
FOV = 70                   # Field of view
```

### Modify Enemy Difficulty
In the `Enemy.__init__()` method:
```python
if enemy_type == 'normal':
    self.health = 100      # Adjust health
    self.speed = 1.0       # Adjust speed
    self.score = 10        # Adjust points
```

### Change Wave Difficulty
```python
# In Game.__init__()
self.enemies_per_wave = 5  # Starting enemies

# In spawn_wave()
self.enemies_per_wave += 2  # Increase per wave
```

## 🎯 Gameplay Tips

1. **Weapon Selection**
   - Use rifle for waves of enemies
   - Switch to shotgun for close encounters
   - Pistol when conserving ammo

2. **Ammo Management**
   - Reload during safe moments
   - Watch the ammo counter (color-coded)
   - Each weapon has different reserve amounts

3. **Enemy Prioritization**
   - Kill fast (orange) enemies first - they're hard to hit
   - Focus tank (purple) enemies when isolated
   - Normal (red) enemies for steady points

4. **Movement**
   - Keep moving to avoid being surrounded
   - Use obstacles for cover
   - Strafe while shooting

5. **Survival Strategy**
   - Manage ammo across all weapons
   - Don't waste shotgun shells on fast enemies
   - Keep distance from tank enemies unless using shotgun

## 🐛 Troubleshooting

### Import Errors
```bash
pip install --upgrade pygame PyOpenGL PyOpenGL-accelerate numpy
```

### Performance Issues
- Lower enemy count in code
- Reduce particle count in `create_explosion()`
- Close other applications

### Mouse Not Working
- Click on the game window to focus
- Start a game mode from main menu to lock mouse
- Press ESC/P to unlock mouse

### Black Screen
- Update graphics drivers
- Ensure OpenGL support is available
- Try running without PyOpenGL-accelerate

### Weapons Not Switching
- Make sure you're in-game (not menu/pause)
- Use number keys 1, 2, 3 (not numpad)

## 💡 Advanced Features

- **Auto-Reload**: Weapons reload automatically when empty
- **Smart UI**: Color-coded health and ammo (white → yellow → red)
- **Screen Shake**: Intensity-based feedback system
- **Particle System**: Physics-based explosion particles
- **Enemy AI**: Basic pursuit and positioning
- **Kill Feed**: Timed message system
- **State Management**: Menu → Playing → Paused → Game Over

## 📊 System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.7 - 3.14+ (fully compatible!)
- **Graphics**: OpenGL 2.1+ compatible GPU
- **RAM**: 512MB minimum
- **Storage**: 50MB

## 🚀 Why Pygame + PyOpenGL?

- ✅ **Python 3.14 Compatible** - Works with latest Python
- ✅ **Cross-Platform** - Windows, Mac, Linux
- ✅ **Lightweight** - Minimal dependencies
- ✅ **Full Control** - Direct OpenGL access
- ✅ **Well Documented** - Mature libraries
- ✅ **Future-Proof** - Will work with future Python versions

## 🎓 Learning Value

This project demonstrates:
- 3D graphics programming with OpenGL
- Game state management
- First-person camera systems
- Raycasting and collision detection
- Particle effects
- UI/HUD design
- Event-driven programming
- Object-oriented design
- Vector mathematics
- Game loop architecture

## 📝 Version History

**v3.0 - Pygame + PyOpenGL Edition**
- Rebuilt for Python 3.14 compatibility
- Uses Pygame + PyOpenGL instead of Ursina
- All features preserved from Enhanced Edition
- Improved performance
- Better cross-platform support

**v2.0 - Enhanced Edition**
- Multiple weapons system
- Ammo and reload mechanics
- Enemy AI and types
- Game modes
- Full UI polish

**v1.0 - Initial Release**
- Basic FPS mechanics
- Simple target shooting

## 🔮 Future Enhancements

- Sound effects and music
- More weapon types (sniper, SMG, grenades)
- Different maps and environments
- Power-ups and pickups
- Leaderboard/high scores
- More enemy types and behaviors
- Difficulty settings
- Custom crosshairs
- Achievements

---

**Enjoy the game!** 🎮

Built with ❤️ using Pygame and PyOpenGL

Compatible with Python 3.7 through 3.14+
