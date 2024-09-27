import pygame
from tkinter import *
import tkinter as tk
from tkinter import messagebox

# Define the game board
board = [
    [0],
    [1,1],
    [1,1,1],
    [1, 1, 1, 1],
    [1, 1, 1, 1, 1]
]

# Initialize Pygame
pygame.init()
pygame.mixer.init()
# Set up the Pygame window
size = width, height = 600, 600
screen = pygame.display.set_mode(size)


sound = pygame.mixer.Sound('C:/Users/Abhinaya/OneDrive/Documents/abhi/PROJECTS/hopping assassins/sound_1.mp3')
# Define colors
white = (255, 255, 255)
black = (0, 0, 0)


# create a button to show the custom message box

message_box = Tk()
message_box.geometry("1600x1600")
message_box.configure(background="purple")
message_box.title("HOPPING ASSASSINS!!!")
bg_image = PhotoImage(file="C:/Users/Abhinaya/OneDrive/Documents/abhi/PROJECTS/hopping assassins/HOPPING ASSASSINS.png")

# create a label to display the image
bg_label = Label(message_box, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

ok_button = Button(message_box, text="Start",font=((34)), command=message_box.destroy)
ok_button.pack(pady=50,side="bottom")
message_box.mainloop()

# Define the function to draw the game board
def draw_board():
    screen.fill((0,0,128))
    cell_size = 80
    for row, row_data in enumerate(board):
        for col, cell_data in enumerate(row_data):
            x0 = col * cell_size + cell_size
            y0 = row * cell_size + cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            pygame.draw.circle(screen, 'red', (x0 + cell_size // 2, y0 + cell_size // 2), cell_size // 2)
            pygame.draw.circle(screen, 'white', (x0 + cell_size // 2, y0 + cell_size // 2), cell_size // 2 - 2)
            if cell_data == 1:
                pygame.draw.circle(screen, 'red', (x0 + cell_size // 2, y0 + cell_size // 2), cell_size // 3)

# Define the function to handle the mouse click
def handle_click(pos):
    col = pos[0] // 80 - 1
    row = pos[1] // 80 - 1
    if row < len(board) and col < len(board[row]) and board[row][col] == 1:
        for d_row, d_col in [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)]:
            new_row = row + d_row
            new_col = col + d_col
            if new_row >= 0 and new_col >= 0 and new_row < len(board) and new_col < len(board[new_row]):
                if board[new_row][new_col] == 0 and board[(row + new_row) // 2][(col + new_col) // 2] == 1:
                    board[row][col] = 0
                    board[(row + new_row) // 2][(col + new_col) // 2] = 0
                    board[new_row][new_col] = 1
                    # Check if the game has been won
                    if sum(row.count(1) for row in board) == 1:
                        tk.messagebox.showinfo("Congratulations!", "You won!")
                    sound.play()
                    return True

    return False

# Main Pygame loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if handle_click(pygame.mouse.get_pos()):
                pass

    # Fill the screen with white
    screen.fill(white)
    # Draw the game board
    
    draw_board()
    

    # Update the Pygame display
    pygame.display.update()

    
