// Deliberately minimal: only exists so Chrome/Edge treat the app as installable
// (they require a registered service worker with a fetch handler). It does not
// cache or rewrite anything — every request just goes straight to the network,
// exactly as if there were no service worker at all. Safer than an offline-cache
// version while the app is still changing often; add caching back later only if
// offline support is actually needed, and test it carefully before relying on it.
self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', () => {
  // no respondWith() call — the browser handles the request normally
});
