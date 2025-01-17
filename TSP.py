import tkinter as tk
from math import sqrt
from PIL import Image, ImageTk

# Global parameters
D = 100
lgMin = float('inf')
trMin = [0] * D
lg = 0
tr = [0] * D
ad = [[0] * D for _ in range(D)]
vis = [False] * D
coords = [] # List to store city coordinates
n = 0 # Number of cities

def display_message(message):
    text_y = 20 # Starting position for message
    messages = canvas.find_withtag("messages")
    if messages:
        # Move the previous message up
        for msg in messages:
            x1, y1, x2, y2 = canvas.bbox(msg)
            canvas.move(msg, 0, -20)

    canvas.create_text(10, text_y, anchor="nw", text=message, fill="black", tags="messages", font=("Times New Roman", 12))

def calculate_distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def greedy():
    global lg, lgMin, tr, trMin, vis, n
    if n < 2:
        display_message("You need to select at least two cities.")
        return

    vis = [False] * (n + 1)
    lg = 0
    tr[1] = 1
    vis[1] = True

    for i in range(2, n + 1):
        current = tr[i - 1]
        next_city = -1
        min_cost = float('inf')

        for j in range(2, n + 1):
            if not vis[j] and ad[current][j] > 0 and ad[current][j] < min_cost:
                min_cost = ad[current][j]
                next_city = j

        if next_city == -1:
            display_message("No valid route was found.")
            return

        tr[i] = next_city
        vis[next_city] = True
        lg += min_cost

    if ad[tr[n]][1] == 0:
        display_message("No valid route was found.")
        return

    lg += ad[tr[n]][1]

    for i in range(1, n + 1):
        trMin[i] = tr[i]
    lgMin = lg

def bkt(k):
    global lg, lgMin, tr, trMin, vis, n

    if k == n:
        if ad[tr[n]][tr[1]] > 0:
            cost = lg + ad[tr[n]][tr[1]]
            if cost < lgMin:
                lgMin = cost
                trMin[1:n+1] = tr[1:n+1]
    else:
        for i in range(2, n+1):
            if not vis[i]:
                vis[i] = True
                tr[k+1] = i
                lg += ad[tr[k]][i]
                if lg < lgMin:
                    bkt(k+1)
                lg -= ad[tr[k]][i]
                vis[i] = False

def dynamic_programming():
    global lgMin, trMin, n
    dp = [[float("inf")] * (1 << n) for _ in range(n)]
    previous = [[-1] * (1 << n) for _ in range(n)]
    dp[0][1] = 0

    for visited_cities in range(1, 1 << n):
        for u in range(n):
            if visited_cities & (1 << u):
                for v in range(n):
                    if not (visited_cities & (1 << v)) and ad[u + 1][v + 1] > 0:
                        new_visited_cities = visited_cities | (1 << v)
                        new_cost = dp[u][visited_cities] + ad[u + 1][v + 1]
                        if new_cost < dp[v][new_visited_cities]:
                            dp[v][new_visited_cities] = new_cost
                            previous[v][new_visited_cities] = u

    lgMin = float('inf')
    last = -1
    for i in range(1, n):
        cost = dp[i][(1 << n) - 1] + ad[i + 1][1]
        if cost < lgMin:
            lgMin = cost
            last = i

    if last == -1:
        display_message("No valid route was found.")
        return

    visited_cities = (1 << n) - 1
    trMin = [0] * (n + 2)
    for i in range(n, 0, -1):
        trMin[i] = last + 1
        last = previous[last][visited_cities]
        visited_cities ^= (1 << (trMin[i] - 1))
    trMin[1] = 1
    trMin[n + 1] = 1

    # Display the minimum route and cost
    display_message(f"Minimum route: {trMin}")
    display_message(f"Minimum cost: {lgMin}")

def draw_greedy():
    global lg, lgMin, tr, trMin, vis, n
    if n < 2:
        display_message("You need to select at least two cities.")
        return

    vis = [False] * (n + 1)
    lg = 0
    tr[1] = 1
    vis[1] = True
    lgMin = float('inf')

    greedy()

    if lgMin == float('inf'):
        display_message("No valid route was found.")
    else:
        display_message(f"Route (Greedy): {int(lgMin)}")
        display_message(' '.join(map(str, trMin[1:n + 1])))

    canvas.delete("path")
    draw_path(canvas)

