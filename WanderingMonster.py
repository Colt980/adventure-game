import random


class WanderingMonster:
    def __init__(self, x, y, monster_type, color, hp):
        self.x = x
        self.y = y
        self.monster_type = monster_type
        self.color = color  # list or tuple of 3 ints
        self.hp = hp

    # ---------------- SERIALIZATION ---------------- #

    def to_dict(self):
        """Convert monster into JSON-safe dictionary."""
        return {
            "x": self.x,
            "y": self.y,
            "monster_type": self.monster_type,
            "color": list(self.color),
            "hp": self.hp
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild monster from dictionary."""
        return cls(
            data["x"],
            data["y"],
            data["monster_type"],
            data["color"],
            data["hp"]
        )

    # ---------------- SPAWNING ---------------- #

    @classmethod
    def random_spawn(cls, occupied, forbidden, grid_w, grid_h):
        """
        Create a monster at a random valid position.
        Avoids occupied + forbidden + grid bounds.
        """
        attempts = 0

        while attempts < 200:
            x = random.randint(0, grid_w - 1)
            y = random.randint(0, grid_h - 1)

            if (x, y) not in occupied and (x, y) not in forbidden:
                monster_type = random.choice(["Goblin", "Slime", "Wraith"])
                color = [
                    random.randint(50, 255),
                    random.randint(50, 255),
                    random.randint(50, 255)
                ]
                hp = random.randint(10, 40)

                return cls(x, y, monster_type, color, hp)

            attempts += 1

        # fallback (should rarely happen)
        return cls(0, 0, "Goblin", [255, 0, 0], 20)

    # ---------------- MOVEMENT ---------------- #

    def move(self, occupied, forbidden, grid_w, grid_h):
        """
        Attempt to move in a random direction.
        Must avoid:
        - other monsters (occupied)
        - forbidden tiles (player/town/etc.)
        - grid boundaries
        """

        directions = [
            (0, -1),  # up
            (0, 1),   # down
            (-1, 0),  # left
            (1, 0)    # right
        ]

        random.shuffle(directions)

        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy

            if 0 <= new_x < grid_w and 0 <= new_y < grid_h:
                if (new_x, new_y) not in occupied and (new_x, new_y) not in forbidden:
                    self.x = new_x
                    self.y = new_y
                    return  # successful move

        # if no valid move, stay in place