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

  renderFailures(result.failures);
}

function renderFailures(failures) {
  if (!Array.isArray(failures) || failures.length === 0) {
    return;
  }
  const term = document.createElement("dt");
  term.textContent = "Why it failed";
  const description = document.createElement("dd");
  const list = document.createElement("ul");
  list.className = "reasons";
  for (const failure of failures) {
    const item = document.createElement("li");
    // Prefer the human-readable message; fall back to the stable reason code.
    item.textContent = failure.message || failure.reason_code || failure.rule_id;
    item.dataset.ruleId = failure.rule_id || "";
    item.dataset.reasonCode = failure.reason_code || "";
    list.append(item);
  }
  description.append(list);
  resultList.append(term, description);
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
