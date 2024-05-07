import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            #All cells are mines
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            #No mines in the current set of cells recorded by the sentence
            return self.cells
        else:
            return None
      
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #If a cell is known to be a mine, remove that cell and decrease the count by one (as a mine has been taken out)
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #If a cell is safe, remove the cell from the sentence without decreasing the count
        #If this is the first time that a move is being made, dont remove it.
        # breakpoint()
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """        
        #add_knowledge should accept a cell (represented as a tuple (i, j)) and its corresponding count, and update self.mines, self.safes, self.moves_made, and self.knowledge with any new information that the AI can infer, given that cell is known to be a safe cell with count mines neighboring it.
#The function should mark the cell as one of the moves made in the game.
#The function should mark the cell as a safe cell, updating any sentences that contain the cell as well.
#The function should add a new sentence to the AI’s knowledge base, 
# based on the value of cell and count, to indicate that count of the cell’s neighbors are mines. 
# Be sure to only include cells whose state is still undetermined in the sentence.
#If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, then the function should do so.
#If, based on any of the sentences in self.knowledge, new sentences can be inferred (using the subset method described in the Background), 
# then those sentences should be added to the knowledge base as well.
#Note that any time that you make any change to your AI’s knowledge, 
# it may be possible to draw new inferences that weren’t possible before. 
# Be sure that those new inferences are added to the knowledge base if it is possible to do so.
        #1
        self.moves_made.add(cell)

        #2
        self.mark_safe(cell)

        #3
        neighboring_cells = set()
        i,j = cell

        for _i in range(i-1,i+2):
            for _j in range(j-1,j+2):
                if (_i,_j) == cell:
                    #ignore
                    continue

                if (_i,_j) in self.safes:
                    continue
                
                if (_i,_j) in self.mines:
                    #already known to be mines, ignore
                    count -= 1
                    continue
                if 0 <= _i < self.height and 0 <= _j < self.height:
                    assert _i != 8, f"i is equal to 8 or above, OUT OF BOUNDS! _i = {_i}"
                    assert _j != 8, f"j is equal to 8 or above, OUT OF BOUNDS! _j = {_j}"
                    #If cell is in bounds
                    neighboring_cells.add((_i,_j))
        #Create a new sentence
        if neighboring_cells != set():
            new_sentence = Sentence(neighboring_cells,count)
            print(f"Created new sentence {{{new_sentence.cells}}} = {new_sentence.count}")
            self.knowledge.append(new_sentence)
        else:
            print(f"Neighboring cells all in safes or mines, no new sentence created")
       

        #Consider the case of s1 - s2 = count1-count2
        changed = True


        while changed:
            #Keep iterating until no further changes are made
            if changed:
                changed = False
                
                #If changed - loop through everything again and check.
                for sentence in self.knowledge:
                    if sentence.cells == set():
                        print(f"Found empty sentence, continuing.")
                        continue
                    else:
                        new_mines = sentence.known_mines()
                        new_safes = sentence.known_safes()

                        if new_mines is not None:
                        #New mines found!
                            assert new_mines != set(), f"new_mines {new_mines} is supposed to be a full set, but instead got empty set. Sentence is {{{sentence.cells}}} = {sentence.count}"
                            print(f"New mines found: {new_mines}")
                            for mine in new_mines.copy():
                                #.copy() prevents RuntimeError: set size changed during iteration
                                if mine not in self.mines:
                                    print(f"While cleaning the knowledge base, found new mine {mine}!")
                                    self.mark_mine(mine)
                                    changed = True
                                    print("Set changed to true")
                        if new_safes is not None:
                            assert new_safes != set(), f"new_safes {new_safes} is supposed to be a full set, but instead got empty set. Sentence is {{{sentence.cells}}} = {sentence.count}"
                            print(f"new safes found: {new_safes}")
                            for safe in new_safes.copy():
                                if safe not in self.safes:
                                    print(f"While cleaning the knowledge base, found new safe cell {safe}!")
                                    self.mark_safe(safe)
                                    changed = True
                                    print("Set changed to true")
                
            for sentence_1 in self.knowledge:
                for sentence_2 in self.knowledge:
                    if sentence_1 == sentence_2:
                        continue
                    if sentence_1.cells == set() or sentence_2.cells == set():
                        continue
                    if sentence_1.cells.issubset(sentence_2.cells):
                        #Ensure neither is an empty sentence
                        assert sentence_1.cells != set(), f"Expected sentence 1 to be a set, instead got empty set {sentence_1.cells} with {sentence_1.count} - current KB is {self.knowledge}"
                        assert sentence_2.cells != set(), f"Expected sentence 2 to be a set, instead got empty set {sentence_2.cells} with {sentence_2.count} - current KB is {self.knowledge}"

                        #sentence 1 is a subset of sentence 2
                        resultant_sentence = sentence_2.cells - sentence_1.cells
                        resultant_count = sentence_2.count - sentence_1.count   
                        new_sentence = Sentence(resultant_sentence,resultant_count)
                        print(f"Identified subset rule between sentence {sentence_1} and sentence {sentence_2}, new sentence {new_sentence} identified")

                        if new_sentence not in self.knowledge:
                            assert new_sentence.cells != set(), f"Created new sentence that is an empty set"
                            #New sentence has not been created before, so add it to the KB.
                            self.knowledge.append(new_sentence)
                            
                            changed = True
                            print(f"Added new sentence {new_sentence} to KB")
                            print("Set changed to true")
                        
            #remove empty sets
            empty = Sentence(set(),0)
            self.knowledge[:] = [sentence for sentence in self.knowledge if sentence != empty]
                

                #Update information
        #mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        
        print(f"Moves made are {self.moves_made}")
        print(f"{len(self.safes)} safe moves available - {self.safes}.")
        print(f"There are {len(self.mines)} known mines - {self.mines}")
        print(f"The AIs knowledge base is:")
        for sentence in self.knowledge:
            print(f"{{{sentence.cells}}} = {sentence.count}")
        print("==================================================================================")
        # breakpoint()
                


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        """make_safe_move should return a move (i, j) that is known to be safe.
            The move returned must be known to be safe, and not a move already made.
            If no safe move can be guaranteed, the function should return None.
            The function should not modify self.moves_made, self.mines, self.safes, or self.knowledge."""
        #Eliminate moves already made
        safes = self.safes - self.moves_made
        if safes:
            print("Making safe move - {} safe moves availible".format(len(safes)))
            move = random.choice(list(safes))
            print(f"Made safe move {move}")
            return move
        else:
            return None
                    
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #Make sure the move is actually availible
        all_cells = set((i,j) for i in range(self.height) for j in range(self.width))
        _ =  all_cells - self.mines
        #use _ as a garbage variable - personal preference
        available_cells = _ - self.moves_made

        if available_cells == set():
            #No moves can be made!
            print(f"No random moves possible!")
            return None
        else:
            random_move = random.choice(list(available_cells))
            print(f"Making random move - {random_move}!")
            return random_move




