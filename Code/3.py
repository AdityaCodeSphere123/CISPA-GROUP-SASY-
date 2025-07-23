import math
import random
from collections import deque

class GraphAlgorithm:
    def __init__(self, edges, V, E):
        self.edges = edges  # List of tuples (u, v)
        self.V = V  # Number of vertices
        self.E = E  # Number of edges
        self.d = math.ceil(2 * E / V) + 1  # Updated d calculation
        self.dummy_row_count = 0  # Count rows with all zeros
        self.adjacency_matrix = []  # 2V x (d+1) matrix
        self.outer_loop_count = 0  # Track outer loop cycles
        self.processed_queue_vertices = []  # List of vertices already processed in queue
        self.vertex_bits = [0] * (V + 1)  # Bits for vertices 1 to V
        self.processed_rows = set()  # Track which rows have been processed
        self.max_queue_size = 0  # Track maximum queue size ever reached
        self.max_real_queue_size = 0  # Track maximum real (non-dummy) entries in queue

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
            edges_processed = 0

            while edges_processed < len(outgoing_edges):
                current_row = [vertex]
                for i in range(self.d):
                    if edges_processed < len(outgoing_edges):
                        current_row.append(outgoing_edges[edges_processed])
                        edges_processed += 1
                    else:
                        current_row.append(0)
                self.adjacency_matrix.append(current_row)
                row_count += 1

            if len(outgoing_edges) == 0:
                dummy_row = [vertex] + [0] * self.d
                self.adjacency_matrix.append(dummy_row)
                self.dummy_row_count += 1  # Count dummy row
                row_count += 1

        while row_count < 2 * self.V:
            dummy_row = [0] + [0] * self.d
            self.adjacency_matrix.append(dummy_row)
            self.dummy_row_count += 1  # Count dummy row
            row_count += 1

    def run_algorithm(self, start_vertex, n, compaction_del):
        self.outer_loop_count = 0
        queue = deque()
        vertex_row_map = self._create_vertex_row_mapping()

        self.processed_queue_vertices = []
        self.vertex_bits = [0] * (self.V + 1)
        self.processed_rows = set()
        self.max_queue_size = 0  # Reset max queue size for new run
        self.max_real_queue_size = 0  # Reset max real queue size for new run

        current_vertex = start_vertex
        iteration_count = 0

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

            edges_added = False
            if current_vertex in vertex_row_map:
                rows_for_vertex = vertex_row_map[current_vertex]
                row_to_process = None
                for row_idx in rows_for_vertex:
                    if row_idx not in self.processed_rows:
                        row_to_process = row_idx
                        break

                if row_to_process is not None:
                    self.processed_rows.add(row_to_process)
                    original_row = self.adjacency_matrix[row_to_process]
                    vertex_marker = original_row[0]
                    edges_in_row = original_row[1:]
                    
                    # Process row and get which vertices were real before processing
                    processed_edges, real_vertices_added = self._process_row_with_vertex_bits(edges_in_row)
                    
                    # Add edges to queue
                    for edge in processed_edges:
                        queue.append(edge)
                    
                    # Update max real queue size based on real vertices that were added
                    if len(real_vertices_added) > 0:
                        # Count current real entries in queue (these would be from previous iterations)
                        current_real_in_queue = 0
                        for x in queue:
                            if x != 0 and 1 <= x <= self.V and self.vertex_bits[x] == 0:
                                current_real_in_queue += 1
                        
                        # The max real queue size should consider the moment when real vertices were added
                        # Since real_vertices_added were just processed, they're no longer "real" in queue
                        # But we track the peak that occurred when they were added
                        peak_real_size = current_real_in_queue + len(real_vertices_added)
                        if peak_real_size > self.max_real_queue_size:
                            self.max_real_queue_size = peak_real_size
                    
                    edges_added = True
                    print(f"Processing row {row_to_process} (vertex marker: {vertex_marker})")
                    print(f"Original edges: {edges_in_row}")
                    print(f"Processed edges: {processed_edges}")
                    print(f"Real vertices added: {real_vertices_added}")
                    print(f"Vertex bits after processing: {self.vertex_bits[1:]}")
                else:
                    print(f"No more unprocessed rows for vertex {current_vertex}")

            all_rows_done = all(row_idx in self.processed_rows for row_idx in vertex_row_map.get(current_vertex, []))

            if all_rows_done:
                if current_vertex not in self.processed_queue_vertices:
                    self.processed_queue_vertices.append(current_vertex)
                self.vertex_bits[current_vertex] = 1
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
            
            # Count real (non-dummy and unprocessed) entries in queue
            # Real entries are those that are: 1) non-zero AND 2) not yet processed (vertex_bit = 0)
            real_entries = []
            for x in queue:
                if x != 0 and 1 <= x <= self.V and self.vertex_bits[x] == 0:
                    real_entries.append(x)
            
            real_queue_size = len(real_entries)
            
            # Update max queue size if current size is larger
            if len(queue) > self.max_queue_size:
                self.max_queue_size = len(queue)
            
            # Update max real queue size if current real size is larger
            if real_queue_size > self.max_real_queue_size:
                self.max_real_queue_size = real_queue_size
                
            print(f"Real entries in queue (unprocessed): {real_entries}")
            print(f"Real queue size: {real_queue_size}")
            print(f"Max queue size ever reached: {self.max_queue_size}")
            print(f"Max real queue size ever reached: {self.max_real_queue_size}")

            if iteration_count % n == 0:
                print(f"\n--- Compaction at iteration {iteration_count} ---")
                self._compact_queue(queue, compaction_del)
                print(f"Queue after compaction: {list(queue)}")

            if len(queue) == 0 and all_rows_done:
                break

        print(f"\nAlgorithm completed after {self.outer_loop_count} outer loop iterations")
        print(f"Final processed queue vertices: {self.processed_queue_vertices}")
        print(f"Final vertex bits: {self.vertex_bits[1:]}")
        print(f"Total rows processed: {len(self.processed_rows)}")
        print(f"Maximum queue size ever reached: {self.max_queue_size}")
        print(f"Maximum real queue size ever reached: {self.max_real_queue_size}")
        return self.outer_loop_count

    def _create_vertex_row_mapping(self):
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
        processed_row = []
        real_vertices_added = []  # Track which vertices were kept as real

        for vertex in row:
            if vertex == 0:
                processed_row.append(0)
            elif 1 <= vertex <= self.V:
                if self.vertex_bits[vertex] == 0:
                    self.vertex_bits[vertex] = 1
                    processed_row.append(vertex)
                    real_vertices_added.append(vertex)  # This was a real vertex we kept
                    print(f"  Vertex {vertex}: bit 0->1, keeping vertex")
                else:
                    processed_row.append(0)
                    print(f"  Vertex {vertex}: bit already 1, converting to dummy edge")
            else:
                processed_row.append(0)
                print(f"  Invalid vertex {vertex}, converting to dummy edge")

        return processed_row, real_vertices_added

    def _compact_queue(self, queue, compaction_del):
        queue_list = list(queue)
        queue.clear()

        real_elements = [x for x in queue_list if x != 0]
        dummy_elements = [x for x in queue_list if x == 0]

        compacted = real_elements + dummy_elements
        compacted = compacted[:compaction_del]

        for element in compacted:
            queue.append(element)

        print(f"Compaction: {len(queue_list)} -> {len(compacted)} elements")

    def print_adjacency_matrix(self):
        print("Adjacency Matrix (2V x (d+1)):")
        print("Format: [vertex_marker, edge1, edge2, ..., edged]")
        for i, row in enumerate(self.adjacency_matrix):
            vertex_marker = row[0]
            edges = row[1:]
            print(f"Row {i}: [vertex:{vertex_marker}] {edges}")
        print()

    def get_processed_vertices(self):
        return self.processed_queue_vertices

    def get_vertex_bits(self):
        return self.vertex_bits[1:]

    def get_outer_loop_count(self):
        return self.outer_loop_count

    def get_dummy_row_count(self):
        return self.dummy_row_count

    def get_max_queue_size(self):
        return self.max_queue_size

    def get_max_real_queue_size(self):
        return self.max_real_queue_size

    def reset_tracking(self):
        self.processed_queue_vertices = []
        self.vertex_bits = [0] * (self.V + 1)
        self.processed_rows = set()
        self.max_queue_size = 0  # Reset max queue size
        self.max_real_queue_size = 0  # Reset max real queue size

