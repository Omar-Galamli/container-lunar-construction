const canvas = document.getElementById("prototypeCanvas");
const ctx = canvas.getContext("2d");

const state = {
  phase: "deploy",
  fillRate: 3,
  ballastMass: 110000,
  tileEnergy: 8,
  battery: 30,
  survivalLoad: 1,
  fsp: true,
  t: 0,
};

const phases = {
  deploy: { label: "Deploy and survey", code: "00", build: 0.08, fill: 0.05, anchors: 0, berm: 0.05, offset: -0.18 },
  fill: { label: "Fill ballast cells", code: "01", build: 0.12, fill: 0.88, anchors: 0, berm: 0.1, offset: -0.08 },
  anchor: { label: "Anchor platform", code: "02", build: 0.18, fill: 1, anchors: 1, berm: 0.12, offset: 0 },
  construct: { label: "Construct pad tiles", code: "03", build: 0.72, fill: 1, anchors: 1, berm: 0.2, offset: 0 },
  berm: { label: "Shape protective berm", code: "04", build: 0.92, fill: 0.65, anchors: 1, berm: 0.85, offset: 0.1 },
  relocate: { label: "Dump ballast and relocate", code: "05", build: 1, fill: 0.22, anchors: 0.25, berm: 1, offset: 0.24 },
};

const controls = {
  fillRate: document.getElementById("fillRate"),
  ballastMass: document.getElementById("ballastMass"),
  tileEnergy: document.getElementById("tileEnergy"),
  battery: document.getElementById("battery"),
  survivalLoad: document.getElementById("survivalLoad"),
  fspToggle: document.getElementById("fspToggle"),
};

const outs = {
  fillRate: document.getElementById("fillRateOut"),
  ballast: document.getElementById("ballastOut"),
  tileEnergy: document.getElementById("tileEnergyOut"),
  battery: document.getElementById("batteryOut"),
  survival: document.getElementById("survivalOut"),
  fillTime: document.getElementById("fillTime"),
  safetyFactor: document.getElementById("safetyFactor"),
  totalTileEnergy: document.getElementById("totalTileEnergy"),
  energyBalance: document.getElementById("energyBalance"),
  batterySurvival: document.getElementById("batterySurvival"),
  schedule: document.getElementById("schedule"),
  riskList: document.getElementById("riskList"),
  phaseLabel: document.getElementById("phaseLabel"),
  phaseValue: document.getElementById("phaseValue"),
};

function formatNumber(value) {
  return Math.round(value).toLocaleString("en-US");
}

function compute() {
  const lunarGravity = 1.62;
  const frictionCoefficient = 0.8;
  const staticSafetyFactor = 2;
  const lateralLoad = 36;
  const tileCount = 154;
  const dailyDemand = state.fsp ? 380 : 250;
  const availableEnergy = (state.fsp ? 40 * 24 : 0) + 14 * 12;
  const fillTime = state.ballastMass / state.fillRate / 3600;
  const ballastWeight = state.ballastMass * lunarGravity / 1000;
  const designFriction = ballastWeight * frictionCoefficient / staticSafetyFactor;
  const safetyFactor = designFriction / lateralLoad;
  const tileEnergyTotal = tileCount * state.tileEnergy;
  const energyBalance = availableEnergy - dailyDemand;
  const batterySurvival = state.battery / state.survivalLoad;
  const schedule = state.fsp
    ? 50 * (dailyDemand / 380) * Math.max(0.85, state.tileEnergy / 8)
    : 80 * Math.max(1, dailyDemand / 250) * Math.max(1, state.tileEnergy / 8);

  return {
    fillTime,
    ballastWeight,
    designFriction,
    safetyFactor,
    tileEnergyTotal,
    energyBalance,
    batterySurvival,
    schedule,
  };
}

