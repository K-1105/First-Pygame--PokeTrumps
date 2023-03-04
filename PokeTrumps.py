import random
import shutil  # for badge images
import pygame
import urllib.request  # urllib to get info from URLs (in this case get the pictures that are .png files)
import requests  # for JSON requests
from PIL import Image
from pygame import mixer  # used for music
import Button  # A homemade module saved in the project to define making a button <<
import Typewriter  # A homemade module saved in the project to define making the questions type-out <<
import os.path  # To check if any of the urllib files have been loaded before

# getting some settings in before the defs and game loop--------------------------------------------------------------
pygame.init()

# create window with set size and title caption
SCREEN_WIDTH = 1600  # Constants (as opposed to variables we plan on changing) are usually in CAPS
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PokeTrumps")

# define fonts (may change these later)
large_font = pygame.font.SysFont("twcen", 100)
small_font = pygame.font.SysFont("twcen", 50)
card_font = pygame.font.SysFont("twcen", 25)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Some gameplay variables
rounds = 0
user_score = 0
computer_score = 0
draws = 0
gym_badge = 0
session_pokemon = []
badge_canvass = Image.new("RGBA", (8 * 750, 200), (255, 255, 255, 0))
badge_places = Image.new("RGBA", (8 * 100, 100), (255, 255, 255, 0))


# Some defs to use-----------------------------------------------------------------------------------------------------

# A module to draw/render text onto the screen (aka surface) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def draw_text(text, font, rgb, x, y):
    text_img = font.render(text, True, rgb)  # make a rendered version of the text
    screen.blit(text_img, (x, y))  # blit is the command to make stuff appear on the screen
    pygame.display.update()  # need to manually update whenever we add something


# A module to 'clear' the current screen by overriding with black then putting backdrop on top again . . . . . . . . . .
def clear_screen(update=None):
    # Choose whether it will update at te end by leaving () blank for 'don't update' or anything for 'do update' eg (1)
    screen.fill(BLACK)
    screen.blit(backdrop, (0, 0))
    screen.blit(logo_small, (650, 20))
    # Put badge header in if any badges collected
    if user_score >= 1:
        badge_header = pygame.image.load("Poketrumps assets/Badge Silhouettes.png")
        screen.blit(badge_header, (950, 20))
        badge_images(screen)
    if update is not None:
        pygame.display.update()


# random pokemon generator . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def random_pokemon():
    pokemon_number = random.randint(1, 151)
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon_number)
    response = requests.get(url)
    pokemon = response.json()

    return {
        'name': pokemon['name'],
        'id': pokemon['id'],
        'height': pokemon['height'],
        'weight': pokemon['weight'],
    }


# Turn pngs with transparent backgrounds into silhouettes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def make_silhouette(img_output_name, img_url=None, img_file=None):
    if img_url is not None:
        urllib.request.urlretrieve(img_url, "Temp/not silhouette.png")
        silhouette = Image.open("Temp/not silhouette.png")
    elif img_file is not None:
        silhouette = img_file
    silhouette = silhouette.convert("RGBA")
    datas = silhouette.getdata()

    newData = []
    for item in datas:
        if item[3] != 0:  # if the A part of RGBA is not 0, ie alpha != 0 ie transparent
            newData.append((0, 0, 0, 255))  # make the pixles black and opaque
        else:
            newData.append(item)

    silhouette.putdata(newData)
    silhouette.save(img_output_name)


# Badge info . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
badge_name = ['Boulder badge', 'Cascade badge', 'Thunder badge', 'Rainbow badge', 'Soul badge', 'Marsh badge',
              'Volcano badge', 'Earth badge']

badge_url = ['https://static.wikia.nocookie.net/pokemon/images/2/24/Boulderbadge.png',
             'https://static.wikia.nocookie.net/pokemon/images/4/4d/Cascadebadge.png',
             'https://static.wikia.nocookie.net/pokemon/images/a/a8/Thunderbadge.png',
             'https://static.wikia.nocookie.net/pokemon/images/b/b5/Rainbow_Badge.png',
             'https://static.wikia.nocookie.net/pokemon/images/6/64/Soulbadge.png',
             'https://static.wikia.nocookie.net/pokemon/images/1/1c/Marshbadge.png',
             'https://static.wikia.nocookie.net/pokemon/images/d/d9/Volcanobadge.png',
             'https://static.wikia.nocookie.net/pokemon/images/c/cc/Earthbadge.png']


