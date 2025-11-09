# Quick Start Guide
## Python 3.14 Compatible Version

## ⚡ Installation (30 seconds)

```bash
# Install dependencies
pip install pygame PyOpenGL PyOpenGL-accelerate numpy

# Run the game
python fps_game.py
```

## 🎮 First Time Playing

1. **Main Menu** appears automatically
2. Click to choose your mode:
   - **Target Practice**: Static targets (great for beginners!)
   - **Survival Mode**: Waves of enemies (challenge mode!)
3. Mouse will lock automatically when game starts

## 🕹️ Essential Controls

```
Movement:    W A S D
Look:        Mouse
Shoot:       Left Click
Reload:      R
Weapons:     1 (Pistol)  2 (Rifle)  3 (Shotgun)
Pause:       P or ESC
```

## 🎯 Quick Tips for Beginners

### 1. Start with Target Practice
- Learn the controls without pressure
- Practice with each weapon
- Get familiar with aiming

### 2. Weapon Quick Guide
```
Pistol (1)   → Balanced, good accuracy
Rifle (2)    → Fast fire, lots of ammo
Shotgun (3)  → Massive damage up close
```

### 3. Watch Your Ammo!
- **White** = Good ammo
- **Yellow** = Low ammo  
- **Red** = Empty/critical
- Press **R** to reload manually
- Auto-reloads when empty

### 4. Survival Mode Strategy
```
Orange enemies (Fast)  → Kill FIRST (hard to hit)
Purple enemies (Tank)  → Use shotgun up close
Red enemies (Normal)   → Easy targets
```

### 5. Stay Alive
- **Keep moving!** Don't stand still
- Use gray boxes as cover
- Reload when safe, not during combat
- Watch the health bar (bottom left)

## 🐛 Common Issues

### Game won't start?
```bash
pip install --upgrade pygame PyOpenGL numpy
```

### Mouse not locked?
- **Click** on the game window
- Choose a game mode from menu
- Press ESC to pause and unlock mouse

### Can't see anything?
- Make sure your graphics drivers are updated
- Try running: `pip uninstall PyOpenGL-accelerate`

### Performance slow?
- Close other programs
- Lower the wave count in code (if comfortable editing)

## 🎯 Your First Game

1. **Launch**: `python fps_game.py`
2. **Click** "Target Practice"
3. **Look around** with mouse
4. **Move** with WASD
5. **Shoot** red targets with left click
6. **Reload** with R when ammo is low
7. **Try weapons**: Press 1, 2, 3 to switch
8. **Have fun!** 🎮

## ⌨️ Quick Reference Card

```
┌─────────────────────────────────────┐
│         FPS GAME CONTROLS           │
├─────────────────────────────────────┤
│ W/A/S/D      Move                   │
│ Mouse        Look/Aim               │
│ Left Click   Shoot                  │
│ R            Reload                 │
│ 1/2/3        Switch Weapon          │
│ P / ESC      Pause Menu             │
├─────────────────────────────────────┤
│ WEAPONS:                            │
│ 1 = Pistol    (Balanced)            │
│ 2 = Rifle     (Fast Fire)           │
│ 3 = Shotgun   (High Damage)         │
├─────────────────────────────────────┤
│ ENEMIES:                            │
│ Red    = Normal  (100 HP, 10 pts)   │
│ Orange = Fast    (50 HP, 5 pts)     │
│ Purple = Tank    (150 HP, 15 pts)   │
└─────────────────────────────────────┘
```

## 🎓 Pro Tips

- **Headshots**: Aim at the top of enemies for practice
- **Strafe**: Move sideways (A/D) while shooting
- **Burst Fire**: Tap instead of holding for better accuracy
- **Cover**: Use obstacles between you and enemies
- **Ammo Conservation**: Shotgun is powerful but ammo is limited

## 📱 System Check

**Works on:**
- ✅ Python 3.7 - 3.14+
- ✅ Windows
- ✅ macOS  
- ✅ Linux

**Needs:**
- OpenGL compatible graphics
- Mouse and keyboard
- ~50MB storage

---

**Ready to play? Launch it now!**

```bash
python fps_game.py
```

🎮 **Have fun and good luck!** 🎯



**Create Virtual Environment**
python -m venv venv

**Activate Virtual Environment**
venv\Scripts\Activate.ps1

**install dependencies**
pip install -r requirements.txt