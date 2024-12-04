import pandas as pd
import numpy as np

class Dice:
    
    """
    A class representing a die of N sides or 'faces' and W weights that can be rolled to select a face. By default 
    all faces have equal weight of 1.0, but can be changed after the object is created. Each side of a die contains a
    unique symbol. Symbols may be alphabetic or numeric. The die has one behavior, which is to be rolled one or more times.
    
    ATTRIBUTES:
        faces(np.ndarray): The faces of the die passed as a NumPy array. Could be numeric or strings.
        
        weights (np.ndarray): The weights for each face, defaults to 1.0 for all faces. Can be changed later.
        
        _my_die (pd.DataFrame): A private pandas DataFrame that contains faces and their weights.
        
    METHODS:
        __init__(self, face_array): Initializes the Dice object with faces and sets all weights to 1.0.
        
        change_weight(side, new_weight): Changes the weight of a given face.
        
        roll_the_die(rolls = 1): Rolls the die a specific number of times, and returns a list of outcomes.
            
        die_current_state(): Returns a copy of the current state of the die.
    """
    

    def __init__ (self, face_array):
        """
        PURPOSE: Initiliaze the Dice object with faces and set all weights to 1.0. 
        Wieghts can be changed after initialization. 
        
        INPUTS: 
            face_array(np.ndarray): The faces of the die. Should be an numpy array of distinct values.
            
        RAISES:
            TypeError: If face_array is not a numpy array.
            ValueError: If face_array does not have distinct values.
        """
        
        #Check that face_array is a numpy array 
        if type(face_array) is not np.ndarray:                       
            raise TypeError ("Argument should be a numpy array")    
        
        
        #Check that all values in the array are distinct 
        if len(np.unique(face_array)) != len(face_array):         
            raise ValueError ("Values should be distinct")
        
        self.faces = face_array
        self.weights = np.ones(len(face_array))     #Set default weight of 1.0 for each face
        
        #Save faces and weights in a private data frame with face as index
        self._my_die = pd.DataFrame({                   
        'faces': self.faces,
        'weights': self.weights
    },
        index = self.faces)
        
    def change_weight(self, side, new_weight):
        """
        PURPOSE: Change the weight of a given face of the die
        
        INPUTS:
            side (str or int): The face of the die to change the wieght of.
            new_weight (int or float): The new weight for the given side.
            
        RAISES:
            IndexError: If the face passed is not in the die array.
            TypeError: If new_weight is not an int or float.
        """
        
        # Check that side passed is in the die array
        if side not in self.faces:
            raise IndexError("Face passed is not a valid value")
        
        type_of_weight = [int, float]     #acceptable types of weights
        
        # Check that the weight is numeric 
        if type(new_weight) not in type_of_weight: 
            try:
                new_weight = float(new_weight)               #Check if castable as numeric
            except: 
                raise TypeError("New weight should be of type integer or float")
        
        
        #Change the weight of for the passed side to the new weight
        self._my_die.loc[side, 'weights'] = new_weight
            
            
    def roll_the_die(self, rolls = 1):
        """
        PURPOSE: Roll the die and return a Python list of outcomes.
        
        INPUTS:
            rolls (int): The number of times to roll the die. Defaults to 1.
        
        OUTPUTS: 
            List: A list of rolled faces (outcomes).
        """
        
        results = []       #create list of results
        
        # Roll the die the specified number of times
        
        for i in range(rolls):
            result = self._my_die.faces.sample(weights = self._my_die.weights, replace = True).values[0]
            results.append(result)
        
        return results                           # what does he mean do not interanlly store the results, don't use self?
    
    
    
    def die_current_state(self):
        """
        PURPOSE: Returns a copy of the private die data frame.
        
        OUTPUTS:
            pd.DataFrame: A DataFrame of the die's faces and weights.
        """
        
        # Return a copy of the private die data frame
        return self._my_die.copy()

 #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Game:
    
    """
    Class representing a game consisting of rolling one or more similar dice (Die objects) one or more times. 
    
    Each game is initiated with a Python list of one or more dice. Similar dice mean that each die in a given game 
    has the same number of sides and associated faces, but each die object may have its onw weights. Game objects have 
    behavior to roll all the dice a given number of times. Game objects only keep the results of their most recent play.
    
    ATTRIBUTES:
        list_of_dice(List): A list of one or more Dice objects that are used in the game. All dice must have the has the same number of sides and associated faces.
        
        _play_results(pd.DataFrame): A private DataFrame that stores the results of the most recent play in "wide" format.
    
    METHODS:
        __int__ (self, dice_list): Initializes a game with a list of Die objects.
        
        play(self,rolls): Rolls all the dice the specified number of times and saves the result of the play to a private data frame in "wide" format.
        
        show_results(self, form = 'wide'): Returns a copy of the private data frame of results of the most recent play in either "wide" or "narrow" format.

    
    """
    
    def __init__(self, dice_list):
        """
        PURPOSE: Takes a single parameter, a list of already instantiated similar dice and initializes a Game object with it.
        
        INPUTS:
            dice_list(List): A list of already instantiated similar dice objects.
            
        RAISES: 
            TypeError: If any element in the dice_list is not a Die object.
            ValueError: If any dice in the list have different faces.
        """
        
        #Check that all elements in dice_list are of class Dice
        for d in dice_list:
            if (type(d) is not Dice):
                raise TypeError ("All elements in the dice list must be objects of the Die Class")
        
        
        
        faces = [(x.faces) for x in dice_list]      #get faces of all the die in the dice_list
       
        # Check that all dice have the same faces
        for die in dice_list[1:]:                    #start from the second die
            if not np.array_equal(die.faces, dice_list[0].faces):             #comparing to the first die #*  
                raise ValueError("All dice must have the same faces.")
           
        
        #* from: https://stackoverflow.com/questions/10580676/comparing-two-numpy-arrays-for-equality-element-wise
        
        
        #Initialize the list of dice using the given parameter
        self.list_of_dice = dice_list
    
    
    def play(self,rolls):
        """
        PURPOSE: Simulates playing the game by rolling all dice the specified number of times. Saves results of 
        the play in a private DataFrame ("_play_results") in wide format.
        
        INPUTS:
            rolls (int): The number of times to roll the  dice.
            
        
        """
        
        
        outcomes = {}
        
        
        # Rolls each die and store the results
        for i in range(len(self.list_of_dice)):
            die = self.list_of_dice[i]
            outcomes[i] = die.roll_the_die(rolls)

        
        # Save the results of the play to a private data frame in wide format by defualt
        self._play_results = pd.DataFrame(outcomes)
        
        self._play_results.index = [i+1 for i in range(len(self._play_results.index))]
        
        self._play_results.columns = [i+1 for i in range(len(self._play_results.columns))]
        
        self._play_results.index.name = 'rolls'
        
        self._play_results.columns.name = 'die'
    
    
    def show_results(self, form = "wide"):
        """
        PURPOSE: Returns a copy of the private play data frame to show the user the results of the most recent play in either "wide" or "narrow" format.
        
        INPUTS: 
            form (str): The format ("Wide" or "Narrow") to return the data frame in. Defaults to wide. 
        
            
        OUTPUTS:
            pd.DataFrame: A DataFrame of the results of the most recent play in the requested format.
            
            
        RAISES:
            ValueError: If the user passes an invalid option for form other than "narrow" or "wide".
            
        """
        
        # Check if play_results has been initialized by checking for _play_results      
        if not hasattr(self, '_play_results'): 
            raise Error("The play method must be called before showing results.")
            
            #from https://stackoverflow.com/questions/610883/how-to-check-if-an-object-has-an-attribute
        
        
        if form == "wide":
            return self._play_results.copy()                    #Return a copy of the private play data frame in wide format
        elif form == "narrow": 
            #Convert the data frame to narrow format
            narrow_df = self._play_results.stack().reset_index().set_index(['rolls', 'die'])     
            narrow_df.columns = ['outcomes']
            return narrow_df.copy()                             #Returns a copy of the private play data frame in narrow format                  
        else:
            raise ValueError("Invalid format. Please choose either 'wide' or 'narrow'.")
                                                                    


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Analyzer:
    """
    An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it.
    
    ATTRIBUTES:
        game(Game): A game object based on the given parameter.        
 
    METHODS:
        __init__ (self, game_object): Initializes the given game object.
        
        jackpot (self): Computes how many times the game resulted in a jackpot. Returns an integer for the number of jackpots.
        
        face_count (self): Computes how many times a given face is rolled in each event. Returns a data frame of results.
        
        combo_count (self): Computes the distinct combinations of faces rolled, along with their counts. Returns a data frame of results.
        
        permutation_count (self): Computes the distinct permutations of faces rolled, along with their counts. Returns a data frame of results.
    
    """
    
    def __init__(self, game_object):
        """
        PURPOSE: Takes a game object as its input parameter and initializes it.
        
        INPUTS: 
            game_object(Game): A game object.
        
        RAISES:
            ValueError: If the passed value is not a Game object.
        
        """
        if type(game_object) is not Game:
            raise ValueError ("Passed object is not a game object")
        
        self.game = game_object
        
        
    def jackpot(self):
        """
        PURPOSE:
            Computes how many times the game resulted in a jackpot. A jackpot is a result in which all faces are the same, e.g. all ones for a six-sided die.


        OUTPUTS:
            Int: An integer for the number of jackpots.
           
            
        """
        
        if not hasattr(self.game, '_play_results') or self.game._play_results is None:
            raise ValueError("The game has not been played yet. Please call the play method first.")

        
        
        jackpot = 0 
        
        # Iterate through each roll and check if the faces are all the same, indicating a jackpot       
        for index, row in self.game._play_results.iterrows():                       #* 
            if (len(np.unique(row.values)) == 1):      
                jackpot +=1
        
        return jackpot       
    
    #* from https://stackoverflow.com/questions/16476924/how-can-i-iterate-over-rows-in-a-pandas-dataframe
    
    def face_count(self):
        """
        PURPOSE:
            Computes how many times a given face is rolled in each event. 
        
        
        OUTPUTS: 
          pd.DataFrame: A Data Frame of the face counts. The data frame has an index of the roll number, face values as columns, and count values in the cells.   
        
        """
       
    
        if not hasattr(self.game, '_play_results') or self.game._play_results is None:
            raise ValueError("The game has not been played yet. Please call the play method first.")

        
        counts = self.game._play_results.stack().groupby('rolls').value_counts().unstack()
        counts = counts.fillna(0)
        counts.columns.name = "face values"
        face_num = len(self.game.list_of_dice[0].faces)            #since game objects require all dice have the same number of faces                                             
        counts = counts.reindex(columns = range(1,int(face_num)+1), fill_value = 0.0)
        return counts
        
   
    def combo_count(self): 
        """
        PURPOSE:
            Computes the distinct combinations of faces rolled, along with their counts. Combinations are order-independent and may contain repetitions.
            
        
        OUTPUTS:
            pd.DataFrame: A data frame of the count of order-independent combinations. 
            
        
        """
            
            
        if not hasattr(self.game, '_play_results') or self.game._play_results is None:
            raise ValueError("The game has not been played yet. Please call the play method first.")

        
        
        combos = [*self.game._play_results.itertuples(index = False, name = None)]   #*
        combos = [tuple(sorted(i)) for i in combos]                                            #turning all combos into tuples 
        combo_df = pd.DataFrame(combos)
        combo_df.columns = combo_df.columns +1
        combo_df = combo_df.groupby(combo_df.columns.tolist(), as_index = False).size()
        combo_df.rename(columns={'size': 'Count'}, inplace=True)
        combo_df = combo_df.set_index(combo_df.columns[:-1].tolist())
        
        
        return combo_df

      #* from https://stackoverflow.com/questions/55976283/how-to-get-data-from-rows-into-tuples

    def permutation_count(self):
        """
        PURPOSE:
            Computes the distinct permutations of faces rolled, along with their counts. Permutations are order-dependent and may contain repetitions.


        OUTPUTS:
            pd.DataFrame: A data frame of counts of permutations.
        
        """
        
        if not hasattr(self.game, '_play_results') or self.game._play_results is None:
            raise ValueError("The game has not been played yet. Please call the play method first.")

        
        perm_tuples = [*self.game._play_results.itertuples(index=False, name=None)]                    #turning combos into tuples 
        perm_counts_df = pd.DataFrame(perm_tuples)
        perm_counts_df.columns = perm_counts_df.columns +1
        perm_counts_df = perm_counts_df.groupby(perm_counts_df.columns.tolist(), as_index = False).size()
        perm_counts_df.rename(columns={'size': 'Count'}, inplace=True)
        perm_counts_df = perm_counts_df.set_index(perm_counts_df.columns[:-1].tolist())
        
        return perm_counts_df
        
