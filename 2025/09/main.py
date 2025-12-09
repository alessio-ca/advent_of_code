from utils import read_input, CoordTuple
from itertools import combinations
import numpy as np
from scipy.spatial.distance import pdist

Edge = tuple[int, int, int]  # (x, y_min, y_max)

def create_rectangle(u: np.ndarray, v: np.ndarray) -> tuple[int,int,int,int]:
    """Create a rectangle defined by two corner points u and v (inclusive)."""
    x_min, y_min = np.minimum(u, v)
    x_max, y_max = np.maximum(u, v)
    return x_min, x_max, y_min, y_max 



def get_edges(polygon: list[CoordTuple]) -> tuple[list[Edge], list[Edge]]:
    """Extract horizontal and vertical edges from a polygon defined by its vertices."""
    h_edges = []
    v_edges = []
    x0, y0 = polygon[0]
    for point in polygon[1:] + [polygon[0]]:
        x, y = point
        if x == x0:
            # Vertical edge
            v_edges.append((x, min(y0, y), max(y0, y)))
        else:
            # Horizontal edge
            h_edges.append((y, min(x0, x), max(x0, x)))
        
        x0, y0 = x, y
    return h_edges, v_edges



def is_point_in_polygon(point: CoordTuple, edges: list[tuple[int,int,int]]) -> bool:
    """Determine if a point is inside a polygon using the ray-casting algorithm.
    Use only vertical edges for simplicity. Point on edge is considered inside."""
    x, y = point
    crossings = 0
    for edge_x, y_min, y_max in edges:
        if x > edge_x and y_min <= y < y_max:
            crossings += 1
    return crossings % 2 == 1

def is_rectangle_in_polygon(u: CoordTuple, v: CoordTuple, vertex_set: set[CoordTuple], v_edges: list[Edge], h_edges: list[Edge]) -> bool:
    """Check if the rectangle defined by corners u and v is fully contained within the polygon.
    """
    x_min, x_max, y_min, y_max = create_rectangle(np.array(u), np.array(v))
    rec_vertexes = [ (x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max) ]
    
    for v in rec_vertexes:
        if v not in vertex_set:
            if not is_point_in_polygon(v, v_edges):
                return False
    
    # Check for edge crossing
    for x_edge, y1, y2 in v_edges:
        if x_min < x_edge < x_max: 
            if not (y2 <= y_min or y1 >= y_max): 
                return False
    for y_edge, x1, x2 in h_edges:
        if y_min < y_edge < y_max: 
            if not (x2 <= x_min or x1 >= x_max):
                return False
    return True

def main(filename: str):
    data = np.array([list(map(int, line.split(','))) for line in read_input(filename)], dtype=np.int64)
    def rectangle_area(u: np.ndarray, v: np.ndarray) -> int:
        return np.prod(abs(u - v) + 1)
    areas = pdist(data, metric=rectangle_area).astype(np.int64)
    print(f"Result of part 1: {areas.max()}")
   
   
    polygon = data.tolist()
    h_edges, v_edges = get_edges(polygon)
    vertex_set = set(map(tuple, polygon))
    areas_2 = []
    for u, v in combinations(polygon, 2):
        if is_rectangle_in_polygon(u,v, vertex_set, v_edges, h_edges):
            areas_2.append(rectangle_area(np.array(u), np.array(v)))

    print(f"Result of part 2: {max(areas_2)}")

if __name__ == "__main__":
    main("2025/09/input.txt")
