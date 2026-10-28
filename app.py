from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'halloween-2026-new'

# ============================================================
#  ЗАДАНИЯ
# ============================================================

# TASK 1: Library — 3 монстра с описаниями
# TASK 1: Library — сопоставить картинку монстра с описанием
LIBRARY_MONSTERS = [
    {"id": "1", "name": "Witch", "image": "witch.jpg", "description": "She has got long and black hair, green eyes, a tall and thin body, and a magic ball."},
    {"id": "2", "name": "Ghost", "image": "ghost.jpg", "description": "It has got no hair, black eyes, a transparent body, and nothing in its hands."},
    {"id": "3", "name": "Zombie", "image": "zombie.jpg", "description": "It has got no hair, red eyes, a skeleton body, and rotten skin."},
    {"id": "4", "name": "Werewolf", "image": "werewolf.jpg", "description": "It has got wild and brown hair, yellow eyes, a muscular body, and long claws."},
    {"id": "5", "name": "Skeleton", "image": "skeleton.jpg", "description": "It has got no hair, black eyes, a skeleton body, and bones."},
    {"id": "6", "name": "Frankenstein", "image": "frankenstein.jpg", "description": "It has got short and green hair, black eyes, a muscular body, and chains."},
    {"id": "7", "name": "Mummy", "image": "mummy.jpg", "description": "It has got no hair, black eyes, a body covered in bandages, and bandages."},
    {"id": "8", "name": "Slimer", "image": "slimer.jpg", "description": "It has got no hair, black eyes, a short and fat body, and slime."},
    {"id": "9", "name": "Dracula", "image": "dracula.jpg", "description": "He has got short and black hair, red eyes, a tall and thin body, and a cape."},
    {"id": "10", "name": "Demon", "image": "demon.jpg", "description": "It has got no hair, red eyes, a muscular body, and horns."},
    {"id": "11", "name": "Goblin", "image": "goblin.jpg", "description": "It has got no hair, yellow eyes, a short and fat body, and big ears."}
]

# TASK 2: Kitchen — описать монстра
MONSTER_DESCRIPTIONS = {
    "name": ["Witch", "Dracula", "Zombie", "Werewolf", "Mummy"],
    "mood": ["scary", "angry", "sad", "happy", "mysterious"],
    "hair": ["long and black", "short and green", "no hair", "wild and brown", "spiky and white"],
    "eyes": ["red", "green", "yellow", "black", "glowing"],
    "body": ["tall and thin", "short and fat", "muscular", "skeleton", "covered in bandages"],
    "has_got": ["a magic ball", "long claws", "a cape", "chains", "a broomstick"]
}

CORRECT_MONSTER = {
    "name": "Witch",
    "mood": "mysterious",
    "hair": "long and black",
    "eyes": "green",
    "body": "tall and thin",
    "has_got": "a magic ball"
}

# TASK 3: Basement — найти лишнее слово
ODD_ONE_OUT = [
    {"words": ["pumpkin", "ghost", "pizza", "bat"], "answer": "pizza"},
    {"words": ["witch", "vampire", "teacher", "zombie"], "answer": "teacher"},
    {"words": ["candy", "chocolate", "broomstick", "cookie"], "answer": "broomstick"},
    {"words": ["zombie", "witch", "cauldron", "potion"], "answer": "zombie"},  # ← ИЗМЕНЕНО
    {"words": ["werewolf", "forest", "moon", "spider"], "answer": "spider"},
    {"words": ["trick or treat", "wearing costumes", "apple bobbing", "flying"], "answer": "flying"}
]

# TASK 4: Attic — There is/are (без подсказок)
ROOM_DESCRIPTION_TASKS = [
    {"prompt": "___ a big table in the room.", "answer": "There is",
     "options": ["There is", "Is there", "There are", "Are there"]},
    {"prompt": "___ three ghosts in the attic.", "answer": "There are",
     "options": ["There are", "There is", "Are there", "Is there"]},
    {"prompt": "___ a spider on the wall?", "answer": "Is there",
     "options": ["Is there", "There is", "Are there", "There are"]},
    {"prompt": "___ any bats in this room?", "answer": "Are there",
     "options": ["Are there", "There are", "Is there", "There is"]}
]

