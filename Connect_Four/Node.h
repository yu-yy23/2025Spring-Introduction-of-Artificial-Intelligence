#include <vector>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include "State.h"

class SearchTree;

class UCTNode {
private:
    int visit;
    int win;
    State state;
    UCTNode* parent;
    std::vector<UCTNode*> children;
    int depth;
    // std::vector<int> tried;
public:
    UCTNode(const State& s, UCTNode* p, int d);
    void addChild(UCTNode* child);
    void update(int result);
    double getScore() const;
    bool isFullyExpanded();
    UCTNode* expand();
    bool isTerminal() const;
    Point getMove() const;
    Point getMustMove();
    int getDepth() const;
    ~UCTNode();
    friend class SearchTree;
};