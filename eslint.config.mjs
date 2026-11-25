// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt(
  {
    name: 'project/ignores',
    ignores: [
      'backend/**',
      '.venv/**',
      '**/.venv/**',
      '.output/**'
    ]
  }
)