def badge_images(surface):
    global badge_name, gym_badge, img, badge_canvass
    i = gym_badge
    my_url = badge_url[i]
    response = requests.get(my_url, stream=True)

    with open('Temp/my_image.png', 'wb') as file:
        shutil.copyfileobj(response.raw, file)
    del response

    img = Image.open('Temp/my_image.png')
    resized_img = img.resize((80, 80))
    resized_img.save("Temp/resized_image.png")

    badge_canvass.paste(resized_img, (i * 80, 0))
    badge_canvass.save("Temp/Badge Collection.png")
    badge_collection = pygame.image.load("Temp/Badge Collection.png")
    surface.blit(badge_collection, (950, 20))


# Silhouetted badge placeholders
def badge_placeholders():
    url_number = 1
    for urls in badge_url:
        urllib.request.urlretrieve(urls, "Temp/Badge {}.png".format(url_number))
        url_number += 1

    badge1 = Image.open("Temp/Badge 1.png")
    badge2 = Image.open("Temp/Badge 2.png")
    badge3 = Image.open("Temp/Badge 3.png")
    badge4 = Image.open("Temp/Badge 4.png")
    badge5 = Image.open("Temp/Badge 5.png")
    badge6 = Image.open("Temp/Badge 6.png")
    badge7 = Image.open("Temp/Badge 7.png")
    badge8 = Image.open("Temp/Badge 8.png")
    new_badge_size = (80, 80)
    badge1_small = badge1.resize(new_badge_size)
    badge2_small = badge2.resize(new_badge_size)
    badge3_small = badge3.resize(new_badge_size)
    badge4_small = badge4.resize(new_badge_size)
    badge5_small = badge5.resize(new_badge_size)
    badge6_small = badge6.resize(new_badge_size)
    badge7_small = badge7.resize(new_badge_size)
    badge8_small = badge8.resize(new_badge_size)

    small_badges = [
        badge1_small, badge2_small, badge3_small, badge4_small, badge5_small, badge6_small, badge7_small, badge8_small
                    ]

    badge_silouhette_number = 1
    for b in small_badges:

        make_silhouette("Temp/Badge silhouette {}.png".format(badge_silouhette_number), None, b)
        img = Image.open("Temp/Badge silhouette {}.png".format(badge_silouhette_number))
        badge_places.paste(img, ((badge_silouhette_number-1) * 80, 0))
        badge_places.save("Poketrumps assets/Badge Silhouettes.png")
        badge_silouhette_number += 1


# Fight cloud blits. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def cloud_dissipate(img, music, message, pokemon, message2=None, pokemon2=None, message3=None, img2=None):
    cloud_alphas = [255, 150, 100, 50]
    for a in cloud_alphas:
        clear_screen()
        if img2 is None:                    # Image of the winner behind the cloud
            screen.blit(img, (550, 400))
        else:                               # Image of two Pokémon if there is a draw
            screen.blit(img, (350, 400))
            screen.blit(img2, (750, 400))
        cloud.set_alpha(a)
        screen.blit(cloud, (300, 100))
        pygame.display.update()
        pygame.time.wait(300)

    mixer.music.load(music)
    mixer.music.set_volume(0.1)
    mixer.music.play(5, 0, 0)

    clear_screen()
    screen.blit(img, (550, 400))
    pygame.display.update()
    pygame.time.wait(300)
    Typewriter.type(message.format(pokemon['name'].title()), 100, 120, screen)
    if message2 is not None:
        Typewriter.type(message2.format(pokemon2['name'].title()), 100, 180, screen)
    if message3 is not None:
        Typewriter.type(message3.format(pokemon1['name'].title(), pokemon2['name'].title()), 100, 180, screen)


