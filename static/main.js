
// Get Stripe publishable key

fetch("/product-list")
  .then((result) => result.json())
  .then((data) => {
    const productImagesDiv = document.getElementById("productImages");

    data.data.forEach((product) => {
      const imageUrl = product.metadata.image_url;
      console.log(product);
      if (imageUrl) {
        const cardDiv = document.createElement("div");
        cardDiv.className = "card height h-200";
        cardDiv.style.height = "250px";
        cardDiv.className = "card width w-300";
        cardDiv.style.width = "950px";


        const img = document.createElement("img");
        img.src = imageUrl;
        img.className = "card-img-top mx-auto";
        img.alt = product.name;
        img.style.height = "125px";
        img.style.width = "325px";

        const cardBodyDiv = document.createElement("div");
        cardBodyDiv.className = "card-body";
        cardBodyDiv.style.width = "800px";

        const cardTitle = document.createElement("h4");
        cardTitle.className = "card-title";
        cardTitle.textContent = product.name;
        cardTitle.style.fontSize = "16px";

        const cardText = document.createElement("h1");
        cardText.className = "card-text ";
        cardText.textContent = product.description;
        cardText.style.fontSize = "10px";

        const buyButton = document.createElement("button");
        buyButton.className = "btn btn-primary";
        buyButton.href = "#";
        buyButton.id = "submitBtn"
        buyButton.textContent = "Compre agora";

        fetch("/config")
        .then((result) => { return result.json(); })
        .then((data) => {

          const stripe = Stripe(data.publicKey);

          document.querySelector("#submitBtn").addEventListener("click", () => {
            // Get Checkout Session ID
            fetch("/create-checkout-session")
            .then((result) => { return result.json(); })
            .then((data) => {

              // Redirect to Stripe Checkout
              return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
              console.log(res);
            });
          });
        });


        cardBodyDiv.appendChild(cardTitle);
        cardBodyDiv.appendChild(cardText);
        cardBodyDiv.appendChild(buyButton);

        cardDiv.appendChild(img);
        cardDiv.appendChild(cardBodyDiv);

        productImagesDiv.appendChild(cardDiv);
      }
    });
  });