def draw_backtracking():
    global lg, lgMin, tr, trMin, vis, n
    if n < 2:
        display_message("You need to select at least two cities.")
        return

    vis = [False] * (n + 1)
    lg = 0
    tr[1] = 1
    vis[1] = True
    lgMin = float('inf')

    bkt(1)

    if lgMin == float('inf'):
        display_message("No valid route was found.")
    else:
        display_message(f"Route (Backtracking): {int(lgMin)}")
        display_message(' '.join(map(str, trMin[1:n + 1])))

    canvas.delete("path")
    draw_path(canvas)

def draw_dynamic_programming():
    global lg, lgMin, tr, trMin, vis, n
    if n < 2:
        display_message("You need to select at least two cities.")
        return

    vis = [False] * (n + 1)
    lg = 0
    tr[1] = 1
    vis[1] = True
    lgMin = float('inf')

    dynamic_programming()

    if lgMin == float('inf'):
        display_message("No valid route was found.")
    else:
        display_message(f"Route (Dynamic Programming): {int(lgMin)}")
        display_message(' '.join(map(str, trMin[1:n + 1])))

    canvas.delete("path")
    draw_path(canvas)

def draw_path(canvas):
    radius = 5

    # Draw the cities
    for i, (x, y) in enumerate(coords, start=1):
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='black', tags="points")
        canvas.create_text(x, y - 10, text=str(i), fill='black', tags="points")

    # Draw the route
    if lgMin != float('inf'):
        for i in range(1, n):
            x1, y1 = coords[trMin[i] - 1]
            x2, y2 = coords[trMin[i + 1] - 1]
            canvas.create_line(x1, y1, x2, y2, fill='blue', tags="path", width=2)

        # Return route to the starting city
        x1, y1 = coords[trMin[n] - 1]
        x2, y2 = coords[trMin[1] - 1]
        canvas.create_line(x1, y1, x2, y2, fill='blue', tags="path", width=2)

def add_city(event):
    global n
    x, y = event.x, event.y
    coords.append((x, y))
    n += 1

    # Update the distance matrix
    for i in range(n):
        ad[i + 1][n] = ad[n][i + 1] = calculate_distance(coords[i][0], coords[i][1], x, y)

    draw_path(canvas)

def reset():
    global lgMin, lg, trMin, tr, vis, coords, n
    lgMin = float('inf')
    lg = 0
    trMin = [0] * D
    tr = [0] * D
    vis = [False] * D
    coords = []
    n = 0
    canvas.delete("points")
    canvas.delete("path")
    canvas.delete("messages")
    display_message("Window reset.")

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
canvas = tk.Canvas(root, width=screen_width, height=screen_height - 200)
canvas.pack()

try:
    img = Image.open("C:\\RomanEmpire.png")
    img = img.resize((1280, 800))
    background_image = ImageTk.PhotoImage(img)
    x = (screen_width - background_image.width()) // 2 
    y = (screen_height - background_image.height()) // 2 - 90

    canvas.create_image(x, y, anchor=tk.NW, image=background_image)
except Exception as e:
    print(f"Error loading image: {e}")

if __name__ == "__main__":
    # Configure the GUI window
    root.title("TSP Problem")

    # Event for adding cities
    canvas.bind("<Button-1>", add_city)

    button_greedy = tk.Button(root, text="Greedy", command=draw_greedy, 
                              font=("Algerian", 12), 
                              foreground="black", bg="beige",
                              activebackground="beige",
                              activeforeground="beige",
                              relief="raised",
                              width=15,
                              height=1,
                              border=10)
    button_greedy.pack(side=tk.LEFT, padx=30, pady=30)

    button_backtracking = tk.Button(root, text="Backtracking", command=draw_backtracking,
                                    font=("Algerian", 12), 
                                    foreground="black", bg="beige",
                                    activebackground="beige",
                                    activeforeground="beige",
                                    relief="raised",
                                    width=15,
                                    height=1,
                                    border=10)
    button_backtracking.pack(side=tk.LEFT, padx=30, pady=30)

    button_dynamic = tk.Button(root, text="Dynamic Prog.", command=draw_dynamic_programming,
                                font=("Algerian", 12),
                                foreground="black", bg="beige",
                                activebackground="beige",
                                activeforeground="beige",
                                relief="raised",
                                width=15,
                                height=1,
                                border=10)
    button_dynamic.pack(side=tk.LEFT, padx=30, pady=30)

    # Add reset button
    button_reset = tk.Button(root, text="Reset", command=reset,
                              font=("Algerian", 12), 
                              foreground="black", bg="beige",
                              activebackground="beige",
                              activeforeground="beige",
                              relief="raised",
                              width=15,
                              height=1,
                              border=10)
    button_reset.pack(side=tk.LEFT, padx=30, pady=30)

    root.mainloop()