# TASK 5: Mirror Room — there is / there are / it is / they are по картинке
MIRROR_QUESTIONS = [
    {
        "item": "skull",
        "prompt": "... a skull on the shelf.",
        "options": ["It is", "There is", "There are"],
        "answer": "There is"
    },
    {
        "item": "magic orb",
        "prompt": "... a magic orb.",
        "options": ["There is", "It is", "There are"],
        "answer": "It is"
    },
    {
        "item": "witch's hat",
        "prompt": "... a witch's hat.",
        "options": ["There are", "There is", "It is"],
        "answer": "It is"
    },
    {
        "item": "2 feathers",
        "prompt": "... 2 feathers in the inkpot.",
        "options": ["It is", "There is", "They are", "There are"],
        "answer": "There are"
    },
    {
        "item": "books",
        "prompt": "... books under the desk.",
        "options": ["It is", "They are", "There is", "There are"],
        "answer": "There are"
    },
    {
        "item": "3 candles",
        "prompt": "... 3 candles.",
        "options": ["It is", "They are", "There is", "There are"],
        "answer": "They are"
    }
]

CRYPT_QUESTIONS = [
    {
        "item": "skull",
        "prompt": "___ is a skull on the shelf.",
        "options": ["This", "That", "These", "Those"],
        "answer": "That"
    },
    {
        "item": "magic orb",
        "prompt": "___ is a magic orb on the table.",
        "options": ["That", "Those", "This", "These"],
        "answer": "This"
    },
    {
        "item": "witch's hat",  # Вернули шляпу!
        "prompt": "___ is a witch's hat on the floor.",
        "options": ["These", "This", "Those", "That"],
        "answer": "That"
    },
    {
        "item": "2 feathers",
        "prompt": "___ are 2 feathers in the inkpot.",
        "options": ["That", "This", "Those", "These"],
        "answer": "These"
    },
    {
        "item": "books",
        "prompt": "___ are books under the desk.",
        "options": ["This", "That", "Those", "These"],
        "answer": "Those"
    },
    {
        "item": "3 candles",
        "prompt": "___ are 3 candles on the table.",
        "options": ["Those", "That", "These", "This"],
        "answer": "These"
    }
]

# TASK 7: Garden — Викторина про Хэллоуин
GARDEN_TASKS = [
    {
        "question": "Where did Halloween start?",
        "options": ["India", "America", "Britain", "France"],
        "answer": "Britain"
    },
    {
        "question": "What month is Halloween celebrated?",
        "options": ["September", "October", "November", "December"],
        "answer": "October"
    },
    {
        "question": "What is a witch's traditional pet?",
        "options": ["Black cat", "White rabbit", "Grey parrot", "Golden fish"],
        "answer": "Black cat"
    },
    {
        "question": "What do children say when they go door-to-door?",
        "options": ["Happy Halloween", "Trick or treat", "Give me candy", "Boo!"],
        "answer": "Trick or treat"
    },
    {
        "question": "What do people traditionally carve for Halloween?",
        "options": ["Watermelons", "Potatoes", "Pumpkins", "Apples"],
        "answer": "Pumpkins"
    }
]

ALL_INGREDIENTS = [
    "Spider Web", "Bat's Wing", "Pumpkin Dust",
    "Ghost Essence", "Shadow Crystal", "Bone Dust", "Moonflower"
]

VICTORY_STORY = """
You pour the glowing potion into the witch's cauldron...

Suddenly, the dark magic fades away! 
The witch's black hat falls off, and her scary face turns into 
a kind smile. She is not a witch anymore — she is just an old 
woman named Margaret.

"I was lonely," she says with tears in her eyes. 
"The dark magic made me evil. Thank you for saving me!"

You become friends. Margaret teaches you how to bake 
the best cookies in the world. And every Halloween, 
she gives candy to all the children in the village.

🌟 THE END — Friendship is the strongest magic! 🌟
"""


