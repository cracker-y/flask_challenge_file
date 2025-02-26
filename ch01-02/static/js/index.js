const span = document.querySelector("span#switch");
const h3 = document.querySelector(".mt-5");
const h1 = document.querySelector("h1");

span.addEventListener("click", function () {
    let text = span.textContent;
    if (text === "다크모드") {
        document.body.style.backgroundColor = "black";
        // document.textContent.style.color = "black";
        span.style.color = "white";
        h3.style.color = "white";
        h1.style.color = "white";
        span.textContent = "일반모드";
    } else {
        document.body.style.backgroundColor = "white";
        // document.textContent.style.color = "white";
        span.style.color = "black";
        h3.style.color = "black";
        h1.style.color = "black";
        span.textContent = "다크모드";
    }
});


function fetchItem() {
    fetch("/")
        .then((response) => response.json())
        .then((users) => {
            const grid = document.querySelector(".grid");
            grid.innerHTML = "";
            users.forEach((user) => {
                const userItem = document.createElement("div");
                userItem.textContent = `{% if data %} {% for item in data %}
        <div class="flex bg-white rounded-lg shadow-md overflow-hidden">
            <!-- <img src="{{ item.item_img }}" alt="{{ item.product_name }}" class="w-32 h-32 object-cover" /> -->
            <img src="{{ url_for('get_image', filename='image.png')}}" alt="{{ item.product_name }}" class="w-32 h-32 object-cover" />
            <div class="p-4 flex-1">
                <p class="text-sm text-gray-500">{{ item.category }}</p>
                <p class="text-lg font-semibold">{{ item.brand }}</p>
                <p class="text-gray-700">{{ item.product_name }}</p>
                <p class="text-blue-600 font-bold">{{ item.price }}</p>
            </div>
        </div>
        {% endfor %} {% else %}
        <p>상품이 없습니다.</p>
        {% endif %}
        </div>`;
                grid.appendChild(userItem);
            });
        })
        .catch((error) => console.error("Error:", error));
}

