

import random


import concurrent.futures

class Negamax(AI):
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor()
        # ...

    def findMove(self, gs, valid_moves):
        random.shuffle(valid_moves)
        self.findMoveNegaMaxAlphaBeta(gs, valid_moves, self.DEPTH, -self.CHECKMATE, self.CHECKMATE, 1 if gs.red_to_move else -1)
        return self.next_move

    def findMoveNegaMaxAlphaBeta(self, gs, valid_moves, depth, alpha, beta, turn):
        if depth == 0:
            return turn * self.scoreMaterial(gs.board)
        bestValue = -self.CHECKMATE
        next_moves_futures = []
        for move in valid_moves:
            gs.makeMove(move)
            next_moves_futures.append(self.executor.submit(gs.getAllPossibleMoves))
            gs.undoMove()
        for move, next_moves_future in zip(valid_moves, next_moves_futures):
            gs.makeMove(move)
            next_moves = next_moves_future.result()
            score_future = self.executor.submit(self.findMoveNegaMaxAlphaBeta, gs, next_moves, depth - 1, -beta, -alpha, -turn)
            score = -score_future.result()
            gs.undoMove()
            if score > bestValue:
                bestValue = score
                if depth == self.DEPTH:
                    self.next_move = move
            alpha = max(alpha, bestValue)
            if alpha >= beta:
                break
        return bestValue

