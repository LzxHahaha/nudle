#pragma once

#include <algorithm>
#include <cmath>
#include "disjoint-set.h"

// threshold function
#define THRESHOLD(size, c) (c/size)

typedef struct
{
	float w;
	int a, b;
} edge;

bool operator<(const edge &a, const edge &b)
{
	return a.w < b.w;
}

/*
* Segment a graph
*
* Returns a disjoint-set forest representing the segmentation.
*
* nu_vertices: number of vertices in graph.
* nu_edges: number of edges in graph
* edges: array of edges.
* c: constant for treshold function.
*/
universe *segment_graph(int nu_vertices, int nu_edges, edge *edges, float c)
{
	// sort edges by weight
	std::sort(edges, edges + nu_edges);

	// make a disjoint-set forest
	universe *u = new universe(nu_vertices);

	// init thresholds
	float *threshold = new float[nu_vertices];
	for (int i = 0; i < nu_vertices; i++)
		threshold[i] = THRESHOLD(1, c);

	// for each edge, in non-decreasing weight order...
	for (int i = 0; i < nu_edges; i++)
	{
		edge *pedge = &edges[i];

		// components conected by this edge
		int a = u->find(pedge->a);
		int b = u->find(pedge->b);
		if (a != b)
		{
			if ((pedge->w <= threshold[a]) &&
				(pedge->w <= threshold[b]))
			{
				u->join(a, b);
				a = u->find(a);
				threshold[a] = pedge->w + THRESHOLD(u->size(a), c);
			}
		}
	}

	// free up
	delete threshold;
	return u;
}
