#include "State.h"
#include <iostream>

bool State::isLegalMove(const Point& p) const {
    // std::cerr << "Checking legality of move: " << p.x << ", " << p.y << std::endl;
    if (p.x < 0 || p.x >= M || p.y < 0 || p.y >= N) {
        std::cerr << "Move out of bounds: " << p << std::endl;
        return false;
    }
    if (p.x >= top[p.y]) {
        std::cerr << "Move to occupied cell: board[" << p.x << "][" << p.y << "]: "<< board.getCell(p.x, p.y) << std::endl;
        return false;
    }
    if (p.x == prohibitedMove.x && p.y == prohibitedMove.y) {
        std::cerr << "Move is prohibited: " << p << std::endl;
        return false;
    }
    // std::cerr << "Move is legal: " << p.x << ", " << p.y << std::endl;
    return true;
}

State::State(const int m, const int n, int** _board, const int* _top,
        const bool _own, const Point& _lastMove, const Point& _prohibitedMove)
    : M(m), N(n), own(_own), lastMove(-1, -1), totalWeight(0),
        prohibitedMove(_prohibitedMove), thisMove(_lastMove),
        board(m, n, _board, _prohibitedMove) {
    top = new int[N];
    for (int i = 0; i < N; ++i) {
        top[i] = _top[i];
    }
    weights = new int[N];
    for (int i = 0; i <= N / 2; ++i) {
        weights[i] = (i + 1);
        totalWeight += weights[i];
    }
    for (int i = N / 2 + 1; i < N; ++i) {
        weights[i] = weights[N - i - 1];
        totalWeight += weights[i];
    }
}

State::State(const State& other)
    : M(other.M), N(other.N), own(other.own), lastMove(other.lastMove),
        thisMove(other.thisMove), prohibitedMove(other.prohibitedMove),
        totalWeight(other.totalWeight), availableMoves(other.availableMoves),
        orderedAvailableMoves(other.orderedAvailableMoves), board(other.board) {
    top = new int[N];
    for (int i = 0; i < N; ++i) {
        top[i] = other.top[i];
    }
    weights = new int[N];
    for (int i = 0; i < N; ++i) {
        weights[i] = other.weights[i];
    }
}

bool State::move(const Point& p) {
    // std::cerr << "Attempting to move to: " << p << std::endl;
    if (!isLegalMove(p)) {
        std::cerr << "Move is illegal: " << p << std::endl;
        return false;
    }
    // std::cerr << "Move is legal, proceeding..." << std::endl;
    lastMove = thisMove;
    thisMove = p;
    board.setCell(p.x, p.y, own ? 1 : 2);
    own = !own;
    top[p.y]--;
    if (top[p.y] - 1 == prohibitedMove.x && p.y == prohibitedMove.y) {
        top[p.y]--;
    }
    // std::cerr << "Move completed: " << p << std::endl;
    // printState();
    return true;
}

bool State::isOver() const {
    // std::cerr << "Checking if game is over..." << std::endl;
    if (thisMove.x == -1 && thisMove.y == -1) {
        // std::cerr << "Game began just now" << std::endl;
        return false;
    }
    // return (own ? machineWin(thisMove.x, thisMove.y, M, N, board) :
    //     userWin(thisMove.x, thisMove.y, M, N, board)) || isTie(N, top);
    if (own && isOwnWin(thisMove.x, thisMove.y)) {
        // std::cerr << "Machine wins!" << std::endl;
        return true;
    }
    if (!own && isOpponentWin(thisMove.x, thisMove.y)) {
        // std::cerr << "User wins!" << std::endl;
        return true;
    }
    if (isTie()) {
        // std::cerr << "Game is a tie!" << std::endl;
        return true;
    }
    return false;
}

int State::getResult() const {
    if (own && isOwnWin(thisMove.x, thisMove.y)) {
        return 1;
    }
    if (!own && isOpponentWin(thisMove.x, thisMove.y)) {
        return -1;
    }
    return 0;
}

Point State::getFirstAvailableMove() {
    if (orderedAvailableMoves.empty()) {
        return Point(-1, -1);
    }
    Point firstAvailableMove = orderedAvailableMoves.back().first;
    orderedAvailableMoves.pop_back();
    return firstAvailableMove;
}

bool State::isFullyExpanded() const {
    return orderedAvailableMoves.empty();
}

std::vector<Point> State::getAvailableMoves() const {
    return availableMoves;
}

Point State::getRandomMove() const {
    if (availableMoves.empty()) {
        // std::cerr << "No available random moves!" << std::endl;
        return Point(-1, -1);
    }
    int randomWeight = rand() % totalWeight;
    int accumulatedWeight = 0;
    for (int i = 0; i < N; ++i) {
        accumulatedWeight += weights[i];
        if (randomWeight < accumulatedWeight && top[i] > 0) {
            return Point(top[i] - 1, i);
        }
    }
    return availableMoves[0];
}

Point State::getThisMove() const {
    return thisMove;
}

void State::updateAvailableMoves() {
    availableMoves.clear();
    orderedAvailableMoves.clear();
    for (int i = 0; i < N; ++i) {
        if (top[i] > 0) {
            availableMoves.push_back(Point(top[i] - 1, i));
            orderedAvailableMoves.push_back(std::make_pair(Point(top[i] - 1, i), weights[i]));
        }
    }
}

void State::sortOrderedAvailableMoves() {
    std::sort(orderedAvailableMoves.begin(), orderedAvailableMoves.end(),
        [](const std::pair<Point, int>& a, const std::pair<Point, int>& b) {
            return a.second < b.second;
        });
}

