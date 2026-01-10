const BASE_URL = "http://127.0.0.1:8000";

export async function checkHealth() {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) throw new Error("Backend not reachable");
  return res.json();
}

export async function startDetection() {
  const res = await fetch(`${BASE_URL}/start`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to start detection");
  return res.json();
}

export async function stopDetection() {
  const res = await fetch(`${BASE_URL}/stop`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to stop detection");
  return res.json();
}

export async function getStatus() {
  const res = await fetch(`${BASE_URL}/status`);
  if (!res.ok) throw new Error("Failed to fetch status");
  return res.json();
}