# ============================================================
# 🔧 ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def get_inventory():
    return session.get('inventory', [])


def set_inventory(inv):
    session['inventory'] = inv


def add_ingredient(item):
    inv = get_inventory()
    if item not in inv:
        inv.append(item)
        set_inventory(inv)


def rooms_visited():
    return session.get('visited', [])


def visit_room(room):
    v = rooms_visited()
    if room not in v:
        v.append(room)
    session['visited'] = v


@app.context_processor
def inject_globals():
    return {
        'inventory': get_inventory(),
        'visited': rooms_visited(),
        'all_ingredients': ALL_INGREDIENTS
    }


# ============================================================
# 🚪 РОУТЫ
# ============================================================

@app.route('/')
def start():
    session.clear()
    return render_template('start.html')


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('start'))


@app.route('/hall')
def hall():
    visit_room('hall')
    return render_template('hall.html')


@app.route('/door_room')
def door_room():
    visit_room('door_room')
    return render_template('door_room.html')


@app.route('/fireplace_room')
def fireplace_room():
    visit_room('fireplace_room')
    return render_template('fireplace_room.html')


@app.route('/library', methods=['GET', 'POST'])
def library():
    visit_room('library')
    solved = 'Spider Web' in get_inventory()

    if request.method == 'POST':
        add_ingredient('Spider Web')
        return render_template('library.html', monsters=LIBRARY_MONSTERS, solved=True)

    # Перемешиваем описания (картинки остаются в порядке)
    shuffled_descriptions = LIBRARY_MONSTERS.copy()
    random.shuffle(shuffled_descriptions)

    return render_template('library.html',
                           monsters=LIBRARY_MONSTERS,
                           shuffled_descriptions=shuffled_descriptions,
                           solved=solved)


@app.route('/kitchen', methods=['GET', 'POST'])
def kitchen():
    visit_room('kitchen')
    solved = 'Pumpkin Dust' in get_inventory()

    if request.method == 'POST':
        user_answers = {
            "name": request.form.get('name', ''),
            "mood": request.form.get('mood', ''),
            "hair": request.form.get('hair', ''),
            "eyes": request.form.get('eyes', ''),
            "body": request.form.get('body', ''),
            "has_got": request.form.get('has_got', '')
        }

        if user_answers == CORRECT_MONSTER:
            add_ingredient('Pumpkin Dust')
            return render_template('kitchen.html',
                                   descriptions=MONSTER_DESCRIPTIONS,
                                   correct_monster=CORRECT_MONSTER,
                                   solved=True)
        else:
            wrong_fields = []
            for field, correct_value in CORRECT_MONSTER.items():
                if user_answers.get(field) != correct_value:
                    wrong_fields.append(field)

            return render_template('kitchen.html',
                                   descriptions=MONSTER_DESCRIPTIONS,
                                   wrong_fields=wrong_fields,
                                   user_answers=user_answers,
                                   solved=False)

    return render_template('kitchen.html',
                           descriptions=MONSTER_DESCRIPTIONS,
                           correct_monster=CORRECT_MONSTER if solved else None,
                           wrong_fields=[],
                           user_answers={},
                           solved=solved)


@app.route('/basement', methods=['GET', 'POST'])
def basement():
    visit_room('basement')
    solved = "Bat's Wing" in get_inventory()

    if request.method == 'POST':
        all_correct = True
        for i, task in enumerate(ODD_ONE_OUT):
            user_answer = request.form.get(f'answer{i}', '').strip().lower()
            correct_answer = task['answer'].strip().lower()
            if user_answer != correct_answer:
                all_correct = False
                break

        if all_correct:
            add_ingredient("Bat's Wing")
            return render_template('basement.html', tasks=ODD_ONE_OUT, solved=True)
        else:
            return render_template('basement.html', tasks=ODD_ONE_OUT, solved=False, error="Some answers are wrong!")

    return render_template('basement.html', tasks=ODD_ONE_OUT, solved=solved)


