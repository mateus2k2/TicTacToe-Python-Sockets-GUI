    def play(self, flag):
        self.buttons = []

        self.playPage = Frame(self)
        self.playPage.pack()
        self.playPage.pack_propagate(False)
        self.playPage.configure(width=900, height=600)
        self.play = self.createCanvas(self.playPage)
        self.play.create_image(0, 0, image=self.image, anchor=NW)
        self.play.create_text(450, 100, text="Jogando", font=("Impact", 15), fill = "white")
        
        self.simbolo = ""
        self.simboloInt = getSimbolo()

        if(self.simboloInt == 0):
            self.simbolo = "X"
        else:
            self.simbolo = "O"

        self.turn = getTurn()

        if self.turn == 'PLAY': 
            for i in range(9):
                button = Button(self.play, width=10, height=5, command=lambda i=i: self.turnPlay(i))
                button.grid(row=i//3, column=i%3)
                self.buttons.append(button)
        
        elif self.turn == 'WAIT':
            self.turnWait()