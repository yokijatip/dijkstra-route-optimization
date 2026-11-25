export interface GraphNode {
  id: string
  name: string
  latitude?: number | null
  longitude?: number | null
}

export interface GraphEdge {
  from: string
  to: string
  weight: number
  bidirectional: boolean
}

export interface DatasetSummary {
  id: string
  name: string
  version: string
  description: string
  source?: string
  region?: string
  networkType?: string
  weightUnit?: string
  nodeCount: number
  edgeCount: number
  validationStatus: string
}

export interface DatasetDetail extends DatasetSummary {
  nodes: GraphNode[]
  edges: GraphEdge[]
}

export interface RouteResult {
  algorithm: 'standard' | 'optimized'
  algorithmVersion: string
  datasetId: string
  datasetVersion: string
  sourceId: string
  destinationId: string
  status: 'success' | 'unreachable' | 'error'
  path: string[]
  pathLength: number
  totalCost: number | null
  executionTimeNs: number
  executionTimeMs: number
  visitedNodes: number
  processedEdges: number
}

export interface CompareResponse {
  datasetId: string
  datasetVersion: string
  sourceId: string
  destinationId: string
  standard: RouteResult
  optimized: RouteResult
  correctnessMatch: boolean
  tolerance: number
  improvement: {
    executionTimePct: number
    visitedNodesPct: number
    processedEdgesPct: number
  }
}

export type BenchmarkPairMode = 'preset' | 'random'

export interface BenchmarkRequest {
  datasetId: string
  testCaseCount: number
  pairMode: BenchmarkPairMode
  warmupRuns: number
  repeatCount: number
  randomSeed?: number | null
  tolerance?: number
}

export interface AggregateMetrics {
  runCount: number
  successCount: number
  unreachableCount: number
  meanExecutionTimeNs: number
  medianExecutionTimeNs: number
  minimumExecutionTimeNs: number
  maximumExecutionTimeNs: number
  standardDeviationExecutionTimeNs: number
  meanExecutionTimeMs: number
  meanVisitedNodes: number
  meanProcessedEdges: number
  meanPathLength: number
}

export interface BenchmarkSummary {
  experimentId: string
  datasetId: string
  datasetVersion: string
  testCaseCount: number
  repeatCount: number
  warmupRuns: number
  pairMode: BenchmarkPairMode
  randomSeed: number | null
  correctnessMismatchCount: number
  standard: AggregateMetrics
  optimized: AggregateMetrics
  improvement: {
    executionTimePct: number
    visitedNodesPct: number
    processedEdgesPct: number
  }
  createdAt: string
}

export interface BenchmarkRun {
  id: string
  experimentId: string
  datasetId: string
  datasetVersion: string
  sourceId: string
  destinationId: string
  algorithm: 'standard' | 'optimized'
  algorithmVersion: string
  executionTimeNs: number
  executionTimeMs: number
  visitedNodes: number
  processedEdges: number
  totalCost: number | null
  path: string[]
  pathLength: number
  status: 'success' | 'unreachable' | 'error'
  createdAt: string
}

export interface BenchmarkResponse {
  summary: BenchmarkSummary
  runs: BenchmarkRun[]
}

export interface ExperimentHistoryItem {
  experimentId: string
  datasetId: string
  datasetVersion: string
  testCaseCount: number
  repeatCount: number
  correctnessMismatchCount: number
  createdAt: string
}

export interface FirebaseStatus {
  enabled: boolean
  connected: boolean
  mode: 'firestore' | 'memory'
  message: string
}
