(() => {
  "use strict";

  const clean = (s) => String(s ?? "").trim();
  const byId = (id) => document.getElementById(id);

  // Edit these values to match your deployment
  const CONFIG = Object.freeze({
    name: "Genesis-X: GPU-Free LLM Injection",
    tagline: "Instant, permanent LLM knowledge injection on CPU via analytic steering (framework + architecture).",
    githubRepo: "https://github.com/gss1147/Genesis_X",
    canonicalUrl: "https://gss1147.github.io/Genesis_X/",
    notificationMs: 3000
  });

  const shareUrl = (() => {
    const proto = (location && location.protocol) ? String(location.protocol) : "";
    if (proto === "http:" || proto === "https:") return clean(window.location.href);
    return clean(CONFIG.canonicalUrl);
  })();

  const PROJECT = Object.freeze({
    name: clean(CONFIG.name),
    tagline: clean(CONFIG.tagline),
    url: shareUrl,
    githubRepo: clean(CONFIG.githubRepo)
  });

  const notifier = (() => {
    const el = byId("notification");
    let t = null;

    function show(message, color = "rgba(16, 185, 129, 0.92)") {
      if (!el) return;
      el.textContent = message;
      el.style.background = color;
      el.style.display = "block";
      if (t) window.clearTimeout(t);
      t = window.setTimeout(() => {
        el.style.display = "none";
      }, CONFIG.notificationMs);
    }

    return { show };
  })();

  const encode = (s) => encodeURIComponent(String(s ?? ""));

  const safeNavigate = (url) => {
    const target = clean(url);
    const w = window.open(target, "_blank", "noopener,noreferrer");

    if (!w) {
      try {
        window.location.href = target;
        return true;
      } catch {
        return false;
      }
    }
    try { w.opener = null; } catch {}
    return true;
  };

  async function copyToClipboard(text) {
    const warn = "rgba(245, 158, 11, 0.92)";
    const value = clean(text);

    if (!window.isSecureContext || !navigator.clipboard?.writeText) {
      notifier.show("Clipboard not available here. Copy the URL from the address bar.", warn);
      return false;
    }
    try {
      await navigator.clipboard.writeText(value);
      notifier.show("Link copied to clipboard.", "rgba(59, 130, 246, 0.92)");
      return true;
    } catch {
      notifier.show("Could not copy. Copy the URL from the address bar.", warn);
      return false;
    }
  }

  async function tryNativeShare() {
    if (!navigator.share) return false;
    try {
      await navigator.share({
        title: PROJECT.name,
        text: PROJECT.tagline,
        url: PROJECT.url
      });
      notifier.show("Opened system share sheet.", "rgba(59, 130, 246, 0.92)");
      return true;
    } catch {
      return false;
    }
  }

  function shareX() {
    const text = `${PROJECT.name} — ${PROJECT.tagline}`;
    const xUrl = `https://x.com/intent/post?text=${encode(text)}&url=${encode(PROJECT.url)}`;
    const twUrl = `https://twitter.com/intent/tweet?text=${encode(text)}&url=${encode(PROJECT.url)}`;

    const ok = safeNavigate(xUrl);
    if (!ok) safeNavigate(twUrl);

    notifier.show("Opened share composer.", "rgba(59, 130, 246, 0.92)");
  }

  function shareLinkedIn() {
    const url = `https://www.linkedin.com/sharing/share-offsite/?url=${encode(PROJECT.url)}`;
    safeNavigate(url) ? notifier.show("Opened LinkedIn share dialog.", "rgba(59, 130, 246, 0.92)")
                      : notifier.show("Share blocked. Try Copy Link.", "rgba(245, 158, 11, 0.92)");
  }

  function shareReddit() {
    const url = `https://www.reddit.com/submit?url=${encode(PROJECT.url)}&title=${encode(PROJECT.name)}`;
    safeNavigate(url) ? notifier.show("Opened Reddit submission page.", "rgba(59, 130, 246, 0.92)")
                      : notifier.show("Share blocked. Try Copy Link.", "rgba(245, 158, 11, 0.92)");
  }

  function openGitHub() {
    safeNavigate(PROJECT.githubRepo) ? notifier.show("Opened GitHub repository.", "rgba(59, 130, 246, 0.92)")
                                     : notifier.show("Popup blocked. Copy the link instead.", "rgba(245, 158, 11, 0.92)");
  }

  function buildArchitecturePacketMarkdown() {
    return `# ${PROJECT.name} (Architecture Packet)

Developed by Within Us AI (2026)

## Overview
Genesis-X is a theoretical + architectural framework for fast knowledge injection via spectral grafting and analytic weight steering on CPU.

## Core Innovation
**Spectral Grafting**: a zero-gradient weight modification concept intended to encode high-level semantic concepts as preferred activation-space directions.

## Components
1. Omni-Parser: universal ingestion (50+ formats)
2. Knowledge Graph: structure + normalization
3. Singularity Core: analytic steering / graft synthesis
4. LLM Model: quantized runtime with adapters

## Claimed Properties (as presented)
- Training time reduction vs traditional finetuning
- Permanent retention (conceptual goal)
- CPU-only operation (no GPU requirement)
- Broad format support (documents, tabular, scientific, multimedia, geospatial, databases)

## Implementation Notes
- UI: NiceGUI (as listed)
- Runtime: llama.cpp / llama-cpp-python
- Data: docling, pandas, numpy, scipy, openpyxl, etc.

---
Generated from the Genesis-X landing page.
`;
  }

  function downloadArchitecturePacket(buttonEl) {
    const btn = buttonEl || null;
    if (btn) btn.disabled = true;

    try {
      const md = buildArchitecturePacketMarkdown();
      const blob = new Blob([md], { type: "text/markdown;charset=utf-8" });
      const objUrl = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = objUrl;
      a.download = "Genesis-X_Architecture_Packet.md";
      document.body.appendChild(a);
      a.click();
      a.remove();

      URL.revokeObjectURL(objUrl);
      notifier.show("Genesis-X Architecture packet downloaded.");
    } finally {
      window.setTimeout(() => { if (btn) btn.disabled = false; }, 350);
    }
  }

  async function handleAction(action, targetButton) {
    switch (action) {
      case "share-x":
        if (await tryNativeShare()) return;
        shareX();
        return;

      case "share-linkedin":
        if (await tryNativeShare()) return;
        shareLinkedIn();
        return;

      case "share-reddit":
        if (await tryNativeShare()) return;
        shareReddit();
        return;

      case "open-github":
        openGitHub();
        return;

      case "copy-link":
        await copyToClipboard(PROJECT.url);
        return;

      case "download-packet":
        downloadArchitecturePacket(targetButton);
        return;

      default:
        notifier.show("Unknown action.", "rgba(239, 68, 68, 0.92)");
    }
  }

  document.addEventListener("click", async (ev) => {
    const el = ev.target.closest("[data-action]");
    if (!el) return;
    const action = el.getAttribute("data-action");
    if (!action) return;
    ev.preventDefault();
    await handleAction(action, el);
  });

  document.addEventListener("DOMContentLoaded", () => {
    notifier.show("Ready.", "rgba(59, 130, 246, 0.92)");
  });
})();
