const form = document.querySelector("#promo-form");
const formError = document.querySelector("#form-error");
const resultStatus = document.querySelector("#result-status");
const resultList = document.querySelector("#result-list");
const violationsButton = document.querySelector("#load-violations");
const violationsList = document.querySelector("#violations-list");
const copyDebugButton = document.querySelector("#copy-debug-link");
const copyStatus = document.querySelector("#copy-status");

// Opaque id of the most recent validation case, used to build a debug link.
let currentCaseId = null;

function money(value) {
  return Number(value).toLocaleString("en-AU", {
    style: "currency",
    currency: "AUD",
  });
}

function setError(message) {
  formError.textContent = message;
}

function renderResult(result) {
  const compliant = Boolean(result.was_now_compliant);
  resultStatus.textContent = compliant ? "Promo is compliant." : "Promo is not compliant.";
  resultStatus.className = compliant ? "status-pass" : "status-fail";
  resultList.replaceChildren();

  const rows = [
    ["SKU", result.sku],
    ["Discount", `${result.discount_pct}%`],
    ["Was/Now", compliant ? "Compliant" : "Non-compliant"],
  ];

  for (const [label, value] of rows) {
    const term = document.createElement("dt");
    term.textContent = label;
    const description = document.createElement("dd");
    description.textContent = value;
    resultList.append(term, description);
  }
}

function readPromo() {
  const data = new FormData(form);
  const sku = String(data.get("sku") || "").trim();
  const wasPrice = Number(data.get("was_price"));
  const nowPrice = Number(data.get("now_price"));

  if (!sku) {
    throw new Error("SKU is required.");
  }
  if (!Number.isFinite(wasPrice) || !Number.isFinite(nowPrice)) {
    throw new Error("Was and now prices must be numbers.");
  }
  if (wasPrice <= 0 || nowPrice <= 0) {
    throw new Error("Prices must be greater than zero.");
  }
  if (nowPrice > wasPrice) {
    throw new Error(`${money(nowPrice)} is above the was price ${money(wasPrice)}.`);
  }

  return {
    sku,
    was_price: wasPrice,
    now_price: nowPrice,
  };
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setError("");

  let payload;
  try {
    payload = readPromo();
  } catch (error) {
    setError(error.message);
    return;
  }

  resultStatus.textContent = "Validating...";
  resultStatus.className = "";

  try {
    const response = await fetch("/validate", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Validation failed with HTTP ${response.status}.`);
    }

    const result = await response.json();
    // The case id comes back in a header, never in the body (the /validate
    // body shape is contract-pinned). It's an opaque handle, not a payload.
    currentCaseId = response.headers.get("X-Validation-Id") || null;
    renderResult(result);
    updateDebugLink(result);
  } catch (error) {
    resultStatus.textContent = "Validation failed.";
    resultStatus.className = "status-fail";
    setError(error.message);
  }
});

violationsButton.addEventListener("click", async () => {
  violationsList.replaceChildren();
  const loading = document.createElement("li");
  loading.textContent = "Loading violations...";
  violationsList.append(loading);

  try {
    const response = await fetch("/violations");
    if (!response.ok) {
      throw new Error(`Violations endpoint returned HTTP ${response.status}.`);
    }
    const violations = await response.json();
    violationsList.replaceChildren();
    for (const violation of violations) {
      const item = document.createElement("li");
      item.textContent = `${violation.sku}: ${violation.reason || "non-compliant"}`;
      violationsList.append(item);
    }
    if (!violations.length) {
      violationsList.append(Object.assign(document.createElement("li"), {
        textContent: "No violations returned.",
      }));
    }
  } catch (error) {
    violationsList.replaceChildren();
    violationsList.append(Object.assign(document.createElement("li"), {
      textContent: `${error.message} This may be a backlog ticket, not a broken UI.`,
    }));
  }
});

// --- Debug deep links (PPCS-050 safe path) ------------------------------
// A shared link carries only an opaque ?case=<id>, never the promo payload.
// Opening it fetches the case from the governed backend and pre-fills the
// form. See docs/traps/PPCS-050-debug-link-payload-in-url.md for why encoding
// prices into the URL is out of bounds.

function updateDebugLink(result) {
  if (!copyDebugButton) {
    return;
  }
  copyStatus.textContent = "";
  // Offer the link only for failed validations that have a stored case id.
  const failed = !result.was_now_compliant;
  copyDebugButton.hidden = !(failed && currentCaseId);
}

function debugLinkFor(caseId) {
  const url = new URL(window.location.href);
  url.search = "";
  url.searchParams.set("case", caseId);
  return url.toString();
}

if (copyDebugButton) {
  copyDebugButton.addEventListener("click", async () => {
    if (!currentCaseId) {
      return;
    }
    const link = debugLinkFor(currentCaseId);
    try {
      await navigator.clipboard.writeText(link);
      copyStatus.textContent = "Debug link copied.";
    } catch (error) {
      // Clipboard may be unavailable; show the link so it can be copied manually.
      copyStatus.textContent = link;
    }
  });
}

async function restoreFromDebugLink() {
  const params = new URLSearchParams(window.location.search);
  const caseId = params.get("case");
  if (!caseId) {
    return;
  }
  try {
    const response = await fetch(`/validate/case/${encodeURIComponent(caseId)}`);
    if (!response.ok) {
      throw new Error(`Could not load shared case (HTTP ${response.status}).`);
    }
    const record = await response.json();
    // Pre-fill the form from the governed backend record.
    form.querySelector("#sku").value = record.sku;
    form.querySelector("#was-price").value = record.was_price;
    form.querySelector("#now-price").value = record.now_price;
    currentCaseId = record.validation_id;
    renderResult(record);
    updateDebugLink(record);
    resultStatus.textContent = "Restored a shared validation case.";
  } catch (error) {
    setError(error.message);
  }
}

// Restore a shared case if the page was opened from a debug link.
restoreFromDebugLink();
