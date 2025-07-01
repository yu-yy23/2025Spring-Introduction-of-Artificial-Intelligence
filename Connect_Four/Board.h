#ifndef BOARD_H
#define BOARD_H
#include <vector>
#include <algorithm>
#include "Point.h"

using uint64 = unsigned long long int;

class Board {
private:
    int M;
    int N;
    uint64 bits[3];
    Point prohibitedMove;
public:
    Board(int m, int n, int** _board, const Point& p);
    Board(const Board& other);
    int getCell(int x, int y) const;
    void setCell(int x, int y, int val);
};
#endif