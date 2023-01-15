from AI.AI import AI


class Minimax(AI):

    def findMove(self, gs, valid_moves):
        alpha = -self.CHECKMATE
        beta = self.CHECKMATE
        self.findMoveMinimax(gs, valid_moves, self.DEPTH, gs.red_to_move, alpha, beta)
        return self.next_move

    def findMoveMinimax(self, gs, valid_moves, depth, red_to_move, alpha, beta):
        if depth == 0 or self.isQuiescent(gs):
            return self.scoreMaterial(gs.board)
        if red_to_move:
            max_score = -self.CHECKMATE
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getAllPossibleMoves()
                score = self.findMoveMinimax(gs, next_moves, depth - 1, False, alpha, beta)
                gs.undoMove()
                if score > max_score:
                    max_score = score
                    if depth == self.DEPTH:
                        self.next_move = move
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return max_score
        else:
            min_score = self.CHECKMATE
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getAllPossibleMoves()
                score = self.findMoveMinimax(gs, next_moves, depth - 1, True, alpha, beta)
                gs.undoMove()
                if score < min_score:
                    min_score = score
                    if depth == self.DEPTH:
                        self.next_move = move
                beta = min(beta, score)
                if alpha >= beta:
                    break
            return min_score

    def isQuiescent(self, gs):
        """
        Function to determine if the current position is 'quiescent'
        """
        for r in range(len(gs.board)):
            for c in range(len(gs.board[r])):
                if gs.board[r][c][0] in ['b','r']:
                    return False
        return True
