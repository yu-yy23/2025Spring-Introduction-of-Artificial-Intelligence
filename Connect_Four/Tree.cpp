#include "Tree.h"
#include <iostream>

SearchTree::SearchTree(const int m, const int n, int** _board,
    const int* _top, const Point& lastP, const Point& proP)
    : M(m), N(n), prohibitedMove(proP) {
    root = new UCTNode(State(m, n, _board, _top, false, lastP, proP), nullptr, 0);
    root->state.updateAvailableMoves();
    srand(time(0));
    // std::cerr << "SearchTree initialized with root state." << std::endl;
}

Point SearchTree::Search() {
    // std::cerr << "Starting search..." << std::endl;
    clock_t startTime = clock();
    // int times = 0;
    // root->state.printState();
    Point mustWinMove = root->getMustMove();
    if (mustWinMove != Point(-1, -1)) {
        // std::cerr << "Must win move found: " << mustWinMove << std::endl;
        return mustWinMove;
    }
    while (static_cast<double>(clock() - startTime) < TIME_LIMIT) {
        // std::cerr << "Current times: " << ++times << std::endl;
        // std::cerr << "Current time: " << static_cast<double>(clock() - startTime) / CLOCKS_PER_SEC << std::endl;
        UCTNode* selectedNode = Select(root);
        double result = Simulate(selectedNode);
        Backup(selectedNode, result);
    }
    // std::cerr << "Search completed." << std::endl;
    // std::cerr << "Root visit times: " << root->visit << std::endl;
    UCTNode* bestChild = BestChild(root, 0.0);
    // std::cerr << "visit times:" << bestChild->visit << std::endl;
    // updateRoot(bestChild->getMove());
    return bestChild->getMove();
}

UCTNode* SearchTree::Select(UCTNode* node) {
    // std::cerr << "Tree policy..." << std::endl;
    // node->state.printState();
    // std::cerr << "Start node: " << node << std::endl;
    // while (!node->isTerminal() && node->getDepth() - root->getDepth() < MAX_DEPTH) {
    while (!node->isTerminal()) {
        // std::cerr << "Current node: " << node << std::endl;
        UCTNode* child = node->expand();
        if (child) {
            // std::cerr << "Child node: " << child << std::endl;
            return child;
        }
        node = BestChild(node, 1.2);
        // std::cerr << "Best child: " << node << std::endl;
    }
    // std::cerr << "Finish tree policy" << std::endl;
    return node;
}

int SearchTree::Simulate(UCTNode* node) {
    // std::cerr << "Default policy..." << std::endl;
    State state = node->state;
    // int times = 0;
    // state.printState();
    while (!state.isOver()) {
        // std::cerr << "Current times: " << ++times << std::endl;
        // Point mustWinMove = state.getMustWinMove();
        // if (mustWinMove != Point(-1, -1)) {
        //     state.move(mustWinMove);
        //     break;
        // }
        Point randomMove = state.getRandomMove();
        if (randomMove == Point(-1, -1)) {
            break;
        }
        state.move(randomMove);
        state.updateAvailableMoves();
        // std::cerr << "move: " << randomMove << std::endl;
    }
    // std::cerr << "Root state: " << std::endl;
    // root->state.printState();
    // std::cerr << "Finish default policy" << std::endl;
    return state.getResult();
}

UCTNode* SearchTree::BestChild(UCTNode* node, double c) {
    double bestScore = -1.0;
    UCTNode* bestChild = nullptr;
    for (auto child : node->children) {
        // if (c == 0.0) std::cerr << "Child node: " << child << std::endl;
        // if (c == 0.0) std::cerr << "Child move: " << child->getMove() << ", score: " << child->getScore() << std::endl;
        double score = child->getScore() + c * sqrt(2 * log(node->visit) / child->visit);
        if (score > bestScore) {
            bestScore = score;
            bestChild = child;
        }
    }
    return bestChild;
}

void SearchTree::Backup(UCTNode* node, int result) {
    // std::cerr << "Backup..." << std::endl;
    while (node) {
        node->update(result);
        node = node->parent;
    }
    // std::cerr << "Finish backup" << std::endl;
}

UCTNode* SearchTree::updateRoot(const Point& lastP) {
    UCTNode* newRoot = nullptr;
    // std::cerr << "lastP: " << lastP << std::endl;
    // std::cerr << "Size of children: " << root->children.size() << std::endl;
    for (auto child : root->children) {
        // std::cerr << "Child node this move: " << child->state.getThisMove() << std::endl;
        if (child->state.getThisMove() == lastP) {
            // std::cerr << "Found child node with matching last move." << std::endl;
            newRoot = child;
            continue;
        }
        // std::cerr << "Deleting child node: " << child << std::endl;
        delete child;
    }
    if (!newRoot) {
        // std::cerr << "Creating new root node." << std::endl;
        newRoot = new UCTNode(root->state, nullptr, 0);
        newRoot->state.move(lastP);
        newRoot->state.updateAvailableMoves();
    }
    newRoot->parent = nullptr;
    root->children.clear();
    // std::cerr << "Deleting old root node: " << root << std::endl;
    delete root;
    // std::cerr << "Setting new root node: " << newRoot << std::endl;
    root = newRoot;
    return root;
}

SearchTree::~SearchTree() {
    // std::cerr << "Deleting search tree..." << std::endl;
    delete root;
}