@app.route('/attic', methods=['GET', 'POST'])
def attic():
    visit_room('attic')
    solved = 'Ghost Essence' in get_inventory()

    if request.method == 'POST':
        all_correct = True
        for i, task in enumerate(ROOM_DESCRIPTION_TASKS):
            user_answer = request.form.get(f'answer{i}', '').strip()
            if user_answer != task['answer']:
                all_correct = False
                break

        if all_correct:
            add_ingredient('Ghost Essence')
            return render_template('attic.html', tasks=ROOM_DESCRIPTION_TASKS, solved=True)

    return render_template('attic.html', tasks=ROOM_DESCRIPTION_TASKS, solved=solved)


@app.route('/mirror', methods=['GET', 'POST'])
def mirror():
    visit_room('mirror')
    solved = 'Shadow Crystal' in get_inventory()

    if request.method == 'POST':
        all_correct = True
        for i, task in enumerate(MIRROR_QUESTIONS):
            user_answer = request.form.get(f'answer{i}', '').strip()
            if user_answer != task['answer']:
                all_correct = False
                break

        if all_correct:
            add_ingredient('Shadow Crystal')
            return render_template('mirror.html', questions=MIRROR_QUESTIONS, solved=True)

    return render_template('mirror.html', questions=MIRROR_QUESTIONS, solved=solved)


@app.route('/crypt', methods=['GET', 'POST'])
def crypt():
    visit_room('crypt')
    solved = 'Bone Dust' in get_inventory()

    if request.method == 'POST':
        all_correct = True
        for i, task in enumerate(CRYPT_QUESTIONS):
            user_answer = request.form.get(f'answer{i}', '').strip()
            if user_answer != task['answer']:
                all_correct = False
                break

        if all_correct:
            add_ingredient('Bone Dust')
            return render_template('crypt.html', questions=CRYPT_QUESTIONS, solved=True)

    return render_template('crypt.html', questions=CRYPT_QUESTIONS, solved=solved)


@app.route('/garden', methods=['GET', 'POST'])
def garden():
    required = ['Spider Web', "Bat's Wing", 'Pumpkin Dust', 'Ghost Essence', 'Shadow Crystal', 'Bone Dust']
    inv = get_inventory()

    for item in required:
        if item not in inv:
            return redirect(url_for('hall'))

    visit_room('garden')
    solved = 'Moonflower' in inv

    if request.method == 'POST':
        all_correct = True
        for i, task in enumerate(GARDEN_TASKS):
            answer = request.form.get(f'answer{i}', '').strip()
            if answer != task['answer']:
                all_correct = False
                break

        if all_correct:
            add_ingredient('Moonflower')
            return render_template('garden.html', tasks=GARDEN_TASKS, solved=True)

    return render_template('garden.html', tasks=GARDEN_TASKS, solved=solved)


# Правильный порядок ингредиентов для рецепта
POTION_RECIPE = [
    "Spider Web",
    "Bat's Wing",
    "Pumpkin Dust",
    "Ghost Essence",
    "Bone Dust",
    "Shadow Crystal",
    "Moonflower"
]


@app.route('/cauldron', methods=['GET', 'POST'])
def cauldron():
    visit_room('cauldron')
    inv = get_inventory()

    missing = [item for item in ALL_INGREDIENTS if item not in inv]
    all_collected = len(missing) == 0

    if request.method == 'POST' and all_collected:
        session['victory'] = True
        return redirect(url_for('victory'))

    return render_template('cauldron.html',
                           missing=missing,
                           all_collected=all_collected,
                           inventory=inv,
                           recipe=POTION_RECIPE,
                           story=VICTORY_STORY)


@app.route('/victory')
def victory():
    if not session.get('victory'):
        return redirect(url_for('start'))
    return render_template('victory.html', story=VICTORY_STORY)


if __name__ == '__main__':
    app.run(debug=True)