#  Start of main loop---------------------------------------------------------------------------------------------------
def run():
    global rounds, user_score, computer_score, draws, badge_name, gym_badge, img, badge_canvass, session_pokemon, \
        badge_header
    rounds += 1

    clear_screen(1)
    Typewriter.type(" Round: {} ".format(rounds), 100, 40, screen)

    # Choose the random pokemon then make a list of them
    my_pokemon1 = random_pokemon()
    my_pokemon2 = random_pokemon()
    opponent_pokemon1 = random_pokemon()
    opponent_pokemon2 = random_pokemon()
    all_pokemon = [my_pokemon1, my_pokemon2, opponent_pokemon1, opponent_pokemon2]

    # Session pokemon list: Append each item found in the all_pokemon list to the list for the whole session
    for a in range(0, len(all_pokemon)):
        session_pokemon.append(all_pokemon[a])

    # Getting the images of the pokemon from this round . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    pokemon_number = 0
    for _ in all_pokemon:
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{}.png"
            .format(all_pokemon[pokemon_number]['id']),
            "Temp/{}.png".format(pokemon_number))  # asking to identify the .png in this URL "pokemon1.png"
        pokemon_number += 1

    img1_orig = pygame.image.load("Temp/0.png")
    img2_orig = pygame.image.load("Temp/1.png")
    img3_orig = pygame.image.load("Temp/2.png")
    img4_orig = pygame.image.load("Temp/3.png")
    img_scale = 0.35  # The are a bit big so rescale
    img1 = pygame.transform.smoothscale(img1_orig, (475 * img_scale, 475 * img_scale))
    img2 = pygame.transform.smoothscale(img2_orig, (475 * img_scale, 475 * img_scale))
    img3 = pygame.transform.smoothscale(img3_orig, (475 * img_scale, 475 * img_scale))
    img4 = pygame.transform.smoothscale(img4_orig, (475 * img_scale, 475 * img_scale))

    Typewriter.type(" You were given...", 100, 130, screen)

    # 1st of my pokecards . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    pokecard_xcoord = 100
    pokecard_ycoord = 200
    Typewriter.type(" You were given...", pokecard_xcoord, 130, screen)
    screen.blit(pokecard, (pokecard_xcoord, pokecard_ycoord))
    screen.blit(img1, (pokecard_xcoord + 70, pokecard_ycoord + 40))
    draw_text("{}".format(my_pokemon1['name'].title()), card_font, BLACK, pokecard_xcoord + 70, pokecard_ycoord + 15)
    draw_text("ID number: {}".format(my_pokemon1['id']), card_font, BLACK, pokecard_xcoord + 30, pokecard_ycoord + 220)
    draw_text("Height:      {}".format(my_pokemon1['height']), card_font, BLACK, pokecard_xcoord + 30,
              pokecard_ycoord + 250)
    draw_text("Weight:     {}".format(my_pokemon1['weight']), card_font, BLACK, pokecard_xcoord + 30,
              pokecard_ycoord + 280)
    pygame.display.update()
    pygame.time.wait(1000)

    # 2nd of my pokecards
    pokecard_xcoord += 350
    Typewriter.type("or", pokecard_xcoord - 50, 400, screen)
    screen.blit(pokecard, (pokecard_xcoord, pokecard_ycoord))
    screen.blit(img2, (pokecard_xcoord + 70, pokecard_ycoord + 40))
    draw_text("{}".format(my_pokemon2['name'].title()), card_font, BLACK, pokecard_xcoord + 70, pokecard_ycoord + 15)
    draw_text("ID number: {}".format(my_pokemon2['id']), card_font, BLACK, pokecard_xcoord + 30, pokecard_ycoord + 220)
    draw_text("Height:      {}".format(my_pokemon2['height']), card_font, BLACK, pokecard_xcoord + 30,
              pokecard_ycoord + 250)
    draw_text("Weight:     {}".format(my_pokemon2['weight']), card_font, BLACK, pokecard_xcoord + 30,
              pokecard_ycoord + 280)
    pygame.display.update()

    # 1st of opponent's pokecards
    pokecard_xcoord += 400
    Typewriter.type(" Your opponent has... ", pokecard_xcoord, 130, screen)
    screen.blit(pokecard, (pokecard_xcoord, pokecard_ycoord))
    screen.blit(img3, (pokecard_xcoord + 70, pokecard_ycoord + 40))
    draw_text("{}".format(opponent_pokemon1['name'].title()), card_font, BLACK, pokecard_xcoord + 70,
              pokecard_ycoord + 15)
    draw_text("ID number: {}".format(opponent_pokemon1['id']), card_font, BLACK, pokecard_xcoord + 30,
              pokecard_ycoord + 220)
    draw_text("Height:      {}".format(opponent_pokemon1['height']), card_font, BLACK, pokecard_xcoord + 30,
              pokecard_ycoord + 250)
    draw_text("Weight:     {}".format(opponent_pokemon1['weight']), card_font, BLACK, pokecard_xcoord + 30,
              pokecard_ycoord + 280)
    pygame.display.update()

    # 2nd of opponent's pokecards
    pokecard_xcoord += 350
    Typewriter.type("or", pokecard_xcoord - 50, 400, screen)
    screen.blit(pokecard, (pokecard_xcoord, pokecard_ycoord))
    screen.blit(img4, (pokecard_xcoord + 70, pokecard_ycoord + 40))
    draw_text("{}".format(opponent_pokemon2['name'].title()), card_font, BLACK, pokecard_xcoord + 70,
              pokecard_ycoord + 15)
    draw_text("ID number: {}".format(opponent_pokemon2['id']), card_font, BLACK, pokecard_xcoord + 30,
              pokecard_ycoord + 220)
    draw_text("Height:      {}".format(opponent_pokemon2['height']), card_font, BLACK, pokecard_xcoord + 30,
              pokecard_ycoord + 250)
    draw_text("Weight:    {}".format(opponent_pokemon2['weight']), card_font, BLACK, pokecard_xcoord + 30,
              pokecard_ycoord + 280)
    pygame.display.update()

    pygame.time.wait(100)
    Typewriter.type(" Wow, what a selection, click on who you choose to battle ", 100, 700, screen)

    pokecard1_button = Button.Button_card(100, pokecard_ycoord, pokecard, RED, screen)
    pokecard2_button = Button.Button_card(450, pokecard_ycoord, pokecard, RED, screen)

    # make the game wait until a button has been pressed otherwise we'll go round the game loop continuously
    card_button_been_pressed = False
    while not card_button_been_pressed:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()

        #  Chose 1st pokemon section....................................................................................

        elif pokecard1_button.draw(screen):
            card_button_been_pressed = True
            clear_screen(1)
            competing_categories = 'id', 'height', 'weight'
            stat_choice = random.choice(competing_categories)
            my_stat = my_pokemon1[stat_choice]

            opponent_starter_pokemon = opponent_pokemon1, opponent_pokemon2
            opponent_choice = random.choice(opponent_starter_pokemon)
            opponent_stat = opponent_choice[stat_choice]

            Typewriter.type(" You chose {}! ".format(my_pokemon1['name'].title()), 100, 160, screen)
            screen.blit(img1_orig, (350, 400))
            pygame.display.update()
            Typewriter.type(" Your opponent chose {}. ".format(opponent_choice['name'].title()), 850, 160, screen)
            if opponent_choice == opponent_pokemon1:
                screen.blit(img3_orig, (750, 400))
            else:
                screen.blit(img4_orig, (750, 400))
            pygame.display.update()
            pygame.time.wait(2000)

            #  Fight section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

            Typewriter.type(" Let the battle commence ", 550, 300, screen)

            mixer.music.load("Poketrumps assets/battle.mp3")
            mixer.music.set_volume(0.1)
            mixer.music.play(0, 0, 0)

            pygame.time.wait(2000)
            clear_screen(1)

            cloud.set_alpha(255)
            screen.blit(cloud, (300, 100))
            pygame.display.update()
            pygame.time.wait(300)

            clear_screen()
            screen.blit(pygame.transform.rotate(cloud, -2), (300, 100))
            screen.blit(pygame.transform.rotate(fight_bursts[random.randint(0, len(fight_bursts) - 1)], 30), (500, 250))
            pygame.display.update()
            pygame.time.wait(500)

            clear_screen()
            screen.blit(cloud, (300, 100))
            pygame.display.update()
            pygame.time.wait(300)

            clear_screen()
            screen.blit(pygame.transform.rotate(cloud, 2), (300, 100))
            screen.blit(pygame.transform.rotate(fight_bursts[random.randint(0, len(fight_bursts) - 1)], -20),
                        (650, 300))
            pygame.display.update()
            pygame.time.wait(500)

            clear_screen()
            screen.blit(cloud, (300, 100))
            pygame.display.update()
            pygame.time.wait(300)

            clear_screen()
            screen.blit(pygame.transform.rotate(cloud, -2), (300, 100))
            screen.blit(pygame.transform.rotate(fight_bursts[random.randint(0, len(fight_bursts) - 1)], 0), (575, 500))
            pygame.display.update()
            pygame.time.wait(500)

            clear_screen()
            screen.blit(cloud, (300, 100))
            pygame.display.update()
            pygame.time.wait(300)

            clear_screen()
            screen.blit(pygame.transform.rotate(cloud, 2), (300, 100))
            screen.blit(pygame.transform.rotate(fight_bursts[random.randint(0, len(fight_bursts) - 1)], 0), (575, 300))
            pygame.display.update()
            pygame.time.wait(500)

            clear_screen()
            screen.blit(cloud, (300, 100))
            pygame.display.update()
            pygame.time.wait(300)

            Typewriter.type(" It looked like {} and {} competed using their {}. ".format(
                my_pokemon1['name'].title(),
                opponent_choice['name'].title(),
                stat_choice), 100, 120, screen)
            Typewriter.type(" But who was victorious?... ", 100, 180, screen)
            pygame.time.wait(2000)

            #  Cloud dissipate section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # Win  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            if my_stat > opponent_stat:
                cloud_dissipate(img1_orig, "Poketrumps assets/victory.mp3", " You and {} win! ", my_pokemon1,)
                pygame.time.wait(2000)

                user_score += 1
                if user_score == 1:
                    clear_screen(1)
                    Typewriter.type(" You have earned your first badge! It is the Boulder Badge! ", 100, 120, screen)
                    boulder_badge = pygame.image.load("Temp/Badge {}.png".format(user_score))
                    boulder_badge_large = pygame.transform.scale(boulder_badge, (400, 400))
                    screen.blit(boulder_badge_large, (600, 300))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    clear_screen(1)
                    badge_header = pygame.image.load("Poketrumps assets/Badge Silhouettes.png")
                    for x in range(3):      # make badges flash in placeholders this many times
                        screen.blit(badge_header, (950, 20))
                        badge_images(screen)
                        pygame.display.update()
                        pygame.time.wait(100)
                        screen.blit(badge_header, (950, 20))
                        pygame.display.update()
                        pygame.time.wait(100)
                        badge_images(screen)
                        pygame.display.update()

                elif user_score in range(1, 8):
                    i = gym_badge
                    Typewriter.type("You've just earned the {}! We've added it to your collection. "
                                    " You now have {} badges!: ".format(badge_name[i], user_score), 100, 120, screen)
                    badge_name_ycord = 120
                    for b in range(i):
                        badge_name_ycord += 60
                        Typewriter.type("{}".format(badge_name[0:i + 1]), 100, badge_name_ycord, screen)
                    badge_images(screen)
                    badge_header = pygame.image.load("Poketrumps assets/Badge Silhouettes.png")
                    screen.blit(badge_header, (950, 20))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    gym_badge += 1


            # Lose to opponent pokemon 1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            elif my_stat < opponent_stat and opponent_choice == opponent_pokemon1:
                cloud_dissipate(img3_orig, "Poketrumps assets/loss.mp3",
                                " I'm afraid {} wasn't quite up to this one. You Lose! ",
                                my_pokemon1, " {} was victorious ", opponent_pokemon1)

            # Lose to opponent pokemon 2  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            elif my_stat < opponent_stat and opponent_choice == opponent_pokemon2:
                cloud_dissipate(img4_orig, "Poketrumps assets/loss.mp3",
                                " I'm afraid {} wasn't quite up to this one. You Lose! ",
                                my_pokemon1, " {} was victorious ", opponent_pokemon2)

            # Draw to opponent pokemon 1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            elif my_stat < opponent_stat and opponent_choice == opponent_pokemon1:
                cloud_dissipate(img1_orig, "Poketrumps assets/draw.mp3", "It's a draw! ",
                                my_pokemon1, None, opponent_pokemon1, " {} and {} had the same stat! ", img3_orig)

            # Draw to opponent pokemon 2  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            elif my_stat < opponent_stat and opponent_choice == opponent_pokemon2:
                cloud_dissipate(img1_orig, "Poketrumps assets/draw.mp3", " It's a draw! ",
                                my_pokemon1, None, opponent_pokemon2, " {} and {} had the same stat! ", img4_orig)

                # elif my_stat < opponent_stat:

                #     mixer.music.load("loss.mp3")
                #     mixer.music.set_volume(0.1)
                #     mixer.music.play(5, 0, 0)
                #     print("\n\nI'm afraid {} wasn't quite up to this one.
                #     You Lose!".format(my_chosen_pokemon['name'].title()))
                #     computer_score += 1
                # else:
                #     urllib.request.urlretrieve(
                #         "https://vgmsite.com/soundtracks/pokemon-gameboy-sound-collection/eyuaeomq/
                #         133-celadon%20city.mp3", "draw.mp3")
                #     mixer.music.load("draw.mp3")
                #     mixer.music.set_volume(0.1)
                #     mixer.music.play(5, 0, 0)
                #     print("\n\nIt's a draw!")
                #     draws += 1
                # time.sleep(2)

            pygame.time.wait(10000)

        elif pokecard2_button.draw(screen):
            card_button_been_pressed = True
            clear_screen(1)
            competing_categories = 'ID', 'height', 'weight'
            stat_choice = random.choice(competing_categories)
            my_stat = my_pokemon2[stat_choice]

            opponent_starter_pokemon = opponent_pokemon1, opponent_pokemon2
            opponent_choice = random.choice(opponent_starter_pokemon)
            opponent_stat = opponent_choice[stat_choice]

            Typewriter.type(" You chose {}. ".format(my_pokemon2['name'].title()), 100, 160, screen)
            screen.blit(img2_orig, (350, 400))
            pygame.display.update()
            pygame.time.wait(1000)
            Typewriter.type(" Your opponent chose {}. ".format(opponent_choice['name'].title()), 850, 160, screen)
            if opponent_choice == opponent_pokemon1:
                screen.blit(img3_orig, (750, 400))
            else:
                screen.blit(img4_orig, (750, 400))
            pygame.display.update()

            pygame.time.wait(10000)

        #     while not button_been_pressed:
        #         event = pygame.event.wait()
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #         elif rules_yes_button.draw(screen):
        #             clear_screen()
        #             draw_text("OK, let's battle some Pokemon!!", large_font, RED, 200, 300)
        #             pygame.time.wait(2000)
        #             button_been_pressed = True
        #         elif rules_no_button.draw(screen):
        #             clear_screen()
        #             Typewriter.type(" No problem, see you next time! ", 100, 200, screen)
        #             pygame.time.wait(2000)
        #             pygame.quit()
        #
        # elif no_button.draw(screen):
        #     clear_screen()
        #     draw_text("Let's battle some Pokemon!!", large_font, RED, 250, 300)
        #     pygame.time.wait(2000)
        #     button_been_pressed = True

    # Start the original game loop run()..............................................................................
    run()

    #
    #
    #
    #
    # print("\n\nLet's check the score sheet...")
    # time.sleep(0.5)
    # print("Won: {}\nLost: {}\nDraws: {}".format(user_score, computer_score, draws))
    # time.sleep(1)
    # winning_average = int(user_score / (user_score + computer_score + draws) * 100)
    # if rounds != 1:
    #     print("\nThat's a winning average of {}% over {} rounds".format(winning_average, rounds))
    #     time.sleep(2)
    # else:
    #     print("\nThat's a winning average of {}% over {} round".format(winning_average, rounds))
    #     time.sleep(2)