def generate_large_test_case(V, target_E):
    """
    Generate a well-connected graph with V vertices and approximately target_E edges.
    Ensures the graph is strongly connected and has good distribution of edges.
    """
    edges = []
    random.seed(42)  # For reproducible results
    
    # Ensure we have enough edges to connect all vertices
    min_edges_needed = V - 1
    if target_E < min_edges_needed:
        print(f"Warning: target_E ({target_E}) is less than minimum needed for connectivity ({min_edges_needed})")
        target_E = min_edges_needed
    
    # Step 1: Create a spanning tree to ensure basic connectivity
    # This guarantees all vertices are reachable
    print(f"Creating spanning tree with {V-1} edges...")
    for i in range(2, V + 1):
        parent = random.randint(1, i - 1)
        edges.append((parent, i))
    
    edge_set = set(edges)
    print(f"Spanning tree created. Current edges: {len(edges)}")
    
    # Step 2: Add additional edges to strengthen connectivity
    # Focus on creating a well-connected graph
    remaining_edges = target_E - (V - 1)
    print(f"Adding {remaining_edges} more edges for better connectivity...")
    
    attempts = 0
    max_attempts = remaining_edges * 5  # Increase attempts for better coverage
    
    while len(edges) < target_E and attempts < max_attempts:
        u = random.randint(1, V)
        v = random.randint(1, V)
        
        # Avoid self-loops and duplicate edges (both directions)
        if u != v and (u, v) not in edge_set and (v, u) not in edge_set:
            edges.append((u, v))
            edge_set.add((u, v))
            edge_set.add((v, u))  # Mark both directions to avoid reverse duplicates
        
        attempts += 1
    
    # Step 3: Verify connectivity by checking if we can build adjacency list
    adj_list_check = {i: [] for i in range(1, V + 1)}
    for u, v in edges:
        adj_list_check[u].append(v)
    
    # Count vertices with outgoing edges
    vertices_with_edges = sum(1 for v in range(1, V + 1) if len(adj_list_check[v]) > 0)
    
    print(f"Generated graph with {len(edges)} edges (target was {target_E})")
    print(f"Vertices with outgoing edges: {vertices_with_edges}/{V}")
    print(f"Graph density: {len(edges)/(V*(V-1)/2)*100:.2f}% of maximum possible edges")
    
    # Additional check: ensure no isolated vertices by adding more edges if needed
    isolated_vertices = [v for v in range(1, V + 1) if len(adj_list_check[v]) == 0]
    if isolated_vertices:
        print(f"Warning: Found {len(isolated_vertices)} vertices with no outgoing edges")
        print(f"Isolated vertices: {isolated_vertices[:10]}...")  # Show first 10
        
        # Add edges from isolated vertices to random connected vertices
        for isolated_v in isolated_vertices:
            if len(edges) < target_E:
                # Find a random vertex that has edges
                connected_vertices = [v for v in range(1, V + 1) if len(adj_list_check[v]) > 0]
                if connected_vertices:
                    target_v = random.choice(connected_vertices)
                    if (isolated_v, target_v) not in edge_set and (target_v, isolated_v) not in edge_set:
                        edges.append((isolated_v, target_v))
                        edge_set.add((isolated_v, target_v))
                        edge_set.add((target_v, isolated_v))
                        adj_list_check[isolated_v].append(target_v)
    
    print(f"Final graph: {len(edges)} edges, all vertices connected")
    return edges

