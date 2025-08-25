/*

//pre menu/recipe_options integration
document.addEventListener("DOMContentLoaded", () => {
    console.log("Custom script loaded");

    // Utility function to get the CSRF token from cookies
    function getCSRFToken() {
        const name = "csrftoken";
        const cookies = document.cookie.split("; ");
        for (const cookie of cookies) {
            const [key, value] = cookie.split("=");
            if (key === name) return value;
        }
        return null;
    }

    // Async function to fetch AI content
    async function fetchAIContent(formData) {
        try {
            // Placeholder for dynamic content
            const placeholder = document.getElementById("ai-content-placeholder");
            placeholder.innerHTML = "<p>Loading...</p>";

            // Make the POST request
            const response = await fetch("/api/fetch-ai-content/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken(), // Include CSRF token
                },
                body: new URLSearchParams(formData), // Encode form data
            });

            // Process the response
            if (response.ok) {
                const data = await response.json();
                placeholder.innerHTML = `
                    <h3>${data.title}</h3>
                    <p>${data.description}</p>
                    <ul>
                        ${data.ingredients.map((ing) => `<li>${ing}</li>`).join("")}
                    </ul>
                    <ol>
                        ${data.instructions.map((inst) => `<li>${inst}</li>`).join("")}
                    </ol>
                `;
            } else {
                placeholder.innerHTML = "<p>Failed to load content. Please try again.</p>";
            }
        } catch (error) {
            console.error("Error fetching AI content:", error);
            document.getElementById("ai-content-placeholder").innerHTML = "<p>An error occurred.</p>";
        }
    }

    // Attach event listener to the form
    const recipeForm = document.getElementById("recipe-form");
    if (recipeForm) {
        recipeForm.addEventListener("submit", async (event) => {
            event.preventDefault(); // Prevent default form submission
            const formData = new FormData(event.target); // Collect form data
            await fetchAIContent(formData); // Call the async function
        });
    } else {
        console.warn("Recipe form not found");
    }
});


*/

document.addEventListener("DOMContentLoaded", () => {
    console.log("Custom script loaded");

    // Utility function to get the CSRF token from cookies
    function getCSRFToken() {
        const name = "csrftoken";
        const cookies = document.cookie.split("; ");
        for (const cookie of cookies) {
            const [key, value] = cookie.split("=");
            if (key === name) return value;
        }
        return null;
    }

    // Async function to fetch AI content
    async function fetchAIContent(formData) {
        try {
            const response = await fetch("/api/fetch-ai-content/", {
                method: "POST",
                body: formData,
            });
            
            if (!response.ok) throw new Error("Failed to fetch AI content");
    
            const data = await response.json();
            const recipeOptions = data.options || [];
    
            // Update the placeholder with recipe options
            const aiContentPlaceholder = document.getElementById("ai-content-placeholder");
            const recipeOptionsList = document.getElementById("recipe-options-list");
    
            // Clear previous content
            recipeOptionsList.innerHTML = "";
    
            if (recipeOptions.length > 0) {
                recipeOptions.forEach((recipe, index) => {
                    // Create a new recipe item
                    const listItem = document.createElement("li");
                    listItem.className = "recipe-opt-item";
                    listItem.innerHTML = `
                        <a href="#" class="new-recipe-link w-inline-block">
                          <div class="w-layout-blockcontainer recipe-opt w-container">
                            <h2 class="recipe-title">${recipe.title}</h2>
                            <p class="recipe-description">
                              ${recipe.description}<br>(${recipe.time})
                            </p>
                          </div>
                        </a>
                    `;
                    recipeOptionsList.appendChild(listItem);
                });
            } else {
                // Handle empty state
                recipeOptionsList.innerHTML = "<li>No recipe options found. Try refreshing!</li>";
            }
    
            // Show the placeholder
            aiContentPlaceholder.style.display = "block";
    
        } catch (error) {
            console.error("Error fetching AI content:", error);
            alert("An error occurred. Please try again.");
        }
    }

    // Display recipe options dynamically
    function displayRecipeOptions(options) {
        const placeholder = document.getElementById("ai-content-placeholder");
        if (options && options.length > 0) {
            placeholder.innerHTML = `
                <p>See recipe options below or <a href="#" id="edit-ingredients-link">change your ingredients</a>.</p>
                <ul>
                    ${options
                        .map(
                            (option) =>
                                `<li>
                                    <h3>${option.title}</h3>
                                    <p>${option.description}</p>
                                    <a href="${option.detail_url}" class="view-recipe-link">View Full Recipe</a>
                                </li>`
                        )
                        .join("")}
                </ul>
            `;
        } else {
            placeholder.innerHTML = "<p>No recipe options found. Try adjusting your ingredients!</p>";
        }

        // Attach listener to "change your ingredients" link
        const editLink = document.getElementById("edit-ingredients-link");
        if (editLink) {
            editLink.addEventListener("click", (event) => {
                event.preventDefault();
                reopenFormWithPrefilledData();
            });
        }
    }

    // Reopen the form with prefilled data
    function reopenFormWithPrefilledData() {
        const form = document.getElementById("recipe-form");
        const placeholder = document.getElementById("ai-content-placeholder");
        const formDataSnapshot = JSON.parse(localStorage.getItem("formDataSnapshot")) || {};

        // Restore form values
        for (const [key, value] of Object.entries(formDataSnapshot)) {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) input.value = value;
        }

        // Show the form and hide the placeholder
        form.style.display = "block";
        placeholder.style.display = "none";
    }

    // Attach event listener to the form
    const recipeForm = document.getElementById("wf-form-recipegen");
    if (recipeForm) {
        recipeForm.addEventListener("submit", async (event) => {
            event.preventDefault(); // Prevent default form submission
            const formData = new FormData(event.target);

            // Save form data snapshot for reopening later
            const formDataSnapshot = {};
            for (const [key, value] of formData.entries()) {
                formDataSnapshot[key] = value;
            }
            localStorage.setItem("formDataSnapshot", JSON.stringify(formDataSnapshot));

            // Hide the form and fetch AI content
            recipeForm.style.display = "none";
            await fetchAIContent(formData);
        });
    } else {
        console.warn("Recipe form not found");
    }

    const refreshButton = document.getElementById("refresh-options");
    if (refreshButton) {
        refreshButton.addEventListener("click", async () => {
            const formDataSnapshot = JSON.parse(localStorage.getItem("formDataSnapshot"));
            if (formDataSnapshot) {
                const formData = new FormData();
                for (const [key, value] of Object.entries(formDataSnapshot)) {
                    formData.append(key, value);
                }
                await fetchAIContent(formData);
            } else {
                alert("No form data available. Please enter your ingredients again.");
            }
        });
    }
});
