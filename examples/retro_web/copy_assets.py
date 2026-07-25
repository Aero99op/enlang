import shutil
import os

src1 = r"C:\Users\spand\.gemini\antigravity-ide\brain\f746d4fa-7a0b-4434-85e0-24f528bd70f7\retro_cyber_hero_1784968926279.png"
src2 = r"C:\Users\spand\.gemini\antigravity-ide\brain\f746d4fa-7a0b-4434-85e0-24f528bd70f7\retro_arcade_showcase_1784968939414.png"

dest_dir = r"d:\enlangg\examples\retro_web\assets"
os.makedirs(dest_dir, exist_ok=True)

shutil.copy(src1, os.path.join(dest_dir, "hero.png"))
shutil.copy(src2, os.path.join(dest_dir, "arcade.png"))
print("Assets copied successfully!")