#  Make some loading prompts as things can take a while to download
# Getting a background image from online but checking whether is has been loaded before first
if not os.path.exists("Poketrumps assets/backdrop.png"):
    screen.fill(BLACK)
    draw_text("LOADING BACKROUND...", small_font, WHITE, 500, 400)
    urllib.request.urlretrieve(
        "https://dylanoke.files.wordpress.com/2021/02/kanto_route_4_anime.png", "Poketrumps assets/backdrop.png")
backdrop = pygame.image.load("Poketrumps assets/backdrop.png")
backdrop = pygame.transform.scale(backdrop, (1600, 900))  # It was small so scale it to the screen

# Getting music from online
if not os.path.exists("Poketrumps assets/opening music.mp3"):
    screen.fill(BLACK)
    draw_text("LOADING MUSIC...", small_font, WHITE, 500, 400)
    draw_text("SONG 1 OF 5", small_font, WHITE, 500, 500)
    urllib.request.urlretrieve(
        "https://vgmsite.com/soundtracks/pokemon-gameboy-sound-collection/vvdpydwp/101-opening.mp3",
        "Poketrumps assets/pening music.mp3")

if not os.path.exists("Poketrumps assets/battle.mp3"):
    screen.fill(BLACK)
    draw_text("LOADING MUSIC...", small_font, WHITE, 500, 400)
    draw_text("SONG 2 OF 5", small_font, WHITE, 500, 500)
    urllib.request.urlretrieve(
        "https://vgmsite.com/soundtracks/pokemon-gameboy-sound-collection/jucncspp/115-battle%20%28vs%20trainer%29.mp3",
        "Poketrumps assets/battle.mp3")

