## Optimal Path based on Distance, Time, Roads

### Problem Statement

Write a program using below constraints:-
    - Dataset of major highways segments of the US and other are provided as a graph nodes.
    - Dataset of cities and towns with corresponding lat-lon positions is provided.
    - We have to find the optimal paths from source to destination with different cost functions:-
        - segments, distance, time & delivery(explanation provided in assignment)

### Design Decisions

- Implemented heuristic for all four different cost functions:-
    - Code flow is almost similar, for all four function implemented A* using Algorithm-3. Just inserted different heuristics according to the cost function.
    - Cost Function's heuristic explanation(applied on any road segment):-
        - **SEGMENTS** - used h(s) as the haversine distance(calculated using lat-lon) between destination of the segment and goal destination.
        - **DISTANCE** - used h(s) as the haversine distance from destination of the segment + segment length
        - **TIME** - used h(s) as the ((haversine distance from destination of the segment)/max_speed) + (segment length/ segment speed limit). Max_speed is the maximum speed of any segment in the whole list.
        - **DELIVERY** - used h(s) as the (haversine distance from destination of the segment + segment length) * 2 * probability + (segment length/ segment speed limit)

    - Calculating heuristic cost function of the missing destination in cities dataset:-
        - Some towns don't have (lat,lon), which hinders us from calculating haversine distance.
        - So we have to use, heuristic cost of the source node of the segment - segment_length.
        - Sometimes we don't know the heuristic cost of source also, so we keep passing the latest heuristic cost we are aware of to the successors.

### Solution Review

- Final Solution
    - __Abstraction Used__, A*, Algorithm 3
    - __Cost Function__, Cost function is the distance, time, or the delivery time of segment as given in the road-segments file.
    - __Goal State__, Destination asked to reach via arguments
    - __Successor Function__, returns all the possible segments from the destination of last segment or the starting source. It does not return the segments which are present in duplicate_segments list.
