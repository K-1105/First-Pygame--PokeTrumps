import random
import shutil
import subprocess  # to close the picture viewer
import sys
import time
import urllib.request  # urllib to get info from URLs (in this case get the pictures that are .png files)
import os.path  # To check if any of the urllib files have been loaded before
import requests
from PIL import Image  # image module called pillow, PIL=Python Imaging Library, class called Image
from PIL import ImageDraw  # do draw some text on our images
from PIL import ImageFont  # we will draw text on the image and edit the font
from pygame import mixer  # used for music


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


def instructions():
    print('In this game you will be battling a mixture of cute and fearsome pokemon with an opponent in an attempt '
          'to win all 8 gym badges and become the best poke-trainer in the land.\
\nAll you need to do is select the pokemon you want to play with. \
\nThen, the pokemon with the highest number in a randomly selected stat (ID, Height, or weight) will win!\
\nRemember to take a close look at the pokemon your opponent is choosing between to give yourself \
the best chance of victory!')

# *******start pic work*********
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

def badge_images():
    global badge_name, gym_badge, img, badge_canvass
    i = gym_badge
    my_url = badge_url[i]
    response = requests.get(my_url, stream=True)



    with open('my_image.png', 'wb') as file:
        shutil.copyfileobj(response.raw, file)
    del response

    img = Image.open('my_image.png')
    resized_img = img.resize((200, 200))
    resized_img.save("resized_image.png")
    #resized_img.show()

    badge_canvass.paste(resized_img, (i*200, 0))
    badge_canvass.show()
    badge_canvass.save("Badge Collection.png")


# *******end pic work**********

