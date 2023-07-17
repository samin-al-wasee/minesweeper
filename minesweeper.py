import random


class Minesweeper:
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
        """
        Checks if a cell contains mine or not.

        Args:
            cell (tuple): a single cell in the minesweeper board.

        Returns:
            bool: if the cell contains mine, returns True, false otherwise.
        """
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


class Sentence:
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
            return self.cells

        return None
        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

        return None
        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        try:
            self.cells.remove(cell)
            self.count -= 1
        except KeyError:
            print("No such cells to remove.")
        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        try:
            self.cells.remove(cell)
        except KeyError:
            print("No such cells to remove.")
        # raise NotImplementedError


class MinesweeperAI:
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
        print(f"Moves made so far: {self.moves_made}")
        self.moves_made.add(cell)
        print(f"Moves made so far after the latest move: {self.moves_made}")

        print(f"Marked safe so far: {self.safes}")
        self.mark_safe(cell)
        print(f"Marked safe so far after the latest insertion: {self.safes}")

        self.check_current_knowledge()

        print(f"Mines found so far after latest insertion: {self.mines}")
        print(f"Marked safe so far after the latest insertion: {self.safes}")

        self.show_knowledge()

        new_sentence = self.create_sentence(cell, count)

        for existing_sentence in self.knowledge:
            if new_sentence == existing_sentence:
                return

        self.knowledge.append(new_sentence)
        self.check_current_knowledge()
        self.show_knowledge()

        print(f"Mines found so far after latest insertion: {self.mines}")
        print(f"Marked safe so far after the latest insertion: {self.safes}")
        # raise NotImplementedError

    def check_current_knowledge(self):
        print("Checking current Knowledge-Base.")
        self.forget_mines_or_safes()

        is_unchanged = True
        knowledge_copy = self.knowledge[:]

        for index, existing_sentence in enumerate(knowledge_copy):
            self.knowledge.remove(existing_sentence)
            comparing_index = index
            # self.knowledge_copy = self.knowledge[:]

            for another_sentence in self.knowledge[:]:
                if existing_sentence.cells < another_sentence.cells:
                    self.knowledge.remove(another_sentence)
                    self.knowledge.append(
                        Sentence(
                            another_sentence.cells.difference(existing_sentence.cells),
                            another_sentence.count - existing_sentence.count,
                        )
                    )
                    is_unchanged = False
                elif existing_sentence.cells > another_sentence.cells:
                    existing_sentence = Sentence(
                        existing_sentence.cells.difference(another_sentence.cells),
                        existing_sentence.count - another_sentence.count,
                    )
                    is_unchanged = False

            if is_unchanged:
                self.knowledge.insert(comparing_index + 1, existing_sentence)
                # self.forget_mines_or_safes()
                knowledge_copy = self.knowledge
                print("Knowledge-Base unchanged. Continuing loop.")
            else:
                self.knowledge.append(existing_sentence)
                print("Knowledge-base changed. Rechecking.")
                self.check_current_knowledge()
                print("Knowledge-base checking complete. No new changes.")
                break

    def forget_mines_or_safes(self):
        confirm_mines = []
        confirm_safes = []

        while True:
            is_unchanged = True

            for existing_sentence in self.knowledge[:]:
                if existing_sentence.known_mines() is not None:
                    print("All are mines.")
                    confirm_mines.append(existing_sentence)
                    self.knowledge.remove(existing_sentence)
                    is_unchanged = False
                elif existing_sentence.known_safes() is not None:
                    print("All are safe.")
                    confirm_safes.append(existing_sentence)
                    self.knowledge.remove(existing_sentence)
                    is_unchanged = False

            for new_sentence in confirm_mines[:]:
                for cell in new_sentence.cells:
                    self.mark_mine(cell)

                confirm_mines.remove(new_sentence)

            for new_sentence in confirm_safes[:]:
                for cell in new_sentence.cells:
                    self.mark_safe(cell)

                confirm_safes.remove(new_sentence)

            if is_unchanged:
                print("No new mines or safe cells found. Moving on.")
                break

            print("New mines or safe cells found. Rechecking.")

    def show_knowledge(self):
        print("Here is the current Knowledge-Base: ")

        for sentence in self.knowledge:
            print(sentence)

    def create_sentence(self, cell, count):
        cells_to_be_added = []

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        count -= 1
                        continue
                    elif (i, j) in self.safes:
                        continue
                    else:
                        cells_to_be_added.append((i, j))

        return Sentence(cells_to_be_added, count)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) == 0:
            return None

        for cell in self.safes:
            if cell not in self.moves_made:
                print(f"Here is a safe cell {cell} to dig into.")
                return cell

        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if len(self.moves_made) + len(self.mines) == self.height * self.width:
            return None

        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)

            if (i, j) not in self.moves_made or (i, j) not in self.mines:
                print(
                    f"Random empty cell {(i, j)} found. It is still not a mine but careful, it can be."
                )
                return (i, j)

        # raise NotImplementedError