def main():
    print("=== SMALL TEST CASE ===")
    edges_small = [(1, 2), (2, 5), (3, 4), (3, 5), (4, 1), (5, 2), (5, 3)]
    V_small = 5
    E_small = 7

    algorithm_small = GraphAlgorithm(edges_small, V_small, E_small)

    print("=== Small Algorithm Setup ===")
    print(f"Vertices: {V_small}, Edges: {E_small}")
    print(f"d = ceil(2*{E_small}/{V_small}) + 1 = {algorithm_small.d}")
    print(f"Number of dummy rows (all zeros): {algorithm_small.get_dummy_row_count()}")
    print()

    algorithm_small.print_adjacency_matrix()

    start_vertex_small = 1
    n_small = 3
    compaction_del_small = 5

    cycle_count_small = algorithm_small.run_algorithm(start_vertex_small, n_small, compaction_del_small)

    print(f"\nSmall test - Final outer loop cycle count: {cycle_count_small}")
    print(f"Small test - Maximum queue size reached: {algorithm_small.get_max_queue_size()}")
    print(f"Small test - Maximum real queue size reached: {algorithm_small.get_max_real_queue_size()}")
    print("\n" + "="*60 + "\n")

    print("=== LARGE TEST CASE ===")
    V_large = 1000
    target_E_large = 1500
    
    print(f"Generating large test case with {V_large} vertices and ~{target_E_large} edges...")
    edges_large = generate_large_test_case(V_large, target_E_large)
    E_large = len(edges_large)

    algorithm_large = GraphAlgorithm(edges_large, V_large, E_large)

    print("=== Large Algorithm Setup ===")
    print(f"Vertices: {V_large}, Edges: {E_large}")
    print(f"d = ceil(2*{E_large}/{V_large}) + 1 = {algorithm_large.d}")
    print(f"Number of dummy rows (all zeros): {algorithm_large.get_dummy_row_count()}")
    print(f"Adjacency matrix size: {len(algorithm_large.adjacency_matrix)} x {algorithm_large.d + 1}")
    print()

    # Don't print the adjacency matrix for large case (too big)
    print("Skipping adjacency matrix print for large case (too big to display)")

    start_vertex_large = 1
    n_large = 10  # Compact every 1000 iterations for large case
    compaction_del_large = 100  # Keep max 100 elements after compaction

    print(f"Running large algorithm with start_vertex={start_vertex_large}, n={n_large}, compaction_del={compaction_del_large}")
    print("This may take a while for a graph this size...")
    print()

    cycle_count_large = algorithm_large.run_algorithm(start_vertex_large, n_large, compaction_del_large)

    print(f"\nLarge test - Final outer loop cycle count: {cycle_count_large}")
    print(f"Large test - Maximum queue size reached: {algorithm_large.get_max_queue_size()}")
    print(f"Large test - Maximum real queue size reached: {algorithm_large.get_max_real_queue_size()}")
    print(f"Large test - Total processed vertices: {len(algorithm_large.get_processed_vertices())}")

if __name__ == "__main__":
    main()
