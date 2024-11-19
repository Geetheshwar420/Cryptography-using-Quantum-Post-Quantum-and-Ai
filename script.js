document.getElementById("encrypt-btn").addEventListener("click", () => handleAction("encrypt"));
document.getElementById("decrypt-btn").addEventListener("click", () => handleAction("decrypt"));

async function handleAction(action) {
  const message = document.getElementById("message").value;
  const password = document.getElementById("password").value;
  const type = document.getElementById("type").value;
  const resultField = document.getElementById("result");

  if (!message || !password) {
    resultField.textContent = "Message and password are required!";
    return;
  }

  const url = action === "encrypt" ? "/encrypt" : "/decrypt";
  const payload =
    action === "encrypt"
      ? { message, password, type }
      : { encrypted_message: message, password, type };

  try {
    const response = await fetch(`http://127.0.0.1:5000${url}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (response.ok) {
      resultField.textContent =
        action === "encrypt" ? data.encrypted_message : data.decrypted_message;
    } else {
      resultField.textContent = data.error || "An error occurred!";
    }
  } catch (error) {
    resultField.textContent = "An error occurred!";
  }
}
