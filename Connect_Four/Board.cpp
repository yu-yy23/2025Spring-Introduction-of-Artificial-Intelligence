#include "Board.h"

Board::Board(int m, int n, int** _board, const Point& p): M(m), N(n), prohibitedMove(p) {
    bits[0] = bits[1] = bits[2] = 0;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (_board[i][j] == 1) {
                int index = i * N + j;
                bits[index / 64] |= (1ULL << (index % 64));
            }
        }
    }
}

Board::Board(const Board& other): M(other.M), N(other.N), prohibitedMove(other.prohibitedMove) {
    bits[0] = other.bits[0];
    bits[1] = other.bits[1];
    bits[2] = other.bits[2];
}

int Board::getCell(int x, int y) const {
    if (x == prohibitedMove.x && y == prohibitedMove.y) {
        return 0;
    }
    int index = x * N + y;
    return ((bits[index / 64] >> (index % 64)) & 1) ? 1 : 2;
}

void Board::setCell(int x, int y, int val) {
    int index = x * N + y;
    if (val == 1) {
        bits[index / 64] |= (1ULL << (index % 64));
    } else {
        bits[index / 64] &= ~(1ULL << (index % 64));
    }
}
