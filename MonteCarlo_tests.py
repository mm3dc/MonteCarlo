import unittest
import pandas as pd
import numpy as np

from montecarlo import Dice, Game, Analyzer

class DieGameTestSuite(unittest.TestCase):
    
    
    def test_1_die_init(self): 
        #create a die and test that it has been correctly created 
        faces = np.array([1,2,3,4])
        die1 = Dice(faces)
        die1_faces = die1._my_die.faces
        self.assertTrue((die1_faces == faces).all())
    
    def test_2_change_weight(self):
        # create a die and change the weight of one of its faces. Test if the weight has been changed
        die2 = Dice(np.array([1,2,3,4,5,6]))
        side = 6
        new_weight = 3.0
        die2.change_weight(side, new_weight)
        self.assertEqual(die2._my_die.loc[side,'weights'], new_weight)
    
    def test_3_roll_the_die(self):
        # create a die and roll it. Test if it is rolled the correct amount of times and if the result is a list
        die3 = Dice(np.array([1,2,3,4,5,6]))
        rolls = 4
        results = die3.roll_the_die(rolls)
        self.assertEqual(len(results),rolls)
        self.assertEqual(type(results),list)          
    
    def test_4_die_current_state(self):                                              
        # create a die and test whether its current state matches the initialized state
        die4 = Dice(np.array([1,2,3,4,5,6]))
        current_state = die4.die_current_state()
        initialized_state = die4._my_die                         
        self.assertTrue(current_state.equals(initialized_state))
     
    def test_5_game_init(self):
        #create a game object and test that it was correctly initialized
        faces = np.array([1,2,3,4,5,6])
        d1 = Dice(faces)
        d2 = Dice(faces)
        d3 = Dice(faces)
        game1 = Game([d1,d2,d3])
        self.assertTrue((game1.list_of_dice[0].faces == faces).all())
           
    def test_6_play(self):  
        # create a game object and play. Test if the results are correctly stored
        d1 = Dice(np.array([1,2,3,4,5,6]))
        d2 = Dice(np.array([1,2,3,4,5,6]))
        d3 = Dice(np.array([1,2,3,4,5,6]))
        game2 = Game([d1,d2,d3])
        dice_num = len(game2.list_of_dice)
        rolls = 4
        game2.play(rolls)
        self.assertEqual(game2._play_results.shape, (rolls, dice_num))
        
    def test_7_show_results(self):
        # create a game object and play. Test if the show results data frame is correctly formatted for narrow form
        d1 = Dice(np.array([1,2,3,4,5,6]))
        d2 = Dice(np.array([1,2,3,4,5,6]))
        d3 = Dice(np.array([1,2,3,4,5,6]))
        game3 = Game([d1,d2,d3])
        rolls = 4
        game3.play(rolls)
        narrow_results = game3.show_results('narrow')
        narrow_form = (rolls*len(game3.list_of_dice),1)
        self.assertEqual(narrow_results.shape, narrow_form)       #check that the returned results in narrow form has the expected shape
        
     
    def test_8_analyzer_init(self):
        #create an analyzer object and test whether the raise statement is raising the correct exception
        d1 = Dice(np.array([1,2,3,4,5,6]))
        d2 = Dice(np.array([1,2,3,4,5,6]))
        d3 = Dice(np.array([1,2,3,4,5,6]))
        d4 = Dice(np.array([1,2,3,4,5,6]))
        game4 = Game([d1,d2,d3,d4])
        #analyzer1 = Analyzer(d4)
        self.assertRaises(ValueError, Analyzer, d4)
        
    def test_9_jackpot(self):
        #create an analyzer object. Test if the number of jackpots meet the expected number of jackpots
        d1 = Dice(np.array([1,2,3,4,5,6]))
        d2 = Dice(np.array([1,2,3,4,5,6]))
        d3 = Dice(np.array([1,2,3,4,5,6]))
        d4 = Dice(np.array([1,2,3,4,5,6]))
        game5 = Game([d1,d2,d3,d4])
        rolls = 3
        game5.play(rolls)
        game5._play_results.iloc[1] = [2,2,2,2]          #force a jackpot
        analyzer2 = Analyzer(game5)
        num_jackpot = analyzer2.jackpot() 
        self.assertTrue(num_jackpot >=1)     #test that at least one jackpot is counted -- the forced one
    
    def test_10_face_count(self):
        # create an analyzer object. Test that the face_count returns a data frame of correct shape
        d1 = Dice(np.array([1,2,3,4,5,6]))
        d2 = Dice(np.array([1,2,3,4,5,6]))
        d3 = Dice(np.array([1,2,3,4,5,6]))
        d4 = Dice(np.array([1,2,3,4,5,6]))
        game6 = Game([d1,d2,d3,d4])
        rolls = 3
        game6.play(rolls)
        face_num = len(d1.faces)
        analyzer3 = Analyzer(game6)
        face_counts = analyzer3.face_count() 
        self.assertEqual(type(face_counts), pd.DataFrame)
        self.assertEqual(face_counts.shape, (rolls,face_num))      
        
    def test_11_combo_count(self):
        # create an analyzer object. Test that the combination counts results are returned in a data frame with MultiIndex.
        d1 = Dice(np.array([1,2,3,4,5,6]))
        d2 = Dice(np.array([1,2,3,4,5,6]))
        d3 = Dice(np.array([1,2,3,4,5,6]))
        d4 = Dice(np.array([1,2,3,4,5,6]))
        game7 = Game([d1,d2,d3,d4])
        rolls = 3
        game7.play(rolls)
        analyzer4 = Analyzer(game7)
        combo_counts = analyzer4.combo_count()
        self.assertTrue(type(combo_counts) == pd.DataFrame)
        self.assertTrue(isinstance(combo_counts.index, pd.MultiIndex))                  
        
        #from: https://stackoverflow.com/questions/21081042/detect-whether-a-dataframe-has-a-multiindex
        
    def test_12_permutation_count(self):
        # create an analyzer object. Test that the permutation count results are returned in a data frame with MultiIndex.
        d1 = Dice(np.array([1,2,3,4,5,6]))
        d2 = Dice(np.array([1,2,3,4,5,6]))
        d3 = Dice(np.array([1,2,3,4,5,6]))
        d4 = Dice(np.array([1,2,3,4,5,6]))
        game8 = Game([d1,d2,d3,d4])
        rolls = 3
        game8.play(rolls)
        analyzer5 = Analyzer(game8)
        perm_count = analyzer5.permutation_count()
        self.assertTrue(type(perm_count) == pd.DataFrame)
        self.assertTrue(isinstance(perm_count.index, pd.MultiIndex))

        
        
        
if __name__ == '__main__':
    
    unittest.main(verbosity=3)