def run():

    global my_chosen_pokemon, rounds, user_score, computer_score, draws, badge_name, gym_badge, img, badge_canvass, session_pokemon
    rounds += 1
    print('\n\nRound:{}'.format(rounds))
    time.sleep(1)

    my_pokemon1 = random_pokemon()
    my_pokemon2 = random_pokemon()

    print(
        '\nYou were given...')

    print(
        '\n{} - ID:{}, Height:{}, Weight:{}'.format(my_pokemon1['name'].title(),  # Changed name to title case
                                                    my_pokemon1['id'],
                                                    my_pokemon1['height'],
                                                    my_pokemon1['weight'])
    )
    print(
        'and'
        '\n{} - ID:{}, Height:{}, Weight:{}'.format(my_pokemon2['name'].title(),
                                                    my_pokemon2['id'],
                                                    my_pokemon2['height'],
                                                    my_pokemon2['weight'])
    )
    time.sleep(2)

    opponent_pokemon1 = random_pokemon()
    opponent_pokemon2 = random_pokemon()
    print(
        '\nYour opponent will choose between...')
    print(
        '\n{} - ID:{}, Height:{}, Weight:{}'.format(opponent_pokemon1['name'].title(),
                                                    opponent_pokemon1['id'],
                                                    opponent_pokemon1['height'],
                                                    opponent_pokemon1['weight'])
    )
    print(
        'and'
        '\n{} - ID:{}, Height:{}, Weight:{}'.format(opponent_pokemon2['name'].title(),
                                                    opponent_pokemon2['id'],
                                                    opponent_pokemon2['height'],
                                                    opponent_pokemon2['weight'])
    )

    # ******image code start ******

    all_pokemon = [my_pokemon1, my_pokemon2, opponent_pokemon1, opponent_pokemon2]
    for a in range(0, 4):
        session_pokemon.append(all_pokemon[a])

    def multiple_images():
        pokemon_number = 0
        for _ in all_pokemon:
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{}.png"
                .format(all_pokemon[pokemon_number]['id']),
                "{}.png".format(pokemon_number))  # asking to identify the .png in this URL "pokemon1.png"
            pokemon_number += 1

        img1 = Image.open(
            "0.png")  # opening the "pokemon1.png and giving it the variable "img1" (does image stay open?)
        img2 = Image.open("1.png")
        img3 = Image.open("2.png")
        img4 = Image.open("3.png")

        # start to make a for loop to annotate the images
        all_images = [img1, img2, img3, img4]  # make a list of pokemon images
        font = ImageFont.truetype('segoeprb.ttf', 40)  # define what font we want, truetype fonts are on Windows and mac
        canvas_width = len(
            all_images) * 500  # if we wanted to add more Pokémon to the m_choices list the canvass will expand
        canvass = Image.new("RGBA", (canvas_width, 510),
                            (255, 255, 255, 0))  # making a new image with extra width canvas size with space at bottom
        image_x_coord = 0

        pokemon_text_count = 0

        def prep_img():
            img_larger = Image.new("RGBA", (500, 510), (
                255, 255, 255, 0))  # making a new image with extra space at bottom, so we can put text there
            img_larger.paste(img, (0, 0))  # pasting the img of the Pokémon on the larger, transparent canvas at origin 0

            # now add the Pokémon name to the bottom of the image too

            img_text = ImageDraw.Draw(img_larger)
            text_x_coord = (500 // 2) - (
                    len(all_pokemon[pokemon_text_count]['name']) * 17)  # each letter is approx 17px
            img_text.text((text_x_coord, 450), all_pokemon[pokemon_text_count]['name'].upper(), font=font,
                          fill=(255, 0, 0))
            # now place annotated image into large canvass
            canvass.paste(img_larger, (image_x_coord, 0))

        for img in all_images:
            prep_img()
            pokemon_text_count += 1
            image_x_coord += 500

        urllib.request.urlretrieve(
            "https://comicvine.gamespot.com/a/uploads/original/11140/111409382/7758673-0112870914-daqrp.png",
            "vs.png")
        vs_image = Image.open("vs.png")
        vs_image = vs_image.resize((162, 138))
        canvass.paste(vs_image, (920, 380), vs_image)

        canvass_text = ImageDraw.Draw(canvass)
        canvass_text.text((465, 450), "OR", font=font, fill=(255, 0, 0))
        canvass_text.text((1475, 450), "OR", font=font, fill=(255, 0, 0))

        canvass.show()

    multiple_images()

    # ******image code end******

    while True:
        pokemon_choice = str(input(
            '\nYou can play with either {} or {} - they are both great! Which do you choose? '.format(
                my_pokemon1['name'].title(),
                my_pokemon2['name'].title())).lower())
        if pokemon_choice in [my_pokemon1['name'], my_pokemon2['name']]:
            break
        else:
            print("Oops sorry, I didn't understand '{}', try typing either {} or {}"
                  .format(pokemon_choice, my_pokemon1['name'].title(), my_pokemon2['name'].title()))

    if pokemon_choice == my_pokemon1['name']:
        my_chosen_pokemon = my_pokemon1
    elif pokemon_choice == my_pokemon2['name']:
        my_chosen_pokemon = my_pokemon2

    else:
        pass

    time.sleep(2)

    competing_categories = 'id', 'height', 'weight'
    stat_choice = random.choice(competing_categories)
    my_stat = my_chosen_pokemon[stat_choice]

    opponent_starter_pokemon = opponent_pokemon1, opponent_pokemon2
    opponent_choice = random.choice(opponent_starter_pokemon)
    opponent_stat = opponent_choice[stat_choice]
    print('\n\nGreat! Your opponent chose to play with {}.'.format(opponent_choice['name'].title()))

    # *********Versus image start************

    fighting_pokemon = [my_chosen_pokemon, opponent_choice]

    def two_images():
        pokemon_number = 0
        for _ in fighting_pokemon:
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{}.png"
                .format(fighting_pokemon[pokemon_number]['id']),
                "{}.png".format(pokemon_number))  # asking to identify the .png in this URL "pokemon1.png"
            pokemon_number += 1

        img1 = Image.open(
            "0.png")  # opening the "pokemon1.png and giving it the variable "img1" (does image stay open?)
        img2 = Image.open("1.png")

        # start to make a for loop to annotate the images
        fighting_images = [img1, img2]  # make a list of pokemon images
        font = ImageFont.truetype('segoeprb.ttf', 40)  # define what font we want, truetype fonts are on Windows and mac
        canvas_width = len(
            fighting_images) * 500  # if we wanted to add more Pokémon to the m_choices list the canvass will expand
        canvass = Image.new("RGBA", (canvas_width, 510),
                            (255, 255, 255, 0))  # making a new image with extra width canvas size with space at bottom
        image_x_coord = 0

        pokemon_text_count = 0

        def prep_img():
            img_larger = Image.new("RGBA", (500, 510), (
                255, 255, 255, 0))  # making a new image with extra space at bottom, so we can put text there
            img_larger.paste(img, (0, 0))  # pasting the img of the Pokémon on the larger, black canvas at origin 0

            # now add the Pokémon name to the bottom of the image too

            img_text = ImageDraw.Draw(img_larger)
            text_x_coord = (500 // 2) - (
                    len(fighting_pokemon[pokemon_text_count]['name']) * 17)  # each letter is approx 17px
            img_text.text((text_x_coord, 450), fighting_pokemon[pokemon_text_count]['name'].upper(), font=font,
                          fill=(255, 0, 0))
            # now place annotated image into large canvass
            canvass.paste(img_larger, (image_x_coord, 0))

        for img in fighting_images:
            prep_img()
            pokemon_text_count += 1
            image_x_coord += 500

        urllib.request.urlretrieve(
            "https://comicvine.gamespot.com/a/uploads/original/11140/111409382/7758673-0112870914-daqrp.png",
            "vs.png")
        vs_image = Image.open("vs.png")
        vs_image = vs_image.resize((162, 138))
        canvass.paste(vs_image, (420, 380), vs_image)
        canvass.show()

    two_images()

    # ********Versus image end**************

    time.sleep(2)
    print('\n\n{} and {} will be competing using their {}.'.format(
            my_chosen_pokemon['name'].title(),
            opponent_choice['name'].title(),
            stat_choice.title()))

   #music from https://downloads.khinsider.com/
    if not os.path.exists("battle.mp3"):
        urllib.request.urlretrieve("https://vgmsite.com/soundtracks/pokemon-game-boy-pok-mon-sound-complete-set-play-cd/yzmctgipnq/1-15.%20Battle%20%28Vs.%20Trainer%29.mp3", "battle.mp3")
    mixer.music.load("battle.mp3")
    mixer.music.set_volume(0.1)
    mixer.music.play(0, 0, 0 )
    print('\n\nLet the battle commence!')
    time.sleep(3)
    print('\n\n\nCRASH!')
    time.sleep(0.8)
    print('\n\n\nBANG!')
    time.sleep(0.8)
    print('\n\n\nWALLOP!')
    time.sleep(0.8)
    print('\n\n\nKAPOOOOOW!!!')
    time.sleep(1.5)
    print('\n\n.', end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print('.')
    time.sleep(0.5)

    if my_stat > opponent_stat:
        if not os.path.exists("victory.mp3"):
            urllib.request.urlretrieve(
                "https://vgmsite.com/soundtracks/pokemon-game-boy-pok-mon-sound-complete-set-play-cd/vqnnuvhutx/1-29.%20Victory%20%28Vs.%20Gym%20Leader%29.mp3",
                "victory.mp3")
        mixer.music.load("victory.mp3")
        mixer.music.set_volume(0.1)
        mixer.music.play(5, 0, 0)
        print('\n\nYou and {} win!'.format(my_chosen_pokemon['name'].title()))
        user_score += 1
        if user_score == 1:
            print('\nYou have earned your first badge! It is the Boulder Badge!')
            badge_images()
        elif user_score in range(1, 8):
            i = gym_badge
            print("\nYou've just earned the {}! We've added it to your collection. "
                  "You now have {} badges!: ".format(badge_name[i], user_score))
            print(', \n'.join(badge_name[0:i+1]))
            badge_images()
        gym_badge += 1
    elif my_stat < opponent_stat:
        if not os.path.exists("loss.mp3"):
            urllib.request.urlretrieve(
                "https://vgmsite.com/soundtracks/pokemon-game-boy-pok-mon-sound-complete-set-play-cd/cmyqgmwfdc/1-20.%20Pok%C3%A9mon%20Gym.mp3",
                "loss.mp3")
        mixer.music.load("loss.mp3")
        mixer.music.set_volume(0.1)
        mixer.music.play(5, 0, 0)
        print("\n\nI'm afraid {} wasn't quite up to this one. You Lose!".format(my_chosen_pokemon['name'].title()))
        computer_score += 1
    else:
        if not os.path.exists("draw.mp3"):
            urllib.request.urlretrieve(
                "https://vgmsite.com/soundtracks/pokemon-game-boy-pok-mon-sound-complete-set-play-cd/hjdhsxlpgp/1-33.%20Celadon%20City.mp3",
                "draw.mp3")
        mixer.music.load("draw.mp3")
        mixer.music.set_volume(0.1)
        mixer.music.play(5, 0, 0 )
        print("\n\nIt's a draw!")
        draws += 1
    time.sleep(2)

    print("\n\nLet's check the score sheet...")
    time.sleep(0.5)
    print("Won: {}\nLost: {}\nDraws: {}".format(user_score, computer_score, draws))
    time.sleep(1)
    winning_average = int(user_score / (user_score + computer_score + draws) * 100)
    if rounds != 1:
        print("\nThat's a winning average of {}% over {} rounds".format(winning_average, rounds))
        time.sleep(2)
    else:
        print("\nThat's a winning average of {}% over {} round".format(winning_average, rounds))
        time.sleep(2)


rounds = 0
user_score = 0
computer_score = 0
draws = 0
gym_badge = 0
badge_canvass = Image.new("RGBA", (8*200, 200),(255, 255, 255, 0))
session_pokemon = []


print("\n"*3,"Welcome to Poketrumps!")


while True:
    rules = input('\nDo you need to read the rules? (yes/no) ')

    answer = rules
    if rules.lower() in ['yes', 'no']:  # .lower() coverts input to right case
        break

    print("Oops sorry, I didn't understand '{}', please try again".format(rules))

if rules == 'yes':
    (instructions())
elif rules == 'no':
    pass
else:
    pass

while True:
    start = input('\n\nAre you ready to play? (yes/no) ')
    if start.lower() in ['yes', 'no']:
        break
    else:
        print("Oops sorry, I didn't understand '{}', please try again".format(start))

if start == 'yes':
    print("Let's battle some Pokemon!")     #music from https://downloads.khinsider.com/game-soundtracks/album/pokemon-gameboy-sound-collection
    if not os.path.exists("opening.mp3"):
        urllib.request.urlretrieve(
            "https://vgmsite.com/soundtracks/pokemon-game-boy-pok-mon-sound-complete-set-play-cd/vfywpihuos/1-01.%20Opening.mp3",
            "opening.mp3")
    mixer.init()
    mixer.music.load("opening.mp3")
    mixer.music.set_volume(0.1)
    mixer.music.play(5,0,2000)
elif start == 'no':
    input('No problem! Simply press enter to exit')
    sys.exit()
else:
    pass

while True:
    run()
    if gym_badge == 8:
        print("CONGRATULATIONS!! \nYou beat the game!!")
        time.sleep(0.5)
        print("You have proven yourself to be an elite trainer!")

        subprocess.run(['taskkill', '/f', '/im',
                        "Microsoft.Photos.exe"])  # closes the photo viewer
        break
    restart = input('\n\n\nAre you ready to play again? (yes/no) ')
    if restart.lower() == 'yes':
        print('\n' * 3, "Let me just close those images for you and we'll start the next round...\n\n\n")
        time.sleep(2)
        subprocess.run(['taskkill', '/f', '/im',
                        "Microsoft.Photos.exe"])  # closes the photo viewer
        time.sleep(2)
        pass
    else:
        print('\n' * 3, "Ok, just closing the images...\n\n\n")
        time.sleep(2)
        subprocess.run(['taskkill', '/f', '/im',
                        "Microsoft.Photos.exe"])  # closes the photo viewer
        time.sleep(1)
        break


mixer.music.stop()
play_wdp = input("\n\n\nWould you like to play 'Who's That Pokemon'? (yes/no) ")
time.sleep(2)
if play_wdp.lower() == 'yes':
    print('\n' * 2 , "Great! You saw {} Pokemon this session, let's see if you can guess who's silhouette this is...\n\n\n".format(len(session_pokemon)))
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'MyApp/1.0')]       # this code is because the website didnt like us scraping the file as python, we will look like a web-based program
    urllib.request.install_opener(opener)
    if not os.path.exists("who dat.mp3"):
        urllib.request.urlretrieve("https://www.myinstants.com/media/sounds/whos-that-pokemon_.mp3", "who dat.mp3",  )
    mixer.init()
    mixer.music.load("who dat.mp3")
    mixer.music.set_volume(0.1)
    mixer.music.play(0, 0, 0)
    print("That could be any of these Pokemon!" )
    suspects = []
    for a in range(0, len(session_pokemon)):
        print(session_pokemon[a]['name'])
        suspects.append(session_pokemon[a]['name'])

    whos_that = random.choice(session_pokemon)
    #print(whos_that)
    #print(whos_that['name'])
    #print(suspects)

    innocents = suspects
    innocents.remove(whos_that['name'])
    #print(innocents)
    innocents_set = set(innocents)      #converting to a set removes all duplicates
    #print(innocents_set)

    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{}.png"
        .format(whos_that['id']),
        "whos that.png")
    silhouette = Image.open("whos that.png")
    silhouette = silhouette.convert("RGBA")
    datas = silhouette.getdata()

    newData = []
    for item in datas:
        if item[3] != 0:                # if the A part of RGBA is not 0, ie alpha != 0 ie transparent
            newData.append((0, 0, 0, 255))      # make the pixles black and opaque
        else:
            newData.append(item)

    silhouette.putdata(newData)
    silhouette.save("silhouette.png")

    urllib.request.urlretrieve(
        "https://external-preview.redd.it/e5zoQw-hgw-LCjdhC_4G8IAcHxex5pzda_BD_FPTcBY.png?auto=webp&s=c0b96b5ec20010a15864b8a0c9b202c119e52fe8", "WDP background.png")
    wdp_background = Image.open("WDP background.png")
    wdp_background = wdp_background.resize((1329, 747))
    wdp_background.paste(silhouette,(150, 150),silhouette)
    wdp_background.show()

    while True:
        wdp_answer = input("\n\n\nHmmm, who do you think that could be? ")
        if wdp_answer.lower() == whos_that['name']:
            if not os.path.exists("correct.mp3"):
                urllib.request.urlretrieve(
                    "https://vgmsite.com/soundtracks/pokemon-red-blue-version-gb/wbuniqpomx/47%20Item%20Obtained.mp3", "correct.mp3")
            mixer.init()
            mixer.music.load("correct.mp3")
            mixer.music.set_volume(0.1)
            mixer.music.play(1, 0, 0)
            print("\n\n\nWELL DONE! Yes it was {}! You sure know your Pokemon.".format(whos_that['name']))
            time.sleep(2)
            print("See you next time.")
            time.sleep(1)
            print("\n\n\n...closing images...")
            subprocess.run(['taskkill', '/f', '/im',
                            "Microsoft.Photos.exe"])  # closes the photo viewer
            time.sleep(3)
            break
            pass
        elif wdp_answer.lower() in innocents_set:
            if not os.path.exists("end.mp3"):
                urllib.request.urlretrieve(
                    "https://vgmsite.com/soundtracks/pokemon-red-blue-version-gb/lelaaewkcx/52%20Pokedex%20Evaluation%20Fanfare.mp3",
                    "end.mp3")
            mixer.init()
            mixer.music.load("end.mp3")
            mixer.music.set_volume(0.1)
            mixer.music.play(1, 0, 0)
            print('\n' * 3, "Woops! I'm afraid it was {}.".format(whos_that['name']))
            time.sleep(2)
            print("\n\n\nBetter Luck next time.")
            time.sleep(1)
            print("\n\n\n...closing images...")
            subprocess.run(['taskkill', '/f', '/im',
                            "Microsoft.Photos.exe"])  # closes the photo viewer
            time.sleep(3)
            break

        else:
            print("Sorry, I didn't understand '{}' please try re-typing a name ({}) ".format(wdp_answer, suspects))
        time.sleep(2)
        pass
else:
    print('\n' * 3, "Ok, I'll just close those images before you go...\n\n\n")
    time.sleep(2)
    subprocess.run(['taskkill', '/f', '/im',
                    "Microsoft.Photos.exe"])  # closes the photo viewer
    time.sleep(2)

print('\n\n\nThanks for playing!')