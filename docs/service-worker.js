"use strict";

// -----------------------------------------------------------------------------
// Agilearn — slim JupyterLite service worker
//
// This is a trimmed-down variant of thebe-lite's bundled service-worker.js.
// The upstream version intercepts every GET http request and proxies it
// through `fetch()` even when its cache is disabled, which is at best pointless
// overhead and at worst breaks ordinary navigation (Chrome will return
// ERR_CONTENT_LENGTH_MISMATCH for mkdocs-serve responses that get re-fetched
// this way).
//
// We run with `enableCache=false`, so all we actually need the SW to do is:
//   1. respond to the heartbeat that JupyterLite pings to confirm SW health,
//   2. bridge `/api/drive*` BroadcastChannel messages between the in-browser
//      kernel and the host page (this is the piece that makes
//      `self.clients.claim()` worth doing).
//
// Every other fetch is allowed to pass through untouched — we simply do not
// call `respondWith()` — so Material's CSS, the search index, notebook assets,
// etc. are served by the browser directly without any SW round-trip.
// -----------------------------------------------------------------------------

const broadcast = new BroadcastChannel("/api/drive.v1");

self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // Heartbeat — JupyterLite polls this to know the SW is alive.
  if (url.pathname === "/api/service-worker-heartbeat") {
    event.respondWith(new Response("ok"));
    return;
  }

  // Bridge kernel filesystem requests back to the host page via BroadcastChannel.
  if (url.origin === self.location.origin && url.pathname.includes("/api/drive")) {
    event.respondWith(handleBroadcast(event.request));
    return;
  }

  // Everything else: don't call respondWith(), let the browser handle it.
});

async function handleBroadcast(request) {
  const reply = new Promise((resolve) => {
    broadcast.onmessage = (msg) => {
      resolve(new Response(JSON.stringify(msg.data)));
    };
  });
  const payload = await request.json();
  payload.receiver = "broadcast.ts";
  broadcast.postMessage(payload);
  return reply;
}
