// skins.js — the style picker's catalogue. Each id has a matching block in
// css/skins.css. `swatch` is [page, card, accent, print] for the preview tile.
// To add Lauren's own look: copy a block in skins.css, rename it, add it here.

export const SKINS = [
  { id: 'heirloom', name: 'Heirloom', note: 'Linen paper, old prints, ink-brown type', swatch: ['#f3ece0', '#fbf7f0', '#8a4b2a', '#fffdf8'], font: 'serif' },
  { id: 'gallery', name: 'Gallery', note: 'A quiet, modern museum wall', swatch: ['#fafaf8', '#ffffff', '#16161a', '#e3e3de'], font: 'sans' },
  { id: 'evening', name: 'Evening', note: 'Candlelight, velvet and gold', swatch: ['#16121d', '#231c2e', '#d9b56c', '#3a2f4a'], font: 'serif', prefers: 'dark' },
  { id: 'garden', name: 'Garden', note: 'Sage, cream and soft sunshine', swatch: ['#eef1e6', '#fbfcf6', '#4d6b45', '#c9902b'], font: 'serif' },
  { id: 'postcard', name: 'Postcard', note: 'Sixties color: mustard, teal, tomato', swatch: ['#f6ead2', '#fff7e8', '#b8431f', '#1f7f86'], font: 'sans' },
  { id: 'clear', name: 'Clear view', note: 'Highest contrast, easiest to read', swatch: ['#ffffff', '#ffffff', '#0040c8', '#000000'], font: 'sans' },
];

export const THEME_COLOR = {
  heirloom: { light: '#f3ece0', dark: '#1d1712' },
  gallery: { light: '#fafaf8', dark: '#111113' },
  evening: { light: '#f4eef3', dark: '#16121d' },
  garden: { light: '#eef1e6', dark: '#141a12' },
  postcard: { light: '#f6ead2', dark: '#1d2a2b' },
  clear: { light: '#ffffff', dark: '#000000' },
};