if not os.path.exists("Poketrumps assets/victory.mp3"):
    screen.fill(BLACK)
    draw_text("LOADING MUSIC...", small_font, WHITE, 500, 400)
    draw_text("SONG 3 OF 5", small_font, WHITE, 500, 500)
    urllib.request.urlretrieve(
        "https://vgmsite.com/soundtracks/pokemon-gameboy-sound-collection/rkkmtqon/116-victory%20%28vs%20trainer%29.mp3",
        "Poketrumps assets/victory.mp3")

if not os.path.exists("Poketrumps assets/loss.mp3"):
    screen.fill(BLACK)
    draw_text("LOADING MUSIC...", small_font, WHITE, 500, 400)
    draw_text("SONG 4 OF 5", small_font, WHITE, 500, 500)
    urllib.request.urlretrieve(
        "https://vgmsite.com/soundtracks/pokemon-gameboy-sound-collection/ijviptkm/120-pokemon%20gym.mp3",
        "Poketrumps assets/loss.mp3")

if not os.path.exists("Poketrumps assets/draw.mp3"):
    screen.fill(BLACK)
    draw_text("LOADING MUSIC...", small_font, WHITE, 500, 400)
    draw_text("SONG 5 OF 5", small_font, WHITE, 500, 500)
    urllib.request.urlretrieve(
        "https://vgmsite.com/soundtracks/pokemon-gameboy-sound-collection/eyuaeomq/133-celadon%20city.mp3",
        "Poketrumps assets/draw.mp3")

