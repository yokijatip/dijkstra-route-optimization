<script setup lang="ts">
import type {
  BenchmarkPairMode,
  BenchmarkResponse,
  CompareResponse,
  DatasetDetail,
  DatasetSummary,
  ExperimentHistoryItem,
  FirebaseStatus,
  RouteResult
} from '~/types/api'

type AlgorithmMode = 'compare' | 'standard' | 'optimized'

const api = useDijkstraApi()
const apiBase = String(useRuntimeConfig().public.apiBase)

const datasets = ref<DatasetSummary[]>([])
const dataset = ref<DatasetDetail | null>(null)
const compareResult = ref<CompareResponse | null>(null)
const singleResult = ref<RouteResult | null>(null)
const sourceId = ref('')
const destinationId = ref('')
const selectedDatasetId = ref('small-demo')
const mode = ref<AlgorithmMode>('compare')
const isLoadingDataset = ref(true)
const isRunning = ref(false)
const errorMessage = ref('')
const lastRunAt = ref('Belum ada simulasi')
const benchmarkResult = ref<BenchmarkResponse | null>(null)
const experimentHistory = ref<ExperimentHistoryItem[]>([])
const isRunningBenchmark = ref(false)
const benchmarkError = ref('')
const showDebugGraph = ref(false)
const mapSelectionMode = ref<'source' | 'destination' | null>(null)
const firebaseStatus = ref<FirebaseStatus>({
  enabled: false,
  connected: false,
  mode: 'memory',
  message: 'Firebase belum dikonfigurasi'
})
const benchmarkForm = reactive({
  testCaseCount: 10,
  pairMode: 'random' as BenchmarkPairMode,
  warmupRuns: 1,
  repeatCount: 3,
  randomSeed: 42
})

const sourceNode = computed(() => dataset.value?.nodes.find(node => node.id === sourceId.value))
const destinationNode = computed(() => dataset.value?.nodes.find(node => node.id === destinationId.value))
const selectedDataset = computed(() => datasets.value.find(item => item.id === selectedDatasetId.value))

const activePath = computed(() => {
  if (mode.value === 'standard' || mode.value === 'optimized') return singleResult.value?.path ?? []
  return compareResult.value?.optimized.path ?? []
})

const recentMetric = computed(() => {
  if (compareResult.value) return compareResult.value.optimized
  return singleResult.value
})

const benchmarkCsvUrl = computed(() => {
  const experimentId = benchmarkResult.value?.summary.experimentId
  return experimentId ? api.exportBenchmarkUrl(experimentId) : ''
})

const visibleBenchmarkRuns = computed(() => benchmarkResult.value?.runs.slice(0, 20) ?? [])

const persistenceLabel = computed(() => firebaseStatus.value.connected ? 'Firestore' : 'In memory')

function formatCost(cost: number | null | undefined) {
  if (cost === null || cost === undefined) return '—'
  return cost.toFixed(2)
}

function formatMs(milliseconds: number | undefined) {
  if (milliseconds === undefined) return '—'
  return `${milliseconds < 0.01 ? milliseconds.toFixed(3) : milliseconds.toFixed(2)} ms`
}

function formatPercent(value: number | undefined) {
  if (value === undefined) return '—'
  return `${value >= 0 ? '' : '−'}${Math.abs(value).toFixed(1)}%`
}

function handleDatasetChange(event: Event) {
  const target = event.target as HTMLSelectElement
  selectedDatasetId.value = target.value
  void loadDataset(target.value)
}

function selectMapNode(mode: 'source' | 'destination') {
  mapSelectionMode.value = mapSelectionMode.value === mode ? null : mode
}

function handleMapNodeSelect(nodeId: string) {
  if (mapSelectionMode.value === 'source') sourceId.value = nodeId
  if (mapSelectionMode.value === 'destination') destinationId.value = nodeId
  mapSelectionMode.value = null
  errorMessage.value = ''
}

async function loadDataset(datasetId: string) {
  isLoadingDataset.value = true
  errorMessage.value = ''
  compareResult.value = null
  singleResult.value = null
  benchmarkResult.value = null

  try {
    const loadedDataset = await api.getDataset(datasetId)
    dataset.value = loadedDataset
    sourceId.value = loadedDataset.nodes[0]?.id ?? ''
    destinationId.value = loadedDataset.nodes[loadedDataset.nodes.length - 1]?.id ?? ''
  } catch {
    errorMessage.value = 'Backend belum terhubung. Jalankan FastAPI pada port 8000, lalu muat ulang halaman.'
  } finally {
    isLoadingDataset.value = false
  }
}

