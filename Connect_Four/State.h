#ifndef STATE_H
#define STATE_H
#include <vector>
#include <algorithm>
#include "Point.h"
#include "Board.h"

class State {
private:
    int M;
    int N;
    Board board;
    int* top;
    int* weights;
    bool own;
    int totalWeight;
    Point lastMove;
    Point thisMove;
    Point prohibitedMove;
    std::vector<Point> availableMoves;
    std::vector<std::pair<Point, int> > orderedAvailableMoves;
protected:
    bool isLegalMove(const Point& p) const;
public:
    State(const int m, const int n, int** _board, const int* _top,
        const bool _own, const Point& lastMove, const Point& _prohibitedMove);
    State(const State& other);
    bool move(const Point& p);
    bool isOver() const;
    int getResult() const;
    Point getFirstAvailableMove();
    bool isFullyExpanded() const;
    std::vector<Point> getAvailableMoves() const;
    void updateAvailableMoves();
    void sortOrderedAvailableMoves();
    Point getThisMove() const;
    Point getRandomMove() const;
    void printState() const;
    void printAvailableMoves() const;
    bool isOwn() const;
    Point getMustMove();
    bool isOwnWin(const int x, const int y) const;
    bool isOpponentWin(const int x, const int y) const;
    bool isTie() const;
    ~State();
};
#endif