import tkinter as tk
import random

class EuroDiffusion:
    def __init__(self, size):
        self.size = size
        self.grid = [[{'coins': [0] * size} for _ in range(size)] for _ in range(size)]
        
        # Initialize with some random distribution of coins
        for i in range(size):
            for j in range(size):
                self.grid[i][j]['coins'][random.randint(0, size - 1)] = random.randint(1, 10)
    
    def step(self):
        new_grid = [[{'coins': [0] * self.size} for _ in range(self.size)] for _ in range(self.size)]
        
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    if self.grid[i][j]['coins'][k] > 0:
                        diffused_amount = self.grid[i][j]['coins'][k] // 4
                        if i > 0:
                            new_grid[i - 1][j]['coins'][k] += diffused_amount
                        if i < self.size - 1:
                            new_grid[i + 1][j]['coins'][k] += diffused_amount
                        if j > 0:
                            new_grid[i][j - 1]['coins'][k] += diffused_amount
                        if j < self.size - 1:
                            new_grid[i][j + 1]['coins'][k] += diffused_amount
                        
                        new_grid[i][j]['coins'][k] += self.grid[i][j]['coins'][k] - diffused_amount * 4
        
        self.grid = new_grid

    def convert_to_currency(self, euros, currency):
        exchange_rates = {
            'USD': 1.1,
            'INR': 90,
            'GBP': 0.85,
            'JPY': 140,
            'AUD': 1.6
        }
        if currency in exchange_rates:
            return euros * exchange_rates[currency]
        else:
            raise ValueError(f"Exchange rate for {currency} not defined.")

class EuroDiffusionApp:
    def __init__(self, root, size=5):
        self.root = root
        self.size = size
        self.simulation = EuroDiffusion(size)
        
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()
        
        self.start_button = tk.Button(root, text="Start", command=self.start_simulation)
        self.start_button.pack()
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_simulation)
        self.stop_button.pack()
        
        self.currency_var = tk.StringVar(root)
        self.currency_var.set("INR") # default currency
        self.currency_menu = tk.OptionMenu(root, self.currency_var, "USD", "INR", "GBP", "JPY", "AUD")
        self.currency_menu.pack()
        
        self.is_running = False
        self.draw_grid()
    
    def draw_grid(self):
        self.canvas.delete("all")
        cell_width = 500 // self.size
        cell_height = 500 // self.size
        
        for i in range(self.size):
            for j in range(self.size):
                x0 = j * cell_width
                y0 = i * cell_height
                x1 = x0 + cell_width
                y1 = y0 + cell_height
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                
                coins = sum(self.simulation.grid[i][j]['coins'])
                currency = self.currency_var.get()
                converted_value = self.simulation.convert_to_currency(coins, currency)
                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=f"{converted_value:.2f} {currency}")
    
    def update(self):
        if self.is_running:
            self.simulation.step()
            self.draw_grid()
            self.root.after(1000, self.update)
    
    def start_simulation(self):
        if not self.is_running:
            self.is_running = True
            self.update()
    
    def stop_simulation(self):
        self.is_running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = EuroDiffusionApp(root)
    root.mainloop()
