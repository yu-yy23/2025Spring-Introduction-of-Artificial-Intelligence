#include "Node.h"

UCTNode::UCTNode(const State& s, UCTNode* p, int d)
    : state(s), parent(p), visit(0), win(0), depth(d) { }

void UCTNode::addChild(UCTNode* child) {
    children.push_back(child);
}

void UCTNode::update(int result) {
    ++visit;
    if (state.isOwn()) win += result;
    else win -= result;
}

double UCTNode::getScore() const {
    if (visit == 0) return -1.0;  // temporary value
    return (double)win / (double)visit;
}

bool UCTNode::isFullyExpanded() {
    return state.isFullyExpanded();
}

UCTNode* UCTNode::expand() {
    state.sortOrderedAvailableMoves();
    // state.printAvailableMoves();
    Point availableMove = state.getFirstAvailableMove();
    if (availableMove == Point(-1, -1)) return nullptr;
    State newState = state;
    newState.move(availableMove);
    newState.updateAvailableMoves();
    UCTNode* child = new UCTNode(newState, this, depth + 1);
    addChild(child);
    return child;
}

bool UCTNode::isTerminal() const {
    return state.isOver();
}

Point UCTNode::getMove() const {
    return state.getThisMove();
}

Point UCTNode::getMustMove() {
    return state.getMustMove();
}

int UCTNode::getDepth() const {
    return depth;
}

UCTNode::~UCTNode() {
    for (auto child : children) {
        delete child;
    }
}
