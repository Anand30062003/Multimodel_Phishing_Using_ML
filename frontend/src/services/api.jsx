export async function checkPhishing(url, text, image) {
  const formData = new FormData();
  formData.append("url", url);
  formData.append("text", text);
  if (image) formData.append("image", image);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/check",
      {
        method: "POST",
        body: formData,
      }
    );

    return await response.json();
  } catch (error) {
    return {
      result: "ERROR",
      score: 0,
      message: "Server connection failed",
    };
  }
}
