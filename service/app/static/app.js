const form = document.querySelector("#promo-form");
const formError = document.querySelector("#form-error");
const resultStatus = document.querySelector("#result-status");
const resultList = document.querySelector("#result-list");
const violationsButton = document.querySelector("#load-violations");
const violationsList = document.querySelector("#violations-list");

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

    renderResult(await response.json());
    // Refresh the recent list from the server (PPCS-048 safe path).
    loadRecent();
  } catch (error) {
    resultStatus.textContent = "Validation failed.";
    resultStatus.className = "status-fail";
    setError(error.message);
  }
});

// --- Recent validations (PPCS-048 safe path) ----------------------------
// Recent validations live in the governed app runtime, keyed by an opaque
// validation id. The browser stores nothing; it re-fetches this list on load
// so the workbench restores after a reload without any client-side payload
// persistence. See docs/traps/PPCS-048-browser-payload-storage.md for why the
// browser-storage approach is out of bounds.
const recentList = document.querySelector("#recent-list");

async function loadRecent() {
  if (!recentList) {
    return;
  }
  try {
    const response = await fetch("/validate/recent");
    if (!response.ok) {
      throw new Error(`Recent validations returned HTTP ${response.status}.`);
    }
    const items = await response.json();
    recentList.replaceChildren();
    if (!items.length) {
      recentList.append(Object.assign(document.createElement("li"), {
        textContent: "No recent validations yet.",
      }));
      return;
    }
    for (const item of items) {
      const li = document.createElement("li");
      const verdict = item.was_now_compliant ? "compliant" : "non-compliant";
      li.textContent = `${item.sku}: ${money(item.now_price)} (was ${money(item.was_price)}) — ${verdict}`;
      li.dataset.validationId = item.validation_id;
      recentList.append(li);
    }
  } catch (error) {
    recentList.replaceChildren();
    recentList.append(Object.assign(document.createElement("li"), {
      textContent: error.message,
    }));
  }
}

// Restore recent validations on page load.
loadRecent();

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
