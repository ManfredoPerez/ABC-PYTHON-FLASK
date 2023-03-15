const userForm = document.querySelector("#userForm");

let users = [];
let editing = false;
let userId = null;

window.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("/api/users");
  const data = await response.json();
  users = data;
  renderUser(users);
});

userForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const descripcion = userForm["descripcion"].value;
  const precio = userForm["precio"].value;
  const cantidad = userForm["cantidad"].value;
  const categoria = userForm["categoria"].value;
  const descripcion_categoria = userForm["descripcion_categoria"].value;

  if (!editing) {
    // send user to backend
    const response = await fetch("/api/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        descripcion,
        precio,
        cantidad,
        categoria, 
        descripcion_categoria,
      }),
    });

    const data = await response.json();
    users.push(data);
    renderUser(users);
  } else {
    const response = await fetch(`/api/users/${userId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        descripcion,
        precio,
        cantidad,
        categoria, 
        descripcion_categoria,
      }),
    });
    const updatedUser = await response.json();

    users = users.map((user) =>
      user.id === updatedUser.id ? updatedUser : user
    );
    console.log(users)
    renderUser(users);

    editing = false;
    userId = null;
  }
  userForm.reset();
});

function renderUser(users)  {
  const userList = document.querySelector("#userList");
  userList.innerHTML = "";
  users.forEach((user) => {
    const userItem = document.createElement("li");
    userItem.classList = "list-group-item list-group-item-danger my-2";
    userItem.innerHTML = `
      <div class="container">  
          <header class="d-flex justify-content-between ">
            <h4>Descripcion: ${user.descripcion}</h4>
            <div>
              <button data-id="${user.id}" class="btn-delete btn btn-danger btn-sm">Delete</button>
              <button data-id="${user.id}" class="btn-edit btn btn-secondary btn-sm">Edit</button>
            </div>
          </header>
          <h5>Precio: ${user.precio}</h5>
          <h5>Cantidad: ${user.cantidad}</h5>
          <h5>Categoria: ${user.categoria}</h5>
          <h5 class="text-truncate">${user.descripcion_categoria}</h5>
        </div>  
    `;

    // Handle delete button
    const btnDelete = userItem.querySelector(".btn-delete");

    btnDelete.addEventListener("click", async (e) => {
      const response = await fetch(`/api/users/${user.id}`, {
        method: "DELETE",
      });

      const data = await response.json();

      users = users.filter((user) => user.id !== data.id);
      renderUser(users);
    });

    userList.appendChild(userItem);

    // Handle edit button
    const btnEdit = userItem.querySelector(".btn-edit");

    btnEdit.addEventListener("click", async (e) => {
      const response = await fetch(`/api/users/${user.id}`);
      const data = await response.json();

      userForm["descripcion"].value = data.descripcion;
      userForm["precio"].value = data.precio;
      userForm["cantidad"].value = data.cantidad;
      userForm["categoria"].value = data.categoria;
      userForm["descripcion_categoria"].value = data.descripcion_categoria;

      editing = true;
      userId = user.id;
    });
  });
}