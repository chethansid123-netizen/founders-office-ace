"""Dialogue for 'Friday Party': Swish Team Orders, 45 s.
Each line: (id, speaker, planned start in seconds, text).
voices.py turns this into dialogue.wav + dialogue.json (real start/end + per-frame mouth envelope per speaker).
"""

CAST = {
    # name        voice        role
    'Arjun':  ('am_michael', 'Team lead, 32'),
    'Priya':  ('af_bella',   'Product designer, 27'),
    'Neha':   ('af_nicole',  'Engineer, 26'),
    'Rahul':  ('am_adam',    'Engineer, 28'),
    'Kavya':  ('af_sarah',   'Analyst, 25'),
    'Karan':  ('am_eric',    'Sales, 31'),
    'Sneha':  ('bf_emma',    'Marketing, 29'),
    'Vikram': ('am_liam',    'Engineer, 27'),
    'Aditi':  ('af_heart',   'Design lead, 30'),
    'Rider':  ('am_puck',    'Swish rider'),
    'VO':     ('af_heart',   'Voice-over'),
}

LINES = [
    # 1 · the announcement
    ('l01', 'Arjun', 0.35, "Okay team, killer quarter. Lunch today is on me!"),
    ('l02', 'Priya', 3.45, "Ordering for nine people? That's a whole project."),
    # 2 · the idea
    ('l03', 'Neha', 6.05, "Swish has Team Orders now. One link, everyone picks."),
    ('l04', 'Arjun', 10.25, "Let's do it."),
    # 3 · the link goes to WhatsApp
    ('l05', 'Arjun', 11.85, "Done. Link's in the group."),
    # 4 · everyone orders from their own phone
    ('l06', 'Rahul', 14.30, "Chicken biryani. Obviously."),
    ('l07', 'Kavya', 16.10, "Paneer bowl for me. And they pack veg separately!"),
    ('l08', 'Karan', 18.95, "Cold coffee. Large."),
    ('l09', 'Sneha', 20.25, "Should we split the bill?"),
    # 5 · one checkout
    ('l10', 'Arjun', 21.75, "Nine orders, one bill. It's on me."),
    # 6 · downstairs
    ('l11', 'Vikram', 25.25, "Rider's downstairs already!"),
    ('l12', 'Rider', 27.35, "Team order for Arjun? Nine meals, all labelled."),
    ('l13', 'Priya', 30.05, "That was quick!"),
    ('l14', 'Rider', 31.05, "Ten minutes. Enjoy!"),
    # 7 · back upstairs, eating together
    ('l15', 'Rahul', 33.30, "Kavya, paneer bowl. Karan, your coffee."),
    ('l16', 'Aditi', 35.75, "Honestly? Easiest party ever."),
    ('l17', 'Arjun', 37.55, "Same time next Friday?"),
    # 8 · end card
    ('l18', 'VO', 40.55, "Swish Team Orders. One link. One delivery. One bill."),
]

# overlapping crowd reactions (several voices at once)
CROWD = [
    ('cheer', 2.85, [('Rahul', 'Woo!'), ('Kavya', 'Yay!'), ('Karan', 'Yes!'), ('Sneha', 'Woohoo!'), ('Vikram', 'Let\'s go!')]),
    ('yes', 38.95, [('Priya', 'Yes!'), ('Neha', 'Yes!'), ('Rahul', 'Obviously!'), ('Kavya', 'Yes please!'), ('Karan', 'Done!')]),
    ('laugh', 36.95, [('Priya', 'Ha ha!'), ('Neha', 'Ha ha ha!'), ('Karan', 'Ha!')]),
]
