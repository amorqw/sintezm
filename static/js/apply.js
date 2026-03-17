function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

async function submitForm(form) {
  const resultEl = form.querySelector(".form-result");
  if (resultEl) resultEl.textContent = "??????????…";

  const formData = new FormData(form);
  normalizePhoneField(form, formData);
  if (!validateRequiredFields(form, resultEl)) {
    return;
  }
  const csrf = formData.get("csrfmiddlewaretoken") || getCookie("csrftoken");

  const resp = await fetch(form.action, {
    method: "POST",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrf,
    },
    body: formData,
    credentials: "same-origin",
  });

  const payload = await resp.json().catch(() => null);
  if (!resp.ok || !payload || payload.success !== true) {
    const err = (payload && payload.error) ? payload.error : "?? ??????? ?????????. ?????????? ??? ???.";
    if (resultEl) resultEl.textContent = err;
    return;
  }

  form.reset();
  if (resultEl) resultEl.textContent = "?????? ??????????. ?? ???????? ? ????.";
}

document.addEventListener("submit", (e) => {
  const form = e.target;
  if (!(form instanceof HTMLFormElement)) return;
  if (!form.classList.contains("js-app-form")) return;
  e.preventDefault();
  submitForm(form).catch(() => {
    const resultEl = form.querySelector(".form-result");
    if (resultEl) resultEl.textContent = "?????? ????. ?????????? ??? ???.";
  });
});

function normalizePhoneField(form, formData) {
  const input = form.querySelector('input[name="phone"]');
  if (!input) return;
  const normalized = normalizeRussianPhone(input.value || "");
  input.value = normalized.display;
  formData.set("phone", normalized.raw);
}

function normalizeRussianPhone(value) {
  let digits = (value || "").replace(/\D/g, "");
  if (!digits) {
    return { display: "", raw: "" };
  }

  if (digits[0] === "8") {
    digits = "7" + digits.slice(1);
  } else if (digits[0] === "9") {
    digits = "7" + digits;
  }

  if (digits[0] !== "7") {
    return { display: value, raw: value };
  }

  digits = digits.slice(0, 11);

  const raw = "+7" + digits.slice(1);
  const d = digits;

  let display = "+7";
  if (d.length > 1) {
    display += " (" + d.slice(1, Math.min(4, d.length));
  }
  if (d.length >= 4) {
    display += ")";
  }
  if (d.length >= 5) {
    display += " " + d.slice(4, Math.min(7, d.length));
  }
  if (d.length >= 8) {
    display += "-" + d.slice(7, Math.min(9, d.length));
  }
  if (d.length >= 10) {
    display += "-" + d.slice(9, Math.min(11, d.length));
  }

  return { display, raw };
}

document.addEventListener("input", (e) => {
  const target = e.target;
  if (!(target instanceof HTMLInputElement)) return;
  if (!target.classList.contains("js-phone")) return;

  const { display } = normalizeRussianPhone(target.value || "");
  target.value = display;
});

function validateRequiredFields(form, resultEl) {
  const nameField = form.querySelector('input[name="name"]');
  const phoneField = form.querySelector('input[name="phone"]');
  const emailField = form.querySelector('input[name="email"]');
  let ok = true;

  [nameField, phoneField, emailField].forEach((field) => {
    if (!field) return;
    const wrapper = field.closest(".field");
    if (!wrapper) return;
    wrapper.classList.remove("field-error");
    const msg = wrapper.querySelector(".field-error-message");
    if (msg) msg.remove();
  });

  if (nameField && !nameField.value.trim()) {
    markFieldError(nameField, "??????? ???");
    ok = false;
  }
  if (phoneField && phoneField.value.replace(/\D/g, "").length < 11) {
    markFieldError(phoneField, "??????? ?????????? ???????");
    ok = false;
  }
  if (emailField && !emailField.value.trim()) {
    markFieldError(emailField, "??????? email");
    ok = false;
  }

  if (!ok && resultEl) {
    resultEl.textContent = "????????? ?????????? ????.";
  }
  return ok;
}

function markFieldError(input, message) {
  const wrapper = input.closest(".field");
  if (!wrapper) return;
  wrapper.classList.add("field-error");
  const div = document.createElement("div");
  div.className = "field-error-message";
  div.textContent = message;
  wrapper.appendChild(div);
}

function initNavToggle() {
  const toggle = document.querySelector(".nav-toggle");
  const header = document.querySelector(".site-header");
  if (!toggle || !header) return;

  const closeNav = () => {
    document.body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
  };

  toggle.addEventListener("click", () => {
    const isOpen = document.body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });

  header.querySelectorAll(".nav a").forEach((link) => {
    link.addEventListener("click", closeNav);
  });

  document.addEventListener("click", (event) => {
    if (!document.body.classList.contains("nav-open")) return;
    if (header.contains(event.target)) return;
    closeNav();
  });
}

document.addEventListener("DOMContentLoaded", initNavToggle);

