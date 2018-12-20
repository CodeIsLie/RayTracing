from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk, ImageDraw
from space_model import *


class WorkArea:

    DEFAULT_WIDTH = 500
    DEFAULT_HEIGHT = 500

    def __init__(self):
        self.root = Tk()
        self.root.title("Ray Tracing")
        self.root.resizable(False, False)

        self.model = SpaceModel.get_scene()

        self.canvas = Canvas(self.root, bg='white', width=self.DEFAULT_WIDTH, height=self.DEFAULT_WIDTH)
        self.canvas.grid(row=1, columnspan=10)
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.redraw()
        self.root.mainloop()


    def erase(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)

    def redraw(self):
        # use model
        self.erase()
        self.model.ray_tracing(WorkArea.DEFAULT_WIDTH, WorkArea.DEFAULT_HEIGHT)

        # Ray tracing call
        pixels = self.model.pixels
        for x in range(self.image.width):
            for y in range(self.image.height):
                self.draw.point([(x, y)], pixels[x][y])

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')


gui = WorkArea()