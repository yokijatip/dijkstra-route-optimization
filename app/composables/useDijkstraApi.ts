import type {
  BenchmarkRequest,
  BenchmarkResponse,
  CompareResponse,
  DatasetDetail,
  DatasetSummary,
  ExperimentHistoryItem,
  FirebaseStatus,
  RouteResult
} from '~/types/api'

export function useDijkstraApi() {
  const config = useRuntimeConfig()
  const apiBase = String(config.public.apiBase).replace(/\/$/, '')

  function request<T>(path: string, options?: Parameters<typeof $fetch<T>>[1]) {
    return $fetch<T>(`${apiBase}${path}`, options)
  }

  return {
    listDatasets: () => request<DatasetSummary[]>('/api/datasets'),
    getDataset: (datasetId: string) => request<DatasetDetail>(`/api/datasets/${datasetId}`),
    compare: (payload: {
      datasetId: string
      sourceId: string
      destinationId: string
    }) => request<CompareResponse>('/api/routes/compare', {
      method: 'POST',
      body: payload
    }),
    route: (algorithm: 'standard' | 'optimized', payload: {
      datasetId: string
      sourceId: string
      destinationId: string
    }) => request<RouteResult>(`/api/routes/${algorithm}`, {
      method: 'POST',
      body: payload
    }),
    createBenchmark: (payload: BenchmarkRequest) => request<BenchmarkResponse>('/api/benchmarks', {
      method: 'POST',
      body: payload
    }),
    getBenchmark: (experimentId: string) => request<BenchmarkResponse>(`/api/benchmarks/${experimentId}`),
    listExperiments: () => request<ExperimentHistoryItem[]>('/api/experiments'),
    getFirebaseStatus: () => request<FirebaseStatus>('/api/firebase/status'),
    exportBenchmarkUrl: (experimentId: string) => `${apiBase}/api/experiments/${experimentId}/export.csv`
  }
}