# Getting a Pokecard image from online
if not os.path.exists("Poketrumps assets/pokecard.png"):
    screen.fill(BLACK)
    draw_text("LOADING ASSETS...", small_font, WHITE, 500, 400)
    urllib.request.urlretrieve(
        "https://www.pngkey.com/png/full/230-2302492_pokemon-blank-card-template-48746-stock-photography.png",
        "Poketrumps assets/pokecard.png")
pokecard = pygame.image.load("Poketrumps assets/pokecard.png")
pokecard = pygame.transform.smoothscale(pokecard, (420 * 0.7, 590 * 0.7))  # It was a bit big so rescale

# Making Badge placeholder image from URLs
if not os.path.exists("Poketrumps assets/Badge Silhouettes.png"):
    screen.fill(BLACK)
    draw_text("LOADING ASSETS...", small_font, WHITE, 500, 400)
    badge_placeholders()

# PokeTrumps logo
logo = pygame.image.load("Poketrumps assets/PokeTrumps logo.png")  # A homemade image stored in project folder <<
logo_small = pygame.transform.smoothscale(logo, (875 * 0.3, 250 * 0.3))  # Resize the logo to put as header

# Fight images
cloud = pygame.image.load("Poketrumps assets/cloud drawing.png")  # A homemade image stored in project folder <<
cloud = pygame.transform.smoothscale(cloud, (900, 900))
cloud_right = pygame.transform.rotate(cloud, 5)
cloud_left = pygame.transform.rotate(cloud, -5)

