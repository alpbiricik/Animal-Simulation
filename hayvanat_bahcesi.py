import random
import math
import logging

# Sabitler
WIDTH, HEIGHT = 500, 500

# Hayvan türleri ve hareket birimleri
ANIMAL_TYPES = {
    "Koyun": {"count": 30, "move": 2},
    "Kurt": {"count": 10, "move": 3},
    "İnek": {"count": 10, "move": 2},
    "Tavuk": {"count": 10, "move": 1},
    "Horoz": {"count": 10, "move": 1},
    "Aslan": {"count": 8, "move": 4}
}

# Cinsiyetler
GENDERS = ["Erkek", "Dişi"]

# Logger ayarları
logging.basicConfig(
    filename='simulasyon.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

class Alive:
    def __init__(self, move_unit):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.move_unit = move_unit
        self.id = id(self)
    def move(self):
        angle = random.uniform(0, 2 * math.pi)
        dx = int(self.move_unit * math.cos(angle))
        dy = int(self.move_unit * math.sin(angle))
        old_x, old_y = self.x, self.y
        self.x = min(max(self.x + dx, 0), WIDTH)
        self.y = min(max(self.y + dy, 0), HEIGHT)
        return old_x, old_y, self.x, self.y
    def distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

class Animal(Alive):
    def __init__(self, animal_type, gender, move_unit):
        super().__init__(move_unit)
        self.animal_type = animal_type
        self.gender = gender
        self.alive = True

class Hunter(Alive):
    def __init__(self, move_unit=1):
        super().__init__(move_unit)
        self.animal_type = "Avcı"
    def hunt(self, animals):
        for prey in animals:
            if prey.alive and self.distance(prey) <= 8:
                prey.alive = False
                logger.info(f"Avcı {self.id}, {prey.animal_type} ({prey.gender}) {prey.id}'i avladı.")

def create_animals():
    animals = []
    for i in range(15):
        animals.append(Animal("Koyun", "Erkek", 2))
        animals.append(Animal("Koyun", "Dişi", 2))
    for i in range(5):
        animals.append(Animal("İnek", "Erkek", 2))
        animals.append(Animal("İnek", "Dişi", 2))
    for i in range(5):
        animals.append(Animal("Tavuk", "Dişi", 1))
        animals.append(Animal("Horoz", "Erkek", 1))
    for i in range(5):
        animals.append(Animal("Kurt", "Erkek", 3))
        animals.append(Animal("Kurt", "Dişi", 3))
    for i in range(4):
        animals.append(Animal("Aslan", "Erkek", 4))
        animals.append(Animal("Aslan", "Dişi", 4))
    return animals

def simulate():
    logger.info('--- Hayvanat Bahçesi Simülasyonu Başladı ---')
    animals = create_animals()
    hunter = Hunter()
    for step in range(1, 1001):
        logger.info(f"\n--- Adım {step} ---")
        # Hareket
        for animal in animals:
            if animal.alive:
                old_x, old_y, new_x, new_y = animal.move()
                logger.debug(f"{animal.animal_type} ({animal.gender}) {animal.id} ({old_x},{old_y}) -> ({new_x},{new_y}) hareket etti.")
        old_x, old_y, new_x, new_y = hunter.move()
        logger.debug(f"Avcı {hunter.id} ({old_x},{old_y}) -> ({new_x},{new_y}) hareket etti.")
        # Avlanma
        for animal in animals:
            if not animal.alive:
                continue
            if animal.animal_type == "Kurt":
                for prey in animals:
                    if prey.alive and prey.animal_type in ["Koyun", "Tavuk", "Horoz"] and animal.distance(prey) <= 4:
                        prey.alive = False
                        logger.info(f"Kurt ({animal.gender}) {animal.id}, {prey.animal_type} ({prey.gender}) {prey.id}'i avladı.")
            elif animal.animal_type == "Aslan":
                for prey in animals:
                    if prey.alive and prey.animal_type in ["İnek", "Koyun"] and animal.distance(prey) <= 5:
                        prey.alive = False
                        logger.info(f"Aslan ({animal.gender}) {animal.id}, {prey.animal_type} ({prey.gender}) {prey.id}'i avladı.")
        hunter.hunt(animals)
        # Üreme
        new_animals = []
        for i, animal1 in enumerate(animals):
            if not animal1.alive:
                continue
            for animal2 in animals[i+1:]:
                if not animal2.alive:
                    continue
                if (animal1.animal_type == animal2.animal_type and
                    animal1.gender != animal2.gender and
                    animal1.distance(animal2) <= 3):
                    gender = random.choice(GENDERS)
                    move_unit = animal1.move_unit
                    new_animal = Animal(animal1.animal_type, gender, move_unit)
                    new_animals.append(new_animal)
                    logger.info(f"{animal1.animal_type} ({animal1.gender}) {animal1.id} ile {animal2.animal_type} ({animal2.gender}) {animal2.id} üredi. Yeni: {new_animal.animal_type} ({new_animal.gender}) {new_animal.id}")
        animals.extend(new_animals)
        # Her adım sonunda hayatta kalan hayvan sayıları
        summary = {}
        for animal in animals:
            if animal.alive:
                key = f"{animal.animal_type} ({animal.gender})"
                summary[key] = summary.get(key, 0) + 1
        logger.info("\nHayatta kalanlar: " + ", ".join([f"\n {k}: {v} " for k, v in summary.items()]))
    # Sonuçları yazdır
    result = {}
    for animal in animals:
        if animal.alive:
            key = f"{animal.animal_type} ({animal.gender})"
            result[key] = result.get(key, 0) + 1
    result["Avcı"] = 1
    for k, v in result.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    simulate() 