void State::printState() const {
    std::cerr << "Current board state:" << std::endl;
    for (int i = 0; i < M; ++i) {
        for (int j = 0; j < N; ++j) {
            if (i >= top[j]) {
                std::cerr << board.getCell(i, j) << " ";
            } else {
                std::cerr << "0 ";
            }
        }
        std::cerr << std::endl;
    }
    std::cerr << "Current top state:" << std::endl;
    for (int i = 0; i < N; ++i) {
        std::cerr << top[i] << " ";
    }
    std::cerr << std::endl;
}

void State::printAvailableMoves() const {
    std::cerr << "Available moves:" << std::endl;
    for (const auto& move : availableMoves) {
        std::cerr << move << " ";
    }
    std::cerr << std::endl;
}

bool State::isOwn() const {
    return own;
}

Point State::getMustMove() {
    for (const auto& move : availableMoves) {
        if (own) {
            board.setCell(move.x, move.y, 1);
            top[move.y]--;
            if (isOpponentWin(move.x, move.y)) {
                board.setCell(move.x, move.y, 0);
                top[move.y]++;
                // std::cerr << "1" << std::endl;
                return move;
            }
            board.setCell(move.x, move.y, 0);
            top[move.y]++;
        } else {
            board.setCell(move.x, move.y, 2);
            top[move.y]--;
            if (isOwnWin(move.x, move.y)) {
                board.setCell(move.x, move.y, 0);
                top[move.y]++;
                // std::cerr << "2" << std::endl;
                return move;
            }
            board.setCell(move.x, move.y, 0);
            top[move.y]++;
        }
    }
    for (const auto& move : availableMoves) {
        if (own) {
            board.setCell(move.x, move.y, 2);
            top[move.y]--;
            if (isOwnWin(move.x, move.y)) {
                board.setCell(move.x, move.y, 0);
                top[move.y]++;
                // std::cerr << "3" << std::endl;
                return move;
            }
            board.setCell(move.x, move.y, 0);
            top[move.y]++;
        } else {
            board.setCell(move.x, move.y, 1);
            top[move.y]--;
            if (isOpponentWin(move.x, move.y)) {
                board.setCell(move.x, move.y, 0);
                top[move.y]++;
                // std::cerr << "4" << std::endl;
                return move;
            }
            board.setCell(move.x, move.y, 0);
            top[move.y]++;
        }
    }
    return Point(-1, -1);
}

bool State::isOwnWin(const int x, const int y) const {
    //横向检测
    int i, j;
    int count = 0;
    for (i = y; i >= 0 && x >= top[i]; i--)
        if (!(board.getCell(x, i) == 2))
            break;
    count += (y - i);
    for (i = y; i < N && x >= top[i]; i++)
        if (!(board.getCell(x, i) == 2))
            break;
    count += (i - y - 1);
    if (count >= 4)
        return true;

    //纵向检测
    count = 0;
    for (i = x; i < M; i++)
        if (!(board.getCell(i, y) == 2))
            break;
    count += (i - x);
    if (count >= 4)
        return true;

    //左下-右上
    count = 0;
    for (i = x, j = y; i < M && j >= 0 && i >= top[j]; i++, j--)
        if (!(board.getCell(i, j) == 2))
            break;
    count += (y - j);
    for (i = x, j = y; i >= 0 && j < N && i >= top[j]; i--, j++)
        if (!(board.getCell(i, j) == 2))
            break;
    count += (j - y - 1);
    if (count >= 4)
        return true;

    //左上-右下
    count = 0;
    for (i = x, j = y; i >= 0 && j >= 0 && i >= top[j]; i--, j--)
        if (!(board.getCell(i, j) == 2))
            break;
    count += (y - j);
    for (i = x, j = y; i < M && j < N && i >= top[j]; i++, j++)
        if (!(board.getCell(i, j) == 2))
            break;
    count += (j - y - 1);
    if (count >= 4)
        return true;

    return false;
}

bool State::isOpponentWin(const int x, const int y) const {
    //横向检测
    int i, j;
    int count = 0;
    for (i = y; i >= 0 && x >= top[i]; i--)
        if (!(board.getCell(x, i) == 1))
            break;
    count += (y - i);
    for (i = y; i < N && x >= top[i]; i++)
        if (!(board.getCell(x, i) == 1))
            break;
    count += (i - y - 1);
    if (count >= 4)
        return true;

    //纵向检测
    count = 0;
    for (i = x; i < M; i++)
        if (!(board.getCell(i, y) == 1))
            break;
    count += (i - x);
    if (count >= 4)
        return true;

    //左下-右上
    count = 0;
    for (i = x, j = y; i < M && j >= 0 && i >= top[j]; i++, j--)
        if (!(board.getCell(i, j) == 1))
            break;
    count += (y - j);
    for (i = x, j = y; i >= 0 && j < N && i >= top[j]; i--, j++)
        if (!(board.getCell(i, j) == 1))
            break;
    count += (j - y - 1);
    if (count >= 4)
        return true;

    //左上-右下
    count = 0;
    for (i = x, j = y; i >= 0 && j >= 0 && i >= top[j]; i--, j--)
        if (!(board.getCell(i, j) == 1))
            break;
    count += (y - j);
    for (i = x, j = y; i < M && j < N && i >= top[j]; i++, j++)
        if (!(board.getCell(i, j) == 1))
            break;
    count += (j - y - 1);
    if (count >= 4)
        return true;

    return false;
}

bool State::isTie() const {
    for (int i = 0; i < N; ++i) {
        if (top[i] > 0) {
            return false;
        }
    }
    return true;
}

State::~State() {
    delete[] top;
    delete[] weights;
}