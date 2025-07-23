import math
from collections import deque

class GraphAlgorithm:
    def __init__(self, edges, V, E):
        self.edges = edges  # List of tuples (u, v)
        self.V = V  # Number of vertices
        self.E = E  # Number of edges
        self.d = 2 * math.ceil(E / V) + 1  # Calculate d
        self.adjacency_matrix = []  # 2V x (d+1) matrix
        self.outer_loop_count = 0  # Track outer loop cycles
        self.processed_queue_vertices = []  # List of vertices already processed in queue
        self.vertex_bits = [0] * (V + 1)  # Array from 0 to V, index 0 unused, bits for vertices 1 to V
        self.processed_rows = set()  # Track which rows have been processed
        
        self.adj_list = {i: [] for i in range(1, V + 1)}
        for u, v in edges:
            self.adj_list[u].append(v)
        
        self._create_adjacency_matrix()
    
    def _create_adjacency_matrix(self):
        """Create the 2V x (d+1) adjacency matrix with padding and overflow handling"""
        self.adjacency_matrix = []
        row_count = 0
        
        for vertex in range(1, self.V + 1):
            outgoing_edges = self.adj_list[vertex]
            
            # Process edges for this vertex
            edges_processed = 0
            while edges_processed < len(outgoing_edges):
                current_row = [vertex]  # First element is the vertex this row belongs to
                
                # Fill current row with up to d edges
                for i in range(self.d):
                    if edges_processed < len(outgoing_edges):
                        current_row.append(outgoing_edges[edges_processed])
                        edges_processed += 1
                    else:
                        current_row.append(0)  # Dummy edge
                
                self.adjacency_matrix.append(current_row)
                row_count += 1
            
            # If vertex has no outgoing edges, add one row with vertex marker
            if len(outgoing_edges) == 0:
                dummy_row = [vertex] + [0] * self.d  # Vertex marker + dummy edges
                self.adjacency_matrix.append(dummy_row)
                row_count += 1
        
        # Pad matrix to exactly 2V rows with dummy edges (vertex marker = 0)
        while row_count < 2 * self.V:
            dummy_row = [0] + [0] * self.d  # All dummy (vertex marker = 0)
            self.adjacency_matrix.append(dummy_row)
            row_count += 1
    
    def run_algorithm(self, start_vertex, n, compaction_del):
        self.outer_loop_count = 0
        queue = deque()
        vertex_row_map = self._create_vertex_row_mapping()

        self.processed_queue_vertices = []
        self.vertex_bits = [0] * (self.V + 1)
        self.processed_rows = set()

        # Start with the starting vertex
        current_vertex = start_vertex
        current_vertex_row_index = 0
        iteration_count = 0

        # Insert source vertex into processed list and set bit marker
        if current_vertex not in self.processed_queue_vertices:
            self.processed_queue_vertices.append(current_vertex)
        self.vertex_bits[current_vertex] = 1

        print(f"Starting algorithm with vertex {start_vertex}")
        print(f"d = {self.d}, n = {n}, compaction_del = {compaction_del}")
        print(f"Adjacency matrix size: {len(self.adjacency_matrix)} x {self.d + 1}")
        print(f"Initial vertex bits: {self.vertex_bits[1:]}")
        print()

        while True:
            self.outer_loop_count += 1
            iteration_count += 1

            print(f"=== Outer Loop Iteration {self.outer_loop_count} ===")
            print(f"Current vertex to process: {current_vertex}")

            # Add edges from current vertex to queue (process one row only)
            edges_added = False
            if current_vertex in vertex_row_map:
                rows_for_vertex = vertex_row_map[current_vertex]
                row_to_process = None
                for row_idx in rows_for_vertex:
                    if row_idx not in self.processed_rows:
                        row_to_process = row_idx
                        break

                if row_to_process is not None and row_to_process < len(self.adjacency_matrix):
                    self.processed_rows.add(row_to_process)
                    original_row = self.adjacency_matrix[row_to_process]
                    vertex_marker = original_row[0]
                    edges_in_row = original_row[1:]
                    processed_edges = self._process_row_with_vertex_bits(edges_in_row)
                    for edge in processed_edges:
                        queue.append(edge)
                    edges_added = True
                    print(f"Processing row {row_to_process} (vertex marker: {vertex_marker})")
                    print(f"Original edges: {edges_in_row}")
                    print(f"Processed edges: {processed_edges}")
                    print(f"Vertex bits after processing: {self.vertex_bits[1:]}")
                else:
                    print(f"No more unprocessed rows for vertex {current_vertex}")

            all_rows_done = all(row_idx in self.processed_rows for row_idx in vertex_row_map.get(current_vertex, []))

            if all_rows_done:
                if current_vertex not in self.processed_queue_vertices:
                    self.processed_queue_vertices.append(current_vertex)
                self.vertex_bits[current_vertex] = 1  # Set bit marker for processed vertex
                if len(self.processed_queue_vertices) == self.V:
                    print("All vertices processed in queue. Algorithm complete.")
                    break
                if queue:
                    next_vertex = queue.popleft()
                    print(f"All rows for vertex {current_vertex} processed. Switching to next vertex from queue: {next_vertex}")
                    if next_vertex != 0:
                        current_vertex = next_vertex
                    else:
                        print("Top element is dummy, doing nothing")
                elif not edges_added:
                    print("No edges added and queue is empty - algorithm may be complete")
                    break

            print(f"Current queue: {list(queue)}")
            print(f"Queue size: {len(queue)}")

            if iteration_count % n == 0:
                print(f"\n--- Compaction at iteration {iteration_count} ---")
                self._compact_queue(queue, compaction_del)
                print(f"Queue after compaction: {list(queue)}")

            if len(queue) == 0 and all_rows_done:
                break

        print()
        print(f"\nAlgorithm completed after {self.outer_loop_count} outer loop iterations")
        print(f"Final processed queue vertices: {self.processed_queue_vertices}")
        print(f"Final vertex bits: {self.vertex_bits[1:]}")
        print(f"Total rows processed: {len(self.processed_rows)}")
        return self.outer_loop_count
    
    def _create_vertex_row_mapping(self):
        """Create mapping from vertex to its rows in adjacency matrix"""
        vertex_row_map = {}
        current_row = 0
        
        for vertex in range(1, self.V + 1):
            vertex_row_map[vertex] = []
            outgoing_edges = self.adj_list[vertex]
            
            if len(outgoing_edges) == 0:
                vertex_row_map[vertex].append(current_row)
                current_row += 1
            else:
                edges_processed = 0
                while edges_processed < len(outgoing_edges):
                    vertex_row_map[vertex].append(current_row)
                    edges_processed += self.d
                    current_row += 1
        
        return vertex_row_map
    
    def _process_row_with_vertex_bits(self, row):
        """
        Process a row by checking vertex bits and updating them.
        If vertex bit is 0, set it to 1 and keep the vertex.
        If vertex bit is 1, convert to dummy edge (0).
        """
        processed_row = []
        
        for vertex in row:
            if vertex == 0:  # Already a dummy edge
                processed_row.append(0)
            elif 1 <= vertex <= self.V:  # Valid vertex
                if self.vertex_bits[vertex] == 0:
                    # First time seeing this vertex, set bit to 1 and keep it
                    self.vertex_bits[vertex] = 1
                    processed_row.append(vertex)
                    print(f"  Vertex {vertex}: bit 0->1, keeping vertex")
                else:
                    # Already processed this vertex, convert to dummy edge
                    processed_row.append(0)
                    print(f"  Vertex {vertex}: bit already 1, converting to dummy edge")
            else:
                # Invalid vertex, treat as dummy
                processed_row.append(0)
                print(f"  Invalid vertex {vertex}, converting to dummy edge")
        
        return processed_row
    
    def _compact_queue(self, queue, compaction_del):
        """Perform compaction: move real elements to front, remove excess"""
        # Convert to list for easier manipulation
        queue_list = list(queue)
        queue.clear()
        
        # Separate real and dummy elements
        real_elements = [x for x in queue_list if x != 0]
        dummy_elements = [x for x in queue_list if x == 0]
        
        # Add real elements first, then dummies
        compacted = real_elements + dummy_elements
        
        # Keep only first compaction_del elements
        compacted = compacted[:compaction_del]
        
        # Put back in queue
        for element in compacted:
            queue.append(element)
        
        print(f"Compaction: {len(queue_list)} -> {len(compacted)} elements")
    
    def print_adjacency_matrix(self):
        """Print the adjacency matrix for debugging"""
        print("Adjacency Matrix (2V x (d+1)):")
        print("Format: [vertex_marker, edge1, edge2, ..., edged]")
        for i, row in enumerate(self.adjacency_matrix):
            vertex_marker = row[0]
            edges = row[1:]
            print(f"Row {i}: [vertex:{vertex_marker}] {edges}")
        print()
    
    def get_processed_vertices(self):
        """Return the list of processed queue vertices"""
        return self.processed_queue_vertices
    
    def get_vertex_bits(self):
        """Return the vertex bits array (excluding index 0)"""
        return self.vertex_bits[1:]
    
    def reset_tracking(self):
        """Reset the vertex tracking arrays"""
        self.processed_queue_vertices = []
        self.vertex_bits = [0] * (self.V + 1)
        self.processed_rows = set()
    
    def get_outer_loop_count(self):
        """Return the total number of outer loop iterations"""
        return self.outer_loop_count


def main():
    
    edges = [(1, 2), (2, 5), (3, 4), (3, 5), (4, 1), (5, 2), (5,3)]
    V = 5  
    E = 7  
    
    algorithm = GraphAlgorithm(edges, V, E)
    
    print("=== Algorithm Setup ===")
    print(f"Vertices: {V}, Edges: {E}")
    print(f"d = 2 * ceil({E}/{V}) + 1 = {algorithm.d}")
    print()
    
    
    algorithm.print_adjacency_matrix()
    
    # Run algorithm
    start_vertex = 1
    n = 3  # Compaction
    compaction_del = 5  # Keep max elem after compaction
    
    cycle_count = algorithm.run_algorithm(start_vertex, n, compaction_del)
    
    print(f"\nFinal outer loop cycle count: {cycle_count}")


if __name__ == "__main__":
    main()