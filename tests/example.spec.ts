import { expect, test } from '@nuxt/test-utils/playwright'

test('navigation simulator renders', async ({ page, goto }) => {
  await goto('/', { waitUntil: 'hydration' })
  await expect(page).toHaveTitle(/Dijkstra/)
  await expect(page.getByRole('heading', { name: 'Navigation simulator' })).toBeVisible()
  await expect(page.getByText('Graph visualization')).toBeVisible()
  await expect(page.getByText('Run simulation')).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Benchmark lab' })).toBeVisible()
  await expect(page.getByRole('button', { name: 'Run benchmark' })).toBeVisible()
})