async function runSimulation() {
  if (!sourceId.value || !destinationId.value) return
  if (sourceId.value === destinationId.value) {
    errorMessage.value = 'Titik awal dan tujuan harus berbeda untuk simulasi ini.'
    return
  }

  isRunning.value = true
  errorMessage.value = ''

  const payload = {
    datasetId: selectedDatasetId.value,
    sourceId: sourceId.value,
    destinationId: destinationId.value
  }

  try {
    if (mode.value === 'compare') {
      compareResult.value = await api.compare(payload)
      singleResult.value = null
    } else {
      singleResult.value = await api.route(mode.value, payload)
      compareResult.value = null
    }
    lastRunAt.value = new Intl.DateTimeFormat('id-ID', {
      hour: '2-digit',
      minute: '2-digit'
    }).format(new Date())
  } catch {
    errorMessage.value = 'Simulasi gagal dijalankan. Pastikan FastAPI aktif dan source-destination valid.'
  } finally {
    isRunning.value = false
  }
}

function formatDate(value: string | undefined) {
  if (!value) return '—'
  return new Intl.DateTimeFormat('id-ID', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(value))
}

function formatMetric(value: number | undefined, digits = 2) {
  if (value === undefined) return '—'
  return value.toLocaleString('id-ID', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits
  })
}

async function runBenchmark() {
  isRunningBenchmark.value = true
  benchmarkError.value = ''

  try {
    benchmarkResult.value = await api.createBenchmark({
      datasetId: selectedDatasetId.value,
      testCaseCount: benchmarkForm.testCaseCount,
      pairMode: benchmarkForm.pairMode,
      warmupRuns: benchmarkForm.warmupRuns,
      repeatCount: benchmarkForm.repeatCount,
      randomSeed: benchmarkForm.randomSeed,
      tolerance: 1e-9
    })
    experimentHistory.value = await api.listExperiments()
  } catch {
    benchmarkError.value = 'Benchmark gagal dijalankan. Periksa konfigurasi dan pastikan backend aktif.'
  } finally {
    isRunningBenchmark.value = false
  }
}

async function loadExperiment(experimentId: string) {
  benchmarkError.value = ''

  try {
    const experiment = experimentHistory.value.find(item => item.experimentId === experimentId)
    if (experiment && experiment.datasetId !== selectedDatasetId.value) {
      selectedDatasetId.value = experiment.datasetId
      await loadDataset(experiment.datasetId)
    }
    benchmarkResult.value = await api.getBenchmark(experimentId)
  } catch {
    benchmarkError.value = 'Detail eksperimen tidak dapat dimuat. Riwayat benchmark mungkin sudah hilang setelah backend restart.'
  }
}

async function loadExperimentHistory() {
  try {
    experimentHistory.value = await api.listExperiments()
  } catch {
    experimentHistory.value = []
  }
}

async function loadFirebaseStatus() {
  try {
    firebaseStatus.value = await api.getFirebaseStatus()
  } catch {
    firebaseStatus.value = {
      enabled: false,
      connected: false,
      mode: 'memory',
      message: 'Status Firebase tidak tersedia'
    }
  }
}

onMounted(async () => {
  try {
    datasets.value = await api.listDatasets()
    if (datasets.value.length && !datasets.value.some(item => item.id === selectedDatasetId.value)) {
      selectedDatasetId.value = datasets.value[0]?.id ?? 'small-demo'
    }
    await loadDataset(selectedDatasetId.value)
    await loadExperimentHistory()
    await loadFirebaseStatus()
  } catch {
    isLoadingDataset.value = false
    errorMessage.value = 'Backend belum terhubung. Jalankan FastAPI pada port 8000, lalu muat ulang halaman.'
  }
})
</script>

