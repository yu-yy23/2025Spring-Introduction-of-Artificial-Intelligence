/********************************************************
*	Point.h : 棋盘点类                                  *
*	张永锋                                              *
*	zhangyf07@gmail.com                                 *
*	2014.5                                              *
*********************************************************/

#ifndef POINT_H_
#define POINT_H_
#include <iostream>

class Point
{
public:
	int x;
	int y;

	Point(int x, int y)
	{
		this->x = x;
		this->y = y;
	}

	Point(const Point& p)
	{
		this->x = p.x;
		this->y = p.y;
	}

	void operator=(const Point& p) {
		this->x = p.x;
		this->y = p.y;
	}

	bool operator==(const Point& p) const {
		return (this->x == p.x && this->y == p.y);
	}

	bool operator!=(const Point& p) const {
		return !(*this == p);
	}

	friend std::ostream& operator<<(std::ostream& out, const Point& p) {
		out << "(" << p.x << ", " << p.y << ")";
		return out;
	}
};

#endif
