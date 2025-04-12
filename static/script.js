document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("uploadForm");
  const resultSection = document.getElementById("resultSection");
  const imageLinks = document.getElementById("imageLinks");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];

    if (!file) {
      alert("PDF 파일을 선택해주세요.");
      return;
    }

    const formData = new FormData();
    formData.append("pdfFile", file);

    try {
      const response = await fetch("/convert", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("서버 오류가 발생했습니다.");
      }

      const result = await response.json();

      // 결과 섹션 초기화
      imageLinks.innerHTML = "";
      resultSection.style.display = "block";

      if (result.images && result.images.length > 0) {
        result.images.forEach((imgUrl, index) => {
          const link = document.createElement("a");
          link.href = imgUrl;
          link.download = `page_${index + 1}.jpg`;
          link.textContent = `이미지 ${index + 1} 다운로드`;
          imageLinks.appendChild(link);
        });
      } else {
        imageLinks.innerHTML = "<p>변환된 이미지가 없습니다.</p>";
      }
    } catch (error) {
      alert("변환 중 오류가 발생했습니다. 다시 시도해주세요.");
      console.error(error);
    }
  });
});