function updateOutputs() {
  const m = compute();
  outs.fillRate.textContent = `${state.fillRate.toFixed(1)} kg/s`;
  outs.ballast.textContent = `${formatNumber(state.ballastMass)} kg`;
  outs.tileEnergy.textContent = `${state.tileEnergy.toFixed(1)} kWh`;
  outs.battery.textContent = `${formatNumber(state.battery)} kWh`;
  outs.survival.textContent = `${state.survivalLoad.toFixed(1)} kW`;
  outs.fillTime.textContent = `${m.fillTime.toFixed(1)} h`;
  outs.safetyFactor.textContent = m.safetyFactor.toFixed(2);
  outs.totalTileEnergy.textContent = `${formatNumber(m.tileEnergyTotal)} kWh`;
  outs.energyBalance.textContent = `${m.energyBalance >= 0 ? "+" : ""}${formatNumber(m.energyBalance)} kWh`;
  outs.energyBalance.style.color = m.energyBalance >= 0 ? "var(--good)" : "var(--bad)";
  outs.batterySurvival.textContent = `${m.batterySurvival.toFixed(0)} h`;
  outs.schedule.textContent = `${m.schedule.toFixed(0)} d`;

  const p = phases[state.phase];
  outs.phaseLabel.textContent = p.label;
  outs.phaseValue.textContent = p.code;

  const risks = [];
  risks.push({
    status: m.safetyFactor >= 2 ? "good" : "bad",
    text: m.safetyFactor >= 2
      ? "Ballast-only stability reaches the current target margin."
      : "Ballast-only stability is below the 2.0 target; anchors remain critical.",
  });
  risks.push({
    status: m.energyBalance >= 0 ? "good" : "bad",
    text: m.energyBalance >= 0
      ? "Daily energy closes under this power scenario."
      : "Daily energy does not close; reduce duty cycle or add power.",
  });
  risks.push({
    status: m.batterySurvival >= 48 ? "good" : "bad",
    text: m.batterySurvival >= 48
      ? "Battery survival reaches the 48 h shadow case at this load."
      : "Battery survival misses the 48 h shadow case at this load.",
  });
  risks.push({
    status: state.fillRate >= 3 ? "good" : "",
    text: state.fillRate >= 3
      ? "Fill throughput matches the current baseline."
      : "Lower fill throughput stretches setup time and needs testing.",
  });

  outs.riskList.innerHTML = risks
    .map((risk) => `<li class="${risk.status}">${risk.text}</li>`)
    .join("");
}

function resizeCanvas() {
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(900, Math.floor(rect.width * dpr));
  canvas.height = Math.max(560, Math.floor(rect.height * dpr));
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function iso(x, y, z = 0, originX, originY, scale) {
  return {
    x: originX + (x - y) * scale,
    y: originY + (x + y) * scale * 0.52 - z * scale,
  };
}

function poly(points, fill, stroke = "rgba(255,255,255,0.12)", width = 1) {
  ctx.beginPath();
  points.forEach((p, index) => {
    if (index === 0) ctx.moveTo(p.x, p.y);
    else ctx.lineTo(p.x, p.y);
  });
  ctx.closePath();
  ctx.fillStyle = fill;
  ctx.fill();
  ctx.strokeStyle = stroke;
  ctx.lineWidth = width;
  ctx.stroke();
}

function line(a, b, color, width = 2) {
  ctx.beginPath();
  ctx.moveTo(a.x, a.y);
  ctx.lineTo(b.x, b.y);
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.lineCap = "round";
  ctx.stroke();
}

function drawBlock(cx, cy, w, d, h, fill, originX, originY, scale) {
  const p1 = iso(cx - w / 2, cy - d / 2, 0, originX, originY, scale);
  const p2 = iso(cx + w / 2, cy - d / 2, 0, originX, originY, scale);
  const p3 = iso(cx + w / 2, cy + d / 2, 0, originX, originY, scale);
  const p4 = iso(cx - w / 2, cy + d / 2, 0, originX, originY, scale);
  const t1 = iso(cx - w / 2, cy - d / 2, h, originX, originY, scale);
  const t2 = iso(cx + w / 2, cy - d / 2, h, originX, originY, scale);
  const t3 = iso(cx + w / 2, cy + d / 2, h, originX, originY, scale);
  const t4 = iso(cx - w / 2, cy + d / 2, h, originX, originY, scale);
  poly([p2, p3, t3, t2], shade(fill, -18), "rgba(0,0,0,0.22)");
  poly([p3, p4, t4, t3], shade(fill, -28), "rgba(0,0,0,0.22)");
  poly([t1, t2, t3, t4], fill, "rgba(255,255,255,0.2)");
}

function shade(hex, amt) {
  const num = parseInt(hex.replace("#", ""), 16);
  const r = Math.max(0, Math.min(255, (num >> 16) + amt));
  const g = Math.max(0, Math.min(255, ((num >> 8) & 255) + amt));
  const b = Math.max(0, Math.min(255, (num & 255) + amt));
  return `rgb(${r}, ${g}, ${b})`;
}

function drawScene() {
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  ctx.clearRect(0, 0, w, h);

  const gradient = ctx.createLinearGradient(0, 0, 0, h);
  gradient.addColorStop(0, "#111821");
  gradient.addColorStop(0.55, "#151312");
  gradient.addColorStop(1, "#2a261f");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, w, h);

  const originX = w * 0.49;
  const originY = h * 0.34;
  const scale = Math.min(w / 42, h / 26);
  const phase = phases[state.phase];
  const pulse = (Math.sin(state.t * 0.04) + 1) / 2;

  drawStars(w, h);
  drawGround(originX, originY, scale, w, h);
  drawPad(originX, originY, scale, phase.build);
  drawBerm(originX, originY, scale, phase.berm);
  drawContainer(originX, originY, scale, phase.fill, phase.offset, pulse);
  drawLabels(originX, originY, scale);
}

