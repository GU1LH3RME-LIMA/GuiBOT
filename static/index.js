document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#enviar");
  const anexo = document.querySelector("#anexo");
  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault(); // impede o reload

      const pergunta = document.querySelector("#pergunta").value;

      const formData = new FormData();
      formData.append("pergunta", pergunta);

      try {
        const response = await fetch("/enviar", {
          method: "POST",
          body: formData
        });

        const data = await response.json();

        if (data.success) {
          document.querySelector("#resposta").value = data.resposta;
          document.querySelector("#pergunta").value = "";
        } else {
          document.querySelector("#resposta").value = "Erro ao processar resposta";
        }
      } catch (error) {
        document.querySelector("#resposta").value = "Erro de comunicação com o servidor";
        console.error("Erro:", error);
      }
    });
  }
if (anexo) {
  anexo.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(anexo); // cria FormData com o conteúdo real do formulário

    try {
      const response = await fetch("/anexar", {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        document.querySelector("#anexado").innerHTML = data.arquivo;
      } else {
        document.querySelector("#anexado").innerHTML = "Erro ao anexar arquivo.";
      }
    } catch (error) {
      document.querySelector("#anexado").innerHTML = "Erro de comunicação com o servidor.";
      console.error("Erro:", error);
    }
  });


  }
});
