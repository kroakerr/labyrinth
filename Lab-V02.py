import turtle
import math
import time  # time modul für clock (Monster)

# 1) Fenster

Fenster = turtle.Screen()
Fenster.bgcolor("chocolate")
Fenster.title("Labyrinth")
Fenster.setup(700, 700)

# Alle Sprites

Fenster.addshape("sprites/wall.gif")
Fenster.addshape("sprites/eye.gif")
Fenster.addshape("sprites/door.gif")
Fenster.addshape("sprites/door2.gif")
Fenster.addshape("sprites/player.gif")
Fenster.addshape("sprites/key.gif")

# Globale Werte

current_level = 1
lives = 3
view_radius = 120 

# Klassen

class Mauer(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("sprites/wall.gif")
        self.penup()
        self.speed(0)

class Spieler(turtle.Turtle):
    """Player character."""
    def __init__(self):
        super().__init__()
        self.shape("sprites/player.gif")
        self.color("green")
        self.penup()
        self.speed(0)

        self.gold = 0
        self.hasKey = False 

        # Damit Spieler nicht aus dem Labyrinth kommen
        self.min_x = -288
        self.max_x =  288
        self.min_y = -288
        self.max_y =  288

    def _check_bounding_box(self, x, y):
        """Return True if (x, y) is in valid map range, else False."""
        return (self.min_x <= x <= self.max_x and
                self.min_y <= y <= self.max_y)

    def _try_open_door(self, x, y):
        """
        Wenn (x, y) eine Tür ist, wird 200 Gold subtrahiert und die Tür wird von doorliste gelöscht
        """
        for d in DoorListe:
            if d.x_block == x and d.y_block == y:
                # Found the door tile. Check the gold
                if self.gold >= 200:
                    print("Door unlocked! Subtracting 200 gold.")
                    self.gold -= 200
                    # Remove door from DoorListe
                    DoorListe.remove(d)
                    d.destroy()
                    return True
                else:
                    print("Need at least 200 gold to open this door!")
                    return False
        # Not a door tile
        return True

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24

        # bounding box
        if not self._check_bounding_box(move_to_x, move_to_y):
            return

        if not self._try_open_door(move_to_x, move_to_y):
            return  

        self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24

        if not self._check_bounding_box(move_to_x, move_to_y):
            return

        if (move_to_x, move_to_y) in Mauerliste:
            print("Blocked by a wall!")
            return

        if not self._try_open_door(move_to_x, move_to_y):
            return

        self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()

        if not self._check_bounding_box(move_to_x, move_to_y):
            return

        if (move_to_x, move_to_y) in Mauerliste:
            print("Blocked by a wall!")
            return

        if not self._try_open_door(move_to_x, move_to_y):
            return

        self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()

        if not self._check_bounding_box(move_to_x, move_to_y):
            return

        if (move_to_x, move_to_y) in Mauerliste:
            print("Blocked by a wall!")
            return

        if not self._try_open_door(move_to_x, move_to_y):
            return

        self.goto(move_to_x, move_to_y)

    def kollision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        dist = math.sqrt((a**2) + (b**2))
        return dist < 5

class Schatz(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.left(90)
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Eye(turtle.Turtle):
    # Radius wird um 40 erhöht
    def __init__(self, x, y):
        super().__init__()
        self.shape("sprites/eye.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.extension = 40

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Ausgang(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("sprites/door2.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Key(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.left(90)
        self.shape("sprites/key.gif")
        self.color("purple")
        self.penup()
        self.speed(0)
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Door(turtle.Turtle):

    def __init__(self, x, y):
        super().__init__()
        self.shape("sprites/door.gif") 
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.x_block = x
        self.y_block = y

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Monster(turtle.Turtle):

    def __init__(self, x, y):
        super().__init__()
        self.shape("square") 
        self.color("red")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.direction = None 
        self.set_initial_direction()

    def set_initial_direction(self):

        current_x = self.xcor()
        current_y = self.ycor()

        # Check if there's a wall to the left and right
        if (current_x - 24, current_y) in Mauerliste and (current_x + 24, current_y) in Mauerliste:
            self.direction = "up"  # Move vertically
        # Check if there's a wall above and below
        elif (current_x, current_y + 24) in Mauerliste and (current_x, current_y - 24) in Mauerliste:
            self.direction = "right"  # Move horizontally
        else:
            # Default direction: move right
            self.direction = "right"

    def move(self):
        current_x = self.xcor()
        current_y = self.ycor()

        # Move based on the current direction
        if self.direction == "right":
            if (current_x + 24, current_y) in Mauerliste or current_x + 24 > 288:
                self.direction = "left"
            else:
                self.goto(current_x + 24, current_y)
        elif self.direction == "left":
            if (current_x - 24, current_y) in Mauerliste or current_x - 24 < -288:
                self.direction = "right"
            else:
                self.goto(current_x - 24, current_y)
        elif self.direction == "up":
            if (current_x, current_y + 24) in Mauerliste or current_y + 24 > 288:
                self.direction = "down"
            else:
                self.goto(current_x, current_y + 24)
        elif self.direction == "down":
            if (current_x, current_y - 24) in Mauerliste or current_y - 24 < -288:
                self.direction = "up"
            else:
                self.goto(current_x, current_y - 24)


def Anzeige(x):
    turtle.clear()
    turtle.penup()
    turtle.goto(-290, 300)
    turtle.pendown()
    turtle.color("white")
    turtle.write("Gold: " + str(x), font=("Verdana", 15, "normal"))

    turtle.penup()
    turtle.goto(-150, 300)
    turtle.pendown()
    turtle.write("Level: " + str(current_level), font=("Verdana", 15, "normal"))

    # Display Leben
    turtle.penup()
    turtle.goto(200, 300)
    turtle.pendown()
    if lives == 1:  # Wenn nur noch ein Leben übrig: rot anzeiggen
        turtle.color("red")
    else:
        turtle.color("white")
    turtle.write("Leben: " + str(lives), font=("Verdana", 15, "normal"))

    turtle.hideturtle()


# Levels

Levelliste = [""]  # dummy-wert?

# Example levels
Level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP XXXXXXXXXXXXXXXXXXXXXX",
"X  XXXXXXXXXXXXXXXXXXXXXX",
"X   T   XXXXXXXXXXXXXXXXX",
"XXXXXX  XXXXXXX    XXXXXX",
"XXXXXX  XXXXXXX    XXXXXX",
"XXXXXX     XXXX  K XXXXXX",
"XXXXXXXXX  XXXX    XXXXXX",
"XXXXXXXXXE XXXX  M XXXXXX",
"XXXXXXXXX  XXXX    XXXXXX",
"XXXXXXXXX   XXXDXXXXXXXXX",
"XXXXXXXXXXX     T XXXXXXX",
"XXXXXXXXXXX  XXXXXXXXXXXX",
"XXXXXXXXXXX   XXXXXXXXXXX",
"XXXXXXX       XXXXXXXXXXX",
"XXXXXXXXXXXX  XXXXXXXXXXX",
"XXXXXXXXXXXX  XXXXXXXXXXX",
"XXXXXXXXXXXXX  XXXXXXXXXX",
"XXXXXXXXXXXXX  XXXXXXXXXX",
"XXXXXXXXXXXXX  XXXXXXXXXX",
"XXXXXXXXXXXXX  XXXXXXXXXX",
"XXXXXXXX  M     XXXXXXXXX",
"XXXXXXXXXXXXX AXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX"
]

Level_2 = [
"XXXXXXXXXXXXXXXXXXXXX",
"XTTT   M    XXX X XPX",
"XDXXXXXXX XXX XXX X X",
"X   X            EX X",
"XXX XXX XXXXX X XXX X",
"X   X     X   X X   X",
"XXX X X XXX X XXXXX X",
"X   X X   X X  TT   X",
"X XXX XXXXXXXXXXX XXX",
"X              MX   X",
"XXX X XXXXX XXXXXXX X",
"X X X   X    MX   X X",
"X X X X XXXXX X X X X",
"X   X X X X   X X X X",
"X X X X X X X X X XXX",
"XTX X X X   X   X   X",
"XXXXX X XXXXXXXXX X X",
"X     X X X   X  MXDX",
"X XXXXXXX XXX X XXX X",
"XKX           X    AX",
"XXXXXXXXXXXXXXXXXXXXX",
]

Level_3 = [
"XXXXXXXXXXXXXXXXXXXXX",
"X   X X X       X XTX",
"X X X X XXX X XXX X X",
"X X X       X X     X",
"X X X XXXXXXX XXXXX X",
"XPX      MXT   MX   X",
"XXX XXX XXXXXXXXXXX X",
"X   X   X X         X",
"X X XXXXX XXX XXXXX X",
"X X X   X      MX   X",
"X XXX X XXX XXXXX X X",
"X X   X         X X X",
"X XXX X XXXXX XXXXX X",
"X   MX X   X X  M T X",
"X XXX XXX X X XXXXXXX",
"X X   X X X      MX X",
"X XXX X X XXXDXXX X X",
"X X   X     X  MX X X",
"X XXXXX XXXXXDXXX X X",
"X  T MX XA     MX   X",
"XXXXXXXXXXXXXXXXXXXXX",
]

Level_4 = [
"XXXXXXXXXXXXXXXXXXXXX",
"X P   E X X   XT    X",
"XXX XXXXX X X XXXXX X",
"XTX M       XTX     X",
"X XXX X XXXXXXX X X X",
"X X   X       X X X X",
"X X XXXXX X X XXX XXX",
"X X     X X X   X X X",
"X XXXXX XMXXX XXX XKX",
"X     X X X X     X X",
"X XXX X XXX X XXXXX X",
"X   X     X     X X X",
"XXX XXX XXX XXX X X X",
"X     X X     X     X",
"XXX XXX XXXXX XXXXXDX",
"X   X   X X       X X",
"XXX XXXXX XXX XXXXX X",
"X   X X   X       XDX",
"X X X XXX XXX X XXX X",
"X X        TX X   XAX",
"XXXXXXXXXXXXXXXXXXXXX"
]

Levelliste.append(Level_1)
Levelliste.append(Level_2)
Levelliste.append(Level_3)

Schatzliste = []
Mauerliste = []
EyeListe   = []
AusgangListe = []
KeyListe   = []
DoorListe  = []
MonsterListe = [] 


Stein = Mauer()
Stein.hideturtle()
player = Spieler()

def Start(level_index):
    global Schatzliste, Mauerliste, EyeListe, AusgangListe, KeyListe, DoorListe, MonsterListe

    # Alte Locations löschen
    Schatzliste = []
    Mauerliste = []
    EyeListe   = []
    AusgangListe = []
    KeyListe   = []
    DoorListe  = []
    for monster in MonsterListe:
        monster.hideturtle() 
        del monster
    MonsterListe = []

    Stein.clearstamps()

    n = Levelliste[level_index]

    for y in range(len(n)):
        for x in range(len(n[y])):
            character = n[y][x]
            screen_x = -288 + (x * 24)
            screen_y =  288 - (y * 24)

            if character == "X":
                Mauerliste.append((screen_x, screen_y))
            elif character == "P":
                player.goto(screen_x, screen_y)
            elif character == "T":
                Schatzliste.append(Schatz(screen_x, screen_y))
            elif character == "E":
                EyeListe.append(Eye(screen_x, screen_y))
            elif character == "A":
                AusgangListe.append(Ausgang(screen_x, screen_y))
            elif character == "K":
                KeyListe.append(Key(screen_x, screen_y))
            elif character == "D":
                DoorListe.append(Door(screen_x, screen_y))
            elif character == "M":
                MonsterListe.append(Monster(screen_x, screen_y))

# Neuzeichnen

def redraw_scene():
    global view_radius
    Stein.clearstamps()

    # Mauern
    for (wx, wy) in Mauerliste:
        dist = math.hypot(player.xcor() - wx, player.ycor() - wy)
        if dist < view_radius:
            Stein.goto(wx, wy)
            Stein.stamp()

    # Schatz/Gold
    for schatz in Schatzliste:
        d_schatz = math.hypot(player.xcor() - schatz.xcor(),
                              player.ycor() - schatz.ycor())
        if d_schatz < view_radius:
            schatz.showturtle()
        else:
            schatz.hideturtle()

    # Auge
    for eye in EyeListe:
        d_eye = math.hypot(player.xcor() - eye.xcor(),
                          player.ycor() - eye.ycor())
        if d_eye < view_radius:
            eye.showturtle()
        else:
            eye.hideturtle()

    # Schlüüsel
    for k in KeyListe:
        d_key = math.hypot(player.xcor() - k.xcor(),
                          player.ycor() - k.ycor())
        if d_key < view_radius:
            k.showturtle()
        else:
            k.hideturtle()

    # Tür
    for d in DoorListe:
        d_door = math.hypot(player.xcor() - d.xcor(),
                            player.ycor() - d.ycor())
        if d_door < view_radius:
            d.showturtle()
        else:
            d.hideturtle()

    # Ausgang
    for aus in AusgangListe:
        d_aus = math.hypot(player.xcor() - aus.xcor(),
                          player.ycor() - aus.ycor())
        if d_aus < view_radius:
            aus.showturtle()
        else:
            aus.hideturtle()

    # Monsters
    for monster in MonsterListe:
        d_monster = math.hypot(player.xcor() - monster.xcor(),
                              player.ycor() - monster.ycor())
        if d_monster < view_radius:
            monster.showturtle()
        else:
            monster.hideturtle()

# 11) GO TO NEXT LEVEL (HELPER FUNCTION)

def go_to_next_level():
    global current_level, lives
    current_level += 1
    lives = 3
    player.hasKey = False
    player.gold = 0
    if current_level < len(Levelliste):
        print(f"Moving to level {current_level} ...")
        Start(current_level)
    else:
        print("No more levels! You won!")
        turtle.bye()

# 12) KEYBINDINGS

turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")


# 13) MAIN LOOP

Fenster.tracer(0)

Start(current_level)

while True:
    # Kollision mit Schatz
    for schatz in Schatzliste:
        if player.kollision(schatz):
            player.gold += schatz.gold
            print("Player Gold:", player.gold)
            schatz.destroy()
            Schatzliste.remove(schatz)
            break

    # Kollision mit dem Auge: größeres Sichtfeld
    for eye in EyeListe:
        if player.kollision(eye):
            view_radius += eye.extension
            print(f"Collected Eye! New radius = {view_radius}")
            eye.destroy()
            EyeListe.remove(eye)
            break

    # Kollision mit Schlüssel
    for k in KeyListe:
        if player.kollision(k):
            print("Collected the Key!")
            player.hasKey = True
            k.destroy()
            KeyListe.remove(k)
            break

    # Bedinung: Spieler braucht Schlüssel um ins nächste Level zu kommen
    for aus in AusgangListe:
        if player.kollision(aus):
            if player.hasKey:
                print("Using the key to open final door & go next level.")
                aus.destroy()
                AusgangListe.remove(aus)
                go_to_next_level()
            else:
                print("Need the key to open the final exit!")
            break
    
    for monster in MonsterListe:
        
        if player.kollision(monster):
            lives -= 1
            print("Du wurdest von einem Monster getroffen! Du hast nur noch so viel Leben: ", lives)
            if lives == 0:
                print("Game Over!")
                turtle.penup()
                turtle.goto(0, 0)
                turtle.color("red")
                turtle.write("Game Over", align="center", font=("Arial", 40, "normal"))
                turtle.done() 
            else:
                # Spieler wird um 24 Pixel nach unten versetzt
                player.goto(player.xcor(), player.ycor() - 24) 
            break 


    for monster in MonsterListe:
        monster.move()

    Anzeige(player.gold)

    redraw_scene()

    Fenster.update()
     # Geschwindigkeit des Monsters
    if current_level == 1:
        time.sleep(0.1) 
    if current_level == 2:
        time.sleep(0.08)
    if current_level == 3:
        time.sleep(0.06)
    if current_level == 4:
        time.sleep(0.05)