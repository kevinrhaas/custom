import { defineConfig } from 'vite';

// The game is published under /custom/joliet/app/ on GitHub Pages (the `custom`
// repo publishes only site/). Base is relative so the same bundle also works
// from a local `vite preview` and from artifacts/ during the shot harness.
export default defineConfig({
  base: './',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    target: 'es2022',
    assetsInlineLimit: 0,
    chunkSizeWarningLimit: 6000,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('@babylonjs')) return 'babylon';
          return undefined;
        },
      },
    },
  },
  server: { port: 5173, host: true },
});