function drawStars(w, h) {
  ctx.fillStyle = "rgba(255,255,255,0.72)";
  for (let i = 0; i < 90; i += 1) {
    const x = (i * 127) % w;
    const y = (i * 53) % Math.max(180, h * 0.42);
    const r = i % 9 === 0 ? 1.5 : 0.8;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawGround(originX, originY, scale, w, h) {
  const a = iso(-17, -11, 0, originX, originY, scale);
  const b = iso(17, -11, 0, originX, originY, scale);
  const c = iso(20, 12, 0, originX, originY, scale);
  const d = iso(-20, 12, 0, originX, originY, scale);
  poly([a, b, c, d], "#6f685c", "rgba(255,255,255,0.08)");

  ctx.strokeStyle = "rgba(255,255,255,0.06)";
  ctx.lineWidth = 1;
  for (let i = -16; i <= 16; i += 2) {
    line(iso(i, -10, 0.01, originX, originY, scale), iso(i, 11, 0.01, originX, originY, scale), "rgba(255,255,255,0.05)", 1);
    line(iso(-16, i / 1.4, 0.01, originX, originY, scale), iso(17, i / 1.4, 0.01, originX, originY, scale), "rgba(255,255,255,0.04)", 1);
  }
}

function drawPad(originX, originY, scale, build) {
  const radius = 7;
  const tile = 1;
  let drawn = 0;
  const total = 154;
  const limit = Math.floor(total * build);

  for (let y = -6.5; y <= 6.5; y += tile) {
    for (let x = -6.5; x <= 6.5; x += tile) {
      if (Math.hypot(x + 0.5, y + 0.5) <= radius) {
        drawn += 1;
        if (drawn > limit) continue;
        const p1 = iso(x, y, 0.05, originX, originY, scale);
        const p2 = iso(x + tile * 0.92, y, 0.05, originX, originY, scale);
        const p3 = iso(x + tile * 0.92, y + tile * 0.92, 0.05, originX, originY, scale);
        const p4 = iso(x, y + tile * 0.92, 0.05, originX, originY, scale);
        const shadeShift = (drawn % 5) * 5;
        poly([p1, p2, p3, p4], `rgb(${195 + shadeShift}, ${198 + shadeShift}, ${190 + shadeShift})`, "rgba(80,80,80,0.28)", 0.8);
      }
    }
  }

  ctx.beginPath();
  for (let i = 0; i <= 80; i += 1) {
    const a = (Math.PI * 2 * i) / 80;
    const p = iso(Math.cos(a) * radius, Math.sin(a) * radius, 0.08, originX, originY, scale);
    if (i === 0) ctx.moveTo(p.x, p.y);
    else ctx.lineTo(p.x, p.y);
  }
  ctx.strokeStyle = "rgba(255,255,255,0.32)";
  ctx.lineWidth = 2;
  ctx.stroke();
}

function drawBerm(originX, originY, scale, amount) {
  if (amount <= 0) return;
  const outer = 12;
  const inner = 9;
  const segments = 84;
  for (let i = 0; i < segments * amount; i += 1) {
    const a1 = (Math.PI * 2 * i) / segments;
    const a2 = (Math.PI * 2 * (i + 0.8)) / segments;
    const p1 = iso(Math.cos(a1) * inner, Math.sin(a1) * inner, 0.12, originX, originY, scale);
    const p2 = iso(Math.cos(a2) * inner, Math.sin(a2) * inner, 0.12, originX, originY, scale);
    const p3 = iso(Math.cos(a2) * outer, Math.sin(a2) * outer, 0.55 + amount * 0.55, originX, originY, scale);
    const p4 = iso(Math.cos(a1) * outer, Math.sin(a1) * outer, 0.55 + amount * 0.55, originX, originY, scale);
    poly([p1, p2, p3, p4], i % 2 ? "#a18257" : "#927246", "rgba(35,28,20,0.36)", 0.6);
  }
}

function drawContainer(originX, originY, scale, fill, offset, pulse) {
  const cx = -2 + offset * 8;
  const cy = -9 + offset * 5;
  drawShadow(cx, cy, 8, 4.6, originX, originY, scale);

  drawBlock(cx, cy, 6.6, 3.4, 0.65, "#5db6be", originX, originY, scale);
  drawBlock(cx, cy, 5.8, 2.6, 0.7 + fill * 1.25, "#427e86", originX, originY, scale);

  for (let i = 0; i < 12; i += 1) {
    const row = Math.floor(i / 4);
    const col = i % 4;
    const cellX = cx - 2.25 + col * 1.5;
    const cellY = cy - 0.85 + row * 0.85;
    drawBlock(cellX, cellY, 1.1, 0.48, 0.72 + fill * (0.28 + (i % 3) * 0.04), "#b08b58", originX, originY, scale);
  }

  drawGantry(cx, cy, originX, originY, scale, pulse);
  drawAnchors(cx, cy, originX, originY, scale, phases[state.phase].anchors);
  drawIntake(cx, cy, originX, originY, scale, fill);
  drawWheels(cx, cy, originX, originY, scale);
}

function drawShadow(cx, cy, w, d, originX, originY, scale) {
  const p1 = iso(cx - w / 2, cy - d / 2, -0.05, originX, originY, scale);
  const p2 = iso(cx + w / 2, cy - d / 2, -0.05, originX, originY, scale);
  const p3 = iso(cx + w / 2, cy + d / 2, -0.05, originX, originY, scale);
  const p4 = iso(cx - w / 2, cy + d / 2, -0.05, originX, originY, scale);
  poly([p1, p2, p3, p4], "rgba(0,0,0,0.28)", "rgba(0,0,0,0)");
}

function drawGantry(cx, cy, originX, originY, scale, pulse) {
  const z = 2.75;
  const corners = [
    [cx - 3.6, cy - 2.1],
    [cx + 3.6, cy - 2.1],
    [cx + 3.6, cy + 2.1],
    [cx - 3.6, cy + 2.1],
  ];
  corners.forEach(([x, y]) => {
    line(iso(x, y, 0.6, originX, originY, scale), iso(x, y, z, originX, originY, scale), "#c8d3d3", 3);
  });
  line(iso(cx - 3.8, cy - 2.3, z, originX, originY, scale), iso(cx + 3.8, cy - 2.3, z, originX, originY, scale), "#d8dfdd", 4);
  line(iso(cx - 3.8, cy + 2.3, z, originX, originY, scale), iso(cx + 3.8, cy + 2.3, z, originX, originY, scale), "#d8dfdd", 4);
  const toolX = cx - 2.6 + pulse * 5.2;
  line(iso(toolX, cy - 2.35, z + 0.05, originX, originY, scale), iso(toolX, cy + 2.35, z + 0.05, originX, originY, scale), "#f0c96d", 3);
  drawBlock(toolX, cy, 0.45, 0.55, 0.8, "#d9b15f", originX, originY, scale);
}

function drawAnchors(cx, cy, originX, originY, scale, amount) {
  const points = [
    [cx - 4.2, cy - 2.6], [cx + 4.2, cy - 2.6], [cx + 4.2, cy + 2.6], [cx - 4.2, cy + 2.6],
    [cx - 2.8, cy - 2.9], [cx + 2.8, cy - 2.9], [cx + 2.8, cy + 2.9], [cx - 2.8, cy + 2.9],
  ];
  points.forEach(([x, y]) => {
    const top = iso(x, y, 0.3, originX, originY, scale);
    const bottom = iso(x, y, -0.6 * amount, originX, originY, scale);
    line(top, bottom, amount > 0.5 ? "#d9b15f" : "rgba(217,177,95,0.4)", 3);
    ctx.beginPath();
    ctx.arc(top.x, top.y, 5, 0, Math.PI * 2);
    ctx.fillStyle = "#d9b15f";
    ctx.fill();
  });
}

function drawIntake(cx, cy, originX, originY, scale, fill) {
  const bladeA = iso(cx - 4.6, cy - 0.7, 0.25, originX, originY, scale);
  const bladeB = iso(cx - 6.4, cy - 0.7, 0.05, originX, originY, scale);
  const bladeC = iso(cx - 6.4, cy + 0.8, 0.05, originX, originY, scale);
  const bladeD = iso(cx - 4.6, cy + 0.8, 0.25, originX, originY, scale);
  poly([bladeA, bladeB, bladeC, bladeD], "#c2b38e", "rgba(255,255,255,0.16)", 1);
  line(iso(cx - 4.4, cy, 0.8, originX, originY, scale), iso(cx - 1.6, cy, 2.1, originX, originY, scale), "#aeb5b6", 5);
  if (state.phase === "fill") {
    for (let i = 0; i < 7; i += 1) {
      const p = iso(cx - 5.8 + i * 0.5, cy + Math.sin(state.t * 0.08 + i) * 0.2, 0.18 + fill * 0.4, originX, originY, scale);
      ctx.beginPath();
      ctx.arc(p.x, p.y, 2.5, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(217,177,95,0.8)";
      ctx.fill();
    }
  }
}

function drawWheels(cx, cy, originX, originY, scale) {
  [[-3, -2.1], [3, -2.1], [3, 2.1], [-3, 2.1]].forEach(([dx, dy]) => {
    const p = iso(cx + dx, cy + dy, 0.18, originX, originY, scale);
    ctx.beginPath();
    ctx.ellipse(p.x, p.y, 10, 6, 0.35, 0, Math.PI * 2);
    ctx.fillStyle = "#1f2528";
    ctx.fill();
    ctx.strokeStyle = "#6f7779";
    ctx.lineWidth = 2;
    ctx.stroke();
  });
}

function drawLabels(originX, originY, scale) {
  const labels = [
    ["14 m pad", 0, 0, 0.2],
    ["5 m stand-off berm", 10.5, 1, 1.2],
    ["12 ballast cells", -2, -9, 3.4],
    ["8 helical anchors", 4, -12, 0.7],
  ];
  ctx.font = "700 13px Inter, sans-serif";
  ctx.textAlign = "center";
  labels.forEach(([text, x, y, z]) => {
    const p = iso(x, y, z, originX, originY, scale);
    ctx.fillStyle = "rgba(17,18,20,0.72)";
    const width = ctx.measureText(text).width + 16;
    ctx.fillRect(p.x - width / 2, p.y - 22, width, 24);
    ctx.strokeStyle = "rgba(255,255,255,0.14)";
    ctx.strokeRect(p.x - width / 2, p.y - 22, width, 24);
    ctx.fillStyle = "#f3f1ec";
    ctx.fillText(text, p.x, p.y - 6);
  });
}

function bindControls() {
  document.querySelectorAll(".phase-button").forEach((button) => {
    button.addEventListener("click", () => {
      state.phase = button.dataset.phase;
      document.querySelectorAll(".phase-button").forEach((b) => b.classList.remove("is-active"));
      button.classList.add("is-active");
      updateOutputs();
    });
  });

  controls.fillRate.addEventListener("input", (e) => {
    state.fillRate = Number(e.target.value);
    updateOutputs();
  });
  controls.ballastMass.addEventListener("input", (e) => {
    state.ballastMass = Number(e.target.value);
    updateOutputs();
  });
  controls.tileEnergy.addEventListener("input", (e) => {
    state.tileEnergy = Number(e.target.value);
    updateOutputs();
  });
  controls.battery.addEventListener("input", (e) => {
    state.battery = Number(e.target.value);
    updateOutputs();
  });
  controls.survivalLoad.addEventListener("input", (e) => {
    state.survivalLoad = Number(e.target.value);
    updateOutputs();
  });
  controls.fspToggle.addEventListener("change", (e) => {
    state.fsp = e.target.checked;
    updateOutputs();
  });
}

function tick() {
  state.t += 1;
  drawScene();
  requestAnimationFrame(tick);
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
bindControls();
updateOutputs();
tick();

