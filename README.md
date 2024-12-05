# MonteCarlo


META DATA

    Final Project (Monte Carlo Simulator) by Maheen Mubashar

SYNOPSIS

    This is a simple Monte Carlo Simulator with three related classes -- a Dice class, a Game class, and an Analyzer class.
    The classes are related in the following way: Game objects are initialized with a Dice object, and Analyzer objects are initialized with a Game object.

[Dice] --> [Game] --> [Analyzer]

In this simulation, a 'die' can be any discrete random variable associated with a stochastic process, sucha as using a deck of card, flipping a coin, rolling an actual die, or speaking a language.

Installing:

    ! pip install .

Importing:

    from montecarlo import Die, Game, Analyzer


CREATING A DICE:

1. To create a dice object called Die:

        faces = np.array(['face_1', 'face_2'])
        Die = Dice(faces)


2. To change the weight of the face_1 to 5.0:

        Die.change_weight('face_1', 5.0)


3. To roll the Die a 100 times:

        Die.roll_the_die(100)


4. To show the current state of the Die:

        Die.die_current_state()


CREATING A GAME:

1. To create Game object game with Die:

        game = Game([Die])


2. To play the game a 100 times:

        game.play(100)


3. To show results of the play in 'narrow' format:

        game.show_results('narrow')


CREATING AN ANALYZER:

1. To create an Analyzer object analyzer with game:

        analyzer = Analyzer(game)


2. To find the number of jackpots:

        analyzer.jackpot()


3. To find count of all faces rolled:

        analyzer.face_count()


4. To get count of all combinations:

        analyzer.combo_count()


5. To get count of all permutations:

        analyzer.permutation_count()



API DESCRIPTION

Dice Class:

A class representing a die of N sides or 'faces' and W weights that can be rolled to select a face. By default 
    all faces have equal weight of 1.0, but can be changed after the object is created. Each side of a die contains a
    unique symbol. Symbols may be alphabetic or numeric. The die has one behavior, which is to be rolled one or more times.
    
    ATTRIBUTES:
        faces(np.ndarray): The faces of the die passed as a NumPy array. Could be numeric or strings.
        
        weights (np.ndarray): The weights for each face, defaults to 1.0 for all faces. Can be changed later.
        
    METHODS:
        
        __init__(self, face_array): Initializes the Dice object with faces and sets all weights to 1.0.
        
            INPUTS: 
                face_array(np.ndarray): The faces of the die. Should be an numpy array of distinct values.
            
            RAISES:
                TypeError: If face_array is not a numpy array.
                ValueError: If face_array does not have distinct values.
        
        change_weight(side, new_weight): Changes the weight of a given face.
        
            INPUTS:
                side (str or int): The face of the die to change the wieght of.
                new_weight (int or float): The new weight for the given side.
                
            RAISES:
                IndexError: If the face passed is not in the die array.
                TypeError: If new_weight is not an int or float.
            
        roll_the_die(rolls = 1): Rolls the die a specific number of times, and returns a list of outcomes.
        
            INPUTS:
                rolls (int): The number of times to roll the die. Defaults to 1.
        
            OUTPUTS: 
                List: A list of rolled faces (outcomes).
            
        die_current_state(): Returns a copy of the current state of the die.
            INPUTS:
                none
            OUTPUTS:
                pd.DataFrame: A DataFrame of the die's faces and weights.
                
 
Game Class:

Class representing a game consisting of rolling one or more similar dice (Die objects) one or more times. 
    
    Each game is initiated with a Python list of one or more dice. Similar dice mean that each die in a given game 
    has the same number of sides and associated faces, but each die object may have its onw weights. Game objects have 
    behavior to roll all the dice a given number of times. Game objects only keep the results of their most recent play.
    
    ATTRIBUTES:
        list_of_dice(List): A list of one or more Dice objects that are used in the game. All dice must have the has the same number of sides and associated faces.
        
    
    METHODS:
        
        __int__ (self, dice_list): Initializes a game with a list of Die objects.
            INPUTS:
                dice_list(List): A list of already instantiated similar dice objects.
            
            RAISES: 
                TypeError: If any element in the dice_list is not a Die object.
                ValueError: If any dice in the list have different faces.
                
        play(self,rolls): Rolls all the dice the specified number of times and saves the result of the play to a private data frame in "wide" format.
            INPUTS:
                rolls (int): The number of times to roll the  dice.
        
        show_results(self, form = 'wide'): Returns a copy of the private data frame of results of the most recent play in either "wide" or "narrow" format.
            INPUTS: 
                form (str): The format ("Wide" or "Narrow") to return the data frame in. Defaults to wide. 
        
            OUTPUTS:
                pd.DataFrame: A DataFrame of the results of the most recent play in the requested format.
            
            RAISES:
                ValueError: If the user passes an invalid option for form other than "narrow" or "wide".
                
Analyzer Class

An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it.
    
    ATTRIBUTES:
        game(Game): A game object based on the given parameter.        
 
    METHODS:
        __init__ (self, game_object): Initializes the given game object.
            INPUTS: 
                game_object(Game): A game object.
        
            RAISES:
                ValueError: If the passed value is not a Game object.
        
        jackpot (self): Computes how many times the game resulted in a jackpot. Returns an integer for the number of jackpots.
            INPUTS:
                none
            OUTPUTS:
                Int: An integer for the number of jackpots.
        
        face_count (self): Computes how many times a given face is rolled in each event. Returns a data frame of results.
            INPUTS:
                none
            OUTPUTS: 
                pd.DataFrame: A Data Frame of the face counts. The data frame has an index of the roll number, face values as columns, and count values in the cells.  
        
        combo_count (self): Computes the distinct combinations of faces rolled, along with their counts. Returns a data frame of results.
            INPUTS:
                none
            OUTPUTS:
                pd.DataFrame: A data frame of the count of order-independent combinations. 
                
        permutation_count (self): Computes the distinct permutations of faces rolled, along with their counts. Returns a data frame of results.
            INPUTS:
                none
            OUTPUTS:
                pd.DataFrame: A data frame of counts of permutations.
    
