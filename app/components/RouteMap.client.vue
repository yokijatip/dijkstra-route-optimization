<script setup lang="ts">
import * as L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { DatasetDetail } from '~/types/api'

const props = withDefaults(defineProps<{
  dataset: DatasetDetail
  path: string[]
  sourceId: string
  destinationId: string
  showDebugGraph?: boolean
  selectionMode?: 'source' | 'destination' | null
}>(), {
  showDebugGraph: false,
  selectionMode: null
})

const emit = defineEmits<{
  nodeSelect: [nodeId: string]
}>()

const mapElement = ref<HTMLElement | null>(null)
let map: L.Map | null = null
let networkLayer: L.LayerGroup | null = null
let routeLayer: L.LayerGroup | null = null
let markerLayer: L.LayerGroup | null = null

const nodesWithCoordinates = computed(() => props.dataset.nodes.filter(node => (
  typeof node.latitude === 'number' && typeof node.longitude === 'number'
)))

const nodeById = computed(() => new Map(props.dataset.nodes.map(node => [node.id, node])))

function nodeLatLng(nodeId: string) {
  const node = nodeById.value.get(nodeId)
  if (!node || typeof node.latitude !== 'number' || typeof node.longitude !== 'number') return null
  return L.latLng(node.latitude, node.longitude)
}

function nearestNodeId(latitude: number, longitude: number) {
  let nearestId = ''
  let nearestDistance = Number.POSITIVE_INFINITY

  for (const node of nodesWithCoordinates.value) {
    const latitudeDistance = node.latitude! - latitude
    const longitudeDistance = node.longitude! - longitude
    const distance = latitudeDistance ** 2 + longitudeDistance ** 2
    if (distance < nearestDistance) {
      nearestDistance = distance
      nearestId = node.id
    }
  }

  return nearestId
}

function clearLayers() {
  networkLayer?.clearLayers()
  routeLayer?.clearLayers()
  markerLayer?.clearLayers()
}

function renderLayers() {
  if (!map || !networkLayer || !routeLayer || !markerLayer) return

  clearLayers()

  if (props.showDebugGraph) {
    for (const edge of props.dataset.edges) {
      const from = nodeLatLng(edge.from)
      const to = nodeLatLng(edge.to)
      if (!from || !to) continue
      L.polyline([from, to], {
        color: '#cbd5e1',
        opacity: 0.65,
        weight: 2
      }).addTo(networkLayer)
    }
  }

  const routeCoordinates = props.path
    .map(nodeId => nodeLatLng(nodeId))
    .filter((coordinate): coordinate is L.LatLng => coordinate !== null)

  if (routeCoordinates.length > 1) {
    L.polyline(routeCoordinates, {
      color: '#2563eb',
      opacity: 0.95,
      weight: 6,
      lineCap: 'round',
      lineJoin: 'round'
    }).addTo(routeLayer)
  }

  const source = nodeLatLng(props.sourceId)
  if (source) {
    L.circleMarker(source, {
      radius: 9,
      color: '#047857',
      weight: 4,
      fillColor: '#34d399',
      fillOpacity: 1
    }).bindTooltip('Source').addTo(markerLayer)
  }

  const destination = nodeLatLng(props.destinationId)
  if (destination) {
    L.circleMarker(destination, {
      radius: 9,
      color: '#be123c',
      weight: 4,
      fillColor: '#fb7185',
      fillOpacity: 1
    }).bindTooltip('Destination').addTo(markerLayer)
  }
}

function initializeMap() {
  if (!mapElement.value || map) return

  map = L.map(mapElement.value, {
    zoomControl: true,
    attributionControl: true
  })

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
  }).addTo(map)

  networkLayer = L.layerGroup().addTo(map)
  routeLayer = L.layerGroup().addTo(map)
  markerLayer = L.layerGroup().addTo(map)

  map.on('click', (event) => {
    if (!props.selectionMode) return
    const nodeId = nearestNodeId(event.latlng.lat, event.latlng.lng)
    if (nodeId) emit('nodeSelect', nodeId)
  })

  const bounds = nodesWithCoordinates.value.map(node => [node.latitude!, node.longitude!] as [number, number])
  if (bounds.length) map.fitBounds(bounds, { padding: [24, 24] })
  renderLayers()
  window.setTimeout(() => map?.invalidateSize(), 0)
}

function refreshMap() {
  if (!map) {
    initializeMap()
    return
  }
  renderLayers()
}

watch(
  () => [props.dataset.id, props.path, props.sourceId, props.destinationId, props.showDebugGraph],
  () => nextTick(refreshMap),
  { deep: true }
)

watch(
  () => props.selectionMode,
  (selectionMode) => {
    if (mapElement.value) mapElement.value.style.cursor = selectionMode ? 'crosshair' : ''
  }
)

onMounted(() => nextTick(initializeMap))

onBeforeUnmount(() => {
  map?.remove()
  map = null
})
</script>

<template>
  <div
    ref="mapElement"
    class="route-map h-full min-h-[350px] w-full"
    :aria-label="selectionMode ? 'Klik peta untuk memilih node' : 'Peta jaringan jalan dan rute terpendek'"
  />
</template>

<style scoped>
.route-map {
  background: #e2e8f0;
  min-height: 350px;
  z-index: 0;
}

.route-map :deep(.leaflet-control-attribution) {
  font-size: 10px;
}
</style>
