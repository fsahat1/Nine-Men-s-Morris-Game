import pygame
from GUIControl.GameState import GameState

class RemovingState(GameState):
    
    def handle_events(self, game, state, index):
        try:
            game.remove_piece(state.global_player,index)
            state.global_player = 2 if state.global_player == 1 else 1
            state.placed = False
            state.mill_tested = True
            state.placed_index = -1
        except Exception as e:
            state.text_command = str(e)