import pygame
import sys
import os

pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(int(pygame.display.Info().current_w * 0.65),
                                                     int(pygame.display.Info().current_h * 0.80))

background_color = (107, 46, 16)
sky_blue = (135, 206, 235)  # Sky blue color

screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
screen.fill(background_color)

bg_image = pygame.image.load('bg.png').convert_alpha()
WIDTH, HEIGHT = bg_image.get_width(), bg_image.get_height()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.SRCALPHA)
screen.fill(background_color)

pygame.display.set_caption("The World Machine")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

font_size = 28
font = pygame.font.Font("font.ttf", font_size)

TEXT_X, TEXT_Y = 20, 18
MAX_TEXT_WIDTH = 450
MAX_TEXT_LINES = 3
FONT_SIZE_DECREASE_FACTOR = 0.84

# Semi-transparent textbox properties
TEXTBOX_WIDTH = WIDTH
TEXTBOX_HEIGHT = 40
TEXTBOX_COLOR = (135, 206, 235, 180)  # Sky blue color with less transparency
TEXTBOX_X = 0
TEXTBOX_Y = HEIGHT - TEXTBOX_HEIGHT
TEXT_COLOR = (255, 255, 255)  # White text color

user_input = ""
window_mode = pygame.NOFRAME

def find_and_replace_faces(text, face_images):
    words = text.split()
    replaced_text = ''
    image_paths = []
    for word in words:
        if word.startswith('[') and word.endswith(']'):
            face_name = word[1:-1]
            if face_name in face_images:
                image_path = face_images[face_name]
                replaced_text += ' '
                image_paths.append(image_path)
            else:
                replaced_text += word
        else:
            replaced_text += ' ' + word
    return replaced_text.strip(), image_paths

def play_text_sound():
    pygame.mixer.music.load('./text.wav')
    pygame.mixer.music.play()

def display_text(text_lines, image_paths):
    screen.fill(background_color)
    screen.blit(bg_image, (0, 0))
    y_offset = TEXT_Y
    num_lines = len(text_lines)
    font_to_use = font if num_lines <= MAX_TEXT_LINES else pygame.font.Font("font.ttf", int(font_size * (FONT_SIZE_DECREASE_FACTOR ** (num_lines - MAX_TEXT_LINES))))
    for line in text_lines:
        text_surface = font_to_use.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (TEXT_X, y_offset))
        blurred_text_surface = pygame.transform.gaussian_blur(text_surface, 1)
        screen.blit(blurred_text_surface, (TEXT_X, y_offset))
        y_offset += font_to_use.get_height()
    if image_paths:
        image = pygame.image.load(image_paths[-1])
        screen.blit(image, (496, 16))
    
    if window_mode == pygame.SHOWN:  # Only display textbox when in SHOWN mode
        # Draw semi-transparent textbox with rounded corners
        textbox_surface = pygame.Surface((TEXTBOX_WIDTH, TEXTBOX_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(textbox_surface, TEXTBOX_COLOR, (0, 0, TEXTBOX_WIDTH, TEXTBOX_HEIGHT), border_radius=10)
        screen.blit(textbox_surface, (TEXTBOX_X, TEXTBOX_Y))

        if user_input:
            input_font_size = font_size
            input_text_width = font.size(user_input)[0]
            while input_text_width > WIDTH - 20:  # Decrease font size until text fits in the textbox
                input_font_size -= 1
                font_to_use = pygame.font.Font("font.ttf", input_font_size)
                input_text_width = font_to_use.size(user_input)[0]
            text_surface = font_to_use.render(user_input, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(midleft=(20, HEIGHT - TEXTBOX_HEIGHT // 2))
            screen.blit(text_surface, text_rect)

    pygame.display.update(pygame.Rect(TEXT_X, TEXT_Y, MAX_TEXT_WIDTH, HEIGHT))

def split_text_into_lines(text):
    lines = []
    words = text.split()
    if not words:
        return lines
    current_line = words[0]
    for word in words[1:]:
        if font.size(current_line + ' ' + word)[0] < MAX_TEXT_WIDTH:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def main():
    global user_input
    global window_mode
    if len(sys.argv) != 2:
        print("Usage: python dev.py <text>")
        sys.exit(1)

    input_text = sys.argv[1]
    clock = pygame.time.Clock()
    done = False

    text_lines = []
    index = 0

    face_images = {}
    for file_name in os.listdir('./faces'):
        if file_name.endswith('.png'):
            face_name = os.path.splitext(file_name)[0]
            face_images[face_name] = os.path.join('faces', file_name)

    input_text_with_images, image_paths = find_and_replace_faces(input_text, face_images)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if window_mode == pygame.NOFRAME:
                    window_mode = pygame.SHOWN
                else:
                    window_mode = pygame.NOFRAME
                pygame.display.set_mode((WIDTH, HEIGHT), window_mode | pygame.SRCALPHA)
            elif event.type == pygame.KEYDOWN:
                if window_mode == pygame.SHOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        print("User input:", user_input)
                        user_input = ""
                    else:
                        user_input += event.unicode

        if index < len(input_text_with_images):
            text_lines = split_text_into_lines(input_text_with_images[:index + 1])
            index += 1

            if index % 3 == 0:
                play_text_sound()

        display_text(text_lines, image_paths)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
