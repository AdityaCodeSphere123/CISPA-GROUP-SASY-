// Inside the TEE
struct DNormalizedGraph {
    int n;  // Number of vertices
    int d;  // Fixed degree for each vertex
    OKVS adjacencyLists;  // Stores d neighbors for each vertex
}

// Initialize OKVS with d-normalized adjacency lists
function initializeGraph(G, d):
    for each vertex v in G:
        realNeighbors = getNeighbors(v)
        normalizedList = new array of size d
        
        // Copy real neighbors
        for i from 0 to min(realNeighbors.length, d)-1:
            normalizedList[i] = realNeighbors[i]
            
        // Pad with dummy vertices if needed
        for i from realNeighbors.length to d-1:
            normalizedList[i] = DUMMY_VERTEX
            
        // Store in OKVS with vertex ID as key
        adjacencyLists.put(v, normalizedList)

function obliviousBFS(graph, startVertex):
    // Initialize data structures
    queue = new ObliviousQueue()
    visited = new ObliviousArray(graph.n) // Initialized to false
    distance = new ObliviousArray(graph.n) // Initialized to INFINITY
    
    // Enqueue the start vertex
    queue.enqueue(startVertex)
    visited.obliviousWrite(startVertex, true)
    distance.obliviousWrite(startVertex, 0)
    
    while not queue.isEmpty():
        currentVertex = queue.dequeue()
        currentDist = distance.obliviousRead(currentVertex)
        
        // Get neighbors using OKVS access
        neighbors = graph.adjacencyLists.obliviousGet(currentVertex)
        
        // Process all d neighbors (real and dummy)
        for i from 0 to graph.d-1:
            neighbor = neighbors[i]
            
            // Skip dummy vertices
            isDummy = (neighbor == DUMMY_VERTEX)
            
            // Oblivious operations regardless of whether vertex is dummy
            isVisited = visited.obliviousRead(neighbor)
            shouldProcess = !isDummy && !isVisited
            
            // Obliviously update data structures
            visited.obliviousConditionalWrite(neighbor, true, shouldProcess)
            distance.obliviousConditionalWrite(neighbor, currentDist + 1, shouldProcess)
            queue.obliviousConditionalEnqueue(neighbor, shouldProcess)
    
    return distance

function obliviousGet(key):
    // Access every entry in the store with constant pattern
    result = null
    for each k, v in store:
        // Only actually capture the value when k matches key
        if k == key:
            result = v
    return result

function obliviousConditionalWrite(index, newValue, condition):
    currentValue = this.obliviousRead(index)
    valueToWrite = condition ? newValue : currentValue
    this.obliviousWrite(index, valueToWrite)