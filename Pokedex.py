import random
import time
import requests
import urllib.request
from PIL import Image  # image module called pillow, PIL=Python Imaging Library, class called Image
from PIL import ImageDraw  # do draw some text on our images
from PIL import ImageFont  # we will draw text on the image and edit the font

#define random pokemon
def random_pokemon():
    pokemon_number = random.randint(1, 151)
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon_number)
    response = requests.get(url)
    pokemon = response.json()

    return {
        'name': pokemon['name'],
        'id': pokemon['id'],
        'height': pokemon['height'],
        'weight': pokemon['weight']
    }


# def pokemon choice code
def pokemon_choice():
    pokedex_search = input(
        "\nWhich Pokemon would you like to know more about? Simply enter their corresponding ID number here: ")
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokedex_search)
    response = requests.get(url)
    pokemon = response.json()
    return {
        'name': pokemon['name'],
        'id': pokemon['id'],
        'height': pokemon['height'],
        'weight': pokemon['weight'],
        'poke_types': pokemon['types']
    }


# define characteristic code
def random_characteristic():
    characteristic_number = random.randint(1, 35)
    characteristics = [
        'Loves to eat',
        'Proud of its power',
        'Sturdy body',
        'Grumpy in the morning',
        'Strong willed',
        'Likes to run',
        'Takes plenty of siestas',
        'Often dozes off',
        'Likes bubble baths',
        'Mischievous',
        'Somewhat vain',
        'Allergic to sarcasm',
        'Allergic to berries',
        'Loves Taylor Swift',
        'Is scared of The Muppets',
        'Sings showtunes in the shower',
        'Nods off a lot',
        'Messy little chap',
        'A little quick tempered',
        'Persistent',
        'Cunning',
        'Strongly defiant',
        'Impetuous and silly',
        'Likes to fight',
        'Loves roast dinners',
        'Often lost in thought',
        'Hates to lose',
        'Somewhat of a clown',
        'Binge watches crime dramas',
        'Quick tempered',
        'Very picky',
        'An absolute chatterbox',
        'Cowardly',
        'Believes in a pantheon of ancient gods',
        'Obsessed with becoming an influencer'
    ]
    output = characteristics[characteristic_number]
    print('Characteristic: {}'.format(output))



#start to image work - not functional yet
# def image():
#     poke_pic = pokemon_choice()
#     pokemon_number = 0
#     for _ in poke_pic:
#         urllib.request.urlretrieve(
#             "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{}.png"
#             .format(poke_pic['id']),
#             "{}.png".format(pokemon_number))  # asking to identify the .png in this URL "pokemon1.png"
#
#     img1 = Image.open(
#         "0.png")  # opening the "pokemon1.png and giving it the variable "img1"
#
#     # start to make a for loop to annotate the images
#     pokemon_images = [img1]  # make a list of pokemon images
#     font = ImageFont.truetype('segoeprb.ttf', 40)  # define what font we want, truetype fonts are on Windows and mac
#     canvas_width = len(
#         pokemon_images) * 500  # if we wanted to add more Pokémon to the m_choices list the canvass will expand
#     canvass = Image.new("RGBA", (canvas_width, 510),
#                         (255, 255, 255, 0))  # making a new image with extra width canvas size with space at bottom
#     image_x_coord = 0
#
#     pokemon_text_count = 0
#
#     def prep_img():
#         img_larger = Image.new("RGBA", (500, 510), (
#             255, 255, 255, 0))  # making a new image with extra space at bottom, so we can put text there
#         img_larger.paste(img, (0, 0))  # pasting the img of the Pokémon on the larger, black canvas at origin 0
#
#         # now add the Pokémon name to the bottom of the image too
#
#         img_text = ImageDraw.Draw(img_larger)
#         text_x_coord = (500 // 2) - (
#                 len(poke_pic[pokemon_text_count]['name']) * 17)  # each letter is approx 17px
#         img_text.text((text_x_coord, 450), poke_pic[pokemon_text_count]['name'].upper(), font=font,
#                       fill=(255, 0, 0))
#         # now place annotated image into large canvass
#         canvass.paste(img_larger, (image_x_coord, 0))
#
#     for img in pokemon_images:
#         prep_img()
#         pokemon_text_count += 1
#         image_x_coord += 500
#
#     canvass.show()


def run():
    my_pokemon1 = random_pokemon()
    my_pokemon2 = random_pokemon()
    opponent_pokemon1 = random_pokemon()
    opponent_pokemon2 = random_pokemon()

    print(
        '\nHere are all the pokemon:')

    all_pokemon = [my_pokemon1, my_pokemon2, opponent_pokemon1, opponent_pokemon2]
    for a in range(0, len(all_pokemon)):
        print(all_pokemon[a]['name'].title()) # Useful while testing, but in reality this part will come through
        # gameplay and the update pokedex section will be what is added

    def update_pokedex():
        with open('Pokedex.txt', 'a+') as f:
            for poke in range(0, len(all_pokemon)):
                f.write(str(all_pokemon[poke]["id"]))
                f.write(' - ')
                f.write(all_pokemon[poke]["name"].title())
                f.write('\n')
        lines = open('Pokedex.txt', 'r').readlines()
        lines.sort()
        lines_set = set(lines)
        out = open('Pokedex.txt', 'w')
        for line in lines_set:
            out.write(line)

    update_pokedex()


def use_pokedex():
    pokedex_go = input(
        '\nWould you like to explore information about the Pokemon you have seen using your Pokedex? (Yes/No) ')
    if pokedex_go.lower() == 'yes':
        print('Great! Here are all the Pokemon you have seen so far.\n')
    else:
        print('Thanks for playing!')
        quit()
    time.sleep(1)
    with open('Pokedex.txt') as f:
        lines = (f.readlines())
        lines.sort(key=lambda line: int(line.split()[0]))
        for line in lines[:151]:
            print(line.strip())
    time.sleep(3)
    print("\n\nYou're well on your way to being a great Poke-trainer with all this Pokemon knowledge at \
your fingertips!")
    while True:
        class color:
            PURPLE = '\033[95m'
            CYAN = '\033[96m'
            DARKCYAN = '\033[36m'
            BLUE = '\033[94m'
            GREEN = '\033[92m'
            YELLOW = '\033[93m'
            RED = '\033[91m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'
            END = '\033[0m'

        pokedex_result = pokemon_choice()
        print(
            color.BOLD + color.UNDERLINE + '\n{}'.format(pokedex_result['name'].title() + color.END))
        print('ID:{} \nHeight:{} \nWeight:{}'.format(pokedex_result['id'],
                                                                   pokedex_result['height'],
                                                                   pokedex_result['weight']
                                                                   ))
        random_characteristic()
        print('Type(s):')
        for typee in pokedex_result['poke_types']:
            print('   *{}'.format(typee['type']['name']))
        #image()
        time.sleep(2)
        cont = input('\nWould you like to search for another Pokemon? (Yes/No)')
        if cont.lower() == 'yes':
            pass
        else:
            print('Thanks for playing!')
            quit()


run()
use_pokedex()