bam = pygame.image.load("Poketrumps assets/bam.png")
bang = pygame.image.load("Poketrumps assets/bang.png")
boom = pygame.image.load("Poketrumps assets/boom.png")
thwack = pygame.image.load("Poketrumps assets/thwack.png")
wow = pygame.image.load("Poketrumps assets/wow.png")
zap = pygame.image.load("Poketrumps assets/zap.png")
fight_bursts = [bam, bang, boom, thwack, wow, zap]

# Game time! Start the intro::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
running = True
while running:  # the code will try and constantly cycle this while loop unless we 'wait' (eg for a button click)

    screen.fill(BLACK)
    draw_text("STARTING...", small_font, WHITE, 665, 400)

    # Opening music (from https://downloads.khinsider.com/game-soundtracks/album/pokemon-gameboy-sound-collection)
    if mixer.music.get_busy():
        pass  # As the code might loop back to here, didn't want to load it again if already playing (ie busy == True)
    else:
        mixer.init()
        mixer.music.load("Poketrumps assets/opening music.mp3")
        mixer.music.set_volume(0.1)
        mixer.music.play(5, 0, 2000)

    pygame.time.wait(1000)

    # Display background image
    screen.blit(backdrop, (0, 0))
    pygame.display.update()
    pygame.time.wait(1000)
    # display intro logo (logo adapted from https://www.deviantart.com/supastefano/art/Pokemon-Logo-Redesign-904423671)
    draw_text("Welcome to", large_font, RED, 550, 100)
    pygame.time.wait(1000)

    screen.blit(logo, (350, 200))
    pygame.display.update()
    pygame.time.wait(2000)

    # Instructions..................................................................................................
    # Use the homemade typewriter module to display questions
    Typewriter.type(" Hello, are you ready to play? ", 465, 500, screen)

    # User the homemade button modules to create button from xy positions and text strings
    no_button = Button.Button(670, 630, " START ", WHITE, BLACK, small_font, 1, screen)
    yes_button = Button.Button(670, 730, " RULES ", WHITE, BLACK, small_font, 1, screen)
    pygame.display.update()

    # make the game wait until a button has been pressed otherwise we'll keep going round the game loop continuously
    button_been_pressed = False
    while not button_been_pressed:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
        elif yes_button.draw(screen):
            clear_screen(1)
            Typewriter.type(" In this game you will be battling a mixture of cute and fearsome ", 100, 160, screen)
            Typewriter.type(" pokemon with an opponent in an attempt to win all 8 gym badges ", 100, 215, screen)
            Typewriter.type(" and become the best poke-trainer in the land. ", 100, 270, screen)
            Typewriter.type(" All you need to do is select the pokemon you want to play with. ", 100, 345, screen)
            Typewriter.type(" Then, the pokemon with the highest number in a randomly selected ", 100, 400, screen)
            Typewriter.type(" stat (ID, Height, or Weight) will win! ", 100, 455, screen)
            Typewriter.type(" Remember to take a close look at the pokemon your opponent is ", 100, 530, screen)
            Typewriter.type(" choosing between to give yourself the best chance of victory! ", 100, 585, screen)

            rules_yes_button = Button.Button(100, 700, " I'm ready to play! ", WHITE, BLACK, small_font, 1, screen)
            rules_no_button = Button.Button(100, 800, " Actually, I don't want to play thanks ",
                                            WHITE, BLACK, small_font, 1, screen)
            pygame.display.update()
            button_been_pressed = False
            while not button_been_pressed:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif rules_yes_button.draw(screen):
                    clear_screen(1)
                    draw_text("OK, let's battle some Pokemon!!", large_font, RED, 200, 300)
                    pygame.time.wait(2000)
                    button_been_pressed = True
                elif rules_no_button.draw(screen):
                    clear_screen(1)
                    Typewriter.type(" No problem, see you next time! ", 100, 200, screen)
                    pygame.time.wait(2000)
                    pygame.quit()

        elif no_button.draw(screen):
            clear_screen(1)
            draw_text("Let's battle some Pokemon!!", large_font, RED, 250, 300)
            pygame.time.wait(2000)
            button_been_pressed = True

    # Start the original game loop run()...............................................................................
    run()

    # pygame.display.update()

    # to close game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