<template>
  <div class="min-h-screen bg-[#f5f7fb] text-slate-900">
    <aside class="fixed inset-y-0 left-0 z-20 hidden w-[244px] flex-col border-r border-slate-200 bg-white px-5 py-6 lg:flex">
      <div class="flex items-center gap-3 px-2">
        <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-lg font-bold text-white shadow-lg shadow-blue-200">
          D
        </div>
        <div>
          <p class="text-sm font-bold tracking-tight text-slate-950">
            Dijkstra Lab
          </p>
          <p class="text-[11px] font-medium text-slate-400">
            Research workspace
          </p>
        </div>
      </div>

      <nav class="mt-10 space-y-1">
        <p class="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-400">
          Workspace
        </p>
        <a
          class="flex items-center gap-3 rounded-xl bg-blue-50 px-3 py-3 text-sm font-semibold text-blue-700"
          href="#simulator"
        ><span class="text-base">⌁</span> Navigation simulator</a>
        <a
          class="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-500 transition hover:bg-slate-50 hover:text-slate-900"
          href="#comparison"
        ><span class="text-base">◈</span> Comparison</a>
        <a
          class="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-500 transition hover:bg-slate-50 hover:text-slate-900"
          href="#benchmark"
        ><span class="text-base">▥</span> Benchmark lab</a>
        <a
          class="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-500 transition hover:bg-slate-50 hover:text-slate-900"
          href="#history"
        ><span class="text-base">↺</span> Experiment history</a>
      </nav>

      <div class="mt-auto rounded-2xl bg-slate-950 p-4 text-white">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold">API status</span>
          <span class="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_0_4px_rgba(52,211,153,0.15)]" />
        </div>
        <p class="mt-2 text-[11px] leading-5 text-slate-400">
          Graph engine ready for isolated algorithm timing.
        </p>
        <p class="mt-3 text-[11px] font-semibold text-emerald-300">
          Persistence: {{ persistenceLabel }}
        </p>
        <p class="mt-3 truncate text-[10px] font-medium text-slate-500">
          {{ apiBase }}
        </p>
      </div>
    </aside>

    <main class="lg:ml-[244px]">
      <header class="sticky top-0 z-10 flex h-[76px] items-center justify-between border-b border-slate-200/80 bg-[#f5f7fb]/90 px-5 backdrop-blur-xl sm:px-8 lg:px-10">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.16em] text-blue-600">
            Dijkstra optimization lab
          </p>
          <h1 class="mt-1 text-xl font-bold tracking-tight text-slate-950 sm:text-2xl">
            Navigation simulator
          </h1>
        </div>
        <div class="flex items-center gap-3">
          <span class="hidden rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-500 sm:inline-flex">Dataset v{{ dataset?.version ?? '—' }}</span>
          <div class="flex h-9 w-9 items-center justify-center rounded-full bg-blue-100 text-xs font-bold text-blue-700">
            ZU
          </div>
        </div>
      </header>

      <div class="mx-auto max-w-[1480px] space-y-6 px-5 py-7 sm:px-8 lg:px-10 lg:py-9">
        <section class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div class="flex items-center justify-between">
              <p class="text-xs font-semibold text-slate-500">
                Active dataset
              </p><span class="rounded-lg bg-blue-50 px-2 py-1 text-xs font-bold text-blue-600">LIVE</span>
            </div><p class="mt-4 text-2xl font-bold tracking-tight text-slate-950">
              {{ dataset?.name ?? 'Loading…' }}
            </p><p class="mt-1 text-xs text-slate-400">
              {{ dataset?.nodeCount ?? 0 }} nodes · {{ dataset?.edgeCount ?? 0 }} edges
            </p>
          </div>
          <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs font-semibold text-slate-500">
              Current route
            </p><p class="mt-4 truncate text-2xl font-bold tracking-tight text-slate-950">
              {{ sourceNode?.name ?? '—' }} <span class="font-normal text-slate-300">→</span>
            </p><p class="mt-1 truncate text-xs text-slate-400">
              {{ destinationNode?.name ?? 'Pilih tujuan' }}
            </p>
          </div>
          <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs font-semibold text-slate-500">
              Latest optimized time
            </p><p class="mt-4 text-2xl font-bold tracking-tight text-slate-950">
              {{ formatMs(compareResult?.optimized.executionTimeMs ?? (mode === 'optimized' ? singleResult?.executionTimeMs : undefined)) }}
            </p><p class="mt-1 text-xs text-emerald-600">
              {{ compareResult ? `${formatPercent(compareResult.improvement.executionTimePct)} vs standard` : 'Run a comparison to measure' }}
            </p>
          </div>
          <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs font-semibold text-slate-500">
              Last activity
            </p><p class="mt-4 text-2xl font-bold tracking-tight text-slate-950">
              {{ lastRunAt }}
            </p><p class="mt-1 text-xs text-slate-400">
              Timing excludes API and render latency
            </p>
          </div>
        </section>

        <section
          id="simulator"
          class="grid gap-6 xl:grid-cols-[minmax(0,1.45fr)_minmax(350px,0.8fr)]"
        >
          <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 px-5 py-4 sm:px-6">
              <div>
                <h2 class="font-bold text-slate-950">
                  Graph visualization
                </h2><p class="mt-1 text-xs text-slate-400">
                  Shortest path ditandai dengan garis biru.
                </p>
              </div><div class="flex items-center gap-3 text-[11px] font-medium text-slate-400">
                <span class="flex items-center gap-1.5"><i class="h-2 w-2 rounded-full bg-blue-600" /> Route</span><span class="flex items-center gap-1.5"><i class="h-2 w-2 rounded-full bg-slate-300" /> Network</span>
              </div>
            </div>
            <div class="relative min-h-[390px] bg-[#fbfcfe] p-4 sm:p-7">
              <div
                v-if="isLoadingDataset"
                class="absolute inset-0 flex items-center justify-center text-sm text-slate-400"
              >
                Memuat graf…
              </div>
              <div
                v-else-if="!dataset"
                class="absolute inset-0 flex items-center justify-center px-8 text-center text-sm text-slate-400"
              >
                Graf belum tersedia. Pastikan backend berjalan.
              </div>
              <RouteMap
                v-else
                :dataset="dataset"
                :path="activePath"
                :source-id="sourceId"
                :destination-id="destinationId"
                :show-debug-graph="showDebugGraph"
                :selection-mode="mapSelectionMode"
                @node-select="handleMapNodeSelect"
              />
              <div
                v-if="dataset"
                class="absolute left-7 top-7 z-[400] flex flex-wrap items-center gap-2"
              >
                <button
                  type="button"
                  class="rounded-lg border border-slate-200 bg-white/95 px-3 py-2 text-xs font-bold text-slate-600 shadow-sm backdrop-blur transition hover:text-blue-700"
                  @click="showDebugGraph = !showDebugGraph"
                >
                  {{ showDebugGraph ? 'Hide graph' : 'Show graph' }}
                </button>
                <span class="rounded-lg bg-white/95 px-3 py-2 text-xs font-semibold text-slate-500 shadow-sm backdrop-blur">
                  {{ dataset.nodeCount }} nodes · {{ dataset.edgeCount }} edges
                </span>
              </div>
              <div
                v-if="mapSelectionMode"
                class="absolute bottom-7 left-1/2 z-[400] -translate-x-1/2 rounded-xl bg-slate-950/95 px-4 py-3 text-center text-xs font-semibold text-white shadow-xl"
              >
                Klik peta untuk memilih {{ mapSelectionMode === 'source' ? 'source' : 'destination' }}
              </div>
            </div>
          </div>

          <div class="space-y-6">
            <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
              <div class="flex items-start justify-between">
                <div>
                  <h2 class="font-bold text-slate-950">
                    Run simulation
                  </h2><p class="mt-1 text-xs leading-5 text-slate-400">
                    Pilih pasangan node dan metode pencarian.
                  </p>
                </div><span class="rounded-lg bg-slate-100 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-500">Single run</span>
              </div>
              <div class="mt-6 space-y-4">
                <label class="block"><span class="mb-2 block text-xs font-semibold text-slate-600">Dataset</span><select
                  :value="selectedDatasetId"
                  class="field-control"
                  @change="handleDatasetChange"
                ><option
                  v-for="datasetItem in datasets"
                  :key="datasetItem.id"
                  :value="datasetItem.id"
                >{{ datasetItem.name }}</option></select></label>
                <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-1 2xl:grid-cols-2">
                  <label class="block"><span class="mb-2 block text-xs font-semibold text-slate-600">Source</span><select
                    v-model="sourceId"
                    class="field-control"
                  ><option
                    v-for="node in dataset?.nodes ?? []"
                    :key="node.id"
                    :value="node.id"
                  >{{ node.name }}</option></select><button
                    type="button"
                    class="mt-2 text-[11px] font-bold text-blue-600 hover:text-blue-700"
                    @click="selectMapNode('source')"
                  >{{ mapSelectionMode === 'source' ? 'Cancel map selection' : 'Choose on map' }}</button></label><label class="block"><span class="mb-2 block text-xs font-semibold text-slate-600">Destination</span><select
                    v-model="destinationId"
                    class="field-control"
                  ><option
                    v-for="node in dataset?.nodes ?? []"
                    :key="node.id"
                    :value="node.id"
                  >{{ node.name }}</option></select><button
                    type="button"
                    class="mt-2 text-[11px] font-bold text-blue-600 hover:text-blue-700"
                    @click="selectMapNode('destination')"
                  >{{ mapSelectionMode === 'destination' ? 'Cancel map selection' : 'Choose on map' }}</button></label>
                </div>
                <div>
                  <span class="mb-2 block text-xs font-semibold text-slate-600">Algorithm mode</span><div class="grid grid-cols-3 gap-2 rounded-xl bg-slate-100 p-1">
                    <button
                      v-for="algorithm in (['standard', 'optimized', 'compare'] as AlgorithmMode[])"
                      :key="algorithm"
                      type="button"
                      class="rounded-lg px-2 py-2 text-[11px] font-bold capitalize transition"
                      :class="mode === algorithm ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-400 hover:text-slate-700'"
                      @click="mode = algorithm"
                    >
                      {{ algorithm }}
                    </button>
                  </div>
                </div>
                <p
                  v-if="errorMessage"
                  class="rounded-xl border border-rose-100 bg-rose-50 px-3 py-2.5 text-xs leading-5 text-rose-600"
                >
                  {{ errorMessage }}
                </p><button
                  type="button"
                  class="flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white shadow-lg shadow-blue-200 transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                  :disabled="isRunning || isLoadingDataset || !dataset"
                  @click="runSimulation"
                >
                  <span
                    v-if="isRunning"
                    class="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white"
                  />{{ isRunning ? 'Running algorithm…' : 'Run shortest path' }}
                </button>
              </div>
            </div>
            <div class="rounded-2xl bg-slate-950 p-5 text-white shadow-sm sm:p-6">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-xs font-semibold text-slate-400">
                    Selected route
                  </p><p class="mt-2 text-lg font-bold">
                    {{ sourceNode?.name ?? '—' }} <span class="text-slate-500">→</span> {{ destinationNode?.name ?? '—' }}
                  </p>
                </div><span
                  v-if="recentMetric?.status === 'success'"
                  class="rounded-full bg-emerald-400/15 px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-emerald-300"
                >Success</span>
              </div><div class="mt-6 grid grid-cols-2 gap-4">
                <div>
                  <p class="text-[10px] uppercase tracking-wider text-slate-500">
                    Total cost
                  </p><p class="mt-1 text-xl font-bold">
                    {{ formatCost(recentMetric?.totalCost) }}
                  </p>
                </div><div>
                  <p class="text-[10px] uppercase tracking-wider text-slate-500">
                    Path length
                  </p><p class="mt-1 text-xl font-bold">
                    {{ recentMetric?.pathLength ?? '—' }} <span class="text-xs font-medium text-slate-500">edges</span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section
          id="comparison"
          class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6"
        >
          <div class="flex flex-wrap items-end justify-between gap-3">
            <div>
              <p class="text-xs font-bold uppercase tracking-[0.16em] text-blue-600">
                Performance snapshot
              </p><h2 class="mt-1 text-xl font-bold tracking-tight text-slate-950">
                Standard vs optimized
              </h2>
            </div><span
              v-if="compareResult"
              class="rounded-full px-3 py-1.5 text-xs font-bold"
              :class="compareResult.correctnessMatch ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600'"
            >{{ compareResult.correctnessMatch ? '✓ Correctness matched' : '× Correctness mismatch' }}</span>
          </div>
          <div
            v-if="compareResult"
            class="mt-6 grid gap-4 md:grid-cols-2"
          >
            <div class="rounded-xl border border-slate-200 p-4">
              <div class="flex items-center justify-between">
                <p class="text-sm font-bold text-slate-700">
                  Standard Dijkstra
                </p><span class="h-2 w-2 rounded-full bg-slate-400" />
              </div><div class="mt-5 grid grid-cols-2 gap-y-5">
                <div>
                  <p class="metric-label">
                    Execution time
                  </p><p class="metric-value">
                    {{ formatMs(compareResult.standard.executionTimeMs) }}
                  </p>
                </div><div>
                  <p class="metric-label">
                    Visited nodes
                  </p><p class="metric-value">
                    {{ compareResult.standard.visitedNodes }}
                  </p>
                </div><div>
                  <p class="metric-label">
                    Processed edges
                  </p><p class="metric-value">
                    {{ compareResult.standard.processedEdges }}
                  </p>
                </div><div>
                  <p class="metric-label">
                    Total cost
                  </p><p class="metric-value">
                    {{ formatCost(compareResult.standard.totalCost) }}
                  </p>
                </div>
              </div>
            </div><div class="rounded-xl border border-blue-100 bg-blue-50/50 p-4">
              <div class="flex items-center justify-between">
                <p class="text-sm font-bold text-blue-700">
                  Optimized Dijkstra
                </p><span class="h-2 w-2 rounded-full bg-blue-600" />
              </div><div class="mt-5 grid grid-cols-2 gap-y-5">
                <div>
                  <p class="metric-label">
                    Execution time
                  </p><p class="metric-value text-blue-700">
                    {{ formatMs(compareResult.optimized.executionTimeMs) }}
                  </p>
                </div><div>
                  <p class="metric-label">
                    Visited nodes
                  </p><p class="metric-value text-blue-700">
                    {{ compareResult.optimized.visitedNodes }}
                  </p>
                </div><div>
                  <p class="metric-label">
                    Processed edges
                  </p><p class="metric-value text-blue-700">
                    {{ compareResult.optimized.processedEdges }}
                  </p>
                </div><div>
                  <p class="metric-label">
                    Total cost
                  </p><p class="metric-value text-blue-700">
                    {{ formatCost(compareResult.optimized.totalCost) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div
            v-else
            class="mt-6 rounded-xl border border-dashed border-slate-200 px-5 py-10 text-center"
          >
            <p class="text-sm font-semibold text-slate-500">
              Belum ada hasil comparison
            </p><p class="mt-1 text-xs text-slate-400">
              Jalankan mode Compare untuk melihat dampak optimasi secara terukur.
            </p>
          </div><div
            v-if="compareResult"
            class="mt-5 grid gap-3 sm:grid-cols-3"
          >
            <div class="rounded-xl bg-slate-50 p-4">
              <p class="metric-label">
                Time improvement
              </p><p class="mt-1 text-lg font-bold text-emerald-600">
                {{ formatPercent(compareResult.improvement.executionTimePct) }}
              </p>
            </div><div class="rounded-xl bg-slate-50 p-4">
              <p class="metric-label">
                Visited reduction
              </p><p class="mt-1 text-lg font-bold text-emerald-600">
                {{ formatPercent(compareResult.improvement.visitedNodesPct) }}
              </p>
            </div><div class="rounded-xl bg-slate-50 p-4">
              <p class="metric-label">
                Edge reduction
              </p><p class="mt-1 text-lg font-bold text-emerald-600">
                {{ formatPercent(compareResult.improvement.processedEdgesPct) }}
              </p>
            </div>
          </div>
        </section>

        <section
          id="benchmark"
          class="grid gap-6 lg:grid-cols-[1fr_0.75fr]"
        >
          <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
            <p class="text-xs font-bold uppercase tracking-[0.16em] text-blue-600">
              Research workflow
            </p><h2 class="mt-1 text-xl font-bold tracking-tight text-slate-950">
              Benchmark lab
            </h2><p class="mt-2 max-w-xl text-sm leading-6 text-slate-500">
              Jalankan pasangan node yang sama berkali-kali untuk memperoleh metrik waktu, node yang dikunjungi, edge yang diproses, dan validasi correctness.
            </p>

            <form
              class="mt-6 space-y-4"
              @submit.prevent="runBenchmark"
            >
              <div class="grid gap-3 sm:grid-cols-2">
                <label class="block"><span class="mb-2 block text-xs font-semibold text-slate-600">Dataset</span><select
                  :value="selectedDatasetId"
                  class="field-control"
                  @change="handleDatasetChange"
                ><option
                  v-for="datasetItem in datasets"
                  :key="datasetItem.id"
                  :value="datasetItem.id"
                >{{ datasetItem.name }}</option></select></label>
                <label class="block"><span class="mb-2 block text-xs font-semibold text-slate-600">Pair mode</span><select
                  v-model="benchmarkForm.pairMode"
                  class="field-control"
                ><option value="random">Random pairs</option><option value="preset">Preset pairs</option></select></label>
              </div>
              <div class="grid gap-3 sm:grid-cols-3">
                <label class="block"><span class="mb-2 block text-xs font-semibold text-slate-600">Test cases</span><input
                  v-model.number="benchmarkForm.testCaseCount"
                  class="field-control"
                  type="number"
                  min="1"
                  max="1000"
                ></label>
                <label class="block"><span class="mb-2 block text-xs font-semibold text-slate-600">Warmup runs</span><input
                  v-model.number="benchmarkForm.warmupRuns"
                  class="field-control"
                  type="number"
                  min="0"
                  max="10"
                ></label>
                <label class="block"><span class="mb-2 block text-xs font-semibold text-slate-600">Repeat / case</span><input
                  v-model.number="benchmarkForm.repeatCount"
                  class="field-control"
                  type="number"
                  min="1"
                  max="50"
                ></label>
              </div>
              <div class="flex flex-wrap items-end gap-3">
                <label class="block w-full sm:w-40"><span class="mb-2 block text-xs font-semibold text-slate-600">Random seed</span><input
                  v-model.number="benchmarkForm.randomSeed"
                  class="field-control"
                  type="number"
                ></label>
                <button
                  type="submit"
                  class="flex min-h-11 flex-1 items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white shadow-lg shadow-blue-200 transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60 sm:flex-none"
                  :disabled="isRunningBenchmark || !datasets.length"
                >
                  <span
                    v-if="isRunningBenchmark"
                    class="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white"
                  />{{ isRunningBenchmark ? 'Running benchmark...' : 'Run benchmark' }}
                </button>
              </div>
            </form>

            <p
              v-if="benchmarkError"
              class="mt-4 rounded-xl border border-rose-100 bg-rose-50 px-3 py-2.5 text-xs leading-5 text-rose-600"
            >
              {{ benchmarkError }}
            </p>

            <div
              v-if="benchmarkResult"
              class="mt-6 border-t border-slate-100 pt-6"
            >
              <div class="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p class="text-xs font-bold uppercase tracking-[0.16em] text-blue-600">
                    Latest result
                  </p>
                  <p class="mt-1 text-sm text-slate-500">
                    {{ benchmarkResult.summary.testCaseCount }} cases · {{ benchmarkResult.summary.repeatCount }} repeats · {{ benchmarkResult.summary.warmupRuns }} warmup
                  </p>
                </div>
                <span
                  class="rounded-full px-3 py-1.5 text-xs font-bold"
                  :class="benchmarkResult.summary.correctnessMismatchCount === 0 ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600'"
                >{{ benchmarkResult.summary.correctnessMismatchCount === 0 ? 'Correctness matched' : `${benchmarkResult.summary.correctnessMismatchCount} mismatch` }}</span>
              </div>

              <div class="mt-5 grid gap-3 sm:grid-cols-3">
                <div class="rounded-xl bg-blue-50 p-4">
                  <p class="metric-label">
                    Time improvement
                  </p>
                  <p class="mt-1 text-lg font-bold text-blue-700">
                    {{ formatPercent(benchmarkResult.summary.improvement.executionTimePct) }}
                  </p>
                </div>
                <div class="rounded-xl bg-slate-50 p-4">
                  <p class="metric-label">
                    Visited reduction
                  </p>
                  <p class="mt-1 text-lg font-bold text-emerald-600">
                    {{ formatPercent(benchmarkResult.summary.improvement.visitedNodesPct) }}
                  </p>
                </div>
                <div class="rounded-xl bg-slate-50 p-4">
                  <p class="metric-label">
                    Edge reduction
                  </p>
                  <p class="mt-1 text-lg font-bold text-emerald-600">
                    {{ formatPercent(benchmarkResult.summary.improvement.processedEdgesPct) }}
                  </p>
                </div>
              </div>

              <div class="mt-5 grid gap-4 sm:grid-cols-2">
                <div class="rounded-xl border border-slate-200 p-4">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-bold text-slate-700">
                      Standard Dijkstra
                    </p><span class="h-2 w-2 rounded-full bg-slate-400" />
                  </div>
                  <div class="mt-4 grid grid-cols-2 gap-4">
                    <div>
                      <p class="metric-label">
                        Mean time
                      </p><p class="metric-value">
                        {{ formatMs(benchmarkResult.summary.standard.meanExecutionTimeMs) }}
                      </p>
                    </div>
                    <div>
                      <p class="metric-label">
                        Median
                      </p><p class="metric-value">
                        {{ formatMs(benchmarkResult.summary.standard.medianExecutionTimeNs / 1000000) }}
                      </p>
                    </div>
                    <div>
                      <p class="metric-label">
                        Visited nodes
                      </p><p class="metric-value">
                        {{ formatMetric(benchmarkResult.summary.standard.meanVisitedNodes) }}
                      </p>
                    </div>
                    <div>
                      <p class="metric-label">
                        Processed edges
                      </p><p class="metric-value">
                        {{ formatMetric(benchmarkResult.summary.standard.meanProcessedEdges) }}
                      </p>
                    </div>
                  </div>
                </div>
                <div class="rounded-xl border border-blue-100 bg-blue-50/50 p-4">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-bold text-blue-700">
                      Optimized Dijkstra
                    </p><span class="h-2 w-2 rounded-full bg-blue-600" />
                  </div>
                  <div class="mt-4 grid grid-cols-2 gap-4">
                    <div>
                      <p class="metric-label">
                        Mean time
                      </p><p class="metric-value text-blue-700">
                        {{ formatMs(benchmarkResult.summary.optimized.meanExecutionTimeMs) }}
                      </p>
                    </div>
                    <div>
                      <p class="metric-label">
                        Median
                      </p><p class="metric-value text-blue-700">
                        {{ formatMs(benchmarkResult.summary.optimized.medianExecutionTimeNs / 1000000) }}
                      </p>
                    </div>
                    <div>
                      <p class="metric-label">
                        Visited nodes
                      </p><p class="metric-value text-blue-700">
                        {{ formatMetric(benchmarkResult.summary.optimized.meanVisitedNodes) }}
                      </p>
                    </div>
                    <div>
                      <p class="metric-label">
                        Processed edges
                      </p><p class="metric-value text-blue-700">
                        {{ formatMetric(benchmarkResult.summary.optimized.meanProcessedEdges) }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-5 flex flex-wrap items-center justify-between gap-3">
                <p class="text-xs text-slate-400">
                  Menampilkan {{ visibleBenchmarkRuns.length }} dari {{ benchmarkResult.runs.length }} raw runs.
                </p>
                <a
                  v-if="benchmarkCsvUrl"
                  :href="benchmarkCsvUrl"
                  class="text-xs font-bold text-blue-600 hover:text-blue-700"
                  download
                >Download CSV</a>
              </div>
              <div class="mt-3 overflow-x-auto rounded-xl border border-slate-200">
                <table class="min-w-full text-left text-xs">
                  <thead class="bg-slate-50 text-[10px] uppercase tracking-wider text-slate-400">
                    <tr>
                      <th class="px-3 py-3 font-bold">
                        Algorithm
                      </th><th class="px-3 py-3 font-bold">
                        Pair
                      </th><th class="px-3 py-3 font-bold">
                        Time
                      </th><th class="px-3 py-3 font-bold">
                        Visited
                      </th><th class="px-3 py-3 font-bold">
                        Status
                      </th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 text-slate-600">
                    <tr
                      v-for="run in visibleBenchmarkRuns"
                      :key="run.id"
                    >
                      <td
                        class="px-3 py-2.5 font-semibold"
                        :class="run.algorithm === 'optimized' ? 'text-blue-600' : 'text-slate-700'"
                      >
                        {{ run.algorithm }}
                      </td>
                      <td class="max-w-40 truncate px-3 py-2.5">
                        {{ run.sourceId }} → {{ run.destinationId }}
                      </td>
                      <td class="px-3 py-2.5">
                        {{ formatMs(run.executionTimeMs) }}
                      </td>
                      <td class="px-3 py-2.5">
                        {{ run.visitedNodes }}
                      </td>
                      <td class="px-3 py-2.5">
                        {{ run.status }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div
            id="history"
            class="rounded-2xl bg-slate-950 p-5 text-white shadow-sm sm:p-6"
          >
            <div class="flex items-center justify-between">
              <h2 class="font-bold">
                Experiment history
              </h2><span class="rounded-full bg-white/10 px-2.5 py-1 text-[10px] font-bold text-slate-400">SESSION</span>
            </div>
            <div
              v-if="!experimentHistory.length"
              class="mt-6 rounded-xl border border-dashed border-white/10 px-4 py-8 text-center"
            >
              <p class="text-sm font-semibold text-slate-400">
                No experiments yet
              </p>
              <p class="mt-1 text-xs leading-5 text-slate-600">
                Hasil benchmark akan muncul di sini selama backend masih berjalan.
              </p>
            </div>
            <div
              v-else
              class="mt-5 space-y-2"
            >
              <button
                v-for="experiment in experimentHistory.slice(0, 8)"
                :key="experiment.experimentId"
                type="button"
                class="w-full rounded-xl border border-white/10 p-3 text-left transition hover:border-blue-400/50 hover:bg-white/5"
                @click="loadExperiment(experiment.experimentId)"
              >
                <div class="flex items-center justify-between gap-3">
                  <span class="truncate text-xs font-bold text-slate-200">{{ experiment.experimentId.slice(0, 12) }}...</span>
                  <span class="text-[10px] text-slate-500">{{ formatDate(experiment.createdAt) }}</span>
                </div>
                <div class="mt-2 flex items-center justify-between gap-3 text-[11px]">
                  <span class="truncate text-slate-500">{{ experiment.datasetId }}</span>
                  <span :class="experiment.correctnessMismatchCount === 0 ? 'text-emerald-400' : 'text-rose-400'">{{ experiment.correctnessMismatchCount === 0 ? 'Matched' : 'Mismatch' }}</span>
                </div>
              </button>
            </div>
            <div class="mt-5 space-y-3 border-t border-white/10 pt-5 text-xs">
              <div class="flex justify-between gap-4">
                <span class="text-slate-500">Dataset aktif</span><span class="truncate font-semibold text-slate-300">{{ selectedDataset?.name ?? '—' }}</span>
              </div>
              <div class="flex justify-between gap-4">
                <span class="text-slate-500">Version</span><span class="font-semibold text-slate-300">{{ dataset?.version ?? '—' }}</span>
              </div>
              <div class="flex justify-between gap-4">
                <span class="text-slate-500">Persistence</span><span
                  class="font-semibold"
                  :class="firebaseStatus.connected ? 'text-emerald-300' : 'text-amber-300'"
                >{{ persistenceLabel }}</span>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>
