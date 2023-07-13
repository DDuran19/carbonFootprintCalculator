import tkinter as tk
import tkinter.font as tkFont
import customtkinter as CTk

class CircularProgressBar:
    def __init__(self, canvas, percentage, color, rating, x=100, y=100, radius=80):
        self.fontFormattedPercentage = tkFont.Font(family="Helvetica", size=35, weight='bold')
        self.fontRating = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.color = color
        self.rating = rating
        self.canvas = canvas
        self.x, self.y = x, y
        self.tx, self.ty = x, y
        self.formattedPercentage = '{:.01f}%'.format(percentage)
        self.rating = rating

        self.radius = radius
        self.percentage = percentage

        # Draw the background circle
        self.bg_circle = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline='#95d1e6', width=11)

        # Calculate the angle based on the percentage
        angle = 359.999 * (percentage / 100)

        # Draw the progress arc
        self.progress_arc = self.canvas.create_arc(x - radius, y - radius, x + radius, y + radius, start=90,
                                                   extent=angle, style='arc', outline=self.color, width=10)

        self.label_percentage = self.canvas.create_text(self.tx, self.ty - 5, text=self.formattedPercentage,
                                                        font=self.fontFormattedPercentage)

        self.label_rating = self.canvas.create_text(self.tx, self.ty + 20, text=self.rating,
                                                    font=self.fontRating)

    def update_percentage(self, percentage):
        self.percentage = percentage
        self.formattedPercentage = '{:.0f}%'.format(percentage)

        # Calculate the angle based on the new percentage
        angle = 359.999 * (percentage / 100)

        # Update the extent of the progress arc
        self.canvas.itemconfigure(self.progress_arc, extent=angle)
        self.canvas.itemconfigure(self.label_percentage, text=self.formattedPercentage)

if __name__ == "__main__":
    # Example usage
    root = CTk.CTk()
    canvas = CTk.CTkCanvas(root, width=200, height=200, background = "red")
    canvas.pack()

    # Create a circular progress bar with an initial percentage of 100%
    progress_bar = CircularProgressBar(canvas, x=100, y=100, radius=80, percentage=100, color='red', rating="XCould be better")

    # Update the percentage to 80%
    # progress_bar.update_percentage(80)

    root.mainloop()
