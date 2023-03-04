import pygame


def type(text, x, y, surface):

    #RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    font = pygame.font.SysFont( "twcen", 50)
    text_cursor  = 0   # what length of text is shown
    text_image   = font.render( '', True, BLACK, WHITE )  # starting image
    typing_speed = 10  # milliseconds, smaller is faster
    next_update  = 0   # time (in future) next letter is added

    while True:
        clock = pygame.time.get_ticks()   # time now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        surface.blit( text_image, (x, y))

        # Is it time to type another letter
        if ( clock > next_update ):
            # Set the time for the *next* letter-add
            next_update = clock + typing_speed  # in the future
            if ( text_cursor < len( text ) ):
                # Update the text
                text_cursor += 1
                # Re-make the text-bitmap with another letter
                text_image = font.render( text[0:text_cursor], True, BLACK , WHITE)
            else:
                # The final result
                text_image = font.render(text, True, BLACK, WHITE)
                break

        pygame.display.flip()

    surface.blit(text_image, (x, y))


